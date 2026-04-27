# Prioritisation Analysis: Impact vs Effort Matrix

**Product:** Autism Therapy Platform (India)
**Author:** Product Consultant
**Date:** 2026-04-14
**Stage:** Discovery — no features built
**Input:** Three problem areas surfaced through secondary research

---

## 1. Impact vs Effort Matrix

### Scoring Methodology

**Impact** is scored across three dimensions:
- Clinical value — does solving this improve the quality of therapy delivered to the child?
- Commercial pull — does solving this drive revenue, retention, or adoption leverage?
- Regulatory necessity — does the product create or close a compliance risk?

**Effort** is scored across three dimensions:
- Build complexity — how technically and informationally complex is the solution?
- Adoption friction — how much behaviour change is required from end users?
- Validation risk — how much of what we currently believe is still unconfirmed assumption?

Each problem is rated High / Medium / Low on each axis, with rationale.

---

### Problem 1: In-Session Data Collection

**Impact: HIGH**

- Clinical value is the highest of the three problems. Real-time trial-by-trial recording is a structural clinical requirement in ABA — retrospective recording degrades accuracy in a documented, measurable way. This is not a convenience improvement; it is the foundation of clinically defensible therapy delivery.
- Commercial pull is high because this feature is used in every session, every day, by every therapist. Daily utility drives daily habit, which drives retention and word-of-mouth. It is also the feature most invisible to center directors but most felt by clinical staff — who are the make-or-break adoption variable. If therapists adopt it, the product survives. If they don't, nothing else matters.
- Regulatory necessity is moderate — there is no specific DPDPA 2023 trigger for in-session data collection itself, but it generates the structured clinical records that satisfy RPWD Act 2016 documentation obligations.

**Effort: MEDIUM**

- Build complexity is moderate. The core interaction model is well-established (tap-to-record, one-handed, offline-first). This is a solved design problem in the US market. The challenge is not novel engineering — it is constraint-aware execution: low-end Android performance, offline sync, and an onboarding experience that works for non-technical therapists without a training session.
- Adoption friction is the most significant effort variable. This requires therapists to change their in-session behaviour — the highest-stakes moment of their professional day. Paper is low-friction; a new mobile app is not. However, if the interaction is genuinely ≤ 2 taps and works offline, friction drops significantly. The design must earn adoption, not assume it.
- Validation risk is medium. The clinical case for real-time recording is established. The open assumption is whether Indian special educators experience the current workflow as painful enough to change — this requires primary research but is the most narrowly scoped assumption of the three problems.

**Summary: HIGH impact, MEDIUM effort. Best ratio of the three.**

---

### Problem 2: Patient Enrollment and Intake

**Impact: MEDIUM**

- Clinical value is real but indirect. A well-structured intake reduces the gap between assessment results and program design, and reduces early dropout. But the clinical value accrues over weeks, not sessions — and it is harder to attribute to a specific tool.
- Commercial pull is lower than Problem 1. The buyer (center director) recognises intake as chaotic, but it is not their most acute daily pain. It doesn't recur every session. DPDPA 2023 compliance is a meaningful differentiator — but enforcement is still nascent and most directors may not yet perceive it as urgent risk.
- Regulatory necessity is the strongest of the three problems here. DPDPA 2023 requires verifiable parental consent for processing health data of minors. Every center that stores digital records is technically non-compliant without a formal consent mechanism. This will matter more as enforcement develops, but it is a genuine and growing risk, not a theoretical one.

**Effort: HIGH**

- Build complexity is the highest of the three problems. A full intake module involves: inquiry tracking, developmental history collection, assessment-to-program handoff, UDID documentation support, consent capture, and scheduling integration. Each of these is its own workflow with its own edge cases and data model.
- Adoption friction is high because intake involves multiple roles (admin, senior therapist, parent) and changes a process that currently spans multiple tools and conversations. It requires the center to commit to a new workflow at the most critical trust moment with a new family.
- Validation risk is the highest of the three problems. The number of open assumptions is substantial: whether center directors perceive intake software as worth paying for; whether DPDPA compliance urgency is felt; what the actual step-by-step intake workflow looks like at Indian centers; what the drop-off rate from inquiry to enrollment is. We do not have enough evidence to define the right scope without primary fieldwork.

**Summary: MEDIUM impact, HIGH effort. Poor ratio. High assumption load.**

---

### Problem 3: Treatment Plans, Billing, and Follow-Up Reminders

**Impact: MEDIUM-HIGH** (but internally fragmented — the three sub-problems are not equal)

