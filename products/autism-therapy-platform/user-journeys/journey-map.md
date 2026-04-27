# User Journey Map: Full Therapy Center Lifecycle
**Product:** Autism Therapy Platform (India)
**Author:** Product Manager Agent
**Date:** 2026-04-14
**Evidence base:** Secondary research only (desk research, live web searches, peer-reviewed literature — April 2026). No primary fieldwork has been conducted.
**Stage:** Discovery

---

## 🔄 Scope Revision — 22 April 2026

> **Updated:** 2026-04-22T00:00:00+05:30 | Engineering Alignment Meeting

Following the engineering alignment session on 22 April 2026, the MVP scope for the platform has been revised. This journey map reflects the original 9-journey model (including in-session data collection). The table below documents which journeys are in scope for the MVP and which are deferred.

| Journey | Original scope | MVP status | Decision rationale |
| --- | --- | --- | --- |
| J1 — Child Enrollment and Intake | In | ✅ **In scope** | Core to onboarding; reusable EMR components available |
| J2 — Clinical Program Design | In | ❌ **Deferred — post-MVP** | Therapy-specific; requires net-new build |
| J3 — Session Notes / Clinical Notes | In | ✅ **In scope** | Clinical documentation; reusable components available |
| J4 — Progress Reports | In | ❌ **Deferred — post-MVP** | Therapy-specific reporting; requires net-new build |
| J5 — Billing | In | ✅ **In scope** | Core to center operations; reusable components available |
| J6 — Scheduling and Attendance | In | ✅ **In scope** | Core to center operations; reusable components available |
| J7 — Dropout Prevention | In | ✅ **In scope** | Operational workflow; reusable components available |
| J8 — Analytics Dashboard | In | ✅ **In scope** | Center visibility; reusable components available |
| J9 — DPDPA Consent Management | In | ✅ **In scope** | Hard regulatory gate; must ship before any child health data enters the system |
| In-Session Data Collection | Out | ❌ **Out of scope — India MVP** | No reimbursement driver in Indian out-of-pocket market; future opportunity for US/international |

**Strategic implication:** The MVP will function as a **clinical management tool** rather than a therapy-specific platform. J2 (program design) and J4 (progress reports) — the most clinically differentiated features — require primary research validation before being confirmed as safe to defer. If research shows they are adoption blockers for therapists, this decision must be revisited before scope is locked.

**Open action:** Product to run primary research with therapy centers to validate whether deferring J2 and J4 creates an adoption blocker. See meeting summary: `meetings/engineering/2026-04-22-engineering-alignment-meeting-summary.md`

---

