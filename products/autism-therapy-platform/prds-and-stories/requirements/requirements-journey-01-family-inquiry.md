# Requirements: Journey 1 — Family Inquiry & First Contact

**Product:** Autism Therapy Platform (India)
**Journey:** Journey 1 — Family Inquiry & First Contact
**MVP status:** ✅ IN SCOPE — MVP
**Primary actor:** Rahul (Center Director / Admin)
**Supporting actor:** Meena (Parent / Primary Caregiver — receives reminder only)
**Date:** 2026-04-29
**Story ID prefix:** INQ-
**Source documents:**
- `user-journeys/journey-01-family-inquiry-first-contact.md`
- `user-journeys/journey-map.md` — Part 2, Journey 1

---

## Epic: INQ — Inquiry Pipeline & First Contact

**Goal:** Give Rahul a structured, Android-native pipeline to log, track, and follow up on inbound family inquiries — replacing WhatsApp scroll history and memory as the center's lead management system. By the end of this epic, every new inquiry is a structured record with a status, a linked intake appointment, and an automated T-24h reminder to the parent.

**Copied from:** SimplePractice (lead intake pipeline), Jane App (new client request flow), CentralReach (referral source tracking). No direct Indian competitor has this feature — TherapEZ and PractiPal cover admin and billing only; neither has an inquiry pipeline. This is a differentiator in the Indian market.

**Target user(s):** Rahul (Center Director / Admin)

**Definition of Done:**
- Rahul can log a new inquiry in under 60 seconds on minimum-spec Android (Redmi/Realme, 2GB RAM, Android 10+)
- Every inquiry record persists as a structured lead record with child name, approximate age, diagnosis, guardian name, guardian mobile, and inquiry source
- Duplicate inquiry check runs on every submission against guardian mobile number
- Rahul can schedule an intake appointment linked to the inquiry record
- A T-24h SMS or WhatsApp reminder fires automatically to the parent before the intake appointment
- Rahul can see all center inquiries in a single pipeline view sorted by status
- Inquiry statuses — Inquiry / Intake Scheduled / Enrolled / No Response — are visible at a glance and manually updateable
- All stories pass QA on minimum-spec Android (Redmi/Realme, 2GB RAM, Android 10+)
- Offline behavior confirmed for all data-write steps
- No DPDPA gate applied to this journey (no health data stored at inquiry stage)

**Out of scope (this epic):**
- Child EMR creation — Journey 2 (Intake & Enrollment)
- DPDPA consent collection — Journey 2
- Parent-facing portal or parent login
- Automated follow-up messages beyond the single T-24h appointment reminder
- CRM-style lead scoring, tagging, or custom pipeline stages
- WhatsApp Business API integration (reminder falls back to SMS if WA Business API is not configured)
- Bulk import of existing inquiry records
- Multi-center or multi-branch pipeline views

**[ASSUMPTION — NOT VALIDATED]** This epic is built on the assumption that Rahul currently tracks inquiries in WhatsApp threads or paper notebooks and experiences losing warm leads as a genuine operational pain point (H-04). No primary research with Indian center directors has confirmed this. Validate via contextual observation and director interviews before sprint planning.

---

## Story INQ-001: Log a new inquiry from the Home Screen

**As a** Rahul (Center Director)
**I want to** open a simple form and log a new family inquiry — child name, approximate age, diagnosis, parent contact, and how they reached us — while on the phone or right after a WhatsApp message
**So that** the inquiry is captured as a structured record instead of getting buried in my WhatsApp history

**Inspired by:** Jane App "New Client Request" form; SimplePractice lead intake panel

**Context:** Rahul is at his desk or on his phone when a parent contacts the center. He is often mid-conversation with the parent. He needs to log the inquiry immediately — before he forgets or before the WhatsApp thread scrolls away. Primary device: Android smartphone. Connectivity assumed at admin/front desk.

