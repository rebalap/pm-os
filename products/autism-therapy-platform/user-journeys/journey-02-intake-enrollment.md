# User Journey: Intake & Enrollment

**Previously:** J1 (enrollment phase) | ✅ **IN SCOPE — MVP**
**Trigger:** Family arrives at the center for their intake appointment, or Rahul begins formal enrollment for a family that has expressed intent to proceed
**Primary actor:** Rahul (Center Director / Admin)
**Supporting actors:** Meena (Parent / Primary Caregiver), Dr. Sunita (Clinical Supervisor who accepts the intake and schedules assessment)
**Entry condition:** Inquiry record exists (Journey 1 complete) with intake appointment scheduled; center has an active platform account with Center Director role; at least one therapist staff account exists; the center's intake form template has been configured (INT-001); room configuration is in place for scheduling; DPDPA consent capture is part of this journey
**End state:** Child has an active EMR record with confirmed DPDPA parental consent (green badge on record), a verified intake form submission on file, all prior documents uploaded, an ABHA ID linked (if available), a Primary Therapist assigned with correct role-based access, and a first assessment session created in the calendar
**Journey source documents:**
- `cluster-1-clinical-documentation.md` — EMR-001, EMR-002, EMR-003, EMR-005
- `cluster-2-patient-records-intake.md` — INT-001 through INT-005, ABDM-001, MPM-001, MPM-002, MPM-005
- `cluster-4-scheduling-communication.md` — SCHED-001, SCHED-002

---

## Discovery Context

**Previously known as:** J1 (enrollment phase) | ✅ **IN SCOPE — MVP**

**Pain points & friction (current state without the platform):**
- No standardized intake protocol in India — process varies center to center and staff to staff ✅ PMC research: "There is no standardized protocol or critical pathway"
- Documentation collected ad hoc — staff remember to ask for some documents but not others 🔶 [HYPOTHESIS]
- DPDPA 2023 compliance risk: collecting and digitizing child health records of minors without verifiable parental consent ⚠️ ✅ DPDPA 2023 Section 9 confirmed; compliance gap in Indian centers is 🔶 [HYPOTHESIS]
- Fee agreement often verbal — no signed document creates ambiguity later 🔶 [HYPOTHESIS]
- Enrollment drop-off: some families who complete intake never return for first therapy session 🔵 Inferred — consistent with "dropout begins at enrollment" finding and Indian access barriers

**Emotional states:**
- Meena: Overwhelmed and emotionally raw. Needs to feel heard and to trust the center. This is often the first time someone has presented a structured plan for her child. ✅ Tandfonline 2025 — "caregivers must repeatedly demonstrate patience and compliance to secure support"
- Dr. Sunita: Professional, focused on clinical picture. May feel rushed if intake appointment is squeezed between clinical sessions. 🔶 [HYPOTHESIS]
- Rahul: Commercially aware — converting an inquiry to enrollment. Also carrying compliance awareness about documentation requirements. 🔶 [HYPOTHESIS]

**Current workarounds:**
- Staff rely on experience to remember what to collect — no checklist exists 🔶 [HYPOTHESIS]
- UDID documentation is produced retrospectively when families request it, rather than captured at intake 🔶 [HYPOTHESIS]

**⚠️ DPDPA exposure:**
- Step 3 (child record creation): Creating a child record constitutes processing personal data of a minor; the DPDPA consent banner must be prominently displayed before any clinical data entry is enabled.
- Step 6 (consent capture): Consent record must be write-once and immutable; cannot be captured offline; pre-checked checkboxes are not permitted under DPDPA 2023 — the consent is invalid if the checkbox is pre-selected.
- Step 10 (intake form submission): Intake form data (child health data) cannot be written to the child record until consent_status = "confirmed"; the entire transaction must roll back on server error — no partial writes.
- Step 12 (document upload): Uploaded documents are clinical records of a minor; must be encrypted in transit and at rest; upload action logged in the audit trail.
- Step 14 (ABHA linking): ABHA ID is government identity data of a minor; admin-only access; encrypted storage required; ABDM consent (ABDM-002) is a separate consent flow required before health records are pushed to ABHA locker.

---

## Step-by-Step Flow

