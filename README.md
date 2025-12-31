<p align="center">
  <img src="https://img.shields.io/badge/jobs-252+-blue?style=for-the-badge" alt="Jobs Count">
  <img src="https://img.shields.io/badge/companies-121+-purple?style=for-the-badge" alt="Companies">
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
- **Auto-Updated Every 6 Hours** - Fresh jobs from 121+ companies via GitHub Actions
- **Zero Infrastructure** - Runs entirely on GitHub Pages + Cloudflare (free tier)
- **Lightweight** - Pure Python, no external dependencies, <1MB total size
- **SEO Optimized** - Proper sitemaps, meta tags, and structured content

## Job Statistics

| Category | Count |
|----------|------:|
| Other | 160 |
| Healthcare | 33 |
| Engineering | 25 |
| Management | 12 |
| Finance | 6 |
| Marketing | 5 |
| Sales | 4 |
| HR | 4 |
| Operations | 3 |

**Top Hiring Companies:** Varsity Tutors, a Nerdy Company, Eaton, micro1, Hire With Near, Thomson Reuters

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
│  │ Sitemap     │   │ (252+ jobs) │   │ (README + HTML)     │   │
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
- **And 121+ other companies**

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
  <em>Updated December 31, 2025 · Showing 200 of 252+ jobs</em>
</p>