- The appointment reminder sub-problem has the strongest evidence base of any finding across all three problem areas. The data is striking and directly translatable: no-show rates drop from 39% (no reminder) to 3% (live contact). Revenue and clinical continuity impact is immediate and measurable.
- Treatment plan documentation burden is real and quantified globally (2–3 hours/day, reducible to 30–60 minutes). But whether this manifests at similar scale in Indian centers is unvalidated — Indian centers likely have less formal documentation requirements than US insurance-driven practices, meaning the burden may be lower and the willingness to pay for a solution correspondingly lower.
- Billing is the weakest sub-problem commercially. Fee collection in small Indian centers is a relationship act, not an administrative one. Directors are unlikely to pay for software that automates a social dynamic they manage personally through WhatsApp. The risk of building a billing feature that doesn't fit the actual social context of Indian fee collection is high.

**Effort: HIGH** (because the three sub-problems require separate solutions bundled together)

- Build complexity is highest of the three problems if pursued as a bundle. Treatment plan authorship, billing workflows, and appointment reminders are architecturally distinct. Bundling them increases scope risk without a clear user who owns all three.
- Adoption friction is high for treatment plan authorship (requires clinical workflow change at the supervisor level, not the therapist level) and for billing (requires centers to surface financial data in a new system). Appointment reminders are the exception — low friction, high impact, high autonomy once set up.
- Validation risk is significant. The core assumptions around documentation burden in Indian centers, the social dynamics of billing, and whether directors experience these as a unified problem are all unvalidated. The bundling of three distinct problems under one label is itself a scope risk.

**The bundling is the problem.** Appointment reminders as a standalone feature would score HIGH impact, LOW effort — it is a focused, evidence-backed intervention with a clear success metric and minimal adoption friction. As part of a treatment-plan-billing-reminders bundle, it gets dragged into high-effort territory unnecessarily.

**Summary: MEDIUM-HIGH impact if scoped to reminders only; HIGH effort as currently framed. Needs decomposition.**

---

### Matrix Summary

| Problem | Impact | Effort | Net Priority | Key caveat |
|---------|--------|--------|--------------|------------|
| In-Session Data Collection | HIGH | MEDIUM | **First** | Requires primary research to validate adoption willingness |
| Patient Enrollment and Intake | MEDIUM | HIGH | Third | High assumption load; high regulatory upside long-term |
| Treatment Plans, Billing, Follow-Up | MEDIUM-HIGH (fragmented) | HIGH (as bundle) | Second (if decomposed) | Appointment reminders alone would be high-priority; billing is a trap |

---

## 2. Prioritisation Recommendation

**Build in-session data collection first.**

The case is not complicated:

This is the only problem where the end user and the make-or-break adoption variable are the same person. If a special educator uses this tool during live sessions, the product survives. If they don't, the product fails regardless of what else is built. Everything downstream — supervisor review, progress reports, treatment plan updates, parent communication — depends on structured session data existing in the first place. Data collection is the foundational layer. Build it first or there is nothing to build on.

The interaction model is proven. One-handed, offline-first, tap-to-record ABA data collection is a design pattern with years of market validation in the US. The design challenge is execution within Indian device and context constraints — not invention. This reduces technical risk substantially compared to the other two problems.

The gap is real and unoccupied. No India-specific therapist-side data collection tool exists. TherapEZ is general practice management. Cognitivebotics is child-facing. The market is genuinely open.

The effort-to-impact ratio is the best of the three. MEDIUM effort against HIGH impact, with a narrower assumption set than either alternative.

**Do not attempt all three problems.** This is a 5–20 person team buying from a small business with thin margins. The willingness-to-pay signal is unvalidated. A product that tries to solve intake, billing, data collection, treatment plans, and reminders simultaneously will take 18 months to ship, will never get clinical staff adoption, and will not find product-market fit. The question is not "which features does our platform need?" — it is "what is the smallest thing that creates real clinical value and proves the product can be adopted?"

**Appointment reminders are the one exception worth noting.** The evidence for their impact is stronger than any other single finding in this research. If there is a fast-follow-on feature after data collection, a lightweight attendance tracking and WhatsApp reminder integration is a strong candidate — narrow, evidence-backed, and commercially meaningful to center directors.

---

## 3. Scope Brief: In-Session Data Collection

**Target user:** Special Educator / Behavior Therapist — an RCI-licensed clinician delivering ABA-based therapy to a child with autism during a live, structured session. Typically 22–35 years old, works at a small Indian therapy center, uses a low-to-mid-range Android device, is not highly tech-savvy, and currently records session data on paper or not at all.

**Job to be done:** When I am running a live therapy session with a child, I want to record trial outcomes, frequency counts, and behavioral observations in real time, so that my clinical supervisor can review accurate data and adjust the therapy program — and so I am not reconstructing sessions from memory at the end of the day.

**Success metric (90 days):** At least 70% of active therapist users log data in-app during live sessions (not retrospectively) on at least 4 out of 5 working days — as measured by session timestamp metadata within a 10-minute window of scheduled session start.