> All elements carry an evidence label: ✅ Observed (primary research / direct quotation from source) | 🔵 Inferred (logical derivation from observed data) | 🔶 [HYPOTHESIS] (assumed; not yet validated in Indian therapy center context)
> ⚠️ DPDPA — applied to any step involving digital storage or transmission of child health data (minors' data under DPDPA 2023 requires verifiable parental consent)

---

## Part 1 — Persona Definitions

### Persona 1: Priya — Special Educator / Behavior Therapist

| Attribute | Detail | Evidence |
| --- | --- | --- |
| Role | Front-line therapist delivering ABA and skill-building sessions (1:1 with child) | ✅ CLAUDE.md product context |
| Certification | RCI-licensed Special Educator (B.Ed Special Education ASD or equivalent). Not a BCBA — that credential is rare in India (<500 nationwide) | ✅ Secondary research — Action For Autism, CLAUDE.md |
| Core job-to-be-done | When running a live therapy session, she wants to accurately log what the child did during every trial, so she can give her supervisor evidence-based data to adjust the program | 🔵 Inferred from ABA clinical literature |
| Primary device | Low-to-mid-range Android smartphone (e.g., Redmi, Realme); paper data sheets during sessions | 🔶 [HYPOTHESIS] — device type not confirmed by primary research in Indian therapy setting; consistent with broader India workforce data |
| Tech comfort | Moderate — comfortable with WhatsApp, basic Android apps. Not familiar with clinical software. 🔶 [HYPOTHESIS] lacks structured training in digital data collection tools | 🔶 [HYPOTHESIS] — inferred from SAGE Journals assistive technology review noting training gap |
| Key pain today | Records trial data on paper during sessions → transcribes to Excel or WhatsApp → supervisor sees data days later. Paper creates transcription errors, illegible notes, and delayed feedback loops | 🔵 Inferred — paper failure modes documented globally; India-specific confirmation pending primary research |
| Relationship to others | Reports to Clinical Supervisor (Priya's programs are designed by supervisor). Interacts with parents post-session informally. Coordinates with Center Director on scheduling | 🔵 Inferred from center org structure |
| Evidence gaps | Whether she records data in-session at all in Indian context, which data types she captures, whether she experiences the workflow as painful enough to change | Gaps identified in secondary research |

---

### Persona 2: Dr. Sunita — Clinical Supervisor / Senior Therapist

| Attribute | Detail | Evidence |
| --- | --- | --- |
| Role | Senior clinical staff who designs therapy programs, supervises junior special educators, and writes progress reports for families | ✅ CLAUDE.md product context |
| Certification | Senior RCI-licensed professional; may hold BCBA (rare) or a postgraduate qualification (M.Ed Special Education, M.Phil) | 🔵 Inferred from RCI regulatory structure and CLAUDE.md |
| Core job-to-be-done | When reviewing a child's progress, she wants to see accurate session data quickly, so she can update the therapy program and write a meaningful progress report without spending evenings reconstructing what happened | 🔵 Inferred from ABA supervisor workflow literature |
| Primary device | Laptop or desktop for report writing; Android smartphone for WhatsApp-mediated communication | 🔶 [HYPOTHESIS] — not confirmed by primary research |
| Tech comfort | Moderate to high — likely familiar with basic office tools (Word, Excel, Google Docs). May use WhatsApp Groups for coordination | 🔶 [HYPOTHESIS] |
| Key pain today | Data from junior therapists arrives in inconsistent formats (paper, WhatsApp photos, verbal briefings). Report writing takes significant uncompensated time — potentially 2–3 hours/day for documentation tasks globally; Indian equivalent unvalidated | 🔶 [HYPOTHESIS] — 2–3 hour figure from ABA Matrix (US context); whether this applies to Indian centers is unconfirmed |
| Relationship to others | Manages Priya (junior therapist). Reports to Center Director. Primary clinical contact for parents when concerns arise | 🔵 Inferred |
| Evidence gaps | Actual time spent on documentation, whether she distinguishes treatment plan authorship from progress report writing as separate burdens, how she receives session data from junior staff | Gaps identified in secondary research |

---

### Persona 3: Rahul — Center Director / Founder

| Attribute | Detail | Evidence |
| --- | --- | --- |
| Role | Runs the center operationally and often also provides clinical care. Economic buyer for any software decision. Wears clinical, administrative, and commercial hats simultaneously | ✅ CLAUDE.md product context |
| Certification | Often a clinician who founded the center — may hold RCI license or BCBA (rare). Administrative role is self-taught | 🔵 Inferred from "founder-led by a therapist" description in product context |
| Core job-to-be-done | When managing the center day-to-day, he wants to know which children attended, which payments are outstanding, and whether his staff are delivering quality therapy — so he can run a financially sustainable center without drowning in admin | 🔵 Inferred from product context and billing/follow-up research |
| Primary device | Likely Android smartphone as primary; laptop for Excel-based records | 🔶 [HYPOTHESIS] |
| Tech comfort | Variable — some founders are tech-forward, most are not. Likely power-user of WhatsApp for coordination | 🔶 [HYPOTHESIS] |
| Key pain today | No unified system — uses WhatsApp, Excel, paper files, and verbal coordination simultaneously. Cannot see at a glance which families owe fees or which children are at dropout risk. Fee conversations are uncomfortable and often delayed | 🔵 Inferred from product context and billing research |
| Relationship to others | Employs Priya and Dr. Sunita. The commercial relationship owner with families. The person who would purchase and implement any new tool | ✅ Product context for buyer role; 🔵 inferred for purchase decision dynamic |
| Evidence gaps | Willingness-to-pay at Indian price points, what business metrics he actually tracks today, whether he tracks enrollment pipeline at all | Gaps in secondary research |

---

### Persona 4: Meena — Parent / Primary Caregiver

| Attribute | Detail | Evidence |
| --- | --- | --- |
| Role | Mother (or primary caregiver — often grandmother or aunt in extended family arrangements). Responsible for bringing child to sessions, paying fees, and implementing home programs | ✅ CLAUDE.md product context; 🔵 extended family structure inferred from Indian caregiving literature |
| Certification | None — lay caregiver | N/A |
| Core job-to-be-done | When her child is in therapy, she wants to understand what progress he is making and what she should be doing at home, so she can feel useful rather than helpless and know whether the investment is working | 🔵 Inferred from caregiver burden research and parent engagement findings |
| Primary device | Android smartphone; WhatsApp is primary communication channel | ✅ WhatsApp role confirmed by multiple secondary sources |
| Tech comfort | Variable — WhatsApp-fluent; likely not comfortable with clinical platforms or formal apps requiring login | 🔶 [HYPOTHESIS] — no primary data on parent tech behavior in Indian autism therapy context |
| Key pain today | Receives clinical reports in formats she does not understand. Updates happen via WhatsApp informally — no structured view of progress. Arrived at therapy after a long, exhausting diagnostic journey; is emotionally vulnerable and financially stretched | ✅ "Families quietly withdraw under cumulative strain" (Tandfonline 2025); caregiver burden data from NJCM India |
| Relationship to others | Primary source of fee revenue for Rahul. Receives progress information from Dr. Sunita. Implements home programs created by Dr. Sunita | 🔵 Inferred |
| Evidence gaps | Whether she wants structured digital updates (vs. preferring WhatsApp informality), willingness to engage with a parent-facing portal, language preferences | Gaps in secondary research |

---

### Persona 5: Arjun — The Child (Therapy Recipient)

> Arjun is not a software user but his developmental profile and behavioral presentation directly shape the physical constraints of every other persona's workflow. He is included as a context anchor.

| Attribute | Detail | Evidence |
| --- | --- | --- |
| Profile | Child aged 3–12 with autism diagnosis; active or dysregulated during sessions; may not tolerate interruptions from the therapist | 🔵 Inferred from ABA clinical context |
| Relevance to product design | His presence in the session room is the reason in-session data collection must be one-handed, haptic, and non-interruptive. Any step that requires Priya to break eye contact or pause the interaction is a break point | ✅ One-handed design requirement is confirmed design standard in ABA data collection literature |

---

## Part 2 — End-to-End Journey Map

> One connected journey seen through multiple persona lenses. Trigger: family first contacts the center. End state: child is enrolled in ongoing therapy with consistent attendance, data-driven program updates, and family engagement.
>
> **MVP scope key:** ✅ **IN SCOPE — MVP** | ❌ **OUT OF SCOPE — MVP** (deferred post-MVP or India-specific exclusion)
>
> **Journey order rationale:** DPDPA consent (Journey 0) gates all data entry and must precede enrollment. Scheduling (Journey 3) is set up at enrollment and runs in parallel with all clinical journeys thereafter. Out-of-scope journeys are preserved in full for post-MVP planning.

---

### Journey 0 — DPDPA Consent Management
**Journey:** J9 | ✅ **IN SCOPE — MVP** | *Regulatory prerequisite — gates all subsequent data entry*

**What starts this journey:** The center adopts a digital system and needs to store any child personal or health data. Under DPDPA 2023, verifiable parental consent is a legal prerequisite before the first record is created.

#### Steps

| # | Action | Actor | Tool / Channel | Evidence |
| --- | --- | --- | --- | --- |
| 1 | Staff inform the parent what personal and health data will be collected, how it will be stored, and what it will be used for | Rahul / admin | Verbal + written notice | ✅ DPDPA 2023 Section 5 — notice must precede consent |
| 2 | Parent reads consent notice and gives explicit, informed consent — ideally in their preferred language | Meena | Digital consent screen / written form | ✅ DPDPA 2023 Section 6 — consent must be free, specific, informed, and unconditional |
| 3 | Consent record created with timestamp, version, and scope of consent ⚠️ DPDPA | System | Secure digital record | ✅ DPDPA 2023 — consent must be auditable; verifiable consent for minors' data is a hard legal requirement |
| 4 | Consent status visible to clinical staff — no child data entry permitted until consent is on record | System | Platform gate | 🔵 Inferred from compliance requirement |
| 5 | Parent informed of their right to withdraw consent at any time and the effect of withdrawal on data retention | Rahul / admin | Verbal + consent notice | ✅ DPDPA 2023 Section 6(4) — right to withdraw must be communicated at time of consent |
| 6 | Consent records retained for the duration of data processing and available for regulatory audit | System | Secure storage | ✅ DPDPA 2023 — data fiduciary must maintain auditable consent records |

**Emotional state:**
- Meena: Trust is not yet established at this journey. Consent language must be plain and accessible — clinical or legal jargon will cause passive non-engagement rather than refusal. 🔵 Inferred from caregiver trust and health literacy literature
- Rahul: Likely unfamiliar with DPDPA requirements — will experience this as friction unless it is embedded naturally into the intake flow rather than presented as a separate compliance step. 🔶 [HYPOTHESIS]

**Pain points & friction:**
- Indian autism therapy centers currently have no DPDPA-compliant consent process — paper consent forms (where they exist) do not reference digital data processing ⚠️ DPDPA 🔶 [HYPOTHESIS]
- Staff have no training on DPDPA requirements for processing minors' health data 🔶 [HYPOTHESIS]
- No mechanism for consent withdrawal in any current workflow — once data is in a system, no deletion protocol exists 🔵 Inferred gap

**Why this journey is first:** Every subsequent journey involves creating, storing, or processing a child's personal or health data. DPDPA 2023 makes parental consent a legal prerequisite. This cannot be a post-launch addition.

---

### Journey 1 — Family Inquiry & First Contact
**Journey:** J1 | ✅ **IN SCOPE — MVP**

**What starts this journey:** Parent hears about the center through word of mouth, a paediatrician referral, or a parent WhatsApp group.

#### Steps

| # | Action | Actor | Tool / Channel | Evidence |
| --- | --- | --- | --- | --- |
| 1 | Parent sends a WhatsApp message or makes a phone call to the center asking about therapy availability | Meena | WhatsApp / phone call | ✅ WhatsApp as primary contact channel confirmed across multiple secondary sources |
| 2 | Center Director or reception staff receives inquiry and responds | Rahul / admin | WhatsApp / phone | 🔵 Inferred from center structure |
| 3 | Basic details are noted — child's name, age, diagnosis, contact number | Rahul / admin | Paper notebook or WhatsApp chat itself | 🔶 [HYPOTHESIS] — no structured lead capture tool exists; inquiry details likely remain in WhatsApp thread |
| 4 | An initial appointment is scheduled verbally or via WhatsApp | Rahul / admin | WhatsApp | 🔵 Inferred — consistent with WhatsApp-mediated operations |
| 5 | No formal confirmation or reminder is sent (unless staff remember to do it) | — | — | 🔶 [HYPOTHESIS] — no reminder system documented in any Indian center; consistent with informal operations |

**Emotional state:**
- Meena: Anxious, hopeful, exhausted from a long diagnostic journey. High emotional stakes — this contact matters. ✅ Supported by Tandfonline 2025 research on caregiver emotional burden at entry into services
- Rahul: Pragmatic — this is a new enrollment opportunity. 🔵 Inferred

**Pain points & friction:**
- Inquiry details are captured in a WhatsApp thread or paper note with no structured record — information is easily lost 🔶 [HYPOTHESIS]
- No pipeline visibility: Rahul has no way to see how many families are in inquiry vs. enrolled state 🔶 [HYPOTHESIS]
- No automated follow-up if the family does not respond to the appointment invite 🔶 [HYPOTHESIS]

**Workarounds:**
- Staff rely on memory and WhatsApp scroll history to follow up on warm leads 🔶 [HYPOTHESIS]
- Some centers may use a WhatsApp Business label to tag "new inquiry" families 🔶 [HYPOTHESIS]

---

### Journey 2 — Intake & Enrollment
**Journey:** J1 | ✅ **IN SCOPE — MVP**

**What starts this journey:** Family arrives for initial visit / intake appointment.

#### Steps

| # | Action | Actor | Tool / Channel | Evidence |
| --- | --- | --- | --- | --- |
| 1 | Family arrives; child is observed informally by senior therapist or director | Dr. Sunita / Rahul | In-person | 🔵 Inferred |
| 2 | Developmental history interview with parents | Dr. Sunita | Paper form or verbal conversation | 🔶 [HYPOTHESIS] — format of history intake not confirmed for Indian centers specifically |
| 3 | Prior documentation collected: diagnosis report, school records, previous therapy reports, UDID card if applicable ⚠️ DPDPA | Rahul / admin | Physical paper / photocopies | ✅ Documentation types confirmed by India Autism Center UDID guide; ⚠️ collecting and storing health records of a minor requires verifiable parental consent under DPDPA 2023 |
| 4 | Fee structure and schedule explained to family | Rahul | Verbal / WhatsApp | 🔶 [HYPOTHESIS] — no formal fee document or signed agreement documented in Indian center context |
| 5 | Consent form signed for therapy | Rahul / admin | Paper | 🔶 [HYPOTHESIS] — existence and quality of consent forms in Indian centers not confirmed; DPDPA-compliant digital consent not yet documented anywhere in Indian center context ⚠️ DPDPA |
| 6 | Child's record created in the center's system | Admin / Rahul | Paper file / Excel spreadsheet | 🔵 Inferred from "patchwork of WhatsApp, Excel, and paper" product context description |
| 7 | First assessment session scheduled | Dr. Sunita / Rahul | WhatsApp / verbal | 🔵 Inferred |

**Emotional state:**
- Meena: Overwhelmed and emotionally raw. Needs to feel heard and to trust the center. This is often the first time someone has presented a structured plan for her child. ✅ Tandfonline 2025 — "caregivers must repeatedly demonstrate patience and compliance to secure support"
- Dr. Sunita: Professional, focused on clinical picture. May feel rushed if intake appointment is squeezed between clinical sessions. 🔶 [HYPOTHESIS]
- Rahul: Commercially aware — converting an inquiry to enrollment. Also carrying compliance awareness about documentation requirements. 🔶 [HYPOTHESIS]

**Pain points & friction:**
- No standardized intake protocol in India — process varies center to center and staff to staff ✅ PMC research: "There is no standardized protocol or critical pathway"
- Documentation collected ad hoc — staff remember to ask for some documents but not others 🔶 [HYPOTHESIS]
- DPDPA 2023 compliance risk: collecting and digitizing child health records of minors without verifiable parental consent ⚠️ ✅ DPDPA 2023 Section 9 confirmed; compliance gap in Indian centers is 🔶 [HYPOTHESIS]
- Fee agreement often verbal — no signed document creates ambiguity later 🔶 [HYPOTHESIS]
- Enrollment drop-off: some families who complete intake never return for first therapy session 🔵 Inferred — consistent with "dropout begins at enrollment" finding and Indian access barriers

**Workarounds:**
- Staff rely on experience to remember what to collect — no checklist exists 🔶 [HYPOTHESIS]
- UDID documentation is produced retrospectively when families request it, rather than captured at intake 🔶 [HYPOTHESIS]

---

### Journey 3 — Scheduling & Attendance Management
**Journey:** J6 | ✅ **IN SCOPE — MVP**

**What starts this journey:** A child is enrolled and sessions need to be scheduled. This journey repeats weekly throughout the child's active enrollment and is the primary data source for billing and dropout detection.

#### Steps

| # | Action | Actor | Tool / Channel | Evidence |
| --- | --- | --- | --- | --- |
| 1 | Center director or admin creates the weekly schedule — assigning children to therapists and time slots | Rahul / admin | Paper register / Excel / verbal coordination | 🔵 Inferred from "no single system" product context |
| 2 | Schedule communicated to therapists | Rahul → Priya, Dr. Sunita | WhatsApp message or verbal briefing | 🔶 [HYPOTHESIS] — schedule distribution method not confirmed |
| 3 | Appointment reminder sent to parent before the session | Rahul → Meena | WhatsApp (manual) / nothing | 🔶 [HYPOTHESIS] — no automated reminder system documented in Indian therapy center context |
| 4 | On session day, therapist marks attendance for each child — present, absent, or cancelled ⚠️ DPDPA | Priya / Rahul | Paper attendance register | 🔵 Inferred; paper attendance register is the documented source of truth for billing in Indian centers |
| 5 | If child is absent, reason is noted if known (illness, travel, financial, no response) | Rahul / Priya | Paper note / WhatsApp message | 🔶 [HYPOTHESIS] — whether absence reason is systematically recorded is unconfirmed |
| 6 | Attendance data used at month end to calculate billing for each family | Rahul | Paper register → manual Excel calculation | 🔵 Inferred from billing journey dependency (J5) |
| 7 | Attendance pattern reviewed (if reviewed at all) to identify children at dropout risk | Rahul | Memory / manual scan of paper register | 🔶 [HYPOTHESIS] — no structured dropout signal derived from attendance in current workflow |

**Emotional state:**
- Rahul: Schedule management is a daily operational overhead — managing changes, cancellations, and no-shows informally is a persistent context switch. 🔶 [HYPOTHESIS]
- Priya: Last-minute schedule changes and unclear therapist assignments disrupt session preparation. 🔶 [HYPOTHESIS]
- Meena: Absence of proactive appointment reminders increases missed sessions — WhatsApp-based reminder is expected but not guaranteed. 🔵 Inferred from no-show rate research

**Pain points & friction:**
- Scheduling managed in paper or Excel — no real-time visibility for staff or parents 🔵 Inferred
- Therapist assignment is verbal — coverage gaps appear when a therapist is absent and no contingency is documented 🔶 [HYPOTHESIS]
- Attendance marked on paper — data not available in real time for billing or dropout detection 🔵 Inferred
- No automated session reminder to parents — no-show rate is directly tied to reminder presence ✅ Psychiatric Services: 39% no-show without reminder vs. 3% with live contact
- Absence reason rarely captured — center cannot distinguish unavoidable absence from early-stage disengagement 🔶 [HYPOTHESIS]
- **Critical design constraint:** Attendance mark is the highest-frequency data entry action in the platform. Must be ≤ 2 taps on a low-end Android device and must function offline. ✅ Platform constraint defined in CLAUDE.md product context

**Workarounds:**
- WhatsApp group message used for daily schedule updates — informal, no audit trail 🔶 [HYPOTHESIS]
- Paper attendance registers serve as the billing source of truth at month end 🔵 Inferred
- Some centers send a WhatsApp reminder manually the day before each session 🔶 [HYPOTHESIS]

---

### Journey 4 — Clinical Program Design
**Journey:** J2 | ❌ **OUT OF SCOPE — MVP**

> **Decision date:** 22 April 2026 | **Rationale:** Therapy-specific feature requiring net-new build; existing EMR components cannot be reused. Deferred to post-MVP. | **Deferred to:** Post-MVP release
>
> **Adoption risk:** Clinical program design is the core clinical value proposition for supervisors and therapists. Deferring this means the MVP launches without the features most likely to matter to clinical staff. If primary research confirms J2 is an adoption blocker, this decision must be revisited before scope is locked. See: `meetings/engineering/2026-04-22-engineering-alignment-meeting-summary.md`
>
> *Content below preserved in full for post-MVP planning.*

---

**What starts this journey:** Child's baseline assessment is complete. Clinical Supervisor designs the individualized therapy program.

#### Steps

| # | Action | Actor | Tool / Channel | Evidence |
| --- | --- | --- | --- | --- |
| 1 | Standardized assessment conducted across 1–3 sessions (ISAA, CARS, Vineland, functional behavior assessment) ⚠️ DPDPA | Dr. Sunita | Paper assessment forms | ✅ Assessment tools named in intake research; paper format is 🔵 inferred |
| 2 | Assessment data compiled into a baseline profile | Dr. Sunita | Paper / Word document / Excel | 🔶 [HYPOTHESIS] — format not confirmed for Indian centers |
| 3 | Program targets selected across domains: communication, social skills, adaptive behavior, academics, maladaptive behaviors | Dr. Sunita | Paper / Word | 🔵 Inferred from ABA treatment plan content literature |
| 4 | Individualized therapy program written ⚠️ DPDPA | Dr. Sunita | Paper / Word document | 🔶 [HYPOTHESIS] — treatment plan formality and structure varies; no India-standard template documented |
| 5 | Program communicated to junior therapist (Priya) who will deliver sessions | Dr. Sunita → Priya | Verbal briefing / paper handover | 🔶 [HYPOTHESIS] — handover mechanism not confirmed; verbal briefing with paper copy is probable based on tool constraints |
| 6 | Program communicated to parents | Dr. Sunita / Rahul → Meena | Verbal / WhatsApp summary | 🔶 [HYPOTHESIS] — no formal parent program handover documented in Indian context |
| 7 | First therapy session scheduled | Rahul | WhatsApp / verbal | 🔵 Inferred |

**Emotional state:**
- Dr. Sunita: This is the core clinical work — likely engaged and invested. Pressure point is time: assessment + program design competes with ongoing clinical caseload 🔶 [HYPOTHESIS]
- Meena: Anxious to understand the plan. May not fully comprehend clinical terminology used in verbal explanation 🔵 Inferred from caregiver burden research — educational gaps noted
- Priya: Receives program; may ask clarifying questions. 🔶 [HYPOTHESIS] Level of handover clarity varies

**Pain points & friction:**
- Assessment data captured on paper — not readily usable for trend tracking or report generation 🔵 Inferred
- Program design-to-therapist handover gap: if the briefing is verbal, Priya may misremember prompt levels or reinforcement schedules 🔶 [HYPOTHESIS]
- Parent communication of the program is informal — Meena leaves without a clear written summary of what is being worked on and why 🔶 [HYPOTHESIS]
- No structured home program document produced at this journey 🔶 [HYPOTHESIS]
- RPWD Act 2016 mandates documentation of individualized programs — but no structured format or filing system confirmed in small Indian centers ✅ RPWD Act cited; compliance gap is 🔶 [HYPOTHESIS]

**Workarounds:**
- Some supervisors maintain personal program binders per child — not shared across staff 🔶 [HYPOTHESIS]
- Parents receive WhatsApp voice notes summarizing the program 🔶 [HYPOTHESIS]

---

### Journey 5 — Ongoing Therapy Sessions (In-Session Data Collection)
**Journey:** In-Session Data Collection | ❌ **OUT OF SCOPE — India MVP**

> **Decision date:** 22 April 2026 | **Rationale:** Indian therapy is paid out-of-pocket. No insurance reimbursement system creates an external driver for trial-by-trial data logging. In-session digital data collection is a strong differentiator for US and international markets where insurance authorization requires granular clinical documentation — but this does not apply to Indian centers at this stage. | **Deferred to:** US / international market expansion
>
> **Long-term note:** This is the foundational break point identified in the original journey analysis — every downstream feature (supervisor review, progress reports, billing accuracy) depends on the quality of data captured here. The MVP accepts this limitation by design. Monitor primary research for signal on whether Indian centers are willing to adopt in-session digital data collection even without a reimbursement driver.
>
> *Content below preserved in full for future planning.*

---

**What starts this journey:** Priya arrives at the session room with the child. Session begins.

#### Steps

| # | Action | Actor | Tool / Channel | Evidence |
| --- | --- | --- | --- | --- |
| 1 | Priya retrieves child's data sheet for the session — paper form with current program targets listed | Priya | Paper data sheet | 🔵 Inferred from global ABA paper data collection standard; India-specific confirmation pending |
| 2 | Session begins — Priya runs discrete trials (DTT) or naturalistic teaching (NET) activities with the child | Priya | In-person with child | ✅ DTT and NET described as primary teaching methods in Indian ABA context |
| 3 | For each trial, Priya marks outcome on the paper sheet: correct (✓), incorrect (✗), or prompted (P) | Priya | Paper / pen | 🔵 Inferred — trial-by-trial recording is the documented ABA standard |
| 4 | Simultaneously tracks frequency of maladaptive behaviors using tally marks | Priya | Paper data sheet | 🔵 Inferred from ABA data collection literature |
| 5 | If a maladaptive behavioral episode occurs, notes antecedent and consequence in margin (ABC data) | Priya | Paper | 🔵 Inferred — ABC data is often retrospective due to cognitive load |
| 6 | At session end, Priya writes a brief session note (what was covered, child's mood, any incidents) | Priya | Paper / WhatsApp message to supervisor | 🔶 [HYPOTHESIS] — whether a formal session note exists or whether this is a verbal debrief is unconfirmed |
| 7 | Paper data sheet is placed in the child's physical file or handed to supervisor | Priya | Physical paper | 🔵 Inferred |
| 8 | Supervisor reviews paper data — typically in batch, not same-day | Dr. Sunita | Paper / occasional Excel transcription | 🔶 [HYPOTHESIS] — review frequency not confirmed; research suggests paper creates 1–2 week review delays |

**Emotional state:**
- Priya during session: Fully focused on the child — data collection is secondary to session management. Feels the tension between giving full attention to the child and accurately recording outcomes. 🔵 Inferred from "one-handed constraint" documented in US ABA literature; applies structurally to any therapist doing live data collection
- Priya post-session: Relief. Possibly rushed — next child may be waiting. 🔶 [HYPOTHESIS]
- Dr. Sunita reviewing data: Frustrated by illegibility, inconsistent formats, missing entries. 🔵 Inferred from documented paper failure modes

**Pain points & friction:**
- One-handed constraint: marking paper while managing a child's activity with the other hand is physically awkward and causes data entry errors 🔵 Inferred from ABA clinical context and global design standard
- Retrospective ABC data: the antecedent is often forgotten by session end — ABC notes are incomplete or inaccurate 🔵 Inferred from clinical documentation literature
- Paper illegibility: "unclear handwriting that often occur with paper systems" — transcription errors compound ✅ ResearchGate peer-reviewed comparison study on electronic vs. paper DTT data collection
- Delayed supervisor feedback: with paper, supervisor "may be able to analyze data only every one or two weeks" ✅ BHCOE research
- Connectivity unknown: if a mobile tool were introduced, session room connectivity may be unreliable — making offline-first a likely hard requirement 🔶 [HYPOTHESIS]
- No automatic graph or trend generation from paper data — supervisor must manually plot or calculate progress 🔵 Inferred

**Workarounds:**
- Some therapists write abbreviated tally codes they alone understand — reducing transcription time but creating handover risk 🔶 [HYPOTHESIS]
- WhatsApp photo of paper data sheet sent to supervisor as a shortcut to physical handover 🔶 [HYPOTHESIS] ⚠️ DPDPA — photo of child's clinical data sent via WhatsApp is unencrypted transmission of minor's health data
- Retrospective session note written from memory at day end, not in-session 🔶 [HYPOTHESIS]

---

### Journey 6 — Session Notes / Clinical Notes
**Journey:** J3 | ✅ **IN SCOPE — MVP**

**What starts this journey:** A therapy session ends. The therapist needs to document what happened before seeing the next child.

#### Steps

| # | Action | Actor | Tool / Channel | Evidence |
| --- | --- | --- | --- | --- |
| 1 | Session ends — child leaves the session room | Priya | — | — |
| 2 | Therapist writes a post-session note covering: activities covered, child's engagement and mood, any behavioral incidents, observations to flag to supervisor | Priya | Paper / WhatsApp message to supervisor | 🔶 [HYPOTHESIS] — whether a structured post-session note is written (vs. verbal debrief) not confirmed for Indian centers |
| 3 | Session note submitted or communicated to supervisor | Priya → Dr. Sunita | Paper handover / WhatsApp | 🔵 Inferred |
| 4 | Supervisor reviews session notes — may add clinical observations, flag concerns, or mark as reviewed | Dr. Sunita | Paper / WhatsApp reply | 🔶 [HYPOTHESIS] — whether supervisors review individual session notes (vs. only batch data review) not confirmed |
| 5 | Clinical concerns identified in notes (behavioral incidents, regression) escalated to director if required | Dr. Sunita → Rahul | Verbal / WhatsApp | 🔶 [HYPOTHESIS] |
| 6 | Session notes archived as part of the child's clinical record ⚠️ DPDPA | Admin | Paper file / no system | 🔵 Inferred — session notes are rarely systematically archived in Indian centers; most remain in a physical file or disappear into WhatsApp threads |

**Emotional state:**
- Priya: Post-session note writing feels like administrative overhead — next child may already be waiting. Documentation motivation is low when the benefit (supervisor review, program update) is delayed by days or weeks. 🔶 [HYPOTHESIS]
- Dr. Sunita: Without structured session notes, her understanding of each session depends on Priya's verbal recall — which degrades quickly. Inconsistent note quality makes clinical decisions harder. 🔵 Inferred from documentation literature
- Rahul: Session notes are invisible to the director in the current workflow — no aggregated view of what is happening clinically across the center. 🔶 [HYPOTHESIS]

**Pain points & friction:**
- No standard template for session notes — quality and completeness vary by therapist and by day 🔶 [HYPOTHESIS]
- Notes written on paper accumulate in a physical file with no search, filter, or trend analysis capability 🔵 Inferred
- WhatsApp-based session notes ⚠️ DPDPA — unencrypted transmission of child clinical data to supervisor's personal device 🔶 [HYPOTHESIS]
- Note writing competes with next session preparation — rushed or missed entries are common 🔶 [HYPOTHESIS]
- Session notes are the data foundation for progress reports (J4, deferred post-MVP) — without structured digital notes, progress reporting cannot be semi-automated 🔵 Inferred structural dependency

**Workarounds:**
- Therapists send a WhatsApp voice note to supervisor instead of writing — reduces friction but creates an unstructured, unarchived record ⚠️ DPDPA 🔶 [HYPOTHESIS]
- End-of-day summary note written from memory covering all sessions — compressed and retrospective 🔶 [HYPOTHESIS]

---

### Journey 7 — Supervisor Review & Program Updates
**Journey:** J2 (extension) | ❌ **OUT OF SCOPE — MVP**

> **Decision date:** 22 April 2026 | **Rationale:** Deferred as part of J2 (Clinical Program Design). Structured program update workflows require a digital program management system to exist first. | **Deferred to:** Post-MVP release
>
> **Note:** Supervisor review of individual session notes (J3) is in scope for MVP. What is deferred is the structured clinical workflow of modifying targets, prompt levels, reinforcement schedules, and program versions in a digital record.
>
> *Content below preserved in full for post-MVP planning.*

---

**What starts this journey:** Dr. Sunita sits down to review session data — typically weekly or fortnightly.

#### Steps

| # | Action | Actor | Tool / Channel | Evidence |
| --- | --- | --- | --- | --- |
| 1 | Collects paper data sheets from Priya's physical file or reads WhatsApp photos of data sheets | Dr. Sunita | Paper / WhatsApp | 🔶 [HYPOTHESIS] — collection method not confirmed for Indian centers |
| 2 | Manually calculates percentage correct per target across sessions | Dr. Sunita | Mental arithmetic / calculator / Excel | 🔶 [HYPOTHESIS] — whether any calculation tool is used is unconfirmed |
| 3 | Plots or reads trends — is the child making progress, plateauing, or regressing on each target? | Dr. Sunita | Paper graph / Excel chart | 🔶 [HYPOTHESIS] |
| 4 | Identifies targets that have reached mastery criteria — marks for next phase (fading prompts, generalizing to new contexts) | Dr. Sunita | Paper / verbal | 🔵 Inferred from ABA program management literature |
| 5 | Identifies targets where child is not progressing — modifies procedure, prompt level, or reinforcer | Dr. Sunita | Paper / new program sheet | 🔵 Inferred |
| 6 | Updates the therapy program — adds new targets, removes mastered ones, modifies procedures | Dr. Sunita | Paper / Word | 🔶 [HYPOTHESIS] — update frequency and format not confirmed |
| 7 | Communicates program changes to Priya | Dr. Sunita → Priya | Verbal briefing / paper | 🔶 [HYPOTHESIS] |
| 8 | Supervision session documented (if at all) | Dr. Sunita | Paper / nothing | 🔶 [HYPOTHESIS] — whether supervision meetings are formally documented in Indian centers is unknown |

**Emotional state:**
- Dr. Sunita: Cognitively taxed — this is complex analytical work done in fragmented time, often outside clinical hours 🔶 [HYPOTHESIS]
- Priya: Uncertain about program changes until explicitly told — may continue running outdated targets if communication breaks down 🔶 [HYPOTHESIS]

**Pain points & friction:**
- Manual calculation of progress metrics is time-consuming and error-prone 🔵 Inferred from ABA Matrix documentation burden finding
- 2–3 hours/day on documentation in non-automated practices (US figure) — Indian equivalent unvalidated but likely directionally true 🔶 [HYPOTHESIS] ✅ Source: ABA Matrix
- Review happens in batch — a child may be running an outdated program target for 1–2 weeks before supervisor notices ✅ BHCOE: "supervisor can analyze data only every one or two weeks" with paper
- Program update communication to Priya is verbal — high risk of being misapplied or misremembered 🔶 [HYPOTHESIS]
- No version history for the therapy program — what was the target prompt level 4 weeks ago? 🔵 Inferred as a structural gap

**Workarounds:**
- Some supervisors maintain handwritten "master notebooks" per child with program versions — a single point of failure 🔶 [HYPOTHESIS]
- Verbal "stand-up" at start of day to communicate program changes — relies on memory and attendance 🔶 [HYPOTHESIS]

---

### Journey 8 — Progress Reporting to Parents
**Journey:** J4 | ❌ **OUT OF SCOPE — MVP**

> **Decision date:** 22 April 2026 | **Rationale:** Therapy-specific reporting requiring net-new build. Depends on structured session data and digital program records — both of which depend on deferred features (J2, in-session data collection). Cannot be built meaningfully without the upstream data chain. | **Deferred to:** Post-MVP release
>
> **Adoption risk:** Progress reports are the primary evidence families see of clinical value. Without structured reporting, parent engagement and retention may be harder to sustain at MVP. Monitor in primary research.
>
> *Content below preserved in full for post-MVP planning.*

---

**What starts this journey:** Monthly or quarterly progress report is due, or a parent requests an update.

#### Steps

| # | Action | Actor | Tool / Channel | Evidence |
| --- | --- | --- | --- | --- |
| 1 | Dr. Sunita compiles session data across the reporting period | Dr. Sunita | Paper files / Excel if transcribed | 🔵 Inferred |
| 2 | Writes progress narrative per domain — what was worked on, what progress was made, what remains challenging | Dr. Sunita | Word document / paper | 🔶 [HYPOTHESIS] — format and regularity of Indian center progress reports unconfirmed |
| 3 | Report is printed and given to family at the center, or sent as a WhatsApp PDF ⚠️ DPDPA | Dr. Sunita / admin | Paper / WhatsApp | 🔶 [HYPOTHESIS] — delivery mechanism not confirmed ⚠️ DPDPA — sending child health report via WhatsApp is unencrypted transmission |
| 4 | Family meeting (verbal) to explain the report | Dr. Sunita / Rahul | In-person / phone call | 🔶 [HYPOTHESIS] — whether a family meeting accompanies the report is not confirmed |
| 5 | Home program updated and communicated to Meena | Dr. Sunita → Meena | Verbal / WhatsApp voice note | 🔶 [HYPOTHESIS] |
| 6 | Parent asked to sign off or acknowledge receipt | — | Paper / nothing | 🔶 [HYPOTHESIS] — formal acknowledgement unlikely in current workflows |

**Emotional state:**
- Dr. Sunita: Report writing is effortful and competes with clinical time — likely experienced as administrative burden 🔶 [HYPOTHESIS] (supported directionally by 2–3 hours/day documentation figure)
- Meena: Wants to understand what progress her child has made. Report language may be too clinical; she may not know what questions to ask. ✅ Product context: "Receives clinical reports they don't understand"
- Rahul: Progress reports are a retention tool — families who see clear progress are more likely to continue. 🔵 Inferred

**Pain points & friction:**
- Report writing starts from scratch every reporting cycle — no carry-forward from previous reports or auto-population from session data 🔵 Inferred as structural gap
- Report language is often inaccessible to lay parents 🔶 [HYPOTHESIS] — no Indian data available; consistent with global finding that clinical documents are poorly understood by families
- Reports are sent via WhatsApp — unencrypted channel for sensitive child health data ⚠️ DPDPA 🔵 Inferred from WhatsApp-dominant communication pattern
- Home program instructions given verbally — Meena may not remember what to practice 🔶 [HYPOTHESIS]
- No structured mechanism for parents to ask questions or confirm understanding 🔶 [HYPOTHESIS]

**Workarounds:**
- Some supervisors dictate key points to parents verbally rather than relying on written reports 🔶 [HYPOTHESIS]
- WhatsApp voice notes used to explain report contents informally 🔶 [HYPOTHESIS]

---

### Journey 9 — Billing & Fee Collection
**Journey:** J5 | ✅ **IN SCOPE — MVP**

**What starts this journey:** End of month, or as per center's billing cycle (some centers bill per session, some monthly).

#### Steps

| # | Action | Actor | Tool / Channel | Evidence |
| --- | --- | --- | --- | --- |
| 1 | Rahul (or admin) tallies sessions delivered for each child from paper attendance register | Rahul | Paper register / Excel | 🔵 Inferred from "Excel and paper" tool landscape |
| 2 | Invoice amount calculated | Rahul | Mental arithmetic / Excel | 🔶 [HYPOTHESIS] |
| 3 | Fee reminder sent to family | Rahul | WhatsApp message | ✅ WhatsApp as billing channel consistent with all secondary research describing cash-pay, WhatsApp-mediated India billing context |
| 4 | Payment collected — cash, UPI transfer, or bank transfer | Meena | Cash / UPI (GPay, PhonePe) | 🔵 Inferred — UPI is dominant in Indian cash transactions |
| 5 | Payment recorded in center register | Rahul / admin | Paper receipt / Excel | 🔶 [HYPOTHESIS] — no structured billing software documented for Indian therapy centers |
| 6 | Overdue follow-up: if family hasn't paid, Rahul sends a second message or calls | Rahul | WhatsApp / phone | 🔶 [HYPOTHESIS] |
| 7 | Fee waiver or extension negotiated informally for financially stressed families | Rahul | Verbal / WhatsApp | 🔵 Inferred from Indian therapy context and "financially stressed families" research finding |

**Emotional state:**
- Rahul: Asking families for money is uncomfortable — especially when he knows the family is financially stretched. Likely delays these conversations. 🔶 [HYPOTHESIS] (pattern documented in small Indian private health practices analogously)
- Meena: Financial stress is documented. Fee reminder may trigger anxiety or disengagement. ✅ Tandfonline 2025: "financial pressures" as driver of "invisible exits"

**Pain points & friction:**
- No automated payment reminder — Rahul must manually track who has paid and who hasn't 🔵 Inferred from absence of structured billing tool
- Session count for billing depends on paper attendance records that may be inconsistent 🔶 [HYPOTHESIS]
- Fee conversations are relationship-sensitive — delayed or avoided, leading to receivables piling up 🔶 [HYPOTHESIS]
- No financial dashboard: Rahul cannot see at a glance monthly revenue, outstanding fees, or collection rate 🔵 Inferred from "no single system" product context
- Evidence base for structured reminders reducing no-shows: 39% no-show (no reminder) vs. 3% (live call) ✅ Psychiatric Services study — directly applicable to appointment reminders; fee payment reminder ROI is 🔵 inferred analogy

**Workarounds:**
- WhatsApp status used to post payment deadline reminders — indirect, non-confrontational 🔶 [HYPOTHESIS]
- Some centers require advance payment to avoid collection awkwardness 🔶 [HYPOTHESIS]
- Excel with conditional formatting used to track outstanding balances 🔶 [HYPOTHESIS]

---

### Journey 10 — Appointment Follow-Up & Dropout Prevention
**Journey:** J7 | ✅ **IN SCOPE — MVP**

**What starts this journey:** A family misses a session, attendance frequency drops, or a child has not been seen for 2+ weeks.

#### Steps

| # | Action | Actor | Tool / Channel | Evidence |
| --- | --- | --- | --- | --- |
| 1 | Staff notices a child's absence — through memory or a gap in the physical schedule | Priya / Rahul | Memory / paper schedule | 🔶 [HYPOTHESIS] — no automated absence detection documented in Indian center context |
| 2 | WhatsApp message sent to family: "Is everything okay? Arjun missed his session today" | Rahul / Priya | WhatsApp | 🔶 [HYPOTHESIS] — single follow-up message is the likely default |
| 3 | Family responds — reason given (illness, travel, financial pressure, competing family event) | Meena | WhatsApp | 🔵 Inferred |
| 4 | Session rescheduled or not (no formal reschedule protocol) | Rahul | WhatsApp / verbal | 🔶 [HYPOTHESIS] |
| 5 | If family goes quiet for 2+ weeks, dropout is effectively accepted without formal intervention | Rahul | — | 🔶 [HYPOTHESIS] — "dropout is experienced as an outcome, not a process failure" consistent with absence of tracking systems |
| 6 | No attendance trend analysis — center has no way to see which children are at dropout risk based on attendance patterns | — | — | 🔵 Inferred from "no single system" landscape |

**Emotional state:**
- Meena (if dropping out): Exhausted, financially strained, possibly ashamed. "Invisible exit" — she may simply stop responding to WhatsApp messages. ✅ Tandfonline 2025 — "invisible exits" is a documented phenomenon in Indian autism care
- Rahul: Dropout feels inevitable rather than preventable — because there's no system to surface it early 🔶 [HYPOTHESIS]
- Dr. Sunita: May not be aware a child has dropped out until the schedule reveals a persistent gap 🔶 [HYPOTHESIS]

**Pain points & friction:**
- No systematic attendance tracking — dropout is invisible until it has already happened 🔵 Inferred
- Single WhatsApp message is insufficient as a dropout intervention — evidence suggests live contact reduces no-shows dramatically ✅ Psychiatric Services: 3% no-show with live call vs. 39% with no reminder
- Dropout driven by financial pressure and caregiver exhaustion — not addressable by reminders alone ✅ Tandfonline 2025 and PMC research on caregiver burden
- No structured re-engagement protocol: what happens if a family returns after a gap? Does the program need updating? 🔶 [HYPOTHESIS]

**Workarounds:**
- Staff informally "check in" on families they're close to — relationship-based retention only 🔶 [HYPOTHESIS]
- Some centers WhatsApp parent groups where community pressure informally encourages continued attendance 🔶 [HYPOTHESIS]

---

### Journey 11 — Analytics Dashboard
**Journey:** J8 | ✅ **IN SCOPE — MVP**

**What starts this journey:** Center director needs operational visibility — attendance, billing, and dropout risk — without assembling data manually from paper and Excel.

#### Steps

| # | Action | Actor | Tool / Channel | Evidence |
| --- | --- | --- | --- | --- |
| 1 | Director opens the dashboard — sees center-level summary: active children, sessions delivered today, attendance rate this week | Rahul | Platform dashboard | 🔵 Inferred — the inverse of what exists today; "no single system" is the current state |
| 2 | Reviews billing status: invoices sent this month, outstanding balances, overall collection rate | Rahul | Platform dashboard | 🔵 Inferred from billing pain point (J5) |
| 3 | Reviews attendance trends per child — flags children with declining attendance as dropout risk candidates | Rahul | Platform dashboard | 🔵 Inferred — feeds J7 Dropout Prevention workflow |
| 4 | Reviews staff utilization: sessions delivered vs. scheduled capacity per therapist | Rahul | Platform dashboard | 🔵 Inferred from center operations context |
| 5 | Identifies children overdue for a session or without an upcoming scheduled appointment | Rahul | Platform dashboard | 🔵 Inferred as structural gap in current workflow |
| 6 | Exports summary data for external compliance reporting (RPWD Act documentation, government scheme records) if required | Rahul | Platform export | 🔶 [HYPOTHESIS] — specific export format and compliance reporting requirements for Indian centers not confirmed |

**Emotional state:**
- Rahul: Currently operating on intuition and retrospective data — problems are discovered after they have already escalated. A real-time dashboard is a qualitative shift in how the center is managed. 🔵 Inferred from "no single system" context
- Rahul: Risk of dashboard overload — he needs a prioritised summary that flags what needs action, not a raw data grid. 🔶 [HYPOTHESIS]

**Pain points & friction:**
- No single view of center health exists today — revenue, attendance, and clinical status are held in separate, incompatible sources 🔵 Inferred from product context
- Key operational metrics (collection rate, utilization, dropout risk) are invisible until they become crises 🔵 Inferred
- Manual Excel reconciliation of attendance and fees is backward-looking — by the time it is assembled, the data is stale 🔵 Inferred
- No enrollment pipeline view: Rahul has no structured way to track the inquiry → enrolled → active → at-risk → dropout funnel 🔶 [HYPOTHESIS]

**Workarounds:**
- Rahul maintains a mental model of which families are "at risk" based on personal relationships and gut instinct 🔶 [HYPOTHESIS]
- Monthly Excel spreadsheet reconciling attendance and payments is the closest current approximation of a center dashboard 🔶 [HYPOTHESIS]

---

## Part 3 — Journey Break Points

> Consolidated table of the highest-friction moments across the full journey. Sorted by downstream impact severity.

| # | Journey | Persona(s) Affected | Friction Description | Evidence Level | Downstream Impact |
| --- | --- | --- | --- | --- | --- |
| BP-01 | Journey 4: In-session data collection | Priya, Dr. Sunita | Paper data collection during live sessions causes transcription errors, illegibility, and missed entries — one-handed constraint makes it physically awkward | 🔵 Inferred (paper failure modes ✅; India-specific confirmation pending) | Clinical decisions made on inaccurate data; supervisor cannot trust trends; delayed program updates |
| BP-02 | Journey 5: Supervisor review | Dr. Sunita | Session data arrives in batches, up to 2 weeks delayed; supervisor cannot identify plateau or regression promptly | ✅ BHCOE research (US); 🔵 inferred for India | Child runs outdated targets for weeks; program quality degrades silently |
| BP-03 | Journey 6: Progress reporting | Dr. Sunita | Report writing starts from scratch each cycle with no auto-population from session data; estimated 2–3 hours/day on documentation globally | 🔶 [HYPOTHESIS] for India scale; ✅ for global benchmark | Supervisor time is consumed by administrative work; reports are late or superficial; parent trust erodes |
| BP-04 | Journey 2: Intake | All | No standardized intake protocol — documentation collected ad hoc; DPDPA non-compliance risk | ✅ PMC; ⚠️ DPDPA | Child records are incomplete; clinical gaps at program start; regulatory exposure |
| BP-05 | Journey 8: Dropout | Meena, Rahul | No systematic attendance tracking; dropout is invisible until it has fully happened; single WhatsApp message is the only intervention | 🔵 Inferred (pattern) / 🔶 [HYPOTHESIS] (specifics) | Revenue loss; clinical harm from interrupted therapy; no early warning system exists |
| BP-06 | Journey 7: Billing | Rahul, Meena | Billing is manual, relationship-sensitive, and delayed; outstanding fees accumulate without a structured tracking system | 🔵 Inferred | Cash flow pressure; fee conversations avoided; financial stress accelerates dropout |
| BP-07 | Journey 3: Program design | Dr. Sunita, Priya | Program-to-therapist handover is verbal — Priya may misremember prompt levels, targets, or reinforcement schedules | 🔶 [HYPOTHESIS] | Sessions misaligned with prescribed program; data collected against wrong targets |
| BP-08 | Journey 1: Inquiry | Rahul | Inquiry details captured in WhatsApp thread with no structured record; no pipeline visibility | 🔶 [HYPOTHESIS] | Warm leads lost; no conversion tracking; no follow-up on non-responding families |
| BP-09 | Journey 4: In-session data collection | Priya | WhatsApp photo of paper data sheet used as digital shortcut — transmitting child health data unencrypted | 🔶 [HYPOTHESIS] | ⚠️ DPDPA violation; sensitive clinical data exposed on personal devices with no access control |
| BP-10 | Journey 6: Progress reporting | Meena | Reports written in clinical language Meena does not understand; no structured home program document | 🔶 [HYPOTHESIS] | Parent cannot implement home program; therapeutic gains are not reinforced between sessions; family disengages |
| BP-11 | Journey 3: Assessment | Dr. Sunita | Assessment data captured on paper — cannot be reused for automated report generation or trend tracking | 🔵 Inferred | High manual transcription burden; longitudinal baseline data is inaccessible |
| BP-12 | Journey 8: Dropout | Rahul | No re-engagement protocol: if a family returns after a gap, the center has no structured way to update the program or re-onboard the family | 🔶 [HYPOTHESIS] | Returning families receive inconsistent or stale care; dropout restarts |

---

## Part 4 — Hypothesis Register

> All 🔶 [HYPOTHESIS] items extracted from the journey map. Every hypothesis is stated as a falsifiable claim.

| # | Hypothesis | Centrality | Uncertainty | Risk Level | Validation Method | Validated When... | Invalidated When... |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H-01 | We believe special educators (Priya) in Indian autism centers record trial-by-trial data during live sessions on paper data sheets, because no digital tool exists that meets one-handed, in-session constraints | High | High | **High** | Contextual observation in 3–5 centers | We directly observe paper data sheets in use during sessions in majority of centers visited | Most therapists we observe skip in-session recording entirely, or use a digital tool we haven't identified |
| H-02 | We believe Indian special educators lack structured training in digital data collection tools, making onboarding burden a critical adoption variable | High | High | **High** | Semi-structured interview (n=8–10 therapists) + survey (n=30+) | 70%+ of therapist interviewees report never having used clinical data collection software | Majority report prior software experience; onboarding barrier is low |
| H-03 | We believe connectivity is intermittent enough in a meaningful proportion of Indian therapy session rooms to make offline-first capability a hard product requirement | High | High | **High** | On-site observation (connectivity test in session rooms across 5+ centers, mix of metro/tier-2) | >40% of session rooms tested have unreliable data connection during session hours | Connectivity is consistently reliable in all tested session rooms |
| H-04 | We believe inquiry details at Indian autism centers are captured in WhatsApp threads or paper notebooks with no structured record — giving centers no enrollment pipeline visibility | Medium | High | **High** | Contextual observation + director interview (n=5–8 center directors) | All or most center directors observed confirm they have no structured inquiry log | Majority of centers have a CRM or structured intake register for inquiries |
| H-05 | We believe the therapist-to-supervisor program handover at Indian centers is primarily verbal, leading to Priya running session targets with incomplete or inaccurate understanding of current prompt levels and reinforcement schedules | High | High | **High** | Contextual observation of handover moment + debrief interview with both parties | We observe verbal-only handover with no written program reference accessible in session room in majority of centers | Program binders or printed program sheets are consistently present and referenced during sessions |
| H-06 | We believe most Indian autism therapy centers are not DPDPA 2023-compliant at intake because consent for digital data processing is not collected in a verifiable format | High | Medium | **High** | Director interview (n=5–8) + review of existing consent forms | No center visited has a DPDPA-compliant digital consent flow; paper consent forms do not reference digital data processing | Multiple centers produce consent forms that reference DPDPA obligations explicitly |
| H-07 | We believe clinical supervisors at Indian autism centers spend significant uncompensated time (evenings or weekends) writing progress reports, because documentation competes with a full clinical caseload during working hours | High | High | **High** | Time-diary study or semi-structured interview with time-tracking component (n=5–8 supervisors) | Average reported documentation time outside clinical hours is >1 hour/week per supervisor | Supervisors report documentation is manageable within working hours; no significant out-of-hours burden |
| H-08 | We believe treatment plans in Indian centers are less formally structured and less consistently updated than US clinical standards recommend, because there is no external forcing function (insurance audits, payor authorization cycles) | Medium | Medium | **Medium** | Document review at 3–5 centers (request to see an existing child's therapy program) + supervisor interview | Program documents reviewed are informal, inconsistent in structure, and updated infrequently | Programs are consistently structured, version-controlled, and updated on a defined cycle |
| H-09 | We believe center directors experience fee collection as socially uncomfortable with financially stressed families, causing them to delay billing conversations and accumulate outstanding receivables | High | Medium | **Medium** | Semi-structured interview with center directors (n=5–8) | Directors describe avoiding or delaying fee conversations; receivables backlog confirmed as a recurring issue | Directors report fee collection is routine and timely; outstanding balances are minimal |
| H-10 | We believe when a family misses a session, follow-up is a single WhatsApp message — and no structured follow-up protocol exists for identifying or intervening with dropout-risk families | High | Medium | **Medium** | Director interview + contextual observation of admin workflow (n=5 centers) | No center has a written dropout intervention protocol; WhatsApp-only follow-up confirmed | At least some centers have a structured follow-up SOP with escalation beyond a single message |
| H-11 | We believe centers that use Cognitivebotics still rely on paper, WhatsApp, or spreadsheets for in-session clinical data collection, because Cognitivebotics does not provide therapist-side trial recording | Medium | Medium | **Medium** | Interview with 3–5 therapists at Cognitivebotics-using centers | All confirm paper or WhatsApp as their data collection method for clinical targets | Some centers have integrated Cognitivebotics data into their clinical program in ways that replace trial-recording |
| H-12 | We believe fee collection in Indian autism therapy centers is managed through WhatsApp messages, verbal conversation, and handwritten receipts — with no digital invoicing or payment tracking tool in use | Medium | Medium | **Medium** | Director interview + request to see billing workflow (n=5 directors) | WhatsApp-based billing confirmed in majority of centers; no digital invoicing tool identified | Multiple centers already use a digital payment tracking tool (Practo, Excel-based, or other) |
| H-13 | We believe Indian parents receive progress reports in clinical language they do not understand, and leave parent meetings without a clear written home program to follow | Medium | High | **Medium** | Parent interview (n=5–8 parents) + document review (review of 2–3 existing progress reports per center) | Parents describe not understanding reports; home program guidance is verbal only | Parents demonstrate comprehension of reports; written home programs are routinely provided |
| H-14 | We believe WhatsApp photos of paper data sheets are used by some therapists as an informal way to share session data with supervisors — transmitting unencrypted child health data via personal messaging apps | Medium | High | **Medium** | Contextual observation + therapist interview (n=5–8) | Majority of therapists report or are observed sending WhatsApp photos of data sheets | No center uses WhatsApp to transmit clinical data; all data is handled via physical handover only |
| H-15 | We believe UDID documentation is produced retrospectively when families request it, not captured at intake in a structured way — creating recurring admin burden with no systematic workflow | Low | High | **Medium** | Director interview (n=5–8) | Directors confirm UDID documentation is produced on-demand; no intake workflow captures it proactively | Centers have a structured UDID documentation workflow at intake |
| H-16 | We believe English-only UI is acceptable for therapist-facing features in metro market Indian therapy centers at launch, because clinical training programs in these markets use English-medium instruction | Medium | High | **Medium** | Semi-structured interview with therapists (n=8–10) — ask about language preference for any digital tool | 70%+ of metro therapists express comfort with English UI | Significant proportion (>30%) express need for Hindi or regional language UI before adoption |
| H-17 | We believe progress report writing at Indian centers starts from scratch each reporting cycle — with no carry-forward from previous reports or auto-population from session data | High | Medium | **High** | Contextual observation of report writing process + document review | No structured template or data carry-forward process identified in centers visited | Centers use a consistent report template with structured sections carried forward from prior reports |
| H-18 | We believe that when an Indian autism therapy center family withdraws from therapy, the center director experiences it as an unavoidable outcome rather than a process failure — because there is no attendance tracking system that surfaces early warning signals | Medium | Medium | **Medium** | Director interview (n=5–8) | Directors describe dropout as something they discover after the fact; no proactive monitoring described | Directors describe reviewing attendance weekly and contacting at-risk families systematically |

---

## Hypothesis Priority Summary

| Priority | Hypotheses | Why urgent |
| --- | --- | --- |
| Validate first (core product risk) | H-01, H-02, H-03, H-05, H-06, H-07, H-17 | These determine whether the core product proposition (in-session digital data collection, offline-first, reduced documentation burden) is actually valid for this market |
| Validate second (feature design risk) | H-04, H-09, H-10, H-13, H-16 | These shape how specific features must be designed; getting them wrong means building the right feature badly |
| Validate third (compliance and market sizing) | H-08, H-11, H-12, H-14, H-15, H-18 | Important for product and compliance design but lower build risk if wrong |

---

## Open Assumptions Still Requiring Primary Fieldwork

The following assumptions from the product CLAUDE.md are reflected in the hypothesis register above:

- [ASSUMPTION] Special educators find paper/WhatsApp-based data collection disruptive enough to pay for a software alternative → **H-01, H-02**
- [ASSUMPTION] Clinical supervisors spend significant uncompensated time on manual progress report writing → **H-07, H-17**
- [ASSUMPTION] Center directors would pay for a unified tool if it reduced their admin burden → **H-09, H-12 (partial)**
- [ASSUMPTION] Parents want structured progress updates beyond WhatsApp messages → **H-13**
- [ASSUMPTION] Offline-first is a hard requirement for most centers → **H-03**
- [ASSUMPTION] English-only UI is acceptable for therapist-facing features at launch → **H-16**
- [ASSUMPTION] WhatsApp cannot realistically be replaced for parent communication → Inferred structural constraint not yet hypothesis-tested; add to next research cycle

---

*What would need to be true for this product to succeed:*
1. Priya finds that paper-based in-session data collection is painful enough to switch to a new tool during live sessions with an active child (H-01)
2. The tool works offline in session rooms — not a nice-to-have (H-03)
3. Dr. Sunita's documentation burden is real, significant, and experienced as a problem worth solving — not just background cost of the job (H-07)
4. Rahul is willing to pay at Indian price points for a tool that reduces his admin burden, even with no insurance mandate to drive compliance pressure (H-09)
5. Therapist adoption happens within 2–4 weeks of rollout — without this, the data chain never starts and every downstream feature fails
