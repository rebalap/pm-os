# User Journey: DPDPA Consent Management & Data Subject Rights

**Previously:** J9 | ✅ **IN SCOPE — MVP**
**Trigger:**
- **Path A (Consent Capture):** A new child record has been created but no health data has been written yet. Parental consent is the gate before any clinical data can be stored or processed.
- **Path B (Data Subject Rights):** An existing parent (Meena) contacts the centre to withdraw consent, request a copy of her child's data, or request erasure of her child's records.

**Primary actors:**
- **Path A:** Rahul (Centre Director / data fiduciary — captures consent at intake) and Meena (parent / data principal — gives consent)
- **Path B:** Meena (exercises data subject rights) handled by Rahul (Centre Director / data fiduciary)

**Supporting actors:**
- System (enforces consent gates across all clinical features; all downstream data writes are blocked until consent is confirmed)
- Dr. Sunita (notified when consent is withdrawn for a child on her active supervision caseload)

**Entry condition — Path A:** A child record (EMR-001) exists with status "Pending consent." No session notes, therapy programs, SOAP notes, or clinical documents have been written. The intake form may or may not be complete. The system is actively blocking clinical data entry.

**Entry condition — Path B:** Meena has an active parent portal account (RBAC-005) or contacts the centre by phone/WhatsApp. Consent was previously captured (DPDPA-001 confirmed). She is requesting one of: (i) consent withdrawal, (ii) data portability / download, or (iii) erasure.

**End state — Path A:** Verifiable parental consent is recorded with server-confirmed timestamp (IST), actor identity, consent notice version, method of consent (digital signature, digital checkbox, or staff-assisted verbal with follow-up flag), and device/IP metadata. The child's record status transitions from "Pending consent" to "Active." All subsequent clinical data writes across every feature in the product are unlocked for this child.

**End state — Path B — Withdrawal:** Meena's withdrawal is recorded as an immutable audit event. New clinical data creation for this child is blocked immediately. Dr. Sunita and Rahul are notified. Existing records remain accessible to authorised staff (withdrawal is prospective — it does not auto-erase historical data). Audit trail records every action taken.

**End state — Path B — Data Portability:** Meena has received a PDF of all data held about her child. The export is logged in the audit trail.

**End state — Path B — Erasure:** Meena's erasure request has been submitted and assigned to Rahul with a 30-day DPDPA-compliant processing clock. The DPDPA/RPWD conflict decision has been surfaced and a human (Rahul + legal) has either confirmed full erasure or documented the retention obligation. Audit trail records every action. If erasure is confirmed, all clinical data is removed from active storage; only an anonymised erasure event record remains.

**Journey source documents:**
- `cluster-5-analytics-compliance-access.md` — DPDPA-001 through DPDPA-005, AUDIT-001 through AUDIT-003, RBAC-001 through RBAC-005
- `cluster-2-patient-records-intake.md` — INT-003 (DPDPA consent capture at intake form submission)
- `cluster-1-clinical-documentation.md` — EMR-001 (child record creation), EMR-002 (DPDPA consent in EMR), SNOTE-001 (consent gate on session notes), TMPL-001 (consent gate on therapy programs), SOAP-001 (consent gate on SOAP notes)

---

## Discovery Context

**MVP Scope:** ✅ **IN SCOPE — MVP** | Regulatory prerequisite — gates all data entry

**Pain points & friction:**
- Indian autism therapy centers currently have no DPDPA-compliant consent process — paper consent forms (where they exist) do not reference digital data processing ⚠️ DPDPA 🔶 [HYPOTHESIS]
- Staff have no training on DPDPA requirements for processing minors' health data 🔶 [HYPOTHESIS]
- No mechanism for consent withdrawal in any current workflow — once data is in a system, no deletion protocol exists 🔵 Inferred gap

**Emotional states:**
- Meena: Trust is not yet established at this journey. Consent language must be plain and accessible — clinical or legal jargon will cause passive non-engagement rather than refusal. 🔵 Inferred from caregiver trust and health literacy literature
- Rahul: Likely unfamiliar with DPDPA requirements — will experience this as friction unless it is embedded naturally into the intake flow rather than presented as a separate compliance step. 🔶 [HYPOTHESIS]

**Current workarounds:**
- No structured workarounds exist for DPDPA compliance — centers are either unaware of the obligation or have no digital consent mechanism in place 🔶 [HYPOTHESIS]
- Paper consent forms (where they exist) reference therapy consent only, not digital data processing 🔶 [HYPOTHESIS]

**⚠️ DPDPA exposure:**
- Step A-01 (child record creation): Creating a child record begins processing personal data of a minor — DPDPA 2023 consent gate must activate immediately; no health data can be written without confirmed consent.
- Step A-07 (consent record write): The consent record is the legal compliance mechanism — must be an atomic, server-confirmed transaction; a failed write must roll back the entire consent action with no partial state stored.
- Step B1-04 (withdrawal): DPDPA Section 6(4) requires withdrawal to be processed without delay; the platform must execute within the same session.
- Step B2-03 (data portability): DPDPA Section 12 makes portability a mandatory, unjustifiable right — the request cannot be blocked or require the parent to explain herself.
- Step B3-05 (erasure review): DPDPA Section 12(c) right to erasure conflicts with RPWD Act 2016 retention obligation — this conflict cannot be resolved by engineering; a human decision by Rahul (with legal counsel) is required.

---

## Regulatory Context — Read Before Reviewing This Document

> **DPDPA 2023 is the governing law. HIPAA does not apply in India.**

| Regulation | Relevance to this journey |
|---|---|
| **DPDPA 2023 Section 9** | Processing personal data of minors requires verifiable parental consent — not a checkbox as an afterthought. Consent must be specific to purpose. |
| **DPDPA 2023 Section 6(2)** | Consent must be informed — parent must receive a privacy notice in plain language before consenting. |
| **DPDPA 2023 Section 6(4)** | Right to withdraw consent at any time — withdrawal is prospective; it stops future processing but does not automatically erase historical data. |
| **DPDPA 2023 Section 12(c)** | Right to erasure — data principal can request deletion; data fiduciary must respond within the prescribed period (platform target: 30 days). |
| **DPDPA 2023 Section 12 (data portability)** | Parent can request a machine-readable or PDF export of all data held about their child. |
| **RPWD Act 2016** | Creates a documentation and retention obligation for individualized therapy program records. This obligation may conflict with the DPDPA right to erasure. This conflict cannot be resolved by the system — it requires human (Rahul + legal) sign-off. |
| **RCI licensing context** | RCI-licensed special educators and clinical supervisors are required to maintain clinical records. The RPWD Act retention obligation applies to their documentation. |

---

## PATH A — Consent Capture at Intake

### Step-by-Step Flow

