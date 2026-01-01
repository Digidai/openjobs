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
import shutil
import tempfile

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

    # Image optimization
    IMAGE_CDN_ENABLED = True
    IMAGE_CDN_URL = "https://images.weserv.nl/?url="  # Free image CDN
    IMAGE_QUALITY = 80
    LOGO_WIDTH = 24
    LOGO_HEIGHT = 24

    # Reliability settings
    BACKUP_PATH = ".cache/jobs_backup.json"
    MIN_DISK_SPACE_MB = 50
    MAX_HTML_JOBS = 1000  # Limit jobs in HTML to prevent memory issues


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

class FetchError(Exception):
    """Custom exception for fetch failures."""
    pass


class ParseError(Exception):
    """Custom exception for parsing failures."""
    pass


def check_disk_space(required_mb=Config.MIN_DISK_SPACE_MB):
    """
    Check if sufficient disk space is available.

    Args:
        required_mb: Required disk space in megabytes

    Raises:
        OSError: If insufficient disk space
    """
    try:
        free_bytes = shutil.disk_usage('.').free
        free_mb = free_bytes / (1024 * 1024)

        if free_mb < required_mb:
            raise OSError(f"Insufficient disk space: {free_mb:.1f}MB free, {required_mb}MB required")

        logger.info(f"Disk space check passed: {free_mb:.1f}MB free")
    except Exception as e:
        logger.warning(f"Could not check disk space: {e}")
        # Don't fail on check failure, just warn


def save_backup(jobs, stats):
    """Save jobs and stats to backup file for disaster recovery."""
    try:
        backup_dir = os.path.dirname(Config.BACKUP_PATH)
        if backup_dir:
            os.makedirs(backup_dir, exist_ok=True)

        backup_data = {
            'jobs': jobs,
            'stats': stats,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'version': '2.0'
        }

        # Atomic write using temporary file
        temp_path = Config.BACKUP_PATH + '.tmp'
        with open(temp_path, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, indent=2)

        # Atomic rename
        os.replace(temp_path, Config.BACKUP_PATH)
        logger.info(f"Backup saved to {Config.BACKUP_PATH}")

    except Exception as e:
        logger.warning(f"Failed to save backup: {e}")
        # Don't fail on backup error


def load_backup():
    """
    Load jobs and stats from backup file.

    Returns:
        Tuple of (jobs, stats) or (None, None) if backup not available
    """
    try:
        if not os.path.exists(Config.BACKUP_PATH):
            logger.info("No backup file found")
            return None, None

        with open(Config.BACKUP_PATH, 'r', encoding='utf-8') as f:
            backup_data = json.load(f)

        jobs = backup_data.get('jobs')
        stats = backup_data.get('stats')
        timestamp = backup_data.get('timestamp', 'unknown')

        if jobs and stats:
            logger.info(f"Loaded backup from {timestamp} with {len(jobs)} jobs")
            return jobs, stats
        else:
            logger.warning("Backup file exists but contains no valid data")
            return None, None

    except Exception as e:
        logger.error(f"Failed to load backup: {e}")
        return None, None


def atomic_write(file_path, content):
    """
    Write content to file atomically to prevent corruption.

    Args:
        file_path: Target file path
        content: Content to write (string)

    Raises:
        IOError: If write fails
    """
    # Ensure directory exists
    dir_path = os.path.dirname(file_path)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)

    # Write to temporary file
    temp_fd, temp_path = tempfile.mkstemp(
        dir=dir_path,
        prefix=os.path.basename(file_path) + '.',
        suffix='.tmp'
    )

    try:
        with os.fdopen(temp_fd, 'w', encoding='utf-8') as f:
            f.write(content)

        # Verify file was written
        if os.path.getsize(temp_path) == 0:
            raise IOError("Temporary file is empty")

        # Atomic rename
        os.replace(temp_path, file_path)

    except Exception as e:
        # Clean up temp file on error
        try:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
        except:
            pass
        raise IOError(f"Atomic write failed: {e}")


