<p align="center">
  <img src="https://img.shields.io/badge/jobs-88+-blue?style=for-the-badge" alt="Jobs Count">
  <img src="https://img.shields.io/badge/companies-82+-purple?style=for-the-badge" alt="Companies">
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
- **Auto-Updated Every 6 Hours** - Fresh jobs from 82+ companies via GitHub Actions
- **Zero Infrastructure** - Runs entirely on GitHub Pages + Cloudflare (free tier)
- **Lightweight** - Pure Python, no external dependencies, <1MB total size
- **SEO Optimized** - Proper sitemaps, meta tags, and structured content

## Job Statistics

| Category | Count |
|----------|------:|
| Other | 55 |
| Healthcare | 14 |
| Management | 9 |
| Engineering | 4 |
| Sales | 3 |
| Finance | 2 |
| Operations | 1 |
| Marketing | 0 |
| HR | 0 |

**Top Hiring Companies:** City of Sunrise, UNC Health Blue Ridge, Tennova Healthcare- North Knoxville Medical Center, Brown University Health, U.S. Bank

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
│  │ Sitemap     │   │ (88+ jobs) │   │ (README + HTML)     │   │
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
- **And 82+ other companies**

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
  <em>Updated January 08, 2026 · Showing 88 of 88+ jobs</em>
</p>

