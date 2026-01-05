<p align="center">
  <img src="https://img.shields.io/badge/jobs-27+-blue?style=for-the-badge" alt="Jobs Count">
  <img src="https://img.shields.io/badge/companies-15+-purple?style=for-the-badge" alt="Companies">
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
- **Auto-Updated Every 6 Hours** - Fresh jobs from 15+ companies via GitHub Actions
- **Zero Infrastructure** - Runs entirely on GitHub Pages + Cloudflare (free tier)
- **Lightweight** - Pure Python, no external dependencies, <1MB total size
- **SEO Optimized** - Proper sitemaps, meta tags, and structured content

## Job Statistics

| Category | Count |
|----------|------:|
| Other | 17 |
| Engineering | 3 |
| Management | 3 |
| Healthcare | 2 |
| Sales | 1 |
| Finance | 1 |
| Marketing | 0 |
| HR | 0 |
| Operations | 0 |

**Top Hiring Companies:** Old Colony YMCA, Deel, Scale AI, PandoLogic, Blanche Ames Elementary-Part Time at Old Colony YMCA

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
│  │ Sitemap     │   │ (27+ jobs) │   │ (README + HTML)     │   │
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
- **And 15+ other companies**

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
  <em>Updated January 05, 2026 · Showing 27 of 27+ jobs</em>
</p>

