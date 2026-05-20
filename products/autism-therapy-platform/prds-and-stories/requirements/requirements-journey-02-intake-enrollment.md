# Requirements: Journey 2 — Intake & Enrollment

**Product:** Autism Therapy Platform (India)
**Journey:** Journey 2 — Intake & Enrollment
**MVP status:** ✅ IN SCOPE — MVP
**Primary actor:** Rahul (Center Director / Admin)
**Supporting actors:** Meena (Parent / Primary Caregiver), Dr. Sunita (Clinical Supervisor), Priya (Special Educator)
**Date:** 2026-05-05
**Story ID prefix:** INT-
**Source documents:**
- `user-journeys/journey-02-intake-enrollment.md`
- `user-journeys/journey-map.md` — Part 2, Journey 2

---

## Epic: INT — Intake & Enrollment

**Goal:** Give Rahul a structured, DPDPA-compliant workflow to create a child's EMR, capture verified parental consent, collect a complete developmental history via a mobile-first intake form, upload prior documents, optionally link a government ABHA health ID, assign a care team, and schedule the first assessment session — all from a low-end Android device, with the child's record going from zero to operationally active without a single paper form.

**Copied from:** CentralReach (client record creation and document management), Motivity (intake form and consent workflow), Jane App (care team assignment and scheduling), SimplePractice (intake form partial-save and family-facing link). No Indian competitor (TherapEZ, PractiPal) has any clinical intake capability — this is a differentiator in the Indian market at every step beyond the basic contact record.

**Target user(s):** Rahul (Center Director / Admin), Meena (Parent / Primary Caregiver — completes family-facing intake form)

**Definition of Done:**
- Rahul can create a minimum child record (5 required fields) in under 60 seconds on minimum-spec Android (Redmi/Realme, 2GB RAM, Android 10+)
- Duplicate detection runs on child name and date of birth combination before every record creation
- DPDPA parental consent is captured with explicit opt-in checkbox (never pre-checked), on-screen signature, and write-once immutable server-side record; consent cannot be captured offline
- All clinical tabs on the child profile are locked until consent_status = "confirmed"
- Family-facing intake form is completable in a mobile browser with no app installed, supports partial save for 48 hours, and auto-clears on submit on shared tablet
- Intake form submission is an atomic transaction — server error causes full rollback; no partial writes to the child record
- Document upload supports PDF, JPG, PNG, HEIC up to 20MB per file; all uploads encrypted in transit and at rest; upload action logged in audit trail
- Intake form completion status (Not Sent / In Progress / Awaiting Consent / Completed) visible to Rahul at a glance per child
- ABHA linking shows "unavailable" gracefully if ABDM HIP registration is not complete — does not block enrollment
- Care team assignment immediately applies role-based access control for assigned staff
- First assessment session can be created with conflict detection against therapist availability and room bookings
- All stories pass QA on minimum-spec Android (Redmi/Realme, 2GB RAM, Android 10+)
- Offline behavior confirmed for every data-write step

**Out of scope (this epic):**
- DPDPA consent form implementation — this is CONSENT-002 (Journey 0); INT-003 is an integration point only, not a reimplementation
- ABDM consent for pushing health records to ABHA locker (ABDM-002) — separate consent flow, post-MVP
- Parent-facing portal or parent login — parents access only the public intake form link
- Recurring schedule configuration — Journey 3 (Scheduling & Attendance Management)
- Clinical program design — Journey 4 (deferred post-MVP)
- Fee agreement or billing setup — Journey 9
- Automated session reminders beyond the first assessment appointment — Journey 3
- Bulk import of existing child records or historic intake data
- Multi-language intake form — Phase 2; English only at launch
- Shadow teacher assignment — deferred; Care Team tab supports this role but the shadow teacher workflow is out of scope for MVP

**[ASSUMPTION — NOT VALIDATED]** This epic assumes that Indian autism therapy center parents are willing and able to complete a digital intake form on a shared center tablet or their own Android phone, and that center directors will adopt digital child record creation over their existing paper/WhatsApp intake workflow. Neither behavior has been validated in primary research with Indian centers. Validate via contextual observation and director interviews before sprint planning. See `/research` agent task: validate H-06 (DPDPA intake gap) and parent tech literacy.

---

## Story INT-001: Create new child record with minimum required fields and duplicate detection

**As a** Rahul (Center Director)
**I want to** open a form and create a new child record by entering five required fields — child first name, date of birth, primary diagnosis, parent/guardian name, and parent mobile number — and have the system warn me if a matching record may already exist
**So that** every enrolled child has a structured digital record from day one, and I don't accidentally create duplicates for the same child

**Inspired by:** CentralReach new client record creation; Motivity patient enrollment; Jane App new client form

**Context:** Rahul is at the center, at his desk, or on his phone when a family arrives or calls to enroll. He needs to create the record immediately. The form must be fast enough that he can complete it while speaking to the parent. Primary device: Android smartphone. Connectivity assumed at front desk; offline draft behavior required for edge cases.

**Acceptance Criteria:**
- [ ] AC-01: Given Rahul is logged in as Center Director or Admin, when he taps "Add New Child" on the Home Screen or Children List, then the New Child Record Form opens in under 1.5 seconds on minimum-spec Android (2GB RAM, Android 10+)
- [ ] AC-02: Given the form is open, then exactly five fields are marked required with a red asterisk: Child first name (text), Date of birth (native Android date picker), Primary diagnosis (single-select dropdown: ASD / ASD with intellectual disability / ADHD / Cerebral Palsy / Multiple disabilities / Other), Parent/guardian name (text), Parent/guardian mobile number (phone input, +91 prefix auto-populated)
- [ ] AC-03: Given the form is open, then an "Add more details (optional)" toggle is visible and collapsed; tapping it expands optional fields: gender, address, second guardian name and mobile, language preference, UDID number, school name, emergency contact
- [ ] AC-04: Given the required fields are complete, when Rahul taps "Create Record", then the system runs a duplicate check (child first name + date of birth match against existing records) before writing
- [ ] AC-05: Given no duplicate is found, then POST /children is called; on success the Child Profile Screen (consent-blocked state) opens within 2 seconds; all required fields are persisted
- [ ] AC-06: Given a duplicate is detected (name + DOB match), then a dialog appears: "A record for a child with this name and birthdate already exists. Are you sure this is a different child?" with two actions — "Confirm this is a different child" and "Review existing record"
- [ ] AC-07: Given Rahul selects "Confirm this is a different child", then the record is created with a system note: "Created despite duplicate detection — confirmed different child by [user name] on [date]"
- [ ] AC-08: Given Rahul selects "Review existing record", then the dialog closes, the system navigates to the existing child's profile, and the new record form is discarded
- [ ] AC-09: Given Rahul taps "Create Record" with one or more required fields empty, then inline validation errors appear on each empty required field and the form does not submit
- [ ] AC-10: Given Rahul loses connectivity before submitting, then a banner reads "You're offline — your form is saved locally. You'll need a connection to create the record." and all entered data is preserved in device-local draft storage
- [ ] AC-11: Given a local draft exists, when Rahul reopens the app after restoring connectivity, then a "Resume draft" prompt appears and loads the saved form state
- [ ] AC-12: Given the form loads, then a non-dismissible amber DPDPA notice banner is visible at the top: "You'll need to confirm parental consent before adding clinical records. You can do this right after creating the record."

