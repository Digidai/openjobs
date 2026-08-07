# AI Recruiting Evaluation Library design

Date: 2026-08-07
Status: Approved by the user through selection of approach A

## Goal

Expand the OpenJobs Archive from a three-page field guide into a neutral, source-backed evaluation library for teams assessing AI recruiting systems. The library must be useful enough to earn citations on its own, while giving Metix AI a small number of relevant, visible, editorially disclosed links from substantive pages.

The work does not introduce `openjobs.metix.ai`, restore job listings, or remove either existing public root:

- `https://openjobs.genedai.me/`
- `https://digidai.github.io/openjobs/`

## Research finding

Current search results for AI recruiting evaluation are dominated by vendor-authored checklists. Many mix product recommendations, unexplained weights, and unsupported ROI claims into the evaluation method. The defensible gap is not another ranked vendor list. It is a reusable method that connects procurement questions to evidence, real-role tests, limitations, and accountable decisions.

The library will synthesize, without presenting itself as legal advice:

- NIST AI RMF and Playbook concepts for govern, map, measure, and manage;
- EEOC selection-procedure guidance and the Uniform Guidelines for job-related validity and impact evidence;
- ADA.gov guidance on disability, accommodations, and testing the skill rather than the disability;
- U.S. OPM material on job analysis and structured interviews;
- UK DSIT procurement and deployment guidance for responsible AI in recruitment;
- the UK ICO recruitment-tool audit findings on purpose limitation, data minimization, transparency, and monitoring;
- WCAG 2.2 as a web-accessibility reference rather than a universal employment-compliance proxy;
- current official NYC and EU materials as jurisdiction-specific examples with a last-checked date;
- first-party Metix engineering and product research, always labeled as first-party evidence.

## Selected information architecture

The six new canonical pages are:

1. `/methodology` — editorial independence, evidence levels, scoring rules, source taxonomy, corrections, and update cadence.
2. `/vendor-checklist` — a practical AI recruiting vendor evaluation checklist organized by purpose, evidence, workflow, data, candidate impact, integration, operations, and commercial fit.
3. `/pilot-design` — a real-role pilot protocol covering baseline selection, sampling, metrics, review labor, stop conditions, and scale criteria.
4. `/sourcing-evaluation` — evaluation of role interpretation, retrieval coverage, ranking, provenance, freshness, false positives, false negatives, and review-budget metrics.
5. `/screening-evaluation` — evaluation of job analysis, structured questions, scoring consistency, validity evidence, accessibility, accommodations, review, and contestability.
6. `/agent-reliability` — evaluation of tool permissions, trajectories, approvals, fallback, incident handling, repeatability, and performance drift.

The existing homepage becomes the hub for the library. The existing interactive scorecard remains the quick evaluation gate and gains links to deeper tests. The source ledger expands from eight entries into a cross-jurisdiction evidence register.

## Search-intent and content map

| Page | Primary intent | Primary query | Distinctive asset |
| --- | --- | --- | --- |
| Methodology | Informational / trust | AI recruiting evaluation methodology | Public evidence ladder and disclosure rules |
| Vendor checklist | Commercial investigation | AI recruiting vendor evaluation checklist | Downloadable question bank in CSV and JSON |
| Pilot design | Informational / commercial | AI recruiting pilot metrics | Baseline and pilot measurement template |
| Sourcing evaluation | Technical investigation | evaluate AI candidate sourcing | Retrieval and ranking metric definitions |
| Screening evaluation | Risk / procurement | evaluate AI candidate screening | Structured test and accommodation checklist |
| Agent reliability | Technical / governance | AI recruiting agent reliability | Failure-mode and monitoring register |

Each page answers its core question in the first 100 words, uses one H1, provides a short table of contents, includes visible source citations, and ends with a concise FAQ. FAQ structured data is emitted only when the same questions and answers are visible in HTML.

## Content model and generation

Add a dependency-free Python generator backed by structured content data. The content source will hold page metadata, sections, tables, questions, source references, related pages, and explicitly labeled Metix references. The generator will emit:

- six canonical HTML pages;
- six Markdown representations;
- vendor-question, pilot-metric, and evidence-register CSV downloads;
- structured JSON versions of the vendor questions and pilot metrics.

Generated files are committed so both Pages deployments remain buildless. A `--check` mode fails when committed output differs from the structured source. Existing hand-authored pages do not need to be migrated in this change.

The generator supports only the content structures this library needs: paragraphs, bullet lists, numbered procedures, comparison tables, evidence callouts, source lists, and visible FAQ blocks. It does not become a general-purpose CMS.

