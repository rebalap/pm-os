# Executive Summary: End-to-End User Journey
## Autism Therapy Platform — Indian Therapy Center Lifecycle

**Date:** 2026-04-14 | **Stage:** Discovery | **Evidence base:** Secondary research only
**Prepared for:** Product & Design Leadership

---

## 🔄 MVP Scope Update — 22 April 2026

> **Updated:** 2026-04-22T00:00:00+05:30 | Engineering Alignment Meeting

The engineering alignment session on 22 April 2026 produced a key scope decision. The journey model has since been updated from the original 9 journeys to **12 journeys (Journey 0–11)**. Of the 12, eight journeys are in scope for the MVP — all buildable using existing EMR components. Four journeys are not in scope: **Journey 4 (Clinical Program Design)**, **Journey 7 (Supervisor Review & Program Updates)**, and **Journey 8 (Progress Reports)** require net-new build and are deferred to post-MVP; **Journey 5 (In-Session Data Collection)** remains out of scope for the Indian market.

**Revised MVP scope at a glance:**

| Journey | MVP |
| --- | --- |
| Journey 0 — DPDPA Consent Management | ✅ In |
| Journey 1 — Family Inquiry & First Contact | ✅ In |
| Journey 2 — Intake & Enrollment | ✅ In |
| Journey 3 — Scheduling & Attendance Management | ✅ In |
| Journey 4 — Clinical Program Design | ❌ Deferred |
| Journey 5 — In-Session Data Collection | ❌ Out — India MVP |
| Journey 6 — Session Notes / Clinical Notes | ✅ In |
| Journey 7 — Supervisor Review & Program Updates | ❌ Deferred |
| Journey 8 — Progress Reporting to Parents | ❌ Deferred |
| Journey 9 — Billing & Fee Collection | ✅ In |
| Journey 10 — Dropout Prevention | ✅ In |
| Journey 11 — Analytics Dashboard | ✅ In |

**What this changes:** The original exec summary below identifies in-session data collection (Journey 5) as the foundational break point and the highest-priority problem to solve. That recommendation stands for the long-term product vision. For the MVP, however, the platform will launch as a **clinical management tool** — solving scheduling, billing, enrollment, and dropout prevention — rather than as a therapy-specific data platform. Clinical differentiation (program design, supervisor review workflows, structured progress reporting) follows in a subsequent release.

**Risk to monitor:** Therapist adoption is the make-or-break variable. Primary research is underway to determine whether deferring Journey 4, Journey 7, and Journey 8 creates an adoption blocker before MVP scope is locked.

---

> Evidence labels: ✅ Observed (peer-reviewed / regulatory source) | 🔵 Inferred | 🔶 Hypothesis (unvalidated)
> ⚠️ DPDPA = regulatory risk flag (Digital Personal Data Protection Act 2023)

---

## The Journey at a Glance

A child's therapy journey at an Indian autism center spans 8 stages across 4 personas —
from a family's first WhatsApp message to ongoing therapy, billing, and (too often) silent dropout.
The entire journey runs on paper, WhatsApp, and memory. No structured digital tool exists at any stage.

| Stage | Primary persona | Core tool today | Biggest break |
| --- | --- | --- | --- |
| 1. Family inquiry | Rahul (Director) | WhatsApp / memory | No inquiry tracking; leads lost |
| 2. Intake & enrollment | Rahul, Dr. Sunita | Paper forms | No consent mechanism; DPDPA exposure ⚠️ |
| 3. Assessment & program design | Dr. Sunita (Supervisor) | Paper / Word | Verbal handover to therapist; program misapplied |
| 4. In-session data collection | Priya (Special Educator) | Paper data sheet | One-handed constraint; 1–2 week feedback lag |
| 5. Supervisor review | Dr. Sunita | Paper / Excel | Batch review; outdated targets run for weeks |
| 6. Progress reporting | Dr. Sunita | Word / WhatsApp | Written from scratch; reports parents can't read ⚠️ |
| 7. Billing & fee collection | Rahul | WhatsApp / paper | Manual, relationship-sensitive; fees delayed |
| 8. Dropout & follow-up | Rahul | WhatsApp message | No tracking; dropout invisible until it's done |

