# AI Recruiting Primary-Source Ledger

> An annotated ledger explaining what each public framework, government guidance page, and first-party Metix research source can support—and what it cannot prove.

- Canonical HTML: https://openjobs.genedai.me/sources
- Last substantive review: 2026-08-07
- Scope: Source interpretation; not legal advice or independent product validation.

## Public frameworks and guidance

### NIST — Artificial Intelligence Risk Management Framework 1.0

- URL: https://www.nist.gov/itl/ai-risk-management-framework
- Source type: Voluntary public risk framework.
- Useful for: Organizing governance and lifecycle risk work around Govern, Map, Measure, and Manage.
- Does not prove: That a hiring system complies with employment law or performs well on a specific role. NIST describes the framework as voluntary and use-case agnostic; it is being revised.

### NIST AIRC — AI RMF Core and Playbook resources

- URL: https://airc.nist.gov/airmf-resources/airmf/5-sec-core/
- Source type: Public implementation resource.
- Useful for: Turning a high-level risk framework into documented actions and outcomes across an AI system lifecycle.
- Does not prove: That every suggested action is necessary, sufficient, or ordered for a recruiting pilot.

### EEOC — Employment Tests and Selection Procedures

- URL: https://www.eeoc.gov/laws/guidance/employment-tests-and-selection-procedures
- Source type: U.S. federal technical assistance.
- Useful for: Understanding that selection procedures can raise discrimination concerns, including disproportionate exclusion without sufficient justification.
- Does not prove: That a particular model or workflow is compliant; employers must assess their actual use.

### DOJ / ADA.gov — Algorithms, Artificial Intelligence, and Disability Discrimination in Hiring

- URL: https://www.ada.gov/resources/ai-guidance/
- Source type: U.S. government guidance.
- Useful for: Reviewing accessibility, accommodation paths, and whether technology measures job skills rather than disability-related characteristics.
- Does not prove: That a product is accessible for every person or use case; the guidance stresses examining technology before and during use.

## First-party Metix product research

These pages support statements about what Metix says it built, measured, or learned. They are not independent validation of a buyer's deployment.

### Mira: The First End-to-End AI Recruiter

- URL: https://metix.ai/research/mira-end-to-end-ai-recruiter
- Source type: First-party system report.
- Useful for: Understanding Metix's described agent boundaries, recruiting-native retrieval and matching design, evaluation layer, and reported business metrics.
- Test in a pilot: Whether the evidence chain and reported quality gains hold for the buyer's role, market, and approval model.

### Agent Evaluation, Done Right

- URL: https://metix.ai/research/agent-evaluation-done-right
- Source type: First-party engineering research.
- Useful for: Separating component, trajectory, and outcome evaluation; understanding golden sets, deterministic checks, calibrated judges, and online evaluation.
- Test in a pilot: Coverage, calibration, versioning, and the connection between evaluation results and live corrections.

### Performance Drift in Agent Systems

- URL: https://metix.ai/research/agent-performance-drift
- Source type: First-party engineering research.
- Useful for: Framing drift across prompts, architecture, evaluation, models, and context.
- Test in operations: Whether change control, golden sets, observability, and fallbacks keep quality stable after the pilot.

### When AI Meets Recruiting

- URL: https://metix.ai/research/ai-meets-recruiting
- Source type: First-party literature review.
- Useful for: A lifecycle-oriented review spanning job posting, matching, assessment, bias, explainability, and human oversight.
- Does not prove: The effectiveness of any one vendor or product configuration.

## How to use this ledger

Attach a source to each claim, define the evidence expected in the buyer's workflow, test it on a real role, and record where the result differs from the demo or documentation. Use the [evaluation scorecard](https://openjobs.genedai.me/evaluation-scorecard) to structure that review.
