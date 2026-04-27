# Engineering Alignment Meeting — Summary
**Date:** 22 April 2026
**Product:** Autism Therapy Platform (India)
**Attendees:** Product, Engineering (EMR team)

---

## Purpose

A walkthrough of the full platform lifecycle to align engineering on the scope of the MVP. The session covered 8 user journeys end-to-end and concluded with a key architectural decision about how much of the platform can be built on top of existing EMR components.

---

## Journeys Discussed

Eight journeys were presented covering the complete operating cycle of an autism therapy center:

| # | Journey | Description |
| --- | --- | --- |
| J1 | Child Enrollment and Intake | Onboarding a new child — intake, consent (DPDPA), profile creation, therapist assignment |
| J2 | Clinical Program Design | Designing in-person therapy programs; defining targets, baselines, and approval workflows for therapists |
| J3 | Session Notes / Clinical Notes | Post-session documentation by therapists; supervisor review and approval |
| J4 | Progress Reports | Monthly reports auto-populated from session notes; reviewed by supervisor and delivered to parents |
| J5 | Billing | Attendance-driven invoice generation and payment collection (UPI, cash, cheque) |
| J6 | Scheduling and Attendance Management | Weekly schedule creation and the critical attendance mark by therapists (≤ 2 taps, offline-first) |
| J7 | Dropout Prevention / Patient Engagement | Absence detection, WhatsApp follow-up, escalation, and discharge workflows |
| J8 | Dashboard and Analytics | Center-level visibility into attendance, revenue, clinical outcomes, and dropout risk |

> **Note:** In-session data collection was explicitly excluded from this scope discussion. It was not presented as one of the  journeys.

---

## Key Discussion Points

### In-Session Data Collection — Explicitly Out of Scope

In-session behavioral data collection (e.g., trial-by-trial ABA data) was not included in the journey walkthrough and is out of scope for the MVP. The reasoning shared in the meeting:

- In the Indian market, therapy is paid out-of-pocket and there is no reimbursement system that requires session-level data logging to generate a billing claim.
- In-session data collection would be a strong differentiator for **US and international markets where insurance reimbursement requires granular clinical documentation** — but this does not apply to Indian centers at this stage.

### Engineering's Position — Reuse Existing EMR Components

After reviewing the full journey walkthrough, the engineering team (working on an existing EMR product) indicated that **most of the 8 journeys — with the exception of J2 (Program Design) and J4 (Progress Reports) — can be built by reusing existing EMR components** with relatively low incremental effort.

This has a significant implication for how the product is positioned:

> **The platform will function as a clinical management tool rather than a therapy-specific platform at MVP.** The highly clinical features — individualized therapy program design and structured progress reporting — are the parts that require net-new build and are therefore deferred.

This is a pragmatic approach to get to market faster, but it means the MVP will not differentiate on clinical depth. That is an acceptable trade-off only if the core management workflows (scheduling, billing, notes, enrollment) provide enough value to drive adoption and generate primary research signal.

---

## MVP Scope Decision

| Journey | MVP Status | Rationale |
| --- | --- | --- |
| J1 — Enrollment and Intake | **In scope** | Core to onboarding; reusable EMR components available |
| J2 — Clinical Program Design | **Out of scope** | Therapy-specific; requires net-new build; deferred to post-MVP |
| J3 — Session Notes | **In scope** | Clinical documentation; reusable components available |
| J4 — Progress Reports | **Out of scope** | Therapy-specific reporting; requires net-new build; deferred |
| J5 — Billing | **In scope** | Core to center operations; reusable components available |
| J6 — Scheduling and Attendance | **In scope** | Core to center operations; reusable components available |
| J7 — Dropout Prevention | **In scope** | Operational workflow; reusable components available |
| J8 — Analytics Dashboard | **In scope** | Center visibility; reusable components available |
| In-Session Data Collection | **Out of scope** | Not applicable in Indian out-of-pocket market; US/international opportunity |

---

## Risks and Open Questions

- **Adoption risk without J2 and J4:** Program design and progress reports are two of the highest-value features for therapists and supervisors. Without them, the MVP is primarily an admin and scheduling tool. The risk is that therapists — whose adoption is the make-or-break variable — do not find enough clinical value to change their current WhatsApp/paper workflow.
- **Validation needed:** Before confirming which features are safe to omit, primary research with therapy centers is required to understand which pain points are genuinely acute. Some features marked as deferrable may turn out to be blockers for adoption.
- **"Clinical management tool" positioning:** This is a strategic shift from the original product framing. It needs to be reflected in updated journey maps, PRD scope, and any customer-facing messaging.

---

## Next Steps

| Action | Owner | Notes |
| --- | --- | --- |
| Analyse capabilities and confirm what can be reused from existing EMR | Engineering | Validate the assumption that J1, J3, J5, J6, J7, J8 are achievable via component reuse |
| Primary research with therapy centers | Product | Validate pain points and understand which features are high-risk to omit — specifically test whether J2 and J4 are blockers to adoption |
| Update journey maps and flows to reflect MVP scope | Product | Remove J2 and J4 from MVP journeys; update dependency chain accordingly |
| Confirm final MVP scope | Product + Engineering | After research findings and engineering analysis are complete |

---

## Decisions Log

| Decision | Made by | Date |
| --- | --- | --- |
| J2 (Program Design) is out of scope for MVP | Engineering + Product | 22 April 2026 |
| J4 (Progress Reports) is out of scope for MVP | Engineering + Product | 22 April 2026 |
| In-session data collection is out of scope for MVP | Product | 22 April 2026 |
| MVP will act as a clinical management tool, not a therapy-specific platform | Engineering + Product | 22 April 2026 |
