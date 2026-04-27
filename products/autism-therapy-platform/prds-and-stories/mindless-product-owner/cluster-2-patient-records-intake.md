# Cluster 2: Patient Records, Intake & Multi-Practitioner Management
**Product:** Autism Therapy Platform (India)
**Agent:** Mindless Product Owner
**Date:** 2026-04-16
**Cluster scope:** Custom Intake Forms · ABDM/ABHA Integration · Multi-Therapist/Multi-Doctor Management
**Explicitly OUT OF SCOPE:** In-session trial-by-trial data collection (DTT/NET)
**Journey stages served:** Stage 2 (Intake & Enrollment), Stage 3 (Program Design), Stage 5 (Supervisor Review), Stage 6 (Progress Reporting — ABDM records)

> **Note on competitor research:** The four Tavily search queries specified in the task brief require Bash CLI access, which is not available in this session. The Feature Inspiration Table below is constructed from: (1) the competitive analysis in `research/secondary/competitive-analysis-autism-therapy-software.md`, (2) known product capabilities of CentralReach, SimplePractice, Jane App, TheraNest, Hi Rasmus, and PractiPal based on their public product pages and documentation, and (3) ABDM/ABHA official NHA documentation. Evidence levels are marked accordingly.

---

## Feature Inspiration: Patient Records, Intake & Multi-Practitioner Management

| Feature | Competitor(s) | Prevalence | How it works | Evidence |
|---|---|---|---|---|
| Digital intake forms with configurable fields | CentralReach, SimplePractice, Jane App, TheraNest, PractiPal | Table stakes (US); absent in India | Center or practice admin configures a form template; families complete digitally before or at first appointment; data maps into the client record automatically | ✅ CentralReach, SimplePractice, Jane App product pages confirm configurable intake |
| DPDPA / consent capture at intake | No Indian tool has this | Differentiator (India) | Consent for data processing of a minor collected as a verifiable digital signature or checkbox with timestamp; stored against the child's record | 🔵 Inferred from DPDPA 2023 Section 9 requirements; no Indian center tool currently provides this |
| UDID / disability certificate capture | No tool — India-specific | Novel | Structured field at intake for UDID number + certificate upload; reminder if missing | 🔶 Inferred from India Autism Center UDID documentation workflow |
| Prior diagnosis / therapy history intake | CentralReach, SimplePractice, Jane App, Hi Rasmus | Table stakes (US) | Structured form fields capturing diagnosis type, date, referring clinician, prior therapy duration and outcomes | ✅ Confirmed in CentralReach and Jane App onboarding documentation |
| Document upload at intake (diagnosis reports, school records) | CentralReach, Jane App, SimplePractice | Table stakes (US); absent in Indian tools | Family uploads scanned documents; stored against child's record with document type labels | ✅ Confirmed in Jane App and CentralReach client portal documentation |
| National health ID / EMR number linking | ABDM/ABHA (India) | Novel — India-specific regulatory integration | Child's ABHA (Ayushman Bharat Health Account) health ID is linked to their center record; clinical records can be pushed to the ABDM health locker as FHIR-compliant health documents | ✅ ABDM/NHA official documentation; no clinic software in the Indian therapy center market is documented as ABDM-integrated |
| ABDM-compliant health record generation | ABDM Health Information Framework | Novel — India-specific | Session records and progress reports formatted as FHIR R4 ABDM health records and pushed to the child's ABHA health locker | 🔵 Inferred from NHA ABDM Health Information Provider (HIP) specifications |
| Multi-staff assignment to a client record | CentralReach, Hi Rasmus, TheraNest, Jane App | Table stakes (US); absent in Indian tools | A child's record can have a primary therapist, supervisor, shadow teacher, and additional staff assigned; each role has defined access level | ✅ CentralReach and TheraNest client record assignment confirmed |
| Role-based record access control | CentralReach, SimplePractice, Jane App | Table stakes (US) | Staff see only the children assigned to them; supervisors see all children under their supervision; director has full access | ✅ Confirmed in CentralReach and SimplePractice permissions documentation |
| Caseload visibility dashboard for supervisors / directors | CentralReach, Hi Rasmus, Theralytics | Differentiator (US) | A view showing all active clients, their assigned therapist(s), last session date, and any open action items (program updates due, reports overdue) | 🔵 Inferred from CentralReach and Hi Rasmus supervisor dashboard descriptions |
| Staff handover / co-treatment notes | Hi Rasmus, CentralReach | Differentiator | Structured handover note when a child's primary therapist changes; version-stamped so the receiving therapist sees previous therapist's notes | 🔵 Inferred from Hi Rasmus supervision workflow documentation |

---

## Feature Brief: Custom Intake Forms

**Inspired by:** CentralReach, SimplePractice, Jane App, TheraNest, Hi Rasmus
**Prevalence:** Table stakes (US market); absent in India — no Indian therapy center tool has configurable digital intake with DPDPA-compliant consent
**Target user:** Rahul (Center Director — configures forms); Dr. Sunita (reviews completed intake data); Meena (completes the form at or before the intake appointment)
**What it does:** Allows the center director or admin to configure a digital intake form template for new child enrollments. The form captures developmental history, diagnosis details, prior therapy history, family background, and UDID/disability certificate details. DPDPA 2023-compliant parental consent for digital processing of a minor's health data is embedded as a mandatory, verifiable step. Families can complete the form on a tablet at the center or on their own Android device before the appointment. Completed data maps directly into the child's record.
**What "done" looks like:** A new family completes a fully digital intake form — including DPDPA consent — without staff needing to transcribe anything. The child's record is pre-populated from intake data before the first assessment session begins.

**[ASSUMPTION — NOT VALIDATED]** This feature assumes that Indian autism therapy centers currently capture intake data on paper or verbally, and that digitizing this process will reduce admin burden and compliance risk. No primary research has confirmed the depth of the intake gap or whether parents in this market will complete a digital form without assistance. Validate before committing engineering capacity.

---

## Feature Brief: ABDM / ABHA Compliant Health Records

