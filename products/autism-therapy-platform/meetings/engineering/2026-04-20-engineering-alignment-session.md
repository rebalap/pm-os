# Engineering Alignment Session — Autism Therapy Platform

**Date:** April 20, 2026
**Duration:** 60 minutes
**Audience:** Engineering team (all roles — backend, frontend, mobile, QA)
**Facilitator:** PM
**Status:** Prepared — ready to run

---

## Meeting Objective

Give every engineer a shared, accurate mental model of who we are building for, what the full product does end-to-end, and the exact order we need to build it in — so that sprint planning produces a dependency-safe, constraint-aware build sequence.

**What we want engineers to leave with:**

- **Shared mental model of the user:** A clear picture of four specific people — what they do, the device in their hand, the room they're in, and what breaks if we get the product wrong for them
- **Clarity on what we're building:** How the 9 user journeys connect to the 5 feature clusters, and which journeys are load-bearing versus which can ship later
- **Clarity on build sequence and constraints:** A non-negotiable Phase 1 foundation, the technical constraints that are hard walls not preferences, and the dependency chain that governs everything downstream

---

## Pre-Read List

Engineers attending this session should read at least these three documents before walking in. Reading time: approximately 25–30 minutes total.

| Document | Path | Why it matters |
|---|---|---|
| **Journey Map** — Full lifecycle, personas, and hypothesis register | `products/autism-therapy-platform/research/journey-map.md` | Gives you the clinical and operational context everything else is built on. The persona definitions and the 8 lifecycle stages are the foundation for the whole session. |
| **Journey 9 — DPDPA Consent Management** | `products/autism-therapy-platform/user-journeys/journey-09-dpdpa-consent-management.md` | This is the technical and regulatory gate that makes every other journey possible. The 423-Locked pattern, the atomic transaction requirement, and the DPDPA/RPWD conflict decision are non-negotiable constraints engineering must understand before we talk about any clinical feature. |
| **Journey 3 — Post-Session Documentation** | `products/autism-therapy-platform/user-journeys/journey-03-post-session-documentation.md` | The most technically constrained journey in the product. The offline-first write pattern, the sync → review → co-sign state machine, and the one-handed UX requirement are fully documented here. If you read nothing else, read this. |

**Optional fourth pre-read** (10 minutes): Journey 1 (Child Enrollment) — for the DPDPA consent flow in intake context, duplicate detection, and the care team assignment mechanics.

---

## Timed Agenda — 60 Minutes

| Time | Section | What is covered | Leads | Key question answered |
|---|---|---|---|---|
| 0:00–0:05 | Why we're here | Context setting: what the product is, what market we're in, why now | PM | What are we actually building and why does it matter? |
| 0:05–0:15 | Who we're building for | Walk through the 4 personas: Priya, Dr. Sunita, Rahul, Meena — their devices, their context, their non-negotiable constraints | PM | Who is the human on the other end of every API we write? |
| 0:15–0:30 | The therapy centre lifecycle | Walk through all 8 stages of the clinical and operational lifecycle. What happens today (paper, WhatsApp, Excel). What the software must do instead. | PM | What is the full arc of the problem we are solving? |
| 0:30–0:50 | Journey-to-feature mapping | Walk through all 9 user journeys: trigger, actor, critical screen, critical technical requirement, and dependency chain | PM, Engineering leads to flag questions in real-time | Which features depend on which other features, and what breaks if we build them out of order? |
| 0:50–1:00 | Technical constraints, build sequence, open questions | Non-negotiable constraints. Phase 1–4 build order. Structured Q&A on the 8 engineering questions listed in Section 9. | PM facilitates, engineers answer | What is the defensible build sequence and which open technical decisions do we need to close today? |

---

## Section 1: Who We're Building For — Persona Briefing

### Persona 1: Priya — Special Educator / Behavior Therapist

**Role and job-to-be-done:** Delivers 1:1 ABA therapy sessions with children; needs to log what happened during each trial so her supervisor can see accurate data and adjust the program.

**The single most important thing engineering must understand about building for Priya:** She has one hand on the child and one hand on her phone. The session does not pause for data entry. Every tap beyond two is a failure mode. She will not use a feature that requires her to look away from a dysregulated 7-year-old.

**Device, connectivity, and context of use:**
- Device: Low-to-mid-range Android (Redmi Note, Realme C series). 2–3 GB RAM, Android 10+. Assume no iOS.
- Connectivity: Session rooms may have poor or no mobile data. Offline-first is not a design preference — it is a product requirement.
- Context: In-session, physically active child, noise, haptic feedback preferred over audio.

**The one constraint that cannot be compromised:** Attendance marking must be completable in ≤ 2 taps from her home screen. This is QA-verified on physical device as a launch criterion. If it takes 3 taps on a Redmi Note 11, the feature fails.

---

### Persona 2: Dr. Sunita — Clinical Supervisor / Senior Therapist