| Step | Actor | Action | Screen / State | Technical Note |
|---|---|---|---|---|
| A-01 | Rahul / Admin | Creates a new child record with the five required fields (child name, DOB, diagnosis, parent name, parent mobile) | Child Record Creation screen (EMR-001) | Writes to: child_record table (status = "pending_consent"). No health data written. API: `POST /children`. Offline: form drafts locally, record creation requires connectivity. Regulatory gate: record creation itself is processing personal data — the consent prompt banner appears immediately on record creation (AC-05 of EMR-001). |
| A-02 | System | Blocks all clinical data entry tabs (Session Notes, Therapy Program, SOAP Notes, Documents) with a non-dismissible orange consent banner | Child Record — "Pending consent" state | System state: child record status = "pending_consent". All clinical write endpoints return 423 (Locked) if consent is not confirmed. Banner reads: "Parental consent required — clinical records cannot be added until consent is confirmed. Add consent now." This is not a soft warning; it is a hard gate. |
| A-03 | Rahul | Taps "Add consent now" from the consent banner, or navigates to the Consent tab on the child's record | Consent Capture screen (DPDPA-001 / EMR-002) | Entry point: orange banner CTA or Consent tab. RBAC check: only Director and Admin roles can initiate consent capture. DPDPA gate: this screen is the DPDPA compliance mechanism — consent must not be pre-checked or auto-filled. |
| A-04 | Rahul | Presents the consent screen to Meena. System renders the plain-language Privacy Notice — all six required sections (what data, why, who has access, retention period, parent rights, contact) | Privacy Notice + Consent Form screen (DPDPA-003) | Privacy Notice content is version-stamped. Notice version is stored with the consent record so that future changes to the notice are trackable. Font: minimum 16px, line height ≥ 1.5, WCAG AA contrast. Must be readable on a mid-range Android without pinch-zooming. This is the DPDPA Section 6(2) informed consent requirement. |
| A-05 | Meena | Reads the privacy notice. May ask Rahul questions about what is being collected or why. | Privacy Notice — reading state | No system action. Rahul is responsible for explaining verbally if Meena cannot read English. If verbal explanation is needed, admin checks "Explained verbally in [language]" at the next step (captured in consent record, flagged for Phase 2 translated notice). |
| A-06 | Meena | Gives consent via one of three mechanisms: (i) on-screen digital signature (finger/stylus), (ii) explicit checkbox confirmation ("I confirm I am the legal parent/guardian of [child name] and consent to collection and processing of their health data as described above" — NOT pre-checked), or (iii) if parent is absent: staff records "Staff-assisted consent — verbal" with follow-up flag | Consent Capture screen — confirmation step | Pre-checked checkboxes are NOT permitted (DPDPA 2023 requirement for affirmative consent). Mechanism (iii) is flagged in the record as non-compliant and prompts for digital consent at next visit. |
| A-07 | Rahul | Taps "Confirm consent" | Consent submission | System writes consent record (immutable, server-confirmed): parent name, relationship to child, date/time (IST), platform consent notice version ID, method (signature / checkbox / verbal-staff-assisted), admin who recorded it, device identifier. API: `POST /children/{id}/consent`. This call requires active connectivity — consent cannot be written from an offline queue; the server timestamp is the legally significant timestamp. If the server write fails, the form does not submit and no partial data is stored. |
| A-08 | System | Consent record written as immutable entry. Child record status transitions from "pending_consent" to "active". Orange consent banner replaced with green indicator: "Consent confirmed — [date]". | Child Record — Active state | State transition: child_record.status = "active". Consent record: append-only; no UPDATE or DELETE endpoint exists. AUDIT-001 event: CREATE, consent_record, actor, timestamp, "DPDPA high-risk" flag. All clinical data write endpoints (session notes, programs, SOAP notes, documents) are now unlocked for this child. |
| A-09 | Rahul | Optionally views the consent record from the Consent tab — it is read-only and shows all captured fields | Consent Record — read-only view (DPDPA-005) | Access to consent record: Director and Admin roles only. All other roles see only the "Consent confirmed [date]" badge in the record header. The consent record is never shown in full to therapist or parent portal (different views expose different fields). |
| A-10 | System | "Consent confirmed" badge is permanently visible in the record header for all authorised staff who open this child's record | Child Record header — all tabs | Badge format: "DPDPA Consent: Confirmed [date]" (INT-003 AC-06). Visible to all roles with access to this child's record. Clinical tabs now load normally. |

---

## PATH B — Data Subject Rights Request

### Path B-i: Consent Withdrawal

| Step | Actor | Action | Screen / State | Technical Note |
|---|---|---|---|---|
| B1-01 | Meena | Logs into the parent portal and navigates to Account > Privacy > My Consent | Parent Portal — Privacy settings (DPDPA-002, RBAC-005) | RBAC gate: Parent role only. Meena sees only records linked to her child(ren). API: `GET /parent/consent-status`. |
| B1-02 | Meena | Views her active consent record — date given, purposes covered, how to withdraw | Consent Status screen | System displays: consent date, purposes (as listed in the notice version she signed), and a "Withdraw consent" button. Plain-language explanation is present. |
| B1-03 | Meena | Taps "Withdraw consent" | Consent Withdrawal flow — explanation screen (DPDPA-002) | System displays a plain-language explanation: "If you withdraw consent, no new therapy or session records will be created for [child name]. Existing records will remain unless you also request erasure. The centre will be notified." Meena must take an explicit action to continue — this is not a one-tap withdrawal. |
| B1-04 | Meena | Confirms withdrawal (explicit affirmative tap — "Yes, withdraw my consent") | Consent withdrawal confirmation | API: `POST /children/{id}/consent/withdraw`. Requires active connectivity. Withdrawal record written as immutable audit event (action = "CONSENT_WITHDRAWAL", actor = parent, timestamp, "DPDPA high-risk" flag per AUDIT-001 AC-05). Response within the same session — no delays permitted under DPDPA Section 6(4). |
| B1-05 | System | Child record status transitions from "active" to "consent_withdrawn". New clinical data creation blocked. In-progress sessions: any session note currently being written is allowed to complete but is flagged; no new sessions can be started. | Child Record — "Consent withdrawn" state | State transition: child_record.status = "consent_withdrawn". Clinical write endpoints return 423 (Locked) again. "Consent withdrawn — data processing suspended" banner appears on the child's record for all staff. Existing records remain readable by authorised staff but no new data can be written. |
| B1-06 | System | Rahul receives in-app notification: "[Child first name]'s parent has withdrawn data processing consent." Dr. Sunita (if assigned as supervisor) receives in-app notification: "Consent withdrawn for [child first name] — new session data cannot be recorded." | Notification — admin and supervisor | Notification delivery within 60 seconds of withdrawal confirmation. Rahul and Dr. Sunita are responsible for operationally managing the impact (e.g., cancelling upcoming sessions, communicating with Priya). |
| B1-07 | Rahul | Reviews the withdrawal notification. Opens the child's record. Decides on next steps (contact Meena, pause scheduling, initiate erasure if requested). | Child Record — "Consent withdrawn" state | Rahul can see all existing records (they are not erased by withdrawal). He cannot create new clinical data. He can see the consent withdrawal event in the Consent tab timeline. |
| B1-08 (Optional re-consent path) | Rahul / Meena | If Meena re-consents at a later date, Rahul initiates a new consent capture (Path A from A-03). A new, separate consent record is created. The withdrawal record is NOT modified — both the withdrawal and the new consent exist as immutable events in the timeline. | Consent Capture screen (Path A) | New consent record supersedes withdrawal for future data processing. All prior consent and withdrawal events remain in the immutable audit log. The child's record status returns to "active" on new consent confirmation. |

---

### Path B-ii: Data Portability Request

