<p align="center">
  <img src="https://img.shields.io/badge/jobs-49+-blue?style=for-the-badge" alt="Jobs Count">
  <img src="https://img.shields.io/badge/companies-47+-purple?style=for-the-badge" alt="Companies">
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
- **Auto-Updated Every 6 Hours** - Fresh jobs from 47+ companies via GitHub Actions
- **Zero Infrastructure** - Runs entirely on GitHub Pages + Cloudflare (free tier)
- **Lightweight** - Pure Python, no external dependencies, <1MB total size
- **SEO Optimized** - Proper sitemaps, meta tags, and structured content

## Job Statistics

| Category | Count |
|----------|------:|
| Other | 26 |
| Healthcare | 13 |
| Engineering | 4 |
| Sales | 3 |
| Management | 3 |
| Finance | 0 |
| Marketing | 0 |
| HR | 0 |
| Operations | 0 |

**Top Hiring Companies:** MUSC Health, Northwell Health, Merakey, Arcfield, Multiple Opportunities, Jefferson

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
│  │ Sitemap     │   │ (49+ jobs) │   │ (README + HTML)     │   │
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
- **And 47+ other companies**

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
  <em>Updated January 03, 2026 · Showing 49 of 49+ jobs</em>
</p>

| Job Title | Company | Apply |
|-----------|---------|:-----:|
| Travel Registered Nurse, RN, Preop/PACU | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/b/f3/2333d35228766428d500d9c926e9d.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Saint Joseph Mercy Health System | [View](https://www.openjobs-ai.com/jobs/travel-registered-nurse-rn-preoppacu-chelsea-mi-120060366553088002) |
| Travel Certified Nursing Assistant CNA- Madison, WI | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/a/31/b21e61326ffe28cdfe762f0d9ca93.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Vibra Healthcare | [View](https://www.openjobs-ai.com/jobs/travel-certified-nursing-assistant-cna-madison-wi-madison-wi-120060366553088003) |
| UHC-Emergency Department Associate (3pm-3:30am)-ED | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/3/36/45bd8ef0ce034df92f81dba43d97f.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> United Hospital Center | [View](https://www.openjobs-ai.com/jobs/uhc-emergency-department-associate-3pm-330am-ed-bridgeport-wv-120060366553088004) |
| Penn Medicine Clinician (Department of Ophthalmology) | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/8/a0/b7b8294e678b7a6abe1f8dc30f73e.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Inside Higher Ed | [View](https://www.openjobs-ai.com/jobs/penn-medicine-clinician-department-of-ophthalmology-philadelphia-pa-120060542713856000) |
| Supported Living Aide | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/b/cc/ca52bce9acdc7a17495369e4c4b29.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Merakey | [View](https://www.openjobs-ai.com/jobs/supported-living-aide-middletown-pa-120059972288512026) |
| Portfolio & Strategic Planning Analyst | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/1/76/618905f90a763f4604896f7ed7599.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Arcfield | [View](https://www.openjobs-ai.com/jobs/portfolio-strategic-planning-analyst-chantilly-va-120059972288512027) |
| Graduate Nurse | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/3/f8/cac30b742d64b4ec837083f80ce7b.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Multiple Opportunities, Jefferson | [View](https://www.openjobs-ai.com/jobs/graduate-nurse-multiple-opportunities-jefferson-sign-on-bonus-clairton-pa-120059972288512028) |
| Guest Services Representative (Concierge) | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/e/16/eb7f343d8c9142856d7ab257ea40a.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> MUSC Health | [View](https://www.openjobs-ai.com/jobs/guest-services-representative-concierge-charleston-sc-120059972288512029) |
| Intern APRN | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/7/48/57c57e59564f634ad9008098fc050.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Lakeview Center | [View](https://www.openjobs-ai.com/jobs/intern-aprn-pensacola-fl-120059972288512030) |
| Retail Sales Associate | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/5/52/5ff59adcaac313923ab89d0a618c5.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Verizon | [View](https://www.openjobs-ai.com/jobs/retail-sales-associate-staten-island-ny-120059972288512031) |
| Medical Specialist 2 | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/9/33/7af27fb32cbfac2a3a53fa51ef09f.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> NYS Office for People With Developmental Disabilities | [View](https://www.openjobs-ai.com/jobs/medical-specialist-2-wyoming-united-states-120059972288512032) |
| Energy Sales Specialist | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/a/55/55a1f18d9e6ab6d34b65f95e05ea2.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> 2020 Companies | [View](https://www.openjobs-ai.com/jobs/energy-sales-specialist-waco-tx-120059972288512033) |
| Physical Therapist   Mineola, TX | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/0/6e/6511b28e511eae9184f0c0cfe3f71.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Continuum Rehab Group | [View](https://www.openjobs-ai.com/jobs/physical-therapist-mineola-tx-mineola-tx-120059972288512034) |
| Semantic Data Engineer | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/0/26/b748e01bb402e80b11dacc7da0976.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Cambia Health Solutions | [View](https://www.openjobs-ai.com/jobs/semantic-data-engineer-boise-id-120059972288512035) |
| Social Worker Senior | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/3/f8/cac30b742d64b4ec837083f80ce7b.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Center for Inclusion Health | [View](https://www.openjobs-ai.com/jobs/social-worker-senior-center-for-inclusion-health-full-time-day-shift-pittsburgh-pa-120059972288512036) |
| LPN - Licensed Practical Nurse | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/9/bd/61cd761fa5af96b437777af4bcbb1.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Elderwood | [View](https://www.openjobs-ai.com/jobs/lpn-licensed-practical-nurse-burlington-vt-120059972288512037) |
| Personal Care Aide - Hartfield | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/c/e3/0aef1e0adce8f087bfa8f644c36c7.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Americare Plus | [View](https://www.openjobs-ai.com/jobs/personal-care-aide-hartfield-hartfield-va-120059972288512038) |
| Registered Nurse II - RN CICU ( PRN ) | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/e/16/eb7f343d8c9142856d7ab257ea40a.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> MUSC Health | [View](https://www.openjobs-ai.com/jobs/registered-nurse-ii-rn-cicu-prn--columbia-sc-120059972288512039) |
| Senior IT Project/Program Manager | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/d/1c/d6e549ab60b728497f73aeeccc9ba.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> ServiceNow | [View](https://www.openjobs-ai.com/jobs/senior-it-projectprogram-manager-atlanta-ga-120059972288512041) |
| Assistant Branch Manager | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/c/92/cb0d3026f31b1cfeec587106702f6.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> NBT Bank | [View](https://www.openjobs-ai.com/jobs/assistant-branch-manager-syracuse-ny-120059972288512042) |
| Naval Engineering Systems Analyst | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/4/0a/3a863dd9addd216cb485c989a2665.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> ICI Services Corporation | [View](https://www.openjobs-ai.com/jobs/naval-engineering-systems-analyst-portsmouth-va-120059972288512043) |
| Backbone Network Engineer | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/9/77/ce84ab4f0d997a3f6a22ad9766923.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> IMC Trading | [View](https://www.openjobs-ai.com/jobs/backbone-network-engineer-chicago-il-120059972288512044) |
| Purchasing Assistant - Hudson, FL | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/b/a5/96fcd7b0a047a960f685075910a6b.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> VetJobs | [View](https://www.openjobs-ai.com/jobs/purchasing-assistant-hudson-fl-hudson-fl-120059972288512045) |
| Account Executive | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/5/15/496aebe827c2583f1eaa804c796de.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> PaulHood | [View](https://www.openjobs-ai.com/jobs/account-executive-united-states-120059972288512046) |
| ServiceNow | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/5/13/9fe096ac3abc5eb9438fae1dd49d1.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Strategic Portfolio Mgmt (SPM) Senior | [View](https://www.openjobs-ai.com/jobs/servicenow-strategic-portfolio-mgmt-spm-senior-tech-cons-open-location-milwaukee-wi-120059972288512047) |
| Nurse Assistant | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/e/f2/496687eb1e6a5defe1e3999262b82.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> MG2 Telemetry | [View](https://www.openjobs-ai.com/jobs/nurse-assistant-mg2-telemetry-full-time-nights-st-mary-langhorne-pa-120059972288512048) |
| Coding Expert -  Java (Contract) | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/2c/fa2b73798467213ecb36f32690252.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Alignerr | [View](https://www.openjobs-ai.com/jobs/coding-expert-java-contract-san-francisco-ca-120059972288512049) |
| Naturalist, Education Specialist - Outdoor Education | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/7/df/add544544e242ae5c80f03e0cab7c.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Los Angeles County Office of Education | [View](https://www.openjobs-ai.com/jobs/naturalist-education-specialist-outdoor-education-downey-ca-120059972288512050) |
| Senior Patient Account Representative | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/5/43/22ecadc07886b17b3ef5fad15e04b.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Northwell Health | [View](https://www.openjobs-ai.com/jobs/senior-patient-account-representative-melville-ny-120060165226496000) |
| Nursing Assistant II (SY) | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/5/43/22ecadc07886b17b3ef5fad15e04b.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Northwell Health | [View](https://www.openjobs-ai.com/jobs/nursing-assistant-ii-sy-syosset-ny-120060165226496001) |
| Senior Buyer | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/c/41/6e19b06d4280a2af63bd4da27448c.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Kindred Motorworks | [View](https://www.openjobs-ai.com/jobs/senior-buyer-vallejo-ca-120060165226496002) |
| As-Needed Student Intern I/II/III | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/6/2d/8f3c24f3bda92221ddb6549434ea2.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> City of Santa Clara | [View](https://www.openjobs-ai.com/jobs/as-needed-student-intern-iiiiii-santa-clara-ca-120060165226496003) |
| Outpatient Registered Nurse - Melanoma Medical Oncology | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/2/09/9c4fdc666c6fb7f228bbcdf9dfbbc.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> University of Utah Health | [View](https://www.openjobs-ai.com/jobs/outpatient-registered-nurse-melanoma-medical-oncology-salt-lake-city-ut-120060165226496004) |
| Delivery Driver(2496) | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/a/c3/db8b53ac9db0fb462a49a5c694d42.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Domino's | [View](https://www.openjobs-ai.com/jobs/delivery-driver2496-chardon-oh-120060165226496005) |
| Customer Success, Midwest (Chicago Based) | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/b/99/f4ffa9ab72edd083fd16dd2e86ca5.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Goalbook | [View](https://www.openjobs-ai.com/jobs/customer-success-midwest-chicago-based-chicago-il-120060165226496006) |
| Stylist | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/6/5a/7325633d5b9df8511e994c1a08f29.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Supercuts | [View](https://www.openjobs-ai.com/jobs/stylist-fishers-in-120060165226496007) |
| OILER | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/b/23/77f1461d9cc31d071224503137542.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Solid Waste Authority of Palm Beach County | [View](https://www.openjobs-ai.com/jobs/oiler-west-palm-beach-fl-120060165226496008) |
| Aquatics Recreation Activities Instructor | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/3/d0/4c3990560ee196dc381e4d485a97a.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> City of Norfolk, VA | [View](https://www.openjobs-ai.com/jobs/aquatics-recreation-activities-instructor-norfolk-va-120060165226496009) |
| Director of Health Services | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/a/ea/2946be6fac74ead98638a99078b2b.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> MBK Senior Living | [View](https://www.openjobs-ai.com/jobs/director-of-health-services-petaluma-ca-120060165226496010) |
| Construction Maintenance Technician - Transportation and Environmental Services | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/3/82/98a3de3c46c7fb9b732356d8432cb.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> City of Kannapolis | [View](https://www.openjobs-ai.com/jobs/construction-maintenance-technician-transportation-and-environmental-services-kannapolis-nc-120060165226496011) |
| Juvenile Probation Officer I: Field | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/c/c7/475150220b86db4eabbb714509630.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Williamson County | [View](https://www.openjobs-ai.com/jobs/juvenile-probation-officer-i-field-georgetown-tx-120060165226496012) |
| Accountant I - Chaska | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/0/93/16f0f1f508c37efe305f8df780556.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Central Minnesota Jobs and Training Services, Inc. | [View](https://www.openjobs-ai.com/jobs/accountant-i-chaska-minnesota-united-states-120060165226496013) |
| Receptionist - (Spanish/English) | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/8/4d/d261e0e2deb9c2df92d5aca47be72.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Tulsa Health Department | [View](https://www.openjobs-ai.com/jobs/receptionist-spanishenglish-tulsa-ok-120060165226496015) |
| **Customer Service & Data Entry Specialists (Multiple Positions) | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/c/9f/58a5ecf648b32acec045a8e4592aa.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Clerk of the Circuit Court & Comptroller, Palm Beach County | [View](https://www.openjobs-ai.com/jobs/customer-service-data-entry-specialists-multiple-positions-west-palm-beach-fl-120060165226496017) |
| Tax | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/5/13/9fe096ac3abc5eb9438fae1dd49d1.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Business Tax Services | [View](https://www.openjobs-ai.com/jobs/tax-business-tax-services-private-tax-wealth-tax-advisory-senior-indianapolis-in-120060165226496021) |
| Chief Health and Human Services Officer | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/9/6b/fab59ee61ae4a0f0e5c48d96e0f42.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> New Hanover County | [View](https://www.openjobs-ai.com/jobs/chief-health-and-human-services-officer-wilmington-nc-120060165226496022) |
| Physical Therapy Assistant - Home Health | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/4/1d/52157ce5aaf1dc255d03d1492f70f.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Capital Health Care Network | [View](https://www.openjobs-ai.com/jobs/physical-therapy-assistant-home-health-dublin-oh-120060165226496023) |
| Graduate Leadership Program - AI Strategy, Solutions & Automation Track | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/6/9c/b08fe26d10bea71059627c6d76301.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Camelot Strategic Marketing & Media | [View](https://www.openjobs-ai.com/jobs/graduate-leadership-program-ai-strategy-solutions-automation-track-dallas-tx-120060366553088000) |
| Systems Modernization & Tech Delivery Solution Architect - Manager | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/d/e9/eb4f510fd5b7c1314d9f9b37e43f8.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> PwC | [View](https://www.openjobs-ai.com/jobs/systems-modernization-tech-delivery-solution-architect-manager-las-vegas-nv-120060366553088001) |

<p align="center">
  <em>...and 0 more jobs</em>
</p>

<p align="center">
  <a href="https://www.openjobs-ai.com/deepsearch"><strong>Browse All Jobs →</strong></a>
</p>

---

<p align="center">
  Made with Python + GitHub Actions · Updated January 03, 2026
</p>
