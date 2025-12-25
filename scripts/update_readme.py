#!/usr/bin/env python3
"""
OpenJobs - Job Aggregator Script
Fetches job listings from XML source and generates README.md and HTML pages.
Supports auto-discovery of latest data sources and smart job rotation.
"""

import xml.etree.ElementTree as ET
import urllib.request
import urllib.error
from datetime import datetime, timezone
from collections import Counter
import re
import os
import sys
import logging
import json

# =============================================================================
# CONFIGURATION
# =============================================================================

class Config:
    """Configuration settings for the job aggregator."""

    # Data source
    SITEMAP_URL = "https://www.openjobs-ai.com/xml/sitemap.xml"
    DEFAULT_LOGO = "https://www.openjobs-ai.com/logo.png"

    # Output paths
    README_PATH = "README.md"
    HTML_PATH = "public/index.html"
    CF_SITEMAP_PATH = "public/sitemap.xml"
    GH_SITEMAP_PATH = "sitemap.xml"
    STATS_PATH = "public/stats.json"

    # Display settings
    JOBS_PER_PAGE = 200
    HTML_JOBS_COUNT = 50
    ROTATION_HOURS = 6

    # Site URLs
    CF_SITE_URL = "https://openjobs.genedai.me"
    GH_SITE_URL = "https://digidai.github.io/openjobs"

    # Request settings
    USER_AGENT = "Mozilla/5.0 (compatible; OpenJobs/1.0)"
    REQUEST_TIMEOUT = 30
    MAX_RETRIES = 3


# =============================================================================
# LOGGING SETUP
# =============================================================================

