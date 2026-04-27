# Executive Summary: Autism Therapy Platform — Discovery Research
**Date:** 2026-04-14 | **Stage:** Discovery | **Prepared for:** Leadership

---

## What We Know

- **There is no India-specific software for any core clinical workflow.** No purpose-built tool exists for in-session data collection, intake, treatment planning, or billing in Indian autism therapy centers. TherapEZ offers general scheduling; Cognitivebotics is child-facing only. The entire stack — paper, WhatsApp, Excel — is informal and unstructured across all three workstreams.
- **The documentation burden is high and concentrated in the most time-scarce person.** Global evidence puts manual clinical documentation at 2–3 hours per day for therapy providers. In Indian centers, treatment plan authorship and progress reporting fall primarily on the senior therapist or founder — the same person running the center.
- **Regulatory exposure is real and unaddressed.** DPDPA 2023 requires verifiable parental consent for digital processing of minors' health data. RPWD Act 2016 mandates individualized program documentation. UDID documentation is a recurring obligation. Current informal workflows meet none of these requirements.
- **No-show and dropout rates are high and measurable.** Evidence shows no-show rates drop from 39% (no reminder) to 3% (live contact). Dropout in Indian autism therapy is driven by financial pressure, caregiver exhaustion, and the absence of any tracking system — meaning centers experience dropout as an outcome, not a process failure they can intervene on.
- **Intake is a trust-critical moment that currently has no structure.** Families arrive after long, exhausting diagnostic journeys. Disorganized intake actively increases early dropout risk. The transition from assessment to therapy program — a clinical quality handoff — happens informally or not at all.

---

## What This Means — Decisions Required

- **Decide which user's pain to solve first — the special educator's in-session data collection or the center director's administrative burden** — before scoping any feature. These are different users, different devices, and different sessions. Picking both at launch is scope risk.
- **Decide whether DPDPA 2023 compliance is a product differentiator or a minimum bar** before building any data storage or intake flow. If compliance is a selling point, design it into the intake workflow from day one. If it is table stakes, define the minimum viable consent mechanism now.
- **Decide how the product will handle WhatsApp** before designing any communication or follow-up feature. WhatsApp is infrastructure for parent communication and billing; a tool that ignores this will be rejected in field adoption.
- **Decide whether offline-first is a hard requirement for the MVP** before committing to a technical architecture. This decision gates the entire data collection module design and cannot be reversed cheaply.
- **Validate willingness-to-pay at Indian price points before building anything**, particularly for the center director persona. The gap between an admin burden that is painful and one that justifies software spend is the make-or-break commercial question.

---

## Open Risks & Assumptions

| Assumption / Risk | Level | Status |
|---|---|---|
| Special educators find current data collection painful enough to change behavior | High | Unvalidated |
| Documentation burden (2–3 hrs/day) manifests at scale in Indian centers | High | Unvalidated |
| Center directors will pay for a unified tool at Indian price points | High | Unvalidated |
| Most Indian centers are not DPDPA 2023 compliant | High | Unvalidated |
| Offline-first is a hard requirement, not a nice-to-have, for session rooms in Indian centers | High | Unvalidated |
| Treatment plan authorship falls on the most time-scarce staff member | Medium | Unvalidated |
| Centers using Cognitivebotics still rely on paper for in-session clinical data collection | Medium | Unvalidated |
| UDID documentation support is a recurring admin pain centers would pay to streamline | Medium | Unvalidated |
| Parents would engage with structured progress updates beyond WhatsApp | Medium | Unvalidated |
| English-only UI is acceptable for metro market at launch | Low | Unvalidated |

---

## Recommended Next Steps

| Action | Owner | Timeframe |
|---|---|---|
| Conduct contextual inquiry at 3–5 Indian therapy centers — observe in-session data collection and intake workflows firsthand | Researcher | Next 3 weeks |
| Interview 5+ center directors on documentation burden, billing workflows, and willingness-to-pay | Researcher | Next 3 weeks |
| Define the primary persona for MVP scope — special educator or center director | Product Consultant | Before fieldwork synthesis |
| Assess DPDPA 2023 obligations with a legal or compliance advisor; document minimum consent requirements | Product / Legal | Before any data architecture decisions |
| Synthesize primary fieldwork into validated findings and update the product CLAUDE.md | Researcher | Within 1 week of fieldwork completion |