**Inspired by:** ABDM / NHA (Ayushman Bharat Digital Mission — National Health Authority, Government of India)
**Prevalence:** Novel — no autism therapy center management software in India is documented as ABDM-integrated. This is an India-specific regulatory integration with no US equivalent. Do not apply US EMR or HL7 FHIR US Core comparisons — use the ABDM Health Information Framework (FHIR R4, India profile).
**Target user:** Rahul (Center Director — enables ABDM integration for the center, acts as Health Information Provider); Dr. Sunita (generates ABDM-compliant progress records); Meena (links her child's ABHA ID; benefits from a portable health record)
**What it does:** The platform acts as an ABDM Health Information Provider (HIP). At intake, the child's ABHA (Ayushman Bharat Health Account) health ID is collected and linked to their center record. Therapy records and progress reports generated on the platform can be pushed to the child's ABHA health locker as FHIR R4-compliant health documents. Parental consent for ABDM health data sharing is captured in-app as part of the ABDM consent flow.
**What "done" looks like:** A center registered as an ABDM HIP can link a child's ABHA ID during intake, generate a FHIR-compliant health document from a progress report, and push it to the child's ABHA health locker — with a verifiable consent audit trail.

**[ASSUMPTION — NOT VALIDATED]** This feature assumes: (1) Indian autism therapy centers will benefit commercially or regulatorily from ABDM registration; (2) ABHA adoption among families attending private therapy centers is or will be sufficient to make this integration useful at launch; (3) the ABDM HIP registration and FHIR compliance burden is manageable within the ATP engineering roadmap. None of these assumptions have been validated. ABDM adoption is growing but penetration among private therapy center families is unknown. Validate ABHA awareness and uptake with center directors before scheduling.

---

## Feature Brief: Multi-Therapist / Multi-Doctor Management

**Inspired by:** CentralReach, TheraNest, Hi Rasmus, Jane App
**Prevalence:** Table stakes (US market); absent in all Indian therapy center tools reviewed
**Target user:** Rahul (Director — assigns staff to children, monitors caseloads); Dr. Sunita (Supervisor — reviews records of all children under her supervision, manages handovers); Priya (Therapist — sees her assigned caseload, receives handover notes)
**What it does:** A child's record can be assigned to multiple staff members simultaneously — a primary therapist, a clinical supervisor, a shadow teacher (if applicable), and additional co-treating staff. Each role has defined access permissions. When a child's primary therapist changes, a structured handover workflow is triggered. The center director has a caseload dashboard showing all active children, their assigned staff, and key status flags (last session, open program updates, overdue reports).
**What "done" looks like:** Rahul can see, in a single view, every active child and which staff are assigned to them. Dr. Sunita receives a handover package when she takes over a child or when a new therapist joins a child's care team. Priya sees only the children she is assigned to.

**[ASSUMPTION — NOT VALIDATED]** This feature assumes Indian autism therapy centers have multi-staff assignment complexity significant enough to warrant a structured tool — i.e., that children are routinely seen by more than one therapist and that handovers cause meaningful quality or continuity problems. This is more likely in centers with 5+ staff; may not be a pain point in very small (2–3 staff) centers. Validate center size distribution and handover frequency in director interviews.

---

## Epic: Custom Intake Forms

**Goal:** Enable centers to replace paper-based and verbal intake with a configurable digital form that captures structured child data and DPDPA-compliant parental consent at enrollment — so that the child's record is populated from day one without manual transcription.
**Copied from:** CentralReach (intake forms + consent capture), SimplePractice (configurable intake templates), Jane App (client intake with document upload)
**Target user(s):** Rahul (configures forms), Meena (completes forms), Dr. Sunita (reviews intake data), Admin staff (manages completion status)
**Definition of Done:**
- Center admin can create and publish a custom intake form template
- Families can complete the form on a shared tablet at the center or on their own Android device
- DPDPA-compliant parental consent is captured as a required, verifiable step before form submission
- Completed intake data is automatically written to the child's record with no manual transcription
- UDID number and disability certificate can be captured and stored
- Prior documentation (diagnosis report, school records, previous therapy reports) can be uploaded as attachments
- Form completion status is visible to admin (completed / pending / not sent)
- All child health data stored under this epic is tagged for DPDPA compliance audit

**Out of scope (this epic):**
- In-session data collection of any kind
- Assessment forms (ISAA, CARS, Vineland) — these are a separate Epic in the Assessment cluster
- ABDM/ABHA linking — covered in the ABDM Epic
- Multi-language form support — Phase 2
- Parent portal / ongoing parent communication — separate cluster
- Fee agreement or billing at intake — separate billing cluster
- Automated appointment reminders — separate cluster

**[ASSUMPTION — NOT VALIDATED]** This epic assumes that families at Indian autism therapy centers are willing and able to complete a digital form on a tablet or Android device, either independently or with minimal staff assistance. The tech literacy level required to complete a form has not been tested with Indian therapy center parents.

---

### Story INT-001: Configure a custom intake form template

**As a** Rahul (Center Director)
**I want to** create and configure a digital intake form template for new child enrollments, selecting which fields are required vs. optional and adding center-specific questions
**So that** every new family completes a consistent intake form that captures the data my center needs, without staff having to remember what to ask

**Inspired by:** Jane App (configurable intake form builder), SimplePractice (template-based intake)

**Context:** Rahul is setting up the platform for the first time, or updating the intake template after his center changes its intake protocol. He is on a desktop or Android device, not in a session room. This is an admin-mode action.

**Acceptance Criteria:**
- [ ] AC-01: Given Rahul is logged in as Center Director or Admin, when he opens the Intake Forms settings section, then he sees a form builder interface showing the current active template (or a blank template if none exists)
- [ ] AC-02: Given Rahul is in the form builder, when he adds a field, then he can choose from field types: short text, long text, date, number, single-select dropdown, multi-select checkbox, file upload, and section header
- [ ] AC-03: Given Rahul configures a field, when he sets it as Required, then the system prevents form submission if that field is blank
- [ ] AC-04: Given Rahul adds a field, when he labels it, then the label accepts up to 200 characters and supports Unicode (for Hindi field labels in Phase 2 readiness)
- [ ] AC-05: Given Rahul saves the template, when any new intake form is opened for a new child, then it uses the latest saved template version
- [ ] AC-06: Given Rahul publishes a new template version, when there are in-progress intake forms using the old template, then those in-progress forms are NOT changed mid-completion; the new template applies only to forms opened after publish
- [ ] AC-07: Given the form template, when Rahul previews it, then he sees a rendered form view matching exactly what families will see
- [ ] AC-08: Given a saved template, when Rahul attempts to delete the only active template, then the system prevents deletion and shows an explanatory message: "At least one active intake template is required"

**Edge Cases & Error States:**
- [ ] EC-01: If Rahul closes the browser or app mid-configuration without saving, then auto-save of the draft is preserved and a "Resume draft" prompt appears on next open
- [ ] EC-02: If two admin users edit the template simultaneously, then the system shows a conflict warning: "Another admin is editing this template. Your changes may overwrite theirs." — last-write-wins with a conflict timestamp in the audit log
- [ ] EC-03: If a required field type (file upload) is added but the device has insufficient storage, then the field gracefully degrades to show an error and allows the user to skip the upload with a note

**Non-Functional Requirements:**
- Performance: Form builder loads within 3 seconds on a mid-range Android device (2GB RAM, Android 10+)
- Offline: Form template editing requires internet connectivity; clear "offline — changes cannot be saved" state shown if connection is lost during editing
- Accessibility: All form builder controls have touch targets ≥ 44px; field labels are screen reader-compatible
- Privacy: ⚠️ DPDPA — the template itself does not contain child health data; no DPDPA tagging required on the template configuration. DPDPA tagging applies at the data-submission step (INT-003)

**Dependencies:**
- Blocked by: None (foundational)
- Enables: INT-002, INT-003, INT-004, INT-005

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android (Redmi/Realme, 2GB RAM, Android 10+)
- [ ] Edge cases tested
- [ ] Code reviewed and merged

---

### Story INT-002: Complete the intake form as a family (tablet / Android)

**As a** Meena (Parent / Primary Caregiver)
**I want to** complete my child's intake form on a tablet at the center (or on my own Android phone before the appointment)
**So that** I only have to provide my child's details once, in a structured way, without repeating myself verbally to multiple staff members

**Inspired by:** Jane App (client-facing intake completion), SimplePractice (client portal intake forms)

**Context:** Meena is at the center for the first appointment, or she has received a link via WhatsApp before the appointment. She is using a shared center tablet or her own Android phone. She is not technically confident; the form must be self-explanatory.

**Acceptance Criteria:**
- [ ] AC-01: Given an intake form has been prepared for Meena's child, when Meena opens the form link (or the form is opened on the center tablet by a staff member), then she sees the form rendered in a clean, single-column layout optimized for mobile
- [ ] AC-02: Given Meena is completing the form, when she reaches a required field and attempts to proceed past it without answering, then the field is highlighted in red with the message "This field is required" in English (Hindi in Phase 2)
- [ ] AC-03: Given Meena completes all fields and reaches the end of the form, when she taps Submit, then she first sees the DPDPA consent screen (Story INT-003) before final submission is accepted
- [ ] AC-04: Given Meena partially completes the form and the session is interrupted (phone call, connection loss), when she reopens the form link within 48 hours, then her partial answers are restored
- [ ] AC-05: Given the form includes a file upload field (e.g., diagnosis report), when Meena taps the upload field, then she can select a file from her phone storage or take a photo directly; supported formats: PDF, JPG, PNG; max file size: 10MB per file
- [ ] AC-06: Given Meena submits the form successfully, when submission is confirmed, then she sees a success screen with the message: "Thank you. Your child's details have been received. [Center name] will contact you shortly." — no clinical data echoed back on this screen
- [ ] AC-07: Given the form is opened on a shared center tablet, when Meena submits, then the form automatically clears and returns to a neutral state (no personal data visible to the next user who opens the device)

**Edge Cases & Error States:**
- [ ] EC-01: If Meena's internet connection drops mid-form, then the form saves her current progress locally and shows: "No connection — your answers are saved. Submit when you have internet."
- [ ] EC-02: If the form link has expired (older than 7 days), then Meena sees: "This link has expired. Please ask [Center name] to resend your intake form." — not a blank error page
- [ ] EC-03: If a file upload fails (file too large, unsupported format), then the specific upload field shows an error; the rest of the form remains valid and submittable without the file, unless the field is marked Required
- [ ] EC-04: If Meena attempts to submit without completing a Required field that was skipped by scrolling, then the form scrolls to the first incomplete required field and highlights it

**Non-Functional Requirements:**
- Performance: Form renders within 2 seconds on a mid-range Android (2GB RAM, 4G connectivity); file upload progress bar shown for uploads > 2 seconds
- Offline: Partial form answers saved locally; submission requires connectivity
- Accessibility: Touch targets ≥ 44px; font size minimum 16px for readability; no color-only error indication (icon + text label used alongside red border)
- Privacy: ⚠️ DPDPA — form data contains child health information and parent PII; data transmitted over HTTPS only; stored encrypted at rest; consent must be captured before data is permanently written to the child's record (INT-003 dependency)

**Dependencies:**
- Blocked by: INT-001 (form template must exist), INT-003 (DPDPA consent must be captured at submission)
- Enables: INT-004 (data writes to child record), INT-005 (document storage)

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android (Redmi/Realme, 2GB RAM, Android 10+)
- [ ] Tested with a form containing all supported field types
- [ ] File upload tested with PDF, JPG, and PNG; error states tested for oversized files
- [ ] Edge cases tested
- [ ] Code reviewed and merged

---

### Story INT-003: Capture DPDPA-compliant parental consent at intake

**As a** Rahul (Center Director)
**I want to** collect verifiable digital parental consent for processing my child patient's health data — as required under DPDPA 2023 — at the point of intake form submission
**So that** the center has a legally defensible consent record and is not exposed to DPDPA compliance risk when storing and processing a minor's health data

**Inspired by:** DPDPA 2023 (Section 9 — processing of personal data of a child; Section 6 — consent requirements); no direct competitor has India-specific DPDPA consent flows; closest analogy is HIPAA consent capture in US tools (CentralReach, SimplePractice) which must NOT be used as the compliance framework here

**Context:** This story is triggered at the final step of the intake form (INT-002). Meena has completed the form fields and is about to submit. Before submission is accepted, she must provide verifiable consent. This is a regulatory requirement, not a UX nicety.

**Acceptance Criteria:**
- [ ] AC-01: Given Meena reaches the end of the intake form and taps Submit, when the consent screen appears, then it displays a plain-language summary (not legal jargon) of: (a) what data is being collected, (b) why it is being processed, (c) who will have access to it within the center, (d) how long it will be retained, and (e) how the parent can withdraw consent
- [ ] AC-02: Given Meena is on the consent screen, when she must confirm consent, then the consent mechanism is an explicit affirmative action: a checkbox labeled "I give consent for [Center name] to collect and process my child's health data as described above" — pre-checked checkboxes are NOT permitted
- [ ] AC-03: Given Meena checks the consent checkbox and taps Confirm, when the system records the consent, then it stores: parent name, parent contact number, child name, date and time of consent (IST), form version ID, and the platform version — creating an immutable consent record
- [ ] AC-04: Given consent is stored, when the center or a parent requests a consent audit record, then an admin can export a PDF showing all fields from AC-03 for that specific consent event
- [ ] AC-05: Given Meena does NOT check the consent checkbox, when she taps Confirm, then the system does NOT submit the form; it shows: "Consent is required to proceed. We cannot collect or store your child's health data without your agreement." with an explanation link
- [ ] AC-06: Given consent is stored, when the child's record is opened by any staff member, then a "DPDPA Consent: Confirmed [date]" badge is visible in the record header
- [ ] AC-07: Given a parent wishes to withdraw consent at a later date, when Rahul processes the withdrawal in the admin panel, then the system flags the child's record as "Consent Withdrawn — data processing suspended" and surfaces this to all staff with access to the record

**Edge Cases & Error States:**
- [ ] EC-01: If the consent screen fails to load (connectivity issue), then the form does not submit silently; the user sees: "Unable to load consent screen. Please check your connection and try again." — no health data is written without confirmed consent
- [ ] EC-02: If a staff member (not the parent) is completing the form on the center's behalf, then the consent step still requires identification of the consenting party; the staff member must enter the parent's name and confirm they have obtained verbal consent; this is flagged as "Staff-assisted consent — verbal" in the audit record, with a follow-up prompt to obtain digital consent at next visit
- [ ] EC-03: If the consent record fails to write to the database (server error), then the form submission is rolled back entirely; no partial data is stored; the user sees: "Something went wrong. Your information has not been saved. Please try again or ask a staff member for help."

**Non-Functional Requirements:**
- Performance: Consent screen loads within 1 second (it is a simple static screen; no complex data fetch required)
- Offline: Consent cannot be accepted offline — consent record must be written to the server with a server timestamp to be legally defensible; if offline, show: "An internet connection is required to complete consent. Your form answers are saved and will be here when you reconnect."
- Accessibility: Consent text minimum font size 16px; checkbox touch target ≥ 44px; consent text must be readable by a screen reader in full
- Privacy: ⚠️ DPDPA — this story IS the DPDPA compliance mechanism; the consent record is the most legally sensitive data in the system; stored with write-once, immutable audit log; never deletable even if child record is deleted (retention period per DPDPA guidance)

**Dependencies:**
- Blocked by: INT-001 (form must exist), INT-002 (form completion flow)
- Enables: INT-004 (child record population is gated on this), all downstream clinical stories in the platform

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android (Redmi/Realme, 2GB RAM, Android 10+)
- [ ] Consent record verified as immutable in DB — update and delete operations blocked at schema level
- [ ] Consent audit PDF export tested
- [ ] Consent withdrawal flow tested end-to-end
- [ ] Legal/compliance review of consent language signed off before shipping
- [ ] Edge cases tested
- [ ] Code reviewed and merged

---

### Story INT-004: Auto-populate child record from completed intake form

**As a** Dr. Sunita (Clinical Supervisor)
**I want to** open a newly enrolled child's record and find it already populated with their developmental history, diagnosis details, prior therapy history, and family background from the intake form
**So that** I can begin assessment and program design without having to ask the family for information that was already collected at intake

**Inspired by:** CentralReach (intake-to-record mapping), Jane App (client intake populating client profile), TheraNest (intake forms auto-creating client records)

**Context:** Dr. Sunita opens the child's record after the family has completed the intake form and consent has been confirmed (INT-003). She is on a desktop or Android device, in her office or between sessions.

**Acceptance Criteria:**
- [ ] AC-01: Given a family has submitted an intake form with confirmed DPDPA consent, when Dr. Sunita opens the child's record, then the record Profile tab displays all answered intake fields in clearly labeled sections: Child Details, Developmental History, Diagnosis, Prior Therapy History, Family Background, Documents, UDID
- [ ] AC-02: Given the intake form included a UDID number field, when the UDID field was completed, then the child's record displays a "UDID: [number]" field in the Profile tab; if the UDID field was blank, then the record shows "UDID: Not provided" with a flag icon and a prompt to collect at next visit
- [ ] AC-03: Given the intake form included file uploads (diagnosis report, school records), when the form was submitted, then the uploaded files appear in a Documents section on the child's record, labeled by document type and upload date
- [ ] AC-04: Given the child's record is populated, when Dr. Sunita edits a field in the record (e.g., updates the diagnosis date after reviewing the report), then the edited value is saved as the current value; the original intake form response is preserved in a read-only intake submission view (audit trail)
- [ ] AC-05: Given the intake data is displayed, when a required field was left blank by the family, then the record shows "Not provided" for that field — not an empty cell or null — with a flag indicating it should be collected

**Edge Cases & Error States:**
- [ ] EC-01: If consent was recorded as "Staff-assisted verbal" (EC-02 from INT-003), then the child's record displays a banner: "Full digital consent pending — collect at next visit" until proper digital consent is confirmed
- [ ] EC-02: If a file upload in the intake form was corrupted or failed silently, then the Documents section shows the document name with a "Upload failed — please re-upload" status, not a broken link

**Non-Functional Requirements:**
- Performance: Child record loads within 3 seconds including intake data and document thumbnails, on 4G connectivity
- Offline: Child record is readable offline if previously loaded; document downloads require connectivity; edits made offline sync when connection is restored with a sync timestamp
- Privacy: ⚠️ DPDPA — child record contains sensitive health data of a minor; access is role-gated (staff must be assigned to this child OR be the center director/supervisor to view); access log maintained per record

**Dependencies:**
- Blocked by: INT-003 (consent required before data write)
- Enables: All clinical stories (program design, session recording, progress reporting), ABDM-001 (ABHA linking uses the child record), MPM-001 (staff assignment uses the child record)

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android (Redmi/Realme, 2GB RAM, Android 10+)
- [ ] Intake data visible across all supported field types
- [ ] Document upload and retrieval tested
- [ ] Audit trail of original intake submission verified as read-only
- [ ] Edge cases tested
- [ ] Code reviewed and merged

---

### Story INT-005: Track intake form completion status (admin view)

**As a** Rahul (Center Director)
**I want to** see which newly enrolled families have completed their intake forms and which have not
**So that** I can follow up with incomplete families before their first appointment and avoid starting assessments with incomplete records

**Inspired by:** Jane App (client intake status dashboard), SimplePractice (intake task tracking)

**Context:** Rahul is in the admin panel, reviewing enrollment pipeline. He is on an Android phone or desktop, not in a session room. This is a quick status check, not a deep reporting view.

**Acceptance Criteria:**
- [ ] AC-01: Given Rahul opens the Intake Status view, when he views the list of recently created child records, then he sees each record with an intake status badge: Completed / In Progress / Not Sent / Awaiting Consent
- [ ] AC-02: Given a record has status "Not Sent", when Rahul taps it, then he can generate a form link and copy it to share via WhatsApp (a single tap copies the link; the system does not auto-send WhatsApp messages without Rahul's action)
- [ ] AC-03: Given a record has status "In Progress" (family started but not submitted), when Rahul views it, then he sees what percentage of fields have been answered and when the form was last opened
- [ ] AC-04: Given a record has status "Awaiting Consent" (all fields complete but consent step not confirmed), when Rahul views it, then he sees a prompt: "Consent not yet confirmed — ask family to complete the consent step"
- [ ] AC-05: Given a record has status "Completed", when Rahul views it, then he sees the submission timestamp and the consent confirmation timestamp

**Edge Cases & Error States:**
- [ ] EC-01: If a family completes the form but their internet connection drops before the submission writes to the server, then the status remains "In Progress" (not "Completed") until server confirmation is received; no false-completed status
- [ ] EC-02: If a form link is opened by a family but the form template has since been updated by Rahul, then the family completes the version that was active when their link was generated; Rahul's intake status view notes: "Completed with previous template version [v.X]"

**Non-Functional Requirements:**
- Performance: Intake status list loads within 2 seconds for up to 50 active records
- Offline: Intake status view available offline with last-synced data; staleness timestamp shown if offline
- Privacy: ⚠️ DPDPA — status list shows child names and intake completion state; access restricted to Center Director and Admin roles only

**Dependencies:**
- Blocked by: INT-001, INT-002, INT-003
- Enables: None (reporting/monitoring story)

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android (Redmi/Realme, 2GB RAM, Android 10+)
- [ ] All four status states tested
- [ ] WhatsApp link copy tested on Android
- [ ] Edge cases tested
- [ ] Code reviewed and merged

---

## Backlog: Custom Intake Forms Epic

| Story ID | Title | Persona | Complexity | Priority | Blocked by |
|---|---|---|---|---|---|
| INT-001 | Configure a custom intake form template | Rahul | M | P0 | None |
| INT-002 | Complete the intake form as a family (tablet / Android) | Meena | L | P0 | INT-001 |
| INT-003 | Capture DPDPA-compliant parental consent at intake | Meena / Rahul | M | P0 | INT-001, INT-002 |
| INT-004 | Auto-populate child record from completed intake form | Dr. Sunita / Rahul | M | P0 | INT-003 |
| INT-005 | Track intake form completion status (admin view) | Rahul | S | P1 | INT-001, INT-002, INT-003 |

---

## Epic: ABDM / ABHA Compliant Health Records

**Goal:** Enable the center to operate as an ABDM Health Information Provider (HIP), link a child's ABHA health ID to their center record at intake, and generate FHIR R4-compliant ABDM health records from therapy progress reports — so that families have a portable, government-linked health record for their child and the center meets India's emerging digital health infrastructure requirements.
**Copied from:** ABDM/NHA (India national health infrastructure); no direct competitor copy — this is a novel India-regulatory integration
**Target user(s):** Rahul (enables ABDM integration at center level), Meena (links child's ABHA ID; benefits from portable health record), Dr. Sunita (generates ABDM-compliant health documents from progress reports)
**Definition of Done:**
- Center can be registered in the platform as an ABDM Health Information Provider with a facility ABDM ID
- A child's ABHA health ID can be collected and verified at intake
- At least one record type (progress report / therapy summary) can be formatted as an ABDM FHIR R4-compliant health document
- ABDM consent for health data sharing is captured using the ABDM consent flow (separate from DPDPA intake consent in INT-003)
- ABDM health records can be pushed to the child's ABHA health locker
- All ABDM interactions are logged in an audit trail

**Out of scope (this epic):**
- Full ABDM Health Information User (HIU) role — pulling records from other providers (Phase 2+)
- ABHA-linked billing or insurance claims (not relevant in India's out-of-pocket therapy market)
- NHA-mandated teleconsultation features
- ABDM integration for staff / therapist identity management (separate from child records)
- Real-time ABDM health data exchange during sessions

**[ASSUMPTION — NOT VALIDATED]** This epic assumes: (1) Indian therapy center families have or will obtain ABHA IDs at meaningful rates; (2) center directors see ABDM registration as a value-add or regulatory signal rather than an administrative burden; (3) the NHA HIP registration process is feasible for small private therapy centers. None of these are confirmed. ABDM adoption is government-mandated for public health facilities but optional for private centers as of April 2026. This feature carries high implementation risk and should be validated with center directors before scheduling.

---

### Story ABDM-001: Collect and verify a child's ABHA health ID at intake

**As a** Rahul (Center Director) / Admin staff
**I want to** collect and verify a child's ABHA (Ayushman Bharat Health Account) health ID during intake
**So that** the child's center record is linked to India's national health ID infrastructure from the start of their care journey

**Inspired by:** ABDM HIP Integration Specification (NHA, Government of India); no direct competitor has this in the therapy center software market

**Context:** During intake — either as part of the intake form (INT-002) or as a separate step by admin staff — the child's ABHA ID (14-digit number or @abdm handle) is collected and linked to their record. This step is optional for families without an ABHA ID but flagged as recommended. ABHA verification is done via the ABDM gateway API.

**Acceptance Criteria:**
- [ ] AC-01: Given the child's record has been created (post INT-004), when an admin opens the ABDM/ABHA section of the child's record, then they see an "ABHA ID" field with status "Not linked" and a "Link ABHA ID" button
- [ ] AC-02: Given an admin taps "Link ABHA ID", when they enter the child's 14-digit ABHA number or @abdm handle, then the system calls the ABDM gateway to verify the ABHA ID exists and is active; on verification success, the ABHA ID is stored against the child's record with status "Verified"
- [ ] AC-03: Given ABHA verification is successful, when the system stores the ABHA ID, then it also stores the ABHA profile name and verification timestamp from the gateway response — for cross-check with the child's name in the center record
- [ ] AC-04: Given the ABHA name from the gateway does not match the child's name in the center record, when this mismatch is detected, then the system shows a warning: "ABHA name '[name from ABHA]' does not match the name in this record '[center record name]'. Please confirm this is the correct ABHA ID before linking." — admin must explicitly confirm to proceed
- [ ] AC-05: Given an ABHA ID is linked, when any staff member views the child's record header, then they see an "ABHA Linked" badge showing the ABHA ID (last 4 digits shown; full ID available to admin only)
- [ ] AC-06: Given a family does not have an ABHA ID, when this is indicated during intake, then the record shows "ABHA: Not available" — not blank — with an optional informational prompt: "Families can create a free ABHA ID at [abdm.gov.in/ABHA]"

**Edge Cases & Error States:**
- [ ] EC-01: If the ABDM gateway API is unavailable (connectivity or NHA downtime), then the system shows: "ABHA verification is temporarily unavailable. The ABHA ID has been saved and will be verified automatically when the service is restored." — center operations are not blocked by ABDM unavailability
- [ ] EC-02: If an invalid ABHA ID format is entered (not 14 digits, not a valid @handle format), then the system shows a format error before calling the gateway: "ABHA IDs are 14 digits or use the format name@abdm. Please check and re-enter."
- [ ] EC-03: If the same ABHA ID is already linked to a different child record in the same center, then the system blocks the link and shows: "This ABHA ID is already linked to [child name] in your center. Please verify."

**Non-Functional Requirements:**
- Performance: ABDM gateway verification call should complete within 5 seconds; timeout at 10 seconds with a retry prompt
- Offline: ABHA ID can be entered offline and stored locally; gateway verification queued for when connectivity restores; record shows "ABHA: Pending verification" until verified
- Privacy: ⚠️ DPDPA — ABHA ID is government-issued identity data of a minor; treated as sensitive PII; stored encrypted; access restricted to admin and center director roles by default
- Regulatory: ABDM HIP integration must comply with NHA's HIP Integration Specifications v2.x (FHIR R4 India profile); use the ABDM sandbox for development; production requires NHA HIP registration

**Dependencies:**
- Blocked by: INT-004 (child record must exist), ABDM-000 (center must be registered as ABDM HIP — infrastructure story, not a user story)
- Enables: ABDM-002, ABDM-003

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android (Redmi/Realme, 2GB RAM, Android 10+)
- [ ] ABDM sandbox integration tested end-to-end (not production — sandbox only until NHA registration complete)
- [ ] Name mismatch warning tested
- [ ] Duplicate ABHA link blocking tested
- [ ] Offline queue and deferred verification tested
- [ ] Edge cases tested
- [ ] Code reviewed and merged

---

### Story ABDM-002: Capture ABDM consent for health data sharing

**As a** Meena (Parent / Primary Caregiver)
**I want to** understand what health data the center will share with ABDM and give my consent specifically for that sharing
**So that** I retain control over my child's health records on India's national digital health infrastructure, as required by the ABDM consent framework

**Inspired by:** ABDM Consent Manager Framework (NHA); ABDM Personal Health Records (PHR) app consent flow

**Context:** After an ABHA ID is linked (ABDM-001), Meena must give a separate, explicit consent for the center to act as a Health Information Provider and push records to the ABHA health locker. This is distinct from the DPDPA intake consent (INT-003) — ABDM has its own consent requirements. This consent may be facilitated by an admin at the center.

**Acceptance Criteria:**
- [ ] AC-01: Given an ABHA ID is linked to the child's record, when the admin opens the ABDM section, then they see an "ABDM Consent" sub-section with status "Consent not captured"
- [ ] AC-02: Given the admin initiates the ABDM consent flow, when Meena confirms consent (via ABDM's consent mechanism — OTP to ABHA-registered mobile, or in-app consent via PHR app), then the consent artifact is stored against the child's record with ABDM-issued consent ID and timestamp
- [ ] AC-03: Given ABDM consent is confirmed, when any staff member views the ABDM section of the child's record, then they see "ABDM Consent: Active — [date]" with the consent scope listed (what record types are covered)
- [ ] AC-04: Given Meena wishes to revoke ABDM consent, when she does so (via ABDM PHR app or through the center admin), then the system marks ABDM consent as "Revoked" and blocks any further ABDM health record pushes for this child; existing pushed records are not deleted (per ABDM framework — revocation is prospective)
- [ ] AC-05: Given ABDM consent has not been captured, when an admin attempts to push a health record to the ABHA locker (ABDM-003), then the system blocks the push and shows: "ABDM consent is required before health records can be shared. Please obtain consent from the parent."

**Edge Cases & Error States:**
- [ ] EC-01: If the ABDM consent gateway is unavailable, then the system shows: "ABDM consent service is temporarily unavailable. Please try again later." — center operations are not blocked
- [ ] EC-02: If the parent's ABHA-registered mobile number is different from the number in the center's records, then the OTP step fails; admin is prompted: "OTP could not be sent — the parent's ABHA mobile number may differ from what we have. Ask the parent to complete consent via the ABDM PHR app directly."

**Non-Functional Requirements:**
- Offline: ABDM consent requires live ABDM gateway connectivity; cannot be completed offline
- Privacy: ⚠️ DPDPA + ABDM — this consent is dual-purpose; stored as an ABDM consent artifact AND referenced in the DPDPA consent record; the two consent records are linked by child record ID but stored separately
- Regulatory: ABDM consent flow must follow NHA Consent Manager specifications; do not build a proprietary consent UI that bypasses the ABDM consent artifact requirement

**Dependencies:**
- Blocked by: ABDM-001 (ABHA ID must be linked), ABDM-000 (center ABDM HIP registration)
- Enables: ABDM-003

**Definition of Done:**
- [ ] All AC pass in QA on ABDM sandbox
- [ ] ABDM consent artifact stored and retrievable
- [ ] Revocation flow tested
- [ ] Push-blocked-without-consent tested
- [ ] Edge cases tested
- [ ] Code reviewed and merged

---

### Story ABDM-003: Generate and push an ABDM-compliant health record to the ABHA locker

**As a** Dr. Sunita (Clinical Supervisor)
**I want to** generate an ABDM-compliant health record from a completed progress report and push it to the child's ABHA health locker
**So that** the child has a portable, government-linked health record of their therapy progress that can be accessed by other healthcare providers in future

**Inspired by:** ABDM Health Information Provider (HIP) specifications — Health Record types: Discharge Summary, Op Consultation, Wellness Record (most relevant for therapy progress); FHIR R4 India profile

**Context:** Dr. Sunita has completed a quarterly progress report. She wants to make the report available on the child's national health record. She is on a desktop or Android device in her office.

**Acceptance Criteria:**
- [ ] AC-01: Given a progress report is marked as complete in the system, when Dr. Sunita opens the report and taps "Share to ABHA Locker", then the system checks: (a) the child has a verified ABHA ID, (b) ABDM consent is active — and if both are true, proceeds
- [ ] AC-02: Given the pre-push checks pass, when Dr. Sunita confirms the push, then the system formats the progress report as an ABDM-compatible health record (FHIR R4, relevant record type: Wellness Record or Op Consultation) and submits it to the ABDM HIP API
- [ ] AC-03: Given the ABDM push is successful, when the system receives a successful response from the ABDM gateway, then the progress report record is tagged "Shared to ABHA — [date]" and the ABDM document ID is stored
- [ ] AC-04: Given a health record has been pushed, when the ABDM section of the child's record is viewed, then it shows a history of all documents pushed to the ABHA locker with document type, push date, and ABDM document ID
- [ ] AC-05: Given the ABDM push fails (API error, FHIR validation error), when the failure occurs, then Dr. Sunita sees a specific error message: "ABDM push failed: [reason]. The report has been saved locally. You can retry from the Reports section." — the local progress report is NOT affected by the push failure

**Edge Cases & Error States:**
- [ ] EC-01: If the progress report contains free-text fields that exceed ABDM FHIR field character limits, then the system truncates with a flag and shows a preview of the truncated ABDM document before pushing: "The following sections were shortened to meet ABDM format requirements. Review before confirming."
- [ ] EC-02: If ABDM consent is revoked between when the report is generated and when the push is attempted, then the push is blocked with: "ABDM consent has been revoked for this child. Health records cannot be shared with ABHA until consent is re-established."

**Non-Functional Requirements:**
- Performance: FHIR record generation and ABDM push should complete within 10 seconds; progress indicator shown; timeout at 30 seconds
- Offline: Push requires internet connectivity; if offline, the push option is greyed out with label "ABDM push requires internet connection"
- Privacy: ⚠️ DPDPA + ABDM — pushing child health data to a government infrastructure provider requires confirmed ABDM consent; audit log of every push attempt (success and failure) maintained
- Regulatory: FHIR R4 India profile must be used (not US FHIR Core); record type must match NHA HIP specifications; test against ABDM sandbox before production

**Dependencies:**
- Blocked by: ABDM-001, ABDM-002, and progress report generation (a separate epic in the Progress Reporting cluster)
- Enables: None (terminal story for this epic)

**Definition of Done:**
- [ ] All AC pass in QA against ABDM sandbox
- [ ] FHIR R4 record validated against ABDM FHIR validator
- [ ] Successful push and ABDM document ID storage verified
- [ ] Failure handling tested (API error, FHIR validation error, consent revocation)
- [ ] Audit log entries verified
- [ ] Edge cases tested
- [ ] Code reviewed and merged

---

### Story ABDM-004: Register the center as an ABDM Health Information Provider (infrastructure story)

**As a** Rahul (Center Director)
**I want to** register my center as an ABDM Health Information Provider (HIP) within the platform
**So that** my center can legally link child ABHA IDs and push health records to the national health infrastructure

**Inspired by:** NHA ABDM HIP onboarding process; ABDM Facility Registry

**Context:** This is an admin/infrastructure story. Without HIP registration, ABDM-001, ABDM-002, and ABDM-003 cannot function in production. This story covers the in-product onboarding flow; the actual NHA registration involves an external process that the center director must complete with the NHA portal (out of scope for this story to automate).

**Acceptance Criteria:**
- [ ] AC-01: Given Rahul opens the ABDM Settings section, when the center is not yet registered, then he sees: an explanation of what ABDM HIP registration means, a link to the NHA registration portal, and a form to enter the center's ABDM Facility ID and HIP credentials once obtained from NHA
- [ ] AC-02: Given Rahul enters a valid ABDM Facility ID and HIP API credentials, when he saves them, then the system validates connectivity to the ABDM sandbox/production gateway and shows: "ABDM HIP registration verified. Your center is now connected to the ABDM gateway."
- [ ] AC-03: Given HIP registration is active, when any ABDM-dependent feature (ABDM-001, ABDM-002, ABDM-003) is accessed, then the feature is available; if HIP registration is not active, then those features are greyed out with label "Requires ABDM HIP registration — see Settings > ABDM"
- [ ] AC-04: Given the ABDM HIP credentials expire or the gateway connection fails, when this is detected, then Rahul sees a banner on the admin panel: "ABDM connection error — check your HIP credentials in Settings > ABDM"

**Edge Cases & Error States:**
- [ ] EC-01: If Rahul enters invalid HIP credentials, then the validation step fails with: "Could not connect to ABDM gateway. Please check your Facility ID and credentials." — no partial registration state is saved

**Non-Functional Requirements:**
- Privacy: ⚠️ DPDPA — ABDM HIP credentials are sensitive API keys; stored encrypted; never displayed in plaintext after save; masked as ****
- Regulatory: ABDM HIP credentials obtained through NHA's official registration process only; the platform must not attempt to automate or bypass NHA's registration process

**Dependencies:**
- Blocked by: None (infrastructure prerequisite for the entire ABDM epic)
- Enables: ABDM-001, ABDM-002, ABDM-003

**Definition of Done:**
- [ ] All AC pass in QA against ABDM sandbox credentials
- [ ] Credential storage verified as encrypted and masked
- [ ] Connection validation tested with valid and invalid credentials
- [ ] Greyed-out feature state tested when HIP not registered
- [ ] Edge cases tested
- [ ] Code reviewed and merged

---

## Backlog: ABDM / ABHA Compliant Health Records Epic

| Story ID | Title | Persona | Complexity | Priority | Blocked by |
|---|---|---|---|---|---|
| ABDM-004 | Register the center as an ABDM HIP (infrastructure) | Rahul | L | P0 | None |
| ABDM-001 | Collect and verify a child's ABHA health ID at intake | Rahul / Admin | M | P1 | ABDM-004, INT-004 |
| ABDM-002 | Capture ABDM consent for health data sharing | Meena / Admin | M | P1 | ABDM-001 |
| ABDM-003 | Generate and push an ABDM-compliant health record to the ABHA locker | Dr. Sunita | L | P2 | ABDM-001, ABDM-002 |

---

## Epic: Multi-Therapist / Multi-Doctor Management

**Goal:** Allow a child's record to be assigned to multiple staff members with defined roles and access levels — so that clinical supervisors can oversee their assigned caseload, therapists see only their children, center directors have full visibility, and handovers between staff are structured and documented rather than verbal.
**Copied from:** CentralReach (multi-staff assignment, role-based access), TheraNest (staff assignment to clients), Hi Rasmus (supervision and handover workflows), Jane App (staff access controls)
**Target user(s):** Rahul (Director — assigns staff, views caseload dashboard), Dr. Sunita (Supervisor — views assigned caseload, receives handover notes), Priya (Therapist — views her assigned children only)
**Definition of Done:**
- A child's record can be assigned to multiple staff members simultaneously
- Staff roles (Primary Therapist, Supervisor, Shadow Teacher, Co-Therapist) are defined with distinct permission levels
- Staff members see only the children assigned to them (role-appropriate view)
- Center Director and Supervisor see all children within their scope
- A structured handover flow exists when a child's primary therapist changes
- Rahul has a caseload dashboard showing all active children, assigned staff, and key status flags

**Out of scope (this epic):**
- In-session data collection access controls — those are handled within the session recording epic
- Billing or scheduling assignment to staff — separate billing/scheduling cluster
- Staff performance reporting or HR features
- Multi-center (franchise) support — Phase 2
- External referral partners (external doctors, school teachers outside the center) — Phase 2

**[ASSUMPTION — NOT VALIDATED]** This epic assumes Indian autism therapy centers have multi-staff assignment complexity that causes real coordination problems. This is more likely true for centers with 5+ staff and 20+ active children. Very small centers (2–3 staff, 10 children) may not experience this as a pain point. Center size distribution has not been validated.

---

### Story MPM-001: Assign staff roles to a child's record

**As a** Rahul (Center Director)
**I want to** assign one or more staff members to a child's record with defined roles — Primary Therapist, Supervisor, Shadow Teacher, Co-Therapist
**So that** each staff member knows which children they are responsible for, and access to records is automatically controlled by their role

**Inspired by:** CentralReach (staff assignment to learner records), TheraNest (therapist assignment), Jane App (provider assignment)

**Context:** Rahul is enrolling a new child or reassigning an existing child after a staff change. He is on the admin panel, on desktop or Android. This is an administrative action, not an in-session action.

**Acceptance Criteria:**
- [ ] AC-01: Given Rahul opens a child's record as Center Director, when he opens the "Care Team" tab, then he sees a list of assigned staff (empty for a new record) with an "Add Staff Member" button
- [ ] AC-02: Given Rahul taps "Add Staff Member", when he selects a staff member from the center's staff list and assigns a role (Primary Therapist / Supervisor / Shadow Teacher / Co-Therapist), then the staff member appears in the child's Care Team with their role label and assignment date
- [ ] AC-03: Given a child's record has at least one assigned staff member, when a staff member who is NOT assigned to this child attempts to open the record, then they receive: "You do not have access to this child's record. Contact your center director if you believe this is an error." — no clinical data is visible
- [ ] AC-04: Given a child's record, when a Supervisor role is assigned, then that staff member automatically gains read access to all session data and program records for that child, but cannot edit the child's profile fields (edit access stays with Director/Admin)
- [ ] AC-05: Given a child's record, when a Primary Therapist role is assigned, then that therapist can view and enter session data for that child; they cannot view billing or admin fields
- [ ] AC-06: Given a child's record, when a Shadow Teacher role is assigned, then that staff member can view the child's therapy program and session notes in read-only mode; they cannot enter data
- [ ] AC-07: Given Rahul removes a staff member from a child's Care Team, when the removal is saved, then the staff member immediately loses access to that child's record; their previously entered session data and notes are retained with their name as the author

**Edge Cases & Error States:**
- [ ] EC-01: If Rahul attempts to remove the only Primary Therapist from a child's Care Team, then the system shows a warning: "This child will have no Primary Therapist assigned. Are you sure? You can assign a new therapist immediately." — allows proceed or cancel
- [ ] EC-02: If a staff member is deactivated (leaves the center) while assigned to children, then all their child records are flagged with a banner: "Primary Therapist [name] is no longer active. Please assign a replacement." — records remain accessible to supervisors and directors; the deactivated therapist's access is revoked

**Non-Functional Requirements:**
- Performance: Care Team tab loads within 2 seconds; staff assignment saves within 1 second
- Offline: Care Team view readable offline with last-synced data; changes to assignments require connectivity
- Privacy: ⚠️ DPDPA — role assignment is an access control action; changes logged in audit trail with actor, timestamp, and new role state; audit log is immutable
- Accessibility: Touch targets ≥ 44px; role dropdown legible at standard Android font sizes

**Dependencies:**
- Blocked by: INT-004 (child record must exist); Staff management / user accounts story (not in this cluster — prerequisite infrastructure)
- Enables: MPM-002, MPM-003, MPM-004

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android (Redmi/Realme, 2GB RAM, Android 10+)
- [ ] All four role types tested for access control boundaries
- [ ] Deactivated staff scenario tested
- [ ] Audit log entries verified for all assignment changes
- [ ] Edge cases tested
- [ ] Code reviewed and merged

---

### Story MPM-002: Therapist caseload view — "my children"

**As a** Priya (Special Educator / Therapist)
**I want to** open the app and immediately see only the children assigned to me
**So that** I can find my next child's record and session information without scrolling through children who are not mine

**Inspired by:** Motivity (therapist home screen — assigned learner list), Hi Rasmus (therapist caseload view), Jane App (client list filtered by provider)

**Context:** Priya is at the center, between sessions or before the day starts. She is on her low-end Android phone. She needs to quickly find a child's record or check who her next session is with. She does not need to see children assigned to other therapists.

**Acceptance Criteria:**
- [ ] AC-01: Given Priya logs in, when the home screen loads, then she sees a "My Children" list showing only the children for whom she has an active assignment (Primary Therapist or Co-Therapist role)
- [ ] AC-02: Given the "My Children" list, when Priya views it, then each child card shows: child's first name (or initials if privacy mode is enabled), next scheduled session date/time, and a color-coded status indicator (Active / Suspended / No upcoming session)
- [ ] AC-03: Given Priya taps a child card, when the child's record opens, then she lands on the Session tab (not the Profile tab) — the most relevant view for her workflow
- [ ] AC-04: Given Priya has no children assigned, when the home screen loads, then she sees: "No children assigned to you yet. Contact your center director to be assigned."
- [ ] AC-05: Given the list has more than 10 children, when Priya scrolls, then the list loads additional children progressively (pagination or infinite scroll); no full-page refresh required

**Edge Cases & Error States:**
- [ ] EC-01: If a child is assigned to Priya but the child's record has no consent confirmed (INT-003), then the child appears in Priya's list with a badge: "Intake incomplete" — she can see the child's name but the clinical record tabs are locked until consent is confirmed
- [ ] EC-02: If Priya's assignment to a child is removed while she has the child's record open, then on her next app refresh or session end, the child disappears from her list and the record shows: "You no longer have access to this child's record."

**Non-Functional Requirements:**
- Performance: "My Children" list loads within 2 seconds for up to 30 assigned children on a 4G connection; skeleton loading state shown while loading
- Offline: List and child records are available offline if previously loaded; session data entry works offline (per the session data collection epic NFRs); sync on restore
- Accessibility: Child cards have touch targets ≥ 44px; color-coded status indicators also carry text labels (not color-only)
- Privacy: ⚠️ DPDPA — the home screen shows child names; device-level lock screen is recommended but outside app scope; the app should lock after 5 minutes of inactivity (configurable by admin)

**Dependencies:**
- Blocked by: MPM-001 (assignment must exist)
- Enables: All session-level stories for Priya (session data collection epic); MPM-003 (supervisor sees Priya's caseload)

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android (Redmi/Realme, 2GB RAM, Android 10+)
- [ ] List loads tested with 0, 5, 15, and 30 assigned children
- [ ] Offline behavior tested
- [ ] Intake-incomplete badge tested
- [ ] Edge cases tested
- [ ] Code reviewed and merged

---

### Story MPM-003: Supervisor caseload dashboard

**As a** Dr. Sunita (Clinical Supervisor)
**I want to** see a dashboard of all children under my supervision — who is assigned to which therapist, when their last session was, and whether any program updates or reports are overdue
**So that** I can prioritize my review work and spot children who have not been seen recently or whose programs have not been updated

**Inspired by:** CentralReach (supervisor dashboard), Hi Rasmus (supervision overview), Theralytics (caseload management view)

**Context:** Dr. Sunita starts her day or checks in between clinical sessions. She is on a desktop or Android device. This is a glanceable overview — she should not need to click into individual records to see status.

**Acceptance Criteria:**
- [ ] AC-01: Given Dr. Sunita logs in with a Supervisor role, when she opens the Caseload Dashboard, then she sees a list of all children for whom she has a Supervisor assignment, with one row per child
- [ ] AC-02: Given the caseload dashboard, when Dr. Sunita views a child row, then she sees: child name, assigned Primary Therapist name, date of last completed session, date of last program update, and a flag if any of these are overdue (configurable threshold — default: session > 7 days ago, program update > 30 days ago)
- [ ] AC-03: Given the dashboard, when Dr. Sunita filters by "Overdue flags only", then the list shows only children with at least one overdue flag; the count of flagged children is shown at the top
- [ ] AC-04: Given Dr. Sunita taps a child row, when the child's record opens, then she lands on the Program/Data tab (not the Profile tab) — the most relevant view for her review workflow
- [ ] AC-05: Given Dr. Sunita is a Supervisor for children assigned to multiple different Primary Therapists, when she uses the "Filter by Therapist" control, then the dashboard filters to show only children assigned to the selected therapist

**Edge Cases & Error States:**
- [ ] EC-01: If Dr. Sunita has no children under her supervision, then the dashboard shows: "No children are currently assigned to your supervision. Contact your center director."
- [ ] EC-02: If a child's session data has not been entered (no sessions logged since enrollment), then the "Last session" field shows "No sessions recorded" — not a date, not blank

**Non-Functional Requirements:**
- Performance: Caseload dashboard loads within 3 seconds for up to 50 supervised children on 4G; the dashboard must be usable on a mid-range Android phone (not desktop-only)
- Offline: Dashboard readable offline with last-synced data; staleness timestamp shown; flag calculations based on last-synced session data
- Privacy: ⚠️ DPDPA — caseload dashboard shows multiple children's names and clinical status; access restricted to Supervisor and Director roles; session-level detail requires opening individual child records

**Dependencies:**
- Blocked by: MPM-001 (assignments must exist), MPM-002 (session data structure must exist for "last session" field)
- Enables: MPM-004 (handover workflow is initiated from here or from child record)

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android (Redmi/Realme, 2GB RAM, Android 10+)
- [ ] Dashboard tested with 0, 10, and 50 supervised children
- [ ] Overdue flag logic tested with configurable thresholds
- [ ] Filter by therapist tested
- [ ] Offline behavior tested
- [ ] Edge cases tested
- [ ] Code reviewed and merged

---

### Story MPM-004: Structured handover when a child's therapist changes

**As a** Dr. Sunita (Clinical Supervisor) / Rahul (Center Director)
**I want to** trigger a structured handover process when a child's Primary Therapist changes — capturing the outgoing therapist's notes and ensuring the incoming therapist has what they need before their first session
**So that** continuity of care is maintained and the new therapist does not start a session without knowing the child's current program, behavioral history, and any open clinical concerns

**Inspired by:** Hi Rasmus (staff handover and supervision notes), CentralReach (note types including handover/transition notes)

**Context:** Priya is leaving or changing assignments. Dr. Sunita or Rahul reassigns the child in the Care Team (MPM-001). A handover flow is triggered. The outgoing therapist (Priya) completes a handover note. The incoming therapist sees it before their first session.

**Acceptance Criteria:**
- [ ] AC-01: Given Rahul or Dr. Sunita changes a child's Primary Therapist in the Care Team (MPM-001), when the new therapist is saved, then the system triggers a handover notification: "A handover note is required before [new therapist name] begins sessions with [child name]. [Outgoing therapist name] has been asked to complete it."
- [ ] AC-02: Given a handover is triggered, when the outgoing therapist (Priya) opens the child's record, then she sees a prompted handover note form with the following structured sections: Current program status (which targets are active, which are mastered), Key behavioral notes (current maladaptive behaviors, effective reinforcers, known triggers), Parent communication notes (any open parent concerns or follow-ups), Other important information (free text)
- [ ] AC-03: Given Priya completes and submits the handover note, when it is saved, then: (a) the incoming therapist sees a "Handover note available" banner when they open the child's record, (b) the note is stored as a version-stamped, read-only record linked to the care transition event
- [ ] AC-04: Given the incoming therapist opens the child's record for the first time, when they view the Handover Note, then they must mark it as "Reviewed" before the handover banner is dismissed; this creates an audit record: "[new therapist name] reviewed handover note on [date]"
- [ ] AC-05: Given a handover is triggered but the outgoing therapist does not complete the handover note within 48 hours, when this occurs, then Dr. Sunita and Rahul receive a notification: "Handover note for [child name] is overdue. [Outgoing therapist name] has not completed it."
- [ ] AC-06: Given a handover note is completed, when Dr. Sunita opens the child's record history, then she sees a Care Team History log showing all staff transitions with dates, outgoing therapist, incoming therapist, and a link to the associated handover note

**Edge Cases & Error States:**
- [ ] EC-01: If the outgoing therapist is deactivated before completing the handover note, then the handover note form is transferred to the Supervisor: "Handover note is incomplete — [outgoing therapist] is no longer active. Please complete the handover note as supervisor."
- [ ] EC-02: If there is no outgoing therapist (child has never had a Primary Therapist assigned, and one is being assigned for the first time), then no handover note is triggered; the incoming therapist sees a prompt: "This child has no previous primary therapist. Review the intake record before your first session."

**Non-Functional Requirements:**
- Performance: Handover note form saves within 2 seconds; notifications delivered within 60 seconds of the triggering event
- Offline: Handover note can be drafted offline and submitted when connectivity is restored; "Saved locally — not yet submitted" state shown
- Privacy: ⚠️ DPDPA — handover notes contain clinical assessments of a minor; access restricted to assigned care team members + supervisor + director; stored encrypted; part of the child's permanent clinical record
- Accessibility: Handover note form fields have touch targets ≥ 44px; structured sections are collapsible for easier navigation on small screens

**Dependencies:**
- Blocked by: MPM-001 (staff assignment and reassignment must work), MPM-002 (outgoing therapist caseload context)
- Enables: All clinical quality features downstream (session recording, program management) — the handover is the bridge between therapists

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android (Redmi/Realme, 2GB RAM, Android 10+)
- [ ] Handover trigger tested on therapist change
- [ ] Handover note form all sections saved and retrieved correctly
- [ ] 48-hour overdue notification tested
- [ ] "Reviewed" confirmation and audit record tested
- [ ] Deactivated therapist scenario tested
- [ ] Edge cases tested
- [ ] Code reviewed and merged

---

### Story MPM-005: Center director full caseload overview

**As a** Rahul (Center Director)
**I want to** see a single view of every active child in the center, their assigned staff, their last session date, and any admin flags (intake incomplete, no therapist assigned, consent not confirmed)
**So that** I can manage my center operationally without having to open individual records to understand the state of each child's enrollment

**Inspired by:** CentralReach (client list with status columns), Jane App (client list with staff assignment), TherapEZ (client list — admin operations)

**Context:** Rahul checks this view at the start of the day or week. He is on a desktop or Android device. He wants a glanceable overview, not a clinical deep-dive.

**Acceptance Criteria:**
- [ ] AC-01: Given Rahul is logged in as Center Director, when he opens the Children view, then he sees all active children in the center (not filtered by assignment — he sees everyone)
- [ ] AC-02: Given the Children view, when Rahul views a child row, then he sees: child name, enrollment date, assigned Primary Therapist, assigned Supervisor, last session date, DPDPA consent status, ABHA link status (if ABDM feature is enabled), and any open admin flags
- [ ] AC-03: Given the Children view, when Rahul filters by "Admin flags", then the view shows only children with at least one open flag (e.g., no therapist assigned, intake incomplete, consent not confirmed)
- [ ] AC-04: Given the Children view, when Rahul sorts by "Last session", then children who have not had a session in the longest time appear first — enabling a quick dropout-risk scan
- [ ] AC-05: Given Rahul taps a child row, when the child's full record opens, then he has full read and edit access to all tabs (Profile, Care Team, Program, Sessions, Documents, Billing)

**Edge Cases & Error States:**
- [ ] EC-01: If the center has no active children, then the view shows: "No active children enrolled. Add a new child record to get started." with a prominent "Add Child" button

**Non-Functional Requirements:**
- Performance: Children view loads within 3 seconds for up to 100 active children; search/filter operates within 500ms
- Offline: View readable offline with last-synced data; staleness timestamp shown
- Privacy: ⚠️ DPDPA — this view shows all children's names and clinical status in one screen; access restricted to Center Director role only; no export functionality without explicit admin confirmation (to prevent mass data export)

**Dependencies:**
- Blocked by: MPM-001 (assignments must exist), INT-003 (consent status must be trackable)
- Enables: MPM-003 (supervisor view is a scoped subset of this view)

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android (Redmi/Realme, 2GB RAM, Android 10+)
- [ ] View tested with 0, 20, and 100 active children
- [ ] All flag types tested (no therapist, intake incomplete, consent not confirmed)
- [ ] Sort by last session tested
- [ ] Offline behavior tested
- [ ] Edge cases tested
- [ ] Code reviewed and merged

---

## Backlog: Multi-Therapist / Multi-Doctor Management Epic

| Story ID | Title | Persona | Complexity | Priority | Blocked by |
|---|---|---|---|---|---|
| MPM-001 | Assign staff roles to a child's record | Rahul | M | P0 | INT-004, Staff accounts infra |
| MPM-002 | Therapist caseload view — "my children" | Priya | M | P0 | MPM-001 |
| MPM-003 | Supervisor caseload dashboard | Dr. Sunita | L | P0 | MPM-001, MPM-002 |
| MPM-005 | Center director full caseload overview | Rahul | M | P1 | MPM-001, INT-003 |
| MPM-004 | Structured handover when a child's therapist changes | Dr. Sunita / Rahul | L | P1 | MPM-001, MPM-002 |

---

## Cross-Cluster Dependencies Summary

| Story | Depends on (outside this cluster) | Enables (outside this cluster) |
|---|---|---|
| INT-001–005 (Intake Forms) | Staff accounts / user management infrastructure | All clinical epics (program design, session recording, progress reporting) |
| ABDM-001–004 | INT-004 (child record), Progress Reporting epic (for ABDM-003) | Portable health records for families; ABDM-linked progress reporting |
| MPM-001–005 | INT-004 (child record), Staff accounts infrastructure | Session recording epic (Priya's sessions), Program design epic (Dr. Sunita's review), Progress reporting (caseload context) |

---

---
## ⚠️ Feature Factory Disclaimer

These features were defined by competitive observation and category assumption —
not by validated user research. Before committing engineering capacity, a real
product thinker should ask:

**What we copied but haven't validated:**

- **Custom Intake Forms:** Assumed that Indian therapy centers currently collect intake data on paper or verbally and that this is a painful enough problem to drive adoption of a digital form. The depth of the intake gap and whether Indian therapy center parents will complete digital forms (with or without staff assistance) has NOT been tested. Evidence for the gap exists from the journey map (Stage 2 BP-04) but is marked 🔶 [HYPOTHESIS].

- **ABDM / ABHA:** Assumed that (1) ABHA ID adoption among families at private Indian autism therapy centers is sufficient to make this integration valuable at launch; (2) center directors see ABDM HIP registration as a worth-the-effort compliance signal rather than an unnecessary burden; (3) the NHA HIP registration process is feasible for small private centers with 5–20 staff. ABDM is a government initiative with growing adoption but no confirmed data on uptake at private autism therapy centers in India. This feature is HIGH RISK — it carries significant engineering effort for an integration whose demand at this market segment has not been confirmed.

- **Multi-Therapist Management:** Assumed that Indian autism therapy centers have multi-staff coordination complexity that causes real handover problems. More likely to be a genuine pain point for centers with 8+ staff; potentially low-value for small 2–3 staff centers where everyone knows every child. Center size distribution and handover frequency have not been validated.

**What a researcher would ask before building this:**

1. Do Indian therapy center parents complete intake forms at all today — and if so, on what medium? Is there a paper form, or is the intake purely verbal? (Journey map hypothesis H-06 is directly relevant here — but is only rated as 🔶.)
2. Are center directors aware of ABDM/ABHA? Do they see it as relevant to their operations? What proportion of their enrolled families currently have an ABHA ID? (No data exists on this for the private autism therapy center segment.)
3. In centers with 5+ staff, how do therapist handovers happen today? Is the current verbal/WhatsApp handover causing clinical incidents (child runs wrong program after therapist change) or just inefficiency? The severity of the pain determines the build priority.
4. What is the DPDPA awareness level of center directors? Do they know they are currently non-compliant with Section 9 requirements for minors' health data? Would a compliance-first message drive adoption of intake forms, or would it create anxiety?

**What the Product Consultant would challenge:**

1. **ABDM/ABHA is a Phase 2 feature at best.** The implementation effort (NHA HIP registration, FHIR R4 India profile, ABDM consent flow) is substantial. The demand signal at private autism therapy centers is unconfirmed. This should not be in the same sprint as core intake forms. Build intake forms + DPDPA consent first; add ABDM as a differentiated feature once adoption is established.
2. **Multi-therapist management is table stakes for medium centers but overengineered for small ones.** The handover workflow (MPM-004) in particular carries significant UX and notification complexity. For a 3-staff center (which may be the majority of the Indian market at launch), this feature may go entirely unused. Consider whether the MVP should be simply: "assign a primary therapist to a child" — and defer the structured handover, caseload dashboards, and role-based access controls to a second iteration validated by early adopter feedback.
3. **DPDPA consent (INT-003) is the only non-negotiable in this cluster.** If nothing else from Cluster 2 ships in v1, the consent capture mechanism must ship — because every downstream clinical feature writes child health data, and doing so without verifiable consent is a regulatory liability for both the center and the platform. This should be P0 regardless of whether the rest of intake is deferred.

**Risk level:**

| Feature | Risk level | Rationale |
|---|---|---|
| Custom Intake Forms (INT-001–005) | Medium | The problem is real (BP-04 in journey map); the solution is table stakes in the US market; demand in India is inferred not confirmed. DPDPA consent (INT-003) sub-story is Low risk — it is a regulatory requirement regardless of intake form adoption. |
| ABDM / ABHA (ABDM-001–004) | High | Novel feature with no competitive reference in this market; depends on government infrastructure and NHA registration; ABHA family uptake at private autism centers unconfirmed. Build only after validating demand with director interviews. |
| Multi-Therapist Management (MPM-001–005) | Medium-High | US tools confirm this is a real category; Indian market need depends on center size. The basic assignment (MPM-001) and caseload view (MPM-002, MPM-003) are Medium risk — likely needed at 5+ staff. Handover workflows (MPM-004) are higher risk — pain severity unconfirmed. |

Use the `/research` agent to validate ABHA uptake and intake form assumptions before sprint planning.
Use the `/product-consultant` agent to challenge ABDM scope and the handover workflow complexity before committing engineering capacity.

---
*Generated by: Mindless Product Owner agent*
*Source context: competitive-analysis-autism-therapy-software.md, journey-map.md, products/autism-therapy-platform/CLAUDE.md*
*Note: Competitor Tavily searches (TherapEZ, PractiPal, ABDM integration, multi-therapist patterns) were specified but could not be run in this session due to Bash tool unavailability. Feature Inspiration Table is based on competitive analysis already in the research corpus + known public product capabilities. Re-run Tavily searches when Bash is available to strengthen evidence levels on TherapEZ and PractiPal intake capabilities.*