**Role and job-to-be-done:** Designs therapy programs, supervises junior staff, reviews session data, and writes progress reports — currently spending uncompensated evening hours doing documentation that paper makes slow and painful.

**The single most important thing engineering must understand about building for Dr. Sunita:** She is the system's most important data consumer. If session notes don't reach her within 30 seconds of sync, her entire supervision workflow collapses. Her caseload dashboard, the SOAP note flow, and the progress report auto-population all depend on clean, timely, correctly attributed data from Priya.

**Device, connectivity, and context of use:**
- Device: Android phone as primary; laptop/desktop for extended documentation work (report writing, SOAP notes). Both form factors must work — do not design desktop-only for Dr. Sunita.
- Connectivity: Generally reliable — she works from an office or at a desk. Online-first is acceptable for her workflows, with read-from-cache as a fallback.
- Context: Between sessions, reviewing data in batch. Cognitive load is high; she needs filtered, prioritised views — not raw data dumps.

**The one constraint that cannot be compromised:** The supervisor notes queue must scope strictly to her assigned caseload. Cross-caseload visibility without explicit RBAC grant is a DPDPA violation, not a UX edge case.

---

### Persona 3: Rahul — Center Director / Founder

**Role and job-to-be-done:** Runs the center operationally and often clinically — tracks attendance, billing, staff utilization, and dropout risk — currently managing this with WhatsApp, Excel, and memory.

**The single most important thing engineering must understand about building for Rahul:** He is the economic buyer and the person who will or will not roll this product out to his staff. If his home screen takes more than 3 seconds to load his outstanding fees figure, he will go back to Excel. Dashboard performance on a low-end Android is not a nice-to-have.

**Device, connectivity, and context of use:**
- Device: Android phone as primary. Mid-range to low-end. May use a laptop for month-end review.
- Connectivity: Generally reliable in the office.
- Context: Between clinical sessions, often context-switching. The dashboard must be glanceable — one number at a glance, no required navigation to get the summary.

**The one constraint that cannot be compromised:** The center operations home screen must render its outstanding fees total and dropout-risk count within 3 seconds on a 4G connection. No spinner behind a navigation tap to get there.

---

### Persona 4: Meena — Parent / Primary Caregiver

**Role and job-to-be-done:** Brings child to sessions, pays fees, and tries to implement home programs — currently receiving clinical reports she cannot understand and informal updates via WhatsApp.

**The single most important thing engineering must understand about building for Meena:** She is the least technical person in the system and the most emotionally invested. Every interaction she has with the platform — the consent screen, the intake form, the progress report — must pass a comprehension test by a non-technical adult. She is not a user we can onboard with a walkthrough video.

**Device, connectivity, and context of use:**
- Device: Android phone. WhatsApp-fluent. Not comfortable with clinical platforms or formal app login flows.
- Connectivity: Generally reliable on mobile.
- Context: Receiving documents via WhatsApp, not navigating an app. Her primary touchpoint is probably a PDF on her phone, not a dashboard login.

**The one constraint that cannot be compromised:** The DPDPA consent flow must be completable on a shared center tablet by a non-technical parent with minimal staff assistance. Privacy notice minimum font size 16px, plain language, no clinical jargon.

---

### Context anchor: Arjun — the child (not a software user)

Arjun is 3–12 years old, autistic, active or dysregulated during sessions. He is not in the system, but his presence is the reason for every one-handed, haptic-only, ≤ 2-tap constraint in the product. When you are reviewing a design that touches Priya's in-session workflow, ask: "Is Priya doing this while managing Arjun?" If yes, the constraint applies.

---

## Section 2: The Therapy Centre Lifecycle — 8 Stages

This is the full arc of a child's journey through a therapy center. The software must support every stage. The table below shows what happens today (manually) and what the platform must do instead.

