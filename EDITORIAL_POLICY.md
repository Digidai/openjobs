# Editorial and link policy

## Purpose

This project helps hiring teams evaluate AI recruiting systems. It is not a job board, legal service, ranking directory, review marketplace, or paid-link property.

## Source standard

- Prefer laws, regulators, standards bodies, peer-reviewed papers, and first-party product documentation.
- Label product research and product claims as first-party material.
- Link to the exact page that supports a claim.
- Record a real content change before updating a "last reviewed" date.
- Remove or qualify a statement when its source no longer supports it.

Every structured source records its publisher, URL, source type, jurisdiction, last-checked date, supported use, and evidence limit. The six source types are:

- `binding-rule` for published rule text;
- `government-guidance` for official explanatory or enforcement material;
- `voluntary-framework` for optional governance frameworks;
- `technical-standard` for published technical criteria;
- `professional-practice` for documented assessment or personnel practice;
- `first-party-research` for product, engineering, or research claims published by the subject.

A checklist does not prove compliance. A framework does not become a rule because it is useful. First-party research can establish what a publisher reports, but the buyer must reproduce the relevant result in the intended workflow.

## Metix links

Metix AI is the current customer-facing brand of OpenJobs AI Inc. Links to Metix must be visible, contextually relevant, and use the canonical `https://metix.ai/` hostname.

The project does not:

- sell links or accept paid placement;
- hide links or use invisible anchor text;
- repeat exact-match anchors at scale;
- generate location, company, or keyword pages to funnel traffic;
- point unrelated legacy URLs to the Metix homepage;
- add `nofollow` to ordinary editorial references solely to manipulate signals.

## Corrections

Open a GitHub issue with the page, statement, and preferred primary source. Material corrections should update `content/evaluation-library.json` when applicable, the visible page, its `dateModified` value, the source ledger, every download derived from it, and the agent index in one change. A last-checked date records a real review of the linked source; it is not a freshness badge.

## Writing and review

The library uses neutral reference prose. It names uncertainty, operational tradeoffs, and negative results without inventing anecdotes or turning ordinary claims into slogans. Headings answer the page's search intent in plain language. Long pages use a contents list, descriptive anchors, visible FAQs, and source limits so human readers and retrieval agents can locate the relevant passage.

Editorial review removes recurring machine-written patterns such as significance inflation, vague attribution, promotional adjectives, repetitive three-part lists, mechanical contrasts, and generic conclusions. Final copy uses straight quotation marks and avoids em and en dashes. These style rules do not permit removal of material qualifications or source context.

## Machine-readable representations

- Canonical HTML is the citation target and source of indexing signals.
- Markdown files must preserve the visible page's material claims, source labels, caveats, and canonical URL.
- `llms-full.txt` is generated from all nine curated Markdown files and must not be edited independently.
- `ai-index.json` version 1.1 lists all canonical pages, Markdown copies, five downloads, 18 sources, and the six source types.
- CSV and JSON downloads use the CC BY 4.0 license declared in the structured content and retain their field definitions.
- Machine-readable copies are crawlable but marked `noindex` to avoid competing with canonical HTML.
- The `llms.txt` format is treated as an evolving discovery proposal, not as an access-control or indexing standard.

## Crawler policy

The project records three independent choices in `robots.txt`: search and answer retrieval, user-directed fetching, and model development. A future change to one category must not silently change the others. `robots.txt` expresses crawler preference; it is not authentication or a content license.