| Job Title | Company | Apply |
|-----------|---------|:-----:|
| Elementary School English Tutor | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/96/01490799486dac16a48801deb8255.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Varsity Tutors, a Nerdy Company | [View](https://www.openjobs-ai.com/jobs/elementary-school-english-tutor-stamford-ct-118970132725762614) |
| Math Tutor | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/96/01490799486dac16a48801deb8255.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Varsity Tutors, a Nerdy Company | [View](https://www.openjobs-ai.com/jobs/math-tutor-new-haven-ct-118970132725762615) |
| SAT Tutor | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/96/01490799486dac16a48801deb8255.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Varsity Tutors, a Nerdy Company | [View](https://www.openjobs-ai.com/jobs/sat-tutor-fort-lauderdale-fl-118970132725762616) |
| Quickbooks Tutor | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/96/01490799486dac16a48801deb8255.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Varsity Tutors, a Nerdy Company | [View](https://www.openjobs-ai.com/jobs/quickbooks-tutor-austin-tx-118970132725762617) |
| ARDMS | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/96/01490799486dac16a48801deb8255.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> RDCS | [View](https://www.openjobs-ai.com/jobs/ardms-rdcs-pediatric-echocardiography-pe-tutor-nashville-tn-118970132725762618) |
| SAT Writing and Language Tutor | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/96/01490799486dac16a48801deb8255.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Varsity Tutors, a Nerdy Company | [View](https://www.openjobs-ai.com/jobs/sat-writing-and-language-tutor-oklahoma-city-ok-118970132725762619) |
| Web Design Tutor | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/96/01490799486dac16a48801deb8255.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Varsity Tutors, a Nerdy Company | [View](https://www.openjobs-ai.com/jobs/web-design-tutor-st-paul-mn-118970132725762620) |
| PSAT Mathematics Tutor | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/96/01490799486dac16a48801deb8255.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Varsity Tutors, a Nerdy Company | [View](https://www.openjobs-ai.com/jobs/psat-mathematics-tutor-baton-rouge-la-118970132725762621) |
| Acquisition Sales Specialist - AI Solutions | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/0/29/bccac6ab1bba6592027aea13777f1.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Thomson Reuters | [View](https://www.openjobs-ai.com/jobs/acquisition-sales-specialist-ai-solutions-new-york-ny-118970132725762622) |
| Lead Software Engineer, AI | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/0/29/bccac6ab1bba6592027aea13777f1.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Thomson Reuters | [View](https://www.openjobs-ai.com/jobs/lead-software-engineer-ai-eagan-mn-118970132725762623) |
| AP World History Tutors (Instant) | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/96/01490799486dac16a48801deb8255.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Varsity Tutors, a Nerdy Company | [View](https://www.openjobs-ai.com/jobs/ap-world-history-tutors-instant-atlanta-ga-118970132725762624) |
| HSPT Math Tutors (Instant) | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/96/01490799486dac16a48801deb8255.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Varsity Tutors, a Nerdy Company | [View](https://www.openjobs-ai.com/jobs/hspt-math-tutors-instant-minneapolis-mn-118970132725762625) |
| CNA - Certified Nursing Assistant | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/5/ea/665518b12c6afac40d738caf99cf9.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> National Health Care Associates | [View](https://www.openjobs-ai.com/jobs/cna-certified-nursing-assistant-marlborough-ma-118970132725762626) |
| Specialist Learning Operations - Caseyville, IL | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/b/7c/85930fb407cdc32b368b762c9ee3d.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Tyson Foods | [View](https://www.openjobs-ai.com/jobs/specialist-learning-operations-caseyville-il-springdale-ar-118970132725762627) |
| Registered Nurse Critical Care Float Pool, Nights – VUH | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/9/48/74f0949b7736752da518b078f098b.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Vanderbilt University Medical Center | [View](https://www.openjobs-ai.com/jobs/registered-nurse-critical-care-float-pool-nights-vuh-nashville-metropolitan-area-118970132725762628) |
| Production Manager | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/1/bd/12cd729942323481c1637fda20e3f.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> 100% Chiropractic Franchise | [View](https://www.openjobs-ai.com/jobs/production-manager-beaver-falls-pa-118970132725762629) |
| Middle School English Tutor | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/96/01490799486dac16a48801deb8255.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Varsity Tutors, a Nerdy Company | [View](https://www.openjobs-ai.com/jobs/middle-school-english-tutor-united-states-118970132725762630) |
| EAS - Educating All Students (NY Teaching exam) Tutor | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/96/01490799486dac16a48801deb8255.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Varsity Tutors, a Nerdy Company | [View](https://www.openjobs-ai.com/jobs/eas-educating-all-students-ny-teaching-exam-tutor-ohio-united-states-118970132725762631) |
| AP Biology Tutor | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/96/01490799486dac16a48801deb8255.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Varsity Tutors, a Nerdy Company | [View](https://www.openjobs-ai.com/jobs/ap-biology-tutor-iowa-united-states-118970132725762632) |
| Java Tutor | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/96/01490799486dac16a48801deb8255.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Varsity Tutors, a Nerdy Company | [View](https://www.openjobs-ai.com/jobs/java-tutor-united-states-118970132725762633) |
| Calculus 2 Tutor | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/96/01490799486dac16a48801deb8255.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Varsity Tutors, a Nerdy Company | [View](https://www.openjobs-ai.com/jobs/calculus-2-tutor-united-states-118970132725762634) |
| AP Calculus AB Tutor | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/96/01490799486dac16a48801deb8255.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Varsity Tutors, a Nerdy Company | [View](https://www.openjobs-ai.com/jobs/ap-calculus-ab-tutor-united-states-118970132725762635) |
| AP Calculus BC Tutor | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/96/01490799486dac16a48801deb8255.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Varsity Tutors, a Nerdy Company | [View](https://www.openjobs-ai.com/jobs/ap-calculus-bc-tutor-ohio-united-states-118970132725762636) |
| Aerospace Engineering Tutor | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/96/01490799486dac16a48801deb8255.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Varsity Tutors, a Nerdy Company | [View](https://www.openjobs-ai.com/jobs/aerospace-engineering-tutor-united-states-118970132725762637) |
| VTNE - Veterinary Technician National Exam Tutor | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/96/01490799486dac16a48801deb8255.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Varsity Tutors, a Nerdy Company | [View](https://www.openjobs-ai.com/jobs/vtne-veterinary-technician-national-exam-tutor-united-states-118970132725762638) |
| AP Computer Science A Tutor | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/96/01490799486dac16a48801deb8255.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Varsity Tutors, a Nerdy Company | [View](https://www.openjobs-ai.com/jobs/ap-computer-science-a-tutor-united-states-118970132725762639) |
| College Biology Tutor | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/96/01490799486dac16a48801deb8255.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Varsity Tutors, a Nerdy Company | [View](https://www.openjobs-ai.com/jobs/college-biology-tutor-tennessee-united-states-118970132725762640) |
| High School Physics Tutor | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/96/01490799486dac16a48801deb8255.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Varsity Tutors, a Nerdy Company | [View](https://www.openjobs-ai.com/jobs/high-school-physics-tutor-united-states-118970132725762641) |
| Middle School Science Tutor | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/96/01490799486dac16a48801deb8255.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Varsity Tutors, a Nerdy Company | [View](https://www.openjobs-ai.com/jobs/middle-school-science-tutor-united-states-118970132725762642) |
| IBEW - International Brotherhood of Electrical Workers Tutor | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/96/01490799486dac16a48801deb8255.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Varsity Tutors, a Nerdy Company | [View](https://www.openjobs-ai.com/jobs/ibew-international-brotherhood-of-electrical-workers-tutor-lawrence-ma-118970132725762643) |
| Conversational Spanish Tutor | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/96/01490799486dac16a48801deb8255.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Varsity Tutors, a Nerdy Company | [View](https://www.openjobs-ai.com/jobs/conversational-spanish-tutor-united-states-118970132725762644) |
| AANP - American Association of Nurse Practitioners Tutor | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/96/01490799486dac16a48801deb8255.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Varsity Tutors, a Nerdy Company | [View](https://www.openjobs-ai.com/jobs/aanp-american-association-of-nurse-practitioners-tutor-round-rock-tx-118970132725762645) |
| Applied Mathematics Tutor | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/96/01490799486dac16a48801deb8255.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Varsity Tutors, a Nerdy Company | [View](https://www.openjobs-ai.com/jobs/applied-mathematics-tutor-mount-vernon-ny-118970132725762646) |
| SUBSTITUTE - Counselor II | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/2/26/6edc984aadb4286593e6e1b7e089c.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> North Slope Borough | [View](https://www.openjobs-ai.com/jobs/substitute-counselor-ii-utqiagvik-ak-118973303619584000) |
| Solution-Based Casework (SBC) Case Planner (Bronx Location) | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/e/47/1360c08b60b124989247efe72358f.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Arab-American Family Support Center | [View](https://www.openjobs-ai.com/jobs/solution-based-casework-sbc-case-planner-bronx-location-bronx-ny-118973303619584001) |
| Associate Sales Representative | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/e/d9/c7e8be94924d083dee4f0ac80e71f.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Handtevy | [View](https://www.openjobs-ai.com/jobs/associate-sales-representative-fort-lauderdale-fl-118973303619584002) |
| Veterinary Assistant | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/3/3e/516ccdf9ac8f9acf432dce331a9af.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Northwest Animal Hospital at Heartland Veterinary Partners | [View](https://www.openjobs-ai.com/jobs/veterinary-assistant-at-northwest-animal-hospital-des-plaines-il-118973303619584003) |
| PRN Home Infusion RN Needed | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/0/72/29fcd968704990906d93379402011.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Atúlo Health | [View](https://www.openjobs-ai.com/jobs/prn-home-infusion-rn-needed-columbus-ga-118973303619584004) |
| Information System Security Officer (ISSO) | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/5/85/3f817bfa9e3e0c2e821bce2bf1d1e.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> ERT | [View](https://www.openjobs-ai.com/jobs/information-system-security-officer-isso-suitland-md-118973303619584006) |
| Controller | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/a/85/43e12f34233437e37c7e7dfd6ff67.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Gift of Life Donor Program | [View](https://www.openjobs-ai.com/jobs/controller-philadelphia-pa-118973303619584007) |
| Field Service Electronics Technician | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/8/e6/e0bfaf3487255c1ce3251294752b7.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Eaton | [View](https://www.openjobs-ai.com/jobs/field-service-electronics-technician-bellevue-wa-118973303619584008) |
| IN-ROOM DINING ASSISTANT | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/a/a8/801a66d90cf3c432cd6cb347a6c6b.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Froedtert Health | [View](https://www.openjobs-ai.com/jobs/in-room-dining-assistant-manitowoc-wi-118973303619584009) |
| Eaton Development Program: Engineering Technology - Power Electronics | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/8/e6/e0bfaf3487255c1ce3251294752b7.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Eaton | [View](https://www.openjobs-ai.com/jobs/eaton-development-program-engineering-technology-power-electronics-moon-pa-118973303619584010) |
| Lead Teller | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/0/94/98b5f9dfc09428896225a7c4367b8.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> KeyBank | [View](https://www.openjobs-ai.com/jobs/lead-teller-lakewood-wa-118973303619584011) |
| Physical Therapist - Outpatient | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/6/89/39d75e6682e401254ac51423968ab.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Bonsai Rehab | [View](https://www.openjobs-ai.com/jobs/physical-therapist-outpatient-eagle-river-wi-118973303619584013) |
| OB SURGICAL TECH | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/8/f1/be1f24254cafddc85cb99cc1c311c.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Blessing Health | [View](https://www.openjobs-ai.com/jobs/ob-surgical-tech-quincy-il-118973303619584014) |
| Consultant – Atlantic Region | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/1/53/7c7ebb7ff5e0c5bb5f436df96f65a.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> CCS Fundraising | [View](https://www.openjobs-ai.com/jobs/consultant-atlantic-region-maryland-united-states-118973303619584015) |
| Software Engineer, Backend | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/a/88/e4b092655639857f6c9fca03fd850.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Omnissa | [View](https://www.openjobs-ai.com/jobs/software-engineer-backend-north-carolina-united-states-118973303619584016) |
| Speech Language Pathologist - PRN, Acute Care, Atrium Health Union | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/8/07/0d7c1e68b222f536fa6e7efdf7f69.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Atrium Health | [View](https://www.openjobs-ai.com/jobs/speech-language-pathologist-prn-acute-care-atrium-health-union-monroe-nc-118973303619584018) |
| Staff Software Engineer (Remote) | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/2/ad/be64a77b957164fe1b0b7d90c1588.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Pomelo Care | [View](https://www.openjobs-ai.com/jobs/staff-software-engineer-remote-united-states-118973303619584019) |
| Senior Communications Specialist | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/1/3f/bcd3a64fc3c338a06d175bc035aa1.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> ALTEN | [View](https://www.openjobs-ai.com/jobs/senior-communications-specialist-boston-ma-118973303619584020) |
| Data Engineer | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/4/9e/5fd6064ae9ca864c9543d176b153e.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Pride Global | [View](https://www.openjobs-ai.com/jobs/data-engineer-austin-tx-118973303619584021) |
| Enrollment Paraprofessional - 3rd Gr. Honors Math | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/b/c9/9e4da8524fc228c4bc1766d6e607d.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Naperville Community Unit School District 203 | [View](https://www.openjobs-ai.com/jobs/enrollment-paraprofessional-3rd-gr-honors-math-naperville-il-118973303619584022) |
| Cardiology Clinic Nurse | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/d/03/4839dae0d89b917f934a02ea1f6d0.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> CHI | [View](https://www.openjobs-ai.com/jobs/cardiology-clinic-nurse-north-little-rock-ar-118973303619584023) |
| Technology & Privacy Counsel | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/4/af/86e27d53c5acf99c61df739827d86.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Koch | [View](https://www.openjobs-ai.com/jobs/technology-privacy-counsel-wichita-ks-118973303619584024) |
| Life Insurance Project Manager | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/8/43/2e4e3ee668bcc755cd0e8a7e45304.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Synergistic Systems, Inc. | [View](https://www.openjobs-ai.com/jobs/life-insurance-project-manager-charlotte-nc-118973303619584025) |
| Automotive Technician/Mechanic | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/6/76/1a4a39e5c9ef9e53a12a8480a361c.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Monro, Inc. | [View](https://www.openjobs-ai.com/jobs/automotive-technicianmechanic-santa-cruz-ca-118973303619584026) |
| Service Writer | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/d/e1/0e5efd001161fa58917cb70d93bc5.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> AAA Auto Club Enterprises | [View](https://www.openjobs-ai.com/jobs/service-writer-williamsburg-va-118973303619584027) |
| Senior Consultant, Healthcare Performance Improvement - Revenue Cycle | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/0/f3/1cf07abd9362861f6b9fe9f1818c4.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Forvis Mazars US | [View](https://www.openjobs-ai.com/jobs/senior-consultant-healthcare-performance-improvement-revenue-cycle-springfield-mo-118973303619584028) |
| Physical Therapist - Outpatient | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/6/89/39d75e6682e401254ac51423968ab.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Bonsai Rehab | [View](https://www.openjobs-ai.com/jobs/physical-therapist-outpatient-anchorage-ak-118973303619584029) |
| Research and Development Technician Temp | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/b/20/3d25c54ac9009095d5ce01e6baa25.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Autonomous Medical Devices Incorporated | [View](https://www.openjobs-ai.com/jobs/research-and-development-technician-temp-santa-ana-ca-118973303619584030) |
| Analyst Business Systems IT | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/b/5b/6b81941c4c31bf04200c6be53c12c.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Medline Industries, LP | [View](https://www.openjobs-ai.com/jobs/analyst-business-systems-it-northbrook-il-118973303619584031) |
| Physical Therapist Assistant PRN | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/e/e2/055701c742262f93d083f854350b9.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> wewe | [View](https://www.openjobs-ai.com/jobs/physical-therapist-assistant-prn-brook-park-oh-118973303619584032) |
| Speech Therapist, EI | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/2/9a/c94e7c543244139967d978713b5cb.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> The Arc of Union County | [View](https://www.openjobs-ai.com/jobs/speech-therapist-ei-mountainside-nj-118973303619584033) |
| CASE MGR SOCIAL WORK SUPERVISOR | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/9/93/6e5d689df1fc32c9cece182c97212.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> UNM Hospital | [View](https://www.openjobs-ai.com/jobs/case-mgr-social-work-supervisor-albuquerque-nm-118973303619584034) |
| RN Clinical Liaison | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/3/04/e0c8f62ff5aaf76e1982fb4800a9c.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Gentiva | [View](https://www.openjobs-ai.com/jobs/rn-clinical-liaison-austin-tx-118973303619584035) |
| Military Veteran Automotive Technician - Liberty Kia | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/f4/423061b521476db5e06de757a0f34.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> KIA Veterans Technician Apprenticeship Program (VTAP) | [View](https://www.openjobs-ai.com/jobs/military-veteran-automotive-technician-liberty-kia-libertyville-il-118973303619584036) |
| Bilingual Retail Sales Consultant (59696) | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/9/72/e8dd1d89f59247fdd23bf3c444882.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> MOBILY LLC | [View](https://www.openjobs-ai.com/jobs/bilingual-retail-sales-consultant-59696-greater-houston-118973303619584037) |
| Maintenance Tech 7:45 PM-8:00 AM | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/6/3a/8a30e3bfa9a81fdc7f15cae15cb66.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Jabil | [View](https://www.openjobs-ai.com/jobs/maintenance-tech-745-pm-800-am-mebane-nc-118973303619584038) |
| Desktop Support Technician | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/9/dd/2f5da4e1701ae0a7b0f02d77c5b72.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> NTT DATA North America | [View](https://www.openjobs-ai.com/jobs/desktop-support-technician-whippany-nj-118973303619584039) |
| Life Science Engineer, Calibration-Validation | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/2/cb/d0402d2fc3b65b9ba67053bd633a6.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Renovo Solutions | [View](https://www.openjobs-ai.com/jobs/life-science-engineer-calibration-validation-boston-ma-118973303619584040) |
| Eaton Development Program: Power System Controls Engineer | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/8/e6/e0bfaf3487255c1ce3251294752b7.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Eaton | [View](https://www.openjobs-ai.com/jobs/eaton-development-program-power-system-controls-engineer-chandler-az-118973303619584041) |
| Field Commissioning Representative - Wenatchee | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/8/e6/e0bfaf3487255c1ce3251294752b7.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Eaton | [View](https://www.openjobs-ai.com/jobs/field-commissioning-representative-wenatchee-tukwila-wa-118973303619584042) |
| Eaton Development Program: Digital Integrated Solutions Engineer | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/8/e6/e0bfaf3487255c1ce3251294752b7.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Eaton | [View](https://www.openjobs-ai.com/jobs/eaton-development-program-digital-integrated-solutions-engineer-charlotte-nc-118973303619584043) |
| Executive Assistant, AWS Data Center Community | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/b/17/f09b91594e1b16f374b34593d895d.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Amazon Web Services (AWS) | [View](https://www.openjobs-ai.com/jobs/executive-assistant-aws-data-center-community-umatilla-or-118973303619584044) |
| Payment Poster (Hybrid, Towson, Full Time) | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/6/e7/6b39c95222b23d000739e26e338f9.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Sheppard Pratt | [View](https://www.openjobs-ai.com/jobs/payment-poster-hybrid-towson-full-time-towson-md-118973303619584045) |
| Sales Representative | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/b/e4/02f585db95f5220d2c4ca5303ead1.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Global Pacific Support | [View](https://www.openjobs-ai.com/jobs/sales-representative-united-states-118973303619584046) |
| Music Teacher Store 4755 | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/e/b8/3130b6dfd100a4f6a9897dd41a374.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Music & Arts | [View](https://www.openjobs-ai.com/jobs/music-teacher-store-4755-lacey-wa-118973303619584047) |
| Direct Support Professionals I Pt 22 Hrs - DSP 1 Sunday 2pm- 10pm and Saturday 8am-10pm- Red Fox | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/8/87/03be07e6263ebcf141625147c1682.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Continuum of Care | [View](https://www.openjobs-ai.com/jobs/direct-support-professionals-i-pt-22-hrs-dsp-1-sunday-2pm-10pm-and-saturday-8am-10pm-red-fox-wolcott-ct-118973303619584048) |
| Clinical Resource Nurse - AOD Cardiac Cath Lab | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/6/c8/5453596183beb17c1cb28778cd173.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Houston Methodist | [View](https://www.openjobs-ai.com/jobs/clinical-resource-nurse-aod-cardiac-cath-lab-houston-tx-118973303619584049) |
| District Support Engineer | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/8/e6/e0bfaf3487255c1ce3251294752b7.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Eaton | [View](https://www.openjobs-ai.com/jobs/district-support-engineer-sandston-va-118973303619584050) |
| Commercial Real Estate Mortgage Banker | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/8/12/18dbcb58b589a0fe5b21689f6e612.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Slatt Capital | [View](https://www.openjobs-ai.com/jobs/commercial-real-estate-mortgage-banker-denver-co-118973303619584051) |
| Talent Acquisition Specialist | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/8/57/0bdd05aabd4a3d4972ed6a1409a49.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> City of New York | [View](https://www.openjobs-ai.com/jobs/talent-acquisition-specialist-manhattan-ny-118973303619584052) |
| Psychiatric/DD Nurse Supervisor - 2nd or 3rd Shift | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/b/6f/11cf927ecbc8949ff804f0a3c1816.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Ohio Department of Behavioral Health | [View](https://www.openjobs-ai.com/jobs/psychiatricdd-nurse-supervisor-2nd-or-3rd-shift-columbus-oh-118973303619584053) |
| Director, Revenue Transformation | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/1/15/f2b3f0dc7f35f13395bb6f0526e76.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> CoreWeave | [View](https://www.openjobs-ai.com/jobs/director-revenue-transformation-san-francisco-ca-118973303619584054) |
| Field Application Engineer – Control Systems, IIoT & Engineering | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/4/60/ad2e893ad3229c57cd00e23a4360c.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Phoenix Contact USA | [View](https://www.openjobs-ai.com/jobs/field-application-engineer-control-systems-iiot-engineering-seattle-wa-118973303619584055) |
| Registered Nurse (RN) | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/c/46/79e609f5af0ee23f41c2c44408754.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Progressive Care Stepdown Unit 6S (PCU) | [View](https://www.openjobs-ai.com/jobs/registered-nurse-rn-progressive-care-stepdown-unit-6s-pcu-st-elizabeth-boardman-boardman-oh-118973303619584056) |
| Registered Nurse-PACU-Edwardsville | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/d/7c/015df33f3f0b57294766979bc63dc.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Gateway Regional Medical Center | [View](https://www.openjobs-ai.com/jobs/registered-nurse-pacu-edwardsville-granite-city-il-118973303619584057) |
| Relationship Banking Specialist | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/9/f5/75f7f2b9f7298b46c65a6244c48d0.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> 1st Summit Bank | [View](https://www.openjobs-ai.com/jobs/relationship-banking-specialist-latrobe-pa-118973303619584058) |
| Registered Nurse (RN) - PICU | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/6/76/b839d01369a3c48109b9815de0783.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Tenet Healthcare | [View](https://www.openjobs-ai.com/jobs/registered-nurse-rn-picu-boca-raton-fl-118973303619584060) |
| Senior Manager, Brand Analytics | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/3/75/439f01c8e4231284569f49ab5cf0c.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Otsuka Pharmaceutical Companies (U.S.) | [View](https://www.openjobs-ai.com/jobs/senior-manager-brand-analytics-princeton-nj-118973303619584061) |
| Staten Island Preparatory Special Education School Age Teacher | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/4/4a/fa3acd6d11a60407e0e4de385d98b.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> AHRC New York City | [View](https://www.openjobs-ai.com/jobs/staten-island-preparatory-special-education-school-age-teacher-staten-island-ny-118973303619584062) |
| Lead Manufacturing Engineer | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/8/e6/e0bfaf3487255c1ce3251294752b7.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Eaton | [View](https://www.openjobs-ai.com/jobs/lead-manufacturing-engineer-los-angeles-ca-118973303619584063) |
| Eaton Development Program - Applications Engineering | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/8/e6/e0bfaf3487255c1ce3251294752b7.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Eaton | [View](https://www.openjobs-ai.com/jobs/eaton-development-program-applications-engineering-warrendale-pa-118973303619584064) |
| Associate, Cross-Channel Planning | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/4/ea/ef96966a379d7de419199bf2c3460.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Beauty Co-Lab | [View](https://www.openjobs-ai.com/jobs/associate-cross-channel-planning-new-york-ny-118973303619584065) |
| PATIENT SERVICES LEAD (FULL TIME) | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/d2/8f5e19e1aaafa180f7e8a30a37404.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Compass One Healthcare | [View](https://www.openjobs-ai.com/jobs/patient-services-lead-full-time-dayton-oh-118973303619584066) |
| Machine Maintenance Electrician | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/1/91/ac21b9f3f0c6d81637ca45b62cd21.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> FieldCore | [View](https://www.openjobs-ai.com/jobs/machine-maintenance-electrician-goodyear-az-118973303619584067) |
| PCT-East Outpatient GI-Full-Time | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/1/d1/fc49c2d85cb59d509be2a5ac4e599.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Erlanger | [View](https://www.openjobs-ai.com/jobs/pct-east-outpatient-gi-full-time-chattanooga-tn-118973303619584068) |
| Global Operations Center Technician | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/3/82/ad02748c04d9ee86ca7e2c375abb9.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Epic | [View](https://www.openjobs-ai.com/jobs/global-operations-center-technician-st-cloud-mn-118973303619584069) |
| Sous Chef | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/c/e1/7bd85aa5162d59fffc2684b46d1b3.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Senior Lifestyle | [View](https://www.openjobs-ai.com/jobs/sous-chef-auburn-me-118973303619584070) |
| Middle School Special Education Teacher (Salem area) | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/e/85/da246c79a5e000c71a4be008e338d.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Kreyco | [View](https://www.openjobs-ai.com/jobs/middle-school-special-education-teacher-salem-area-monroeville-nj-118973303619584071) |
| Res Care Nurse (A) - Full Time, 1st Shift | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/c/cd/97cf1aa6da0090ba7f7bd0cee1326.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Blanchard Valley Health System | [View](https://www.openjobs-ai.com/jobs/res-care-nurse-a-full-time-1st-shift-findlay-oh-118973303619584072) |
| Solution-Based Casework (SBC) Case Planner (Bronx Location) | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/e/47/1360c08b60b124989247efe72358f.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Arab-American Family Support Center | [View](https://www.openjobs-ai.com/jobs/solution-based-casework-sbc-case-planner-bronx-location-bronx-ny-118973303619584073) |
| Lead IBM i Platform & Power Systems Engineer | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/9/4a/7786528693e02aa98e2794a811e17.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Oshkosh Corporation | [View](https://www.openjobs-ai.com/jobs/lead-ibm-i-platform-power-systems-engineer-oshkosh-wi-118973303619584074) |
| Survivorship Oncology Nurse Navigator | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/e/16/eb7f343d8c9142856d7ab257ea40a.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> MUSC Health | [View](https://www.openjobs-ai.com/jobs/survivorship-oncology-nurse-navigator-charleston-sc-118973303619584075) |
| Claims Specialist - Journal Center | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/5/b4/afb69edba88b752c5b333bc0ee22f.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> TriCore Reference Laboratories | [View](https://www.openjobs-ai.com/jobs/claims-specialist-journal-center-albuquerque-nm-118973303619584076) |
| Freelance Visual Content Creator | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/b/bf/c8007a537ae8742c00b32921446f8.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> SEAWAG | [View](https://www.openjobs-ai.com/jobs/freelance-visual-content-creator-united-states-118973496557568000) |
| AI Research Scientist | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/7/f8/cd4c2c5970704d861c9020b192fb4.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> EDDA Technology, Inc. | [View](https://www.openjobs-ai.com/jobs/ai-research-scientist-princeton-nj-118973496557568001) |
| Head of Growth | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/8/1e/0a9b71a62ed160ff9b1ad73dfb4fd.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Autobound | [View](https://www.openjobs-ai.com/jobs/head-of-growth-austin-tx-118973496557568002) |
| Board Certified Behavior Analyst | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/2/5f/54982b64cc5e0a52eb2ca4d9377ab.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Adapt & Transform Behavior (ATBx) | [View](https://www.openjobs-ai.com/jobs/board-certified-behavior-analyst-greater-tampa-bay-area-118973496557568003) |
| Spanish Bilingual SEO Specialist - Google Ads (ZR_20368_JOB) | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/7/1f/c28858790051acbaaac2db9d2ef0f.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> BruntWork | [View](https://www.openjobs-ai.com/jobs/spanish-bilingual-seo-specialist-google-ads-zr20368job-latin-america-118973496557568004) |
| Medical Office Receptionist | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/d/11/5f83f4fb22f75de48d7404be80e07.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Bay Physical Therapy | [View](https://www.openjobs-ai.com/jobs/medical-office-receptionist-monterey-ca-118973496557568005) |
| Facility Attendant (Recreation Leader) | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/e/16/56faf08a1da4d083f777ef8fd1cdb.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> City of Emeryville | [View](https://www.openjobs-ai.com/jobs/facility-attendant-recreation-leader-emeryville-ca-118973496557568006) |
| Surveyor Associate | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/5/51/a536690e19e8e64702763e7a4ecd1.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> City of Toledo | [View](https://www.openjobs-ai.com/jobs/surveyor-associate-toledo-oh-118973496557568007) |
| Ingeniero de soporte de TI | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/7/20/c947e4dfdd4007f3c3ac672190beb.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Experis Chile | [View](https://www.openjobs-ai.com/jobs/ingeniero-de-soporte-de-ti-latin-america-118973496557568008) |
| Member Resolution Specialist | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/d/d2/1fffbb6db92e2d6f5e17a4b9f3ef6.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> MC Federal Credit Union | [View](https://www.openjobs-ai.com/jobs/member-resolution-specialist-danville-pa-118973496557568009) |
| Preconstruction Manager - Design-Build | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/a/0b/9a4445e09fd1c00a0094bd60281a6.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Jacobs | [View](https://www.openjobs-ai.com/jobs/preconstruction-manager-design-build-denver-co-118973496557568010) |
| Linguistics Expert - AI Evaluator | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/c/9b/eacb6d707e14fddcd09b1f39fa0a9.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> micro1 | [View](https://www.openjobs-ai.com/jobs/linguistics-expert-ai-evaluator-latin-america-118973496557568011) |
| Shopify Developer | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/76/fb7df05443606104442575b8930b3.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Allied Global Technology Services | [View](https://www.openjobs-ai.com/jobs/shopify-developer-latin-america-118973496557568012) |
| Content Creator | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/5/2c/35730bf68c4cacd1ca2da36914464.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Alinea Invest | [View](https://www.openjobs-ai.com/jobs/content-creator-united-states-118973496557568013) |
| Sr.OutSystems Developer | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/a/1f/5a0b79b52449e6abac8e1a02b7fcb.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> GeorgiaTEK Systems Inc. | [View](https://www.openjobs-ai.com/jobs/sroutsystems-developer-latin-america-118973496557568014) |
| Information Technology Support Technician | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/e/d7/856c638fa765f3b4f290ba57209d4.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> WorkBetterNow | [View](https://www.openjobs-ai.com/jobs/information-technology-support-technician-latin-america-118973496557568015) |
| German Language Evaluator - Nachhilfe Deutsch | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/c/9b/eacb6d707e14fddcd09b1f39fa0a9.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> micro1 | [View](https://www.openjobs-ai.com/jobs/german-language-evaluator-nachhilfe-deutsch-latin-america-118973496557568016) |
| Social Media Content Creator/Influencer | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/92/6d6ed024a73f2e3e22f9004b59d3f.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> ATTIX | [View](https://www.openjobs-ai.com/jobs/social-media-content-creatorinfluencer-new-york-city-metropolitan-area-118973496557568017) |
| DevSecOps Specialist - AI Trainer | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/c/9b/eacb6d707e14fddcd09b1f39fa0a9.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> micro1 | [View](https://www.openjobs-ai.com/jobs/devsecops-specialist-ai-trainer-latin-america-118973496557568018) |
| Out systems Developer | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/a/1f/5a0b79b52449e6abac8e1a02b7fcb.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> GeorgiaTEK Systems Inc. | [View](https://www.openjobs-ai.com/jobs/out-systems-developer-latin-america-118973496557568019) |
| Artificial Intelligence Researcher | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/e/44/b9f80073908c60f96b52f681ce2b4.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Reactive Lions® | [View](https://www.openjobs-ai.com/jobs/artificial-intelligence-researcher-boston-ma-118973496557568020) |
| Game Developer | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/c/9b/eacb6d707e14fddcd09b1f39fa0a9.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> micro1 | [View](https://www.openjobs-ai.com/jobs/game-developer-latin-america-118973496557568021) |
| Customer Service Representative - Medical Services | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/4/06/d328a9c711b66a19b850b033db433.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> LaTeam Partners | [View](https://www.openjobs-ai.com/jobs/customer-service-representative-medical-services-latin-america-118973496557568022) |
| VA Box Cybersecurity Engineer | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/0/96/f4e2d6d99604bbd4d025184f8b71b.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Sprezzatura | [View](https://www.openjobs-ai.com/jobs/va-box-cybersecurity-engineer-united-states-118973496557568023) |
| Performance Marketing Manager | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/1/5a/850288df16cb1ba7eabf19d1a59cb.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Hire With Near | [View](https://www.openjobs-ai.com/jobs/performance-marketing-manager-latin-america-118973496557568024) |
| Senior FullStack Engineer | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/8/c9/b338395668f19665d474398eb1009.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Avenue Code | [View](https://www.openjobs-ai.com/jobs/senior-fullstack-engineer-latin-america-118973496557568025) |
| Oracle Supply Chain Management Senior Consultant | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/c/0b/371cda7f205db3b5b825455eaed63.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Protiviti | [View](https://www.openjobs-ai.com/jobs/oracle-supply-chain-management-senior-consultant-denver-co-118973496557568026) |
| Cyber Security -  AI Trainer | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/c/9b/eacb6d707e14fddcd09b1f39fa0a9.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> micro1 | [View](https://www.openjobs-ai.com/jobs/cyber-security-ai-trainer-latin-america-118973496557568027) |
| Aircraft Upholstery Sewer | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/e/49/995a189d2c0988b5672f4212b14ad.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Stevens Aerospace and Defense Systems, LLC. | [View](https://www.openjobs-ai.com/jobs/aircraft-upholstery-sewer-smyrna-tn-118973664329728000) |
| Ejecutivo/a Integral - Valparaíso BP | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/c/8c/dc80fe3f8a20a79505b36ee9e89d4.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Banco Bci | [View](https://www.openjobs-ai.com/jobs/ejecutivoa-integral-valparaso-bp-valparaiso-metropolitan-area-118973664329728001) |
| Client Specialist | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/1/5a/850288df16cb1ba7eabf19d1a59cb.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Hire With Near | [View](https://www.openjobs-ai.com/jobs/client-specialist-latin-america-118973664329728002) |
| Executive Assistant | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/1/5a/850288df16cb1ba7eabf19d1a59cb.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Hire With Near | [View](https://www.openjobs-ai.com/jobs/executive-assistant-latin-america-118973664329728003) |
| Mathematician (PhD/Masters) | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/c/9b/eacb6d707e14fddcd09b1f39fa0a9.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> micro1 | [View](https://www.openjobs-ai.com/jobs/mathematician-phdmasters-latin-america-118973664329728004) |
| Member Experience Specialist | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/35/0f8c117e5250796cdbc9933c41ee5.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> BAY AREA CREDIT UNION | [View](https://www.openjobs-ai.com/jobs/member-experience-specialist-oregon-oh-118973664329728005) |
| RF Signal Processing/Machine Learning Engineer (Focus 2) | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/9/89/0076b168284af7f206788b13fd376.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> VectorWave Corporation | [View](https://www.openjobs-ai.com/jobs/rf-signal-processingmachine-learning-engineer-focus-2-cambridge-ma-118973664329728006) |
| Family Medicine | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/e/8c/eeac0def2b30c55c283969729c036.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Advanced Practitioner | [View](https://www.openjobs-ai.com/jobs/family-medicine-advanced-practitioner-hiawatha-iowa-hiawatha-ia-118973832101888000) |
| MNA Physician Neurohospitalist-2 @ The Woodlands | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/7/3d/c2c6582702584258637d91e504f09.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Memorial Hermann Health System | [View](https://www.openjobs-ai.com/jobs/mna-physician-neurohospitalist-2-the-woodlands-spring-tx-118973832101888001) |
| Medical Laboratory Scientist Group Lead | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/0/b6/024ac3e2a930ca3de64b939488e62.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Quest Diagnostics | [View](https://www.openjobs-ai.com/jobs/medical-laboratory-scientist-group-lead-cleveland-oh-118973832101888002) |
| Recruiter | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/f0/33116a579df00f0922392b64c5940.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> MP Materials | [View](https://www.openjobs-ai.com/jobs/recruiter-fort-worth-tx-118973832101888003) |
| Medical Laboratory Technician (MLT)/Medical Technologist (MT) Full Time (Florence, SC) Day Shift | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/e/16/eb7f343d8c9142856d7ab257ea40a.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> MUSC Health | [View](https://www.openjobs-ai.com/jobs/medical-laboratory-technician-mltmedical-technologist-mt-full-time-florence-sc-day-shift-florence-sc-118973832101888004) |
| Residential Rehab Educator, Part-Time, $20.00 | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/2/98/b4126a7d2fdf86111766065b93d1b.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Aspire Health Alliance | [View](https://www.openjobs-ai.com/jobs/residential-rehab-educator-part-time-2000-norwell-ma-118973832101888005) |
| Residential Rehabilitation Educator, $20.00 | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/2/98/b4126a7d2fdf86111766065b93d1b.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Aspire Health Alliance | [View](https://www.openjobs-ai.com/jobs/residential-rehabilitation-educator-2000-quincy-ma-118973832101888006) |
| Trading Operations Specialist | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/9/6b/0f2d6efd28d386de419eacc1d9c7f.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> GTS | [View](https://www.openjobs-ai.com/jobs/trading-operations-specialist-new-york-ny-118973832101888007) |
| Babysitter | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/89/c133a2199bea162d1f7239f0ecbc1.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Killingly Public Schools | [View](https://www.openjobs-ai.com/jobs/babysitter-danielson-ct-118973832101888008) |
| Registered Nurse - Cardiac | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/7/89/6ed6dbffcc186bb53d5230ca1c3bf.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Novant Health | [View](https://www.openjobs-ai.com/jobs/registered-nurse-cardiac-wilmington-nc-118973832101888009) |
| Clinic RN- Urgent Care | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/1/07/8399750a93bb90d9a5409f37c28ad.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> WVU Medicine Berkeley and Jefferson Medical Centers | [View](https://www.openjobs-ai.com/jobs/clinic-rn-urgent-care-martinsburg-wv-118973832101888010) |
| Charge Nurse (Transitional Care) | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/2/f6/d2344ff30d5b5c68e11f0ad654995.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> MAINE VETERANS HOME | [View](https://www.openjobs-ai.com/jobs/charge-nurse-transitional-care-augusta-me-118974004068352000) |
| AWS DevOps Engineer | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/e/c2/ea0a5ae95f89bddd793e10bb49444.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Remote | [View](https://www.openjobs-ai.com/jobs/aws-devops-engineer-remote-latin-america-valparaiso-metropolitan-area-118974004068352001) |
| Senior Java/Vue Developer | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/e/c2/ea0a5ae95f89bddd793e10bb49444.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Remote | [View](https://www.openjobs-ai.com/jobs/senior-javavue-developer-remote-latin-america-valparaiso-metropolitan-area-118974004068352002) |
| Recruitment Specialist | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/2/4d/b7c608b93655f57863fb8b0e5e942.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Mercor | [View](https://www.openjobs-ai.com/jobs/recruitment-specialist-latin-america-118974004068352003) |
| .NET Developer | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/b/8a/ed1c2e387798a9ff84c51dc5ae20a.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> GraceMark Solutions | [View](https://www.openjobs-ai.com/jobs/net-developer-latin-america-118974004068352004) |
| Search Engine Optimization Specialist | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/4/06/d328a9c711b66a19b850b033db433.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> LaTeam Partners | [View](https://www.openjobs-ai.com/jobs/search-engine-optimization-specialist-latin-america-118974004068352005) |
| DC Clerk | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/9/07/2a51c9ef2f0f92120b133f4315c74.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Milwaukee Tool | [View](https://www.openjobs-ai.com/jobs/dc-clerk-olive-branch-ms-118974180229120000) |
| Patient Care Technician | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/9/c1/5a549533838975f075ba0f0dec1b3.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> DaVita Kidney Care | [View](https://www.openjobs-ai.com/jobs/patient-care-technician-alpena-mi-118974180229120001) |
| LEAD Peer Specialist | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/3/68/d8109ce71a3c4cf41292047163b98.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> People USA | [View](https://www.openjobs-ai.com/jobs/lead-peer-specialist-poughkeepsie-ny-118974180229120002) |
| Founding AI Engineer | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/6/47/1261465dd69b09d75d15bc1ef9bef.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Averi | [View](https://www.openjobs-ai.com/jobs/founding-ai-engineer-brooklyn-ny-118974289281024000) |
| Manufacturing Production Assistant, Consumer Goods (Mandarin Speaking) | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/7/0c/ad3a7f5cd644f63feb58c5ed5195b.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Mvnifest | [View](https://www.openjobs-ai.com/jobs/manufacturing-production-assistant-consumer-goods-mandarin-speaking-hawaii-united-states-118974394138624000) |
| Cryptocurrency Traders – Capital Allocation Or Permanent Roles | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/1/3c/fbe65e99c9c87facc04763e3d1510.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Pagos Consultants | [View](https://www.openjobs-ai.com/jobs/cryptocurrency-traders-capital-allocation-or-permanent-roles-miami-fl-118974507384832000) |
| Nursing/NCLEX Tutor | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/96/01490799486dac16a48801deb8255.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Varsity Tutors, a Nerdy Company | [View](https://www.openjobs-ai.com/jobs/nursingnclex-tutor-reno-nv-118970132725762526) |
| Social Anthropology Tutor | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/96/01490799486dac16a48801deb8255.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Varsity Tutors, a Nerdy Company | [View](https://www.openjobs-ai.com/jobs/social-anthropology-tutor-birmingham-al-118970132725762527) |
| SHSAT Tutor | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/96/01490799486dac16a48801deb8255.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Varsity Tutors, a Nerdy Company | [View](https://www.openjobs-ai.com/jobs/shsat-tutor-reno-nv-118970132725762528) |
| Spanish Tutor | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/96/01490799486dac16a48801deb8255.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Varsity Tutors, a Nerdy Company | [View](https://www.openjobs-ai.com/jobs/spanish-tutor-baton-rouge-la-118970132725762529) |
| UNITY Tutor | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/96/01490799486dac16a48801deb8255.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Varsity Tutors, a Nerdy Company | [View](https://www.openjobs-ai.com/jobs/unity-tutor-augusta-ga-118970132725762530) |
| Social Networking Tutor | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/96/01490799486dac16a48801deb8255.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Varsity Tutors, a Nerdy Company | [View](https://www.openjobs-ai.com/jobs/social-networking-tutor-orlando-fl-118970132725762531) |
| Civics Tutor | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/96/01490799486dac16a48801deb8255.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Varsity Tutors, a Nerdy Company | [View](https://www.openjobs-ai.com/jobs/civics-tutor-baton-rouge-la-118970132725762532) |
| Math 3 Tutor | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/96/01490799486dac16a48801deb8255.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Varsity Tutors, a Nerdy Company | [View](https://www.openjobs-ai.com/jobs/math-3-tutor-reno-nv-118970132725762533) |
| Elementary School Science Tutor | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/96/01490799486dac16a48801deb8255.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Varsity Tutors, a Nerdy Company | [View](https://www.openjobs-ai.com/jobs/elementary-school-science-tutor-clifton-nj-118970132725762534) |
| Team Lead | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/2/8e/7f895f28d9a6cad3c824bb7125937.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Tempur Sealy International | [View](https://www.openjobs-ai.com/jobs/team-lead-phoenix-az-118970132725762535) |
| FRT Tutor | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/96/01490799486dac16a48801deb8255.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Varsity Tutors, a Nerdy Company | [View](https://www.openjobs-ai.com/jobs/frt-tutor-rochester-ny-118970132725762536) |
| CDR Exam - Cardiovascular Disease Recertification Exam Tutor | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/96/01490799486dac16a48801deb8255.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Varsity Tutors, a Nerdy Company | [View](https://www.openjobs-ai.com/jobs/cdr-exam-cardiovascular-disease-recertification-exam-tutor-akron-oh-118970132725762537) |
| Japanese Tutor | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/96/01490799486dac16a48801deb8255.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Varsity Tutors, a Nerdy Company | [View](https://www.openjobs-ai.com/jobs/japanese-tutor-coral-gables-fl-118970132725762538) |
| Immunology Tutor | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/96/01490799486dac16a48801deb8255.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Varsity Tutors, a Nerdy Company | [View](https://www.openjobs-ai.com/jobs/immunology-tutor-birmingham-al-118970132725762539) |
| TEAS Tutor | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/96/01490799486dac16a48801deb8255.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Varsity Tutors, a Nerdy Company | [View](https://www.openjobs-ai.com/jobs/teas-tutor-richmond-va-118970132725762540) |
| High School Government Tutor | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/96/01490799486dac16a48801deb8255.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Varsity Tutors, a Nerdy Company | [View](https://www.openjobs-ai.com/jobs/high-school-government-tutor-richmond-va-118970132725762541) |
| Mac Basic Computer Skills Tutor | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/96/01490799486dac16a48801deb8255.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Varsity Tutors, a Nerdy Company | [View](https://www.openjobs-ai.com/jobs/mac-basic-computer-skills-tutor-reno-nv-118970132725762542) |
| IB Biology Tutor | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/96/01490799486dac16a48801deb8255.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Varsity Tutors, a Nerdy Company | [View](https://www.openjobs-ai.com/jobs/ib-biology-tutor-richmond-va-118970132725762543) |
| Math 3 Tutor | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/96/01490799486dac16a48801deb8255.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Varsity Tutors, a Nerdy Company | [View](https://www.openjobs-ai.com/jobs/math-3-tutor-north-las-vegas-nv-118970132725762544) |
| Adult Literacy Tutor | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/96/01490799486dac16a48801deb8255.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Varsity Tutors, a Nerdy Company | [View](https://www.openjobs-ai.com/jobs/adult-literacy-tutor-richmond-va-118970132725762545) |
| Basic Computer Literacy Tutors (Instant) | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/96/01490799486dac16a48801deb8255.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Varsity Tutors, a Nerdy Company | [View](https://www.openjobs-ai.com/jobs/basic-computer-literacy-tutors-instant-atlanta-ga-118970132725762546) |
| Adult Health and Wellness Tutors (Instant) | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/96/01490799486dac16a48801deb8255.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Varsity Tutors, a Nerdy Company | [View](https://www.openjobs-ai.com/jobs/adult-health-and-wellness-tutors-instant-new-york-ny-118970132725762547) |
| Adult Health and Wellness Tutors (Instant) | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/96/01490799486dac16a48801deb8255.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Varsity Tutors, a Nerdy Company | [View](https://www.openjobs-ai.com/jobs/adult-health-and-wellness-tutors-instant-cincinnati-oh-118970132725762548) |
| Calculus Tutors (Instant) | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/96/01490799486dac16a48801deb8255.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Varsity Tutors, a Nerdy Company | [View](https://www.openjobs-ai.com/jobs/calculus-tutors-instant-new-york-ny-118970132725762549) |
| French 1 Tutor | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/96/01490799486dac16a48801deb8255.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Varsity Tutors, a Nerdy Company | [View](https://www.openjobs-ai.com/jobs/french-1-tutor-richmond-va-118970132725762550) |
| College Physics Tutors (Instant) | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/96/01490799486dac16a48801deb8255.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Varsity Tutors, a Nerdy Company | [View](https://www.openjobs-ai.com/jobs/college-physics-tutors-instant-new-york-ny-118970132725762551) |
| Conversational Spanish Tutors (Instant) | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/96/01490799486dac16a48801deb8255.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Varsity Tutors, a Nerdy Company | [View](https://www.openjobs-ai.com/jobs/conversational-spanish-tutors-instant-las-vegas-nv-118970132725762552) |
| AP Calculus AB Tutors (Instant) | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/96/01490799486dac16a48801deb8255.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Varsity Tutors, a Nerdy Company | [View](https://www.openjobs-ai.com/jobs/ap-calculus-ab-tutors-instant-jacksonville-fl-118970132725762553) |
| College Level American History Tutors (Instant) | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/96/01490799486dac16a48801deb8255.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Varsity Tutors, a Nerdy Company | [View](https://www.openjobs-ai.com/jobs/college-level-american-history-tutors-instant-boston-ma-118970132725762554) |
| AP Biology Tutors (Instant) | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/96/01490799486dac16a48801deb8255.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Varsity Tutors, a Nerdy Company | [View](https://www.openjobs-ai.com/jobs/ap-biology-tutors-instant-syracuse-ny-118970132725762555) |
| AP Statistics Tutors (Instant) | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/96/01490799486dac16a48801deb8255.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Varsity Tutors, a Nerdy Company | [View](https://www.openjobs-ai.com/jobs/ap-statistics-tutors-instant-new-york-ny-118970132725762556) |
| AP Human Geography Tutors (Instant) | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/96/01490799486dac16a48801deb8255.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Varsity Tutors, a Nerdy Company | [View](https://www.openjobs-ai.com/jobs/ap-human-geography-tutors-instant-boston-ma-118970132725762557) |
| College English Tutors (Instant) | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/96/01490799486dac16a48801deb8255.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Varsity Tutors, a Nerdy Company | [View](https://www.openjobs-ai.com/jobs/college-english-tutors-instant-evanston-il-118970132725762558) |
| Adult Health and Wellness Tutors (Instant) | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/96/01490799486dac16a48801deb8255.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Varsity Tutors, a Nerdy Company | [View](https://www.openjobs-ai.com/jobs/adult-health-and-wellness-tutors-instant-miami-fl-118970132725762559) |
| Elementary School Reading Tutors (Instant) | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/96/01490799486dac16a48801deb8255.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Varsity Tutors, a Nerdy Company | [View](https://www.openjobs-ai.com/jobs/elementary-school-reading-tutors-instant-dallas-tx-118970132725762560) |
| ACT Writing Tutors (Instant) | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/96/01490799486dac16a48801deb8255.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Varsity Tutors, a Nerdy Company | [View](https://www.openjobs-ai.com/jobs/act-writing-tutors-instant-dallas-tx-118970132725762561) |

<p align="center">
  <em>...and 52 more jobs</em>
</p>

<p align="center">
  <a href="https://www.openjobs-ai.com/deepsearch"><strong>Browse All Jobs →</strong></a>
</p>

---

<p align="center">
  Made with Python + GitHub Actions · Updated December 31, 2025
</p>
