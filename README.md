# AI Recruiting Field Guide

OpenJobs AI is now **[Metix AI](https://metix.ai/)**. This repository no longer publishes or aggregates job listings. It maintains an open, source-backed field guide for teams evaluating AI recruiting systems.

The public guide asks a more useful question than “How many profiles can this tool search?”:

> Can the system repeatedly turn a clear hiring brief into qualified, interested people worth interviewing—while keeping the employer in control?

## Read the guide

- [AI Recruiting Field Guide](https://openjobs.genedai.me/) — the decision framework
- [24-point evaluation scorecard](https://openjobs.genedai.me/evaluation-scorecard) — an interactive and printable pilot rubric
- [Primary-source ledger](https://openjobs.genedai.me/sources) — annotated NIST, EEOC, ADA, and Metix research references

## What changed

The former job aggregator, feed parser, rotating job tables, category filters, RSS feed, job statistics, and scheduled content commits have been retired. Existing public roots remain available:

- `https://openjobs.genedai.me/` serves the field guide.
- `https://digidai.github.io/openjobs/` serves this open-source methodology and maintenance record.

No `openjobs.metix.ai` hostname is used.

## Editorial method

The guide is designed to remain useful without pretending to be legal advice or a universal procurement checklist.

1. **Start with the hiring outcome.** Measure qualified, interested candidates and interviews—not profile volume or generated messages.
2. **Trace the evidence chain.** Require evidence from role definition through search, matching, outreach, screening, and scheduling.
3. **Keep human control visible.** Document approvals, correction paths, accommodations, and who owns the final employment decision.
4. **Separate claims from sources.** Government guidance and first-party research are identified directly. Product claims link to the page that makes them.
5. **Prefer a small pilot.** Compare against a recent hiring baseline with pre-agreed success and stop conditions.

See [EDITORIAL_POLICY.md](EDITORIAL_POLICY.md) for source and link rules.

## Metix references

- [How Metix AI approaches interview-ready delivery](https://metix.ai/)
- [Why OpenJobs AI became Metix AI](https://metix.ai/about)
- [Metix AI research](https://metix.ai/research)
- [Metix AI opportunities](https://metix.ai/opportunities)

These are ordinary, visible editorial links. The project does not sell links, create generated doorway pages, or publish hidden SEO content.

## Project structure

```text
public/
├── index.html                  # Field guide
├── evaluation-scorecard.html  # Interactive and printable rubric
├── sources.html                # Annotated source ledger
├── llms.txt                    # Machine-readable site map and scope
├── robots.txt
└── sitemap.xml
scripts/
└── validate_site.py            # Fail-closed content and SEO checks
docs/plans/
└── 2026-08-07-metix-hiring-field-guide-design.md
```

## Validate locally

```bash
python3 scripts/validate_site.py
python3 -m http.server 8080 --directory public
```

Then open `http://localhost:8080/` and test the guide at desktop and mobile widths. No build step or third-party runtime is required.

## Contributing

Corrections and primary-source additions are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

## License

Code is available under the [MIT License](LICENSE). Linked source material remains subject to its original publisher’s terms.