**Acceptance Criteria:**
- [ ] AC-01: Given Rahul is logged in as Center Director or Admin, when he taps "New Inquiry" on the Home Screen or Inquiry Pipeline View, then the New Inquiry Form opens in under 1.5 seconds on minimum-spec Android (2GB RAM, Android 10+)
- [ ] AC-02: Given the New Inquiry Form is open, then three fields are marked required: Child first name, Parent / guardian name, Parent mobile number (+91 prefix auto-populated)
- [ ] AC-03: Given the required fields are present, when Rahul views optional fields, then the form also shows: Child age estimate (numeric), Diagnosis (single-select: ASD / ASD with Intellectual Disability / ADHD / Cerebral Palsy / Multiple Disabilities / Other / Unknown), Inquiry source (single-select: WhatsApp / Phone call / Paediatrician referral / Parent group / Walk-in / Other), Notes (multiline free text)
- [ ] AC-04: Given Rahul taps "Save Inquiry" with all required fields completed, then the system creates the inquiry record and navigates to the Inquiry Detail View within 2 seconds
- [ ] AC-05: Given Rahul taps "Save Inquiry" with one or more required fields empty, then inline validation errors appear on each empty required field and the form does not submit
- [ ] AC-06: Given Rahul begins filling the form but loses connectivity before submitting, then a banner reads "You're offline — your form is saved locally. You'll need a connection to save the inquiry" and all entered data is preserved in device-local draft storage
- [ ] AC-07: Given a draft inquiry is saved locally, when Rahul re-opens the app after restoring connectivity, then a "Resume draft" prompt appears and loads the saved form state

**Edge Cases & Error States:**
- [ ] EC-01: If Rahul submits with an invalid mobile number format (non-10-digit after +91), the mobile field shows: "Enter a valid 10-digit mobile number"
- [ ] EC-02: If the server returns an error on POST /inquiries, the form shows "Couldn't save inquiry — tap to retry" and preserves the draft locally
- [ ] EC-03: If Rahul navigates away from an incomplete form with data entered, the system auto-saves a local draft and shows a "Draft saved" toast

**Non-Functional Requirements:**
- Performance: Form loads ≤ 1.5s on minimum-spec Android; submit and navigate ≤ 2s on 4G
- Offline: Local draft written to device storage on any field input; submit requires connectivity; draft survives app close and reopen
- Accessibility: All touch targets ≥ 44px; form operable one-handed; field labels above inputs (not placeholder-only)
- Privacy: No DPDPA gate — inquiry record stores contact info and basic demographic data only; no child health data

**Dependencies:**
- Blocked by: AUTH-001 (Rahul must be authenticated as Center Director or Admin)
- Enables: INQ-002 (duplicate check), INQ-003 (Inquiry Detail View), INQ-005 (pipeline view)

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android
- [ ] Offline draft behavior tested: close app mid-form, reopen, confirm draft loads
- [ ] EC-01 through EC-03 tested
- [ ] Code reviewed and merged

---

## Story INQ-002: Duplicate inquiry detection on guardian mobile number

**As a** Rahul (Center Director)
**I want to** see a warning when I try to save an inquiry whose parent mobile number already exists in the system
**So that** I don't accidentally create duplicate records for the same family

**Inspired by:** CentralReach duplicate client check; SimplePractice duplicate contact detection

**Context:** Runs automatically at form submission. A parent may call twice about the same child, or call about a second child. The system must surface both scenarios clearly without blocking Rahul's ability to proceed.

**Acceptance Criteria:**
- [ ] AC-01: Given Rahul submits the New Inquiry Form with a guardian mobile number matching an existing inquiry or enrolled child record, then a modal dialog appears: "This number is already in your records"
- [ ] AC-02: Given the duplicate dialog is shown, then it displays: the existing record's child name and current status, and two action buttons — "This is a different child — save new inquiry" and "Review existing record"
- [ ] AC-03: Given Rahul taps "This is a different child — save new inquiry", then the new inquiry is created with a system note: "Saved despite duplicate mobile — confirmed different child by [user name] on [date]"
- [ ] AC-04: Given Rahul taps "Review existing record", then the dialog closes, the system navigates to the existing record, and the new inquiry form is discarded
- [ ] AC-05: Given the guardian mobile is unique, then no dialog is shown and the inquiry is created without interruption