---

### In Scope

- **DTT trial recording (correct / incorrect / prompted)** — because this is the highest-frequency data collection task in ABA sessions. If we nail this one interaction, the product has daily utility. Everything else is secondary.
- **Frequency / event counting** — because it is a one-tap interaction with immediate clarity; high frequency of use across maladaptive behavior tracking.
- **Duration timer (start / stop)** — because it is structurally required for behavioral data such as tantrum duration or time-on-task; single-tap with visual confirmation.
- **Offline-first data capture with background sync** — because sessions cannot pause for connectivity. This is non-negotiable, not a nice-to-have.
- **Session summary view (read-only)** — because the therapist needs to close a session with a confirmation that data was captured; this is the minimum viable feedback loop.
- **Child and therapy target setup (minimal, supervisor-configured)** — because the therapist must be able to select the child and the active program targets before a session; supervisors set these up, not therapists.
- **Haptic feedback on tap confirmation** — because session environments are noisy; visual and audio feedback alone are insufficient.

### Out of Scope (this phase)

- **ABC data collection (Antecedent-Behavior-Consequence)** — deferred because this is cognitively demanding, often done retrospectively, and is a second-order workflow. Adding it to MVP increases session-time cognitive load without proportionate clinical return at this stage.
- **Task analysis step-tracking** — deferred because it requires a more complex data model and is used for specific skill types; not universal enough for an MVP across all centers.
- **Interval / time-sampling recording** — deferred; less common in Indian ABA practice and requires a more complex timing interface.
- **Supervisor program design and target management (full UI)** — deferred; supervisors can configure targets via a minimal admin interface or import. Full program management is Phase 2.
- **Progress graphing and data visualisation** — deferred; clinically valuable but a downstream consumer of data, not a data collection tool. A supervisor-facing reporting module is Phase 2.
- **Parent-facing session summaries** — deferred; requires trust in data quality first. Premature until data collection is adopted and reliable.
- **Multi-language UI (Hindi, regional languages)** — deferred to Phase 2; English-only UI is an [ASSUMPTION] for metro markets at launch. Must be validated with primary research before committing to deferral.
- **Billing integration** — out of scope entirely for this feature. Do not combine.
- **iOS support** — deferred; Android-first given device reality of Indian clinical staff.

---

### MVP Recommendation

A mobile-first Android application that allows a special educator to: select a child from a pre-configured list, select an active therapy target within that child's program, and record DTT trial outcomes (correct / incorrect / prompted) via single large tap-targets — all while holding a physical object with their other hand, with no internet connection required.

This is the entire MVP. It must work offline, it must sync automatically when connectivity returns, it must confirm each tap with haptic feedback, and it must allow a therapist to open and close a session in under 30 seconds of active navigation.

**Why this is the right MVP:**
- It validates the single most critical assumption — that Indian special educators will change their in-session recording behaviour if the tool is genuinely lower-friction than paper.
- It creates data that has clinical value the moment it exists — supervisors can see session trends in aggregate even before progress reporting or graphing features are built.
- It is narrow enough to build in 6–8 weeks and test with real therapists in real sessions.
- It does not require solving intake, billing, or treatment plan authorship before it delivers value.

---

### Top Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Special educators do not find current paper-based workflow painful enough to change in-session behaviour | H | H | Primary fieldwork with 6–8 therapists before sprint 1. Observe a live session. Do not build until we have watched at least 5 therapists record data in context. |
| Onboarding failure — therapists cannot get from install to first session data without support | H | H | Invest disproportionately in first-run experience. Target: zero training required for a therapist to log their first trial within 5 minutes of install. Test this with non-technical users before launch. |
| Low-end Android performance causes lag on tap — destroys session-time usability | M | H | Test on minimum-spec Android device (2GB RAM, Android 10) from day one of development. Do not optimize for high-end devices. |
| Offline sync failure causes data loss — destroys trust permanently | M | H | Architect local-first from the start; sync is secondary. Never show "saving..." — show "saved" only when data is confirmed local. Sync happens silently in background. |
| Center directors do not see enough value in data collection alone to pay for a subscription — commercial signal is weak | M | H | Frame early pilots as partially subsidised or paid-in-kind for feedback. Willingness-to-pay is not validated; do not assume it. |
| Supervisor-side target configuration is too burdensome — therapists arrive at sessions with no targets to record against | M | M | Build supervisor target setup as a simple, structured admin flow. Pre-populate with common ABA target libraries for Indian clinical contexts. |
| DPDPA 2023 consent for storing child clinical data digitally is not obtained at enrollment — creates liability before data collection even begins | M | H | Lightweight DPDPA-compliant parental consent capture must be part of child setup, even before a full intake module exists. This is a dependency, not a separate feature. |