---

## Stage-by-Stage Breakdown

### Stage 1 — Family Inquiry & First Contact
A parent hears about the center through word of mouth or a paediatrician referral and sends a WhatsApp message. The inquiry is noted in the WhatsApp thread itself — or in a paper notebook — with no structured record. There is no pipeline visibility, no automated follow-up, and no reminder if the family goes quiet.

**Emotional state:** Meena (parent) arrives anxious and exhausted from a long diagnostic journey. This is a high-stakes trust moment. ✅ Tandfonline 2025

**Key break:** Warm leads are lost because they live in a WhatsApp scroll history. 🔶

---

### Stage 2 — Intake & Enrollment
The family arrives for an intake appointment. A developmental history is taken verbally or on paper. Prior documents — diagnosis reports, school records, UDID card — are collected as photocopies. A fee structure is explained verbally. A consent form may or may not be signed.

**Emotional state:** Meena is overwhelmed and needs to feel heard. Dr. Sunita is clinically focused but time-pressured. ✅ / 🔶

**Key breaks:**
- No standardised intake protocol — process varies by staff and day ✅ PMC
- Digital storage of child health records without verifiable parental consent = **DPDPA 2023 non-compliance** ⚠️ ✅
- Fee agreement is verbal — ambiguity accumulates over months 🔶

---

### Stage 3 — Assessment & Program Design
Dr. Sunita conducts 1–3 assessment sessions (ISAA, CARS, Vineland). Results are compiled on paper into a baseline profile. An individualised therapy program is written — targets, prompt levels, reinforcement schedules. This program is communicated to Priya via a verbal briefing, possibly with a paper handout.

**Key breaks:**
- Verbal handover = Priya may run sessions with misremembered prompt levels or wrong targets 🔶
- Parents leave without a written summary of what is being worked on or why 🔶
- RPWD Act 2016 mandates documented individualised programs — compliance is informal ✅ / 🔶

---

### Stage 4 — Ongoing Therapy Sessions (In-Session Data Collection)
This is the highest-frequency workflow in the product. Priya runs discrete trials (DTT) or naturalistic teaching (NET) with the child, marking outcomes on a paper data sheet — correct, incorrect, or prompted — while managing the child with her other hand.

**Key breaks:**
- **One-handed constraint** makes paper recording physically awkward; entries are missed or illegible 🔵
- ABC data (antecedent-behaviour-consequence) is often written retrospectively from memory — inaccurate by design 🔵
- Paper data sheets sit in a physical file until Dr. Sunita reviews them — sometimes **1–2 weeks later** ✅ BHCOE
- Some therapists photograph paper sheets and send via WhatsApp — unencrypted transmission of child health data ⚠️ DPDPA 🔶

**This is the foundational break point.** Everything downstream — program updates, reports, billing — depends on session data that is currently inaccurate, delayed, and inaccessible.

---

### Stage 5 — Supervisor Review & Program Updates
Dr. Sunita collects paper data sheets and manually calculates percentage-correct per target. She identifies mastery or plateau patterns and updates the therapy program. Changes are communicated to Priya verbally.

**Key breaks:**
- Manual calculation is time-consuming and error-prone 🔵
- Global benchmark: **2–3 hours/day** on documentation without software tools ✅ ABA Matrix — Indian equivalent unvalidated 🔶
- Program update communicated verbally → Priya may continue running old targets 🔶
- No version history: "What was the prompt level 4 weeks ago?" is unanswerable 🔵

---

### Stage 6 — Progress Reporting to Parents
Monthly or quarterly, Dr. Sunita compiles session data and writes a progress narrative per domain. Reports are handed over in person or sent as a PDF via WhatsApp. A verbal meeting may accompany the report. Home program instructions are given verbally.

