# User Journey: Family Inquiry & First Contact

**Previously:** J1 (inquiry phase) | ✅ **IN SCOPE — MVP**
**Trigger:** A parent contacts the center for the first time — via WhatsApp, phone call, or referral from a paediatrician or parent group
**Primary actor:** Rahul (Center Director / Admin)
**Supporting actors:** Meena (Parent / Primary Caregiver)
**Entry condition:** Center has an active platform account; an "Inquiries" or lead capture workflow is configured
**End state:** Inquiry captured as a structured record with child name, age, diagnosis, parent contact; intake appointment scheduled; automated reminder set; inquiry status visible in center pipeline view
**Journey source documents:**
- `cluster-2-patient-records-intake.md` — INT-001 (intake form trigger), MPM-005 (pipeline visibility)
- `cluster-4-scheduling-communication.md` — SCHED-001 (appointment creation), REMIND-001 (reminder)

---

## Discovery Context

**Previously known as:** J1 (inquiry phase) | ✅ **IN SCOPE — MVP**

**Pain points & friction (current state without the platform):**
- Inquiry details are captured in a WhatsApp thread or paper note with no structured record — information is easily lost 🔶 [HYPOTHESIS]
- No pipeline visibility: Rahul has no way to see how many families are in inquiry vs. enrolled state 🔶 [HYPOTHESIS]
- No automated follow-up if the family does not respond to the appointment invite 🔶 [HYPOTHESIS]

**Emotional states:**
- Meena: Anxious, hopeful, exhausted from a long diagnostic journey. High emotional stakes — this contact matters. ✅ Supported by Tandfonline 2025 research on caregiver emotional burden at entry into services
- Rahul: Pragmatic — this is a new enrollment opportunity. 🔵 Inferred

**Current workarounds:**
- Staff rely on memory and WhatsApp scroll history to follow up on warm leads 🔶 [HYPOTHESIS]
- Some centers may use a WhatsApp Business label to tag "new inquiry" families 🔶 [HYPOTHESIS]

---

## Step-by-Step Flow

| Step | Actor | Action | Screen / State | Technical Note |
|---|---|---|---|---|
| 1 | Meena | Sends a WhatsApp message or makes a phone call to the center — asks about therapy availability for her child | Outside platform (WhatsApp / phone) | No platform action at this step; inquiry arrives in Rahul's personal or business WhatsApp or as an incoming call |
| 2 | Rahul | Opens the platform; taps "New Inquiry" from the Home Screen or Inquiry Pipeline View | Home Screen → "New Inquiry" button | AUTH-001 gate: Rahul must be logged in as Center Director or Admin role; if no inquiries exist, empty state shows "Add your first inquiry" CTA |
| 3 | Rahul | Fills the New Inquiry Form: child first name, approximate age or date of birth, primary diagnosis (dropdown or free text), parent / guardian name, parent mobile number (WhatsApp), and inquiry source (dropdown: WhatsApp / Phone call / Paediatrician referral / Parent group / Walk-in / Other) | New Inquiry Form | Required fields: child first name, parent name, parent mobile; all other fields are optional but prompted; form saves draft locally on connectivity loss; no child record is created at this step — this is a lead record only; no DPDPA gate applies yet (no health data stored) |
| 4 | Rahul | Taps "Save Inquiry"; system checks for duplicate inquiry by parent mobile number | Duplicate Inquiry Dialog (if triggered) | API: POST /inquiries — writes: inquiry_id, child_name, child_age_estimate, diagnosis_notes, guardian_name, guardian_mobile, inquiry_source, center_id, created_by, created_at, status="Inquiry"; duplicate check: if a record with the same guardian mobile already exists, Rahul sees a warning dialog with options to review the existing record or confirm this is a different inquiry; offline: draft saved locally; submit requires connectivity |
| 5 | Rahul | Inquiry record created; system opens the Inquiry Detail View with status badge "Inquiry" | Inquiry Detail View (status: Inquiry) | GET /inquiries/{id} — reads: all fields from Step 3; status chip is colour-coded: "Inquiry" (grey), "Intake Scheduled" (amber), "Enrolled" (green), "No Response" (red); no clinical tabs exist at this stage — inquiry record is a lead record, not a child EMR |
| 6 | Rahul | Taps "Schedule Intake" on the Inquiry Detail View; selects a date, time, duration, and (optionally) assigns a staff member to conduct the intake | Schedule Intake Screen | POST /inquiries/{id}/intake-appointment — writes: appointment_id, inquiry_id, scheduled_date, scheduled_time, duration, assigned_staff_id (optional), status="Scheduled"; conflict detection runs against existing appointments for the assigned staff member if specified; offline: appointment creation queues locally; syncs on restore |
| 7 | Rahul | Confirms the appointment; inquiry status updates to "Intake Scheduled" | Inquiry Detail View (status: Intake Scheduled) | PATCH /inquiries/{id}/status — writes: status="Intake Scheduled", intake_appointment_id; appointment card appears on the Inquiry Detail View with date, time, and assigned staff |
| 8 | System | Automated reminder job created: SMS or WhatsApp reminder to Meena 24 hours before the intake appointment | Background Job State | REMIND-001 trigger: job created at appointment creation time; fires at T-24h from appointment start; reminder message contains: child name (first name only), appointment date, appointment time, center name, center address; ⚠️ DPDPA — reminder message must not include diagnosis or clinical details; logistics only; DLT-registered sender ID used for SMS in India |
| 9 | Rahul | Can view all open inquiries and their statuses in the Inquiry Pipeline View — sorted by status and last-updated date | Inquiry Pipeline View (MPM-005) | GET /inquiries — reads: all inquiries for center; pipeline columns or list view: Inquiry → Intake Scheduled → Enrolled → No Response; Rahul can filter by status, sort by date, and tap any inquiry to open the Inquiry Detail View; offline: cached list available |
| 10 | System | At T-24h before the appointment, reminder fires to Meena via SMS or WhatsApp (if WhatsApp Business API is configured) | SMS / WhatsApp delivery | REMIND-001 job executes: checks appointment status at fire time — if appointment is cancelled or rescheduled, reminder is suppressed; delivery receipt logged against the inquiry record; failed delivery flagged for manual follow-up by Rahul |