---

### Open Questions Before Building

- [ ] Do RCI-licensed special educators in Indian centers record data during live sessions at all — and if so, in what format and at what frequency? (Primary fieldwork required — observe sessions, do not ask.)
- [ ] Which data types (DTT trials, frequency counts, duration, ABC) are actually captured versus routinely skipped or approximated? What gets recorded last and least accurately?
- [ ] Is the pain of current recording experienced as a clinical quality problem, a personal burden, or neither? What is the frame?
- [ ] What does "one-handed" actually mean in a live Indian therapy session context — what is the therapist's other hand doing?
- [ ] What is the connectivity situation in the session rooms at 10–15 real Indian centers? Is offline-first a hard requirement or a precaution?
- [ ] How do supervisors currently consume session data — at what frequency, in what format, for what decisions? What is the feedback loop today?
- [ ] What is the minimum viable target configuration burden that a supervisor would accept as part of setup? How structured are current therapy programs?
- [ ] Who actually pays for the product — center director, individual therapist, center trust? What is the payment relationship and the price tolerance?
- [ ] [DPDPA dependency] Is there an existing parental consent mechanism at any center for digital data storage? What does it look like today?

---

### What Would Need to Be True to Succeed

- Indian special educators must experience in-session paper recording as disruptive enough to their clinical work that a simpler alternative is worth a behaviour change during live sessions — the most cognitively demanding moment of their day.
- The interaction model must be genuinely faster and lower-friction than paper for the two or three highest-frequency data types. If it is not, it will not survive contact with a live session.
- Offline-first sync must be flawless. A single data-loss incident at an early center will end the pilot and damage referral reputation in a small, relationship-driven market.
- At least one clinical supervisor per center must actively use session data to inform program decisions — otherwise the data collection creates effort without visible clinical return for the therapist, and adoption collapses.
- Center directors must perceive structured session data as worth paying for — either because it saves supervisors' time, demonstrates clinical credibility to parents, or reduces their compliance risk. Willingness-to-pay at Indian price points is currently an open assumption.
- The product must get through a full working day in a real session environment — noise, one-handed use, low-end hardware — without breaking, lagging, or losing data.

---

## 4. What This Means for the Other Two Problems

### Patient Enrollment and Intake — Deferred, with one dependency carved out

Deferred as a full feature. The assumption load is too high, the scope is too large, and the build complexity is not justified before the clinical data collection layer is validated.

However, one element of intake cannot be fully deferred: **DPDPA 2023 parental consent for digital data storage**. The moment we store a child's clinical session data digitally, we need verifiable parental consent. This is not a future compliance concern — it is a precondition of shipping. A minimal consent capture mechanism (documented digital consent, stored against the child's record) must be built as a dependency of the in-session data collection MVP. It is not a full intake module. It is a single, clearly scoped workflow.

Full intake — inquiry tracking, assessment-to-program handoff, UDID documentation support, enrollment analytics — should not be scoped until primary research has been conducted with at least 5–8 center directors and the in-session data collection MVP has been piloted at 2–3 centers.

### Treatment Plans, Billing, and Follow-Up — Decomposed and partially deferred

**Billing:** Out of scope for the foreseeable future. The evidence suggests fee collection in Indian centers is a relationship act, not an administrative process. Building a billing tool that doesn't fit the social dynamics of how Indian center directors actually collect fees from financially stressed families risks building the wrong thing confidently. This requires significant primary research before any scoping begins.

**Treatment plan documentation:** Deferred until session data exists. Treatment plan generation is downstream of data collection — you cannot automate progress reporting without structured session data to report on. This is a natural Phase 2 feature once the data collection layer is adopted and stable.

**Appointment reminders:** The strongest near-term candidate after data collection. The evidence is striking (39% no-show vs. 3% with live contact), the commercial value to center directors is immediate and tangible, and the interaction model is simple: structured attendance tracking with WhatsApp-native reminder triggers. This is a strong candidate for Phase 2 scoping — but only after in-session data collection is validated. It requires the center director persona to adopt the product, not the therapist — making it architecturally and commercially distinct from the MVP.

Do not pursue all three sub-problems simultaneously. Decompose them and prioritise sequentially.

---

> **What would need to be true for this to succeed?**
>
> Special educators must find recording session data on paper or WhatsApp painful enough — clinically, not just administratively — that they will change their behaviour during a live therapy session. The product must be so low-friction that a non-technical therapist, holding a child's attention with one hand, does not have to think about the tool at all. And at least one person per center — a supervisor or director — must actively use the data that results, so therapists see clinical feedback that makes their effort feel worthwhile. Without that feedback loop, adoption will not sustain beyond the first two weeks.