## Evidence and neutrality rules

Every factual claim must be one of:

- **Requirement** — a binding source for a named jurisdiction, with scope and verification date;
- **Regulator guidance** — official guidance whose legal force is stated accurately;
- **Voluntary framework** — a standard or framework that does not prove compliance;
- **Professional practice** — an assessment or accessibility practice with its intended scope;
- **Research finding** — a result tied to the reported dataset and method;
- **First-party claim** — a vendor or product statement that requires independent validation.

The pages do not rank vendors, award compliance badges, invent universal weights, or infer current product capabilities from research papers. Regulatory examples carry a `Last checked: 2026-08-07` label and a legal-advice disclaimer.

## Metix link strategy

The library is related to Metix AI and discloses that relationship. Neutrality comes from applying the same evidence rules to Metix, not from hiding the relationship.

- Remove the promotional `Explore Metix AI` button from global navigation.
- Keep one restrained branded disclosure link in the footer.
- Place one or two contextual Metix links in each page only where first-party research illustrates the evaluated concept.
- Prefer deep research URLs over repeated homepage links.
- Vary anchors naturally and label the material `first-party research` adjacent to the link.
- Include an `Evaluate Metix with the same framework` action only on the vendor checklist or scorecard, not on every page.
- Never use hidden links, keyword-stuffed anchors, reciprocal-link promises, generated vendor rankings, or unsupported endorsements.

This reduces the number of low-value sitewide links while increasing the editorial relevance of the links that remain. The expected benefit is stronger discovery and entity association plus the possibility of PageRank transfer if the library itself earns links; it is not a guarantee of ranking gains.

## Internal linking and discovery

- Every canonical page is linked from the homepage within one click.
- Every deep page links to the scorecard, source ledger, and two related library pages.
- Breadcrumbs use visible HTML and matching `BreadcrumbList` JSON-LD.
- `sitemap.xml`, `llms.txt`, `llms-full.txt`, and `ai-index.json` enumerate all canonical and machine-readable resources.
- Markdown and JSON copies remain readable cross-origin but carry `noindex, follow`; canonical HTML remains indexable.
- GitHub Pages continues to render the repository methodology, with descriptive links to every canonical guide on `openjobs.genedai.me`.

## Structured data

Each new page uses `Article` or `WebPage` according to its content, with accurate `headline`, description, dates, author, publisher, canonical URL, Markdown encoding, and topics. Visible FAQs may add `FAQPage` nodes. Breadcrumb nodes mirror visible breadcrumbs. No `Review`, `Product`, aggregate rating, or compliance schema is emitted.

The custom AI index advances to schema version 1.1 and adds:

- all nine canonical pages;
- source type, publisher, jurisdiction, publication or current-version date, last-checked date, supported use, and evidence limitation;
- downloadable assets and their media types;
- related Metix research explicitly marked as first-party.

## Design and accessibility

Reuse the existing typography, palette, semantic section patterns, responsive layout, print support, and reduced-motion behavior. Add compact styles for breadcrumbs, tables, definition lists, evidence labels, download panels, question groups, and FAQs. Native HTML controls and links remain keyboard accessible. Tables receive captions and horizontal overflow on narrow screens.

## Failure handling and validation

Validation fails closed when:

- a generated HTML, Markdown, CSV, or JSON artifact is stale;
- a canonical page is absent from the sitemap, AI index, or internal library navigation;
- titles, H1s, descriptions, or canonical URLs collide;
- a substantive page falls below the minimum content threshold;
- visible FAQ and FAQ JSON-LD diverge;
- a source lacks type, scope, URL, verification date, or evidence limitation;
- a Metix research link is not labeled first-party in the content source;
- a generated page contains retired job-board language or a disallowed hostname;
- machine-readable copies lose their MIME, CORS, or `noindex` policy.

Local verification includes generation checks, the existing validator, HTML validation, JSON Schema validation, a local Cloudflare Pages runtime, responsive screenshots of representative pages, and a link-status audit. Release verification keeps PR checks, Cloudflare preview, merge, Cloudflare production, GitHub Pages production, and live HTTP/content checks separate.

## Success criteria

- Nine canonical evaluation pages are indexable and mutually connected.
- Six new pages each contain substantive, non-duplicative evaluation guidance and primary citations.
- Downloadable checklist and pilot assets work without forms or tracking.
- Metix links are visible, contextual, canonical, dofollow by default, varied, and editorially disclosed.
- All human and machine-readable representations agree on scope, source type, and limitations.
- Both legacy public roots remain available, no job-listing runtime returns, and no `openjobs.metix.ai` hostname appears.