**Edge Cases & Error States:**
- [ ] EC-01: If the parent mobile number is not a valid 10-digit Indian number after +91, the field shows: "Enter a valid 10-digit mobile number"
- [ ] EC-02: If the date of birth entered is in the future, the field shows: "Date of birth cannot be in the future"
- [ ] EC-03: If the duplicate check API call fails, the system proceeds with record creation and logs the failed check with a system flag; no silent data loss
- [ ] EC-04: If POST /children returns 5xx, the form shows "Couldn't create record — tap to retry" and preserves the draft locally
- [ ] EC-05: If Rahul navigates away from an incomplete form with data entered, the system auto-saves a local draft and shows a "Draft saved" toast

**Non-Functional Requirements:**
- Performance: Form loads ≤ 1.5s on minimum-spec Android; duplicate check resolves ≤ 1s; record creation and navigation ≤ 2s on 4G
- Offline: Local draft written to device storage on any field input; submit requires connectivity; draft survives app close and reopen
- Accessibility: All touch targets ≥ 44dp; date of birth uses native Android date picker (not custom component) for screen reader compatibility; field labels above inputs, not placeholder-only; one-handed operable on standard 360dp Android screen
- Privacy: ⚠️ DPDPA 2023 — creating a child record constitutes processing personal data of a minor; consent prompt at next step is a mandatory gate; no clinical data may be written until CONSENT-002 is confirmed

**Dependencies:**
- Blocked by: AUTH-001 (Rahul must be authenticated as Center Director or Admin role)
- Enables: INT-003 (DPDPA consent gate — triggered immediately after record creation), INT-007 (care team assignment requires child record to exist)

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android (Redmi/Realme, 2GB RAM, Android 10+)
- [ ] Duplicate detection tested: exact match, no match, API failure
- [ ] Offline draft behavior tested: close app mid-form, reopen, confirm draft loads
- [ ] DPDPA notice banner confirmed non-dismissible
- [ ] EC-01 through EC-05 tested
- [ ] Code reviewed and merged

---

## Story INT-002: Family-facing digital intake form — mobile-first, partial save, no app required

**As a** Meena (Parent / Primary Caregiver) — or Rahul assisting on her behalf
**I want to** receive a link to a digital intake form that opens in my Android browser, complete it in sections with progress saved automatically, and submit it without downloading an app
**So that** the center has my child's full developmental history, diagnosis details, and prior therapy records on file before therapy begins — without me having to fill out paper forms at the center

**Inspired by:** Jane App new client intake form (link-based, no login); SimplePractice client intake portal; Motivity intake form workflow

**Context:** The form is accessed via a link Rahul shares through WhatsApp or the platform's "Copy link" action. Meena opens it on her own Android phone or on a shared center tablet. The form must be completable by a parent with moderate tech literacy, in a single sitting or across multiple sessions using partial save. Primary device: low-to-mid-range Android browser. No app installation required.

**Acceptance Criteria:**
- [ ] AC-01: Given the intake form link is opened in an Android browser, then the form renders in a single-column mobile layout with section headers and progress indicator ("Section 2 of 5") within 2 seconds on a 4G connection
- [ ] AC-02: Given the form is rendered, then it is organized into sections: Child Details, Developmental History, Diagnosis, Prior Therapy, Family Background, UDID / Documents; each section is presented sequentially with a "Continue" button to advance
- [ ] AC-03: Given the following fields are in the form, then they are marked required with a red asterisk AND a "Required" text label (not color alone): child's full name, date of birth, primary diagnosis, parent/guardian name, parent mobile number
- [ ] AC-04: Given optional fields include UDID number, then if left blank, the record shows "UDID: Not provided" with a follow-up flag visible to Rahul on the child profile
- [ ] AC-05: Given Meena completes fields but does not submit, then the form auto-saves progress locally every time she advances a section; progress is retained for 48 hours on the same device/link
- [ ] AC-06: Given Meena returns to the form link within 48 hours on the same device, then a "Resume your form — you were on Section [N]" prompt appears and restores her saved progress
- [ ] AC-07: Given the form includes file upload fields, then accepted types are PDF, JPG, PNG, HEIC; max file size per upload is 10MB; a progress bar is shown for uploads taking more than 2 seconds
- [ ] AC-08: Given Meena reaches the final section and taps "Submit", then the system checks whether DPDPA consent has already been confirmed (consent_status = "confirmed" on the child record); if not, the DPDPA Consent Screen (CONSENT-002) is presented as the final step before submission is accepted
- [ ] AC-09: Given the form is submitted successfully, then a success screen appears: "Thank you. Your child's details have been received." and the tablet auto-clears all form data after 30 seconds (preventing personal data exposure to the next user)
- [ ] AC-10: Given the form link is older than 7 days, then the form shows a human-readable expiry message with the center's name and phone number; the form fields are not displayed
- [ ] AC-11: Given Rahul opens the form on a center tablet on Meena's behalf, then the form behaves identically; after submit the tablet auto-clears

**Edge Cases & Error States:**
- [ ] EC-01: If a required field is left blank on section submit, the field is highlighted with a red border and descriptive error text (not color alone); the page scrolls to the first error
- [ ] EC-02: If a file upload fails (network drop or file too large), an inline error appears per field: "Upload failed — check your connection or try a smaller file." The rest of the form is not blocked
- [ ] EC-03: If the form submission POST /intake/submit returns a server error, the entire transaction is rolled back — no partial writes to the child record; the screen shows "Something went wrong — your answers are saved. Please try again." The "Submit" button is re-enabled
- [ ] EC-04: If connectivity is lost mid-form, a banner reads "No connection — your answers are saved. Submit when you have internet." Partial save is preserved; the submit button is disabled until connectivity restores
- [ ] EC-05: If the child record linked to the form token has consent_status != "confirmed" and Meena reaches the submit step, the consent screen is shown; submission is blocked until consent is captured

**Non-Functional Requirements:**
- Performance: Form template loads ≤ 2s on 4G; skeleton placeholders shown while loading; each section advances without full page reload
- Offline: Partial save preserved in browser local storage; submit requires connectivity; clear messaging that data is not lost
- Accessibility: Font size minimum 16px throughout; all touch targets ≥ 44dp; all required field indicators include text label, not color alone; no reliance on hover states
- Privacy: ⚠️ DPDPA 2023 — intake form data is health data of a minor; POST /intake/submit is atomic; server error = full rollback; form data cannot be written to child record until consent_status = "confirmed"; tablet auto-clear on submit prevents data exposure
- Constraint: Must be completable by a non-tech-confident Indian parent on a low-end Android browser with no app installed; no login required; plain language throughout