| Stage | What happens | Primary actor | Current broken/manual workflow | What the software does instead |
|---|---|---|---|---|
| **1 — Family Inquiry & First Contact** | Parent hears about the center and makes contact for the first time | Rahul / admin | Inquiry details land in a WhatsApp thread or paper notebook with no structured record; no pipeline visibility; no automated follow-up | Structured child record creation with intake status tracking; enrollment pipeline visible to Rahul |
| **2 — Intake & Enrollment** | Family arrives; developmental history captured; documents collected; consent signed; fee explained; schedule agreed | Rahul, Dr. Sunita, Meena | Paper intake form or verbal interview; documents photocopied; consent form on paper (often non-DPDPA-compliant); fee agreement verbal; child record is an Excel row | Digital intake form (parent-completable on shared tablet or own phone); DPDPA-compliant parental consent capture; structured child EMR created; all documents uploaded and encrypted |
| **3 — Assessment & Program Design** | Formal assessment conducted (ISAA, CARS, Vineland equivalent); baseline established; individualized therapy program written; home program created; recurring schedule set | Dr. Sunita | Assessment on paper forms; program written in Word document; verbal briefing to Priya; parent receives verbal or WhatsApp summary of the plan | Digital therapy program created from templates; version-controlled; pushed to Priya's session screen in ≤ 30 seconds; home program created separately with parent-friendly language |
| **4 — Ongoing Therapy Sessions (In-Session Data Collection)** | Priya delivers session; marks outcomes trial by trial; tracks maladaptive behaviors; manages active child one-handed | Priya | Paper data sheet with tick marks; retrospective ABC notes; data handed to supervisor in physical file or WhatsApp photo | Offline-first attendance mark (≤ 2 taps); post-session structured note with goals multi-select from active program targets; haptic-only confirmation |
| **5 — Supervisor Review & Program Updates** | Dr. Sunita reviews session data in batch; calculates progress percentages; identifies mastered or plateaued targets; updates the program | Dr. Sunita | Reviews paper sheets or WhatsApp photos of data sheets; manual calculation; verbal or paper update to Priya; review typically 1–2 weeks delayed | Session notes queue filtered to her caseload; SOAP note creation with guided prompts; program update pushes to Priya's session screen within 30 seconds |
| **6 — Progress Reporting to Parents** | Monthly or quarterly progress report written; home program updated; report shared with family | Dr. Sunita | Report written from scratch in Word; shared as printed paper or WhatsApp PDF (unencrypted); home program guidance verbal | Progress report auto-populated from session notes and SOAP notes; PDF generated with center letterhead; delivered via WhatsApp Business API with consent gate and opt-in gate both checked |
| **7 — Billing & Fee Collection** | End-of-month invoice generated; sent to family; payment collected; overdue followed up | Rahul | Tallies sessions from paper register; calculates fee manually; sends WhatsApp message; records payment in Excel or paper receipt; no dashboard of outstanding balances | Invoice auto-generated from confirmed attendance records; UPI payment link sent via WhatsApp; payment auto-reconciled via webhook; overdue reminders on configurable schedule |
| **8 — Dropout Prevention & Re-engagement** | Family misses a session; staff notice; follow-up sent; session rescheduled or family disengages silently | Rahul | Memory-based detection; single WhatsApp message; no systematic tracking; dropout is invisible until weeks after it has happened | No-show detection triggers 30-minute delayed follow-up message; daily attendance gap scan flags 2+ consecutive missed sessions; "At Risk" status management; "Sort by Last Session" view in Rahul's dashboard |

---

## Section 3: Journey-to-Feature Mapping

The heart of this session. For each of the 9 user journeys: what triggers it, who owns it, what it draws from, and what engineering must know.

---

### Journey Table: All 9 Journeys at a Glance

