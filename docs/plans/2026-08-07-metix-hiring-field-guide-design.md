# Metix Hiring Field Guide redesign

Date: 2026-08-07

## Decision

Retire the OpenJobs job aggregator completely. Keep both existing public roots available:

- `https://openjobs.genedai.me/`
- `https://digidai.github.io/openjobs/`

Do not add an `openjobs.metix.ai` hostname. The Cloudflare surface becomes an editorial AI recruiting evaluation guide. The GitHub Pages surface becomes the open-source methodology and maintenance record for that guide, so the two domains do not publish duplicate primary content.

## Why this approach

Three approaches were considered:

1. Keep the job board and swap outbound URLs. Rejected because the user explicitly asked to retire this content type, and the existing list-page job schema and virtual filter URLs create avoidable search-quality risk.
2. Replace the board with a thin Metix landing page. Rejected because a page created mainly to funnel visitors would provide little independent value and could resemble doorway content.
3. Publish a useful, source-backed hiring evaluation field guide. Selected because it gives hiring teams a standalone decision tool while creating a small number of relevant, contextual links to Metix AI.

## Information architecture

The Cloudflare site contains three canonical pages:

- `/` — the editorial field guide: outcomes, evidence chain, human control, risk review, and pilot design.
- `/evaluation-scorecard` — an interactive and printable 24-point buyer scorecard.
- `/sources` — an annotated primary-source ledger covering NIST, EEOC, ADA guidance, and Metix research.

GitHub Pages renders `README.md` at `/openjobs/`. It documents the editorial method, source policy, link policy, deployments, and validation commands. Copies of files in `public/` that GitHub may expose retain canonical links to `openjobs.genedai.me`.

## Link policy

Metix links use clean canonical URLs with descriptive, varied anchors. The guide links only where Metix is directly relevant: the brand transition, product approach, research, pricing, contact, and opportunities. There are no hidden links, keyword-stuffed anchors, sitewide lists of repeated URLs, paid placements, or generated job pages.

## Technical changes

- Remove the job feed discovery and generation script.
- Remove scheduled content commits, job statistics, RSS, and job-specific assets.
- Replace the workflow with read-only site validation.
- Remove `JobPosting` schema from list pages.
- Submit only real canonical pages in each sitemap.
- Keep self-referencing canonicals for both public roots.
- Use semantic HTML, visible source citations, JSON-LD that matches page content, a print stylesheet, reduced-motion support, and no external JavaScript.

## Failure handling and tests

`scripts/validate_site.py` fails closed when required files are missing, a canonical is wrong, JSON-LD is invalid, local links are broken, retired job-board language returns, an old OpenJobs AI product URL is reintroduced, or a Metix job URL does not follow the canonical slug pattern. CI runs this validation on pull requests and relevant pushes.

Deployment verification must keep four gates separate: pushed commit, GitHub Pages workflow, Cloudflare Pages deployment, and live HTTP/content checks on both public roots.