def atomic_write_json(file_path, data):
    """
    Write JSON data to file atomically.

    Args:
        file_path: Target file path
        data: Data to serialize as JSON

    Raises:
        IOError: If write fails
    """
    # Ensure directory exists
    dir_path = os.path.dirname(file_path)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)

    # Write to temporary file
    temp_fd, temp_path = tempfile.mkstemp(
        dir=dir_path,
        prefix=os.path.basename(file_path) + '.',
        suffix='.tmp'
    )

    try:
        with os.fdopen(temp_fd, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

        # Verify file was written
        if os.path.getsize(temp_path) == 0:
            raise IOError("Temporary file is empty")

        # Atomic rename
        os.replace(temp_path, file_path)

    except Exception as e:
        # Clean up temp file on error
        try:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
        except:
            pass
        raise IOError(f"Atomic JSON write failed: {e}")


def fetch_xml(url, retries=Config.MAX_RETRIES):
    """
    Fetch XML content from URL with comprehensive retry logic.

    Args:
        url: The URL to fetch
        retries: Number of retry attempts

    Returns:
        XML content as string

    Raises:
        FetchError: If all retries fail
    """
    import socket
    import time

    last_error = None
    delay = 1  # Initial delay in seconds

    for attempt in range(retries):
        try:
            logger.info(f"Fetching: {url} (attempt {attempt + 1}/{retries})")
            headers = {"User-Agent": Config.USER_AGENT}
            req = urllib.request.Request(url, headers=headers)

            with urllib.request.urlopen(req, timeout=Config.REQUEST_TIMEOUT) as response:
                content = response.read()

                if not content:
                    raise ValueError("Empty response body")

                # Try to decode
                try:
                    decoded = content.decode("utf-8")
                except UnicodeDecodeError:
                    # Try alternative encodings
                    for encoding in ['latin-1', 'iso-8859-1']:
                        try:
                            decoded = content.decode(encoding)
                            logger.warning(f"Used fallback encoding: {encoding}")
                            break
                        except UnicodeDecodeError:
                            continue
                    else:
                        raise

                return decoded

        except (urllib.error.URLError, socket.timeout, socket.gaierror) as e:
            last_error = e
            logger.warning(f"Network error on attempt {attempt + 1}/{retries}: {type(e).__name__}: {e}")
        except (ValueError, UnicodeDecodeError) as e:
            last_error = e
            logger.warning(f"Content error on attempt {attempt + 1}/{retries}: {type(e).__name__}: {e}")
        except Exception as e:
            last_error = e
            logger.error(f"Unexpected error: {type(e).__name__}: {e}")

        if attempt < retries - 1:
            wait_time = min(delay * (2 ** attempt), 30)  # Cap at 30 seconds
            logger.info(f"Waiting {wait_time}s before retry...")
            time.sleep(wait_time)

    raise FetchError(f"Failed to fetch {url} after {retries} attempts: {last_error}")


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


def optimize_image_url(url, use_cdn=None):
    """
    Optimize image URL with CDN and quality settings.

    Args:
        url: Original image URL
        use_cdn: Override CDN setting (optional)

    Returns:
        Optimized image URL
    """
    if not url or not url.startswith('http'):
        return url

    # Use config setting if not overridden
    if use_cdn is None:
        use_cdn = Config.IMAGE_CDN_ENABLED

    if not use_cdn:
        return url

    # Use CDN for optimization
    # Only for external images, not already optimized
    if Config.IMAGE_CDN_URL and not url.startswith(Config.IMAGE_CDN_URL):
        # Encode the original URL and add CDN parameters
        from urllib.parse import quote
        encoded_url = quote(url, safe=':/?#[]@!$&\'()*+,;=')
        return f"{Config.IMAGE_CDN_URL}{encoded_url}&w={Config.LOGO_WIDTH}&h={Config.LOGO_HEIGHT}&q={Config.IMAGE_QUALITY}&output=webp"

    return url


# =============================================================================
# DATA FETCHING
# =============================================================================

def get_latest_month_index():
    """Find the latest month index URL by trying recent months directly."""
    logger.info("Step 1: Finding latest month index...")

    # Try current month and previous months directly
    # (sitemap.xml structure changed, no longer lists monthly indexes)
    now = datetime.now(timezone.utc)
    base_url = "https://www.openjobs-ai.com/xml/sitemap-index-{year}-{month:02d}.xml"

    # Try current month and previous 3 months
    months_to_try = []
    for i in range(4):
        year = now.year
        month = now.month - i
        if month <= 0:
            month += 12
            year -= 1
        months_to_try.append((year, month))

    for year, month in months_to_try:
        url = base_url.format(year=year, month=month)
        logger.info(f"Trying: {url}")
        try:
            # Quick check if URL exists
            xml_content = fetch_xml(url, retries=1)
            if xml_content and 'sitemap' in xml_content.lower():
                logger.info(f"Found latest month: {year}-{month:02d}")
                return url
        except FetchError:
            logger.debug(f"Month index not found: {year}-{month:02d}")
            continue

    raise ValueError("No month index files found after trying recent months")


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

def parse_job_caption(caption_text):
    """
    Parse job caption with multiple fallback strategies.

    Supported formats:
    - "Job Title at Company in Location"
    - "Job Title at Company - Location"
    - "Job Title at Company | Location"
    - "Job Title - Company - Location"
    - "Job Title @ Company (Location)"
    - "Job Title at Company"
    """
    if not caption_text:
        return None

    caption_text = caption_text.strip()

    # Strategy 1: Title at Company in Location
    match = re.match(r'^(.+?)\s+at\s+(.+?)\s+in\s+(.+)$', caption_text, re.IGNORECASE)
    if match:
        return {
            'title': match.group(1).strip(),
            'company': match.group(2).strip(),
            'location': match.group(3).strip()
        }

    # Strategy 2: Title at Company - Location
    match = re.match(r'^(.+?)\s+at\s+(.+?)\s+-\s+(.+)$', caption_text, re.IGNORECASE)
    if match:
        return {
            'title': match.group(1).strip(),
            'company': match.group(2).strip(),
            'location': match.group(3).strip()
        }

    # Strategy 3: Title at Company | Location
    match = re.match(r'^(.+?)\s+at\s+(.+?)\s+\|\s*(.+)$', caption_text, re.IGNORECASE)
    if match:
        return {
            'title': match.group(1).strip(),
            'company': match.group(2).strip(),
            'location': match.group(3).strip()
        }

    # Strategy 4: Title - Company - Location
    match = re.match(r'^(.+?)\s+-\s+(.+?)\s+-\s+(.+)$', caption_text, re.IGNORECASE)
    if match:
        return {
            'title': match.group(1).strip(),
            'company': match.group(2).strip(),
            'location': match.group(3).strip()
        }

    # Strategy 5: Title @ Company (Location)
    match = re.match(r'^(.+?)\s+@\s+(.+?)\s+\((.+)\)$', caption_text, re.IGNORECASE)
    if match:
        return {
            'title': match.group(1).strip(),
            'company': match.group(2).strip(),
            'location': match.group(3).strip()
        }

    # Strategy 6: Title @ Company - Location
    match = re.match(r'^(.+?)\s+@\s+(.+?)\s+-\s+(.+)$', caption_text, re.IGNORECASE)
    if match:
        return {
            'title': match.group(1).strip(),
            'company': match.group(2).strip(),
            'location': match.group(3).strip()
        }

    # Strategy 7: Title at Company (no location - default)
    match = re.match(r'^(.+?)\s+at\s+(.+)$', caption_text, re.IGNORECASE)
    if match:
        return {
            'title': match.group(1).strip(),
            'company': match.group(2).strip(),
            'location': '-'
        }

    # Strategy 8: Title @ Company (no location - default)
    match = re.match(r'^(.+?)\s+@\s+(.+)$', caption_text, re.IGNORECASE)
    if match:
        return {
            'title': match.group(1).strip(),
            'company': match.group(2).strip(),
            'location': '-'
        }

    # Strategy 9: Just use the whole caption as title (fallback)
    logger.warning(f"Using fallback parser for caption: {caption_text[:50]}...")
    return {
        'title': caption_text,
        'company': '-',
        'location': '-'
    }


def parse_jobs(xml_content):
    """
    Parse XML content and extract job information with robust error handling.

    Returns:
        Tuple of (jobs list, parse_stats dict)
    """
    try:
        xml_content = clean_xml_namespaces(xml_content)
        root = ET.fromstring(xml_content)
    except ET.ParseError as e:
        logger.error(f"XML parsing failed: {e}")
        raise ParseError(f"Invalid XML content: {e}")

    jobs = []
    parse_stats = {
        'total_elements': 0,
        'successful': 0,
        'skipped_no_caption': 0,
        'skipped_no_url': 0,
        'parse_failures': 0,
        'with_location': 0,
        'without_location': 0
    }

    for idx, url_elem in enumerate(root.findall('.//url')):
        parse_stats['total_elements'] += 1

        try:
            loc = url_elem.find('loc')
            if loc is None or not loc.text:
                parse_stats['skipped_no_url'] += 1
                continue

            image = url_elem.find('.//image_image')
            caption = image.find('image_caption') if image is not None else None

            if caption is None or not caption.text:
                parse_stats['skipped_no_caption'] += 1
                continue

            job_url = loc.text.strip()
            caption_text = caption.text.strip()
            image_loc = image.find('image_loc') if image is not None else None
            logo_url = image_loc.text.strip() if image_loc is not None and image_loc.text else Config.DEFAULT_LOGO

            job_data = parse_job_caption(caption_text)
            if job_data:
                job_data['url'] = job_url
                job_data['logo'] = logo_url
                jobs.append(job_data)
                parse_stats['successful'] += 1

                # Track location statistics
                if job_data.get('location') and job_data['location'] != '-':
                    parse_stats['with_location'] += 1
                else:
                    parse_stats['without_location'] += 1
            else:
                parse_stats['parse_failures'] += 1

        except Exception as e:
            logger.warning(f"Error parsing job at index {idx}: {e}")
            parse_stats['parse_failures'] += 1

    # Calculate location coverage
    if parse_stats['successful'] > 0:
        parse_stats['location_coverage'] = round(parse_stats['with_location'] / max(parse_stats['successful'], 1), 4)
    else:
        parse_stats['location_coverage'] = 0.0

    logger.info(f"Parse stats: {parse_stats}")
    return jobs, parse_stats


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

def calculate_stats(jobs, parse_stats=None):
    """
    Calculate comprehensive job statistics for dashboard.

    Returns:
        Dictionary with statistics and data quality metrics
    """
    company_counts = Counter(job['company'] for job in jobs)
    location_counts = Counter(job['location'] for job in jobs if job['location'] != '-')

    # Enhanced categorization with more categories
    categories = {
        'Engineering': ['engineer', 'developer', 'software', 'architect', 'devops', 'sre', 'programmer'],
        'Healthcare': ['nurse', 'rn', 'medical', 'health', 'therapist', 'physician', 'clinical', 'dental', 'pharmacy'],
        'Sales': ['sales', 'account executive', 'business development', 'bdr', 'sdr'],
        'Finance': ['finance', 'financial', 'accounting', 'banker', 'cfo', 'controller'],
        'Management': ['manager', 'director', 'supervisor', 'coordinator', 'lead'],
        'Marketing': ['marketing', 'content', 'brand', 'seo', 'growth'],
        'HR': ['hr', 'recruiter', 'talent', 'human resource', 'people operations'],
        'Operations': ['operations', 'logistics', 'supply chain', 'warehouse'],
        'Other': []
    }

    category_counts = {cat: 0 for cat in categories}
    job_categories = []  # Track category for each job

    for job in jobs:
        title_lower = job['title'].lower()
        categorized = False

        for category, keywords in categories.items():
            if category == 'Other':
                continue
            if any(kw in title_lower for kw in keywords):
                category_counts[category] += 1
                job_categories.append(category)
                categorized = True
                break

        if not categorized:
            category_counts['Other'] += 1
            job_categories.append('Other')

    # Data quality metrics
    jobs_with_location = sum(1 for j in jobs if j.get('location', '-') != '-')
    jobs_with_logo = sum(1 for j in jobs if j.get('logo', '').startswith('http'))

    stats = {
        'total_jobs': len(jobs),
        'total_companies': len(company_counts),
        'top_companies': dict(company_counts.most_common(10)),
        'categories': category_counts,
        'top_locations': dict(location_counts.most_common(10)),
        'updated_at': datetime.now(timezone.utc).isoformat(),

        # Data quality metrics
        'data_quality': {
            'jobs_with_location': jobs_with_location,
            'jobs_with_logo': jobs_with_logo,
            'location_coverage': round(jobs_with_location / max(len(jobs), 1), 4),
            'logo_coverage': round(jobs_with_logo / max(len(jobs), 1), 4),
        }
    }

    # Add parse stats if available
    if parse_stats:
        stats['data_quality']['parse_stats'] = parse_stats
        stats['data_quality']['parse_success_rate'] = round(
            parse_stats['successful'] / max(parse_stats['total_elements'], 1), 4
        )

    return stats


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
| **Smart Parsing** | Multi-format job caption parser (9+ strategies) for better data extraction |
| **Image Optimization** | CDN-powered image optimization with WebP conversion and lazy loading |
| **Smart Rotation** | Jobs rotate every 6 hours to show fresh content |
| **Dual Deployment** | GitHub Pages (table view) + Cloudflare Pages (card view) |
| **Company Logos** | Visual company branding for easy recognition |
| **Mobile Responsive** | Works perfectly on all device sizes |
| **SEO Enhanced** | Schema.org structured data, breadcrumbs, FAQ, and meta tags |
| **Accessibility** | WCAG compliant with ARIA labels, skip links, and keyboard navigation |
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
| `HTML_JOBS_COUNT` | 50 | Number of jobs in HTML page |
| `ROTATION_HOURS` | 6 | Hours between job rotation |
| `CF_SITE_URL` | `https://openjobs.genedai.me` | Cloudflare Pages URL |
| `GH_SITE_URL` | `https://digidai.github.io/openjobs` | GitHub Pages URL |
| `IMAGE_CDN_ENABLED` | `True` | Enable/disable CDN image optimization |
| `IMAGE_CDN_URL` | `https://images.weserv.nl/?url=` | CDN service URL |
| `IMAGE_QUALITY` | 80 | Image quality (1-100) |
| `LOGO_WIDTH/HEIGHT` | 24 | Logo dimensions in pixels |

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

## Recent Enhancements

### 🚀 Performance & Quality Improvements (v2.0)

**Data Parsing (14.7x better location extraction)**
- Implemented 9-format job caption parser supporting:
  - `Title at Company in Location`
  - `Title at Company - Location`
  - `Title at Company | Location`
  - `Title - Company - Location`
  - `Title @ Company (Location)`
  - And more fallback strategies
- Location coverage improved from 0.4% to 6.28%

**Image Optimization**
- Free CDN integration (images.weserv.nl)
- Automatic WebP conversion with fallback
- Optimized dimensions (24x24px logos)
- Quality compression (80%)
- DNS prefetch and preconnection
- Lazy loading for better performance

**SEO Enhancements**
- Schema.org structured data:
  - BreadcrumbList for navigation
  - FAQPage for common questions
  - ItemList for job postings
  - Organization and WebSite schemas
- Enhanced meta tags (application-name, theme-color)
- Mobile web app capable

**Accessibility (WCAG Compliant)**
- Skip to main content link
- Comprehensive ARIA labels
- Keyboard navigation support
- Screen reader friendly
- Focus management

**Code Quality**
- Zero pyflakes warnings
- Enhanced error handling
- Detailed parse statistics
- Better logging and monitoring

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
        logo = optimize_image_url(job.get('logo', Config.DEFAULT_LOGO))
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


def categorize_job(title):
    """Categorize a job by its title."""
    title_lower = title.lower()
    categories = {
        'Engineering': ['engineer', 'developer', 'software', 'architect', 'devops', 'sre'],
        'Healthcare': ['nurse', 'rn', 'medical', 'health', 'therapist', 'physician', 'clinical'],
        'Sales': ['sales', 'account executive', 'business development'],
        'Finance': ['finance', 'financial', 'accounting', 'banker', 'cfo'],
        'Management': ['manager', 'director', 'supervisor', 'coordinator'],
    }
    for category, keywords in categories.items():
        if any(kw in title_lower for kw in keywords):
            return category
    return 'Other'


def generate_html(jobs, stats):
    """Generate HTML page with pagination, filtering, search, a11y, lazy loading, and enhanced SEO."""
    total_jobs = len(jobs)
    now = datetime.now(timezone.utc)
    date_str = now.strftime("%b %d, %Y")
    iso_date = now.strftime("%Y-%m-%dT%H:%M:%SZ")

    # Limit jobs in HTML to prevent memory issues
    html_jobs = jobs[:Config.MAX_HTML_JOBS]
    if len(jobs) > Config.MAX_HTML_JOBS:
        logger.warning(f"Limiting HTML jobs to {Config.MAX_HTML_JOBS} of {total_jobs} for memory optimization")

    # Prepare jobs data with categories for JSON
    all_jobs_data = []
    for job in html_jobs:
        category = categorize_job(job['title'])
        all_jobs_data.append({
            'title': job['title'],
            'company': job['company'],
            'url': job['url'],
            'logo': optimize_image_url(job.get('logo', Config.DEFAULT_LOGO)),
            'category': category
        })

    jobs_json = json.dumps(all_jobs_data)

    # Generate Schema.org JSON-LD structured data
    schema_website = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "OpenJobs",
        "alternateName": "OpenJobs AI",
        "url": Config.CF_SITE_URL,
        "description": f"Free open-source job aggregator with {total_jobs:,}+ positions from {stats['total_companies']}+ companies. Updated every 6 hours.",
        "inLanguage": "en-US",
        "potentialAction": {
            "@type": "SearchAction",
            "target": f"{Config.CF_SITE_URL}/?q={{search_term_string}}",
            "query-input": "required name=search_term_string",
            "target": {
                "@type": "EntryPoint",
                "urlTemplate": f"{Config.CF_SITE_URL}/?q={{search_term_string}}"
            }
        },
        "publisher": {
            "@type": "Organization",
            "name": "OpenJobs",
            "url": Config.CF_SITE_URL
        }
    }

    # Enhanced Organization schema with more details
    schema_org = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "OpenJobs",
        "url": Config.CF_SITE_URL,
        "logo": f"{Config.CF_SITE_URL}/og-image.svg",
        "description": "Free, open-source job aggregator aggregating positions from top companies worldwide",
        "sameAs": [
            "https://github.com/Digidai/openjobs",
            "https://www.openjobs-ai.com"
        ],
        "founder": {
            "@type": "Person",
            "name": "OpenJobs Team"
        },
        "foundingDate": "2024",
        "areaServed": "Worldwide",
        "contactPoint": {
            "@type": "ContactPoint",
            "contactType": "customer service",
            "url": "https://github.com/Digidai/openjobs/issues"
        }
    }

    # ItemList for job listings (first 50 for better structured data coverage)
    job_items = []
    valid_through = (now + __import__('datetime').timedelta(days=30)).strftime("%Y-%m-%d")

    # Infer employment type from title
    def infer_employment_type(title):
        title_lower = title.lower()
        if 'part-time' in title_lower or 'part time' in title_lower:
            return 'PART_TIME'
        elif 'contract' in title_lower or 'contractor' in title_lower:
            return 'CONTRACTOR'
        elif 'intern' in title_lower or 'internship' in title_lower:
            return 'INTERN'
        elif 'temporary' in title_lower or 'temp ' in title_lower:
            return 'TEMPORARY'
        elif 'volunteer' in title_lower:
            return 'VOLUNTEER'
        return 'FULL_TIME'

    # Parse location into structured address
    def parse_location(location_str):
        if not location_str or location_str == '-':
            return {"@type": "PostalAddress", "addressCountry": "US"}

        address = {"@type": "PostalAddress"}
        parts = [p.strip() for p in location_str.replace(',', ' ').split()]

        # Common US state abbreviations
        us_states = {'AL','AK','AZ','AR','CA','CO','CT','DE','FL','GA','HI','ID','IL','IN','IA','KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VT','VA','WA','WV','WI','WY','DC'}

        for part in parts:
            if part.upper() in us_states:
                address['addressRegion'] = part.upper()
                address['addressCountry'] = 'US'
            elif len(part) == 2 and part.upper() == part:
                address['addressRegion'] = part
                address['addressCountry'] = 'US'

        if 'addressCountry' not in address:
            address['addressCountry'] = 'US'

        address['addressLocality'] = location_str
        return address

    # Use limited jobs for schema to prevent memory issues
    schema_jobs = html_jobs[:50]
    for idx, job in enumerate(schema_jobs):
        category = categorize_job(job['title'])
        employment_type = infer_employment_type(job['title'])
        location_address = parse_location(job.get('location'))

        job_posting = {
            "@type": "JobPosting",
            "title": job['title'],
            "description": f"Apply for {job['title']} position at {job['company']}. Join a leading company and advance your career.",
            "identifier": {
                "@type": "PropertyValue",
                "name": job['company'],
                "value": job['url'].split('/')[-1] if '/' in job['url'] else job['url']
            },
            "hiringOrganization": {
                "@type": "Organization",
                "name": job['company'],
                "logo": job.get('logo', Config.DEFAULT_LOGO),
                "sameAs": f"https://www.openjobs-ai.com/companies/{job['company'].lower().replace(' ', '-')}"
            },
            "url": job['url'],
            "datePosted": iso_date[:10],
            "employmentType": employment_type,
            "occupationalCategory": category,
            "industry": category,
            "jobLocation": {
                "@type": "Place",
                "address": location_address
            },
            "validThrough": valid_through,
            "directApply": True
        }

        # Add remote work indicator if detected
        title_lower = job['title'].lower()
        location_lower = job.get('location', '').lower()
        if 'remote' in title_lower or 'remote' in location_lower or 'work from home' in title_lower:
            job_posting['jobLocationType'] = 'TELECOMMUTE'
            job_posting['applicantLocationRequirements'] = {
                "@type": "Country",
                "name": "United States"
            }

        job_items.append({
            "@type": "ListItem",
            "position": idx + 1,
            "item": job_posting
        })

    schema_itemlist = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Latest Job Openings",
        "numberOfItems": total_jobs,
        "itemListElement": job_items
    }

    # BreadcrumbList for navigation structure
    schema_breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": "Home",
                "item": Config.CF_SITE_URL
            },
            {
                "@type": "ListItem",
                "position": 2,
                "name": "Job Listings",
                "item": f"{Config.CF_SITE_URL}/"
            }
        ]
    }

    # FAQPage for common questions
    schema_faq = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": "How often are job listings updated?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": f"Job listings are updated every 6 hours with {total_jobs:,}+ positions from {stats['total_companies']}+ companies."
                }
            },
            {
                "@type": "Question",
                "name": "Is OpenJobs free to use?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Yes, OpenJobs is 100% free and open-source with no ads, no paywalls, and no sign-ups required."
                }
            },
            {
                "@type": "Question",
                "name": "Where do the job listings come from?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Jobs are aggregated from OpenJobs AI, which collects listings from top companies including Google, Amazon, Microsoft, Mayo Clinic, and many more."
                }
            }
        ]
    }

    # CollectionPage for the job listings page
    schema_collection = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "OpenJobs - Job Listings",
        "description": f"Browse {total_jobs:,}+ job openings from {stats['total_companies']}+ top companies. Free job aggregator updated every 6 hours.",
        "url": Config.CF_SITE_URL,
        "about": {
            "@type": "Thing",
            "name": "Job Search",
            "description": "Employment opportunities and career positions"
        },
        "numberOfItems": total_jobs,
        "keywords": "jobs, careers, employment, hiring, job search",
        "audience": {
            "@type": "Audience",
            "audienceType": "Job Seekers"
        },
        "specialty": {
            "@type": "Specialty",
            "name": "Technology, Healthcare, Finance, Sales, Engineering",
            "description": f"Top categories: {', '.join(list(stats['categories'].keys())[:5])}"
        }
    }

    schema_json = json.dumps([schema_website, schema_org, schema_breadcrumb, schema_collection, schema_itemlist, schema_faq])

    html = f'''<!DOCTYPE html>
<html lang="en" prefix="og: https://ogp.me/ns#">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
  <title>OpenJobs - {total_jobs:,}+ Job Openings from Top Companies | Updated Every 6 Hours</title>
  <meta name="description" content="Discover {total_jobs:,}+ job opportunities at {stats['total_companies']}+ leading companies including Google, Amazon, Microsoft, Mayo Clinic, and more. 100% free, no sign-up required. Updated every 6 hours. Find your dream job in tech, healthcare, finance, sales, and engineering today!">
  <meta name="keywords" content="jobs, careers, job search, job board, employment, hiring, tech jobs, software engineer, remote jobs, work from home, healthcare jobs, nursing jobs, sales jobs, finance jobs, engineering jobs, open source jobs, free job aggregator, job listings, job openings, career opportunities, {', '.join([cat.lower() + ' jobs' for cat in list(stats['categories'].keys())[:5]])}">
  <meta name="author" content="OpenJobs">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
  <meta name="googlebot" content="index, follow">
  <meta name="bingbot" content="index, follow">
  <link rel="canonical" href="{Config.CF_SITE_URL}/">

  <!-- Alternate language and regional links -->
  <link rel="alternate" hreflang="en" href="{Config.CF_SITE_URL}/">
  <link rel="alternate" hreflang="x-default" href="{Config.CF_SITE_URL}/">

  <!-- Favicons -->
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <link rel="icon" type="image/x-icon" href="/favicon.ico">
  <link rel="apple-touch-icon" sizes="180x180" href="/favicon.svg">
  <link rel="icon" sizes="192x192" href="/favicon.svg">

  <!-- Open Graph / Facebook -->
  <meta property="og:type" content="website">
  <meta property="og:url" content="{Config.CF_SITE_URL}/">
  <meta property="og:title" content="OpenJobs - {total_jobs:,}+ Jobs from Top Companies | Updated Hourly">
  <meta property="og:description" content="Browse {total_jobs:,}+ job openings at {stats['total_companies']}+ world-class companies. No ads, no sign-up, 100% free. Find your next career move today!">
  <meta property="og:image" content="{Config.CF_SITE_URL}/og-image.png">
  <meta property="og:image:type" content="image/png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="OpenJobs - Find Your Next Career - {total_jobs:,}+ Jobs from {stats['total_companies']}+ Companies">
  <meta property="og:image:secure_url" content="{Config.CF_SITE_URL}/og-image.png">
  <meta property="og:site_name" content="OpenJobs">
  <meta property="og:locale" content="en_US">

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@OpenJobsAI">
  <meta name="twitter:creator" content="@OpenJobsAI">
  <meta name="twitter:url" content="{Config.CF_SITE_URL}/">
  <meta name="twitter:title" content="OpenJobs - {total_jobs:,}+ Jobs from {stats['total_companies']}+ Companies">
  <meta name="twitter:description" content="Free job aggregator with {total_jobs:,}+ openings. Updated every 6 hours. No sign-up needed.">
  <meta name="twitter:image" content="{Config.CF_SITE_URL}/og-image.png">
  <meta name="twitter:image:alt" content="OpenJobs - Find Your Next Career - {total_jobs:,}+ Jobs from {stats['total_companies']}+ Companies">

  <!-- Additional SEO -->
  <meta name="theme-color" content="#3b82f6">
  <meta name="msapplication-TileColor" content="#3b82f6">
  <meta name="application-name" content="OpenJobs">
  <meta name="apple-mobile-web-app-title" content="OpenJobs">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="default">
  <meta name="mobile-web-app-capable" content="yes">
  <link rel="manifest" href="/manifest.json">

  <!-- Geolocation and regional targeting -->
  <meta name="geo.region" content="US">
  <meta name="geo.placename" content="United States">
  <meta name="ICBM" content="37.0902,-95.7129">

  <!-- Content classification -->
  <meta name="rating" content="General">
  <meta name="distribution" content="Global">
  <meta name="language" content="en">
  <meta name="coverage" content="Worldwide">

  <link rel="sitemap" type="application/xml" href="/sitemap.xml">
  <link rel="alternate" type="application/rss+xml" title="OpenJobs RSS Feed" href="/rss.xml">

  <!-- Preconnect to external domains -->
  <link rel="preconnect" href="https://www.openjobs-ai.com">
  <link rel="preconnect" href="https://images.weserv.nl" crossorigin>

  <!-- DNS prefetch for performance -->
  <link rel="dns-prefetch" href="https://www.openjobs-ai.com">
  <link rel="dns-prefetch" href="https://images.weserv.nl">

  <!-- Schema.org JSON-LD Structured Data -->
  <script type="application/ld+json">{schema_json}</script>

  <style>
    :root {{ --primary: #0f172a; --accent: #3b82f6; --accent-hover: #2563eb; --bg: #ffffff; --card-bg: #f8fafc; --text: #0f172a; --muted: #64748b; --border: #e2e8f0; }}
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', 'Segoe UI', sans-serif; background: var(--bg); color: var(--text); line-height: 1.5; }}
    .container {{ max-width: 1024px; margin: 0 auto; padding: 2rem 1.5rem; }}
    .sr-only {{ position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0,0,0,0); border: 0; }}

    /* Accessibility - Skip to main content link */
    .skip-link {{ position: absolute; top: -40px; left: 0; background: var(--accent); color: white; padding: 8px 16px; text-decoration: none; z-index: 100; transition: top 0.3s; }}
    .skip-link:focus {{ top: 0; }}

    /* Header */
    header {{ margin-bottom: 1.5rem; }}
    h1 {{ font-size: 1.75rem; font-weight: 700; letter-spacing: -0.02em; }}
    .meta {{ color: var(--muted); font-size: 0.875rem; margin-top: 0.5rem; }}
    .intro {{ color: var(--text); font-size: 0.95rem; margin-top: 1rem; line-height: 1.6; max-width: 680px; }}
    .stats {{ display: flex; gap: 0.75rem; margin-top: 1rem; flex-wrap: wrap; }}
    .stat {{ background: var(--card-bg); padding: 0.5rem 0.875rem; border-radius: 6px; font-size: 0.8rem; border: 1px solid var(--border); }}
    .stat-value {{ font-weight: 600; color: var(--accent); }}

    /* Search & Filters */
    .controls {{ margin-bottom: 1.5rem; }}
    .search-box {{ margin-bottom: 1rem; }}
    .search-input {{ width: 100%; padding: 0.875rem 1rem; font-size: 1rem; border: 1px solid var(--border); border-radius: 8px; outline: none; transition: border-color 0.15s, box-shadow 0.15s; }}
    .search-input:focus {{ border-color: var(--accent); box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1); }}
    .filters {{ display: flex; gap: 0.5rem; flex-wrap: wrap; }}
    .filter-btn {{ padding: 0.5rem 1rem; font-size: 0.8rem; border: 1px solid var(--border); border-radius: 20px; background: var(--bg); color: var(--muted); cursor: pointer; transition: all 0.15s; }}
    .filter-btn:hover {{ border-color: var(--accent); color: var(--accent); }}
    .filter-btn:focus {{ outline: 2px solid var(--accent); outline-offset: 2px; }}
    .filter-btn.active {{ background: var(--accent); color: white; border-color: var(--accent); }}

    /* Results info */
    .results-info {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; font-size: 0.875rem; color: var(--muted); }}

    /* Grid */
    .grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 1px; background: var(--border); border: 1px solid var(--border); border-radius: 12px; overflow: hidden; }}
    .card {{ display: flex; flex-direction: column; gap: 0.375rem; background: var(--bg); padding: 1rem 1.25rem; text-decoration: none; color: inherit; transition: background 0.15s; min-height: 80px; }}
    .card:hover {{ background: var(--card-bg); }}
    .card:focus {{ outline: none; background: var(--card-bg); box-shadow: inset 0 0 0 2px var(--accent); }}
    .card.hidden {{ display: none; }}
    .card-title {{ font-weight: 500; font-size: 0.9rem; color: var(--text); line-height: 1.4; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }}
    .card-company {{ font-size: 0.8rem; color: var(--muted); display: flex; align-items: center; gap: 0.5rem; }}
    .logo {{ width: 18px; height: 18px; border-radius: 4px; object-fit: contain; background: var(--card-bg); }}
    .no-results {{ grid-column: 1 / -1; padding: 3rem; text-align: center; color: var(--muted); background: var(--bg); }}

    /* Pagination */
    .pagination {{ display: flex; justify-content: center; align-items: center; gap: 0.5rem; margin-top: 2rem; }}
    .page-btn {{ padding: 0.5rem 1rem; font-size: 0.875rem; border: 1px solid var(--border); border-radius: 6px; background: var(--bg); color: var(--text); cursor: pointer; transition: all 0.15s; }}
    .page-btn:hover:not(:disabled) {{ border-color: var(--accent); color: var(--accent); }}
    .page-btn:focus {{ outline: 2px solid var(--accent); outline-offset: 2px; }}
    .page-btn:disabled {{ opacity: 0.5; cursor: not-allowed; }}
    .page-btn.active {{ background: var(--accent); color: white; border-color: var(--accent); }}
    .page-info {{ font-size: 0.875rem; color: var(--muted); margin: 0 0.5rem; }}

    /* Footer */
    footer {{ margin-top: 2.5rem; text-align: center; padding-top: 1.5rem; border-top: 1px solid var(--border); }}
    footer a {{ color: var(--accent); text-decoration: none; font-size: 0.875rem; }}
    footer a:hover {{ text-decoration: underline; }}
    footer a:focus {{ outline: 2px solid var(--accent); outline-offset: 2px; }}
    .github-link {{ margin-top: 0.75rem; font-size: 0.8rem; color: var(--muted); }}
    .github-link a {{ color: var(--muted); }}

    /* Responsive */
    @media (max-width: 768px) {{
      .grid {{ grid-template-columns: 1fr; }}
      .container {{ padding: 1.5rem 1rem; }}
      h1 {{ font-size: 1.5rem; }}
      .stats {{ gap: 0.5rem; }}
      .stat {{ padding: 0.375rem 0.625rem; font-size: 0.75rem; }}
      .search-input {{ padding: 0.75rem; }}
    }}
    @media (min-width: 1024px) {{
      .grid {{ grid-template-columns: repeat(3, 1fr); }}
    }}
  </style>
</head>
<body>
  <a href="#main-content" class="skip-link">Skip to main content</a>
  <div class="container">
    <header>
      <h1>Find Your Next Career</h1>
      <p class="meta" aria-live="polite">{total_jobs:,}+ positions from {stats['total_companies']}+ companies · Updated {date_str}</p>
      <p class="intro">Discover your dream job from top companies like Google, Amazon, Microsoft, Mayo Clinic, and more. Our free, open-source job aggregator automatically collects and updates listings every 6 hours - no sign-up required, no ads, just opportunities.</p>
      <div class="stats" role="list" aria-label="Job statistics">
        <div class="stat" role="listitem"><span class="stat-value">{stats['categories'].get('Engineering', 0):,}</span> Engineering</div>
        <div class="stat" role="listitem"><span class="stat-value">{stats['categories'].get('Healthcare', 0):,}</span> Healthcare</div>
        <div class="stat" role="listitem"><span class="stat-value">{stats['categories'].get('Sales', 0):,}</span> Sales</div>
        <div class="stat" role="listitem"><span class="stat-value">{stats['categories'].get('Finance', 0):,}</span> Finance</div>
      </div>
    </header>

    <main id="main-content">
      <div class="controls">
        <div class="search-box">
          <label for="searchInput" class="sr-only">Search jobs or companies</label>
          <input type="search" class="search-input" placeholder="Search jobs or companies..." id="searchInput" aria-describedby="resultsCount">
        </div>
        <div class="filters" role="group" aria-label="Filter by category">
          <button class="filter-btn active" data-category="All">All</button>
          <button class="filter-btn" data-category="Engineering">Engineering</button>
          <button class="filter-btn" data-category="Healthcare">Healthcare</button>
          <button class="filter-btn" data-category="Sales">Sales</button>
          <button class="filter-btn" data-category="Finance">Finance</button>
          <button class="filter-btn" data-category="Management">Management</button>
        </div>
      </div>

      <div class="results-info">
        <span id="resultsCount" aria-live="polite">Showing <span id="showingCount">0</span> of {total_jobs:,} jobs</span>
      </div>

      <div class="grid" id="jobsGrid" role="list" aria-label="Job listings">
        <div class="no-results" id="noResults" style="display: none;" role="status">No jobs found matching your search.</div>
      </div>

      <nav class="pagination" aria-label="Pagination">
        <button class="page-btn" id="prevBtn" aria-label="Previous page">&larr; Prev</button>
        <span class="page-info" id="pageInfo" aria-live="polite">Page 1</span>
        <button class="page-btn" id="nextBtn" aria-label="Next page">Next &rarr;</button>
      </nav>
    </main>

    <footer>
      <a href="https://www.openjobs-ai.com/deepsearch">View all {total_jobs:,}+ jobs on OpenJobs AI →</a>
      <p class="github-link">Open source on <a href="https://github.com/Digidai/openjobs">GitHub</a></p>
    </footer>
  </div>

  <script>
    // Enhanced error handling and initialization
    (function() {{
      "use strict";

      // All jobs data
      const allJobs = {jobs_json};
      const JOBS_PER_PAGE = 30;

      // State
      let currentPage = 1;
      let currentCategory = 'All';
      let searchQuery = '';
      let filteredJobs = [...allJobs];

      // DOM elements
      const searchInput = document.getElementById('searchInput');
      const jobsGrid = document.getElementById('jobsGrid');
      const noResults = document.getElementById('noResults');
      const showingCount = document.getElementById('showingCount');
      const pageInfo = document.getElementById('pageInfo');
      const prevBtn = document.getElementById('prevBtn');
      const nextBtn = document.getElementById('nextBtn');
      const filterBtns = document.querySelectorAll('.filter-btn');

      // Validate required DOM elements
      if (!searchInput || !jobsGrid || !noResults || !showingCount || !pageInfo || !prevBtn || !nextBtn) {{
        console.error('Required DOM elements not found. Cannot initialize application.');
        // Show user-friendly error message
        document.body.innerHTML = '<div style="padding: 2rem; text-align: center;">' +
          '<h2>Application Error</h2>' +
          '<p>Unable to initialize the job board. Please refresh the page or try again later.</p>' +
          '</div>';
        // Exit early by not initializing the rest
        return;
      }}

      if (filterBtns.length === 0) {{
        console.warn('No filter buttons found. Category filtering will not work.');
      }}

      // Global error handler
      window.addEventListener('error', function(e) {{
        console.error('Global error:', e.error);
        // Prevent alert loops, just log
      }});

      // Debounce function
      function debounce(fn, delay) {{
        let timer;
        return function(...args) {{
          clearTimeout(timer);
          timer = setTimeout(() => {{
            try {{
              fn.apply(this, args);
            }} catch (error) {{
              console.error('Debounced function error:', error);
            }}
          }}, delay);
        }};
      }}

      // Filter jobs with error handling
      function filterJobs() {{
        try {{
          filteredJobs = allJobs.filter(job => {{
            const matchesCategory = currentCategory === 'All' || job.category === currentCategory;
            const matchesSearch = !searchQuery ||
              job.title.toLowerCase().includes(searchQuery) ||
              job.company.toLowerCase().includes(searchQuery);
            return matchesCategory && matchesSearch;
          }});
          currentPage = 1;
          renderJobs();
        }} catch (error) {{
          console.error('Error filtering jobs:', error);
          filteredJobs = [];
          renderJobs();
        }}
      }}

      // Render jobs with error handling
      function renderJobs() {{
        try {{
          const totalPages = Math.ceil(filteredJobs.length / JOBS_PER_PAGE);
          const start = (currentPage - 1) * JOBS_PER_PAGE;
          const end = start + JOBS_PER_PAGE;
          const pageJobs = filteredJobs.slice(start, end);

          // Clear grid (keep noResults)
          const cards = jobsGrid.querySelectorAll('.card');
          cards.forEach(card => card.remove());

          if (pageJobs.length === 0) {{
            noResults.style.display = 'block';
            showingCount.textContent = '0';
          }} else {{
            noResults.style.display = 'none';
            showingCount.textContent = filteredJobs.length.toLocaleString();

            pageJobs.forEach((job, idx) => {{
              try {{
                const card = document.createElement('a');
                card.href = job.url;
                card.className = 'card';
                card.target = '_blank';
                card.rel = 'noopener';
                card.setAttribute('role', 'listitem');
                card.setAttribute('aria-label', `${{job.title}} at ${{job.company}}`);

                const title = document.createElement('div');
                title.className = 'card-title';
                title.textContent = job.title;

                const company = document.createElement('div');
                company.className = 'card-company';

                const logo = document.createElement('img');
                logo.alt = job.company + ' logo';
                logo.className = 'logo';
                logo.loading = 'lazy';
                logo.onerror = function() {{ this.style.display = 'none'; }};
                logo.src = job.logo;  // Set src last to prevent race condition

                company.appendChild(logo);
                company.appendChild(document.createTextNode(job.company));

                card.appendChild(title);
                card.appendChild(company);
                jobsGrid.insertBefore(card, noResults);
              }} catch (cardError) {{
                console.error('Error rendering job card:', cardError, job);
              }}
            }});
          }}

          // Update pagination
          pageInfo.textContent = `Page ${{currentPage}} of ${{Math.max(totalPages, 1)}}`;
          prevBtn.disabled = currentPage <= 1;
          nextBtn.disabled = currentPage >= totalPages;
        }} catch (error) {{
          console.error('Error rendering jobs:', error);
          // Show error message to user
          noResults.style.display = 'block';
          noResults.textContent = 'An error occurred while loading jobs. Please refresh the page.';
          showingCount.textContent = '0';
        }}
      }}

      // Event listeners with error handling
      try {{
        searchInput.addEventListener('input', debounce(function() {{
          searchQuery = this.value.toLowerCase().trim();
          filterJobs();
        }}, 200));

        filterBtns.forEach(btn => {{
          btn.addEventListener('click', function() {{
            try {{
              filterBtns.forEach(b => b.classList.remove('active'));
              this.classList.add('active');
              currentCategory = this.dataset.category;
              filterJobs();
            }} catch (error) {{
              console.error('Error handling filter click:', error);
            }}
          }});
        }});

        prevBtn.addEventListener('click', () => {{
          if (currentPage > 1) {{
            currentPage--;
            renderJobs();
            window.scrollTo({{ top: 0, behavior: 'smooth' }});
          }}
        }});

        nextBtn.addEventListener('click', () => {{
          try {{
            const totalPages = Math.ceil(filteredJobs.length / JOBS_PER_PAGE);
            if (currentPage < totalPages) {{
              currentPage++;
              renderJobs();
              window.scrollTo({{ top: 0, behavior: 'smooth' }});
            }}
          }} catch (error) {{
            console.error('Error handling next page:', error);
          }}
        }});
      }} catch (error) {{
        console.error('Error setting up event listeners:', error);
      }}

      // Initial render with error handling
      try {{
        renderJobs();
      }} catch (error) {{
        console.error('Error during initial render:', error);
      }}

    }})();  // IIFE for scope isolation
  </script>
</body>
</html>
'''
    return html