**Edge Cases & Error States:**
- [ ] EC-01: If the duplicate check API call fails, the system proceeds with inquiry creation and logs the failed check; no silent data loss
- [ ] EC-02: If multiple records match the same mobile, the dialog lists all matches; "Save new inquiry" remains available

**Non-Functional Requirements:**
- Performance: Duplicate check resolves within 1 second; if longer, show "Checking for duplicates..." inline spinner
- Offline: Duplicate check requires connectivity; if offline, saves with pending_duplicate_check flag; server-side dedup runs on sync

**Dependencies:**
- Blocked by: INQ-001
- Enables: INQ-003

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android
- [ ] EC-01 (check failure) and EC-02 (multiple matches) tested
- [ ] Offline duplicate-skip behavior confirmed
- [ ] Code reviewed and merged

---

## Story INQ-003: Inquiry Detail View with status badge

**As a** Rahul (Center Director)
**I want to** open any inquiry and see all its details on a single screen
**So that** I have one place to refer back to when following up with the family

**Inspired by:** Jane App client profile; SimplePractice client detail view

**Context:** Central view for a single inquiry record. Rahul lands here immediately after creating a new inquiry and from the pipeline view. The "Schedule Intake" CTA is the primary next-step action and must be above the fold.

**Acceptance Criteria:**
- [ ] AC-01: Given an inquiry record exists, when Rahul opens the Inquiry Detail View, then the screen displays: child first name, parent / guardian name, parent mobile (tappable — opens native dialler), child age estimate, diagnosis, inquiry source, notes, created date, and a status badge
- [ ] AC-02: Given the inquiry is viewed, then the status badge is colour-coded: "Inquiry" (grey), "Intake Scheduled" (amber), "Enrolled" (green), "No Response" (red/orange flag)
- [ ] AC-03: Given the inquiry status is "Inquiry" (no appointment scheduled), then a full-width "Schedule Intake" CTA is visible above the fold without scrolling on a standard 360dp Android screen
- [ ] AC-04: Given an intake appointment has been created, then an appointment card is shown with: date, time, duration, assigned staff name, and appointment status
- [ ] AC-05: Given Rahul taps the parent mobile number, then the native Android phone dialler opens pre-filled with the number
- [ ] AC-06: Given the screen is loaded while offline, then the most recently synced version is shown with a "Last synced [time]" indicator

**Edge Cases & Error States:**
- [ ] EC-01: If the inquiry record fails to load, the screen shows "Couldn't load this inquiry. Tap to retry."
- [ ] EC-02: If the parent mobile number is malformed in the stored record, the tappable phone link is hidden and a "—" placeholder is shown

**Non-Functional Requirements:**
- Performance: Screen loads ≤ 2 seconds on 4G; cached view loads instantly offline
- Offline: Read-only cached view available; write actions require connectivity

**Dependencies:**
- Blocked by: INQ-001
- Enables: INQ-004 (Schedule Intake CTA), INQ-006 (status update actions)

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android
- [ ] Offline cached view tested
- [ ] Code reviewed and merged

---

## Story INQ-004: Schedule intake appointment from inquiry record

**As a** Rahul (Center Director)
**I want to** create an intake appointment directly from an inquiry record — choosing date, time, duration, and optionally assigning a staff member
**So that** scheduling is part of the same workflow as logging the inquiry, not a separate step I have to remember to do later

**Inspired by:** Jane App appointment booking from client profile; SimplePractice appointment scheduling

