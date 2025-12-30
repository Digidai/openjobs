<p align="center">
  <img src="https://img.shields.io/badge/jobs-159+-blue?style=for-the-badge" alt="Jobs Count">
  <img src="https://img.shields.io/badge/companies-131+-purple?style=for-the-badge" alt="Companies">
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
- **Auto-Updated Every 6 Hours** - Fresh jobs from 131+ companies via GitHub Actions
- **Zero Infrastructure** - Runs entirely on GitHub Pages + Cloudflare (free tier)
- **Lightweight** - Pure Python, no external dependencies, <1MB total size
- **SEO Optimized** - Proper sitemaps, meta tags, and structured content

## Job Statistics

| Category | Count |
|----------|------:|
| Other | 61 |
| Healthcare | 39 |
| Management | 32 |
| Engineering | 15 |
| Sales | 8 |
| HR | 2 |
| Finance | 1 |
| Operations | 1 |
| Marketing | 0 |

**Top Hiring Companies:** Inside Higher Ed, Allegheny Health Network, Addus HomeCare, Apex Systems, CVS Health

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
│  │ Sitemap     │   │ (159+ jobs) │   │ (README + HTML)     │   │
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
- **And 131+ other companies**

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
  <em>Updated December 30, 2025 · Showing 159 of 159+ jobs</em>
</p>