| # | Journey | Trigger | Primary actor | Steps | Feature clusters | Critical screen | Critical technical requirement | Hard dependencies |
|---|---|---|---|---|---|---|---|---|
| J1 | Child Enrollment & Onboarding | Parent contacts center; Rahul decides to enroll | Rahul | 20 | C1 (EMR-001–005), C2 (INT-001–005, MPM-001, MPM-002, MPM-005), C4 (SCHED-001, SCHED-002) | DPDPA Consent Form | Consent record must be written as an atomic transaction: consent write + audit log write succeed together or both fail (no partial state) | J9 (DPDPA consent infrastructure) → J1 |
| J2 | Clinical Program Design | Intake assessment complete; Dr. Sunita builds the therapy program | Dr. Sunita | 24 | C1 (TMPL-001–005, SOAP-001–004, EMR-003–005), C2 (MPM-001–005), C4 (SCHED-001, SCHED-002) | Program Creation Form | Program must push to Priya's session screen within 30 seconds of save; must be available offline from Priya's device from last sync | J1 (child record + consent confirmed) → J2 |
| J3 | Post-Session Documentation | Session ends; Priya needs to document it; Dr. Sunita needs to review it | Priya (write), Dr. Sunita (review) | 19 | C1 (SNOTE-001–005, SOAP-001–004, TMPL-001–003, EMR-004), C2 (MPM-001, MPM-003), C4 (SCHED-004, WA-006) | Note Creation screen | Offline-first write: note saved to local storage immediately on save; syncs in background; no data loss on app close; last-write-wins conflict resolution on sync | J1 (consent), J2 (active program targets needed for Goals multi-select) → J3 |
| J4 | Progress Report Creation | Report cycle due; Dr. Sunita initiates or Rahul flags overdue | Dr. Sunita | 17 | C1 (SNOTE-003–005, SOAP-002–004, EMR-003–004, TMPL-004–005), C2 (MPM-003, MPM-005), C3 (RX-001–005), C4 (WA-001–006) | Progress Report Editor | Auto-population engine must aggregate session notes + SOAP Assessment/Plan sections across a date range in ≤ 3 seconds; PDF generation server-side ≤ 5 seconds | J3 (session notes and SOAP notes must exist as data source) → J4 |
| J5 | Billing & UPI Payments | End of billing cycle; invoices due for all active families | Rahul | 18 | C3 (INV-001–005, UPI-001–005), C4 (WA-003, WA-005, REMIND-003), C2 (INT-003), C1 (EMR-001–002) | Billing Dashboard — Outstanding tab | Invoice auto-generation cron reads confirmed attendance records (status = Present); idempotent UPI callback handler (suppress duplicate webhooks by transaction reference ID) | J6 (attendance must be captured digitally — no attendance data means no auto-invoice) → J5 |
| J6 | Scheduling & Attendance | Center director sets up weekly schedule; sessions run; Priya marks attendance | Rahul (schedule), Priya (attendance) | 17 | C4 (SCHED-001–005, REMIND-001–004, WA-003–004), C3 (INV-002, INV-001), C2 (MPM-001–003), C1 (SNOTE-001, TMPL-003) | Mark Attendance Screen | Offline-first attendance write: PATCH to local DB immediately; sync background; attendance confirmed event queued for billing module; haptic fires offline | J1 (child record + consent) → J6; J6 is the upstream data source for J5 (billing), J7 (dropout), and J4 (report attendance figures) |
| J7 | Missed Session & Dropout Prevention | Priya marks No-show; or system detects 2+ consecutive missed sessions | Rahul (action), System (detection) | 15 | C4 (SCHED-004, SCHED-005, REMIND-002, WA-004–005), C3 (INV-002, INV-005), C2 (MPM-003, MPM-005) | Center Director Dashboard (dropout risk view) | 30-minute delayed no-show follow-up job must be cancellable if Priya re-marks to Present before it fires; daily attendance gap scan cron; dropout risk flag recalculation on any attendance status change | J6 (attendance marking is the only trigger for dropout detection) → J7 |
| J8 | Analytics & Operational Reporting | Rahul opens app at week-start or month-end to review center performance | Rahul | 22 | C5 (PROG-001–005, ANLT-001–004, EXPORT-001–005), C3 (INV-004–005, UPI-004), C4 (REMIND-002), C2 (MPM-003, MPM-005) | Home Screen — Director view | All dashboard charts must be lightweight (CSS/canvas — no heavy chart library); all lists must render ≤ 3–4 seconds on 4G on a 2GB RAM Android; enrollment trend must render as an HTML table, not SVG chart | J5 (billing data), J6 (attendance data), J3 (session note data) must all exist before analytics has anything meaningful to show → J8 |
| J9 | DPDPA Consent Management | New child record created (consent gate activates); or parent exercises data subject rights | Rahul (consent capture), Meena (rights exercise) | 18 (Path A) + 15 (Path B-i/ii/iii) | C5 (DPDPA-001–005, AUDIT-001–003, RBAC-001–005), C2 (INT-003), C1 (EMR-001–002, SNOTE-001, TMPL-001, SOAP-001) | Erasure Review Screen (RPWD conflict decision) | All clinical write endpoints return HTTP 423 Locked when child consent status ≠ "active"; consent record must be written as immutable append-only (no UPDATE or DELETE endpoint); atomic: if AUDIT-001 write fails, consent write rolls back | **J9 is a prerequisite gate for every other clinical journey. It must ship before any clinical data can enter production.** |

---

### Journey Narratives — What Engineering Must Understand

**J1 — Child Enrollment & Onboarding**
Twenty steps across 4 clusters, but the critical path is steps 1–7: child record creation + DPDPA consent capture. Without confirmed consent, every clinical tab returns 423. The consent record is write-once and immutable — there is no UPDATE or DELETE endpoint for it, enforced at the schema level. Steps 8–13 (intake form + document upload) and step 14 (ABHA linking) are sequenceable into v1.1. Steps 15–20 (care team assignment + scheduling) are table stakes but not DPDPA-gated.

**J2 — Clinical Program Design**
The therapy program is the single most important read path on Priya's device. It must be available offline from the last sync — this is a hard offline requirement, not a fallback state. When Dr. Sunita saves a program update, a push event must reach Priya's session screen within 30 seconds. If Priya is in an active session at update time, the update banner must not force a refresh — it should offer a tap-to-refresh only.

**J3 — Post-Session Documentation**
The most technically constrained journey. The offline-first pattern here is a product requirement, not an infrastructure choice. Note saved to local DB immediately with sync_status=pending; background sync on connectivity restore; no data loss on app close. The co-sign action (SNOTE-003) requires active connectivity — it is an integrity requirement, not a bandwidth limitation. The SOAP note template is embedded in the app binary (not server-fetched) so it is always available offline.