**Context:** Rahul taps "Schedule Intake" on the Inquiry Detail View. Staff conflict detection runs if a staff member is assigned. This action triggers the T-24h reminder job.

**Acceptance Criteria:**
- [ ] AC-01: Given Rahul taps "Schedule Intake", then the Schedule Intake Screen opens with: date picker, start time picker, duration dropdown (30/45/60/90 min), optional staff assignment dropdown, and "Confirm Appointment" CTA
- [ ] AC-02: Given Rahul selects date, time, and duration and confirms with no staff assigned, then the appointment is created with status "Scheduled", inquiry status updates to "Intake Scheduled"
- [ ] AC-03: Given Rahul selects a staff member with a conflicting appointment at the chosen date/time, then an inline message appears: "This staff member has another appointment at this time." The "Confirm Appointment" button is disabled until resolved
- [ ] AC-04: Given the appointment is confirmed, then inquiry status updates from "Inquiry" to "Intake Scheduled" and the status badge reflects this immediately
- [ ] AC-05: Given an appointment is already scheduled and Rahul reschedules, then the existing appointment is cancelled and a new one created
- [ ] AC-06: Given Rahul loses connectivity mid-flow, then a banner reads "You're offline — appointment will be saved when you reconnect" and the creation is queued locally

**Edge Cases & Error States:**
- [ ] EC-01: If POST /inquiries/{id}/intake-appointment returns 5xx, the screen shows "Couldn't save appointment — tap to retry"; inquiry status NOT updated
- [ ] EC-02: If date or time is missing, inline validation errors fire and form does not submit
- [ ] EC-03: If the selected date is in the past, an inline validation error appears

**Non-Functional Requirements:**
- Offline: Appointment creation queued locally; syncs on restore
- Accessibility: Date/time pickers use native Android pickers; touch targets ≥ 44px

**Dependencies:**
- Blocked by: INQ-003
- Enables: INQ-005 (reminder job triggered at appointment creation), INQ-006 (status transitions)

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android
- [ ] Staff conflict detection tested
- [ ] Reschedule flow tested
- [ ] Code reviewed and merged

---

## Story INQ-005: Automated T-24h reminder to parent before intake appointment

**As a** Rahul (Center Director)
**I want to** have the system automatically send the parent an SMS or WhatsApp message 24 hours before their intake appointment
**So that** I don't have to remember to send a manual reminder and no-show rates at intake drop

**Inspired by:** Jane App automated reminders; SimplePractice; Theralytics reminder engine. Evidence: Psychiatric Services — 39% no-show without reminder vs. 3% with live contact.

**Context:** The reminder job is created server-side at appointment confirmation. It fires at T-24h. The message contains logistics only — no clinical information.

**Acceptance Criteria:**
- [ ] AC-01: Given an intake appointment is confirmed, then a background reminder job is created with: job ID, inquiry ID, appointment ID, trigger time (appointment start minus 24h), delivery channel (WhatsApp if WA Business API configured, otherwise SMS), template ID, and status "Scheduled"
- [ ] AC-02: Given the reminder job fires at T-24h, then the message contains: child's first name only, appointment date, appointment time, center name, and center address. No diagnosis, therapy type, or clinical information
- [ ] AC-03: Given the reminder fires successfully, then the delivery receipt is logged and Rahul can see "Reminder sent [date/time]" on the Inquiry Detail View
- [ ] AC-04: Given the reminder delivery fails, then a "Reminder failed — follow up manually" indicator appears on the Inquiry Detail View
- [ ] AC-05: Given the appointment is rescheduled, then the original reminder job is cancelled and a new one created
- [ ] AC-06: Given the appointment is cancelled before T-24h, then the reminder job is cancelled and no message is sent
- [ ] AC-07: Given the appointment was created less than 25 hours before start time, then the reminder fires immediately at job creation time