| Step | Actor | Action | Screen / State | Technical Note |
|---|---|---|---|---|
| 1 | Rahul | Receives inquiry (WhatsApp/phone); decides to enroll — opens "Add New Child" from home screen or children list | Home Screen → "Add New Child" button | AUTH-001 gate: Rahul must be logged in as Center Director or Admin role; child list empty state shows "Add New Child" CTA |
| 2 | Rahul | Fills minimum required intake fields: child first name, date of birth, primary diagnosis (dropdown), parent/guardian name, parent mobile number | New Child Record Form (EMR-001) | Required fields: 5 fields only; form saves draft locally on connectivity loss; child record is NOT yet created until Step 3 submit; DPDPA warning visible at top of form |
| 3 | Rahul | Taps "Create Record"; system checks for duplicate (name + DOB match) | Duplicate Detection Dialog (if triggered) | API: POST /children — writes: child_id, name, DOB, diagnosis, guardian_name, guardian_mobile; duplicate check runs server-side before write; offline: form draft saved locally, submit requires connectivity |
| 4 | Rahul | Child profile screen opens; orange DPDPA banner is visible and non-dismissible: "Parental consent required — clinical records cannot be added until consent is confirmed." | Child Profile Screen (consent-blocked state) | System state: child record exists with consent_status = "pending"; all clinical tabs (Program, Notes, Documents) are locked behind the consent gate; only Profile and Care Team tabs are accessible |
| 5 | Rahul | Taps "Add consent now" from the orange banner; consent form opens | DPDPA Consent Screen (EMR-002 / INT-003) | Consent screen must load within 1 second (static screen, no complex data fetch); offline: consent cannot be captured offline — server timestamp is required for legal defensibility |
| 6 | Meena (present) or Rahul (assisted) | Reads plain-language consent summary; checks explicit opt-in checkbox (pre-checked state NOT permitted); signs on-screen with finger/stylus | DPDPA Consent Form | ⚠️ DPDPA GATE — consent record stored with: parent name, mobile, child name, timestamp (IST), form version ID, GPS coordinates (optional), signature image; record is write-once/immutable; if staff-assisted (Meena not present), flagged as "Staff-assisted verbal — digital consent pending" |
| 7 | Rahul | Taps "Confirm consent"; system writes consent record and updates child profile | Child Profile Screen (consent-confirmed state) | consent_status transitions: "pending" → "confirmed"; orange banner replaced by green "DPDPA Consent: Confirmed [date]" badge; all clinical tabs unlocked; background job: send consent confirmation notification to Meena (if WhatsApp opt-in captured) |
| 8 | Meena (on tablet/own phone) or Rahul | Opens intake form link; completes all intake form fields including developmental history, diagnosis details, prior therapy, family background, UDID number | Intake Form (INT-002) | Form renders as single-column mobile layout; partial completion saved locally for 48 hours; UDID field: if left blank, record shows "UDID: Not provided" with a follow-up flag; file upload fields accept PDF/JPG/PNG up to 10MB per file |
| 9 | Meena | Reaches end of form; DPDPA consent screen appears as final step before submission (if not already captured in Steps 5–7) | DPDPA Consent Screen embedded in intake form (INT-003) | If consent was already confirmed in Steps 5–7, this step is pre-passed and skipped; if this is the first consent capture, same write-once logic applies as Step 6; form submission is BLOCKED until consent checkbox is checked |
| 10 | Meena | Taps "Submit"; success screen appears: "Thank you. Your child's details have been received." | Intake Form Success Screen | POST /intake/submit — writes: all form fields mapped to child record; consent record written atomically with form data; on server error, entire submission is rolled back (no partial writes); tablet auto-clears after submit |
| 11 | Dr. Sunita or Rahul | Opens child's record Profile tab; sees it pre-populated from intake data with all sections: Child Details, Developmental History, Diagnosis, Prior Therapy, Family Background, Documents, UDID | Child Profile Tab (INT-004 state) | GET /children/{id}/profile — reads: all intake field mappings; original intake submission preserved as read-only audit record; fields edited post-intake show as "edited" with timestamp; "UDID: Not provided" flags visible with follow-up prompt |
| 12 | Rahul | Navigates to Documents tab; uploads additional prior documents (diagnosis report, school records, previous therapy reports, UDID card) not captured in intake form | Documents Tab (EMR-003) | File picker: device storage or camera; supported types: PDF, JPG, PNG, HEIC; max 20MB per file; document type label required at upload; upload action logged in audit trail (actor, timestamp, file type); ⚠️ DPDPA — all uploads encrypted in transit and at rest |
| 13 | Rahul | Opens Intake Status view; confirms child's record shows status "Completed" with submission and consent timestamps | Intake Status Dashboard (INT-005) | GET /intake/status — reads: form_completion_status, consent_status, submission_timestamp, consent_timestamp; access restricted to Center Director and Admin roles; if status still "In Progress" or "Awaiting Consent", Rahul sees prompts to follow up |
| 14 | Rahul | (Optional, if family has ABHA ID) Opens ABDM/ABHA section of child record; taps "Link ABHA ID"; enters 14-digit ABHA number or @abdm handle | ABHA Linking Screen (ABDM-001) | POST /abdm/verify — calls ABDM gateway API with ABHA ID; response: ABHA profile name, verification status; name mismatch warning shown if ABHA name ≠ center record name; if ABDM gateway unavailable, ABHA ID saved locally and queued for deferred verification; ⚠️ DPDPA — ABHA ID is government identity data of a minor; stored encrypted; admin-only access |
| 15 | Rahul | Opens Care Team tab on child's record; taps "Add Staff Member"; assigns Dr. Sunita as Supervisor and Priya as Primary Therapist | Care Team Tab (MPM-001) | POST /children/{id}/care-team — writes: staff_id, role (Primary Therapist / Supervisor), assignment_date; access control applied immediately: Priya can now see child in "My Children" list; Dr. Sunita can now see child in Caseload Dashboard; access change logged in audit trail |
| 16 | Priya | Opens app; home screen now shows new child in "My Children" list with "Intake incomplete" or "Active" badge depending on consent status | Therapist Home Screen — My Children List (MPM-002) | GET /therapist/{id}/caseload — reads: assigned children, next session date, consent status; child cards show: first name, status indicator, next session; list loads within 2 seconds for up to 30 children; offline: cached list available |
| 17 | Rahul | Navigates to Schedule; taps "Add Schedule" on child's profile; configures first assessment session: date/time, duration, Dr. Sunita as assigned therapist, room | Schedule Creation Screen (SCHED-001) | POST /schedules — writes: child_id, therapist_id, room_id, start_time, duration, recurrence (one-off for first assessment); conflict detection runs: checks therapist availability (SCHED-002) and room double-booking; if conflict, specific dates listed before save; offline: schedule creation queues locally, syncs on restore |
| 18 | Rahul | Confirms schedule; session appears in center calendar view with child name, Dr. Sunita, and room visible | Center Calendar View (SCHED-005) | GET /calendar — reads: all scheduled sessions for center; session card shows: child name, therapist, room, time, status (Scheduled); Rahul sees complete day/week grid; session can be tapped for quick actions |
| 19 | System | (Background) Reminder jobs scheduled: 24h and 2h pre-session SMS/email reminder to Meena | Background Job State | REMIND-001 trigger: jobs created for T-24h and T-2h based on session start time; jobs check session status at fire time — if cancelled, reminders are suppressed; DLT-registered sender ID used for SMS delivery in India |
| 20 | Rahul | Reviews child's full overview in Director Children View; confirms all flags are clear: consent confirmed, intake complete, therapist assigned, session scheduled | Center Director Children View (MPM-005) | GET /director/children — reads: all active children, consent_status, intake_status, assigned_therapist, assigned_supervisor, last_session_date, open admin flags; sort by admin flags to surface any blockers; "Filter by Admin Flags" shows only children with open issues |