| Step | Actor | Action | Screen / State | Technical Note |
|---|---|---|---|---|
| B2-01 | Meena | Logs into the parent portal and navigates to Account > My Child's Data | Parent Portal — Data download screen (EXPORT-004) | RBAC gate: Parent role, linked child only. API: `GET /parent/children/{id}/data-export-status`. |
| B2-02 | Meena | Reads plain-language explanation of her right and what the download will contain: "You have the right to a copy of all information we hold about [child name]. This will include session records, progress reports, and intake information." | Data portability explanation screen | No clinical jargon. Meena must be able to understand this on a low-end Android without technical knowledge. This right cannot be blocked, delayed, or require justification under DPDPA Section 12. |
| B2-03 | Meena | Taps "Download all records" | Export request submission | API: `POST /parent/children/{id}/data-export-request`. Audit log entry created immediately: actor = parent, action = "DATA_PORTABILITY_REQUEST", "DPDPA S.12", timestamp (AUDIT-001 and EXPORT-004 AC-03). |
| B2-04 | System | Generates a PDF of all records held about the child in plain, non-clinical language where possible. For small records (< 12 months): PDF available immediately. For large records (> 2 years): within 24 hours via in-app notification. | PDF generation — background job | PDF includes: cover note ("This document contains all personal and health data recorded about [child name] by [Centre name]. If you believe any information is inaccurate, contact [Centre name] directly."), all intake data, session records, therapy program versions, progress reports. No invoice data in parent-facing export. DPDPA compliance target: 30 days; product target: 24 hours. |
| B2-05 | Meena | Downloads the PDF. Reviews it. | Download confirmation screen | Android share sheet triggered. Export action logged with file ID in audit trail. Meena can see exactly what the centre holds. This visibility often precedes an erasure request (DPDPA-004 is the natural follow-on). |

---

### Path B-iii: Erasure Request (DPDPA/RPWD Conflict Decision Point)

| Step | Actor | Action | Screen / State | Technical Note |
|---|---|---|---|---|
| B3-01 | Meena | In Account > Privacy, taps "Request data erasure" | Erasure request screen (DPDPA-004) | RBAC gate: Parent role. This path typically follows either a data portability download (B2) or consent withdrawal (B1), but can be initiated independently. |
| B3-02 | System | Displays plain-language erasure warning: "Requesting erasure will permanently delete all records about [child name] from our system. This cannot be undone. The centre will no longer have access to your child's therapy history. Are you sure you want to continue?" | Erasure confirmation screen | Irreversibility warning is mandatory. A typed confirmation ("Type DELETE to confirm") is required before the request is submitted. This prevents accidental erasure. |
| B3-03 | Meena | Types "DELETE" and confirms the erasure request | Erasure confirmation — typed input | API: `POST /children/{id}/erasure-request`. Audit log entry: actor = parent, action = "ERASURE_REQUEST", "DPDPA S.12(c)", "DPDPA high-risk" flag, timestamp. A task is created in Rahul's admin queue with a 30-day processing clock. Child record status transitions to "erasure_requested". |
| B3-04 | Rahul | Receives in-app notification: "[Child name]'s parent has requested data erasure. You have 30 days to complete this under DPDPA 2023." Opens admin task queue. | Admin task queue — erasure task (DPDPA-004 AC-02) | 30-day escalating reminders: day 15 (in-app), day 25 (in-app + email), day 30 (in-app + email + flagged prominently in admin dashboard). The clock starts from the moment the request is submitted. |
| **B3-05** | **System** | **⚠️ DPDPA / RPWD CONFLICT SURFACED — HUMAN DECISION REQUIRED** System displays to Rahul: "Certain records may need to be retained under the Rights of Persons with Disabilities Act 2016. RPWD Act 2016 requires documentation of individualized therapy programs for children with disabilities. Erasing these records may put your centre out of compliance with RPWD Act documentation requirements. This is a legal conflict. The system cannot automatically determine which records must be retained. Consult your legal advisor before confirming full erasure." | Erasure review screen — RPWD conflict warning (DPDPA-004 EC-01) | **This is the critical decision point in this journey. The system does NOT automatically block erasure and it does NOT automatically proceed with erasure. It surfaces the legal conflict and requires a human decision.** The system presents three options: (A) Proceed with full erasure — I confirm I have reviewed the RPWD Act retention obligation and take legal responsibility for this decision. (B) Proceed with partial erasure — erase personal contact data and session content but retain the anonymised individualized program documentation required under RPWD Act. (C) Defer — I need to consult a legal advisor before proceeding. The 30-day clock continues running. Engineering cannot resolve this conflict. Rahul and his legal advisor must decide. The system's role is to surface the conflict clearly, document Rahul's decision, and execute what he chooses. |
| B3-06 | Rahul | Makes a decision: (A) full erasure, (B) partial erasure with RPWD retention, or (C) defer for legal review | Erasure decision screen | Rahul's choice and the timestamp of his decision are written to the audit log as an immutable event. If he selects (C), the task remains open in his queue. If he selects (A) or (B), the system proceeds to B3-07. |
| B3-07 | Rahul | Confirms erasure action — final confirmation dialog with irreversibility warning | Final erasure confirmation | For option (A): all clinical data (session notes, therapy programs, SOAP notes, intake data, documents) is deleted from active database storage. Only an anonymised erasure event record is retained in the audit log: child_id (anonymised hash), erasure_date, actor, "DPDPA erasure — full." For option (B): personal contact data and session content is deleted; anonymised program documentation is retained with a retention justification note ("RPWD Act 2016 — retained per centre director decision [date]"). Audit log: "DPDPA erasure — partial, RPWD retention confirmed." |
| B3-08 | System | Erasure confirmed. Meena's parent portal shows: "Your erasure request has been completed. No data about [child name] is held by this system." (or partial erasure variant). | Parent Portal — erasure confirmed state | If partial erasure: parent portal shows which categories of data were retained and the regulatory reason. Consent record is retained as an immutable event in the audit log even after clinical data is erased (the consent record is the evidence that data was lawfully processed; it is not the clinical data itself). Audit log entry: full erasure confirmation with method, timestamp, actor. |

---

## Decision Points and Branches

### Decision 1: Method of Consent at Intake
**At step:** A-06
**Question:** Is Meena present and able to interact with the consent screen directly?
- **Path A-i — Digital self-service (in-person):** Meena signs on-screen or checks the explicit consent checkbox herself. Method recorded as "in-person digital." This is the highest-compliance method.
- **Path A-ii — Staff-assisted (parent present, no digital device):** Rahul records consent on Meena's behalf after explaining it verbally. Method recorded as "Staff-assisted — verbal." System flags this as incomplete: "Full digital consent pending — collect at next visit." A follow-up banner persists on the child's record until digital consent is confirmed.
- **Path A-iii — Remote consent (parent not present at intake):** Rahul generates a WhatsApp-shareable consent link. Meena signs on her own device at home before the next visit. Method recorded as "Remote consent — parent signed via link." Audit trail shows both the link generation and the remote signature event.
- **Path A-iv — Parent refuses consent:** The child's record remains in "pending_consent" state indefinitely. Session data cannot be entered. The record itself can exist for scheduling purposes. Rahul is responsible for managing the clinical and commercial consequences.

---