**Edge Cases & Error States:**
- [ ] EC-01: If the parent mobile number is invalid, the reminder job is immediately flagged "Undeliverable"
- [ ] EC-02: If WhatsApp Business API is not configured, reminder falls back to SMS automatically
- [ ] EC-03: If neither WA API nor DLT-registered SMS is configured, reminder job is created but cannot fire; Rahul sees a center-level warning

**Non-Functional Requirements:**
- Privacy: Reminder message template must be reviewed before DLT registration; logistics fields only; no clinical fields
- Reliability: Server-side job is idempotent — duplicate execution does not send duplicate messages
- TRAI: DLT sender ID registration required for SMS in India

**Dependencies:**
- Blocked by: INQ-004 (appointment creation), INFRA-001 (SMS provider / DLT registration), INFRA-002 (WhatsApp Business API — optional)
- Enables: INQ-006 (No Response flag logic)

**Definition of Done:**
- [ ] All AC pass QA end-to-end
- [ ] Reschedule: original job cancelled, new job created
- [ ] Cancellation: job cancelled, no message sent
- [ ] SMS fallback tested
- [ ] DLT-registered sender ID confirmed before production
- [ ] Code reviewed and merged

---

## Story INQ-006: Inquiry status management — manual updates and No Response flagging

**As a** Rahul (Center Director)
**I want to** manually update an inquiry's status and have the system automatically flag inquiries where the parent hasn't confirmed after 48 hours post-reminder
**So that** my pipeline reflects reality and I can see which families need follow-up

**Inspired by:** CentralReach referral status pipeline; Jane App status management

**Context:** Covers the full status state machine. Manual transitions are Rahul's responsibility; the "No Response" flag is system-generated. Status history is auditable.

**Acceptance Criteria:**
- [ ] AC-01: Given the inquiry status is "Inquiry", when Rahul taps "Change Status", then Rahul can manually set the status to "No Response"
- [ ] AC-02: Given the inquiry status is "Intake Scheduled" and 48 hours have elapsed since the T-24h reminder fired with no manual status update, then the system automatically sets no_response_flag = true
- [ ] AC-03: Given the no_response_flag is true, then a banner appears: "No confirmation received — consider following up via WhatsApp." The banner is dismissible
- [ ] AC-04: Given the no_response_flag is true, when Rahul views the Pipeline View, then the inquiry card shows a "No Response" indicator badge
- [ ] AC-05: Given Rahul taps "Change Status" and selects a status, then a confirmation dialog appears; status is only changed on confirm
- [ ] AC-06: Given an inquiry has status "No Response" and the family re-engages, then Rahul can change status back to "Inquiry" or "Intake Scheduled"; no_response_flag is cleared on status change
- [ ] AC-07: Given the inquiry status is updated, then a status history log entry is written: status_from, status_to, changed_by, changed_at

**Edge Cases & Error States:**
- [ ] EC-01: If PATCH /inquiries/{id}/status fails, the UI reverts the optimistic change and shows "Status update failed — tap to retry"
- [ ] EC-02: If the no_response_flag job runs but the appointment was cancelled since queuing, the flag is not set

**Non-Functional Requirements:**
- Offline: Status change requires connectivity; action blocked with "Connect to update status" prompt

**Dependencies:**
- Blocked by: INQ-003, INQ-004, INQ-005
- Enables: INQ-007 (pipeline view reads status and flag fields), Journey 2 (Enrolled status triggers conversion to child EMR)

**Definition of Done:**
- [ ] All AC pass QA on minimum-spec Android
- [ ] No Response auto-flag tested
- [ ] Status history log tested
- [ ] Code reviewed and merged

---

## Story INQ-007: Inquiry Pipeline View — all-center inquiry list with status and filter

**As a** Rahul (Center Director)
**I want to** see all of my center's inquiries in a single list view sorted by status and last-updated date, with a quick way to filter by status and spot "No Response" families at a glance
**So that** I have a single source of truth for my enrollment pipeline

**Inspired by:** SimplePractice client list; CentralReach referral pipeline; Jane App new client requests view