**Key breaks:**
- **Reports are written from scratch every cycle** — no carry-forward from prior reports or auto-population from session data 🔵
- Report language is clinical; Meena frequently doesn't understand what she's reading ✅ Product context
- WhatsApp delivery of progress reports = unencrypted sensitive health data ⚠️ DPDPA 🔵
- Home program guidance is verbal — Meena is unlikely to remember what to practise 🔶

---

### Stage 7 — Billing & Fee Collection
Rahul tallies sessions from a paper attendance register, calculates fees, and sends a WhatsApp message to the family. Payment is made in cash or via UPI. Outstanding balances are tracked in Excel or not at all.

**Key breaks:**
- Asking financially stressed families for money is emotionally uncomfortable — Rahul delays these conversations 🔶
- No automated reminder — Rahul must manually track who has paid 🔵
- No financial dashboard: monthly revenue, collection rate, outstanding fees are invisible at a glance 🔵
- Evidence: **no-show rates drop from 39% → 3%** with structured reminders ✅ Psychiatric Services — the same principle applies to payment follow-up 🔵

---

### Stage 8 — Appointment Follow-Up & Dropout Prevention
A family misses a session. Staff notice through memory or a gap in the paper schedule. A single WhatsApp message is sent. If the family goes quiet, dropout is effectively accepted — experienced as an outcome, not a process failure.

**Key breaks:**
- No attendance tracking system — dropout is **invisible until it has already happened** 🔵
- "Invisible exits": families withdraw silently under financial strain and caregiver exhaustion ✅ Tandfonline 2025
- One WhatsApp message is the entire dropout intervention — evidence shows live contact is 13× more effective ✅
- No re-engagement protocol: if a family returns after a gap, no structured way to update the program exists 🔶

---

## The 5 Highest-Impact Break Points

| # | Break point | Stage | Personas hit | Evidence |
| --- | --- | --- | --- | --- |
| BP-01 | Paper in-session data collection — delayed, inaccurate, one-handed | Stage 4 | Priya, Dr. Sunita | 🔵 ✅ |
| BP-02 | Supervisor review happens in batch, 1–2 weeks behind | Stage 5 | Dr. Sunita, Priya | ✅ |
| BP-03 | Progress reports written from scratch; parent can't understand them | Stage 6 | Dr. Sunita, Meena | 🔵 🔶 |
| BP-04 | No attendance tracking; dropout invisible until complete | Stage 8 | Rahul, Meena | 🔵 ✅ |
| BP-05 | No intake protocol; DPDPA non-compliance from day one | Stage 2 | All | ✅ ⚠️ |

---

## What This Means — Decisions Required

1. **In-session data collection is the foundation.** Every other break point is downstream of inaccurate, delayed session data. Solve this first or there is nothing reliable to build reporting, billing, or dropout prevention on.

2. **DPDPA compliance is not a later feature.** It appears at Stages 2, 4, and 6. The first time the product stores a child's clinical data digitally, verifiable parental consent is a legal requirement — not a roadmap item.

3. **WhatsApp is in the journey whether we design for it or not.** It is the inquiry channel, the billing channel, the progress report delivery channel, and the dropout follow-up channel. The product must map to these touchpoints, not replace them.

4. **Dropout prevention has the strongest evidence ROI.** The 39% → 3% no-show rate finding is the sharpest data point across all research. Structured attendance tracking with reminder triggers is a high-impact, low-complexity Phase 2 candidate.

5. **Validate before designing.** Approximately 45% of this journey map is hypothesis, not observed fact. Primary fieldwork at 3–5 centers is the gate before any design work begins.

---

## Open Assumptions (Top 5 by Risk)

| Hypothesis | Risk | Validate via |
| --- | --- | --- |
| Priya records trial data on paper during live sessions (vs. skipping entirely) | High | Contextual observation |
| Offline-first is a hard requirement in session rooms | High | On-site connectivity test |
| Supervisor-to-therapist handover is verbal; program is misapplied | High | Observation + debrief interview |
| Supervisors spend significant out-of-hours time on report writing | High | Time-diary / interview |
| Centers are not DPDPA-compliant at intake | High | Director interview + consent form review |
