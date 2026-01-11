<p align="center">
  <img src="https://img.shields.io/badge/jobs-18+-blue?style=for-the-badge" alt="Jobs Count">
  <img src="https://img.shields.io/badge/companies-18+-purple?style=for-the-badge" alt="Companies">
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
- **Auto-Updated Every 6 Hours** - Fresh jobs from 18+ companies via GitHub Actions
- **Zero Infrastructure** - Runs entirely on GitHub Pages + Cloudflare (free tier)
- **Lightweight** - Pure Python, no external dependencies, <1MB total size
- **SEO Optimized** - Proper sitemaps, meta tags, and structured content

## Job Statistics

| Category | Count |
|----------|------:|
| Other | 7 |
| Healthcare | 5 |
| Engineering | 3 |
| Management | 2 |
| Sales | 1 |
| Finance | 0 |
| Marketing | 0 |
| HR | 0 |
| Operations | 0 |

**Top Hiring Companies:** Xylem Tree Experts, Senior, Bonsai Rehab, Indiana University Health, Tennessee Orthopaedic Alliance

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
│  │ Sitemap     │   │ (18+ jobs) │   │ (README + HTML)     │   │
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
- **And 18+ other companies**

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
  <em>Updated January 11, 2026 · Showing 18 of 18+ jobs</em>
</p>

| Job Title | Company | Apply |
|-----------|---------|:-----:|
| Advanced Practice Provider (ACNP/PAC) | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/4/e1/728274e1bcdc43527b9385317bc6e.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> UNIVERSITY HOSPITAL CLEVELAND MEDICAL CENTER | [View](https://www.openjobs-ai.com/jobs/advanced-practice-provider-acnppac-cleveland-oh-122597605900288000) |
| Vascular Sonographer | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/0/88/990f3f3ed832714b7c2699cfb6455.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Colorado Springs Cardiology | [View](https://www.openjobs-ai.com/jobs/vascular-sonographer-colorado-springs-co-122597693980672000) |
| Assistant Store Manager | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/1/06/4f374a8885050a201343f5fa5a04e.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Save A Lot Grocery | [View](https://www.openjobs-ai.com/jobs/assistant-store-manager-warren-oh-122597693980672001) |
| Supply Spec III - YC | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/6/bc/2f275e81504887c7d01c05bcd8c14.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> State of South Carolina | [View](https://www.openjobs-ai.com/jobs/supply-spec-iii-yc-columbia-sc-122597790449664000) |
| Azure DevOps Engineer – AI-Enhanced Cloud Automation | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/a/ba/46b6c52aa61a6c637f1eec5b7248c.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Pinnacle Technology Partners | [View](https://www.openjobs-ai.com/jobs/azure-devops-engineer-ai-enhanced-cloud-automation-latin-america-122597912084480000) |
| Naturopathic Doctor | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/8/ec/a5b55f989afc8207fadafc3b6cd65.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Regenerate Health Medical Center | [View](https://www.openjobs-ai.com/jobs/naturopathic-doctor-santa-barbara-ca-122598109216768000) |
| Foreperson - Chattanooga, TN | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/3/a3/f22bee0e2b0f100729a5f627f017d.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Xylem Tree Experts | [View](https://www.openjobs-ai.com/jobs/foreperson-chattanooga-tn-chattanooga-tn-122597232607232040) |
| Databricks Data Engineer | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/5/13/9fe096ac3abc5eb9438fae1dd49d1.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Senior | [View](https://www.openjobs-ai.com/jobs/databricks-data-engineer-senior-consulting-location-open-1-sacramento-ca-122597232607232041) |
| Physical Therapist - Outpatient | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/6/89/39d75e6682e401254ac51423968ab.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Bonsai Rehab | [View](https://www.openjobs-ai.com/jobs/physical-therapist-outpatient-highland-park-il-122597232607232042) |
| Medical Assistant II - Dermatology | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/e/1f/82e49bae801110e99bcd57841853d.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Indiana University Health | [View](https://www.openjobs-ai.com/jobs/medical-assistant-ii-dermatology-frankfort-in-122597232607232043) |
| Physician Assistant | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/1/73/f525cb5d190277073b6ba9dd816b7.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Tennessee Orthopaedic Alliance | [View](https://www.openjobs-ai.com/jobs/physician-assistant-ethridge-tn-122597232607232044) |
| MICU RN | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/d/03/4839dae0d89b917f934a02ea1f6d0.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> CHI | [View](https://www.openjobs-ai.com/jobs/micu-rn-houston-tx-122597232607232045) |
| Sales Development Representative | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/1/9a/a4b2cd53260650fe45b9a0d6e7540.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Remote Leverage | [View](https://www.openjobs-ai.com/jobs/sales-development-representative-latin-america-122597425545216000) |
| Head Boys Wrestling Coach | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/e/2a/af0492f7d287d5e6fcd5c1d5250e0.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Regina Inter-Parish Catholic Education Center | [View](https://www.openjobs-ai.com/jobs/head-boys-wrestling-coach-iowa-city-ia-122597425545216001) |
| Echocardiographic and Vascular Technicians | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/6/86/b093666f373b552ddd3caa0c8a1e5.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Heart Lab Diagnostics | [View](https://www.openjobs-ai.com/jobs/echocardiographic-and-vascular-technicians-columbia-md-122597425545216002) |
| Psychiatric Nurse Practitioner | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/d/c4/cb61179c543689a4a460f3871ac8f.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> LumiClinics Behavioral Wellness Center | [View](https://www.openjobs-ai.com/jobs/psychiatric-nurse-practitioner-glenview-il-122597425545216003) |
| Founding Agent Infra Engineer | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/9/e2/5dc28e6e2517b74a67f46dc075ea8.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Fibonacci | [View](https://www.openjobs-ai.com/jobs/founding-agentinfra-engineer-san-jose-ca-122597425545216004) |
| Area Director | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/d/f3/b42bf001ae9feb8ce30fc2bb21f30.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Fellowship of Christian Athletes | [View](https://www.openjobs-ai.com/jobs/area-director-durango-co-122597425545216005) |

<p align="center">
  <em>...and 0 more jobs</em>
</p>

<p align="center">
  <a href="https://www.openjobs-ai.com/deepsearch"><strong>Browse All Jobs →</strong></a>
</p>

---

<p align="center">
  Made with Python + GitHub Actions · Updated January 11, 2026
</p>