| Job Title | Company | Apply |
|-----------|---------|:-----:|
| Board Certified Assistant Behavior Analyst | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/c/09/4d89dbf3836f91982dfd93dd33aec.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> The Spark Center For Autism | [View](https://www.openjobs-ai.com/jobs/board-certified-assistant-behavior-analyst-farmington-mi-121872486236160003) |
| Director, Sales | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/8/55/167adba73438514fd36796a83008d.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> TriNet | [View](https://www.openjobs-ai.com/jobs/director-sales-washington-dc-121872486236160004) |
| Director of Sales | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/3/d9/2cbc9d7adbb9c1390a745632dcb18.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Cadrex Manufacturing Solutions | [View](https://www.openjobs-ai.com/jobs/director-of-sales-greater-chicago-area-121872486236160005) |
| Safety Manager | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/9/93/c387ddff46881d42aab12338ef232.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> City of Rockville | [View](https://www.openjobs-ai.com/jobs/safety-manager-rockville-md-121872486236160006) |
| Seasonal Assistant Site Supervisor | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/6/3d/c57d9d3a3cd51e256d1d4df625378.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> City of Sunrise | [View](https://www.openjobs-ai.com/jobs/seasonal-assistant-site-supervisor-sunrise-fl-121872486236160007) |
| Traveling Dental Assistant Endodontics | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/c/28/aa064f136ba3320b0bfba0b859222.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> PDS Health | [View](https://www.openjobs-ai.com/jobs/traveling-dental-assistant-endodontics-west-covina-ca-121872486236160008) |
| Jobs PLUS Ausbildung | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/6/87/9a118453821bfae8b15483b855d8c.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Haus der Barmherzigkeit | [View](https://www.openjobs-ai.com/jobs/jobs-plus-ausbildung-habit-ky-121872486236160009) |
| Physical Therapist Assistant | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/1/f9/634ceab762bd341813afd627274f9.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> BenchMark Physical Therapy | [View](https://www.openjobs-ai.com/jobs/physical-therapist-assistant-clayton-nc-121872486236160010) |
| Seasonal Recreation Counselor II | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/6/3d/c57d9d3a3cd51e256d1d4df625378.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> City of Sunrise | [View](https://www.openjobs-ai.com/jobs/seasonal-recreation-counselor-ii-sunrise-fl-121872486236160011) |
| Police Cadet | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/6/a2/3d1bf639532e4d439c11e9d9fe7a7.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> City of Gaithersburg | [View](https://www.openjobs-ai.com/jobs/police-cadet-gaithersburg-md-121872486236160012) |
| Infusion Registered Nurse | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/b/2c/7c83dce43e8e274d4a082bfd09a46.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Tulea Health | [View](https://www.openjobs-ai.com/jobs/infusion-registered-nurse-meadowbrook-pa-121872486236160013) |
| Project Manager | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/c/34/693d97965058ccaaeca1ecd37f3a1.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> TELUS Digital AI Data Solutions | [View](https://www.openjobs-ai.com/jobs/project-manager-latin-america-121872486236160014) |
| Registrar | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/4/97/c187acec04777d178a57b613f6c3d.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Lutheran Health Network | [View](https://www.openjobs-ai.com/jobs/registrar-fort-wayne-in-121872486236160015) |
| Personal Injury Pre-Litigation Attorney | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/b/51/9c0cfe4ad1eb751751034e15b1ca6.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Alex Hanna Law | [View](https://www.openjobs-ai.com/jobs/personal-injury-pre-litigation-attorney-miami-fl-121872486236160016) |
| RN | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/d/51/406738402c6b2102788ebe2cc2da0.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> UNC Health Blue Ridge | [View](https://www.openjobs-ai.com/jobs/rn-morganton-nc-121872486236160017) |
| Board Certified Behavior Analyst | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/5/af/a324f68c0be1b3e86357b5d9f6025.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> New Hope Health | [View](https://www.openjobs-ai.com/jobs/board-certified-behavior-analyst-sterling-va-121872486236160018) |
| FIIS Global Sales Director | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/d/9f/e2b4076e6c62027ef5849a0d4f77b.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> FUJIFILM Dimatix, Inc. | [View](https://www.openjobs-ai.com/jobs/fiis-global-sales-director-lebanon-nh-121872486236160019) |
| Wind Technician II- Oakfield, ME | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/4/54/b7f66fe3b2d3a8a8b239457810f55.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Vestas | [View](https://www.openjobs-ai.com/jobs/wind-technician-ii-oakfield-me-oakfield-me-121872486236160020) |
| Registered Sleep Technologist | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/b7/c82a4c0f3f1282d52b8b5253d1424.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Marathon Medical DME | [View](https://www.openjobs-ai.com/jobs/registered-sleep-technologist-chicago-il-121872486236160021) |
| Consultor SAP Basis – Experto en Migraciones a SAP S/4HANA Cloud (RISE) – 100% Remoto | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/d/ec/190095eb3d4ac86d17fcf838e4b2c.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> SCL Consultores | [View](https://www.openjobs-ai.com/jobs/consultor-sap-basis-experto-en-migraciones-a-sap-s4hana-cloud-rise-100-remoto-latin-america-121872486236160022) |
| Level II NDE Technician | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/b/a8/c3cf3936387098586293fab4fd06f.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> TEAM, Inc. | [View](https://www.openjobs-ai.com/jobs/level-ii-nde-technician-scott-la-121872486236160023) |
| RN L&D PRN Nights | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/c/09/53ef0892af63e17bcd168dbbb1abf.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Tennova Healthcare- North Knoxville Medical Center | [View](https://www.openjobs-ai.com/jobs/rn-ld-prn-nights-powell-tn-121872486236160024) |
| Classroom Behavior Spclist PD | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/9/63/bf5c4caf1b0f406d3f14864c3b95d.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Brown University Health | [View](https://www.openjobs-ai.com/jobs/classroom-behavior-spclist-pd-cumberland-ri-121872486236160025) |
| Nurse Assistant | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/d/17/44e4888f3fb761cc15e830f610496.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> McLaren Health Care | [View](https://www.openjobs-ai.com/jobs/nurse-assistant-port-huron-mi-121872486236160026) |
| PRN RN or LPN | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/3/1d/d7c241ed7629f35214d72222825da.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> YAD Healthcare | [View](https://www.openjobs-ai.com/jobs/prn-rn-or-lpn-greensboro-nc-121872486236160027) |
| RN | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/d/51/406738402c6b2102788ebe2cc2da0.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> UNC Health Blue Ridge | [View](https://www.openjobs-ai.com/jobs/rn-morganton-nc-121872486236160028) |
| Program Manager - Occupational Therapist /OTR: PRN/Part-time | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/7/cf/9da255a99bba5970bc11581ccc24f.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Aegis Therapies | [View](https://www.openjobs-ai.com/jobs/program-manager-occupational-therapist-otr-prnpart-time-fayetteville-nc-121872486236160029) |
| PT Infusion RN | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/c/b8/83ae08ac3b4b05b22418eba38967f.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Baldwin Health | [View](https://www.openjobs-ai.com/jobs/pt-infusion-rn-foley-al-121872486236160030) |
| RN Dialysis | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/c/09/53ef0892af63e17bcd168dbbb1abf.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Tennova Healthcare- North Knoxville Medical Center | [View](https://www.openjobs-ai.com/jobs/rn-dialysis-knoxville-tn-121872486236160032) |
| Utilization Care Manager | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/9/63/bf5c4caf1b0f406d3f14864c3b95d.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Brown University Health | [View](https://www.openjobs-ai.com/jobs/utilization-care-manager-taunton-ma-121872486236160033) |
| Business Risk Analyst III | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/1/e0/a60d0c3b35d3dfed8785762b2a2eb.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> RCSA Management (Hybrid | [View](https://www.openjobs-ai.com/jobs/business-risk-analyst-iii-rcsa-management-hybrid-buffalo-ny-buffalo-ny-121872486236160034) |
| Client Relationship Consultant 1-4 (Banker) - Cleveland/Akron Area Branches | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/6/06/06696fb406e6784e14759b729c5b2.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> U.S. Bank | [View](https://www.openjobs-ai.com/jobs/client-relationship-consultant-1-4-banker-clevelandakron-area-branches-elyria-oh-121872486236160035) |
| Client Relationship Consultant 1-4 (Banker) - Cleveland/Akron Area Branches | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/6/06/06696fb406e6784e14759b729c5b2.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> U.S. Bank | [View](https://www.openjobs-ai.com/jobs/client-relationship-consultant-1-4-banker-clevelandakron-area-branches-north-royalton-oh-121872486236160036) |
| Crossing Guard | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/1/6e/999a81c6dc4028147ae39e3dcebf6.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> City of Green Bay | [View](https://www.openjobs-ai.com/jobs/crossing-guard-green-bay-wi-121872687562752000) |
| Police Officer | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/a/c1/488968cee301e087f8c0453f95a54.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> City Of Nogales | [View](https://www.openjobs-ai.com/jobs/police-officer-nogales-az-121872687562752001) |
| Bike Program Staff | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/d/a8/974ace0b844278f7e5a178d98b3d5.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> City of Auburn (Washington) | [View](https://www.openjobs-ai.com/jobs/bike-program-staff-auburn-wa-121872687562752002) |
| Retail Territory Manager - San Jose | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/e/fa/e7ca8e1da83a42960b1ea21477936.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Stanley Black & Decker, Inc. | [View](https://www.openjobs-ai.com/jobs/retail-territory-manager-san-jose-sacramento-ca-121872687562752003) |
| Sourcing Integrated Facilities Management (IFM) Services | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/8/3c/eaf644fbcbd1770b76cce4af1944c.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Chain IQ Group AG | [View](https://www.openjobs-ai.com/jobs/sourcing-integrated-facilities-management-ifm-services-chicago-il-121872792420352000) |
| Audit Senior Associate | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/1/ae/adcdd10a3fc7fe87253316d11890d.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Baker Tilly US | [View](https://www.openjobs-ai.com/jobs/audit-senior-associate-santa-monica-ca-121872792420352001) |
| Archaeologist | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/a/84/5776b86c88722c3599922753be001.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Arcadis | [View](https://www.openjobs-ai.com/jobs/archaeologist-dallas-tx-121872792420352002) |
| Blading Technician | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/9/1a/995c24757ae636532ecdc543a3a40.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Sulzer | [View](https://www.openjobs-ai.com/jobs/blading-technician-la-porte-tx-121872792420352003) |
| Microsoft Solutions Consultant – BizApps | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/7/ab/be6a11e312bc3473251366980d3cd.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> SHI International Corp. | [View](https://www.openjobs-ai.com/jobs/microsoft-solutions-consultant-bizapps-united-states-121872792420352004) |
| Lead Structural Engineer | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/4/ca/a619b12559ad6a37ce02ee1e26624.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> WSP | [View](https://www.openjobs-ai.com/jobs/lead-structural-engineer-chicago-il-121872792420352005) |
| Quality Assurance (QA) Associate | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/5/7d/938e292e4fa3be83b7c3d58aae6fd.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Medpace | [View](https://www.openjobs-ai.com/jobs/quality-assurance-qa-associate-cincinnati-oh-121872792420352006) |
| Geotechnical Engineer - Mid-Level | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/2/92/63e48b92ca6f1137597aecd99edf7.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Sargent & Lundy | [View](https://www.openjobs-ai.com/jobs/geotechnical-engineer-mid-level-chicago-il-121872792420352007) |
| Gate Guard Attendant | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/e/4d/19b727a42b9caa47876db2760a70f.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> City of St. Clair Shores, Michigan | [View](https://www.openjobs-ai.com/jobs/gate-guard-attendant-st-clair-shores-mi-121872792420352008) |
| Shelter Assistant | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/0/d3/f21b48d211c510122603a23a73bfd.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> YWCA Charleston WV | [View](https://www.openjobs-ai.com/jobs/shelter-assistant-charleston-wv-121872792420352009) |
| ADVANCED PRACTICE PROFESSIONALS \| RADIATION ONCOLOGY \| Nurse Practitioner (85001) or Physician Assistant (85101) | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/c/00/1511322ed0675a3189328643615a3.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> WVU Medicine | [View](https://www.openjobs-ai.com/jobs/advanced-practice-professionals-radiation-oncology-nurse-practitioner-85001-or-physician-assistant-85101-morgantown-wv-121872792420352010) |
| Risk Engineering Training Program - Pacific Northwest or Arizona (Summer 2026) | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/a/1e/795edcddc17792f1fe5fc1785d77e.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Zurich North America | [View](https://www.openjobs-ai.com/jobs/risk-engineering-training-program-pacific-northwest-or-arizona-summer-2026-oregon-united-states-121872792420352011) |
| Communication Access Facilitator | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/dc/36374cdf563c1780c2100cd5f2ea7.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Genesee Education Consultant Services (GECS) | [View](https://www.openjobs-ai.com/jobs/communication-access-facilitator-flint-mi-121872792420352012) |
| Auditor | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/8/57/0bdd05aabd4a3d4972ed6a1409a49.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> City of New York | [View](https://www.openjobs-ai.com/jobs/auditor-manhattan-ny-121873010524160000) |
| Investigative Counsel | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/3/bf/79ecd887a2d011bad4797aea58c83.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Wisconsin Court System / Wisconsin Supreme Court | [View](https://www.openjobs-ai.com/jobs/investigative-counsel-madison-wi-121873010524160001) |
| Oracle HCM Configuration Lead - Core HR Module | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/3/39/954f26fc843dc265a62e9669e09d3.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Deloitte | [View](https://www.openjobs-ai.com/jobs/oracle-hcm-configuration-lead-core-hr-module-dayton-oh-121873010524160002) |
| GC Retail Operations Associate Store 553 | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/e/ce/b26d66003463af5b483194bbbe6c1.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> The Guitar Center Company | [View](https://www.openjobs-ai.com/jobs/gc-retail-operations-associate-store-553-north-attleboro-ma-121873010524160003) |
| Spanish 4 Tutor | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/96/01490799486dac16a48801deb8255.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Varsity Tutors, a Nerdy Company | [View](https://www.openjobs-ai.com/jobs/spanish-4-tutor-virginia-beach-va-121873119576064000) |
| High School English Tutor | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/96/01490799486dac16a48801deb8255.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Varsity Tutors, a Nerdy Company | [View](https://www.openjobs-ai.com/jobs/high-school-english-tutor-baton-rouge-la-121873119576064001) |
| Teachers | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/1/94/9865559821a0a0d5663bcd944f7e1.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Erlanger KinderCare at KinderCare Learning Companies | [View](https://www.openjobs-ai.com/jobs/teachers-at-erlanger-kindercare-erlanger-ky-121871735455744617) |
| Teachers | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/1/94/9865559821a0a0d5663bcd944f7e1.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Franconia KinderCare at KinderCare Learning Companies | [View](https://www.openjobs-ai.com/jobs/teachers-at-franconia-kindercare-alexandria-va-121871735455744618) |
| Teachers | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/1/94/9865559821a0a0d5663bcd944f7e1.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Deer Park KinderCare at KinderCare Learning Companies | [View](https://www.openjobs-ai.com/jobs/teachers-at-deer-park-kindercare-deer-park-tx-121871735455744619) |
| Teachers | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/1/94/9865559821a0a0d5663bcd944f7e1.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Fruit Cove KinderCare at KinderCare Learning Companies | [View](https://www.openjobs-ai.com/jobs/teachers-at-fruit-cove-kindercare-fruit-cove-fl-121871735455744620) |
| Teachers | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/1/94/9865559821a0a0d5663bcd944f7e1.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Zorn KinderCare at KinderCare Learning Companies | [View](https://www.openjobs-ai.com/jobs/teachers-at-zorn-kindercare-louisville-ky-121871735455744621) |
| Teachers | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/1/94/9865559821a0a0d5663bcd944f7e1.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Towne Lake KinderCare at KinderCare Learning Companies | [View](https://www.openjobs-ai.com/jobs/teachers-at-towne-lake-kindercare-woodstock-ga-121871735455744622) |
| Teachers | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/1/94/9865559821a0a0d5663bcd944f7e1.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Carnegie Boulevard KinderCare at KinderCare Learning Companies | [View](https://www.openjobs-ai.com/jobs/teachers-at-carnegie-boulevard-kindercare-fort-wayne-in-121871735455744623) |
| Lead Teachers | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/1/94/9865559821a0a0d5663bcd944f7e1.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Naperville West KinderCare at KinderCare Learning Companies | [View](https://www.openjobs-ai.com/jobs/lead-teachers-at-naperville-west-kindercare-naperville-il-121871735455744624) |
| Teachers | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/1/94/9865559821a0a0d5663bcd944f7e1.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Wickham KinderCare at KinderCare Learning Companies | [View](https://www.openjobs-ai.com/jobs/teachers-at-wickham-kindercare-melbourne-fl-121871735455744625) |
| Teachers | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/1/94/9865559821a0a0d5663bcd944f7e1.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Russet KinderCare at KinderCare Learning Companies | [View](https://www.openjobs-ai.com/jobs/teachers-at-russet-kindercare-laurel-md-121871735455744626) |
| Teachers | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/1/94/9865559821a0a0d5663bcd944f7e1.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> KinderCare at Kenilworth at KinderCare Learning Companies | [View](https://www.openjobs-ai.com/jobs/teachers-at-kindercare-at-kenilworth-kenilworth-nj-121871735455744627) |
| Assistant Teachers | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/1/94/9865559821a0a0d5663bcd944f7e1.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Darien KinderCare at KinderCare Learning Companies | [View](https://www.openjobs-ai.com/jobs/assistant-teachers-at-darien-kindercare-darien-il-121871735455744628) |
| Test Engineering Manager | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/a/e7/0f5647294d62e7ebbfac66a59bb12.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> CesiumAstro | [View](https://www.openjobs-ai.com/jobs/test-engineering-manager-austin-tx-121871735455744629) |
| Teachers | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/1/94/9865559821a0a0d5663bcd944f7e1.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> KinderCare at Halliburton at KinderCare Learning Companies | [View](https://www.openjobs-ai.com/jobs/teachers-at-kindercare-at-halliburton-houston-tx-121871735455744630) |
| Teachers | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/1/94/9865559821a0a0d5663bcd944f7e1.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Elkin KinderCare at KinderCare Learning Companies | [View](https://www.openjobs-ai.com/jobs/teachers-at-elkin-kindercare-elkin-nc-121871735455744631) |
| Teachers | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/1/94/9865559821a0a0d5663bcd944f7e1.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> North Ridgeville KinderCare at KinderCare Learning Companies | [View](https://www.openjobs-ai.com/jobs/teachers-at-north-ridgeville-kindercare-north-ridgeville-oh-121871735455744632) |
| Teachers | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/1/94/9865559821a0a0d5663bcd944f7e1.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Ballinger Shoreline KinderCare at KinderCare Learning Companies | [View](https://www.openjobs-ai.com/jobs/teachers-at-ballinger-shoreline-kindercare-shoreline-wa-121871735455744633) |
| Teachers | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/1/94/9865559821a0a0d5663bcd944f7e1.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Fielday School KinderCare at KinderCare Learning Companies | [View](https://www.openjobs-ai.com/jobs/teachers-at-fielday-school-kindercare-las-vegas-nv-121871735455744634) |
| Assistant Teachers | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/1/94/9865559821a0a0d5663bcd944f7e1.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> West Oswego KinderCare at KinderCare Learning Companies | [View](https://www.openjobs-ai.com/jobs/assistant-teachers-at-west-oswego-kindercare-oswego-il-121871735455744635) |
| Teachers | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/1/94/9865559821a0a0d5663bcd944f7e1.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Escondido KinderCare at KinderCare Learning Companies | [View](https://www.openjobs-ai.com/jobs/teachers-at-escondido-kindercare-escondido-ca-121871735455744636) |
| Teachers | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/1/94/9865559821a0a0d5663bcd944f7e1.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Neenah KinderCare at KinderCare Learning Companies | [View](https://www.openjobs-ai.com/jobs/teachers-at-neenah-kindercare-neenah-wi-121871735455744637) |
| Lead Teachers | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/1/94/9865559821a0a0d5663bcd944f7e1.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> North Arlington Hts KinderCare at KinderCare Learning Companies | [View](https://www.openjobs-ai.com/jobs/lead-teachers-at-north-arlington-hts-kindercare-arlington-heights-il-121871735455744638) |
| Teachers | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/1/94/9865559821a0a0d5663bcd944f7e1.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Owings Mills KinderCare at KinderCare Learning Companies | [View](https://www.openjobs-ai.com/jobs/teachers-at-owings-mills-kindercare-owings-mills-md-121871735455744639) |
| Lead Teachers | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/1/94/9865559821a0a0d5663bcd944f7e1.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Elmhurst KinderCare at KinderCare Learning Companies | [View](https://www.openjobs-ai.com/jobs/lead-teachers-at-elmhurst-kindercare-elmhurst-il-121871735455744640) |
| Teachers | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/1/94/9865559821a0a0d5663bcd944f7e1.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> KinderCare at Bergstrom Tech at KinderCare Learning Companies | [View](https://www.openjobs-ai.com/jobs/teachers-at-kindercare-at-bergstrom-tech-austin-tx-121871735455744641) |
| Teachers | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/1/94/9865559821a0a0d5663bcd944f7e1.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Cottage Grove KinderCare at KinderCare Learning Companies | [View](https://www.openjobs-ai.com/jobs/teachers-at-cottage-grove-kindercare-cottage-grove-mn-121871735455744642) |
| Teachers | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/1/94/9865559821a0a0d5663bcd944f7e1.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Forestville KinderCare at KinderCare Learning Companies | [View](https://www.openjobs-ai.com/jobs/teachers-at-forestville-kindercare-anderson-oh-121871735455744643) |
| Teachers | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/1/94/9865559821a0a0d5663bcd944f7e1.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Missouri City KinderCare at KinderCare Learning Companies | [View](https://www.openjobs-ai.com/jobs/teachers-at-missouri-city-kindercare-missouri-city-tx-121871735455744644) |
| Teachers | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/1/94/9865559821a0a0d5663bcd944f7e1.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Perris KinderCare at KinderCare Learning Companies | [View](https://www.openjobs-ai.com/jobs/teachers-at-perris-kindercare-perris-ca-121871735455744645) |
| Security Officer | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/7/59/cd572b56558fd2ac997304584961c.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Ann & Robert H. Lurie Children's Hospital of Chicago | [View](https://www.openjobs-ai.com/jobs/security-officer-streeterville-il-121872486236160000) |
| Truck/Equipment Technician III - Fleet | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/0/3c/56df6d7b4b16265888559d2828b62.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Cobb County Government | [View](https://www.openjobs-ai.com/jobs/truckequipment-technician-iii-fleet-marietta-ga-121872486236160001) |
| Learning and Development Partner - AI Adoption and Content | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/e/4e/a15aef1a20a952d17dd0fb9ab024a.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> iPipeline | [View](https://www.openjobs-ai.com/jobs/learning-and-development-partner-ai-adoption-and-content-wayne-pa-121872486236160002) |

<p align="center">
  <em>...and 0 more jobs</em>
</p>

<p align="center">
  <a href="https://www.openjobs-ai.com/deepsearch"><strong>Browse All Jobs →</strong></a>
</p>

---

<p align="center">
  Made with Python + GitHub Actions · Updated January 08, 2026
</p>