**Dependencies:**
- Blocked by: INT-001 (child record must exist for form token to be generated), INT-003 (consent gate checked at submission step), INT-005 (form link status is tracked in the intake status dashboard)
- Enables: INT-004 (document upload from intake form populates Documents tab), INT-005 (submission updates intake completion status to "Completed")

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android browser (Chrome/Samsung Internet, Android 10+)
- [ ] Partial save and 48-hour resume tested: close browser, reopen link, confirm progress restored
- [ ] 7-day link expiry tested
- [ ] Atomic submit/rollback tested by simulating server error mid-transaction
- [ ] Tablet auto-clear tested: submit, confirm data cleared after 30 seconds
- [ ] EC-01 through EC-05 tested
- [ ] Accessibility: text label on required fields confirmed; no color-only indicators; minimum font size confirmed
- [ ] Code reviewed and merged

---

## Story INT-003: DPDPA consent gate at intake — integration point delegating to CONSENT-002

**As a** Rahul (Center Director) — or Meena (Parent) where present
**I want to** be guided to complete DPDPA parental consent immediately after a child record is created, and for that consent to act as the single gate that unlocks all clinical tabs on the child profile
**So that** the center never inadvertently processes a minor's health data without verified parental consent on file, and every clinical workflow is legally gated

**Inspired by:** Motivity HIPAA consent workflow (adapted for DPDPA 2023); CentralReach authorization management. No Indian competitor has a consent gate of this type — this is both a differentiator and a regulatory requirement.

**Context:** INT-003 is an integration point, not a reimplementation. The consent form UI and server-side consent record logic are owned by CONSENT-002 (Journey 0). INT-003 defines how the intake journey surfaces the consent gate — where and when the orange banner appears, which tabs it blocks, what "confirmed" looks like, and the assisted-verbal fallback path for when Meena is not present. This story does not reimplement consent capture; it wires the gate into the enrollment flow.

**Acceptance Criteria:**
- [ ] AC-01: Given a child record is created (INT-001), when the Child Profile Screen opens, then an orange non-dismissible banner is displayed at the top of the screen: "Parental consent required — clinical records cannot be added until consent is confirmed." with a single CTA: "Add consent now"
- [ ] AC-02: Given the consent gate is active (consent_status = "pending"), then the following tabs are locked and display a lock icon with tooltip "Requires parental consent": Program, Session Notes, Documents
- [ ] AC-03: Given the consent gate is active, then only the Profile tab and Care Team tab remain accessible
- [ ] AC-04: Given Rahul taps "Add consent now", then the DPDPA Consent Screen (CONSENT-002) is presented; the pre-checked checkbox state is NOT permitted; the CTA is disabled until the checkbox is checked AND a signature is drawn
- [ ] AC-05: Given consent is confirmed (CONSENT-002 returns consent_status = "confirmed"), then the orange banner is replaced by a green "DPDPA Consent: Confirmed [date]" badge; all locked tabs unlock without requiring a page reload
- [ ] AC-06: Given the intake form (INT-002) reaches the submission step and consent_status is still "pending", then the DPDPA Consent Screen is presented inline as the final step; form submission is blocked until consent is confirmed
- [ ] AC-07: Given Meena is not physically present when the child record is created, then Rahul can tap "Parent not present? Record verbal consent" (small secondary link at bottom of the consent screen); this opens the staff-assisted verbal consent flow which writes consent_type = "staff-assisted-verbal" and sets a persistent follow-up flag: "Digital consent pending — collect at next visit"; the orange banner remains on the child profile until digital consent is confirmed
- [ ] AC-08: Given consent has been captured via staff-assisted verbal path, then the profile shows: "DPDPA Consent: Staff-assisted verbal [date] — digital consent pending" in amber; clinical tabs remain locked until digital consent is confirmed
- [ ] AC-09: Given consent_status = "confirmed", when any staff member attempts to access the consent record, then the record is read-only; no edit path exists; only "View consent record" is available

**Edge Cases & Error States:**
- [ ] EC-01: If CONSENT-002 server call fails during consent confirmation, the child profile remains in consent-blocked state; the orange banner remains; an error toast appears: "Consent could not be saved — check your connection and try again." No partial consent write
- [ ] EC-02: If a staff member who is not Center Director or Admin attempts to access a consent-blocked child profile, they see the locked state but cannot initiate the "Add consent now" flow; only Center Director and Admin roles can trigger consent capture
- [ ] EC-03: If the app is closed mid-consent-form before confirmation, the child record retains consent_status = "pending"; no partial consent record is written

**Non-Functional Requirements:**
- Performance: Consent status check on profile load must not add more than 200ms to profile load time; consent status is returned as part of GET /children/{id} response
- Offline: Consent capture requires connectivity (server timestamp is legally required for DPDPA defensibility); if offline, consent banner remains and an offline message is shown: "An internet connection is required to complete consent. Your form answers are saved and will be here when you reconnect."
- Accessibility: Orange and green consent banners must include text state labels (not color alone); lock icon on tabs must include accessible label "Requires parental consent"
- Privacy: ⚠️ DPDPA 2023 MASTER GATE — consent record is write-once and immutable; pre-checked consent checkboxes are explicitly prohibited; consent_type must be recorded (in-person / remote / staff-assisted-verbal); consent record retained for minimum 3 years post-discharge per DPDPA data retention requirements

**Dependencies:**
- Blocked by: INT-001 (child record must exist), CONSENT-002 (Journey 0 — owns consent form UI and server-side write logic)
- Enables: INT-002 (intake form submission gated on consent confirmation), INT-004 (Documents tab gated on consent confirmation), INT-006 (ABHA linking is admin-accessible post-consent), INT-007 (care team assignment tab accessible pre-consent but clinical session creation requires consent)

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android (Redmi/Realme, 2GB RAM, Android 10+)
- [ ] Tab lock/unlock behavior tested end-to-end: create record, confirm tabs locked, confirm consent, confirm tabs unlock without reload
- [ ] Staff-assisted verbal path tested: flag persists, tabs remain locked, digital consent capture clears flag
- [ ] Pre-checked checkbox state confirmed impossible at UI layer (checkbox initial state = unchecked, verified in code review)
- [ ] Offline consent blocking tested: confirm banner blocks submit when offline
- [ ] EC-01 through EC-03 tested
- [ ] Code reviewed and merged

---

## Story INT-004: Document upload for prior records — diagnosis reports, school records, UDID card