| Job Title | Company | Apply |
|-----------|---------|:-----:|
| Otolaryngologist | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/6/1b/322c639b76a7ab2a6809c698f782e.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Vital Match Talent 🩺 | [View](https://www.openjobs-ai.com/jobs/otolaryngologist-worcester-ma-120800812204032169) |
| Drone Pilot / Reality Capture Technician | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/1/4d/991d101d352dd1c48968ce461c995.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Eye-bot | [View](https://www.openjobs-ai.com/jobs/drone-pilot-reality-capture-technician-pittsburgh-pa-120800812204032170) |
| Customer Support Specialist (LATAM) | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/0/ef/f7c3e94969206f67b87400cbf348b.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Deel | [View](https://www.openjobs-ai.com/jobs/customer-support-specialist-latam-latin-america-120800812204032171) |
| Head of Commercial Strategy | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/9/f4/00dfd380ad7be1fdd5923a007a21d.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Scale AI | [View](https://www.openjobs-ai.com/jobs/head-of-commercial-strategy-middle-east-120800812204032172) |
| Stacker | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/9/96/22ea8646f771edf4ca01132e21955.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> PandoLogic | [View](https://www.openjobs-ai.com/jobs/stacker-lorain-oh-120800812204032173) |
| Psychiatry Locum Needed in Virginia Beach Virginia | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/9/96/22ea8646f771edf4ca01132e21955.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> PandoLogic | [View](https://www.openjobs-ai.com/jobs/psychiatry-locum-needed-in-virginia-beach-virginia-virginia-beach-va-120800812204032174) |
| Physician Assistant | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/9/96/22ea8646f771edf4ca01132e21955.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Emergency Medicine, Nurse Practitioner | [View](https://www.openjobs-ai.com/jobs/physician-assistant-emergency-medicine-nurse-practitioner-emergency-medicine-mi-hancock-mi-120800812204032175) |
| Lead Fullstack Developer (React + .NET) | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/0/f3/229c22a8567fd29fb9fb5068412af.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> SNI | [View](https://www.openjobs-ai.com/jobs/lead-fullstack-developer-react-net-latin-america-120800812204032176) |
| Learning & Development Specialist | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/8/68/4bb6c6ea727adf6f221eda51fd9b0.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> (Remote | [View](https://www.openjobs-ai.com/jobs/learning-development-specialist-remote-worldwide-latin-america-120800812204032177) |
| C++ Competitive Programming Checker | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/c/9b/eacb6d707e14fddcd09b1f39fa0a9.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> micro1 | [View](https://www.openjobs-ai.com/jobs/c-competitive-programming-checker-latin-america-120800812204032178) |
| Strategist, EMEA | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/9/f4/00dfd380ad7be1fdd5923a007a21d.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Scale AI | [View](https://www.openjobs-ai.com/jobs/strategist-emea-middle-east-120800812204032179) |
| Global Service Center Analyst | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/0/ef/f7c3e94969206f67b87400cbf348b.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Deel | [View](https://www.openjobs-ai.com/jobs/global-service-center-analyst-latin-america-120800812204032180) |
| Gymnastics Instructor | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/b/d2/19d24aa8596ad5f326eff7200c0b5.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Old Colony YMCA | [View](https://www.openjobs-ai.com/jobs/gymnastics-instructor-middleboro-ma-120800812204032154) |
| School Age Senior Group Leader | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/b/d2/19d24aa8596ad5f326eff7200c0b5.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Old Colony YMCA | [View](https://www.openjobs-ai.com/jobs/school-age-senior-group-leader-north-pembroke-ma-120800812204032155) |
| Child Care Teacher | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/b/d2/19d24aa8596ad5f326eff7200c0b5.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Old Colony YMCA | [View](https://www.openjobs-ai.com/jobs/child-care-teacher-taunton-ma-120800812204032156) |
| Daytime Les Mills BODYCOMBAT Instructor | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/b/d2/19d24aa8596ad5f326eff7200c0b5.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Old Colony YMCA | [View](https://www.openjobs-ai.com/jobs/daytime-les-mills-bodycombat-instructor-plymouth-ma-120800812204032157) |
| Child Care Teacher Assistant | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/b/d2/19d24aa8596ad5f326eff7200c0b5.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Blanche Ames Elementary-Part Time at Old Colony YMCA | [View](https://www.openjobs-ai.com/jobs/child-care-teacher-assistant-at-blanche-ames-elementary-part-time-easton-center-ma-120800812204032158) |
| Lifeguard | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/b/d2/19d24aa8596ad5f326eff7200c0b5.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Old Colony YMCA | [View](https://www.openjobs-ai.com/jobs/lifeguard-east-bridgewater-ma-120800812204032159) |
| Infant Teacher | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/b/d2/19d24aa8596ad5f326eff7200c0b5.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Old Colony YMCA | [View](https://www.openjobs-ai.com/jobs/infant-teacher-taunton-ma-120800812204032160) |
| Swim Instructor | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/b/d2/19d24aa8596ad5f326eff7200c0b5.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Old Colony YMCA | [View](https://www.openjobs-ai.com/jobs/swim-instructor-easton-center-ma-120800812204032161) |
| School Age Site Coordinator | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/b/d2/19d24aa8596ad5f326eff7200c0b5.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Old Colony YMCA | [View](https://www.openjobs-ai.com/jobs/school-age-site-coordinator-whitman-ma-120800812204032162) |
| Private Volleyball Instructor | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/b/d2/19d24aa8596ad5f326eff7200c0b5.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Old Colony YMCA | [View](https://www.openjobs-ai.com/jobs/private-volleyball-instructor-east-bridgewater-ma-120800812204032163) |
| Housing Coordinator | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/b/d2/19d24aa8596ad5f326eff7200c0b5.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Old Colony YMCA | [View](https://www.openjobs-ai.com/jobs/housing-coordinator-brockton-ma-120800812204032164) |
| Financial Planner | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/1/66/11a12d43fa84348321533d9e969ef.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Prudential Financial | [View](https://www.openjobs-ai.com/jobs/financial-planner-edwardsville-il-120800812204032165) |
| Sr. Sales Director, Biopharma | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/1/cc/1d4f878a2161a08fcf90ddd1a4f2c.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> BostonGene | [View](https://www.openjobs-ai.com/jobs/sr-sales-director-biopharma-united-states-120800812204032166) |
| Sr. Regulatory & Market Compliance Engineer | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/6/0b/90ccf85fb6d59c02cf47ec36866aa.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Tesla | [View](https://www.openjobs-ai.com/jobs/sr-regulatory-market-compliance-engineer-fremont-ca-120800812204032167) |
| Software Engineer - Agentic AI (San Francisco) | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/3/4c/bccba639b03ac2490bb69abb8a6e0.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Greylock Partners | [View](https://www.openjobs-ai.com/jobs/software-engineer-agentic-ai-san-francisco-san-francisco-ca-120800812204032168) |

<p align="center">
  <em>...and 0 more jobs</em>
</p>

<p align="center">
  <a href="https://www.openjobs-ai.com/deepsearch"><strong>Browse All Jobs →</strong></a>
</p>

---

<p align="center">
  Made with Python + GitHub Actions · Updated January 05, 2026
</p>
