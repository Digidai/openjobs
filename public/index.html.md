# The AI Recruiting Field Guide

> Evaluate AI recruiting systems by hiring outcomes, evidence quality, human control, and pilot risk—not by interface polish, profile volume, or automation claims.

- Canonical HTML: https://openjobs.genedai.me/
- Last substantive review: 2026-08-07
- Language: English
- Scope: Buyer-oriented evaluation guidance; not legal advice, a compliance determination, or an independent product endorsement.

## Entity transition

OpenJobs AI is now [Metix AI](https://metix.ai/). The first-party account of the transition is [About Metix AI](https://metix.ai/about). This archive publishes evaluation tools rather than job listings.

## Decision question

Can the system repeatedly turn a clear hiring brief into qualified, interested people worth interviewing—while keeping the employer in control?

## 1. Set the unit of value

A profile is inventory. An interview is progress. Search coverage, match scores, and generated outreach can describe activity without proving a hiring outcome.

- **Quality — worth meeting:** Can the hiring manager explain why each person clears the role's non-negotiable requirements? Review false positives, not just the best examples.
- **Intent — actually interested:** A plausible profile is not a candidate. Verify that interest is current, role-specific, and not inferred from a reply alone.
- **Time — ready to schedule:** Measure elapsed time from an approved brief to an interview-ready handoff. Exclude buyer rework and manual cleanup.

## 2. Trace the evidence chain

A recruiting agent is a sequence of interpretations, retrievals, rankings, messages, replies, and decisions. Inspect every handoff:

1. **Brief:** Separate must-haves, preferences, trade-offs, and evidence of seniority. Record what the hiring manager approved.
2. **Search:** Document sources, refresh dates, coverage limits, exclusions, and likely blind spots.
3. **Match:** Trace each recommendation to role-relevant evidence and make interpretations correctable.
4. **Engage:** Identify who approves sender identity, message content, channel, timing, follow-up, and suppression handling.
5. **Handoff:** Deliver a qualified and interested person with evidence, context, unresolved questions, and a clear next step.

For a first-party architecture example, read Metix AI's [Mira system report](https://metix.ai/research/mira-end-to-end-ai-recruiter). Treat it as product research to test, not independent validation.

## 3. Keep control visible

Autonomy is useful only when correction is cheap. “Human in the loop” is not sufficient without identifiable controls.

- **Approval:** Nothing external happens before the accountable person can review it.
- **Correction:** A bad assumption can be fixed without restarting the workflow.
- **Traceability:** Inputs, recommendations, edits, sends, replies, and handoffs remain distinguishable.
- **Fallback:** The team can pause automation and finish the process manually.

## 4. Review risk in context

Risk depends on the role, jurisdiction, data, selection procedure, and how people use the output. A vendor checklist cannot make the employer's decision.

- **Govern:** Assign responsibility for scope, approved use, incidents, candidate questions, and changes to models or data.
- **Measure:** Test false negatives, accessibility barriers, inconsistent treatment, stale data, unsupported inferences, and message errors.
- **Manage:** Define escalation, accommodation, correction, deletion, and human-takeover paths before a pilot touches real candidates.

Primary references: [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework), [EEOC selection-procedure guidance](https://www.eeoc.gov/laws/guidance/employment-tests-and-selection-procedures), and [ADA.gov hiring technology guidance](https://www.ada.gov/resources/ai-guidance/).

## 5. Run a reversible pilot

Use one real role, one recent baseline, and pre-agreed stop conditions.

1. **Freeze the brief:** Record approved requirements, trade-offs, geography, compensation assumptions, and the evidence standard.
2. **Set the baseline:** Use a comparable role and record time, people reviewed, outreach, interested replies, interviews, and manager rework.
3. **Pre-score quality:** Define “worth interviewing” before seeing the vendor's best candidates; sample rejects and borderline cases.
4. **Limit exposure:** Start with a narrow candidate set, explicit approvals, and a channel that can be paused.
5. **Close the loop:** Compare outcomes and hidden labor; document failures, corrections, and conditions for expansion.

Use the [24-point evaluation scorecard](https://openjobs.genedai.me/evaluation-scorecard) to structure the review.

## 6. Read evidence by source type

The [primary-source ledger](https://openjobs.genedai.me/sources) separates public risk frameworks, employment guidance, and first-party product research. Government guidance can frame obligations and risk questions. First-party research can support statements about what a vendor says it built, measured, or learned. Neither alone proves a specific deployment is lawful, fair, or effective.

## Decision rule

Buy less interface. Demand more evidence. Prefer the system that delivers a better hiring outcome, exposes enough evidence to evaluate it, and makes correction cheaper than carrying a bad assumption forward.

## Related Metix resources

- [Metix AI](https://metix.ai/) — current customer-facing product and brand.
- [Metix AI research](https://metix.ai/research) — first-party product and engineering research.
- [Metix AI pricing](https://metix.ai/pricing) — current first-party commercial information.
- [Contact Metix AI](https://metix.ai/contact) — talk with the product team.