**J4 — Progress Report Creation**
The auto-population engine is the highest-complexity feature in this journey. It aggregates session notes, SOAP Assessment/Plan sections, and program mastery events across a date range server-side. If this engine has nothing to aggregate (because Journey 3 adoption is low), every report section is empty and the time-saving value proposition collapses. The WhatsApp delivery path (Step 13) has three gates that must all pass: DPDPA consent active + parent WhatsApp opt-in confirmed + WABA connected. Any gate failure falls back to a secure shareable link.

**J5 — Billing & UPI Payments**
The auto-invoice generation at billing cycle end reads confirmed attendance records (status = Present only). This means J6 (attendance marking) must be live and generating reliable data before J5 auto-invoicing has meaningful input. The UPI callback handler must be idempotent — duplicate webhook calls from the payment gateway for the same transaction must be suppressed by checking the transaction reference ID before writing.

**J6 — Scheduling & Attendance**
The attendance mark (SCHED-004) is the most upstream data point in the entire system. It feeds J5 (billing), J7 (dropout detection), and J4 (report attendance figures). The ≤ 2-tap constraint from Priya's home screen to confirmed attendance mark is not a design aspiration — it is a launch criterion that must be QA-verified on a physical Redmi Note or Realme device. Offline write fires first; server sync is background.

**J7 — Missed Session & Dropout Prevention**
The 30-minute delayed follow-up job (REMIND-002) must be cancellable. If Priya re-marks a No-show to Present within 30 minutes (child arrived late), the queued job must be suppressed and the no-show counter decremented. The daily attendance gap scan runs server-side at end of day. Discharge is always a human decision — there is no auto-discharge trigger in the product. The "sort by last session" view is the simplest and most important feature in this journey — it converts invisible dropout into a visible, sorted list.

**J8 — Analytics & Operational Reporting**
All analytics data is downstream of clinical, attendance, and billing data. An empty dashboard is worse than no dashboard. This journey should not ship until J3, J5, and J6 are generating reliable data in production. All charts must use lightweight rendering — HTML tables for enrollment trends, CSS bars for revenue — no heavy SVG/canvas chart library. The monthly PDF export is a background job; the user must not wait on-screen for it.

**J9 — DPDPA Consent Management**
This is the most legally sensitive journey in the product. The 423-Locked response from every clinical write endpoint when consent_status ≠ "active" is enforced at the API layer, not the application layer. The atomic transaction pattern (consent write + audit log write succeed or both fail) is a schema-level constraint. The DPDPA/RPWD conflict at step B3-05 (erasure review) is a human decision point — engineering must surface it clearly and document Rahul's choice, but engineering must not resolve the legal conflict automatically. Consent cannot be captured offline — the server timestamp is the legally significant timestamp.

---

## Section 4: Technical Constraints — Non-Negotiables

These constraints are not preferences. Building against them is the difference between a product that works in Indian therapy session rooms and one that works in a San Francisco office.

---

### Device and Performance

- **Target device:** Redmi Note / Realme C series. 2–3 GB RAM, Android 10+, 5.5–6.5 inch screen. No iOS in Phase 1.
- **Attendance mark:** Write to local storage and haptic confirmation must complete in < 200ms (perceived instant). Background sync can be slower.
- **Dashboard charts:** All analytics screens must render within 4 seconds on a 4G connection on a 2GB RAM device.
- **List loads:** Caseload dashboards (up to 50 children) must load within 3 seconds on 4G.
- **Session note creation screen:** Must open in ≤ 1 second (SNOTE-001 NFR).
- **Program view (Priya):** Must load from cache in ≤ 1 second; from network in ≤ 2 seconds.
- **No heavy chart libraries:** All charts and data visualisations must use CSS, canvas, or styled HTML tables. SVG-heavy libraries cause jank on 2GB RAM Android. The 6-month enrollment trend in J8 is explicitly a styled HTML table, not a chart component.
- **Touch targets:** All interactive elements ≥ 44px. Attendance chips on the Mark Attendance screen ≥ 88px height (double the minimum — one-handed accuracy with a child present).

---

### Connectivity and Offline Behaviour

| Feature | Offline behaviour | Notes |
|---|---|---|
| Attendance marking (J6) | Write locally immediately; sync background | Hard offline requirement. Haptic fires offline. |
| Session note creation (J3) | Write to local DB with sync_status=pending; sync on restore | No data loss on app close. |
| Program view — Priya (J2/J3) | Full program text available from last sync cache | Hard offline requirement. "Showing cached program — last synced [date]" banner shown. |
| SOAP note draft (J3) | Draft saves to local storage; final Submit requires connectivity | No partial submit on connectivity loss. |
| DPDPA consent capture (J9) | Blocked offline — cannot be captured from an offline queue | Server timestamp is legally significant. |
| SOAP note co-sign (J3) | Blocked offline | Integrity requirement. |
| Invoice send (J5) | Blocked offline | Cannot transmit financial data without connectivity. |
| Progress report finalize (J4) | Draft saves locally; finalize requires connectivity | Same rule as SOAP submit. |
| Center calendar (J6) | Cached for up to 7 days | Schedule creation requires connectivity for conflict detection. |