**Acceptance Criteria:**
- [ ] AC-01: Given Rahul opens the Inquiry Pipeline View, then all center inquiries load within 2 seconds on 4G, sorted: "No Response" flagged inquiries first, then most recently updated descending
- [ ] AC-02: Given the pipeline list is loaded, then each inquiry card displays: child first name, parent name, inquiry date, status badge, and "No Response" badge if flagged
- [ ] AC-03: Given Rahul taps any inquiry card, then the Inquiry Detail View opens
- [ ] AC-04: Given Rahul taps the filter control, then a filter sheet appears: All / Inquiry / Intake Scheduled / Enrolled / No Response; selecting a filter immediately re-renders the list
- [ ] AC-05: Given Rahul taps the "New Inquiry" FAB, then INQ-001 opens
- [ ] AC-06: Given the pipeline has no inquiries, then: "No inquiries yet. Add your first family." with a "New Inquiry" CTA
- [ ] AC-07: Given Rahul loads the pipeline while offline, then the most recently cached list is shown with a "Showing last synced data" banner; write actions are disabled

**Edge Cases & Error States:**
- [ ] EC-01: If GET /inquiries fails, the screen shows "Couldn't load inquiries. Tap to retry." If cached list exists, it is shown with an error banner
- [ ] EC-02: If a center has more than 100 inquiry records, the list paginates (20 per page) with "Load more" at bottom; total count shown in header

**Non-Functional Requirements:**
- Offline: Cached list view available; write actions blocked with connectivity prompt
- Accessibility: Status badges must include a text label alongside color (not color-only)

**Dependencies:**
- Blocked by: INQ-001, INQ-006

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android
- [ ] Empty state, filter, offline cache tested
- [ ] Status badge text-label accessibility confirmed
- [ ] Code reviewed and merged

---

## Story INQ-008: Staleness indicator on inquiry pipeline cards

**As a** Rahul (Center Director)
**I want to** see how many days have passed since I last did anything with each inquiry
**So that** I can spot warm leads that have gone cold without opening each record individually

**Inspired by:** CentralReach referral aging indicator; Jane App "days since contact"

**Acceptance Criteria:**
- [ ] AC-01: Given any inquiry card is rendered, then a "Last updated [N] days ago" label is shown, calculated from the most recent of: created_at or most recent status history entry
- [ ] AC-02: Given the inquiry was last updated today, then the label reads "Updated today"
- [ ] AC-03: Given the inquiry was last updated yesterday, then the label reads "Updated yesterday"
- [ ] AC-04: Given the inquiry was last updated 30 or more days ago, then the label is rendered in a visually distinct style to signal significant staleness
- [ ] AC-05: Given the pipeline view is rendered offline from cache, then staleness labels continue to display using stored timestamps

**Edge Cases & Error States:**
- [ ] EC-01: If last_updated_at is null, the label falls back to created_at with "Created [N] days ago"

**Non-Functional Requirements:**
- Performance: Staleness label is a client-side derived display field; no additional API call

**Dependencies:**
- Blocked by: INQ-007, INQ-006
- Enables: No downstream dependency

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android
- [ ] EC-01 tested with legacy record
- [ ] 30-day staleness styling confirmed with design before merge
- [ ] Code reviewed and merged

---

## Backlog Summary

| Story ID | Title | Persona | Complexity | Priority | Blocked by |
|---|---|---|---|---|---|
| INQ-001 | Log a new inquiry from the Home Screen | Rahul | M | P0 | AUTH-001 |
| INQ-002 | Duplicate inquiry detection on guardian mobile number | Rahul | S | P0 | INQ-001 |
| INQ-003 | Inquiry Detail View with status badge | Rahul | M | P0 | INQ-001 |
| INQ-004 | Schedule intake appointment from inquiry record | Rahul | M | P0 | INQ-003 |
| INQ-005 | Automated T-24h reminder to parent before intake appointment | Rahul | L | P0 | INQ-004, INFRA-001 |
| INQ-006 | Inquiry status management — manual updates and No Response flagging | Rahul | M | P0 | INQ-003, INQ-004, INQ-005 |
| INQ-007 | Inquiry Pipeline View — all-center list with status and filter | Rahul | M | P0 | INQ-001, INQ-006 |
| INQ-008 | Staleness indicator on inquiry pipeline cards | Rahul | S | P1 | INQ-007, INQ-006 |