---

## Decision Points

### Decision 1: How did the inquiry arrive?

**At step:** 3 (inquiry source field)

**Question:** Through what channel did Meena first contact the center?
- **Path A — WhatsApp or phone call:** Rahul enters details manually into the New Inquiry Form immediately after or during the conversation. Inquiry source: WhatsApp / Phone call. → Continue at Step 4
- **Path B — Walk-in at center:** Family visits without prior contact. Rahul opens the New Inquiry Form at the front desk or on his phone while with the family. Inquiry source: Walk-in. → Continue at Step 4
- **Path C — Referral from a paediatrician or parent group:** Rahul notes the referral source in the inquiry source field and may add a note in the optional notes field (referring doctor name, parent group name). → Continue at Step 4

---

### Decision 2: Is this a duplicate inquiry?

**At step:** 4 (on form submission)

**Question:** Does a record with the same parent mobile number already exist in the system?
- **Path A — No duplicate (Happy path):** Inquiry record created immediately → Continue at Step 5
- **Path B — Duplicate detected (same guardian mobile):** Warning dialog: "An inquiry or record already exists for this contact number. Are you sure this is a different child?" — Rahul selects: "Confirm this is a different child" (creates new inquiry) or "Review existing record" (navigates to existing inquiry or child record; journey ends for new creation)
- **Path C — Connectivity drops mid-form:** Form data saved as local draft; "Resume draft" prompt shown on next open; submit requires connectivity → Step 4 retried on reconnect

---

### Decision 3: Parent non-responsive after scheduling

**At step:** 9–10 (pipeline follow-up)

**Question:** Has Meena responded to or confirmed the intake appointment?
- **Path A — Parent confirms or attends (Happy path):** Appointment proceeds; Rahul manually updates inquiry status to "Enrolled" after intake completion (triggers Journey 2). → Journey ends; Journey 2 begins
- **Path B — No response within 48 hours of the reminder:** System flags the inquiry with a "No Response" indicator in the pipeline view; Rahul sees a follow-up prompt on the Inquiry Detail View: "No confirmation received — consider following up via WhatsApp." Rahul takes manual action. No automated escalation beyond the flag.
- **Path C — Parent contacts to reschedule:** Rahul opens the Inquiry Detail View; taps "Reschedule Intake"; selects a new date and time; reminder job cancels the previous T-24h fire and creates a new one for the updated appointment time. → Inquiry status remains "Intake Scheduled"

---

## Screen Inventory

| Screen name | Purpose | Primary action | Personas who see it | Source story |
|---|---|---|---|---|
| Home Screen | Entry point; launch new inquiry or open pipeline view | Tap "New Inquiry" | Rahul | MPM-005 |
| New Inquiry Form | Capture minimum required fields for a new lead / family inquiry | Tap "Save Inquiry" | Rahul | INT-001 |
| Duplicate Inquiry Dialog | Alert Rahul when an existing record shares the same guardian mobile | Confirm new / Review existing | Rahul | INT-001 |
| Inquiry Detail View | Full view of a single inquiry record with status, contact details, and appointment card | Tap "Schedule Intake" | Rahul | MPM-005, SCHED-001 |
| Schedule Intake Screen | Create an intake appointment linked to the inquiry record | Confirm appointment | Rahul | SCHED-001 |
| Inquiry Pipeline View | All-center view of inquiries in each status stage | Tap inquiry card to open detail | Rahul | MPM-005 |