---

## Decision Points

### Decision 1: Parent present at intake or completing form remotely
**At step:** 6 and 8
**Question:** Is Meena physically present at the center during intake?
- **Path A — Parent present (Happy path):** Meena signs consent in person on shared tablet; completes intake form on tablet; submission and consent captured in one sitting → Continue at Step 7
- **Path B — Parent completing remotely:** Rahul generates a form link via INT-005 ("Not Sent" → copy link); shares via WhatsApp; Meena completes form and signs consent on her own Android phone → System receives submission; DPDPA consent record created with "Remote consent — parent signed via link" flag → Continue at Step 11
- **Path C (Edge case) — Parent not present, form needed urgently:** Rahul completes form on center's behalf; consent step captures "Staff-assisted verbal" with parent name entered by Rahul; consent record flagged as "Staff-assisted verbal — collect digital consent at next visit"; orange banner on child's record remains until digital consent confirmed → Continue at Step 11 with persistent consent follow-up prompt

### Decision 2: Duplicate child record detected
**At step:** 3
**Question:** Does a record with the same first name and date of birth already exist?
- **Path A — No duplicate (Happy path):** Record created immediately → Continue at Step 4
- **Path B — Duplicate detected:** Warning dialog: "A record for a child with this name and birthdate already exists. Are you sure this is a different child?" — Rahul selects: "Confirm this is a different child" (creates new record) or "Review existing record" (navigates to existing record, journey ends for new creation)
- **Path C (Edge case) — Connectivity drops mid-form:** Form data saved as local draft; "Resume draft" prompt shown on next open; submit requires connectivity → Step 3 retried on reconnect

