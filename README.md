# AI Recruiting Field Guide

OpenJobs AI is now **[Metix AI](https://metix.ai/)**. This repository no longer publishes or aggregates job listings. It maintains an open, source-backed field guide for teams evaluating AI recruiting systems.

The public guide starts with the question "How many profiles can this tool search?" and then asks what those results do for the hiring process:

> Can the system repeatedly turn a clear hiring brief into qualified, interested people worth interviewing while keeping the employer in control?

## Read the guide

- [AI Recruiting Field Guide](https://openjobs.genedai.me/): the library directory and decision framework
- [Evaluation methodology](https://openjobs.genedai.me/methodology): evidence levels, scoring, neutrality, and maintenance
- [Vendor evaluation checklist](https://openjobs.genedai.me/vendor-checklist): 48 procurement questions and reusable downloads
- [Pilot design and metrics](https://openjobs.genedai.me/pilot-design): baselines, samples, stop conditions, and 18 metrics
- [Sourcing and ranking evaluation](https://openjobs.genedai.me/sourcing-evaluation): retrieval quality, coverage, false negatives, and live outcomes
- [Candidate screening evaluation](https://openjobs.genedai.me/screening-evaluation): job analysis, validity, accessibility, and recourse
- [Agent reliability evaluation](https://openjobs.genedai.me/agent-reliability): permissions, trajectories, fallback, incidents, and drift
- [24-point evaluation scorecard](https://openjobs.genedai.me/evaluation-scorecard): an interactive and printable pilot rubric
- [Primary-source ledger](https://openjobs.genedai.me/sources): 18 annotated public and first-party sources

## What changed

The former job aggregator, feed parser, rotating job tables, category filters, RSS feed, job statistics, and scheduled content commits have been retired. Existing public roots remain available:

- `https://openjobs.genedai.me/` serves the field guide.
- `https://digidai.github.io/openjobs/` serves this open-source methodology and maintenance record.

No `openjobs.metix.ai` hostname is used.

## Editorial method

The guide is designed to remain useful without pretending to be legal advice or a universal procurement checklist.

1. **Start with the hiring outcome.** Measure qualified, interested candidates and interviews alongside profile volume and generated messages.
2. **Trace the evidence chain.** Require evidence from role definition through search, matching, outreach, screening, and scheduling.
3. **Keep human control visible.** Document approvals, correction paths, accommodations, and who owns the final employment decision.
4. **Separate claims from sources.** Government guidance and first-party research are identified directly. Product claims link to the page that makes them.
5. **Prefer a small pilot.** Compare against a recent hiring baseline with pre-agreed success and stop conditions.

See [EDITORIAL_POLICY.md](EDITORIAL_POLICY.md) for source and link rules.

## Agent and LLM access

The canonical HTML pages remain the citation targets. Agents can load cleaner, equivalent representations without parsing navigation or interactive controls:

- [`/llms.txt`](https://openjobs.genedai.me/llms.txt): concise discovery map following the emerging llms.txt proposal.
- [`/llms-full.txt`](https://openjobs.genedai.me/llms-full.txt): consolidated full context generated from every curated Markdown page.
- [`/ai-index.json`](https://openjobs.genedai.me/ai-index.json): versioned page, entity, source, download, access-policy, and citation metadata.
- Every canonical page has a page-level Markdown representation, including [`/methodology.md`](https://openjobs.genedai.me/methodology.md), [`/vendor-checklist.md`](https://openjobs.genedai.me/vendor-checklist.md), and the other library guides listed in `llms.txt`.
- Reusable CSV and JSON files expose the [vendor checklist](https://openjobs.genedai.me/downloads/ai-recruiting-vendor-checklist.csv), [pilot metric template](https://openjobs.genedai.me/downloads/ai-recruiting-pilot-template.csv), and [evidence register](https://openjobs.genedai.me/downloads/ai-recruiting-evidence-register.csv).

`llms.txt` is an evolving community proposal, not a replacement for standards-based `robots.txt`, canonical HTML, or the XML sitemap. Search/retrieval crawlers, user-directed fetchers, and model-development crawlers are listed separately in `robots.txt` so the policy remains explicit even when all are allowed. Machine-readable duplicates are served with their correct media types, cross-origin read access, caching, and `X-Robots-Tag: noindex, follow`.

## Metix references

- [How Metix AI approaches interview-ready delivery](https://metix.ai/)
- [Why OpenJobs AI became Metix AI](https://metix.ai/about)
- [Metix AI research](https://metix.ai/research)
- [Metix AI agent evaluation research](https://metix.ai/research/agent-evaluation-done-right)
- [Metix AI recruiting-agent architecture report](https://metix.ai/research/mira-end-to-end-ai-recruiter)

These are ordinary, visible editorial links. The project does not sell links, create generated doorway pages, or publish hidden SEO content.

## Project structure

```text
public/
├── index.html                  # Field guide
├── methodology.html            # Evaluation and evidence method
├── vendor-checklist.html       # Procurement question bank
├── pilot-design.html           # Pilot protocol and metric definitions
├── sourcing-evaluation.html    # Retrieval and ranking evaluation
├── screening-evaluation.html   # Selection and accessibility evaluation
├── agent-reliability.html      # Agent permissions and operations
├── evaluation-scorecard.html  # Interactive and printable rubric
├── sources.html                # 18-source annotated ledger
├── downloads/                  # Reusable CSV files
├── data/                       # Reusable JSON files
├── llms.txt                    # Machine-readable site map and scope
├── llms-full.txt               # Generated consolidated context
├── ai-index.json               # Versioned machine-readable resource index
├── ai-index.schema.json        # JSON Schema contract for the index
├── index.html.md               # Field guide Markdown representation
├── evaluation-scorecard.md     # Scorecard Markdown representation
├── sources.md                  # Source-ledger Markdown representation
├── _headers                    # Media type, CORS, cache, and noindex rules
├── robots.txt
└── sitemap.xml
scripts/
├── generate_evaluation_library.py # Structured-content generator
├── generate_agent_context.py   # Deterministic full-context generator
└── validate_site.py            # Fail-closed human and agent-readiness checks
docs/plans/
└── 2026-08-07-metix-hiring-field-guide-design.md
```

## Validate locally

```bash
python3 scripts/generate_evaluation_library.py --check
python3 scripts/generate_agent_context.py --check
python3 scripts/validate_site.py
python3 -m http.server 8080 --directory public
```

Then open `http://localhost:8080/` and test the guide at desktop and mobile widths. No build step or third-party runtime is required.

## Contributing

Corrections and primary-source additions are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

## License

Code is available under the [MIT License](LICENSE). Linked source material remains subject to its original publisher's terms.