def setup_logging():
    """Configure logging with timestamps and levels."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    return logging.getLogger(__name__)

logger = setup_logging()


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def fetch_xml(url, retries=Config.MAX_RETRIES):
    """
    Fetch XML content from URL with retry logic.

    Args:
        url: The URL to fetch
        retries: Number of retry attempts

    Returns:
        XML content as string

    Raises:
        Exception: If all retries fail
    """
    last_error = None

    for attempt in range(retries):
        try:
            logger.info(f"Fetching: {url}")
            headers = {"User-Agent": Config.USER_AGENT}
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=Config.REQUEST_TIMEOUT) as response:
                return response.read().decode("utf-8")
        except urllib.error.URLError as e:
            last_error = e
            logger.warning(f"Attempt {attempt + 1}/{retries} failed: {e}")
            if attempt < retries - 1:
                import time
                time.sleep(2 ** attempt)  # Exponential backoff

    raise Exception(f"Failed to fetch {url} after {retries} attempts: {last_error}")


def clean_xml_namespaces(xml_content):
    """Remove XML namespaces to simplify parsing."""
    xml_content = re.sub(r'\sxmlns[^"]*"[^"]*"', '', xml_content)
    xml_content = re.sub(r'<(/?)image:', r'<\1image_', xml_content)
    return xml_content


def escape_markdown(text):
    """Escape special characters for Markdown tables."""
    return text.replace('|', '\\|')


def escape_html(text):
    """Escape special characters for HTML."""
    return (text
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;'))


# =============================================================================
# DATA FETCHING
# =============================================================================

def get_latest_month_index():
    """Find the latest month index URL from sitemap."""
    logger.info("Step 1: Finding latest month index...")
    xml_content = fetch_xml(Config.SITEMAP_URL)
    xml_content = clean_xml_namespaces(xml_content)

    root = ET.fromstring(xml_content)
    month_indexes = []

    for sitemap in root.findall('.//sitemap'):
        loc = sitemap.find('loc')
        if loc is not None and loc.text:
            url = loc.text.strip()
            match = re.search(r'sitemap-index-(\d{4})-(\d{2})\.xml$', url)
            if match:
                year, month = int(match.group(1)), int(match.group(2))
                month_indexes.append((year, month, url))

    if not month_indexes:
        raise ValueError("No month index files found in sitemap.xml")

    month_indexes.sort(key=lambda x: (x[0], x[1]), reverse=True)
    latest = month_indexes[0]
    logger.info(f"Found latest month: {latest[0]}-{latest[1]:02d}")
    return latest[2]


def get_latest_part_url(month_index_url):
    """Find the latest part file URL from month index."""
    logger.info("Step 2: Finding latest part file...")
    xml_content = fetch_xml(month_index_url)
    xml_content = clean_xml_namespaces(xml_content)

    root = ET.fromstring(xml_content)
    part_files = []

    for sitemap in root.findall('.//sitemap'):
        loc = sitemap.find('loc')
        if loc is not None and loc.text:
            url = loc.text.strip()
            match = re.search(r'jobs-detail-\d{4}-\d{2}-part(\d+)\.xml$', url)
            if match:
                part_num = int(match.group(1))
                part_files.append((part_num, url))

    if not part_files:
        raise ValueError("No part files found in month index")

    part_files.sort(key=lambda x: x[0], reverse=True)
    latest = part_files[0]
    logger.info(f"Found latest part: part{latest[0]}")
    return latest[1]


def get_latest_jobs_url():
    """Get the URL for the latest job data."""
    month_index_url = get_latest_month_index()
    return get_latest_part_url(month_index_url)


# =============================================================================
# JOB PARSING
# =============================================================================

def parse_jobs(xml_content):
    """
    Parse XML content and extract job information.

    Returns:
        List of job dictionaries with title, company, location, url, logo
    """
    xml_content = clean_xml_namespaces(xml_content)
    root = ET.fromstring(xml_content)
    jobs = []

    for url_elem in root.findall('.//url'):
        loc = url_elem.find('loc')
        image = url_elem.find('.//image_image')
        caption = image.find('image_caption') if image is not None else None
        image_loc = image.find('image_loc') if image is not None else None

        if loc is not None and caption is not None:
            job_url = loc.text.strip()
            caption_text = caption.text.strip() if caption.text else ""
            logo_url = image_loc.text.strip() if image_loc is not None and image_loc.text else Config.DEFAULT_LOGO

            # Parse caption: "Job Title at Company in Location"
            parts = caption_text.split(' at ')
            if len(parts) >= 2:
                title = parts[0].strip()
                rest = ' at '.join(parts[1:])

                location_parts = rest.split(' in ')
                if len(location_parts) >= 2:
                    company = location_parts[0].strip()
                    location = ' in '.join(location_parts[1:]).strip()
                else:
                    company = rest.strip()
                    location = "-"
            else:
                title = caption_text
                company = "-"
                location = "-"

            jobs.append({
                'title': title,
                'company': company,
                'location': location,
                'url': job_url,
                'logo': logo_url
            })

    return jobs


def get_rotation_offset(total_jobs):
    """Calculate rotation offset based on current time."""
    now = datetime.now(timezone.utc)
    epoch = datetime(2025, 1, 1, tzinfo=timezone.utc)
    hours_since_epoch = (now - epoch).total_seconds() / 3600
    rotation_period = int(hours_since_epoch / Config.ROTATION_HOURS)
    return (rotation_period * Config.JOBS_PER_PAGE) % max(total_jobs, 1)


# =============================================================================
# STATISTICS
# =============================================================================

def calculate_stats(jobs):
    """
    Calculate job statistics for dashboard.

    Returns:
        Dictionary with various statistics
    """
    company_counts = Counter(job['company'] for job in jobs)

    # Categorize jobs by keywords
    categories = {
        'Engineering': ['engineer', 'developer', 'software', 'architect', 'devops'],
        'Healthcare': ['nurse', 'rn', 'medical', 'health', 'therapist', 'physician', 'clinical'],
        'Sales': ['sales', 'account', 'business development'],
        'Finance': ['finance', 'financial', 'accounting', 'banker', 'analyst'],
        'Management': ['manager', 'director', 'supervisor', 'coordinator'],
        'Other': []
    }

    category_counts = {cat: 0 for cat in categories}

    for job in jobs:
        title_lower = job['title'].lower()
        categorized = False

        for category, keywords in categories.items():
            if category == 'Other':
                continue
            if any(kw in title_lower for kw in keywords):
                category_counts[category] += 1
                categorized = True
                break

        if not categorized:
            category_counts['Other'] += 1

    return {
        'total_jobs': len(jobs),
        'total_companies': len(company_counts),
        'top_companies': dict(company_counts.most_common(10)),
        'categories': category_counts,
        'updated_at': datetime.now(timezone.utc).isoformat()
    }


# =============================================================================
# OUTPUT GENERATION
# =============================================================================

def generate_readme(jobs, stats):
    """Generate README.md content with job listings."""
    total_jobs = len(jobs)
    offset = get_rotation_offset(total_jobs)

    selected_jobs = []
    for i in range(min(Config.JOBS_PER_PAGE, total_jobs)):
        idx = (offset + i) % total_jobs
        selected_jobs.append(jobs[idx])

    now = datetime.now(timezone.utc)
    date_str = now.strftime("%B %d, %Y")

    # Header section with badges and documentation
    readme = f'''<p align="center">
  <img src="https://img.shields.io/badge/jobs-{total_jobs}+-blue?style=for-the-badge" alt="Jobs Count">
  <img src="https://img.shields.io/badge/companies-{stats['total_companies']}+-purple?style=for-the-badge" alt="Companies">
  <img src="https://img.shields.io/badge/updated-every%206h-green?style=for-the-badge" alt="Update Frequency">
  <img src="https://img.shields.io/github/license/digidai/openjobs?style=for-the-badge" alt="License">
  <img src="https://img.shields.io/github/stars/digidai/openjobs?style=for-the-badge" alt="Stars">
</p>

<h1 align="center">OpenJobs</h1>

<p align="center">
  <strong>A free, open-source job aggregator that automatically collects and displays job listings from top companies.</strong>
</p>

<p align="center">
  <a href="https://digidai.github.io/openjobs">GitHub Pages</a> ·
  <a href="https://openjobs.genedai.me">Cloudflare Mirror</a> ·
  <a href="#features">Features</a> ·
  <a href="#quick-start">Quick Start</a> ·
  <a href="#contributing">Contributing</a>
</p>

---

## Why OpenJobs?

Most job boards are cluttered with ads, require sign-ups, or hide the best listings behind paywalls. **OpenJobs** is different:

- **100% Free & Open Source** - No ads, no paywalls, no sign-ups
- **Auto-Updated Every 6 Hours** - Fresh jobs from {stats['total_companies']}+ companies via GitHub Actions
- **Zero Infrastructure** - Runs entirely on GitHub Pages + Cloudflare (free tier)
- **Lightweight** - Pure Python, no external dependencies, <1MB total size
- **SEO Optimized** - Proper sitemaps, meta tags, and structured content

## Job Statistics

| Category | Count |
|----------|------:|
'''

    for category, count in sorted(stats['categories'].items(), key=lambda x: -x[1]):
        readme += f"| {category} | {count:,} |\n"

    readme += f'''
**Top Hiring Companies:** {', '.join(list(stats['top_companies'].keys())[:5])}

## Features

| Feature | Description |
|---------|-------------|
| **Auto Discovery** | Automatically finds and fetches the latest job data sources |
| **Smart Rotation** | Jobs rotate every 6 hours to show fresh content |
| **Dual Deployment** | GitHub Pages (table view) + Cloudflare Pages (card view) |
| **Company Logos** | Visual company branding for easy recognition |
| **Mobile Responsive** | Works perfectly on all device sizes |
| **Daily Sitemaps** | SEO-friendly XML sitemaps updated automatically |

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        GitHub Actions                           │
│                    (Scheduled every 6h)                         │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    update_readme.py                             │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────────────┐   │
│  │ Fetch XML   │ → │ Parse Jobs  │ → │ Generate Output     │   │
│  │ Sitemap     │   │ ({total_jobs}+ jobs) │   │ (README + HTML)     │   │
│  └─────────────┘   └─────────────┘   └─────────────────────┘   │
└─────────────────────────┬───────────────────────────────────────┘
                          │
          ┌───────────────┴───────────────┐
          ▼                               ▼
┌─────────────────────┐       ┌─────────────────────┐
│   GitHub Pages      │       │  Cloudflare Pages   │
│   (README.md)       │       │  (public/index.html)│
│   Table Layout      │       │   Card Grid Layout  │
│   200 jobs/page     │       │   50 jobs/page      │
└─────────────────────┘       └─────────────────────┘
```

## Quick Start

### Prerequisites

- Python 3.11+
- Git

### Local Development

```bash
# Clone the repository
git clone https://github.com/digidai/openjobs.git
cd openjobs

# Run the update script
python scripts/update_readme.py

# View the generated files
open README.md           # GitHub Pages content
open public/index.html   # Cloudflare Pages content
```

### Deploy Your Own

1. **Fork this repository**

2. **Enable GitHub Pages**
   - Go to Settings → Pages
   - Source: Deploy from a branch
   - Branch: `main` / `root`

3. **Enable GitHub Actions**
   - Go to Actions tab
   - Enable workflows
   - Jobs will auto-update every 6 hours

4. **(Optional) Deploy to Cloudflare Pages**
   - Connect your forked repo
   - Build command: (none)
   - Output directory: `public`

## Configuration

Edit `scripts/update_readme.py` to customize:

| Variable | Default | Description |
|----------|---------|-------------|
| `JOBS_PER_PAGE` | 200 | Number of jobs shown on README |
| `ROTATION_HOURS` | 6 | Hours between job rotation |
| `CF_SITE_URL` | `https://openjobs.genedai.me` | Cloudflare Pages URL |
| `GH_SITE_URL` | `https://digidai.github.io/openjobs` | GitHub Pages URL |

## Data Source

Jobs are aggregated from [OpenJobs AI](https://www.openjobs-ai.com), which collects listings from:

- **Tech**: Google, Amazon, Microsoft, Salesforce, SpaceX, and more
- **Healthcare**: Mayo Clinic, CVS Health, Northwell Health, and more
- **Finance**: CME Group, Fidelity, First Citizens Bank, and more
- **Retail**: Macy's, CVS, and more
- **And {stats['total_companies']}+ other companies**

## Project Structure

```
openjobs/
├── .github/
│   ├── workflows/          # GitHub Actions automation
│   └── ISSUE_TEMPLATE/     # Issue templates
├── scripts/
│   └── update_readme.py    # Main Python script
├── public/
│   ├── index.html          # Cloudflare Pages site
│   ├── stats.json          # Job statistics API
│   └── sitemap.xml         # Cloudflare sitemap
├── README.md               # This file (also GitHub Pages)
├── sitemap.xml             # GitHub Pages sitemap
├── _config.yml             # Jekyll configuration
├── LICENSE                 # MIT License
└── CONTRIBUTING.md         # Contribution guidelines
```

## Roadmap

- [ ] Job search/filter functionality
- [ ] Job category tags
- [ ] Salary information (when available)
- [ ] Remote job filtering
- [ ] Email notifications for new jobs
- [ ] RSS feed support
- [x] Job statistics dashboard

## Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) before submitting a PR.

### Ways to Contribute

- Report bugs or suggest features via [Issues](https://github.com/digidai/openjobs/issues)
- Improve documentation
- Add new features
- Optimize performance

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Job data provided by [OpenJobs AI](https://www.openjobs-ai.com)
- Hosted on [GitHub Pages](https://pages.github.com) and [Cloudflare Pages](https://pages.cloudflare.com)

---

<h2 align="center">Latest Job Openings</h2>

<p align="center">
  <em>Updated {date_str} · Showing {len(selected_jobs)} of {total_jobs:,}+ jobs</em>
</p>

| Job Title | Company | Apply |
|-----------|---------|:-----:|
'''

    for job in selected_jobs:
        title = escape_markdown(job['title'])
        company = escape_markdown(job['company'])
        logo = job.get('logo', Config.DEFAULT_LOGO)
        readme += f'| {title} | <img src="{logo}" width="20" height="20" alt=""> {company} | [View]({job["url"]}) |\n'

    readme += f'''
<p align="center">
  <em>...and {total_jobs - len(selected_jobs):,} more jobs</em>
</p>

<p align="center">
  <a href="https://www.openjobs-ai.com/deepsearch"><strong>Browse All Jobs →</strong></a>
</p>

---

<p align="center">
  Made with Python + GitHub Actions · Updated {date_str}
</p>
'''

    return readme


def generate_html(jobs, stats):
    """Generate HTML page with card layout and search functionality."""
    total_jobs = len(jobs)
    offset = get_rotation_offset(total_jobs) + Config.JOBS_PER_PAGE

    selected_jobs = []
    for i in range(min(Config.HTML_JOBS_COUNT, total_jobs)):
        idx = (offset + i) % total_jobs
        selected_jobs.append(jobs[idx])

    now = datetime.now(timezone.utc)
    date_str = now.strftime("%b %d, %Y")

    jobs_json = json.dumps([{
        'title': job['title'],
        'company': job['company'],
        'url': job['url'],
        'logo': job.get('logo', Config.DEFAULT_LOGO)
    } for job in selected_jobs])

    jobs_cards = ""
    for job in selected_jobs:
        title = escape_html(job['title'])
        company = escape_html(job['company'])
        logo = job.get('logo', Config.DEFAULT_LOGO)
        jobs_cards += f'''    <a href="{job['url']}" class="card" target="_blank" rel="noopener" data-title="{title.lower()}" data-company="{company.lower()}">
      <div class="card-title">{title}</div>
      <div class="card-company"><img src="{logo}" alt="" class="logo">{company}</div>
    </a>
'''

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>OpenJobs - Find Your Next Career</title>
  <meta name="description" content="Browse {total_jobs:,}+ open positions from {stats['total_companies']}+ companies. New jobs added daily from leading employers across tech, healthcare, finance, and more.">
  <link rel="canonical" href="{Config.CF_SITE_URL}/">
  <meta property="og:title" content="OpenJobs - Find Your Next Career">
  <meta property="og:description" content="Browse {total_jobs:,}+ job openings from top companies. Updated every 6 hours.">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{Config.CF_SITE_URL}/">
  <style>
    :root {{ --primary: #0f172a; --accent: #3b82f6; --bg: #ffffff; --card-bg: #fafafa; --text: #0f172a; --muted: #6b7280; --border: #e5e7eb; }}
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif; background: var(--bg); color: var(--text); }}
    .container {{ max-width: 960px; margin: 0 auto; padding: 3rem 1.5rem; }}
    header {{ margin-bottom: 2rem; }}
    h1 {{ font-size: 1.5rem; font-weight: 600; letter-spacing: -0.02em; }}
    .meta {{ color: var(--muted); font-size: 0.875rem; margin-top: 0.5rem; }}
    .stats {{ display: flex; gap: 1.5rem; margin-top: 1rem; flex-wrap: wrap; }}
    .stat {{ background: var(--card-bg); padding: 0.5rem 1rem; border-radius: 6px; font-size: 0.8rem; }}
    .stat-value {{ font-weight: 600; color: var(--accent); }}
    .search-box {{ margin-bottom: 1.5rem; }}
    .search-input {{ width: 100%; padding: 0.75rem 1rem; font-size: 0.9rem; border: 1px solid var(--border); border-radius: 8px; outline: none; transition: border-color 0.15s; }}
    .search-input:focus {{ border-color: var(--accent); }}
    .grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 1px; background: var(--border); border: 1px solid var(--border); border-radius: 8px; overflow: hidden; }}
    .card {{ display: flex; flex-direction: column; gap: 0.375rem; background: var(--bg); padding: 1rem 1.25rem; text-decoration: none; color: inherit; transition: background 0.15s; }}
    .card:hover {{ background: var(--card-bg); }}
    .card.hidden {{ display: none; }}
    .card-title {{ font-weight: 500; font-size: 0.9rem; color: var(--text); line-height: 1.35; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }}
    .card-company {{ font-size: 0.8rem; color: var(--muted); display: flex; align-items: center; gap: 0.4rem; }}
    .logo {{ width: 16px; height: 16px; border-radius: 3px; object-fit: contain; }}
    .no-results {{ grid-column: 1 / -1; padding: 2rem; text-align: center; color: var(--muted); background: var(--bg); }}
    footer {{ margin-top: 2.5rem; text-align: center; }}
    footer a {{ color: var(--accent); text-decoration: none; font-size: 0.875rem; }}
    footer a:hover {{ text-decoration: underline; }}
    .github-link {{ margin-top: 1rem; font-size: 0.8rem; color: var(--muted); }}
    .github-link a {{ color: var(--muted); }}
    @media (max-width: 600px) {{ .grid {{ grid-template-columns: 1fr; }} .container {{ padding: 2rem 1rem; }} .stats {{ gap: 0.75rem; }} }}
  </style>
</head>
<body>
  <div class="container">
    <header>
      <h1>Find Your Next Career</h1>
      <p class="meta">{total_jobs:,}+ positions from {stats['total_companies']}+ companies · Updated {date_str}</p>
      <div class="stats">
        <div class="stat"><span class="stat-value">{stats['categories'].get('Engineering', 0):,}</span> Engineering</div>
        <div class="stat"><span class="stat-value">{stats['categories'].get('Healthcare', 0):,}</span> Healthcare</div>
        <div class="stat"><span class="stat-value">{stats['categories'].get('Sales', 0):,}</span> Sales</div>
        <div class="stat"><span class="stat-value">{stats['categories'].get('Finance', 0):,}</span> Finance</div>
      </div>
    </header>
    <div class="search-box">
      <input type="text" class="search-input" placeholder="Search jobs or companies..." id="searchInput">
    </div>
    <div class="grid" id="jobsGrid">
{jobs_cards}      <div class="no-results" id="noResults" style="display: none;">No jobs found matching your search.</div>
    </div>
    <footer>
      <a href="https://www.openjobs-ai.com/deepsearch">View all {total_jobs:,}+ jobs →</a>
      <p class="github-link">Open source on <a href="https://github.com/digidai/openjobs">GitHub</a></p>
    </footer>
  </div>
  <script>
    const searchInput = document.getElementById('searchInput');
    const jobsGrid = document.getElementById('jobsGrid');
    const cards = jobsGrid.querySelectorAll('.card:not(.no-results)');
    const noResults = document.getElementById('noResults');

    searchInput.addEventListener('input', function() {{
      const query = this.value.toLowerCase().trim();
      let visibleCount = 0;

      cards.forEach(card => {{
        const title = card.dataset.title || '';
        const company = card.dataset.company || '';
        const matches = !query || title.includes(query) || company.includes(query);
        card.classList.toggle('hidden', !matches);
        if (matches) visibleCount++;
      }});

      noResults.style.display = visibleCount === 0 ? 'block' : 'none';
    }});
  </script>
</body>
</html>
'''
    return html


def generate_sitemap(site_url):
    """Generate XML sitemap."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>{site_url}/</loc>
    <lastmod>{now}</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>
