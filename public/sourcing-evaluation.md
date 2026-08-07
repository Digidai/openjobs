# How to Evaluate AI Candidate Sourcing and Ranking

Canonical HTML: https://openjobs.genedai.me/sourcing-evaluation
Last substantive review: 2026-08-07

> OpenJobs AI is now Metix AI. This archive applies the same evidence rules to Metix first-party material and independent sources.

AI candidate sourcing should be evaluated as a retrieval and ranking workflow, not by database size or a handful of impressive profiles. Test how the system interprets a role, covers the relevant population, ranks evidence within a fixed review budget, and learns from misses without hiding them.

## Contents

- [Turn the role into a testable retrieval task.](#retrieval-task)
- [Evaluate source provenance, coverage, refresh, and exclusions together.](#provenance-coverage)
- [Create a role-specific test set without treating one reviewer as ground truth.](#test-set)
- [Measure precision and coverage at the point a recruiter can actually review.](#retrieval-metrics)
- [Review false positives and false negatives as different product failures.](#error-analysis)
- [Connect retrieval quality to review, engagement, and interview acceptance.](#live-workflow)
- [Re-test when the role, population, source, or model changes.](#freshness-drift)
- [Approve a sourcing system for a defined role family and review budget.](#sourcing-decision)

## 1. Turn the role into a testable retrieval task.

Candidate relevance is conditional on a role brief and a decision. Before measuring a system, separate must-have evidence, acceptable alternatives, preferences, exclusions, seniority signals, location or work authorization constraints, compensation assumptions, and unknowns that require a conversation. Ask the hiring manager to approve this interpretation before seeing the ranked results.

Use job analysis rather than copying every sentence of a legacy description into a prompt. The OPM job-analysis material identifies tasks and competencies as foundations for assessment. In sourcing, the same discipline helps distinguish evidence that a person could perform the work from convenient proxies such as title, employer brand, school, or keyword overlap.

Define the retrieval unit. Is the system finding profiles, enriching known applicants, rediscovering people in an ATS, recommending similar candidates, or producing contactable and currently interested people? A profile can be relevant but stale, duplicate, unreachable, unavailable, or not interested. These later states should not be silently included in retrieval quality.

- **Must-have evidence.** What observable experience, work, skill, or qualification is necessary, and what alternative evidence is acceptable?
- **Trade-offs.** Which requirements can move together, and who approves that movement?
- **Unknowns.** Which questions cannot be answered reliably from available profile data?
- **Outcome.** Does success mean worth reviewing, worth contacting, interested, or accepted for interview?

## 2. Evaluate source provenance, coverage, refresh, and exclusions together.

Ask the provider to describe source categories, licensing or access basis, geographic and occupational coverage, refresh schedules, deletion and correction flows, deduplication, enrichment, and inferred fields. A headline profile count does not show how many records are current, searchable for the relevant role, or usable in the intended communication channel.

Coverage has both visible and invisible gaps. A source may underrepresent a country, sector, early-career population, independent work, non-English profile, or nontraditional path. A ranking model cannot retrieve people who are absent or fields the index does not preserve. Document these gaps before attributing every miss to model quality.

Separate source facts from vendor or model inference. Show dates and provenance for current employer, role, location, skills, contact data, and availability where available. If the system synthesizes a profile summary or inferred seniority, a reviewer should be able to return to the underlying evidence and correct the interpretation.

Table: Coverage questions that a database-size claim cannot answer

| Dimension | Evidence to request | Failure to look for |
| --- | --- | --- |
| Population | Role, geography, language, career stage, and source distribution. | Strong totals masking weak coverage for the evaluated role. |
| Freshness | Field-level dates, refresh method, and stale-record handling. | Current-looking summaries built from outdated employment data. |
| Provenance | Source category and distinction between observed and inferred fields. | Generated claims presented as profile facts. |
| Control | Correction, deletion, suppression, and customer export paths. | Records persisting or reappearing after correction. |
| Duplicates | Entity resolution method and review of merged or split profiles. | One person counted repeatedly or different people merged incorrectly. |

## 3. Create a role-specific test set without treating one reviewer as ground truth.

Build evaluation cases from the approved brief and the population the system will actually search. Include known qualified people where available, hard negatives with similar titles but wrong scope, adjacent backgrounds, unconventional evidence, missing fields, and disputed cases. Preserve why each person was labeled rather than only a binary judgment.

Have reviewers apply the same rubric independently before discussing material disagreement. The goal is not to erase human uncertainty; it is to distinguish model error from an ambiguous brief or inconsistent reviewer. Record consensus, disagreement, and insufficient-information states. Do not force every profile into qualified or unqualified when the available evidence cannot support that conclusion.

Avoid label leakage and showcase selection. If vendor staff know which people are considered qualified and tune the search to them, separate that development set from the final evaluation. A test based only on employees or previously hired candidates can reward historical patterns and omit qualified alternatives.

1. **Draft rubric.** Translate role requirements into observable evidence and acceptable alternatives.
2. **Sample cases.** Include positives, hard negatives, boundary cases, and insufficient-information cases.
3. **Label independently.** Collect reasons and confidence before reviewer discussion.
4. **Hold out evaluation.** Keep final cases separate from vendor tuning or query iteration.

## 4. Measure precision and coverage at the point a recruiter can actually review.

Ranking quality matters within a finite review budget. Precision@K asks what proportion of the top K reviewed people meets the frozen relevance standard. Recall@K asks what proportion of all labeled relevant people in the evaluated pool appears within the top K. When the full relevant population is unknowable, report a recall proxy and explain how the pool was constructed rather than calling it complete recall.

Measure more than one cutoff. A system may be precise in the first ten results but degrade quickly, or it may place qualified adjacent backgrounds just beyond the routine review limit. Rank-sensitive measures and the distribution of first relevant results can help, but plain-language case review remains necessary to understand why movement occurred.

Do not compare metrics across different pools, labels, roles, or retrieval stages as if they share a denominator. A reranker measured on candidates already returned by an upstream retriever cannot establish end-to-end coverage. A model judged by another model carries judge assumptions that should be tested against human review.

Table: Retrieval metrics and their interpretation limits

| Metric | Question answered | Does not answer |
| --- | --- | --- |
| Precision@K | How much of the reviewed top K meets the relevance standard? | How many relevant people were never retrieved or ranked lower. |
| Recall@K | How much of the labeled relevant pool appears in the top K? | Coverage outside the constructed and labeled pool. |
| Yield per reviewer hour | How many accepted profiles result from actual review labor? | Candidate interest, availability, or later interview quality. |
| Rank movement | Where do relevant and hard-negative cases move after reranking? | Whether the upstream pool is representative or complete. |
| Manager acceptance | Which profiles a manager advances under the current rubric? | Objective job performance or absence of manager bias. |

## 5. Review false positives and false negatives as different product failures.

A false positive consumes review or outreach capacity and may create poor candidate contact. A false negative removes opportunity before a conversation. Sample both. False negatives are harder to observe because the system does not present them, so use known qualified cases, lower-ranked samples, alternate queries, source comparisons, and hiring-manager nominations to search for misses.

Classify the failure location: brief parsing, title normalization, skill inference, seniority, geography, source absence, stale data, query generation, embedding, reranking, hard filter, deduplication, or human label disagreement. A single “bad match” bucket cannot guide remediation and encourages changing the entire model for a data or configuration problem.

Look for asymmetric failure patterns across role types, career paths, languages, and sources. A system can meet an average target while systematically losing nontraditional evidence or overvaluing famous employers. Do not claim demographic fairness without appropriate data and analysis, but do not ignore repeated qualitative patterns because a pilot lacks power for a formal estimate.

- **Unsupported leap.** The summary claims a requirement that the underlying profile does not evidence.
- **Boundary confusion.** Similar title or skill vocabulary hides a different function, scope, or level.
- **Missing alternative.** The system recognizes one conventional path but not another approved route to the competency.
- **Hard-filter loss.** A person never reaches semantic ranking because an upstream filter excludes them.
- **Stale relevance.** The historical match is plausible but no longer reflects current work or location.

## 6. Connect retrieval quality to review, engagement, and interview acceptance.

Offline metrics isolate retrieval and ranking, but the live workflow includes recruiter review, contactability, message approval, candidate reply, interest, screening, and hiring-manager acceptance. Keep those stages separate so weak engagement does not get mislabeled as poor retrieval and a broad message campaign does not inflate perceived candidate quality.

Track how explanations affect reviewers. If generated summaries make weak profiles appear persuasive, compare decisions with and without the summary or require evidence links. Measure reviewer correction and query iteration. A system that reaches quality only after extensive hidden prompt work may be useful, but its operating cost and repeatability differ from the initial claim.

Measure candidates delivered under a clear definition: relevant to the approved brief, current enough to evaluate, deduplicated, contact handled under the approved process, and at the interest state promised by the vendor. A list of profiles, a positive reply, and an accepted interview are distinct outcomes.

> **Outcome boundary — Do not call a profile a candidate outcome** Report retrieval quality, review acceptance, contact, interest, and interview acceptance as separate funnel states with their own denominators.

## 7. Re-test when the role, population, source, or model changes.

Sourcing systems operate on moving populations. People change jobs and locations; new evidence appears; source access changes; queries evolve; hiring managers learn; and models or rerankers update. Preserve evaluation cases and rerun them after material changes while also adding new roles so the system cannot optimize only to a static benchmark.

Monitor leading indicators such as accepted-profile rate at fixed review depth, reviewer overrides, unsupported inference, stale-record rate, duplicate rate, source distribution, and rank movement for known cases. Investigate before automatically attributing change to model drift: the brief, labelers, market, source coverage, or downstream filters may have shifted.

Version the complete retrieval path. Record upstream retriever, filters, query interpretation, embeddings, reranker, enrichment, explanation model, and configuration. A reported improvement in one component is not an end-to-end improvement until the deployed chain and real review budget show it.

1. **Keep a stable regression set.** Retain approved role cases and known failure modes across releases.
2. **Add fresh challenge cases.** Introduce new roles, terminology, locations, and career paths to test transfer.
3. **Compare the full chain.** Measure the production configuration, not an isolated replacement component.
4. **Investigate movement.** Attribute changes across role, data, source, model, configuration, and reviewer before acting.

## 8. Approve a sourcing system for a defined role family and review budget.

The sourcing decision should state the tested role families, geographies, languages, sources, review cutoff, required provenance, explanation behavior, acceptable stale and duplicate handling, human review, and monitoring. It should also state where the system is not approved, including screening or autonomous outreach if those functions were not tested.

Compare the system to a current workflow using accepted quality and reviewer labor, not only profile volume or search speed. A smaller, more inspectable pool may outperform a larger ranking if it reduces cleanup and unsupported inference. Conversely, high precision in the top ten may not satisfy a role that requires broader exploration or uncommon backgrounds.

Use the [vendor checklist](/vendor-checklist) for data and commercial questions and the [pilot design](/pilot-design) for a bounded live test. Preserve the failed cases as future regression tests rather than deleting them after a query fix.

> **Approval scope — Name the review budget** A sourcing result is only meaningful at the number of profiles the team can consistently inspect with the agreed evidence standard.

## Sources and evidence limits

- **Voluntary Framework: [NIST — Artificial Intelligence Risk Management Framework 1.0](https://www.nist.gov/itl/ai-risk-management-framework)**
  - Supports: A lifecycle structure for governing, mapping, measuring, and managing AI risk and trustworthiness characteristics.
  - Does not prove: Use of the voluntary framework does not establish legal compliance, product quality, or fitness for a particular hiring process.
- **Professional Practice: [U.S. Office of Personnel Management — Job Analysis](https://www.opm.gov/policy-data-oversight/assessment-and-selection/job-analysis/)**
  - Supports: A practical account of job analysis as the foundation for defining tasks, competencies, and assessment content.
  - Does not prove: Federal personnel practice does not by itself validate a private-sector role brief or every automated assessment.
- **Government Guidance: [UK Department for Science, Innovation and Technology — Responsible AI in Recruitment](https://www.gov.uk/government/publications/responsible-ai-in-recruitment-guide/responsible-ai-in-recruitment)**
  - Supports: Procurement and deployment questions covering purpose, governance, accessibility, assurance, testing, pilots, transparency, and monitoring.
  - Does not prove: The guide expressly does not provide legal assurance and its examples are not universal deployment instructions.
- **Government Guidance: [UK Information Commissioner's Office — AI Tools Used in Recruitment — Audit Outcomes](https://ico.org.uk/action-weve-taken/audits-and-overview-reports/2024/11/ai-tools-used-in-recruitment/)**
  - Supports: Observed privacy and information-rights issues in recruitment sourcing, screening, and selection tools, plus remediation themes.
  - Does not prove: Consensual audits of selected providers do not establish prevalence, legal status, or performance of another product.
- **First-party research: [Mira-Embeddings-V1: Domain-Adapted Semantic Reranking for Recruitment](https://metix.ai/research/mira-embeddings-v1)**
  - Context: The Metix paper reports Recall@K and Precision@K under stated local and global protocols, offering a first-party example of why pool, cutoff, labels, and reranking stage must stay visible.
  - Does not prove: The reported results are protocol-specific and do not independently establish end-to-end sourcing quality, live candidate outcomes, or fairness.

## Frequently asked questions

### Is database size a useful sourcing metric?

It describes potential inventory but not role-specific coverage, freshness, provenance, deduplication, rank quality, contactability, or candidate interest.

### What is the difference between precision and recall in candidate sourcing?

Precision asks how many reviewed results are relevant; recall asks how many relevant people in the evaluated pool were retrieved within the cutoff. Both depend on labels and pool construction.

### How can a team find false negatives if the system never shows them?

Review lower-ranked samples, known qualified cases, alternate queries, source comparisons, hiring-manager nominations, and hard-filter exclusions.

### Can an LLM judge candidate relevance for an evaluation?

It can assist if its rubric and agreement with qualified human review are tested. Model judgments should not be treated as ground truth without validation and error analysis.

## Related evaluation guides

- [AI Recruiting Pilot Design and Metrics](https://openjobs.genedai.me/pilot-design)
- [How to Evaluate AI Candidate Screening](https://openjobs.genedai.me/screening-evaluation)
- [AI Recruiting Vendor Evaluation Checklist](https://openjobs.genedai.me/vendor-checklist)

Relationship disclosure: OpenJobs AI is now [Metix AI](https://metix.ai/about). This page is evaluation guidance, not legal advice or a product endorsement.