---

## Designer Handoff

### Screen: New Inquiry Form

**Purpose:** Capture the minimum viable information about a new family lead — fast enough to do on an Android phone while speaking to a parent on the phone or in person
**Primary action:** Tap "Save Inquiry"
**Entry point(s):** "New Inquiry" button on Home Screen or Inquiry Pipeline View
**Exit point(s):** On success → Inquiry Detail View; on duplicate detection → Duplicate Inquiry Dialog

**Key components:**
- Section header: "New Inquiry" — with inline note: "3 required fields. Add more if you have them."
- Required field group: Child first name (text), Parent / guardian name (text), Parent mobile number (phone input with +91 prefix)
- Optional fields: Child age estimate (number input — "How old is the child?"), Diagnosis (free text or single-select dropdown: ASD / ASD with intellectual disability / ADHD / Cerebral Palsy / Multiple disabilities / Other / Unknown), Inquiry source (single-select: WhatsApp / Phone call / Paediatrician referral / Parent group / Walk-in / Other), Notes (multiline text — "Anything else to note?")
- "Save Inquiry" primary CTA button (full-width, high contrast)

**States:**
- **Empty state:** Form loads blank with all fields empty
- **Loading state:** "Saving inquiry..." spinner on CTA button; form fields disabled
- **Error state:** Inline validation on each required field if left blank on submit; duplicate detection dialog if guardian mobile match found
- **Offline state:** Banner: "You're offline — your form is saved locally. You'll need a connection to save the inquiry."

**Constraints:**
- Touch targets ≥ 44px on all fields and the CTA
- Form must load in ≤ 1.5 seconds on minimum-spec Android (2GB RAM, Android 10+)
- One-handed operable: all required fields reachable without landscape mode
- No DPDPA gate at this step — no health data is being stored; only contact and basic demographic information

---

### Screen: Inquiry Pipeline View

**Purpose:** Give Rahul a single view of all active inquiries and their conversion status — replacing WhatsApp scroll history and memory as the lead tracking tool
**Primary action:** Tap an inquiry card to open the Inquiry Detail View
**Entry point(s):** Home Screen → "Inquiries" tab or shortcut

**Key components:**
- List or kanban-style pipeline with status columns: Inquiry / Intake Scheduled / Enrolled / No Response
- Inquiry cards: child first name, parent name, inquiry date, status badge, days since last update
- "No Response" flag indicator on cards where parent has not confirmed after 48h
- "New Inquiry" FAB (floating action button) to create a new inquiry from this screen
- Filter / sort controls: by status, by date, by flag

**States:**
- **Empty state:** "No inquiries yet. Add your first family." with "New Inquiry" CTA
- **Loading state:** Skeleton cards while fetching from server
- **Offline state:** Cached pipeline visible; "Showing last synced data" banner; write actions (new inquiry, status change) blocked with connectivity prompt

---

### Screen: Schedule Intake Screen

**Purpose:** Create a linked intake appointment for the inquiry — replacing the verbal scheduling that currently happens in WhatsApp
**Primary action:** Confirm appointment
**Entry point(s):** Inquiry Detail View → "Schedule Intake" button

**Key components:**
- Date picker (native Android date picker)
- Start time picker (native Android time picker)
- Duration picker (dropdown: 30 min / 45 min / 60 min / 90 min)
- Staff assignment (optional searchable dropdown — "Who will conduct the intake?")
- Confirm appointment CTA

**States:**
- **Loading state:** "Checking availability..." while conflict detection runs (if staff member selected)
- **Error state — staff conflict:** Inline note: "This staff member has another appointment at this time. Choose a different time or leave staff unassigned."
- **Offline state:** "Saved locally — appointment will sync when you reconnect."

---

## Developer Handoff

### Step-level technical summary

| Step | Data written | Data read | API / event | Offline behavior | Regulatory gate |
|---|---|---|---|---|---|
| 3 | Form draft (local only) | None | None — local draft only | Write draft to device storage | None — no health data written |
| 4 | inquiry_id, child_name, child_age_estimate, diagnosis_notes, guardian_name, guardian_mobile, inquiry_source, center_id, created_by, created_at, status="Inquiry" | Duplicate check: guardian_mobile lookup | POST /inquiries | Queue locally; submit requires connectivity | No DPDPA gate — no health data; basic contact info only |
| 6 | appointment_id, inquiry_id, scheduled_date, scheduled_time, duration, assigned_staff_id, status="Scheduled" | Assigned staff availability (if staff selected) | POST /inquiries/{id}/intake-appointment | Queue locally; sync on restore | None |
| 7 | inquiry.status = "Intake Scheduled", intake_appointment_id | Inquiry record | PATCH /inquiries/{id}/status | N/A (online only) | None |
| 8 | reminder_job_id, inquiry_id, appointment_id, trigger_time (T-24h), channel, template_id, status="Scheduled" | Appointment start time, guardian mobile | Background job: REMIND-001 | Server-side job; client reflects status on next sync | ⚠️ DPDPA — reminder message must not include clinical or diagnosis data; logistics only (child first name, date, time, center name) |