**Pattern:** The write-locally-then-sync pattern is required for all in-session and post-session therapist actions. Sync on connectivity restore. No data loss on app close. Use background sync jobs, not foreground spinners.

---

### In-Session UX Constraints

Every constraint below applies to Priya's in-session workflow. These are QA-verified launch criteria, not design guidelines.

- **≤ 2 taps from Priya's home screen to confirmed attendance mark.** Verified on physical Redmi Note / Realme device. Path: (1) tap session card, (2) tap attendance chip.
- **One-handed operation.** All primary actions must be reachable with a right-hand thumb on a 6-inch screen. No critical actions requiring two hands.
- **Haptic feedback is mandatory on all confirmation actions.** Audio-only confirmation is not acceptable — session rooms are noisy.
- **No audio cues** for session-critical confirmations (attendance, note save). Haptic only.
- **Save button anchored at bottom of screen** on Note Creation. Reachable with thumb.
- **No forced refresh during an active session.** When Dr. Sunita pushes a program update, Priya sees an update banner she can choose to tap — not an auto-refresh that interrupts her session.

---

### Regulatory: DPDPA 2023 — Non-Negotiables

**HIPAA does not apply in India. Do not reference it. The governing law is DPDPA 2023.**

| Constraint | Implementation requirement |
|---|---|
| **Consent as API gate** | All clinical write endpoints return HTTP 423 Locked when child.consent_status ≠ "active". Enforced at API layer, not application layer. |
| **Atomic consent transaction** | POST /children/{id}/consent must write consent_record AND audit_log entry in a single atomic transaction. If AUDIT-001 write fails, consent write rolls back. No partial state. |
| **Consent is write-once** | No UPDATE or DELETE endpoint for consent_record. Schema-level block. New events (withdrawal, re-consent) are appended as separate immutable records. |
| **Server timestamp** | Consent cannot be captured offline. The server-confirmed timestamp (IST) is the legally significant record. |
| **Pre-checked consent is invalid** | The consent checkbox must never be pre-checked. Hard requirement. Affirmative action by the parent is required. |
| **Data localization** | All child health data stored on India-resident servers. This is a DPDPA 2023 Section 16 principle — not optional. |
| **Audit trail on all clinical data events** | AUDIT-001 must log: CREATE, UPDATE, DELETE, and ACCESS events on all child health data. Actor, timestamp, "DPDPA high-risk" flag for consent and erasure events. |
| **DPDPA/RPWD conflict — human sign-off required** | The erasure review screen (J9, B3-05) must surface the conflict between DPDPA erasure rights and RPWD Act 2016 retention obligations and present three options to Rahul. Engineering does not resolve this conflict automatically. |
| **Erasure means hard delete** | Soft-delete is not sufficient for a DPDPA erasure request. Clinical data must be removed from active storage. Only an anonymised erasure event record is retained. |
| **WhatsApp clinical data transmission** | Progress reports and session summaries must be sent via WhatsApp Business API (not personal WhatsApp). Parent must have active DPDPA consent AND active WhatsApp opt-in before transmission. |

**DPDPA Sprint 1 security baseline — these four stories must ship as a unit before any child health data enters production:**

```
RBAC-001 (role-based access control) →
AUTH-001 (2FA authentication) →
AUDIT-001 (immutable audit trail) →
DPDPA-001 (consent gate on all clinical write endpoints)
```

If any one of these is missing, child health data cannot legally or securely exist in the system.

---

## Section 5: Build Sequence and Dependencies

The question this section answers: "If we have to ship in phases, what must come first?"

---

### The Critical Dependency Chain

```
J9 (DPDPA consent)
  → J1 (Child enrollment — consent confirmed enables clinical data)
    → J6 (Scheduling & attendance — sessions exist, attendance is marked)
      → J3 (Session notes — sessions have a Present mark before notes can attach)
        → J4 (Progress reports — session notes + SOAP notes are the data source)
          → J5 (Billing — confirmed attendance records drive invoice auto-generation)
            → J7 (Dropout prevention — no-show marks from J6 are the signal)
              → J8 (Analytics — all upstream data must exist before dashboards are meaningful)
```

The attendance marking chain specifically:
```
J6 (attendance mark) → J5 (billing auto-invoice) + J7 (dropout flag) + J4 (report attendance figures)
```

All three downstream journeys read from the same attendance record. A missed or incorrect attendance mark creates errors in three places simultaneously.

---

### Phase 1 — Foundation: Must ship before anything else works

**This phase is not about features. It is about making the product legally and technically safe to hold any child health data.**