| Job Title | Company | Apply |
|-----------|---------|:-----:|
| Habilitation Technician/ DSP | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/e/25/fdf5c5d48111aedbf1d70ee1845f9.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> BAYADA Home Health Care | [View](https://www.openjobs-ai.com/jobs/habilitation-technician-dsp-butler-pa-118609535827968070) |
| Caregiver | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/2/c5/c9d983d4c0b2660aa197f4229d9fd.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Girling Personal Care | [View](https://www.openjobs-ai.com/jobs/caregiver-eddy-tx-118609535827968071) |
| Caregiver | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/4/4e/67b9271758edace29205a88209e73.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Addus HomeCare | [View](https://www.openjobs-ai.com/jobs/caregiver-abingdon-va-118609535827968072) |
| Home Care Aide Flex | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/4/4e/67b9271758edace29205a88209e73.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Addus HomeCare | [View](https://www.openjobs-ai.com/jobs/home-care-aide-flex-vanadium-nm-118609535827968073) |
| Certified Nurse Assistant | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/0/01/6b469c2071eef5856ef57a5cd3c19.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Kaleida Health | [View](https://www.openjobs-ai.com/jobs/certified-nurse-assistant-buffalo-ny-118609535827968076) |
| Fire Alarm & Sprinkler Inspection Coordinator | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/7/81/c6548ba8eb911a20e02d0f14092d7.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Johnson Controls | [View](https://www.openjobs-ai.com/jobs/fire-alarm-sprinkler-inspection-coordinator-rocky-hill-ct-118609535827968077) |
| WORK FROM HOME | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/a/96/6a1b0b49eb43b920b59369d1a52a8.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> The Jernigan Agency | [View](https://www.openjobs-ai.com/jobs/work-from-home-santa-fe-nm-118609535827968078) |
| Sales Representative- Commercial Knife Sharpening | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/9/07/92add1b37ec41279aab8fdee97b0b.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> ZWILLING J.A. Henckels LLC | [View](https://www.openjobs-ai.com/jobs/sales-representative-commercial-knife-sharpening-united-states-118609535827968079) |
| Senior People Operations Partner | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/7/19/4637430699b20c08fe28014e627ed.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Delta Faucet Company | [View](https://www.openjobs-ai.com/jobs/senior-people-operations-partner-jackson-tn-118609535827968080) |
| Physical Therapist | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/6/7a/ccbdd556d283b6dd5ec2767e14a21.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> AdvisaCare | [View](https://www.openjobs-ai.com/jobs/physical-therapist-lansing-mi-118609535827968081) |
| Scientific Account Manager | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/0/ab/6308602155b169cc66b419afb0c2c.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Genedata | [View](https://www.openjobs-ai.com/jobs/scientific-account-manager-greater-boston-118609535827968082) |
| Telemetry RN | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/0/01/6b469c2071eef5856ef57a5cd3c19.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Kaleida Health | [View](https://www.openjobs-ai.com/jobs/telemetry-rn-buffalo-ny-118609535827968083) |
| Production Packaging Associate | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/4/fe/be475364af816ff305fe1041d72b9.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Altium Packaging | [View](https://www.openjobs-ai.com/jobs/production-packaging-associate-verona-pa-118609535827968084) |
| Sr Principal Systems Engineer - R10217500 | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/9/f9/a06fe333c20e4f7a62138add976cf.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Northrop Grumman | [View](https://www.openjobs-ai.com/jobs/sr-principal-systems-engineer-r10217500-los-angeles-ca-118609535827968085) |
| Occupational Therapist Per Diem 777001 | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/6/bb/f353d6c18a30c9c6273c012c8e406.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Huntington Health | [View](https://www.openjobs-ai.com/jobs/occupational-therapist-per-diem-777001-pasadena-ca-118609535827968086) |
| Finance Associate | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/5/dd/9cba4cb51b5b7fdc0e3594022e5ce.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Varnum LLP | [View](https://www.openjobs-ai.com/jobs/finance-associate-michigan-united-states-118609535827968087) |
| Engineering Associate II | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/2/23/98893dc4672420c800c779c33c344.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Mesa Associates, Inc | [View](https://www.openjobs-ai.com/jobs/engineering-associate-ii-knoxville-tn-118609535827968088) |
| Data Engineer (Fabric, PySpark, Salesforce) - 100% Remote | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/7/c8/1e6b737a4c709e611a7eeb71db08d.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Conexess Group | [View](https://www.openjobs-ai.com/jobs/data-engineer-fabric-pyspark-salesforce-100-remote-norfolk-va-118609535827968089) |
| Presentations/ Audio Visual Lead | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/1/12/7fcb4703bfcf78da7d5be0055dfbd.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> UICGS / Bowhead Family of Companies | [View](https://www.openjobs-ai.com/jobs/presentations-audio-visual-lead-orlando-fl-118609535827968090) |
| Founding Recruiter – Technical Recruiting | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/e/24/f5c322edb984bd84c488b9c8ee8cf.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> interface.ai | [View](https://www.openjobs-ai.com/jobs/founding-recruiter-technical-recruiting-palo-alto-ca-118609535827968091) |
| Electro Mechanical Technician | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/c8/3c74e90ca9ecf5b483949c617504f.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Apex Systems | [View](https://www.openjobs-ai.com/jobs/electro-mechanical-technician-vista-ca-118609535827968092) |
| Sr. Network Engineer | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/c8/3c74e90ca9ecf5b483949c617504f.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Apex Systems | [View](https://www.openjobs-ai.com/jobs/sr-network-engineer-anaheim-ca-118609535827968093) |
| Project Management - Project Manager IV | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/c8/3c74e90ca9ecf5b483949c617504f.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Apex Systems | [View](https://www.openjobs-ai.com/jobs/project-management-project-manager-iv-california-united-states-118609535827968094) |
| Electronic Technician | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/a/78/a2e11769c45cc6097b2c920fc5a47.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Global Edge Group | [View](https://www.openjobs-ai.com/jobs/electronic-technician-santa-clarita-ca-118609535827968095) |
| Mergers and Acquisitions Director | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/d/2e/52c85857953cd65b30ae81ac44d27.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Attolon Partners | [View](https://www.openjobs-ai.com/jobs/mergers-and-acquisitions-director-greater-philadelphia-118609535827968096) |
| PATIENT ACCESS SERVICE REP, FCP - WEST BEND PATIENT CARE GENERAL | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/a/a8/801a66d90cf3c432cd6cb347a6c6b.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Froedtert Health | [View](https://www.openjobs-ai.com/jobs/patient-access-service-rep-fcp-west-bend-patient-care-general-west-bend-wi-118609535827968098) |
| STAFF RN AMBULATORY CLINIC LEAD, NEUROSCIENCES CLINIC | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/a/a8/801a66d90cf3c432cd6cb347a6c6b.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Froedtert Health | [View](https://www.openjobs-ai.com/jobs/staff-rn-ambulatory-clinic-lead-neurosciences-clinic-milwaukee-wi-118609535827968099) |
| Case Stacker | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/d/ea/4317713f637c77775943484ca73b7.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> HP Hood LLC | [View](https://www.openjobs-ai.com/jobs/case-stacker-portland-me-118609535827968100) |
| Personal Care Aide - Lake of the Woods | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/c/e3/0aef1e0adce8f087bfa8f644c36c7.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Americare Plus | [View](https://www.openjobs-ai.com/jobs/personal-care-aide-lake-of-the-woods-lake-of-the-woods-va-118609535827968101) |
| Personal Care Aide - Lawrenceville | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/c/e3/0aef1e0adce8f087bfa8f644c36c7.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Americare Plus | [View](https://www.openjobs-ai.com/jobs/personal-care-aide-lawrenceville-lawrenceville-va-118609535827968102) |
| Tax Analyst( Sales and Use) | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/d/37/7beebcc6b1262cd986e3a17e0f331.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Beacon Hill | [View](https://www.openjobs-ai.com/jobs/tax-analyst-sales-and-use-dallas-tx-118609535827968103) |
| Test Engineer L3 | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/c/1c/f502a9441c48e7ee98f32d1d64413.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Wipro | [View](https://www.openjobs-ai.com/jobs/test-engineer-l3-charlotte-nc-118609535827968104) |
| Associate Director, Field Marketing - Georgia | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/d/a3/58123c652f9259ee87d1dcf956096.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> BioSpace | [View](https://www.openjobs-ai.com/jobs/associate-director-field-marketing-georgia-united-states-118609535827968105) |
| Administrative Assistant | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/b/fa/761c7e317e01cdb48c582f1a58e70.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Suna Solutions | [View](https://www.openjobs-ai.com/jobs/administrative-assistant-san-diego-ca-118609535827968106) |
| District Support Pharmacist - FT | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/7/e1/f4357a9bf0f3643b7bb5652854889.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> CVS Health | [View](https://www.openjobs-ai.com/jobs/district-support-pharmacist-ft-gainesville-ga-118609535827968107) |
| Shift Supervisor | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/7/e1/f4357a9bf0f3643b7bb5652854889.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> CVS Health | [View](https://www.openjobs-ai.com/jobs/shift-supervisor-amarillo-tx-118609535827968108) |
| Pharmacy Technician | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/7/e1/f4357a9bf0f3643b7bb5652854889.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> CVS Health | [View](https://www.openjobs-ai.com/jobs/pharmacy-technician-forked-river-nj-118609535827968109) |
| Awake Overnight Direct Support Professinal Floater | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/9/d2/b2f3d61b71f5e2dc8df69b2dc387e.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Warren, Washington, Albany Counties ARC | [View](https://www.openjobs-ai.com/jobs/awake-overnight-direct-support-professinal-floater-hudson-falls-ny-118609535827968110) |
| Certified Nurse Assistant (CNA) | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/0/35/422a1c7cca94ac69bef69ec440724.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Affirmed Home Care | [View](https://www.openjobs-ai.com/jobs/certified-nurse-assistant-cna-new-haven-ct-118609535827968111) |
| Child Care Program Leader | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/1/ff/c2d0ccefb76910dea73c3c5be728c.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Saint Paul Public Schools | [View](https://www.openjobs-ai.com/jobs/child-care-program-leader-st-paul-mn-118609535827968112) |
| MEAT/ASST DEPT LEADER | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/0/28/c42add1f96f9e2717cfc8ce23c30d.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Kroger Mountain View Foods | [View](https://www.openjobs-ai.com/jobs/meatasst-dept-leader-westminster-co-118609535827968113) |
| Manheim Mobile Inspector II, Columbus West, OH | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/6/ab/7f1a8565540900a18e2f1937139a1.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Cox Automotive Inc. | [View](https://www.openjobs-ai.com/jobs/manheim-mobile-inspector-ii-columbus-west-oh-ohio-oh-118609535827968114) |
| Registered Dietitian RD/N Remote/Hybrid Options | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/2/c2/99b234323b193748365c03fcda1af.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> NutraCo | [View](https://www.openjobs-ai.com/jobs/registered-dietitian-rdn-remotehybrid-options-troy-hills-nj-118609535827968115) |
| Quality Manager | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/5/62/f9cb7b503478644afb2996eca91a3.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Berlin Packaging | [View](https://www.openjobs-ai.com/jobs/quality-manager-dallas-tx-118609535827968116) |
| Sr Project Leader | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/9/07/2a51c9ef2f0f92120b133f4315c74.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Milwaukee Tool | [View](https://www.openjobs-ai.com/jobs/sr-project-leader-milwaukee-wi-118609535827968117) |
| Senior Product Manager, Consumer Experience | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/8/08/63d38f7fb36d7c02de80ce24563bd.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Dorsia | [View](https://www.openjobs-ai.com/jobs/senior-product-manager-consumer-experience-new-york-ny-118609535827968118) |
| Community Liaison | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/c/8b/ba2e6b5edc2bc819be178bfc6d6bf.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Lifespark | [View](https://www.openjobs-ai.com/jobs/community-liaison-st-louis-park-mn-118609535827968119) |
| Production Site Manager | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/5/7e/914475af143593266ac60f8f5f6cb.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Gilat Stellar Blu | [View](https://www.openjobs-ai.com/jobs/production-site-manager-fort-worth-tx-118609535827968120) |
| Warehouse Specialist 2025-02402 | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/5/23/4de18ed96403736af5dbb1bfba8f8.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Wyoming Life Resource Center | [View](https://www.openjobs-ai.com/jobs/warehouse-specialist-2025-02402-lander-wy-118609535827968121) |
| RN McComb | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/e/b0/d735a757ab16f617aea6f9c7be720.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Pine Belt Mental Healthcare Resources | [View](https://www.openjobs-ai.com/jobs/rn-mccomb-mccomb-ms-118609535827968122) |
| Family Service Coordinator- Anthony | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/8/1a/bad8825dda6424c77fbe062861be4.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Tresco Inc | [View](https://www.openjobs-ai.com/jobs/family-service-coordinator-anthony-anthony-nm-118609535827968123) |
| Medical Assistant - Infectious Disease Clinic | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/d/5a/c99e193873cd941885f9c9f0bb78e.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Munson Healthcare | [View](https://www.openjobs-ai.com/jobs/medical-assistant-infectious-disease-clinic-traverse-city-mi-118609535827968124) |
| Senior Interior Designer - Luxury Residential | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/81/4556bb180bba0f23344fd4fd02ccf.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> True Consulting Ltd | [View](https://www.openjobs-ai.com/jobs/senior-interior-designer-luxury-residential-new-york-city-metropolitan-area-118609535827968125) |
| INDUSTRIAL ENGINEER 4 (CONTINUOUS IMPROVEMENT) | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/9/93/c9904b5532fd8bc32e6dddb65d2f2.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> HII | [View](https://www.openjobs-ai.com/jobs/industrial-engineer-4-continuous-improvement-newport-news-va-118609535827968126) |
| IT Security Architecture and Engineering | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/a/d0/288c3e163f271776b1ec970e19180.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Mega Cloud Lab | [View](https://www.openjobs-ai.com/jobs/it-security-architecture-and-engineering-new-york-ny-118609535827968127) |
| Rehabilitation Counselor - Ames | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/2/19/04e295dc8eda40f18404cb786eafb.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> State of Iowa | [View](https://www.openjobs-ai.com/jobs/rehabilitation-counselor-ames-ames-ia-118609535827968128) |
| Chef Manager | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/6/ee/eda20575184f7104a6fa07219f829.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> A Hiring Company | [View](https://www.openjobs-ai.com/jobs/chef-manager-greater-minneapolis-st-paul-area-118609535827968129) |
| Account Manager, Personal Lines | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/3/5d/65e2ab5581dbb79bd7b703740e45c.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Gallagher | [View](https://www.openjobs-ai.com/jobs/account-manager-personal-lines-faribault-mn-118609535827968130) |
| Attorney, Interstate Child Support Unit | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/8/57/0bdd05aabd4a3d4972ed6a1409a49.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> City of New York | [View](https://www.openjobs-ai.com/jobs/attorney-interstate-child-support-unit-new-york-ny-118609535827968131) |
| Litigation Associate | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/7/d9/c401532cf6a3c0c7c2a43c4a0a7ea.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Saltu Legal | [View](https://www.openjobs-ai.com/jobs/litigation-associate-chicago-il-118609535827968132) |
| Mechanical Design Engineer | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/c/08/511e35b2366f6089ea8acbd741d8b.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Applied Engineering, Inc. | [View](https://www.openjobs-ai.com/jobs/mechanical-design-engineer-burnsville-mn-118609535827968133) |
| Senior District Sales Associate | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/a/dc/ed7d426d0e80417065414632d6573.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Faria Education Group | [View](https://www.openjobs-ai.com/jobs/senior-district-sales-associate-philadelphia-pa-118609535827968134) |
| Pharmacist | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/6/2e/8943ac14e0fcaa78b967120320ec3.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Northside Hospital | [View](https://www.openjobs-ai.com/jobs/pharmacist-cumming-ga-118609753931776000) |
| Patient Care Tech PRN Plan 2 | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/1/56/20740459e04568d432d45eae918c1.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Sarasota Memorial Health Care System | [View](https://www.openjobs-ai.com/jobs/patient-care-tech-prn-plan-2-venice-fl-118609753931776001) |
| Logic Pro Software Tutor | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/96/01490799486dac16a48801deb8255.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Varsity Tutors, a Nerdy Company | [View](https://www.openjobs-ai.com/jobs/logic-pro-software-tutor-las-vegas-nv-118609753931776002) |
| Sterile Processing Tech III | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/c/8f/9e4fbc2f51247fb024880e7bb55c1.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Boston Children's Hospital | [View](https://www.openjobs-ai.com/jobs/sterile-processing-tech-iii-boston-ma-118609753931776003) |
| Assistant Coordinating Manager, Specialty Access Improvement Team (SAIT) | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/b/70/5c7fc88b3fd47a518b588fe832649.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> NYC Health + Hospitals | [View](https://www.openjobs-ai.com/jobs/assistant-coordinating-manager-specialty-access-improvement-team-sait-brooklyn-ny-118609753931776004) |
| Academic Clinician Assistant Professor | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/8/a0/b7b8294e678b7a6abe1f8dc30f73e.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Inside Higher Ed | [View](https://www.openjobs-ai.com/jobs/academic-clinician-assistant-professor-philadelphia-pa-118609753931776005) |
| Product Manager | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/2/8c/c693e7df3b7e40f97cb7da20d27b2.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Best Egg | [View](https://www.openjobs-ai.com/jobs/product-manager-united-states-118609753931776006) |
| Director of Construction, Telecom Construction | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/0/23/3daba4e4295d3294d37a2d6312f3f.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> TAK Broadband | [View](https://www.openjobs-ai.com/jobs/director-of-construction-telecom-construction-dallas-tx-118609753931776007) |
| Respiratory Therapist - Adults | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/1/f2/fb1bef9997b2c240769cfe6e1e05d.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Carilion Clinic | [View](https://www.openjobs-ai.com/jobs/respiratory-therapist-adults-roanoke-va-118609753931776008) |
| Solar Sales Representative | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/1/bf/f1d2ede9bc83ee8937828fd3803f1.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Sunrun | [View](https://www.openjobs-ai.com/jobs/solar-sales-representative-corona-ca-118609753931776009) |
| Nurse Practitioner- Nephrology-Temple | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/a8/fb3ab37959f0901daeba3ad01a372.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Baylor Scott & White Health | [View](https://www.openjobs-ai.com/jobs/nurse-practitioner-nephrology-temple-temple-tx-118609753931776010) |
| Direct Support Professional | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/b/cc/ca52bce9acdc7a17495369e4c4b29.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Merakey | [View](https://www.openjobs-ai.com/jobs/direct-support-professional-aliquippa-pa-118609753931776011) |
| Reporting & Analytics Director - Health Economics Value-Based Enablement | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/1/19/e64be56971e98b5c4314eeebe1eb5.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Elevance Health | [View](https://www.openjobs-ai.com/jobs/reporting-analytics-director-health-economics-value-based-enablement-new-york-ny-118609753931776012) |
| The Lifecare Institute - Clinical Grief Counselor | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/0/89/c94569f87c461b2292ca1e868354f.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Luminis Health | [View](https://www.openjobs-ai.com/jobs/the-lifecare-institute-clinical-grief-counselor-annapolis-md-118609753931776014) |
| Seasonal Tax Preparer - Personal and Business Taxes | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/5/1f/214b8b42f7b4a04304f305ff841ed.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> CyberCoders | [View](https://www.openjobs-ai.com/jobs/seasonal-tax-preparer-personal-and-business-taxes-mckinney-tx-118609753931776015) |
| M&A Human Capital Diligence Manager | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/3/39/954f26fc843dc265a62e9669e09d3.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Deloitte | [View](https://www.openjobs-ai.com/jobs/ma-human-capital-diligence-manager-new-york-ny-118609753931776016) |
| Tax Senior - State Income & Franchise, Multistate | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/3/39/954f26fc843dc265a62e9669e09d3.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Deloitte | [View](https://www.openjobs-ai.com/jobs/tax-senior-state-income-franchise-multistate-morristown-nj-118609753931776017) |
| Charles River Developer/Tester – Capital Markets | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/0/d4/4849ea6317dd2fd5dd7605ca5212e.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Matlen Silver | [View](https://www.openjobs-ai.com/jobs/charles-river-developertester-capital-markets-charlotte-nc-118609753931776018) |
| Occupational Therapist | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/1/53/859dcf9018985520f9521d6967453.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Thom Child and Family Services | [View](https://www.openjobs-ai.com/jobs/occupational-therapist-west-newbury-ma-118609753931776019) |
| Registered Nurse - Atrium Health Morehead Medical Plaza Call Center FT | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/8/07/0d7c1e68b222f536fa6e7efdf7f69.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Atrium Health | [View](https://www.openjobs-ai.com/jobs/registered-nurse-atrium-health-morehead-medical-plaza-call-center-ft-charlotte-nc-118609753931776020) |
| Outpatient Registered Nurse - RN | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/e/0d/cd8797fca6888b7f7f26d25e6624d.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Fresenius Medical Care | [View](https://www.openjobs-ai.com/jobs/outpatient-registered-nurse-rn-three-rivers-mi-118609753931776021) |
| Principal AI Engineer | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/5/f5/32a3fc4f1ea403f37070f59a7a53a.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Microsoft | [View](https://www.openjobs-ai.com/jobs/principal-ai-engineer-redmond-wa-118609753931776022) |
| Radiological Technologist-Radiology Diagnostic-Full Time- Evening-Mount Sinai Queens | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/2/2a/550ee1bbc94881de7150bed2d4044.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Mount Sinai Morningside | [View](https://www.openjobs-ai.com/jobs/radiological-technologist-radiology-diagnostic-full-time-evening-mount-sinai-queens-new-york-ny-118609753931776023) |
| Lecturer | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/8/a0/b7b8294e678b7a6abe1f8dc30f73e.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Information and Cybersecurity | [View](https://www.openjobs-ai.com/jobs/lecturer-information-and-cybersecurity-school-of-information-berkeley-ca-118609753931776024) |
| Theatre Production Assistant | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/8/a0/b7b8294e678b7a6abe1f8dc30f73e.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Back House | [View](https://www.openjobs-ai.com/jobs/theatre-production-assistant-back-house-71117-cottleville-mo-118609753931776025) |
| Post Doctoral Fellow / Post Msw Fellow:  College Counseling | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/8/a0/b7b8294e678b7a6abe1f8dc30f73e.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Inside Higher Ed | [View](https://www.openjobs-ai.com/jobs/post-doctoral-fellow-post-msw-fellow-college-counseling-poughkeepsie-ny-118609753931776026) |
| Part-time Faculty Pool: Art | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/8/a0/b7b8294e678b7a6abe1f8dc30f73e.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Inside Higher Ed | [View](https://www.openjobs-ai.com/jobs/part-time-faculty-pool-art-merced-ca-118609753931776027) |
| Staff Nurse- Operating Room- The James | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/8/a0/b7b8294e678b7a6abe1f8dc30f73e.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Inside Higher Ed | [View](https://www.openjobs-ai.com/jobs/staff-nurse-operating-room-the-james-columbus-oh-118609753931776028) |
| Graduate Student Disability Specialist 4 (4557C), Disabled Students Program - 82780 | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/8/a0/b7b8294e678b7a6abe1f8dc30f73e.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Inside Higher Ed | [View](https://www.openjobs-ai.com/jobs/graduate-student-disability-specialist-4-4557c-disabled-students-program-82780-berkeley-ca-118609753931776029) |
| Part Time Nursing Faculty | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/8/a0/b7b8294e678b7a6abe1f8dc30f73e.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Inside Higher Ed | [View](https://www.openjobs-ai.com/jobs/part-time-nursing-faculty-alpine-tx-118609753931776030) |
| Temporary Sales Assistant | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/8/a0/b7b8294e678b7a6abe1f8dc30f73e.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Inside Higher Ed | [View](https://www.openjobs-ai.com/jobs/temporary-sales-assistant-columbus-oh-118609753931776031) |
| Prelicensure Nursing Faculty - Maternity | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/8/a0/b7b8294e678b7a6abe1f8dc30f73e.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Inside Higher Ed | [View](https://www.openjobs-ai.com/jobs/prelicensure-nursing-faculty-maternity-boston-ma-118609753931776032) |
| Microbiology Technologist - University Hospital \| Microbiology Lab | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/8/a0/b7b8294e678b7a6abe1f8dc30f73e.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Inside Higher Ed | [View](https://www.openjobs-ai.com/jobs/microbiology-technologist-university-hospital-microbiology-lab-columbus-oh-118609753931776033) |
| Temporary North Gate Gift Shop Attendant | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/8/a0/b7b8294e678b7a6abe1f8dc30f73e.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Inside Higher Ed | [View](https://www.openjobs-ai.com/jobs/temporary-north-gate-gift-shop-attendant-marquette-mi-118609753931776034) |
| Administrative Assistant (Part -time) - Staff Pool | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/8/a0/b7b8294e678b7a6abe1f8dc30f73e.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Inside Higher Ed | [View](https://www.openjobs-ai.com/jobs/administrative-assistant-part-time-staff-pool-houston-tx-118609753931776035) |
| Bookkeeper | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/a/04/e341b3160d4a365ebfa980e7fc91a.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Robert Half | [View](https://www.openjobs-ai.com/jobs/bookkeeper-new-orleans-la-118609753931776036) |
| Substitute Teacher | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/9/88/c2c55fa1389d9ec264d78d42c2020.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Acquire4Hire | [View](https://www.openjobs-ai.com/jobs/substitute-teacher-menomonee-falls-wi-118609753931776037) |
| Senior Account Manager | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/b/0c/6375bea0f88518a9666eab7c175c1.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Burckhardt Compression | [View](https://www.openjobs-ai.com/jobs/senior-account-manager-greater-houston-118609753931776038) |
| Program Manager (Adult Day Program) | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/5/aa/ff0e56745a9afeec3f6b0c8f544a4.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Croyle-Nielsen Therapeutic Associates, Inc. | [View](https://www.openjobs-ai.com/jobs/program-manager-adult-day-program-somerset-pa-118609753931776039) |
| Right of Way Real Estate Associate | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/7/d0/42466aea1d9cab2748ecee97f5f8f.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Minnesota Department of Transportation | [View](https://www.openjobs-ai.com/jobs/right-of-way-real-estate-associate-roseville-mn-118609753931776040) |
| Tech Lead of Instrument Integration, Engineering - Lab Automation | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/7/e1/2faee40b7e0caaab80f6b3157aea7.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Genentech | [View](https://www.openjobs-ai.com/jobs/tech-lead-of-instrument-integration-engineering-lab-automation-south-san-francisco-ca-118609753931776041) |
| Administrative Coordinator | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/1/f2/fb1bef9997b2c240769cfe6e1e05d.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Care Management | [View](https://www.openjobs-ai.com/jobs/administrative-coordinator-care-management-regular-part-time-roanoke-va-118609753931776042) |
| Retail Sales Consultant | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/1/80/55136b6dd96acb5caf92338dcf498.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Part Time | [View](https://www.openjobs-ai.com/jobs/retail-sales-consultant-part-time-orlando-premium-outlets-orlando-fl-orlando-fl-118609753931776043) |
| Medical Laboratory Scientist II | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/a8/fb3ab37959f0901daeba3ad01a372.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Baylor Scott & White Health | [View](https://www.openjobs-ai.com/jobs/medical-laboratory-scientist-ii-fort-worth-tx-118609753931776044) |
| Associate Director — Global Voice Services Architect | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/d/a3/58123c652f9259ee87d1dcf956096.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> BioSpace | [View](https://www.openjobs-ai.com/jobs/associate-director-global-voice-services-architect-indianapolis-in-118609753931776045) |
| Assistant Store Manager | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/9/94/672943fefbfc46776024917dd842c.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Community Choice Financial Family of Brands | [View](https://www.openjobs-ai.com/jobs/assistant-store-manager-weatherford-tx-118609753931776046) |
| Account Director | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/7/f9/a046ba6fa01224db88cbda5bf4456.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> PPK | [View](https://www.openjobs-ai.com/jobs/account-director-tampa-fl-118609753931776047) |
| Principal Medical Writer | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/2/57/21f9d462f245851c3248ac1df01aa.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Submission Docs (2.5/2.7.2/2.7.3/2.7.4) | [View](https://www.openjobs-ai.com/jobs/principal-medical-writer-submission-docs-25272273274-oncology-remote-based-united-states-118609980424192000) |
| Senior Software Engineer, Windows/Desktop Applications - Lakewood, USA | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/3/69/b0c6c8ecd43300e6a4c7b4cde58a0.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Speechify | [View](https://www.openjobs-ai.com/jobs/senior-software-engineer-windowsdesktop-applications-lakewood-usa-lakewood-wa-118609980424192001) |
| Metrologist | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/4/fd/ee5c4d4262c348dd89c7d337f087b.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Technical Transfer | [View](https://www.openjobs-ai.com/jobs/metrologist-technical-transfer-medical-devices-0579-taunton-ma-taunton-ma-118609980424192002) |
| Rad Tech | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/1/f2/fb1bef9997b2c240769cfe6e1e05d.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Outpatient | [View](https://www.openjobs-ai.com/jobs/rad-tech-outpatient-salem-velocity-care-salem-va-118609980424192003) |
| Paramedic | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/f7/0944ec972c8256b7c410258c18eb2.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Premise Health | [View](https://www.openjobs-ai.com/jobs/paramedic-maryville-tn-118609980424192004) |
| Direct Support Professional | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/4/4e/67b9271758edace29205a88209e73.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Addus HomeCare | [View](https://www.openjobs-ai.com/jobs/direct-support-professional-tennessee-united-states-118609980424192005) |
| FLORAL/CLERK | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/0/28/c42add1f96f9e2717cfc8ce23c30d.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Kroger Mountain View Foods | [View](https://www.openjobs-ai.com/jobs/floralclerk-oak-creek-wi-118609980424192006) |
| Solar Technician | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/4/bb/56579f78bee67477309649f5183fa.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Apex Clean Energy | [View](https://www.openjobs-ai.com/jobs/solar-technician-coldwater-mi-118609980424192007) |
| QC Technician Part-time/Temp | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/9/a8/20cb1267a21bce241acf30f08d8e4.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Charm Sciences, Inc. | [View](https://www.openjobs-ai.com/jobs/qc-technician-part-timetemp-north-andover-ma-118609980424192008) |
| Media Planner | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/d5/d2bd715f1d55f5569a72c496f47c2.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> SINE Digital | [View](https://www.openjobs-ai.com/jobs/media-planner-new-york-united-states-118609980424192009) |
| Strategy & Analytics - Senior Manager (Customer Success) | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/a/8f/f6c9514c35c853b350382534fb624.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Salesforce | [View](https://www.openjobs-ai.com/jobs/strategy-analytics-senior-manager-customer-success-austin-tx-118609980424192010) |
| Lead Research Scientist, Foundation Models and Agentic Systems - Optum AI | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/d/7f/9a060f04bb5c68d1730930c2fe323.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Optum | [View](https://www.openjobs-ai.com/jobs/lead-research-scientist-foundation-models-and-agentic-systems-optum-ai-annapolis-md-118609980424192011) |
| CLERK RECEPTIONIST | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/2/4a/bb74028d722f1149047dc9788c0a0.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> CommonSpirit Health | [View](https://www.openjobs-ai.com/jobs/clerk-receptionist-santa-maria-ca-118610156584960000) |
| Stylist in Training / Apprentice Stylist | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/6/5a/7325633d5b9df8511e994c1a08f29.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Supercuts | [View](https://www.openjobs-ai.com/jobs/stylist-in-training-apprentice-stylist-johns-island-sc-118610156584960001) |
| CNA, Full-Time Nights, Rumford Community Home | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/1/98/d29029922d250ac1e054a04c3b08f.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Central Maine Healthcare | [View](https://www.openjobs-ai.com/jobs/cna-full-time-nights-rumford-community-home-rumford-me-118610156584960002) |
| Billing Specialist | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/0/71/c04f2bccc5afe9594608d7019f27c.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Elara Caring | [View](https://www.openjobs-ai.com/jobs/billing-specialist-san-antonio-tx-118610156584960003) |
| Manager, Performance Transformation (Insurance Sector Focus, Including MGAs) | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/4/aa/5fcf5b530b08bd251ba830e8e0892.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> KPMG US | [View](https://www.openjobs-ai.com/jobs/manager-performance-transformation-insurance-sector-focus-including-mgas-miami-fl-118610286608384000) |
| Account Executive - The Gottsacker Agency | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/b/1c/36a6bacfc9f72d44b9f65d32d401b.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Goosehead Insurance | [View](https://www.openjobs-ai.com/jobs/account-executive-the-gottsacker-agency-river-falls-wi-118610286608384001) |
| Project Manager | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/d/2b/91922e0b332b0a85b67682f9b4611.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Bounteous | [View](https://www.openjobs-ai.com/jobs/project-manager-atlanta-ga-118610286608384002) |
| Travel RN Dialysis Days Killeen TX | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/a/31/b21e61326ffe28cdfe762f0d9ca93.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Vibra Healthcare | [View](https://www.openjobs-ai.com/jobs/travel-rn-dialysis-days-killeen-tx-killeen-tx-118610555043840000) |
| Medical Assistant | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/3/f8/cac30b742d64b4ec837083f80ce7b.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Neurosurgery | [View](https://www.openjobs-ai.com/jobs/medical-assistant-neurosurgery-agh-full-time-travel-pittsburgh-pa-118609535827968040) |
| CNA / PRN / 12 HR Shifts / Weekly Pay $$$ | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/c/1e/247c067752a6509a068c9bf17e211.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Presbyterian Communities of South Carolina | [View](https://www.openjobs-ai.com/jobs/cna-prn-12-hr-shifts-weekly-pay--easley-sc-118609535827968041) |
| Cardiac Cath Technologist Sr / SEIU - E \| AGH | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/3/f8/cac30b742d64b4ec837083f80ce7b.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Allegheny Health Network | [View](https://www.openjobs-ai.com/jobs/cardiac-cath-technologist-sr-seiu-e-agh-pittsburgh-pa-118609535827968042) |
| RN - Acute Inpatient Rehab (Casual), Canonsburg | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/3/f8/cac30b742d64b4ec837083f80ce7b.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Allegheny Health Network | [View](https://www.openjobs-ai.com/jobs/rn-acute-inpatient-rehab-casual-canonsburg-canonsburg-pa-118609535827968043) |
| Registered Nurse - Night Shift 7P-7A (full-time) | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/2/35/9bbd0bdf962b74ee7b8bd7de6dfb2.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Tyler Holmes Memorial Hospital | [View](https://www.openjobs-ai.com/jobs/registered-nurse-night-shift-7p-7a-full-time-winona-ms-118609535827968044) |
| Agricultural Technician | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/1/db/268552563a5134027513f3b420994.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> LandPro Equipment, LLC | [View](https://www.openjobs-ai.com/jobs/agricultural-technician-clymer-ny-118609535827968045) |
| Behavioral Health Clinician | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/3/f8/cac30b742d64b4ec837083f80ce7b.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Pittsburgh | [View](https://www.openjobs-ai.com/jobs/behavioral-health-clinician-pittsburgh-full-time-pittsburgh-pa-118609535827968046) |
| CRNA | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/3/f8/cac30b742d64b4ec837083f80ce7b.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> AGH | [View](https://www.openjobs-ai.com/jobs/crna-agh-full-time-60000-sign-on-bonus-pittsburgh-pa-118609535827968047) |
| Senior Customer Success Manager | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/0/8f/345965b32b33af3da899eacfb147a.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Darrow AI | [View](https://www.openjobs-ai.com/jobs/senior-customer-success-manager-new-york-united-states-118609535827968048) |
| Outpatient Psychiatrist | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/3/f8/cac30b742d64b4ec837083f80ce7b.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Allegheny Health Network | [View](https://www.openjobs-ai.com/jobs/outpatient-psychiatrist-pittsburgh-pa-118609535827968049) |
| Pediatric Institute, Physician - Pediatric Gastroenterologist | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/3/f8/cac30b742d64b4ec837083f80ce7b.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Allegheny Health Network | [View](https://www.openjobs-ai.com/jobs/pediatric-institute-physician-pediatric-gastroenterologist-wexford-pa-118609535827968050) |
| CRNA | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/3/f8/cac30b742d64b4ec837083f80ce7b.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> West Penn Hospital | [View](https://www.openjobs-ai.com/jobs/crna-west-penn-hospital-full-time-pittsburgh-pa-118609535827968051) |
| Junior Data Scientist (TS/SCI) | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/5/7d/afd907f0e66aad0d27c9c23b53ad8.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Take2 Consulting, LLC | [View](https://www.openjobs-ai.com/jobs/junior-data-scientist-tssci-springfield-va-118609535827968052) |
| RN - MSFP (Full Time), St. Vincent | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/3/f8/cac30b742d64b4ec837083f80ce7b.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Allegheny Health Network | [View](https://www.openjobs-ai.com/jobs/rn-msfp-full-time-st-vincent-erie-pa-118609535827968053) |
| Patient Access Coordinator II | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/3/f8/cac30b742d64b4ec837083f80ce7b.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Radiation Oncology | [View](https://www.openjobs-ai.com/jobs/patient-access-coordinator-ii-radiation-oncology-ahn-cancer-institute-allegheny-general-hospital-pittsburgh-pa-118609535827968054) |
| RN 9A Oncology, Allegheny General | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/3/f8/cac30b742d64b4ec837083f80ce7b.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Allegheny Health Network | [View](https://www.openjobs-ai.com/jobs/rn-9a-oncology-allegheny-general-pittsburgh-pa-118609535827968055) |
| Travel Physical Therapy Assistant (PTA) - $1,599 to $1,926 per week in Albuquerque, NM | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/e/cf/b312bbfd6c4ed5cb55e4e772d40a3.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> AlliedTravelCareers | [View](https://www.openjobs-ai.com/jobs/travel-physical-therapy-assistant-pta-1599-to-1926-per-week-in-albuquerque-nm-albuquerque-nm-118609535827968056) |
| DIRECTOR OF BUDGET AND ANALYSIS | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/6/53/0bb3e672b2f7be0548f6cfb4c2509.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> NYC Department of Social Services | [View](https://www.openjobs-ai.com/jobs/director-of-budget-and-analysis-manhattan-ny-118609535827968057) |
| Senior Test Automation Engineer (Remote from California) | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/8/68/4bb6c6ea727adf6f221eda51fd9b0.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Jobgether | [View](https://www.openjobs-ai.com/jobs/senior-test-automation-engineer-remote-from-california-california-united-states-118609535827968058) |
| Recruteur, Bromont | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/e/75/7fd4fedc4fe825bb81b1b466a0947.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> IBM | [View](https://www.openjobs-ai.com/jobs/recruteur-bromont-california-united-states-118609535827968059) |
| Home Health: Licensed Practical Nurse (LPN) | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/3/80/d12c20e8d0a4aa470fc130847f6e8.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Mosaic Health | [View](https://www.openjobs-ai.com/jobs/home-health-licensed-practical-nurse-lpn-lehigh-acres-fl-118609535827968060) |
| LPN (Licensed Practical Nurse) | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/f/41/687e78669e7a24a8516528af966aa.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> American Senior Communities | [View](https://www.openjobs-ai.com/jobs/lpn-licensed-practical-nurse-noblesville-in-118609535827968061) |
| Territory Sales Manager | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/3/ed/174f8a6deec021a371d9ac6552f62.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> United Career Fairs | [View](https://www.openjobs-ai.com/jobs/territory-sales-manager-atlanta-metropolitan-area-118609535827968062) |
| Bilingual (Spanish/English) Overnight Youth Care Worker (11 p.m. - 7 a.m.) Casa Esperanza (Bartlett 60103) | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/6/cb/38b80cbf0294920deb3d8218d187a.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Maryville Academy | [View](https://www.openjobs-ai.com/jobs/bilingual-spanishenglish-overnight-youth-care-worker-11-pm-7-am-casa-esperanza-bartlett-60103-bartlett-il-118609535827968063) |
| Licensed Clinical Social Worker (LCSW) – Flexible Schedule | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/4/8d/e78c5c93b5e21e44cc06834cf1e1b.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> CHE Behavioral Health Services | [View](https://www.openjobs-ai.com/jobs/licensed-clinical-social-worker-lcsw-flexible-schedule-cranbury-nj-118609535827968064) |
| Installation Technician | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/6/5d/b43f237832cbf0f299bd8f2bcf2ac.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> AT&T | [View](https://www.openjobs-ai.com/jobs/installation-technician-bardstown-ky-118609535827968065) |
| Servicing Advisor | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/c/58/ac49dc87b4676ed7daccd60d857bf.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Cornerstone Wealth Associates | [View](https://www.openjobs-ai.com/jobs/servicing-advisor-morristown-nj-118609535827968066) |
| Non CDL Truck Driver | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/1/07/3cbe97c694e0f96549244a4bbeb27.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Unitex | [View](https://www.openjobs-ai.com/jobs/non-cdl-truck-driver-mount-vernon-ny-118609535827968067) |
| Medical Assistant | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/a/49/2b60daf1c665b10bb26c2652c7184.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Pyramid Healthcare | [View](https://www.openjobs-ai.com/jobs/medical-assistant-pittsburgh-pa-118609535827968068) |
| Data Collection Technician - Mandarin Language Specialist | <img src="https://images.weserv.nl/?url=https://front.openjobs-ai.com/data/company-logo/v3/5/b5/250d92dbf2e2880ed5c725fa07d94.png&w=24&h=24&q=80&output=webp" width="20" height="20" alt=""> Experis | [View](https://www.openjobs-ai.com/jobs/data-collection-technician-mandarin-language-specialist-redmond-wa-118609535827968069) |

<p align="center">
  <em>...and 0 more jobs</em>
</p>

<p align="center">
  <a href="https://www.openjobs-ai.com/deepsearch"><strong>Browse All Jobs →</strong></a>
</p>

---

<p align="center">
  Made with Python + GitHub Actions · Updated December 30, 2025
</p>