### Decision 3: ABHA ID availability
**At step:** 14
**Question:** Does the family have an ABHA health ID?
- **Path A — ABHA ID available and verified (Happy path):** ABHA linked with "Verified" status; ABDM-002 consent flow unlocked → Continue at Step 15
- **Path B — ABHA ID not available:** Record shows "ABHA: Not available" with informational prompt linking to abdm.gov.in/ABHA; ABDM features greyed out but center operations not blocked → Continue at Step 15
- **Path C — ABHA ID entered but ABDM gateway unavailable:** ID saved locally with status "ABHA: Pending verification"; verification queued for background retry; center operations not blocked → Continue at Step 15
- **Path D — ABHA ID verified but name mismatch:** Warning shown: "ABHA name does not match record name — confirm before linking"; Rahul must explicitly confirm; mismatch logged in audit trail

### Decision 4: Therapist availability conflict when scheduling first session
**At step:** 17
**Question:** Is the selected therapist available at the requested time, and is the room free?
- **Path A — No conflicts (Happy path):** Session created; appears in calendar → Continue at Step 18
- **Path B — Therapist conflict:** System lists specific conflicting dates/times; Rahul selects alternative slot or resolves conflict first (SCHED-002 availability update) → Retry Step 17 with new time
- **Path C — Room double-booked:** System lists which sessions conflict in that room; Rahul selects a different room or different time → Retry Step 17
- **Path D — No rooms configured (single-room center):** Room field is optional; no conflict detection on room; session created without room assignment → Continue at Step 18

### Decision 5: Intake form completion status
**At step:** 13 (Rahul reviewing intake status)
**Question:** What is the child's intake completion status?
- **Path A — Completed (Happy path):** Submission and consent timestamps confirmed; all required fields present → Continue at Step 14
- **Path B — In Progress:** Form partially filled; Rahul sees percentage complete and last-open date; can resend link via WhatsApp → Return to Step 8 prompt to family
- **Path C — Awaiting Consent:** All fields complete, consent step skipped; prompt: "Consent not yet confirmed — ask family to complete the consent step" → Return to Step 9 / 6
- **Path D — Not Sent:** Form link not yet shared with family; Rahul copies link and sends via WhatsApp → Start Step 8

---

## Screen Inventory

| Screen name | Purpose | Primary action | Personas who see it | Source story |
|---|---|---|---|---|
| Home Screen / Children List | Entry point; launch new child creation or access existing records | Tap "Add New Child" | Rahul, Dr. Sunita, Priya (filtered caseload) | EMR-005, MPM-002 |
| New Child Record Form | Capture minimum required fields to create a child record | Tap "Create Record" | Rahul (admin) | EMR-001 |
| Duplicate Detection Dialog | Alert Rahul when a matching record may already exist | Confirm new / Review existing | Rahul | EMR-001 |
| Child Profile Screen (consent-blocked) | Show child's profile with DPDPA consent gate active | Tap "Add consent now" | Rahul | EMR-002 |
| DPDPA Consent Form | Capture verifiable parental consent for data processing | Check consent checkbox + sign + confirm | Rahul, Meena | EMR-002, INT-003 |
| Child Profile Screen (consent-confirmed) | Full child profile with all tabs unlocked | Navigate to any tab | Rahul, Dr. Sunita | EMR-001, INT-004 |
| Intake Form | Family-facing form for full developmental and diagnosis history | Submit form | Meena (primary), Rahul (assisted) | INT-002 |
| Intake Form Success Screen | Confirm successful intake submission | No action required (tablet auto-clears) | Meena | INT-002 |
| Child Profile Tab | Display all intake-populated data; flag missing fields | Edit fields as needed | Rahul, Dr. Sunita | INT-004 |
| Documents Tab | Upload and view prior documents (diagnosis reports, school records, UDID card) | Upload document | Rahul, Dr. Sunita | EMR-003 |
| Intake Status Dashboard | Track completion status of all intake forms across enrolled children | Copy/resend form link | Rahul | INT-005 |
| ABHA Linking Screen | Link child's ABHA government health ID to center record | Enter ABHA ID + verify | Rahul, admin staff | ABDM-001 |
| Care Team Tab | Assign staff roles (Primary Therapist, Supervisor) to child's record | Add Staff Member | Rahul | MPM-001 |
| Therapist Home Screen — My Children | Priya's personal caseload filtered to her assigned children | Tap child card to open session tab | Priya | MPM-002 |
| Schedule Creation Screen | Create first assessment session with date, time, therapist, room | Confirm schedule | Rahul | SCHED-001 |
| Therapist Availability Screen | Configure therapist working hours and blocked slots | Set working days and hours | Rahul | SCHED-002 |
| Center Calendar View | All-center view of sessions, therapists, rooms for the day/week | Tap session card for quick actions | Rahul | SCHED-005 |
| Center Director Children View | Full operational overview: all children, staff, flags, consent status | Filter by admin flags | Rahul | MPM-005 |