| Stories | Why non-negotiable |
|---|---|
| RBAC-001 (role-based access control) | No role enforcement = any staff member sees all child records. Privacy violation. |
| AUTH-001 (2FA authentication) | Single-factor auth on health data of minors is insufficient. |
| AUDIT-001 (immutable audit trail) | DPDPA accountability obligation requires logging every data access and modification. |
| DPDPA-001 (consent gate — 423 Locked pattern) | Without this, clinical data can be written for children without parental consent. |
| EMR-001 (child record creation) + EMR-002 (DPDPA consent in EMR) | The child record and consent confirmation are the foundation every other feature attaches to. |
| SCHED-001 (session scheduling) + SCHED-004 (attendance marking) | Attendance is the data source for billing, dropout, and progress reports. Must exist early. |

**Without Phase 1, Phase 2 cannot function because:** There is no legally safe data store for clinical records. Every clinical endpoint is either open (security failure) or non-existent (no product).

---

### Phase 2 — Core Clinical Value: What makes the product worth using

**This is the minimum viable product for therapist and supervisor adoption. If these features don't work, the entire proposition fails.**

| Journeys / Key stories | Why this phase |
|---|---|
| J2 — Clinical Program Design (TMPL-001–003, MPM-001–003, SOAP-001) | Priya needs the program on her phone before a session. Dr. Sunita needs to create it digitally. |
| J3 — Post-Session Documentation (SNOTE-001–003, SOAP-001–004) | Session notes are the data that makes every downstream feature work. |
| J1 — Child Enrollment completion (INT-001–004, MPM-001–005) | Intake form, document upload, and care team assignment complete the enrollment record. |
| J6 — Full attendance workflow (REMIND-001–002, WA-004) | Reminders reduce no-shows; no-show detection enables dropout detection. |

**Without Phase 2, Phase 3 cannot function because:** No session notes means no progress report auto-population. No digital attendance means no billing auto-generation. The operations and revenue features are data consumers — the clinical features are the data producers.

---

### Phase 3 — Operations and Revenue: What makes it sticky for the director

**Rahul pays for the product. These features are what justify the purchase decision.**

| Journeys | Why this phase |
|---|---|
| J5 — Billing & UPI Payments (INV-001–005, UPI-001–005) | Auto-invoice from attendance records. UPI payment link. Overdue reminders. |
| J4 — Progress Reporting (SNOTE-003–005, SOAP-002–004, RX-001–005, WA-001–006) | Auto-populated progress report. PDF export. WhatsApp delivery to Meena. |
| J7 — Dropout Prevention (REMIND-002, MPM-005 "sort by last session") | "Sort by last session" + no-show follow-up message is the MVP; full risk scoring is Phase 4. |

**Without Phase 3, Phase 4 cannot function because:** Analytics requires invoices, attendance records, and session notes to exist in production before dashboards have anything meaningful to render.

---

### Phase 4 — Intelligence and Compliance Depth

**These features are high value but depend on the data maturity established by Phases 1–3.**

| Journeys | Why deferred |
|---|---|
| J8 — Analytics & Operational Reporting (ANLT-001–004, PROG-001–005, EXPORT-001–005) | Dashboards are only useful once multiple billing cycles, attendance records, and session notes exist in production. An empty analytics dashboard is worse than no analytics. |
| J9 — Data Subject Rights (DPDPA-002–005, EXPORT-004) | Consent withdrawal, data portability, and the erasure/RPWD conflict flow are DPDPA obligations, but they are rarely exercised in the first 6–12 months of deployment. Phase 1 covers the consent capture gate; the data subject rights flows can follow. |
| Full dropout risk scoring (PROG-004 background job, configurable thresholds) | Requires multiple months of attendance data to produce meaningful signal. |

---

## Section 6: Open Questions for the Session

These are engineering decisions. The PM cannot answer them. We need engineering input to close them before or during sprint planning.

1. **Offline sync conflict resolution for session notes:** The current design specifies last-write-wins when a note edited offline syncs and a version exists on the server. Is there a more robust conflict resolution strategy we should consider, given that session notes are clinical records? What is the implementation cost of a merge or manual resolution approach versus last-write-wins?

2. **RBAC enforcement layer:** Should RBAC be enforced at the API layer (middleware on every endpoint), the application layer, or both? The 423 Locked consent pattern is API-layer-enforced. Should RBAC role checks follow the same pattern, or is there a reason to enforce at the application layer for some checks?

3. **DPDPA consent audit trail atomicity:** What is the most pragmatic implementation of the atomic transaction for consent write + AUDIT-001 write? Are we using a database transaction with a rollback? An outbox pattern? What happens if the audit log service is temporarily unavailable — does consent capture fail, or do we queue the audit event?

4. **WhatsApp Business API — Phase 1 dependency or Phase 3?** WABA setup requires Meta Business Manager verification, a dedicated business phone number, and template approval. This is non-trivial for a small center director. Can we stub WABA with SMS for Phase 2 (appointment reminders, no-show follow-up) and introduce full WABA for Phase 3 (invoice delivery, progress report delivery)? What breaks if we make that trade?