**Key state transitions:**
- inquiry.status transitions: "Inquiry" → "Intake Scheduled" at Step 7 → "Enrolled" (manually by Rahul after Journey 2 completes) → "No Response" (flagged if no confirmation after 48h post-reminder)
- reminder_job.status transitions: "Scheduled" → "Fired" (at T-24h) → "Delivered" / "Failed"

**Background jobs / async events triggered by this journey:**
- REMIND-001 job: triggered at Step 6 (appointment creation); fires at T-24h from appointment start time
- No-Response flag job: triggered at T+48h after reminder fires if no manual status update by Rahul; sets inquiry.flag = "No Response" and surfaces in pipeline view

**DPDPA compliance notes:**
- No DPDPA consent gate applies in this journey — no clinical or health data is stored. The inquiry record contains contact information and basic demographic data only.
- DPDPA consent is triggered in Journey 2 (Intake & Enrollment) at the point of creating the child's EMR record.
- Reminder messages must not contain clinical information (diagnosis, therapy type) — logistics only.

---

## Cross-Journey Dependencies

| Depends on journey | Why | What breaks if missing |
|---|---|---|
| Platform authentication & user accounts (AUTH-001) | Rahul must be logged in as Center Director or Admin role before any inquiry can be created | Journey cannot start; no "New Inquiry" access |
| Journey 2: Intake & Enrollment | Journey 2 begins when Rahul manually updates the inquiry status to "Enrolled" after the intake appointment is complete | Without this journey, the inquiry record has no path to becoming a child EMR; the pipeline view would show all records stuck at "Intake Scheduled" |
| WhatsApp Business API setup (WA-001) and SMS provider (REMIND-001 infra) | Reminder job at Step 8 requires a delivery channel | Reminder job is created but cannot fire; parents receive no appointment reminder; no-show rate at intake appointment may be higher |

---

## ⚠️ Feature Factory Disclaimer

This flow was defined by competitive observation, document synthesis, and category assumption — not by validated user research with Indian autism therapy center directors. Before committing engineering capacity or design effort:

**What we assumed but haven't validated:**
- [ASSUMPTION] Center directors (Rahul) will create a structured inquiry record in the platform when they receive a WhatsApp or phone inquiry, rather than continuing to use WhatsApp and memory as their lead tracking system. The platform must offer enough immediate value at the inquiry stage to offset the friction of switching behavior. (H-04)
- [ASSUMPTION] Inquiry-to-enrollment pipeline visibility is a genuine pain point that Rahul experiences regularly — and not a problem that is already solved through WhatsApp Business labels, a physical notebook, or some other tool. (H-04)
- [ASSUMPTION] Automated SMS / WhatsApp reminders 24 hours before an intake appointment will reduce no-show rates at intake. The 39% vs. 3% no-show finding (Psychiatric Services) is from US clinical data; Indian therapy center appointment behavior with families arriving at intake stage is not confirmed.

**What a researcher would ask before building this:**
- How do center directors currently track warm inquiries? Do they experience losing leads as a real problem, or do most inquiries result in intake appointments promptly? (H-04)
- What is the current no-show rate at intake appointments in Indian therapy centers? Is this a known pain point for directors?
- Would Rahul open a separate app to log an inquiry he just received on WhatsApp, or does the friction make this unlikely without a WhatsApp integration?

**What the Product Consultant would challenge:**
- This journey produces an inquiry record and an appointment reminder — both are lightweight features, but they only create value if Rahul adopts the habit of logging inquiries in the platform. The question is whether the pipeline view has enough value to drive that habit change.
- Consider whether a minimal "log and remind" flow (Steps 3–8 only, no pipeline view at launch) is sufficient to unlock Journey 2 adoption, and whether the pipeline view can be deferred to v1.1 once basic inquiry logging is proven.

**Risk level:**
- Steps 2–8 (inquiry creation + appointment scheduling + reminder): Low–Medium risk — lightweight feature; the risk is adoption, not build complexity
- Step 9 (pipeline view): Low risk — read-only aggregated view; only valuable if Step 4 adoption is strong