**As a** Rahul (Center Director) or Dr. Sunita (Clinical Supervisor)
**I want to** upload prior documents — diagnosis reports, school records, previous therapy reports, and the child's UDID card — to the child's Documents tab after the record is created
**So that** all of a child's relevant prior records are in one place and accessible to assigned staff, replacing the current practice of storing them in physical files or WhatsApp chat histories

**Inspired by:** CentralReach document management; Motivity file attachments; Jane App document storage

**Context:** Document upload occurs in two places: during intake form submission (INT-002 file upload fields) and directly via the Documents tab post-enrollment. This story covers the Documents tab upload path — used by Rahul or Dr. Sunita after the intake form is submitted and the child record is fully active. Upload requires consent_status = "confirmed".

**Acceptance Criteria:**
- [ ] AC-01: Given a child record has consent_status = "confirmed", when Rahul or Dr. Sunita opens the Documents tab, then an "Upload Document" button is visible and tappable
- [ ] AC-02: Given the "Upload Document" button is tapped, then the device file picker opens supporting: device storage, camera (for photographing physical documents), and Google Drive/Files app integration
- [ ] AC-03: Given a file is selected, then supported types are PDF, JPG, PNG, HEIC; maximum file size is 20MB per file; files exceeding 20MB show an inline error: "File is too large — maximum 20MB per upload"
- [ ] AC-04: Given a file is selected and within limits, then a document type label selector is displayed before upload is confirmed; required labels: Diagnosis Report / School Record / Previous Therapy Report / UDID Card / Other (with text field); upload does not proceed without a label
- [ ] AC-05: Given the upload is confirmed, then a progress bar is shown for uploads expected to take more than 2 seconds; a spinner is shown for shorter uploads
- [ ] AC-06: Given the upload completes, then the document appears in the Documents tab list with: document type label, file name, upload date, uploader name; the upload action is written to the audit trail: actor (staff ID), timestamp, file type, document type label
- [ ] AC-07: Given Dr. Sunita opens the Documents tab, then she can only view documents for children assigned to her in Care Team (INT-007); she cannot view documents for children not in her caseload
- [ ] AC-08: Given the Documents tab is accessed, then "UDID: Not provided" follow-up flag is visible at the top of the tab if UDID was not captured in the intake form; the flag is dismissible once a UDID document is uploaded or UDID number is entered in the profile
- [ ] AC-09: Given documents are uploaded, then all files are stored encrypted at rest and transmitted encrypted in transit; the Documents tab does not expose raw file URLs in the UI

**Edge Cases & Error States:**
- [ ] EC-01: If the upload fails mid-transfer (network drop), an inline error appears per file: "Upload failed — tap to retry." Previously uploaded files in the same session are not affected
- [ ] EC-02: If an unsupported file type is selected (e.g., .docx, .mp4), the file picker shows an error inline: "This file type is not supported. Supported types: PDF, JPG, PNG, HEIC"
- [ ] EC-03: If the Documents tab is accessed while the child record has consent_status = "pending", the tab shows the locked state (per INT-003) and upload is not available
- [ ] EC-04: If GET /children/{id}/documents fails, the tab shows: "Couldn't load documents. Tap to retry." with a retry button; cached document list shown if available

**Non-Functional Requirements:**
- Performance: Document list loads ≤ 2s on 4G; upload progress shown for any upload > 2s
- Offline: Document upload requires connectivity; tapping "Upload Document" while offline shows: "Uploads require an internet connection. Try again when you're connected." Cached document list is viewable offline
- Accessibility: Touch targets ≥ 44dp; document type labels and error messages are screen-reader accessible; progress bar has accessible label ("Uploading [filename]...")
- Privacy: ⚠️ DPDPA 2023 — uploaded documents are clinical records of a minor; access scoped to assigned staff only (RBAC enforced at API level); all uploads encrypted in transit (TLS 1.2 minimum) and at rest; upload action logged in immutable audit trail; document URLs are signed and time-limited (not permanent public URLs)

**Dependencies:**
- Blocked by: INT-001 (child record must exist), INT-003 (consent_status must = "confirmed" before Documents tab is accessible), INT-007 (care team assignment controls which staff can access the Documents tab)
- Enables: INT-005 (document upload completion contributes to intake completeness check)

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android (Redmi/Realme, 2GB RAM, Android 10+)
- [ ] File type and size validation tested for each supported and unsupported type
- [ ] Camera capture path tested on physical device
- [ ] Audit trail entry confirmed for each successful upload
- [ ] RBAC scoping tested: Dr. Sunita cannot view documents for unassigned children
- [ ] Encrypted storage confirmed (storage infrastructure check with engineering before merge)
- [ ] UDID follow-up flag tested: appears when UDID absent, dismissible after upload
- [ ] EC-01 through EC-04 tested
- [ ] Code reviewed and merged

---

## Story INT-005: Intake form status tracking dashboard — Not Sent / In Progress / Awaiting Consent / Completed

**As a** Rahul (Center Director)
**I want to** see the intake form completion status for every child in a dashboard view — whether the form has been sent, is in progress, is awaiting consent, or is complete — and be able to copy and resend the form link from the same screen
**So that** I can identify which families still need to complete their intake paperwork and follow up before the first session, without opening each child's record individually

**Inspired by:** Jane App intake status tracker; CentralReach authorization tracking dashboard; SimplePractice intake completion view

**Context:** This is an operational dashboard for Rahul only. It reads across all active child records and surfaces intake blockers at a glance. Access restricted to Center Director and Admin roles. Accessed from the Children List or a dedicated "Intake" tab.

**Acceptance Criteria:**
- [ ] AC-01: Given Rahul opens the Intake Status Dashboard, then all active children load within 2 seconds on 4G, each displaying: child first name, intake form status badge, consent status badge, submission timestamp (if completed), and last-activity date
- [ ] AC-02: Given the dashboard is loaded, then intake form status badges reflect the following states with distinct colors AND text labels (not color alone): "Not Sent" (grey), "In Progress" (blue), "Awaiting Consent" (amber), "Completed" (green)
- [ ] AC-03: Given a child's intake status is "Not Sent", then the child's row shows a "Copy link" action that copies the intake form URL to clipboard; a toast confirms "Link copied"
- [ ] AC-04: Given a child's intake status is "In Progress", then the child's row shows: percentage complete (e.g., "3 of 5 sections"), last-opened date, and a "Resend link" action
- [ ] AC-05: Given a child's intake status is "Awaiting Consent", then the child's row shows: "All fields complete — consent step not yet confirmed" and a "Follow up" prompt; tapping the row navigates to the child's profile consent banner (INT-003)
- [ ] AC-06: Given a child's intake status is "Completed", then the child's row shows: submission timestamp and consent timestamp; no action required
- [ ] AC-07: Given Rahul taps any child row in the dashboard, then the full child profile opens
- [ ] AC-08: Given Rahul loads the dashboard while offline, then the most recently cached state is shown with a "Showing last synced data" banner; no write actions available offline