### Decision 2: Consent Withdrawal Scope
**At step:** B1-03 (after Meena reads the withdrawal explanation)
**Question:** Does Meena want only to stop future processing, or does she also want erasure of existing records?
- **Path B-i — Withdrawal only:** Meena confirms withdrawal. Future data creation is blocked. Existing records remain. This is the default path. Journey ends at B1-07.
- **Path B-i + B3 — Withdrawal followed by erasure:** Meena confirms withdrawal AND then initiates an erasure request. The erasure request follows Path B-iii, starting at B3-01. The DPDPA/RPWD conflict will be surfaced at B3-05.

---

### Decision 3 (Critical): DPDPA Right to Erasure vs. RPWD Act 2016 Retention Obligation
**At step:** B3-05
**Question:** Does the child's therapy record contain individualized program documentation that the RPWD Act 2016 requires the centre to retain, even if the parent has requested erasure?

This is the most legally sensitive decision point in the entire product. The system cannot resolve it automatically.

- **Option A — Full erasure (Rahul + legal confirm RPWD obligation does not apply or is waived):** All clinical data deleted. Rarely the right call if the child is still enrolled or recently discharged. Rahul takes legal responsibility. Audit log records his decision explicitly.
- **Option B — Partial erasure (RPWD retention confirmed):** Personal contact data and session content erased. Anonymised, de-identified individualized program documentation retained with a documented justification. The parent is informed of what was retained and why. This is the most legally defensible path in most cases involving an active or recently active child.
- **Option C — Defer for legal review:** Rahul does not proceed until he has consulted a legal advisor. The 30-day DPDPA clock continues. Rahul must ensure he meets the 30-day deadline or formally requests an extension with documented justification. The system will escalate with reminders at day 15, 25, and 30.

**Why engineering cannot resolve this conflict:**
DPDPA 2023 Section 12(c) creates a mandatory erasure right. RPWD Act 2016 creates a documentation obligation. These are two separate statutes. Neither automatically overrides the other. The resolution depends on: the specific records involved, the child's current enrollment status, the centre's registration under RPWD Act, and legal advice on which obligation takes precedence in the specific case. This is a legal question, not an engineering question. The system's role is to surface the conflict clearly and enforce whatever Rahul decides — not to decide for him.

---

### Decision 4: Data Portability Response Time
**At step:** B2-04
**Question:** Is the child's record small enough for immediate PDF generation?
- **Path B2-i — Small record (< 12 months of data):** PDF generated immediately and offered for download in the same session.
- **Path B2-ii — Large record (> 2 years of data):** Background job generates the PDF. Meena receives an in-app notification when it is ready (target: within 24 hours). She cannot download it immediately but the request has been accepted and the clock is running.

---

## Screen Inventory

| Screen name | Purpose | Primary action | Personas who see it | Source story |
|---|---|---|---|---|
| Child Record Creation | Create a new child record with minimum required fields | Save new child record | Rahul, Admin | EMR-001 |
| Child Record — Pending Consent state | Show blocked clinical tabs and non-dismissible consent banner | Tap "Add consent now" | Rahul, Admin | EMR-001 AC-05, EMR-002 AC-01, DPDPA-001 AC-01 |
| Privacy Notice (consent context) | Display full plain-language privacy notice before consent is captured | Read / scroll to confirm they've seen it | Meena (at intake), Rahul (presenting device) | DPDPA-003, INT-003 AC-01 |
| Consent Capture screen | Capture verifiable parental consent with explicit affirmative action | Confirm consent (signature / checkbox) | Meena (primary actor), Rahul (facilitates) | DPDPA-001, INT-003, EMR-002 |
| Child Record — Active state (post-consent) | Show green consent badge; all clinical tabs unlocked | Navigate to any clinical tab | Rahul, Dr. Sunita, Priya (role-scoped) | EMR-002 AC-04, DPDPA-001 AC-04 |
| Consent Record — read-only view | Show all details of the consent event for compliance purposes | Export consent log (PDF) | Rahul only | DPDPA-005, EMR-002 AC-06 |
| Remote Consent Link (parent device) | Allow Meena to sign consent on her own device at home | Sign consent remotely | Meena | EMR-002 EC-01 |
| Parent Portal — Privacy settings | Show Meena her current consent status and her rights | View / initiate consent withdrawal | Meena | DPDPA-002 AC-01, RBAC-005 |
| Consent Withdrawal explanation screen | Explain in plain language what withdrawal means and what will change | Confirm withdrawal | Meena | DPDPA-002 AC-02 |
| Consent Withdrawal confirmation | Final confirmation of withdrawal action | Confirm withdrawal (irreversible until re-consent) | Meena | DPDPA-002 AC-03 |
| Child Record — "Consent withdrawn" state | Show blocked clinical tabs; withdrawal banner for all staff | None (read-only for clinical) | Rahul, Dr. Sunita, Priya | DPDPA-002 AC-03 |
| Parent Portal — Data download | Explain data portability right and initiate download | Request download | Meena | EXPORT-004 AC-01 |
| Data portability PDF (generated document) | Provide all data held about the child in readable format | Download / share | Meena | EXPORT-004 AC-02, AC-04 |
| Erasure request screen | Initiate data erasure with irreversibility warning | Type DELETE to confirm | Meena | DPDPA-004 AC-01 |
| Erasure review screen — RPWD conflict | Surface the DPDPA/RPWD legal conflict to Rahul; require human decision | Choose: full erasure / partial erasure / defer | Rahul | DPDPA-004 EC-01 — **most important screen in this journey** |
| Admin task queue — erasure task | Show Rahul the pending erasure with 30-day clock | Confirm or defer erasure decision | Rahul | DPDPA-004 AC-02 |
| Audit Log — consent view | Show all consent events for a child in chronological order | Filter / export consent log as PDF | Rahul | DPDPA-005, AUDIT-002 |
| Consent Audit Log export (PDF) | Provide a compliance-ready PDF of all consent events | Download / share with regulator | Rahul | DPDPA-005 AC-02 |
| Center-wide consent status report | Show consent status for all children in a single export | Export CSV | Rahul | DPDPA-005 AC-04 |

---

## Designer Handoff

### Screen: Privacy Notice (Consent Context)

**Purpose:** This is the most important screen in Path A. Meena must be able to read and understand what she is agreeing to before giving consent. DPDPA Section 6(2) requires that consent be informed. If Meena cannot understand this screen, the consent is not legally valid.

**Primary action:** Meena reads and scrolls to the bottom of the notice, then proceeds to the Consent Capture step.

**Entry point(s):** Automatically presented when Rahul taps "Add consent now" (Path A, Step A-03). Cannot be skipped.

**Exit point(s):** "I have read this" / "Proceed to consent" button at the bottom — only visible after the user has scrolled to the end (or after a minimum read time). Leads to Consent Capture screen.