5. **Offline sync strategy for low-end Android:** What is the most pragmatic local storage strategy for low-end Android (2GB RAM, Android 10+)? SQLite, Room, or a simpler approach? How do we handle storage full errors gracefully in the session note creation flow without data loss?

6. **Push notification delivery for program updates:** The program update push to Priya (when Dr. Sunita saves a new program version) has a 30-second SLA. What is the realistic delivery latency for Firebase Cloud Messaging on a low-end Android in India, and should we design a polling fallback for when push notification delivery fails?

7. **UPI callback idempotency:** The UPI gateway may send duplicate callbacks for the same payment. The spec requires idempotent handling by checking the transaction reference ID. What is our preferred pattern — idempotency key at the database layer, or at the API gateway layer?

8. **Server-side PDF generation performance:** Progress reports and invoices both require server-side PDF generation. The target is ≤ 5 seconds for a single report. What tooling are we using (Puppeteer, WeasyPrint, other)? For progress reports auto-populated from a full year of session notes, is 5 seconds a realistic target or do we need a background job with a notification pattern for all cases?

---

## Section 7: Decisions Log

| # | Decision | Options considered | Decision made | Owner | By when |
|---|---|---|---|---|---|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |
| 6 | | | | | |
| 7 | | | | | |
| 8 | | | | | |

---

## Section 8: Parking Lot

Items raised during the session that need follow-up outside this meeting.

| # | Item | Raised by | Action required | Owner |
|---|---|---|---|---|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |
| 5 | | | | |

---

## Glossary — Clinical Terms for Non-Clinical Engineers

| Term | Plain-English definition |
|---|---|
| **ABA** | Applied Behavior Analysis — the therapy methodology used. Skill-building and behavior reduction through structured teaching. |
| **DTT (Discrete Trial Training)** | A structured, repetitive teaching method. Therapist gives an instruction, child responds, therapist records outcome (correct / incorrect / prompted) and repeats. |
| **NET (Natural Environment Teaching)** | Play-based, less structured ABA teaching. Less regimented than DTT. Growing use in Indian centers. |
| **SOAP Note** | A four-section clinical note format used by supervisors: Subjective (what was reported), Objective (what was observed), Assessment (clinical interpretation), Plan (what will be done). |
| **Program target / target behavior** | A specific skill being taught (e.g., "respond to own name") or behavior being reduced (e.g., frequency of self-injurious behavior). Each child has multiple targets. |
| **Prompt level** | How much assistance the therapist provides. Scale: Full Physical → Partial Physical → Gestural → Verbal → Independent. Fading prompts = reducing assistance as the child improves. |
| **Mastery criterion** | The performance threshold at which a target is considered mastered and the next phase begins (e.g., "4 out of 5 correct across 3 consecutive sessions"). |
| **Session note** | Post-session documentation by the therapist: what was worked on, child's response, incidents, next session focus. |
| **Home program** | Activities prescribed for parents to practice with the child between sessions. Different language and format from the clinical program — parent-friendly, no clinical jargon. |
| **RCI** | Rehabilitation Council of India — the statutory licensing body for special educators in India. The Indian equivalent of the US BACB. |
| **BCBA** | Board Certified Behavior Analyst — a US clinical credential. Rare in India (fewer than ~500 in the country). Our primary clinical staff are RCI-licensed, not BCBA-certified. |
| **DPDPA 2023** | India's Digital Personal Data Protection Act, 2023. The governing data privacy law for this product. Not HIPAA (US law). Not GDPR (EU law). DPDPA 2023. |
| **RPWD Act 2016** | Rights of Persons with Disabilities Act 2016 — Indian law that creates documentation obligations for individualized therapy programs for children with disabilities. This law is in tension with DPDPA erasure rights (see J9, B3-05). |
| **UDID** | Unique Disability ID — a government-issued disability certificate. Centers often need to document this at intake for compliance purposes. |
| **ABHA / ABDM** | Ayushman Bharat Health Account — India's national health ID system. ABDM is the broader digital health infrastructure. Linking a child's ABHA ID to their center record is an optional feature in Phase 2+. |
| **Maladaptive behavior** | Problem behaviors being reduced through therapy — e.g., self-harm, aggression, tantrums. These are tracked by frequency per session. |
| **Co-sign** | A supervisor's action to review and digitally sign off on a therapist's session note, creating an immutable clinical record. Requires active connectivity (integrity requirement). |
| **Caseload** | The list of children assigned to a specific therapist or supervisor. Priya sees her caseload. Dr. Sunita sees her supervision caseload. |

---

*Document prepared by: PM*
*Source documents: `/products/autism-therapy-platform/research/journey-map.md`, journeys 01–09, clusters 1–5*
*Date: April 20, 2026*