---

## Designer Handoff

### Screen: New Child Record Form

**Purpose:** Create the minimum viable record for a new child at the moment of enrollment — fast enough to do on an Android phone during or after a family's first visit
**Primary action:** Tap "Create Record"
**Entry point(s):** "Add New Child" button on Home Screen or Children List
**Exit point(s):** On success → Child Profile Screen (consent-blocked state); on duplicate detection → Duplicate Detection Dialog

**Key components:**
- Section header: "Child Details" — with inline note: "You only need 5 fields to get started. Add more later."
- Required field group: Child first name (text), Date of birth (date picker — native Android), Primary diagnosis (single-select dropdown: ASD / ASD with intellectual disability / ADHD / Cerebral Palsy / Multiple disabilities / Other), Parent/guardian name (text), Parent/guardian mobile number (phone input with +91 prefix)
- Optional fields toggle: "Add more details (optional)" — expands to show full optional field list (gender, address, second guardian, language preference, UDID, school, emergency contact)
- DPDPA notice banner at top (non-dismissible, amber): "You'll need to confirm parental consent before adding clinical records. You can do this right after creating the record."
- "Create Record" primary CTA button (full-width, high contrast)

**States:**
- **Empty state:** Form loads blank with all required fields empty; optional fields collapsed
- **Loading state:** "Creating record..." spinner on CTA button; form fields disabled
- **Error state:** Inline validation on each required field if left blank on submit; duplicate detection dialog if name + DOB match found
- **Offline state:** Banner: "You're offline — your form is saved locally. You'll need a connection to create the record."

**Constraints:**
- Touch targets ≥ 44px on all fields and the CTA
- Date of birth uses native Android date picker (not a custom component) for screen reader compatibility
- Form must load in ≤ 1.5 seconds on minimum-spec Android (2GB RAM, Android 10+)
- One-handed operable: all required fields reachable without landscape mode

---

### Screen: DPDPA Consent Form

**Purpose:** Capture verifiable, legally defensible parental consent for processing a minor's health data under DPDPA 2023 — the single most important compliance step in the product
**Primary action:** Check explicit consent checkbox + draw finger signature + tap "Confirm consent"
**Entry point(s):** "Add consent now" from orange banner on Child Profile; or as final step of Intake Form submission
**Exit point(s):** On confirmation → Child Profile Screen (consent-confirmed); all clinical tabs unlock