**Edge Cases & Error States:**
- [ ] EC-01: If GET /intake/status fails, the screen shows "Couldn't load intake status. Tap to retry." with a retry button; cached data shown if available
- [ ] EC-02: If a center has more than 50 active children, the list paginates (25 per page) with a "Load more" option and total count in the header
- [ ] EC-03: If the copied intake form link has expired (> 7 days), Rahul sees a "This link has expired. Generate a new link?" prompt before copying

**Non-Functional Requirements:**
- Performance: Dashboard loads ≤ 2s on 4G; status badges are derived from server-side state fields, not client-side calculation
- Offline: Read-only cached view available; write actions (copy link, resend) require connectivity with appropriate prompts
- Accessibility: All status badges include text label alongside color indicator; touch targets ≥ 44dp
- Privacy: ⚠️ DPDPA 2023 — access to this dashboard is restricted to Center Director and Admin roles (RBAC gate at API level); therapist accounts (Priya) do not have access

**Dependencies:**
- Blocked by: INT-001 (child records must exist), INT-002 (intake form submission updates status), INT-003 (consent confirmation updates consent status)
- Enables: Follow-up actions that feed into Journey 10 (Dropout Prevention — tracking incomplete intakes as an early dropout signal)

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android (Redmi/Realme, 2GB RAM, Android 10+)
- [ ] All four status states tested end-to-end
- [ ] "Copy link" and "Resend link" actions tested
- [ ] RBAC tested: Priya (therapist role) cannot access this dashboard
- [ ] Offline cached view tested
- [ ] EC-01 through EC-03 tested
- [ ] Code reviewed and merged

---

## Story INT-006: ABHA ID linking via ABDM gateway — with graceful degradation if unavailable

**As a** Rahul (Center Director)
**I want to** optionally link a child's ABHA (Ayushman Bharat Health Account) government health ID to their center record by entering the 14-digit ABHA number or @abdm handle and verifying it via the ABDM gateway
**So that** the child's government health ID is on file for future ABDM-compatible health record integrations, without blocking enrollment if the family doesn't have one or if the gateway is unavailable

**Inspired by:** ABDM HIP integration specifications (National Health Authority, India); CentralReach external ID linking

**Context:** ABHA linking is optional and must never block enrollment. It requires the center to be registered as an ABDM Health Information Provider (HIP) — if this registration is not in place, the feature shows "unavailable" rather than failing. ABHA ID is government identity data of a minor and must be stored encrypted with admin-only access. This story does not implement the ABDM consent flow for pushing records to ABHA locker (ABDM-002 — separate consent flow, post-MVP). Rahul is the only persona who can link ABHA IDs.

**Acceptance Criteria:**
- [ ] AC-01: Given the center has completed ABDM HIP registration, when Rahul opens the child's profile and navigates to the ABHA section, then an "ABHA: Not linked" state is shown with a "Link ABHA ID" button
- [ ] AC-02: Given the center has NOT completed ABDM HIP registration, then the ABHA section shows: "ABDM features are not available — your center needs to complete ABDM HIP registration to use this feature" with a link to abdm.gov.in; the "Link ABHA ID" button is not shown; no other part of enrollment is affected
- [ ] AC-03: Given Rahul taps "Link ABHA ID", then an input accepts either a 14-digit numeric ABHA number or an @abdm handle (e.g., name@abdm); a "Verify" button triggers the ABDM gateway call
- [ ] AC-04: Given the ABDM gateway returns a valid match, then the ABHA profile name is displayed for confirmation: "ABHA verified: [name on ABHA profile]"; Rahul must tap "Confirm" to save the link
- [ ] AC-05: Given the ABHA profile name does not match the child's center record name, then a warning is shown: "ABHA name does not match the name in this record — confirm before linking"; Rahul must explicitly confirm; the mismatch is logged in the audit trail
- [ ] AC-06: Given the link is confirmed, then the child's record shows "ABHA: Verified [date]" with the ABHA number masked (last 4 digits visible); ABDM features section notes that ABDM consent (ABDM-002) is required before health records can be shared with the ABHA locker
- [ ] AC-07: Given Rahul enters an ABHA ID but the ABDM gateway is unavailable (timeout or 5xx), then the system saves the ABHA ID locally and shows "ABHA: Pending verification — will verify when gateway is available"; a background retry job queues and retries on next connectivity/gateway restoration; enrollment is not blocked
- [ ] AC-08: Given the ABHA ID was saved with "Pending verification" status, when the background retry succeeds, then the record updates to "ABHA: Verified [date]" and Rahul receives an in-app notification: "ABHA ID for [child name] has been verified."
- [ ] AC-09: Given the family does not have an ABHA ID, then Rahul can tap "Family doesn't have an ABHA ID" and the record shows "ABHA: Not available" with an informational prompt linking to abdm.gov.in/ABHA; enrollment continues unblocked

**Edge Cases & Error States:**
- [ ] EC-01: If the ABHA number format is invalid (not 14 digits or valid @abdm format), the input field shows: "Enter a valid 14-digit ABHA number or @abdm handle"
- [ ] EC-02: If the ABDM gateway returns "ABHA ID not found", the screen shows: "This ABHA ID could not be verified — check the number with the family and try again"
- [ ] EC-03: If Rahul is offline when attempting to link, the input is available but the "Verify" button is disabled with a tooltip: "Verification requires an internet connection." The ABHA ID can be entered and queued without live verification

**Non-Functional Requirements:**
- Performance: ABDM gateway call timeout set to 5 seconds; if no response, treat as gateway unavailable (path C) and queue for retry
- Offline: ABHA ID entry available; verification queued for background retry; enrollment not blocked
- Accessibility: Masked ABHA number (last 4 digits) must be screen-reader readable as "[ABHA number ending in XXXX]"; touch targets ≥ 44dp
- Privacy: ⚠️ DPDPA 2023 — ABHA ID is government identity data of a minor; stored encrypted at rest; access restricted to Center Director and Admin roles (RBAC at API level); ABHA linking action logged in immutable audit trail; ABHA number never exposed in full in the UI (last 4 digits only after linking); ABDM consent (ABDM-002) is a separate flow required before health records are transmitted to ABHA locker — this story does not implement that

**Dependencies:**
- Blocked by: INT-001 (child record must exist), INT-003 (consent_status must = "confirmed" before any health-data-adjacent action), ABDM-004 (center ABDM HIP registration — if not complete, feature shows unavailable state, not an error)
- Enables: ABDM-002 (ABDM consent for locker push — post-MVP; requires ABHA link to be in place first)

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android (Redmi/Realme, 2GB RAM, Android 10+)
- [ ] Happy path tested: enter ABHA ID, gateway verifies, name match, confirm link
- [ ] Name mismatch path tested: warning shown, confirmation required, mismatch logged
- [ ] Gateway unavailable path tested: local save, background retry queue, in-app notification on success
- [ ] ABDM HIP not registered path tested: unavailable state shown, no other functionality affected
- [ ] "Not available" path tested: record shows correctly, enrollment unblocked
- [ ] RBAC tested: Priya (therapist role) cannot access ABHA section
- [ ] EC-01 through EC-03 tested
- [ ] Encrypted storage confirmed (engineering check before merge)
- [ ] Code reviewed and merged