**Key components:**
- Header: "[Centre name] — Privacy Notice" with a plain-language subtitle: "What we collect about your child and why"
- Six sections (presented as clearly labelled blocks, not wall-of-text paragraphs):
  1. What data we collect (bullet list — child's health records, session notes, assessments, therapy programs, intake information)
  2. Why we collect it (purpose list — delivering therapy, tracking progress, communicating with you)
  3. Who can see it (named roles — therapist assigned to your child, clinical supervisor, centre director; no one else)
  4. How long we keep it (plain statement — "We keep your child's records for [X years] after they leave our centre, or until you request erasure")
  5. Your rights (access, correction, erasure, withdrawal — with "How to exercise your rights" link)
  6. Contact us (centre name, contact number or email for data-related queries)
- Language toggle: English (Phase 1). Hindi (Phase 2). If parent cannot read English, admin checks "Explained verbally in [language]" toggle — this is captured in the consent record.
- Scroll progress indicator (subtle — shows Meena she needs to scroll to continue)
- "Proceed to consent" button — only activated after full scroll

**States:**
- **Loading state:** Static content (not server-fetched per-load); loads immediately from cached template. No spinner needed.
- **Error state:** If the consent notice version cannot be confirmed from the server, show: "Unable to load consent form — please check your internet connection." Do not allow consent to proceed without the confirmed notice version being recorded.
- **Offline state:** Consent requires connectivity (the consent record must be written to the server with a server-confirmed timestamp). Show: "An internet connection is required to complete consent. Your progress is saved — please reconnect and continue."
- **Empty/first state:** Not applicable — the notice is always pre-populated.

**Constraints:**
- Font size minimum 16px. Line height minimum 1.5. This is a non-technical Indian parent reading on a low-end Android phone.
- No clinical jargon. Use "health records" not "PHI." Use "therapy plan" not "individualized behaviour intervention program."
- Do not use abbreviations (DPDPA, RPWD, RCI) in the parent-facing notice without plain-language explanation.
- Scroll should feel natural — do not disable the system scroll on this screen.
- Touch targets for any links within the notice ≥ 44px.
- WCAG AA contrast on all text — minimum 4.5:1 for body text.

---

### Screen: Consent Capture Screen

**Purpose:** Capture Meena's verifiable, affirmative consent in a legally defensible form. This is the DPDPA 2023 compliance mechanism — not a UX formality.

**Primary action:** Meena gives explicit consent via digital signature or explicit checkbox — not a pre-checked confirmation.

**Entry point(s):** From the Privacy Notice screen (tap "Proceed to consent"). Cannot be reached by bypassing the Privacy Notice.

**Exit point(s):** Tapping "Confirm consent" submits the consent record to the server. On success: leads to "Consent confirmed" confirmation screen, then to the Active child record. On failure (server error): form does not submit; user sees an error with retry option; no partial data stored.

**Key components:**
- Summary line at top: "You are giving consent for [Centre name] to collect and process [Child name]'s health data for therapy purposes."
- Consent method selector (shown if multiple methods are available):
  - "Sign below" (digital signature input) — preferred for highest compliance
  - "Tick to confirm" (checkbox) — acceptable alternative; NOT pre-checked
- Digital signature field: 200×100px minimum touch area; works with finger and stylus; shows a "Clear" button; the signature is not displayed back to the user after submission (stored securely, not displayed)
- Checkbox (if method chosen): Label: "I confirm that I am the legal parent or guardian of [child name] and I give consent for [centre name] to collect and process their health data as described in the privacy notice I have read."
- Parent name field (pre-filled from child record parent name field, but editable to capture the name of the actual person present if different from the primary guardian)
- Relationship to child dropdown: Mother / Father / Legal guardian / Extended family caregiver / Other (please specify)
- If parent not present: "Parent is not present — record verbal consent" toggle (only visible to staff roles). Activates a note field: "Staff name who obtained verbal consent" and triggers the Staff-Assisted consent method flag.
- "Confirm consent" button — primary action; disabled until the consent mechanism is completed (signature drawn or checkbox ticked)

**States:**
- **Empty state:** Signature field is blank; checkbox is unchecked. "Confirm consent" button is greyed out with label "Complete the consent above to proceed."
- **Loading state (on submit):** "Saving consent record..." with a spinner. The button is disabled during submission. This should complete in ≤ 2 seconds.
- **Error state:** "Consent could not be saved — please check your connection and try again. No data has been stored." Clear retry button. Critically: no partial consent record is written on failure; the transaction is atomic.
- **Offline state:** "An internet connection is required to confirm consent. Please reconnect before proceeding." Consent cannot be captured offline.
- **Staff-assisted consent state:** A yellow banner: "Recording consent on behalf of parent — ensure the parent has read or heard the privacy notice." The consent record will be flagged for follow-up digital consent.

**Constraints:**
- The consent checkbox must never be pre-checked. This is a hard requirement under DPDPA 2023. Pre-checked consent is invalid consent.
- The "Confirm consent" button should not use the word "Accept" or "Agree" — the phrasing "Confirm consent" is the most legally precise language and should be preserved exactly.
- Do not add visual styling that makes the consent feel like a routine "terms and conditions" screen (dark patterns). The screen should feel deliberate and important — appropriate weight for the significance of the action.
- The screen should work on a shared centre tablet being held by a parent — landscape and portrait orientations both functional.

---

### Screen: Child Record — "Pending Consent" State

**Purpose:** Block all clinical data entry for a child whose parental consent has not yet been confirmed, while clearly surfacing what action is needed and who needs to take it.

**Primary action:** Rahul (admin) taps "Add consent now" to begin the consent capture flow.

**Entry point(s):** Automatically shown when any authorised user opens a child record created without confirmed consent.

**Exit point(s):** The banner and blocked state are removed only when consent is confirmed (server-confirmed write of the consent record). There is no "dismiss" or "remind me later" option on the banner.

**Key components:**
- Non-dismissible orange banner at the top of the record, above all tabs: "Parental consent required — clinical records cannot be added until consent is confirmed." with a CTA button: "Add consent now"
- All clinical data tabs (Session Notes, Therapy Program, SOAP Notes, Documents, Assessments): greyed out, with a lock icon and tooltip on tap: "Consent required — tap 'Add consent now' above."
- Non-clinical tabs remain accessible: Profile (demographic fields), Care Team (staff assignment), Scheduling (sessions can be booked but not documented), Billing.
- Intake form tab: accessible if intake form has been sent / completed (INT-002) — the completed intake form data can be viewed but session data cannot be created.

**States:**
- **Empty state:** Not applicable — this state exists because the record was just created.
- **Loading state:** Standard record loading skeleton.
- **Error state:** If the consent banner fails to load (unlikely — static logic), show a generic error and refresh prompt. Never silently allow clinical data entry without confirmed consent.
- **Offline state:** Banner is always shown based on last-synced consent status. If offline and consent status is unknown, conservative default is to keep clinical tabs locked.

**Constraints:**
- The orange banner must be visually distinct from all other banners in the product. Consider: orange background (not the standard blue informational banner, not a red error). Consent is neither an error nor routine information — it is a required action.
- Touch target for "Add consent now" CTA: ≥ 44px height.
- The banner should not disappear on scroll — it should remain visible when the user scrolls down through the tabs.

---

### Screen: Erasure Review Screen — RPWD Conflict Warning

**Purpose:** This is the most important screen in Path B. Its function is to surface the legal conflict between DPDPA 2023 right to erasure and RPWD Act 2016 retention obligation — clearly, accessibly, and without engineering making the decision on behalf of the centre director. Rahul must make an informed, legally accountable choice.

**Primary action:** Rahul selects one of three options: (A) Full erasure, (B) Partial erasure with RPWD retention, (C) Defer for legal review.

**Entry point(s):** Automatically presented when Rahul opens the erasure task from his admin queue (B3-05). Cannot be bypassed.

**Exit point(s):** Selecting option (A) or (B) leads to a final erasure confirmation step (B3-07) with a secondary warning. Selecting option (C) returns Rahul to his admin queue — the task remains open with the 30-day clock running.

**Key components:**
- Header: "Legal review required before proceeding"
- Warning body (plain language, not legalese):
  - "Meena has requested that all records about [child name] be permanently deleted."
  - "However, the Rights of Persons with Disabilities Act 2016 (RPWD Act) may require your centre to keep documentation of [child name]'s individualised therapy program."
  - "This is a legal conflict between two Indian laws. We cannot automatically decide which applies to this situation — that requires a legal judgement about your centre's obligations."
- Three clearly labelled options presented as cards, not radio buttons (cards are more readable on mobile):
  - **Option A — Full erasure:** "Delete all records, including the therapy program. I have reviewed the RPWD Act documentation requirement and confirm it does not apply in this case, or I accept legal responsibility for this decision." [Confirm — leads to B3-07 full erasure confirmation]
  - **Option B — Partial erasure (recommended):** "Delete personal contact data and session content. Keep anonymised therapy program documentation as required by RPWD Act 2016." [Confirm — leads to B3-07 partial erasure confirmation]
  - **Option C — Defer for legal review:** "I need to consult a legal advisor before proceeding. The 30-day DPDPA clock is still running." [Defer — returns to admin queue]
- Informational link: "What does RPWD Act 2016 require?" (opens a plain-language explainer — not a PDF of the Act itself)
- 30-day clock reminder: "Your DPDPA deadline is [date]. You have [N] days remaining."

**States:**
- **Loading state:** Static content; loads immediately.
- **Error state:** If Rahul's selection cannot be written to the server, show: "Could not save your decision — please check your connection and try again." Do not proceed with erasure without a confirmed server write of his decision.
- **Offline state:** This screen requires connectivity. Do not allow erasure decisions to be made offline.
- **Overdue state (day 30+ no decision):** Banner at top: "DPDPA deadline has passed. This erasure request is overdue. Take action immediately or document why processing has been delayed."

**Constraints:**
- Do not make Option B look like the "safe/easy" option by styling it in green or making it visually dominant over Options A and C. All three options are legitimate. The designer should not nudge Rahul toward any particular choice through visual weight.
- The word "recommended" in Option B label should be considered carefully — it may be appropriate (partial erasure is the most legally defensible in most cases) but it should be reviewed by legal before shipping this screen.
- This screen should be desktop-usable. Rahul may want to take notes, consult a legal advisor, and return to it on a laptop. Ensure it renders correctly on desktop Chrome as well as Android.

---

### Screen: Parent Portal — Privacy Settings

**Purpose:** Give Meena a single place to understand her data rights, view her current consent status, and exercise her rights (withdrawal, portability, erasure) — without needing to contact the centre.

**Primary action:** Context-dependent: view consent status / initiate withdrawal / request data download / request erasure.

**Entry point(s):** From parent portal navigation: Account > Privacy.

**Exit point(s):** Each action leads to its respective flow (withdrawal → B1-03, portability → B2-02, erasure → B3-01).

**Key components:**
- "My consent" section: Shows current consent status (Active / Withdrawn), date consent was given, purposes covered (plain language list)
- "Withdraw consent" button (only shown if consent status is Active)
- "Download my child's records" section with plain-language explanation and "Request download" button
- "Request data erasure" section with a warning: "This will permanently delete all records. This cannot be undone." — shown as a tertiary/destructive action, visually de-emphasised relative to the consent and portability sections
- Privacy Notice link: "Read our full privacy notice" — links to DPDPA-003

**States:**
- **Empty state:** Not applicable — Meena only sees this screen if she is logged in and linked to a child.
- **Loading state:** Consent status card shows a skeleton loader while fetching.
- **Error state:** If consent status cannot be fetched: "Unable to load your privacy settings — please check your connection and try again."
- **Offline state:** Show last-cached consent status with a "Data as of [date]" notice. Actions (withdrawal, portability, erasure) require connectivity and should show: "This action requires an internet connection."
- **Post-withdrawal state:** "Withdraw consent" button is replaced with: "Consent withdrawn on [date]. No new records are being created for [child name]." and a "Re-consent" button.

**Constraints:**
- The erasure button should be visually de-emphasised (not a prominent red button). It is a legitimate right but an irreversible action; the UX should not make it easy to trigger accidentally.
- All text in this screen must pass a readability check by a non-technical adult. No legal or clinical terminology without plain-language explanation.
- Touch targets ≥ 44px on all interactive elements.

---

## Developer Handoff

### Step-level Technical Summary — Path A

| Step | Data written | Data read | API / event | Offline behavior | Regulatory gate |
|---|---|---|---|---|---|
| A-01 | child_record (status="pending_consent", required fields only) | None | `POST /children` | Draft saved locally; submission requires connectivity | DPDPA: record creation is the start of personal data processing — consent banner must appear immediately |
| A-02 | None | child_record.status | System state render | Consent banner uses cached status; banner is shown if status ≠ "active" | DPDPA gate: all clinical write endpoints blocked at API layer (return 423) when status = "pending_consent" |
| A-03 | None | consent_notice (current version + content) | `GET /consent-notice/current` | If consent notice version cannot be confirmed from server, block consent capture with connectivity error — do not allow consent to proceed with an unversioned notice | RBAC: Director and Admin roles only can initiate consent capture |
| A-04 | None | consent_notice (version, content for display) | None (static render from fetched notice) | Consent notice must be server-fetched to ensure correct version is displayed and recorded | DPDPA: notice version must be recorded with consent; consent to an unversioned notice is non-compliant |
| A-06 | None (user interaction only) | None | None | N/A — offline consent is blocked | DPDPA: pre-checked checkboxes NOT permitted; affirmative action required |
| A-07 | consent_record (immutable): parent_name, relationship_to_child, consent_datetime_ist, notice_version_id, method, admin_actor_id, device_id | child_record.id | `POST /children/{id}/consent` | Consent cannot be submitted offline — requires server-confirmed timestamp; show connectivity error if offline | DPDPA: if consent_record write fails, originating write is rolled back (atomic transaction); no partial consent state |
| A-08 | child_record.status → "active"; audit_log entry (CREATE, consent_record, actor, "DPDPA high-risk" flag) | consent_record confirmation | State transition via `PATCH /children/{id}/status`; audit_log write (AUDIT-001) | N/A — connectivity required for both writes | AUDIT-001: audit log entry mandatory; if audit log write fails, consent record write must roll back |
| A-09 | None | consent_record (all fields, read-only) | `GET /children/{id}/consent` | Last-cached consent record readable offline in read-only view | RBAC: Director role only can view full consent record detail |
| A-10 | None | child_record.consent_status (for badge) | Included in `GET /children/{id}` response | Consent badge shown from cached child record status | DPDPA: badge is visible to all authorised staff roles; consent record detail restricted to Director |

### Step-level Technical Summary — Path B-i (Withdrawal)

| Step | Data written | Data read | API / event | Offline behavior | Regulatory gate |
|---|---|---|---|---|---|
| B1-01 | None | consent_record (status, date, purposes) | `GET /parent/consent-status` | Last-cached status shown with staleness indicator | RBAC: Parent role — only linked child's data visible |
| B1-04 | consent_withdrawal_record (immutable): actor=parent, datetime_ist, "DPDPA high-risk" flag; child_record.status → "consent_withdrawn" | consent_record.id | `POST /children/{id}/consent/withdraw` | Withdrawal requires connectivity — must be server-confirmed immediately | DPDPA Section 6(4): must not be delayed, blocked, or require justification beyond confirmation step; platform target: immediate |
| B1-05 | audit_log entry (CONSENT_WITHDRAWAL, actor, "DPDPA high-risk" flag); notifications sent to Rahul and Dr. Sunita | None | AUDIT-001 event; `POST /notifications` | N/A — connectivity required for all writes | All clinical write endpoints return 423 again for this child |
| B1-08 (re-consent) | new_consent_record (separate, does not modify withdrawal record) | withdrawal_record.id, child_record.id | `POST /children/{id}/consent` (same as A-07) | Same as A-07 | New consent record is created alongside the withdrawal record — both immutable; consent history shows full timeline |

### Step-level Technical Summary — Path B-iii (Erasure)

| Step | Data written | Data read | API / event | Offline behavior | Regulatory gate |
|---|---|---|---|---|---|
| B3-03 | erasure_request (actor=parent, datetime, "DPDPA high-risk" flag); child_record.status → "erasure_requested"; admin_task created for Rahul | consent_record.id | `POST /children/{id}/erasure-request`; AUDIT-001 | Erasure request requires connectivity | DPDPA Section 12(c): 30-day processing window begins at this timestamp |
| B3-05 | None (human review step — system surfaces conflict, does not write) | child_record.has_therapy_programs (determines if RPWD conflict applies) | `GET /children/{id}/erasure-review` | Connectivity required | ⚠️ DPDPA/RPWD conflict: system surfaces; human must decide |
| B3-06 | erasure_decision_record (immutable): Rahul_actor_id, decision (A/B/C), datetime, rationale | erasure_request.id | `POST /children/{id}/erasure-decision` | Connectivity required — decision must be server-confirmed | AUDIT-001: decision is logged as a "DPDPA high-risk" event regardless of which option Rahul chooses |
| B3-07 (Option A — full erasure) | Hard deletes from active storage: session_notes, therapy_programs, soap_notes, intake_data, documents, clinical_assessments. Retains: anonymised_erasure_log entry only. | All child record tables | `DELETE /children/{id}` (cascades to all clinical tables) | Connectivity required | DPDPA Section 12(c): clinical data gone from active storage. Consent record retained in audit_log as an anonymised hash (not deletable — it is evidence of lawful processing). |
| B3-07 (Option B — partial erasure) | Deletes: contact_fields, session_content, notes_free_text. Anonymises and retains: therapy_program_structure (without PII). Adds retention_justification note. | All child record tables | `PATCH /children/{id}/partial-erasure` | Connectivity required | DPDPA + RPWD: partial retention documented; parent notified of what was retained and why |
| B3-08 | audit_log entry: erasure_complete, method (full/partial), actor (Rahul), datetime; parent_portal status update | None | AUDIT-001; `PATCH /parent/portal/erasure-status` | N/A | Final audit log entry; Meena's portal reflects completion |

**Key state transitions:**
- child_record transitions: `pending_consent` → `active` (at A-08) → `consent_withdrawn` (at B1-05) → `erasure_requested` (at B3-03) → `erased` (at B3-07) / re-enters `active` on new consent (at B1-08)
- consent_record transitions: no state transitions — immutable from creation. New events are appended (withdrawal, re-consent) as separate immutable records, never modifying the original.
- All state transitions are logged as AUDIT-001 events with "DPDPA high-risk" flag.

**Background jobs / async events triggered by this journey:**
- **Consent withdrawal notification job:** triggered at B1-04; delivers in-app notifications to Rahul and Dr. Sunita within 60 seconds
- **Data portability PDF generation job:** triggered at B2-03; generates PDF in background; delivers in-app notification to Meena when ready (target: < 24 hours for large records)
- **Erasure deadline reminder job:** triggered at B3-03; fires in-app reminders to Rahul at day 15, day 25, day 30 from erasure request timestamp
- **Partial erasure anonymisation job:** triggered at B3-07 (Option B); anonymises retained therapy program records in background; confirms completion to Rahul's admin queue

**DPDPA compliance checkpoints:**
- Step A-01: ⚠️ DPDPA — creating a child record begins processing personal data of a minor; consent gate must activate immediately
- Step A-07: ⚠️ DPDPA — consent_record write is the compliance mechanism; atomic transaction required; server timestamp is legally significant
- Step A-08: ⚠️ DPDPA — audit_log write is mandatory and non-optional; if audit log fails, consent write rolls back
- Step B1-04: ⚠️ DPDPA Section 6(4) — withdrawal must not be delayed; platform must process within the same session
- Step B2-03: ⚠️ DPDPA Section 12 — data portability is a mandatory right; request must not be blocked or require justification
- Step B3-03: ⚠️ DPDPA Section 12(c) — erasure request accepted immediately; 30-day clock starts at server-confirmed timestamp
- Step B3-05: ⚠️ DPDPA/RPWD conflict — human decision required; engineering must not auto-resolve
- Step B3-07: ⚠️ DPDPA — erasure must result in actual deletion from active storage; soft-delete is NOT sufficient for an erasure request; the consent_record audit entry is the only data that must be retained (as evidence of lawful processing)

---

## Cross-Journey Dependencies

| Depends on journey | Why | What breaks if missing |
|---|---|---|
| **This journey is a prerequisite gate for every other clinical journey in the product** | DPDPA 2023 Section 9 requires verifiable parental consent before any health data of a minor is stored or processed. Without confirmed consent, no clinical data can be written. | Journey 4 (Clinical Program Design): therapy programs cannot be created. Journey 6 (Post-Session Documentation): session notes cannot be written. Journey 8 (Progress Reporting): progress reports cannot be generated. Journey 3 (Scheduling & Attendance): sessions can be scheduled but not documented. All clinical features in Clusters 1, 2, 3, 4 return 423 (Locked) for any child without confirmed consent. |
| Journey 2 — Child Enrollment & Onboarding | The child record (EMR-001) must exist before consent can be captured. Consent is step 2 in the enrollment journey, not step 1. | If the child record does not exist, there is no record to attach the consent event to. Path A cannot start. |
| RBAC setup (RBAC-001) | Consent capture is a Director/Admin action. Parent portal actions (withdrawal, portability, erasure) require Parent role. If RBAC is not configured, role-based access to consent screens cannot be enforced. | Without RBAC: any staff member could attempt to initiate or view consent records. The Director-only consent audit log view (DPDPA-005) would be accessible to all roles. The parent portal could not be scoped to Meena's child only. |
| Audit Trail infrastructure (AUDIT-001) | Every consent event, withdrawal, erasure request, and erasure decision must be written to the immutable audit log. AUDIT-001 is the infrastructure that makes this possible. | Without AUDIT-001: consent events are not logged. The consent audit log export (DPDPA-005) has nothing to display. DPDPA accountability obligations cannot be met. Export actions (EXPORT-001, EXPORT-003, EXPORT-004) are unlogged. |
| Parent Portal (RBAC-005) | Path B (all data subject rights flows) requires Meena to have a parent portal account. Without a functioning parent portal, Meena cannot self-serve her DPDPA rights — all requests must be mediated by Rahul, increasing his admin burden and creating response-time risk. | Without parent portal: Meena cannot withdraw consent, request portability, or request erasure independently. All rights must be handled by Rahul via manual process, increasing DPDPA response-time risk. |
| 2FA / Auth (AUTH-001) | Parent portal login for Path B requires authenticated access. Without 2FA, a stolen or guessed password gives an attacker access to withdrawal and erasure controls — the most destructive actions in the product. | Without AUTH-001: parent portal login is single-factor; a guessed password could trigger consent withdrawal or erasure. The audit trail records who triggered these actions — but if the account was compromised, the actor ID is meaningless. |

---

## ⚠️ Feature Factory Disclaimer

These flows were defined by document synthesis from DPDPA 2023 statutory text, story files from Clusters 1, 2, and 5, and category observation of consent management patterns in US health SaaS tools (adapted to the Indian regulatory context) — not by validated primary user research with Indian therapy centre directors, parents, or legal counsel.

**What we assumed but haven't validated:**

- [ASSUMPTION] Indian therapy centre directors (Rahul) are aware of DPDPA 2023 as a live compliance obligation and understand that they are data fiduciaries responsible for managing parental consent for minors' health data. Hypothesis H-06 in the journey map rates this as high-uncertainty, high-risk. No primary research has confirmed DPDPA awareness among Indian therapy centre directors as of April 2026.
- [ASSUMPTION] Indian parents (Meena) will engage with a structured digital consent flow at intake rather than treating it as an obstacle. The tech literacy and willingness-to-engage with digital consent on a tablet or phone have not been tested with actual Indian therapy centre parents.
- [ASSUMPTION] The plain-language privacy notice as designed (English, 6 sections, no clinical jargon) will be understood by a non-technical Indian parent at the reading level of a typical mother bringing a child to a private therapy centre. This has not been user-tested.
- [ASSUMPTION] The RPWD Act 2016 creates a real, felt retention obligation for therapy programme documentation that meaningfully constrains full erasure in practice. The specific retention period and the documentation types covered by RPWD Act have not been confirmed with Indian legal counsel — the conflict surfaced at B3-05 is based on a structural reading of the two statutes, not a formal legal opinion.
- [ASSUMPTION] The 30-day DPDPA erasure processing target is achievable for Rahul operationally. If a centre has 30+ erasure requests simultaneously (unlikely but possible at scale), the admin burden of processing each individually may not be sustainable.
- [ASSUMPTION] The parent portal (Meena logging in to exercise her rights) is a realistic user journey. Meena's digital comfort level — specifically whether she will create a platform account, remember login credentials, and navigate a privacy settings screen — has not been validated. In practice, most data subject rights requests in Indian contexts may arrive via WhatsApp or phone call, not through a self-service portal.
- [ASSUMPTION] Staff-assisted verbal consent (Path A-iv, Option iii) is an acceptable fallback that centres will use responsibly and follow up to obtain digital consent. The rate at which "verbal consent" gets upgraded to digital consent at the next visit is unknown.

**What a researcher would ask before building this:**

- Have Indian therapy centre directors ever received a DPDPA inquiry, complaint, or regulatory contact? What is their current awareness of DPDPA 2023 obligations for minors' health data? (Directly tests H-06.)
- Can we observe an actual intake session at a centre and test whether a parent — typical Indian mother at a private autism therapy centre — understands and engages with a consent screen on a tablet? What does she do when shown the privacy notice? Does she read it? Does she ask questions?
- What does RPWD Act 2016 actually require in terms of documentation retention, in the specific context of private therapy centres? Get a formal legal opinion on the conflict between DPDPA erasure rights and RPWD Act retention obligations before shipping the erasure review screen (B3-05).
- What proportion of consent withdrawals in a centre's first year of operation are expected to result in erasure requests? This shapes how much engineering weight to put on the erasure flow vs. the consent capture flow.

**What the Product Consultant would challenge:**

- The full erasure flow (Path B-iii) is a high-complexity, high-stakes feature that is unlikely to be exercised frequently in the first 12 months of product deployment. The more common and urgent compliance need is Path A (consent capture at intake) — which is the gate for every other feature in the product. Consider whether the erasure flow (B3-01 through B3-08, including the RPWD conflict screen) should be deferred to Phase 2, and whether Phase 1 consent management should cover: capture (DPDPA-001), withdrawal (DPDPA-002), privacy notice (DPDPA-003), and audit log (DPDPA-005) — with portability (EXPORT-004) and erasure (DPDPA-004) following in the next sprint.
- The parent self-service portal for data subject rights (Path B via parent portal login) assumes Meena will create and use a platform account. If parent portal adoption is low, all data subject rights requests will arrive by WhatsApp or phone call and Rahul will need to process them manually anyway. Consider building a simple admin-mediated data subject rights workflow (Rahul receives a request via WhatsApp, processes it in the admin panel) before building the self-service parent portal path.

**Risk level per output:**

- **Low risk (regulatory non-negotiable regardless of user research):** Path A — consent capture (DPDPA-001), privacy notice (DPDPA-003), audit trail (AUDIT-001). These are required before any child health data can legally exist in the system. Not building them is not an option.
- **Medium risk (compliance-driven but uncertain in practice):** Consent withdrawal (DPDPA-002), consent audit log (DPDPA-005), data portability (EXPORT-004). Real DPDPA obligations; less certain whether the specific self-service flows designed here match how Indian parents will actually exercise these rights.
- **High risk (legally complex, operationally uncertain):** Full and partial erasure (DPDPA-004), RPWD conflict handling (B3-05). High legal complexity; the RPWD/DPDPA tension requires a formal legal opinion before the screen can be finalised. The operational frequency of erasure requests in the Indian therapy centre market has not been estimated.

Use the `/research` agent to validate DPDPA awareness (H-06), parent consent UX comprehension, and the RPWD Act retention obligation before sprint planning.
Use the `/product-consultant` agent to challenge whether the full erasure flow should be deferred to Phase 2 and whether admin-mediated data subject rights processing is a more pragmatic Phase 1 approach.
Use the `/design-critique` agent to review the Privacy Notice screen and the Erasure Review screen before any prototyping — both involve high-stakes interactions that must be legible to non-technical users on low-end Android hardware.

---

*Generated by: Mindless Product Owner agent — Mode 2 (User Journey Definition)*
*Date: 2026-04-17*
*Source documents:*
- *`products/autism-therapy-platform/prds-and-stories/mindless-product-owner/cluster-5-analytics-compliance-access.md`*
- *`products/autism-therapy-platform/prds-and-stories/mindless-product-owner/cluster-2-patient-records-intake.md`*
- *`products/autism-therapy-platform/prds-and-stories/mindless-product-owner/cluster-1-clinical-documentation.md`*
- *`products/autism-therapy-platform/research/journey-map.md`*
- *`products/autism-therapy-platform/CLAUDE.md`*