**Sprint recommendation:** INQ-001 through INQ-003 are the foundation. INQ-004 and INQ-007 can be built in parallel once those merge. INQ-005 has a hard infrastructure dependency (INFRA-001: DLT SMS / WhatsApp Business API onboarding — 1–4 weeks). Start INFRA-001 immediately.

---

## Pre-Build Decisions Required

| # | Decision | Owner | Needed by |
|---|---|---|---|
| PBD-01 | SMS provider and DLT registration (Exotel, MSG91, or Kaleyra) — takes 1–4 weeks | Rahul / Infra | Before sprint 1 kickoff |
| PBD-02 | WhatsApp Business API: MVP-required or SMS-only at launch | Product | Before sprint 1 kickoff |
| PBD-03 | Is diagnosis a required or optional field on the inquiry form | Product | Before INQ-001 sprint |
| PBD-04 | Who triggers "Enrolled" status and when — manual or system-triggered after Journey 2 | Product | Before INQ-006 sprint |
| PBD-05 | Reminder message template requires legal review before DLT registration | Legal / Product | Before INFRA-001 starts |
| PBD-06 | Offline inquiry creation conflict resolution strategy on sync | Engineering | Before INQ-001 sprint |

---

## ⚠️ Feature Factory Disclaimer

These stories were defined by competitive observation, journey document synthesis, and category assumptions — not by validated primary research with Indian autism therapy center directors.

**What we assumed but haven't validated:**
- [ASSUMPTION] Rahul will adopt the habit of logging inquiries in the platform when they arrive via WhatsApp or phone, rather than continuing to use WhatsApp scroll history (H-04)
- [ASSUMPTION] Inquiry-to-enrollment pipeline visibility is a genuine and recurring pain point for Indian center directors
- [ASSUMPTION] A T-24h SMS reminder will meaningfully reduce no-show rates at intake in Indian therapy centers
- [ASSUMPTION] Duplicate detection by guardian mobile number is sufficient

**What a researcher would ask before building this:**
- How do center directors currently track warm inquiries — is losing a lead a recurring experience they recognize as a real problem? (H-04)
- Would Rahul open a separate app to log an inquiry he just received on WhatsApp, or is the context-switch too high without a native WhatsApp integration?
- What is the actual no-show rate at intake appointments in Indian centers today?

**What the Product Consultant would challenge:**
- The pipeline view only creates value if INQ-001 adoption is strong. If Rahul logs fewer than 50% of inquiries in the platform, the pipeline view becomes misleading.
- INQ-005 has a hard vendor onboarding dependency (DLT registration, 1–4 weeks) outside engineering control. Consider launching INQ-001 through INQ-004 and INQ-007 as a fast first sprint, treating INQ-005 as a second-sprint story.

**Risk level:**
- INQ-001 through INQ-003, INQ-007: Low risk — lightweight CRUD and list view; adoption is the risk, not build complexity
- INQ-004: Low–Medium — conflict detection and appointment state management add moderate complexity
- INQ-005: Medium — infrastructure dependency on DLT/WA API is outside engineering control
- INQ-006: Low — status state machine is well-defined
- INQ-008: Low — display-only derived field

Use the `/researcher` agent to validate H-04 before sprint planning.
Use the `/product-consultant` agent to pressure-test INQ-005 infrastructure dependency and sprint sequencing.
Use the `/design-critique` agent to review the New Inquiry Form and Pipeline View before prototyping.