---

## Story INT-007: Care team assignment — assign Primary Therapist and Supervisor to child record

**As a** Rahul (Center Director)
**I want to** assign a Primary Therapist and a Clinical Supervisor to a child's record from the Care Team tab, with the assignment taking effect immediately for access control
**So that** only the assigned staff members can see and interact with the child's clinical records, and Priya and Dr. Sunita know which children they are responsible for from the moment they log in

**Inspired by:** CentralReach staff assignment and caseload management; Motivity care team role assignment; Jane App practitioner assignment

**Context:** Rahul completes care team assignment after intake form submission and document upload. The assignment immediately controls which records each staff member sees in their personal caseload views. A child without a Primary Therapist assigned cannot begin clinical sessions. Care team changes are logged in the audit trail. This is a prerequisite for session scheduling (Journey 3).

**Acceptance Criteria:**
- [ ] AC-01: Given Rahul opens a child's profile, when he navigates to the Care Team tab, then the tab is accessible even before DPDPA consent is confirmed (Care Team is one of two tabs accessible in consent-blocked state, per INT-003)
- [ ] AC-02: Given the Care Team tab opens with no staff assigned, then the empty state reads: "No staff assigned yet. Add a Primary Therapist to get started." with an "Add Staff Member" CTA
- [ ] AC-03: Given a warning banner is shown when no Primary Therapist is assigned: "This child has no assigned Primary Therapist. Clinical sessions cannot begin.", then the banner remains visible until at least one Primary Therapist is assigned
- [ ] AC-04: Given Rahul taps "Add Staff Member", then a staff picker opens as a searchable dropdown showing only active staff members from the center; deactivated accounts are not shown
- [ ] AC-05: Given Rahul selects a staff member, then a role picker is presented with options: Primary Therapist / Supervisor / Shadow Teacher / Co-Therapist; a role must be selected before the assignment can be saved
- [ ] AC-06: Given Rahul saves the assignment, then POST /children/{id}/care-team is called; on success the Care Team tab updates immediately showing: staff member name, role label, and assignment date; access control is applied within 1 second — Priya can see the child in "My Children" list; Dr. Sunita can see the child in Caseload Dashboard
- [ ] AC-07: Given Priya logs in after being assigned, then the child appears in her "My Children" list with the child's name, current intake/consent status badge, and next session date (empty if not yet scheduled)
- [ ] AC-08: Given Rahul attempts to remove the only assigned Primary Therapist, then a confirmation dialog appears: "This is the only Primary Therapist assigned. Removing them will prevent sessions from being scheduled. Remove anyway?" with an immediate prompt to assign a replacement
- [ ] AC-09: Given an assignment is saved or removed, then the action is written to the audit trail: staff ID, role, action (assigned / removed), changed_by, timestamp
- [ ] AC-10: Given Rahul opens the Care Team tab while offline, then the last-synced team composition is shown; a banner reads "Changes to care team assignments require an internet connection"

**Edge Cases & Error States:**
- [ ] EC-01: If POST /children/{id}/care-team returns 5xx, the UI shows "Could not save assignment — check your connection and try again." The optimistic UI update is reverted and the staff member does not appear in the care team list
- [ ] EC-02: If a staff member is already assigned a role on this child's care team, the staff picker shows them as "Already assigned" and does not allow a duplicate assignment
- [ ] EC-03: If the center has no active staff accounts configured, the staff picker shows: "No active staff found. Staff accounts must be created before assigning a care team."

**Non-Functional Requirements:**
- Performance: Care Team tab loads ≤ 1.5s; access control change (Priya seeing child in caseload) propagates within 1 second of successful save
- Offline: Read-only cached view available; write actions require connectivity
- Accessibility: Staff picker is searchable and keyboard-navigable; role labels are text (not icon-only); touch targets ≥ 44dp; confirmation dialog meets WCAG AA color contrast
- Privacy: ⚠️ DPDPA 2023 — care team assignment controls who has access to a minor's health data; assignment changes are logged in an immutable audit trail; access changes must propagate atomically (no window where a staff member has partial access)

**Dependencies:**
- Blocked by: INT-001 (child record must exist); staff accounts must exist (platform infrastructure prerequisite — no story ID, but must be confirmed before sprint)
- Enables: Journey 3 SCHED-001 (session scheduling requires at least one Primary Therapist assigned), Journey 6 session notes access (scoped to assigned staff), Journey 4 program design access (scoped to assigned Supervisor — post-MVP)

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android (Redmi/Realme, 2GB RAM, Android 10+)
- [ ] Access control propagation tested end-to-end: assign Priya, log in as Priya, confirm child appears in "My Children"
- [ ] Assign Dr. Sunita, log in as Dr. Sunita, confirm child appears in Caseload Dashboard
- [ ] Last-Primary-Therapist removal confirmation dialog tested
- [ ] Audit trail entry confirmed for assignment and removal
- [ ] Offline read state and write blocking tested
- [ ] EC-01 through EC-03 tested
- [ ] Code reviewed and merged

---

## Story INT-008: Child Profile Tab — pre-populated from intake form with follow-up flags for missing data

**As a** Dr. Sunita (Clinical Supervisor) or Rahul (Center Director)
**I want to** open a child's Profile tab and see all intake-form data pre-populated into structured sections — Child Details, Developmental History, Diagnosis, Prior Therapy, Family Background, UDID — with clear flags on any fields left blank by the family
**So that** I have everything I need to begin clinical planning in one place, and I can immediately see what information still needs to be collected

**Inspired by:** CentralReach client profile view; Motivity child record profile; Jane App client detail view

**Context:** The Profile tab is the central reference view for a child's record. It is read from the intake form submission (INT-002) and is editable post-intake by Rahul or Dr. Sunita. The original intake submission is preserved as a read-only audit record. Any field edited post-intake shows an "Edited [date] by [name]" label. Access is gated on consent_status = "confirmed" (per INT-003).