'''


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Main execution function."""
    logger.info("=" * 60)
    logger.info("OpenJobs Updater")
    logger.info("=" * 60)

    try:
        # Fetch data
        jobs_url = get_latest_jobs_url()

        logger.info("Step 3: Fetching job listings...")
        xml_content = fetch_xml(jobs_url)

        logger.info("Step 4: Parsing jobs...")
        jobs = parse_jobs(xml_content)
        logger.info(f"Found {len(jobs)} jobs")

        if not jobs:
            logger.error("No jobs found! Aborting.")
            sys.exit(1)

        logger.info("Step 5: Calculating statistics...")
        stats = calculate_stats(jobs)
        logger.info(f"Stats: {stats['total_jobs']} jobs from {stats['total_companies']} companies")

        logger.info("Step 6: Generating README.md...")
        readme_content = generate_readme(jobs, stats)
        with open(Config.README_PATH, 'w', encoding='utf-8') as f:
            f.write(readme_content)

        logger.info("Step 7: Generating HTML for Cloudflare Pages...")
        os.makedirs(os.path.dirname(Config.HTML_PATH), exist_ok=True)
        html_content = generate_html(jobs, stats)
        with open(Config.HTML_PATH, 'w', encoding='utf-8') as f:
            f.write(html_content)

        logger.info("Step 8: Generating stats.json...")
        with open(Config.STATS_PATH, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2)

        logger.info("Step 9: Generating sitemaps...")
        with open(Config.CF_SITEMAP_PATH, 'w', encoding='utf-8') as f:
            f.write(generate_sitemap(Config.CF_SITE_URL))
        with open(Config.GH_SITEMAP_PATH, 'w', encoding='utf-8') as f:
            f.write(generate_sitemap(Config.GH_SITE_URL))

        logger.info("=" * 60)
        logger.info("Done! Generated files:")
        logger.info(f"  - {Config.README_PATH}")
        logger.info(f"  - {Config.HTML_PATH}")
        logger.info(f"  - {Config.STATS_PATH}")
        logger.info(f"  - {Config.CF_SITEMAP_PATH}")
        logger.info(f"  - {Config.GH_SITEMAP_PATH}")
        logger.info("=" * 60)

    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