**Key components:**
- Plain-language consent summary (max 150 words): what data is collected, why, who accesses it, retention period, how to withdraw — NO legal jargon
- Explicit opt-in checkbox: "I confirm I am the legal parent/guardian of [child name] and consent to collection and processing of their health data as described above" — checkbox starts unchecked, cannot be pre-checked
- Signature capture field: minimum 200×100px; works with finger or stylus; shows "Sign here" placeholder with pen icon
- Parent name field (auto-filled from child record if already entered; editable)
- Date (auto-filled with today's date; read-only)
- "Confirm consent" CTA (disabled until checkbox checked AND signature drawn)
- "Staff-assisted verbal" secondary option: small link text at bottom — "Parent not present? Record verbal consent" — opens a separate assisted flow with additional flag warnings

**States:**
- **Empty state:** Checkbox unchecked; signature field blank; CTA disabled (greyed)
- **Loading state:** "Saving consent record..." spinner; form locked
- **Error state:** If server error on save: "Something went wrong — your information has not been saved. Please try again." — full rollback; no partial write
- **Offline state:** "An internet connection is required to complete consent. Your form answers are saved and will be here when you reconnect." — submit blocked; no fallback

**Constraints:**
- Consent text minimum font size 16px; meets WCAG AA for body text
- Checkbox touch target ≥ 44px
- Full consent text must be screen-reader readable
- CTA cannot be enabled without both checkbox check AND signature present (not one or the other)
- Consent record is immutable after confirmation — no edit path exists; only "View consent record"

---

### Screen: Intake Form (family-facing)

**Purpose:** Capture full developmental history, diagnosis details, prior therapy, and family background from the parent — replacing paper intake and verbal information gathering
**Primary action:** Complete all fields and tap "Submit"
**Entry point(s):** Form link shared via WhatsApp (opens in browser or in-app); or staff opens form on shared center tablet
**Exit point(s):** On submit → DPDPA Consent Screen (if not yet captured); on consent confirmed → Intake Form Success Screen

**Key components:**
- Single-column mobile layout; section headers with field groups (Child Details, Developmental History, Diagnosis, Prior Therapy, Family, UDID/Documents)
- Required field indicators (red asterisk + "Required" label — not color alone)
- File upload fields: device storage or camera; type: PDF/JPG/PNG; max 10MB; upload progress bar for uploads > 2 seconds
- "Save and continue later" link (saves progress for 48 hours to same device/link)
- Progress indicator: "Section 2 of 5" header to reduce perceived complexity
- Submit button: visible only on final section

**States:**
- **Empty state:** All fields blank on first open
- **Loading state:** Skeleton placeholders while form template fetches; "Loading your form..." text
- **Error state:** Required field highlighted in red border + error text label (not color alone); scroll-to-first-error on submit attempt; file upload error shows inline per field
- **Offline state:** "No connection — your answers are saved. Submit when you have internet." — partial save preserved; clear messaging that data is not lost

**Constraints:**
- Font size minimum 16px throughout
- Touch targets ≥ 44px
- Must be completable by a non-tech-confident parent with minimal assistance
- Tablet: auto-clear all data on submit (no personal data visible to next user)
- Link expiry: if link older than 7 days, show human-readable expiry message with center contact details

---

### Screen: Care Team Tab

**Purpose:** Assign staff members to the child's record with defined roles — controls who can see and interact with the record
**Primary action:** Add Staff Member (assign Primary Therapist and Supervisor)
**Entry point(s):** Child Profile → "Care Team" tab
**Exit point(s):** Saved assignment immediately unlocks record access for assigned staff; no navigation away required

**Key components:**
- Staff list: current care team members with role labels, assignment dates, and "Remove" action
- "Add Staff Member" button
- Staff picker: searchable dropdown from center's active staff list
- Role picker: Primary Therapist / Supervisor / Shadow Teacher / Co-Therapist
- Warning banner if no Primary Therapist assigned: "This child has no assigned Primary Therapist. Clinical sessions cannot begin."

**States:**
- **Empty state (new record):** "No staff assigned yet. Add a Primary Therapist to get started." — with "Add Staff Member" CTA
- **Loading state:** Staff list skeleton while fetching assignments
- **Error state:** If assignment save fails: "Could not save assignment — check your connection and try again." — no partial assignment state
- **Offline state:** Reads from cached last-synced state; "Changes to assignments require an internet connection" message if attempting write while offline

**Constraints:**
- Cannot remove the only Primary Therapist without a confirmation dialog + immediate reassignment prompt
- Deactivated staff not shown in the staff picker
- Assignment changes logged in immutable audit trail

---

### Screen: Schedule Creation Screen

**Purpose:** Create the first assessment session for the newly enrolled child
**Primary action:** Confirm schedule
**Entry point(s):** Child Profile → "Add Schedule"; or Center Calendar → "+" button
**Exit point(s):** On success → Center Calendar View showing new session; optional: back to Child Profile

**Key components:**
- Day-of-week selector (chip group: Mon / Tue / Wed / Thu / Fri / Sat)
- Start time picker (native Android time picker)
- Duration picker (dropdown: 30 min / 45 min / 60 min / 90 min)
- Therapist assignment (searchable dropdown, filtered to available therapists)
- Room assignment (dropdown, optional for single-room centers)
- Recurrence toggle: "One-off session" vs. "Recurring weekly"
- Conflict summary (shown inline before save if conflicts detected)

**States:**
- **Empty state:** All fields blank; therapist dropdown shows full staff list
- **Loading state:** "Checking availability..." while conflict detection runs
- **Error state — therapist conflict:** Inline list of conflicting dates with note: "Priya is not available on these dates — select a different time or update her availability"
- **Error state — room conflict:** Inline list of conflicting dates for the selected room
- **Offline state:** "Saved locally — session will appear in the calendar when you reconnect."

**Constraints:**
- Therapist availability must be configured (SCHED-002) before conflict detection works; if not configured, show a setup prompt
- Past sessions not modifiable when editing a series
- For first assessment session: one-off session is the default mode (not recurring weekly)

---

## Developer Handoff

### Step-level technical summary

| Step | Data written | Data read | API / event | Offline behavior | Regulatory gate |
|---|---|---|---|---|---|
| 2 | Form draft (local only) | None | None — local draft only | Write draft to device storage | None yet — no health data written |
| 3 | child_id, first_name, DOB, diagnosis_code, guardian_name, guardian_mobile, center_id, created_by, created_at | Duplicate check: name + DOB lookup | POST /children | Queue locally; submit requires connectivity | DPDPA: Creating record is processing personal data of a minor — consent prompt at Step 4 is mandatory gate |
| 6 | consent_record_id, parent_name, parent_mobile, child_id, timestamp_IST, form_version_id, signature_image_url, gps_coords (optional), consent_type (in-person / remote / staff-assisted) | Child record: child_name, DOB | POST /consent | CANNOT be captured offline — server timestamp required; if offline, show blocking message | ⚠️ DPDPA MASTER GATE — consent record is write-once, immutable; schema-level block on update/delete |
| 7 | child.consent_status = "confirmed" | consent_record | PATCH /children/{id}/consent_status | N/A (online only) | DPDPA — unlocks clinical data write access for this child |
| 10 | All intake form fields → child record fields; document file objects | child_id, consent_status (must = "confirmed") | POST /intake/submit (atomic — form fields + document uploads in one transaction) | Partial save locally; full submit requires connectivity; server error = full rollback, no partial writes | ⚠️ DPDPA — form data is health data of a minor; consent_status must = "confirmed" before any intake data is written to child record |
| 12 | document_id, document_type, document_url (encrypted storage), uploader_id, upload_timestamp, file_size | child_id, consent_status | POST /children/{id}/documents | Upload requires connectivity; retry on failure | ⚠️ DPDPA — uploaded documents are child health records; access scoped to assigned staff; upload action in audit log |
| 14 | abha_id (encrypted), abha_verification_status, abha_profile_name, verification_timestamp | ABDM gateway: ABHA ID validity | POST /abdm/link-abha → ABDM Gateway API | ABHA ID stored locally; verification queued for when connectivity/ABDM gateway available | ⚠️ DPDPA — ABHA ID is government identity data of a minor; admin-only access; encrypted at rest |
| 15 | care_team_assignment: child_id, staff_id, role, assigned_by, assigned_at | Staff list for center | POST /children/{id}/care-team | Reads from cache; writes require connectivity | RBAC gate: role assignment immediately changes which records each staff member can access; logged in immutable audit trail |
| 17 | session_id, child_id, therapist_id, room_id, start_time, duration, recurrence_rule, status="Scheduled" | Therapist availability, room bookings (for conflict detection) | POST /schedules | Queue locally; sync on restore | ⚠️ DPDPA — session schedule is health-adjacent data for a minor; parental consent must be confirmed (Step 7) before schedule is created |
| 19 | reminder_job_id, session_id, trigger_time (T-24h, T-2h), channel, template_id, status="Scheduled" | Session start_time, parent mobile/email | Background job: REMINDER_SCHEDULE event | Server-side job; client reflects status on next sync | DPDPA — reminder message must not include clinical data; logistics only (child name, date, time, center name) |

**Key state transitions:**
- child.consent_status transitions: "pending" → "confirmed" at Step 7
- session.status transitions: "Scheduled" → "Present" / "Absent" / "No-show" / "Cancelled" at SCHED-004 (attendance marking — in Journey 3)
- care_team_assignment.status transitions: "none" → "active" at Step 15 for each assigned staff member
- intake_form.completion_status transitions: "Not Sent" → "In Progress" → "Awaiting Consent" → "Completed" across Steps 8–10

**Background jobs / async events triggered by this journey:**
- REMINDER_SCHEDULE job: triggered at Step 17 (session creation); fires at T-24h and T-2h from session start time
- ABDM_VERIFY queue: triggered at Step 14 if gateway unavailable; retries when connectivity restores
- CONSENT_CONFIRMATION notification (optional): triggered at Step 7; sends WhatsApp/SMS confirmation to parent that consent has been recorded (requires WA opt-in or SMS number)

**DPDPA compliance checkpoints:**
- Step 3: ⚠️ DPDPA — creating a child record constitutes processing personal data of a minor; consent prompt must be prominently displayed before any clinical data entry is enabled
- Step 6: ⚠️ DPDPA MASTER GATE — consent record must be captured; write-once/immutable; retained for minimum 3 years post-discharge; cannot be captured offline
- Step 10: ⚠️ DPDPA — intake form data (health data) cannot be written to child record until consent_status = "confirmed"; atomic transaction ensures no partial writes
- Step 12: ⚠️ DPDPA — uploaded documents are clinical records of a minor; encrypted in transit and at rest; access scoped by role assignment; upload logged in audit trail
- Step 14: ⚠️ DPDPA — ABHA ID is government identity data; encrypted storage; admin-only access; ABDM consent (ABDM-002) is a separate consent flow required before health records are pushed to ABHA locker

---

## Cross-Journey Dependencies

| Depends on journey | Why | What breaks if missing |
|---|---|---|
| Journey 1: Family Inquiry & First Contact | Journey 2 begins after the inquiry record exists and the intake appointment has been scheduled | Without Journey 1 completed, there is no inquiry record to transition to an EMR; Rahul may still create a child record directly (the flow still works), but the pipeline state is inconsistent |
| Platform authentication & user accounts (AUTH-001) | Rahul must be logged in as Center Director role before any child record can be created | Journey cannot start; no "Add New Child" access |
| Staff account creation (infrastructure) | Therapist accounts must exist before Step 15 (Care Team assignment) and Step 17 (schedule creation with assigned therapist) | Care team cannot be populated; scheduling picks up "no staff available" error; Priya cannot appear in "My Children" view |
| Intake form template configuration (INT-001) | Intake form template must be published before family-facing form is accessible | Intake form URL is broken; family cannot complete digital intake; record pre-population (INT-004) does not occur |
| Journey 4: Clinical Program Design | Journey 4 starts only after this journey's end state is reached: child record active, consent confirmed, therapist assigned | No therapy program can be created without an active child record; Dr. Sunita cannot access Caseload Dashboard entry for this child without Supervisor assignment |
| Room configuration (infrastructure) | Session creation (Step 17) requires at least one room configured if room conflict detection is to be meaningful | Scheduling proceeds without room assignment; no double-booking prevention |
| WhatsApp Business API setup (WA-001) and SMS/email provider (REMIND-001 infra) | Reminder jobs created at Step 19 require a delivery channel | Reminder jobs are created but cannot fire; parents receive no appointment reminders; session no-show rate may be higher |
| ABDM HIP registration (ABDM-004) | ABHA linking at Step 14 requires center to be registered as ABDM HIP | ABHA link screen shows "ABDM features unavailable — ABDM HIP registration required"; Step 14 is skipped entirely without blocking the rest of the journey |

---

## ⚠️ Feature Factory Disclaimer

These flows were defined by competitive observation, document synthesis, and category assumption — not by validated user research with Indian autism therapy center staff or families. Before committing engineering capacity or design effort:

**What we assumed but haven't validated:**
- [ASSUMPTION] Indian autism therapy center parents are willing and able to complete a digital intake form, either on a shared tablet at the center or on their own Android phone. Tech literacy and form-completion behavior among this specific parent population has not been tested. (Journey Map H-02, H-06)
- [ASSUMPTION] Center directors (Rahul) will invest the time to create child records digitally at enrollment, rather than continuing the paper/WhatsApp intake workflow they use today. The product must offer enough immediate value at enrollment to offset the data entry effort. (Journey Map H-04)
- [ASSUMPTION] DPDPA consent captured via an on-screen checkbox and finger signature will be legally defensible under DPDPA 2023 for a minor's health data in the Indian regulatory context. This requires legal review before go-live, not just engineering QA.
- [ASSUMPTION] ABHA ID adoption among families attending private Indian autism therapy centers is sufficient to make ABDM linking valuable at launch. ABDM penetration at private therapy centers is unconfirmed. (Cluster 2 disclaimer)
- [ASSUMPTION] Therapist availability conflicts are frequent enough in Indian centers to warrant enforcement logic in the scheduling flow. Small centers (2–3 therapists, 1–2 rooms) may not experience scheduling conflicts as a pain point.

**What a researcher would ask before building this:**
- Do Indian autism therapy center parents experience the current intake process (paper/verbal) as painful? Or is the informal, relationship-based intake part of what makes families feel comfortable? (Journey Map BP-04, H-06)
- What level of digital literacy can we assume from the parent population in metro vs. tier-2 cities at launch? Does the intake form need to be completable with zero assistance, or is staff-guided completion the expected norm?
- Has any Indian therapy center director tried a digital consent flow for DPDPA compliance? What was the reaction — relief, confusion, or resistance? (H-06 directly)

**What the Product Consultant would challenge:**
- The end state defined for this journey requires 20 steps across 4 clusters of functionality. For a v1, consider whether a "minimum viable enrollment" — child record + consent only (Steps 1–7) — is sufficient to unblock Journey 4 (Clinical Program Design), and whether document upload, ABHA linking, and the full intake form can be deferred to v1.1 once therapist adoption of session notes is proven.
- The DPDPA consent flow is non-negotiable and must ship in v1. Everything else in this journey is sequenceable.

**Risk level:**
- Steps 1–7 (record creation + consent): Low risk — table stakes for a clinical platform; compliance requirement is non-negotiable
- Steps 8–13 (intake form + document upload): Medium risk — digitizing an intake that is currently paper/verbal; parent tech literacy assumption unvalidated
- Step 14 (ABHA linking): High risk — depends on ABDM HIP registration and unvalidated ABHA family uptake
- Steps 15–20 (staff assignment + scheduling): Low–Medium risk — table stakes in US/global platforms; Indian market adoption assumption unvalidated

Use the `/research` agent to validate H-06 (DPDPA intake gap) and parent tech literacy before sprint planning.
Use the `/scope` agent to challenge whether the full intake form must ship in v1 or whether consent + minimum record is sufficient to unblock clinical journeys.