**Acceptance Criteria:**
- [ ] AC-01: Given a child's intake form has been submitted (INT-002), when Rahul or Dr. Sunita opens the Profile tab, then all intake fields are pre-populated into their corresponding profile sections with no manual re-entry required
- [ ] AC-02: Given the Profile tab is loaded, then it is organized into sections: Child Details, Developmental History, Diagnosis, Prior Therapy, Family Background, UDID / Government Records; each section is collapsible
- [ ] AC-03: Given a non-required intake field was left blank by the family, then the field shows "Not provided" with a follow-up flag icon and tooltip: "Collect at next visit"
- [ ] AC-04: Given the UDID field was left blank, then a persistent "UDID: Not provided — follow up" banner is shown at the top of the Profile tab until a UDID number is entered or a UDID document is uploaded (INT-004)
- [ ] AC-05: Given Dr. Sunita edits a field post-intake, then the field value updates and an "Edited [date] by [Dr. Sunita name]" label is shown inline below the field; the original intake value is preserved in a read-only audit record accessible via "View original intake submission" link
- [ ] AC-06: Given Rahul or Dr. Sunita taps "View original intake submission", then a read-only overlay displays all fields exactly as submitted by the family with the submission timestamp; no edit path is available in this view
- [ ] AC-07: Given the Profile tab is loaded, then GET /children/{id}/profile returns within 2 seconds on 4G; previously loaded profile data is available from cache when offline with a "Last synced [time]" indicator

**Edge Cases & Error States:**
- [ ] EC-01: If GET /children/{id}/profile fails, the screen shows "Couldn't load this profile. Tap to retry." with a retry button; cached profile shown if available
- [ ] EC-02: If intake form was not submitted (status "Not Sent" or "In Progress"), the Profile tab shows an empty state: "Intake form not yet submitted. Sections will be populated once the family completes the intake form." with a link to INT-005 (Intake Status Dashboard)

**Non-Functional Requirements:**
- Performance: Profile tab loads ≤ 2s on 4G; cached view loads instantly offline
- Offline: Read-only cached profile available; write actions (field edits) require connectivity
- Accessibility: "Not provided" flags must include text label alongside icon; collapsible sections must be keyboard/screen-reader navigable; touch targets ≥ 44dp
- Privacy: ⚠️ DPDPA 2023 — Profile tab is accessible only to assigned care team members and Center Director / Admin (RBAC gate at API level); original intake submission preserved as immutable audit record

**Dependencies:**
- Blocked by: INT-002 (intake form submission populates the profile), INT-003 (consent_status must = "confirmed" before Profile tab is accessible), INT-007 (care team assignment controls who sees the Profile tab)
- Enables: Journey 4 (Clinical Program Design — Dr. Sunita uses Profile tab as input to program design — post-MVP), Journey 6 (Session Notes reference child profile data)

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android (Redmi/Realme, 2GB RAM, Android 10+)
- [ ] Pre-population tested: submit intake form, open Profile tab, verify all mapped fields populated correctly
- [ ] "Not provided" flags tested for optional fields left blank
- [ ] UDID follow-up banner tested: appears when blank, clears after UDID entered
- [ ] Post-intake edit path tested: field edited, audit label visible, original submission preserved
- [ ] "View original intake submission" read-only overlay tested
- [ ] Offline cached profile tested
- [ ] RBAC tested: unassigned therapist cannot open Profile tab
- [ ] EC-01 and EC-02 tested
- [ ] Code reviewed and merged

---

## Story INT-009: Center Director Children View — operational overview with admin flags

**As a** Rahul (Center Director)
**I want to** see a single dashboard view of all active children at the center, with their consent status, intake completion status, assigned therapist, next session, and any open admin flags — and be able to filter to show only children with outstanding issues
**So that** I can run the center's enrollment pipeline from one screen and never miss a child who is stuck waiting for consent, intake, or a therapist assignment

**Inspired by:** CentralReach client dashboard; Motivity caseload overview; Jane App client list with status indicators

**Context:** This is the Center Director's operational home for enrollment pipeline visibility. It reads across all active children and surfaces admin blockers — consent pending, intake incomplete, no therapist assigned, no session scheduled. Rahul uses this view daily to check for children stuck in enrollment limbo.

**Acceptance Criteria:**
- [ ] AC-01: Given Rahul opens the Children View (Center Director role), then all active children load within 2 seconds on 4G, each card showing: child first name, consent status badge, intake status badge, assigned Primary Therapist (or "Unassigned" in red), next session date, and a count of open admin flags
- [ ] AC-02: Given the children list is loaded, then sorting defaults to: children with open admin flags first, then alphabetical by child first name
- [ ] AC-03: Given Rahul taps the "Filter by Admin Flags" control, then a filter sheet appears: All / Consent Pending / Intake Incomplete / No Therapist Assigned / No Session Scheduled; selecting a filter re-renders the list immediately
- [ ] AC-04: Given a child has zero open admin flags, then their card shows a single green "Active" indicator; no flag icons are shown
- [ ] AC-05: Given a child has one or more open admin flags, then each flag is shown as a labeled chip on their card (e.g., "Consent pending", "No therapist", "Intake incomplete")
- [ ] AC-06: Given Rahul taps any child card, then the full child profile opens
- [ ] AC-07: Given Rahul loads the view while offline, then the most recently cached list is shown with a "Showing last synced data" banner

**Edge Cases & Error States:**
- [ ] EC-01: If GET /director/children fails, the screen shows "Couldn't load children list. Tap to retry." with a retry button; cached list shown if available
- [ ] EC-02: If the center has more than 50 active children, the list paginates (25 per page) with "Load more" and a total count in the header
- [ ] EC-03: If the center has no active children, the empty state reads: "No active children yet. Enroll your first child." with a "Add New Child" CTA

**Non-Functional Requirements:**
- Performance: List loads ≤ 2s on 4G for up to 50 children; admin flag calculation is server-side, not client-side
- Offline: Cached read-only view available; write actions redirect with connectivity prompt
- Accessibility: All status badges include text label alongside color; admin flag chips include text; touch targets ≥ 44dp

**Dependencies:**
- Blocked by: INT-001, INT-003, INT-005, INT-007 (all enrollment state fields must exist to derive admin flags)
- Enables: Rahul's daily operational workflow across all journeys; connects to Journey 3 (scheduling), Journey 9 (billing), Journey 10 (dropout prevention)

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android (Redmi/Realme, 2GB RAM, Android 10+)
- [ ] All four admin flag types tested: consent pending, intake incomplete, no therapist, no session scheduled
- [ ] "Filter by Admin Flags" tested for each filter option
- [ ] Offline cached view tested
- [ ] EC-01 through EC-03 tested
- [ ] Code reviewed and merged

---

## Backlog Summary