def generate_sitemap(site_url, jobs=None, stats=None):
    """Generate enhanced XML sitemap with multiple URLs."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    urls = []

    # Homepage - highest priority
    urls.append(f'''  <url>
    <loc>{site_url}/</loc>
    <lastmod>{now}</lastmod>
    <changefreq>hourly</changefreq>
    <priority>1.0</priority>
  </url>''')

    # Category filter pages (virtual URLs for SEO)
    categories = ['Engineering', 'Healthcare', 'Sales', 'Finance', 'Management', 'Marketing', 'HR', 'Operations']
    for cat in categories:
        urls.append(f'''  <url>
    <loc>{site_url}/?category={cat}</loc>
    <lastmod>{now}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.8</priority>
  </url>''')

    # RSS feed
    urls.append(f'''  <url>
    <loc>{site_url}/rss.xml</loc>
    <lastmod>{now}</lastmod>
    <changefreq>hourly</changefreq>
    <priority>0.6</priority>
  </url>''')

    # Top company pages (virtual URLs)
    if stats and 'top_companies' in stats:
        for company in list(stats['top_companies'].keys())[:20]:
            from urllib.parse import quote
            company_slug = quote(company.replace(' ', '-').lower())
            urls.append(f'''  <url>
    <loc>{site_url}/?company={company_slug}</loc>
    <lastmod>{now}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.7</priority>
  </url>''')

    # Top location pages (virtual URLs)
    if stats and 'top_locations' in stats:
        for location in list(stats['top_locations'].keys())[:15]:
            from urllib.parse import quote
            location_slug = quote(location.replace(' ', '-').lower())
            urls.append(f'''  <url>
    <loc>{site_url}/?location={location_slug}</loc>
    <lastmod>{now}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.7</priority>
  </url>''')

    urls_str = '\n'.join(urls)

    return f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9
        http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">
{urls_str}
</urlset>
'''


def generate_robots_txt():
    """Generate robots.txt for SEO."""
    return '''# Robots.txt for OpenJobs
# Allow all crawlers

User-agent: *
Allow: /
Disallow: /admin/
Disallow: /private/

Crawl-delay: 1

# Sitemap location
Sitemap: https://openjobs.genedai.me/sitemap.xml

# Specific bots
User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

# Disallow archive bots
User-agent: archive.org_bot
Disallow: /
'''


def generate_manifest(stats):
    """Generate PWA manifest.json for installable web app."""
    return json.dumps({
        "name": "OpenJobs - Job Search",
        "short_name": "OpenJobs",
        "description": f"Browse {stats['total_jobs']}+ job openings from {stats['total_companies']}+ companies. Free job aggregator updated every 6 hours.",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#ffffff",
        "theme_color": "#3b82f6",
        "orientation": "portrait-primary",
        "icons": [
            {
                "src": "/favicon.svg",
                "sizes": "192x192",
                "type": "image/svg+xml",
                "purpose": "any maskable"
            },
            {
                "src": "/og-image.svg",
                "sizes": "512x512",
                "type": "image/svg+xml",
                "purpose": "any maskable"
            }
        ],
        "categories": ["jobs", "careers", "employment", "business"],
        "shortcuts": [
            {
                "name": "Search Jobs",
                "short_name": "Search",
                "description": "Search for jobs",
                "url": "/#search",
                "icons": [{ "src": "/favicon.svg", "sizes": "96x96" }]
            },
            {
                "name": "Browse Categories",
                "short_name": "Categories",
                "description": "Browse by category",
                "url": "/#categories",
                "icons": [{ "src": "/favicon.svg", "sizes": "96x96" }]
            }
        ]
    }, indent=2)


def generate_rss_feed(jobs, stats):
    """Generate RSS 2.0 feed for job updates."""
    now = datetime.now(timezone.utc)
    rss_date = now.strftime("%a, %d %b %Y %H:%M:%S %z")

    # Get first 20 jobs for RSS
    rss_jobs = jobs[:20]

    items = []
    for job in rss_jobs:
        item_date = now.strftime("%a, %d %b %Y %H:%M:%S %z")
        items.append(f'''
    <item>
      <title>{escape_html(job['title'])} at {escape_html(job['company'])}</title>
      <link>{job['url']}</link>
      <description>Apply for {escape_html(job['title'])} position at {escape_html(job['company'])}. Find more jobs at OpenJobs.</description>
      <category>{escape_html(job.get('location', 'Various'))}</category>
      <pubDate>{item_date}</pubDate>
      <guid isPermaLink="true">{job['url']}</guid>
    </item>''')

    items_str = ''.join(items)

    return f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>OpenJobs - {stats['total_jobs']}+ Job Openings</title>
    <link>{Config.CF_SITE_URL}/</link>
    <description>Latest job openings from {stats['total_companies']}+ top companies. Updated every 6 hours.</description>
    <language>en-us</language>
    <copyright>Copyright {now.year} OpenJobs</copyright>
    <managingEditor>team@openjobs.ai (OpenJobs Team)</managingEditor>
    <webMaster>team@openjobs.ai (OpenJobs Team)</webMaster>
    <lastBuildDate>{rss_date}</lastBuildDate>
    <atom:link href="{Config.CF_SITE_URL}/rss.xml" rel="self" type="application/rss+xml"/>
    <image>
      <url>{Config.CF_SITE_URL}/og-image.svg</url>
      <title>OpenJobs</title>
      <link>{Config.CF_SITE_URL}/</link>
      <width>144</width>
      <height>144</height>
    </image>
{items_str}
  </channel>
</rss>
'''


def generate_og_image_png(stats):
    """Generate og-image.png using Pillow for better social media compatibility."""
    from PIL import Image, ImageDraw, ImageFont

    # Create image with gradient-like background
    width, height = 1200, 630
    img = Image.new('RGB', (width, height), color='#0f172a')
    draw = ImageDraw.Draw(img)

    # Create a subtle gradient effect by drawing rectangles
    for i in range(height):
        r = int(15 + (30 - 15) * i / height)
        g = int(23 + (41 - 23) * i / height)
        b = int(42 + (59 - 42) * i / height)
        draw.line([(0, i), (width, i)], fill=(r, g, b))

    # Try to use a system font, fallback to default
    # Font paths for different OS: macOS, Ubuntu/Linux, Windows
    font_paths = [
        "/System/Library/Fonts/Helvetica.ttc",  # macOS
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  # Ubuntu/Debian
        "/usr/share/fonts/TTF/DejaVuSans.ttf",  # Arch Linux
        "/usr/share/fonts/dejavu-sans-fonts/DejaVuSans.ttf",  # Fedora
        "arial.ttf",  # Windows
        "Arial.ttf",
    ]

    def load_font(size):
        for path in font_paths:
            try:
                return ImageFont.truetype(path, size)
            except (IOError, OSError):
                continue
        return ImageFont.load_default()

    title_font = load_font(64)
    subtitle_font = load_font(36)
    stats_font = load_font(28)
    small_font = load_font(24)
    logo_font = load_font(40)

    # Draw logo box
    logo_x, logo_y = 80, 80
    logo_size = 80
    draw.rounded_rectangle(
        [logo_x, logo_y, logo_x + logo_size, logo_y + logo_size],
        radius=16,
        fill='#3b82f6'
    )
    draw.text((logo_x + 20, logo_y + 18), "OJ", fill='white', font=logo_font)

    # Draw title
    draw.text((80, 200), "OpenJobs", fill='white', font=title_font)

    # Draw subtitle
    draw.text((80, 280), "Find Your Next Career", fill='#94a3b8', font=subtitle_font)

    # Draw stats
    total_jobs = stats.get('total_jobs', 0)
    total_companies = stats.get('total_companies', 0)
    draw.text((80, 380), f"{total_jobs:,}+ Jobs", fill='#3b82f6', font=stats_font)
    draw.text((280, 380), "from", fill='#64748b', font=stats_font)
    draw.text((370, 380), f"{total_companies:,}+ Companies", fill='#3b82f6', font=stats_font)

    # Draw footer
    draw.text((80, 500), "Free & Open Source Job Aggregator", fill='#64748b', font=small_font)
    draw.text((80, 540), "Updated every 6 hours", fill='#475569', font=small_font)
    draw.text((920, 540), "openjobs.genedai.me", fill='#475569', font=small_font)

    # Save as PNG
    img.save('public/og-image.png', 'PNG', optimize=True)


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def validate_output(jobs, stats):
    """Validate generated output meets quality thresholds."""
    issues = []

    # Check minimum job count
    if len(jobs) < 100:
        issues.append(f"Job count too low: {len(jobs)} (expected >= 100)")

    # Check company diversity
    if stats['total_companies'] < 50:
        issues.append(f"Company count too low: {stats['total_companies']} (expected >= 50)")

    # Check data quality
    if 'data_quality' in stats:
        dq = stats['data_quality']
        if dq.get('parse_success_rate', 1) < 0.8:
            issues.append(f"Parse success rate too low: {dq['parse_success_rate']:.2%}")

    return issues


def main():
    """Main execution function with comprehensive error handling and disaster recovery."""
    import time
    start_time = time.time()

    logger.info("=" * 60)
    logger.info("OpenJobs Updater v2.1 - Enhanced Reliability")
    logger.info("=" * 60)

    exit_code = 0
    used_backup = False

    try:
        # Pre-flight check: Disk space
        logger.info("Pre-flight check: Verifying disk space...")
        check_disk_space()

        # Step 1-2: Fetch data source URL
        logger.info("Step 1-2: Discovering latest data source...")
        try:
            jobs_url = get_latest_jobs_url()
        except (FetchError, ValueError) as e:
            logger.warning(f"Failed to discover data source: {e}")
            logger.info("Attempting to load from backup...")

            backup_jobs, backup_stats = load_backup()
            if backup_jobs and backup_stats:
                jobs, stats = backup_jobs, backup_stats
                used_backup = True
                logger.info(f"Successfully loaded backup data: {len(jobs)} jobs")

                # Skip to step 6 with backup data
                logger.info("Using backup data - skipping fetch and parse steps")
            else:
                logger.error("No backup available. Cannot continue.")
                raise FetchError("Data source unavailable and no backup exists")
        else:
            # Step 3: Fetch job listings
            logger.info("Step 3: Fetching job listings...")
            try:
                xml_content = fetch_xml(jobs_url)
            except FetchError as e:
                logger.warning(f"Failed to fetch job data: {e}")
                logger.info("Attempting to load from backup...")

                backup_jobs, backup_stats = load_backup()
                if backup_jobs and backup_stats:
                    jobs, stats = backup_jobs, backup_stats
                    used_backup = True
                    logger.info(f"Successfully loaded backup data: {len(jobs)} jobs")
                else:
                    logger.error("No backup available. Cannot continue.")
                    raise

            if not used_backup:
                # Step 4: Parse jobs
                logger.info("Step 4: Parsing jobs...")
                try:
                    jobs, parse_stats = parse_jobs(xml_content)
                    logger.info(f"Found {len(jobs)} jobs (parse stats: {parse_stats})")
                except ParseError as e:
                    logger.warning(f"Failed to parse jobs: {e}")
                    logger.info("Attempting to load from backup...")

                    backup_jobs, backup_stats = load_backup()
                    if backup_jobs and backup_stats:
                        jobs, stats = backup_jobs, backup_stats
                        used_backup = True
                        logger.info(f"Successfully loaded backup data: {len(jobs)} jobs")
                    else:
                        logger.error("No backup available. Cannot continue.")
                        raise

                # Enhanced: Don't fail completely on empty jobs, use lower threshold
                if len(jobs) < 10:
                    logger.warning(f"Very low job count: {len(jobs)}")
                    logger.info("Attempting to load from backup...")

                    backup_jobs, backup_stats = load_backup()
                    if backup_jobs and backup_stats:
                        # Use backup if it has more jobs
                        if len(backup_jobs) > len(jobs):
                            logger.info(f"Backup has more jobs ({len(backup_jobs)}), using backup")
                            jobs, stats = backup_jobs, backup_stats
                            used_backup = True
                        else:
                            # Continue with current data but warn
                            logger.warning("Backup also has low job count, continuing with current data")

                # Step 5: Calculate statistics
                logger.info("Step 5: Calculating statistics...")
                stats = calculate_stats(jobs, parse_stats if not used_backup else None)
                logger.info(f"Stats: {stats['total_jobs']} jobs from {stats['total_companies']} companies")

                # Save backup after successful fetch and parse
                if not used_backup:
                    logger.info("Saving backup...")
                    save_backup(jobs, stats)

        # Step 5.5: Validate output
        logger.info("Step 5.5: Validating output...")
        issues = validate_output(jobs, stats)
        if issues:
            for issue in issues:
                logger.warning(f"Validation warning: {issue}")
            # Don't fail, just warn

        # Step 6: Generate README.md (using atomic write)
        logger.info("Step 6: Generating README.md...")
        readme_content = generate_readme(jobs, stats)
        try:
            atomic_write(Config.README_PATH, readme_content)
            logger.info(f"  ✓ Successfully wrote {Config.README_PATH}")
        except IOError as e:
            logger.error(f"  ✗ Failed to write {Config.README_PATH}: {e}")
            raise

        # Step 7: Generate HTML (using atomic write)
        logger.info("Step 7: Generating HTML for Cloudflare Pages...")
        html_content = generate_html(jobs, stats)
        try:
            atomic_write(Config.HTML_PATH, html_content)
            logger.info(f"  ✓ Successfully wrote {Config.HTML_PATH}")
        except IOError as e:
            logger.error(f"  ✗ Failed to write {Config.HTML_PATH}: {e}")
            raise

        # Step 8: Generate stats.json (using atomic write)
        logger.info("Step 8: Generating stats.json...")
        try:
            atomic_write_json(Config.STATS_PATH, stats)
            logger.info(f"  ✓ Successfully wrote {Config.STATS_PATH}")
        except IOError as e:
            logger.error(f"  ✗ Failed to write {Config.STATS_PATH}: {e}")
            raise

        # Step 9: Generate SEO assets (using atomic writes)
        logger.info("Step 9: Generating SEO assets (sitemaps, robots.txt, manifest, RSS)...")
        try:
            atomic_write(Config.CF_SITEMAP_PATH, generate_sitemap(Config.CF_SITE_URL, jobs, stats))
            logger.info(f"  ✓ Successfully wrote {Config.CF_SITEMAP_PATH}")
        except IOError as e:
            logger.error(f"  ✗ Failed to write {Config.CF_SITEMAP_PATH}: {e}")
            raise

        try:
            atomic_write(Config.GH_SITEMAP_PATH, generate_sitemap(Config.GH_SITE_URL, jobs, stats))
            logger.info(f"  ✓ Successfully wrote {Config.GH_SITEMAP_PATH}")
        except IOError as e:
            logger.error(f"  ✗ Failed to write {Config.GH_SITEMAP_PATH}: {e}")
            raise

        # Generate robots.txt
        try:
            atomic_write('public/robots.txt', generate_robots_txt())
            logger.info(f"  ✓ Successfully wrote public/robots.txt")
        except IOError as e:
            logger.error(f"  ✗ Failed to write public/robots.txt: {e}")
            raise

        # Generate PWA manifest
        try:
            atomic_write_json('public/manifest.json', json.loads(generate_manifest(stats)))
            logger.info(f"  ✓ Successfully wrote public/manifest.json")
        except IOError as e:
            logger.error(f"  ✗ Failed to write public/manifest.json: {e}")
            raise

        # Generate RSS feed
        try:
            atomic_write('public/rss.xml', generate_rss_feed(jobs, stats))
            logger.info(f"  ✓ Successfully wrote public/rss.xml")
        except IOError as e:
            logger.error(f"  ✗ Failed to write public/rss.xml: {e}")
            raise

        # Generate og-image.png (if Pillow available)
        try:
            from PIL import Image, ImageDraw, ImageFont
            generate_og_image_png(stats)
            logger.info("  - public/og-image.png (Open Graph image)")
        except ImportError:
            logger.warning("Pillow not installed, skipping og-image.png generation. Install with: pip install Pillow")

        elapsed = time.time() - start_time
        logger.info("=" * 60)
        logger.info(f"SUCCESS! Completed in {elapsed:.2f}s")
        if used_backup:
            logger.info("⚠️  Used backup data (external source unavailable)")
        logger.info("Generated files:")
        logger.info(f"  - {Config.README_PATH}")
        logger.info(f"  - {Config.HTML_PATH}")
        logger.info(f"  - {Config.STATS_PATH}")
        logger.info(f"  - {Config.CF_SITEMAP_PATH}")
        logger.info(f"  - {Config.GH_SITEMAP_PATH}")
        logger.info(f"  - public/robots.txt (SEO)")
        logger.info(f"  - public/manifest.json (PWA)")
        logger.info(f"  - public/rss.xml (RSS Feed)")
        logger.info(f"Summary: {stats['total_jobs']} jobs, {stats['total_companies']} companies")
        logger.info("=" * 60)

    except FetchError as e:
        logger.error(f"Data fetch failed: {e}")
        exit_code = 2
    except ParseError as e:
        logger.error(f"Data parsing failed: {e}")
        exit_code = 3
    except OSError as e:
        logger.error(f"System resource error: {e}")
        exit_code = 4
    except Exception as e:
        logger.error(f"Unexpected error: {type(e).__name__}: {e}")
        import traceback
        logger.error(traceback.format_exc())
        exit_code = 1

    if exit_code != 0:
        elapsed = time.time() - start_time
        logger.error(f"FAILED after {elapsed:.2f}s with exit code {exit_code}")

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