| Story ID | Title | Persona | Complexity | Priority | Blocked by |
|---|---|---|---|---|---|
| INT-001 | Create new child record with minimum required fields and duplicate detection | Rahul | M | P0 | AUTH-001 |
| INT-003 | DPDPA consent gate at intake — integration point delegating to CONSENT-002 | Rahul, Meena | M | P0 | INT-001, CONSENT-002 |
| INT-007 | Care team assignment — assign Primary Therapist and Supervisor to child record | Rahul | M | P0 | INT-001 |
| INT-002 | Family-facing digital intake form — mobile-first, partial save, no app required | Meena, Rahul | L | P0 | INT-001, INT-003, INT-005 |
| INT-004 | Document upload for prior records — diagnosis reports, school records, UDID card | Rahul, Dr. Sunita | M | P0 | INT-001, INT-003, INT-007 |
| INT-005 | Intake form status tracking dashboard — Not Sent / In Progress / Awaiting Consent / Completed | Rahul | M | P0 | INT-001, INT-002, INT-003 |
| INT-008 | Child Profile Tab — pre-populated from intake form with follow-up flags for missing data | Rahul, Dr. Sunita | M | P1 | INT-002, INT-003, INT-007 |
| INT-009 | Center Director Children View — operational overview with admin flags | Rahul | M | P1 | INT-001, INT-003, INT-005, INT-007 |
| INT-006 | ABHA ID linking via ABDM gateway — with graceful degradation if unavailable | Rahul | L | P2 | INT-001, INT-003, ABDM-004 |

**Sprint recommendation:** INT-001 and INT-003 are the absolute foundation — nothing else can proceed without them. INT-003 has a hard dependency on CONSENT-002 (Journey 0); confirm CONSENT-002 is in progress or complete before planning INT-003. INT-007 (care team) can run in parallel with INT-003 since it is accessible in the consent-blocked state. INT-002 (intake form) is the highest-complexity story and should begin immediately after INT-001 merges. INT-006 (ABHA linking) is P2 and has a hard external dependency on ABDM HIP registration — start ABDM-004 registration process immediately as it can take 4–8 weeks.

---

## Pre-Build Decisions Required

| # | Decision | Owner | Needed by |
|---|---|---|---|
| PBD-01 | ABDM HIP registration process initiated — registration takes 4–8 weeks minimum; must start before INT-006 sprint | Rahul / Infra | Before sprint 1 kickoff |
| PBD-02 | Legal review of DPDPA consent form text (CONSENT-002) — must confirm that on-screen checkbox + finger signature is legally defensible for minors' health data under DPDPA 2023 | Legal / Product | Before CONSENT-002 sprint |
| PBD-03 | Intake form field set: what fields are truly required vs. optional — define the complete field list and section structure before INT-002 sprint | Product | Before INT-002 sprint |
| PBD-04 | Document storage provider for encrypted at-rest storage (S3/GCS with server-side encryption, or India-resident provider) | Engineering | Before INT-004 sprint |
| PBD-05 | Intake form link expiry policy — is 7 days the right window, or should it be configurable per center? | Product | Before INT-002 sprint |
| PBD-06 | Staff-assisted verbal consent: is this a valid fallback under DPDPA 2023 for opening clinical records, or must digital consent always be in place before clinical data can be entered? | Legal / Product | Before INT-003 sprint |
| PBD-07 | Intake form language: English only at launch, or does Hindi/regional language support need to ship with v1 for target metro centers? | Product | Before INT-002 sprint |

---

## ⚠️ Feature Factory Disclaimer

These stories were defined by competitive observation, journey document synthesis, and category assumptions — not by validated primary research with Indian autism therapy center directors, therapists, or parents.

**What we assumed but haven't validated:**
- [ASSUMPTION] Indian autism therapy center parents are willing and able to complete a digital intake form on a shared tablet at the center or on their own Android phone. Tech literacy and form-completion behavior among this specific parent population has not been tested. (Journey Map H-02, H-06)
- [ASSUMPTION] Center directors (Rahul) will invest the time to create child records digitally at enrollment, rather than continuing the paper/WhatsApp intake workflow they use today. The immediate value of the digital record must be obvious enough to overcome the setup cost. (Journey Map H-04)
- [ASSUMPTION] DPDPA consent captured via an on-screen checkbox and finger signature is legally defensible under DPDPA 2023 for a minor's health data in the Indian regulatory context. This requires legal review before go-live — it is not a question for engineering QA.
- [ASSUMPTION] ABHA ID adoption among families attending private Indian autism therapy centers is sufficient to make ABDM linking valuable at launch. ABDM penetration at private therapy centers is unconfirmed; the feature may see near-zero usage in v1.
- [ASSUMPTION] Therapist availability conflicts occur frequently enough in Indian centers (typically 2–5 therapists, 1–3 rooms) to warrant scheduling conflict detection logic. Small centers may not experience this as a pain point.

**What a researcher would ask before building this:**
- Do Indian autism therapy center parents experience the current intake process (paper/verbal) as painful, or is the informal, relationship-based intake part of what makes families feel comfortable with a new center? (Journey Map BP-04, H-06)
- What level of digital literacy can we realistically assume from the parent population in metro vs. tier-2 cities at launch? Does the intake form need to be completable with zero assistance, or is staff-guided completion the expected norm for v1?
- Has any Indian therapy center director tried a digital consent or intake flow? What was the operational reaction — relief at having a process, or friction from parents unfamiliar with digital consent?

**What the Product Consultant would challenge:**
- The end state for this journey spans 9 stories across 4 clusters of functionality. For v1, consider whether a "minimum viable enrollment" — INT-001 (child record) + INT-003 (consent gate) + INT-007 (care team assignment) — is sufficient to unblock Journey 3 (scheduling) and Journey 6 (session notes), deferring the digital intake form (INT-002), document upload (INT-004), and ABHA linking (INT-006) to v1.1 once therapist adoption of core workflows is proven.
- INT-003 (DPDPA consent gate) is non-negotiable and must ship in v1. INT-006 (ABHA linking) is a P2 with a hard external dependency and should not be on the critical path.

**Risk level per story:**
- INT-001 (child record creation): Low risk — table-stakes CRUD; adoption is the risk, not build complexity
- INT-003 (DPDPA consent gate): Low risk — compliance requirement is non-negotiable; legal text review is the external risk
- INT-007 (care team assignment): Low risk — well-defined RBAC pattern; adoption risk is medium
- INT-002 (intake form): Medium risk — digitizing a paper/verbal workflow; parent tech literacy assumption unvalidated
- INT-004 (document upload): Low–Medium risk — standard file upload; DPDPA encryption requirement adds infrastructure complexity
- INT-005 (intake status dashboard): Low risk — read-only derived view; depends on upstream state accuracy
- INT-008 (profile tab pre-population): Low risk — read-only derived view from intake submission
- INT-009 (director children view): Low risk — read-only operational dashboard
- INT-006 (ABHA linking): High risk — depends on ABDM HIP registration (external, 4–8 weeks) and unvalidated ABHA family uptake at private centers

Use the `/researcher` agent to validate H-06 (DPDPA intake gap) and parent tech literacy before sprint planning.
Use the `/scope` agent to challenge whether the full intake form and document upload must ship in v1 or whether consent + minimum record is sufficient to unblock clinical journeys.
Use the `/design-critique` agent to review the New Child Record Form, DPDPA Consent Form, and Intake Form before prototyping.
