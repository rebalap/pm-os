# Requirements: Journey 3 — Scheduling & Attendance Management

**Product:** Autism Therapy Platform (India)
**Journey:** Journey 3 — Scheduling & Attendance Management
**MVP status:** IN SCOPE — MVP
**Primary actors:** Rahul (Center Director — creates and manages schedules); Priya (Special Educator — marks attendance)
**Supporting actors:** Meena (Parent / Primary Caregiver — receives reminders); Dr. Sunita (Clinical Supervisor — views caseload session delivery)
**Date:** 2026-05-05
**Story ID prefix:** SCHED-
**Source documents:**
- `user-journeys/journey-03-scheduling-attendance-management.md`
- `user-journeys/journey-map.md` — Journey 3 section

---

## Epic: SCHED — Scheduling & Attendance Management

**Goal:** Give Rahul a structured, Android-native weekly scheduling system and give Priya a frictionless attendance marking flow — replacing paper registers, WhatsApp-coordinated schedules, and manual billing tabulations with a single system where sessions are scheduled, attendance is marked in under 2 taps, automated reminders reduce no-shows, and every attendance mark feeds directly into billing and dropout risk detection.

**Copied from:** Jane App (recurring appointment scheduling, automated reminders), SimplePractice (calendar view, attendance status), CentralReach (therapist conflict detection, caseload visibility), Theralytics (attendance-to-billing bridge). No Indian competitor has any of this capability — TherapEZ and PractiPal cover billing admin only. This is a differentiator in the Indian market.

**Target user(s):** Rahul (Center Director); Priya (Special Educator); Meena (Parent — receives reminders only); Dr. Sunita (Clinical Supervisor — read-only caseload view)

**Definition of Done:**
- Rahul can create a recurring weekly session schedule for a child — with therapist and room assignment — that auto-populates 12 weeks forward in under 90 seconds on minimum-spec Android
- Conflict detection runs before save: therapist availability conflicts and room double-bookings are identified before the series is committed
- Priya can mark session attendance (Present / Absent / No-show / Cancelled) in exactly 2 taps from her home screen, confirmed by haptic feedback
- SCHED-004 attendance mark functions offline: writes to local storage immediately; syncs in background; survives app kill and device restart
- Automated pre-session reminders fire at T-24h and T-2h via SMS or WhatsApp; reminder messages contain logistics only — no clinical data
- No-show follow-up message fires within 30 minutes of a No-show mark
- Center calendar loads within 2 seconds for a 7-day view on minimum-spec Android (Redmi/Realme, 2GB RAM, Android 10+)
- Every attendance mark triggers an event to the billing queue (feeds INV-002) and increments the no-show counter (feeds Journey 10 dropout detection)
- All stories pass QA on minimum-spec Android (Redmi/Realme, 2GB RAM, Android 10+)
- DPDPA consent gate confirmed active on child record before any session record is created or attendance data is written

**Out of scope (this epic):**
- Session notes after attendance — Journey 5 (SNOTE-001) and Journey 6
- Invoice generation from attendance — Journey 9 (INV-002 consumes the attendance events emitted here)
- Dropout risk badge and follow-up escalation beyond the first no-show message — Journey 10
- Parent-facing portal or parent login (Meena receives one-way messages only in this journey)
- Two-way WhatsApp reply handling (message is outbound only)
- Multi-center calendar views (single center only)
- Shadow teacher scheduling or school session coordination
- Bulk schedule import from Excel
- Room resource management beyond double-booking conflict detection

**[ASSUMPTION — NOT VALIDATED]** This epic is built on the assumption that Rahul manages scheduling through WhatsApp messages and paper registers and experiences this as a genuine operational pain point. The specific assumption that Priya will mark attendance on an Android phone during or immediately after a live session — rather than on paper and retrospectively — has not been confirmed in primary research with Indian therapy centers. The ≤ 2-tap constraint is designed to minimize cognitive load, but its effectiveness in a real session room with an active child has not been tested. Validate before committing engineering capacity.

---

## Story SCHED-001: Create recurring weekly session schedule for a child

**As a** Rahul (Center Director)
**I want to** create a recurring weekly session schedule for a child — specifying day(s), start time, duration, assigned therapist, and room — and have the system auto-populate the next 12 weeks of sessions with conflict detection
**So that** I never have to manually create individual session records and can see the full forward schedule for every child in the calendar from the moment they are enrolled

**Inspired by:** Jane App recurring appointment scheduling; SimplePractice recurring sessions; CentralReach client schedule management

**Context:** Rahul creates this schedule once at the point a new child begins sessions, or modifies it when a child's schedule changes. He is at his desk or on his Android phone at the center. Connectivity is expected at admin time. The form must surface conflict warnings before committing the series — a saved conflict creates an operations problem Rahul will not discover until the session day.

**Acceptance Criteria:**
- [ ] AC-01: Given Rahul is logged in as Center Director or Admin, when he taps "+ Add Schedule" from a child's profile or the "+" FAB on the center calendar, then the Add Schedule form opens in under 1.5 seconds on minimum-spec Android
- [ ] AC-02: Given the Add Schedule form is open, then the following fields are present: Day(s) of week (multi-select checkboxes Mon–Sun), Start time (time picker), Duration (dropdown: 30 min / 45 min / 60 min / 90 min / Custom), Therapist (single-select from active therapist list), Room (single-select — optional; hidden if center has no rooms configured in Settings)
- [ ] AC-03: Given Rahul completes all required fields (day, time, duration, therapist), then a live preview reads: "This schedule will create [N] sessions over 12 weeks starting [date]." — updating as fields change
- [ ] AC-04: Given Rahul taps "Save", then before committing the system runs conflict detection and checks: (a) whether the therapist's configured availability (SCHED-002) covers each occurrence, and (b) whether the selected room is already booked at any occurrence
- [ ] AC-05: Given a therapist conflict is found, then a red-bordered summary appears listing the specific conflicting dates by name (e.g., "Priya is unavailable on these 3 dates: Mon 12 May, Mon 19 May, Mon 26 May") and the "Save" button is disabled until each conflict is resolved; Rahul can resolve by: skipping those occurrences, choosing a different therapist for the series, or adjusting the time
- [ ] AC-06: Given a room double-booking conflict is found, then the same red-bordered summary lists the conflicting room and dates; resolution options: pick a different room for the series or skip the conflicting occurrences
- [ ] AC-07: Given all conflicts are resolved and Rahul taps "Save", then the system creates session records for all occurrences (status = Scheduled) linked to the child record, therapist ID, and room ID; Rahul is returned to the calendar with the new sessions visible within 3 seconds
- [ ] AC-08: Given the child already has an existing recurring schedule, when Rahul opens "Edit Schedule" from a session card in the series, then a bottom sheet asks: "Edit this session only / Edit all future sessions / Edit all sessions in the series"; selecting "Edit all future sessions" creates a new series from the next occurrence; prior sessions are unmodified
- [ ] AC-09: Given the child's DPDPA consent status is not Active, then the "Save" action is blocked and a banner reads: "Parental consent required before scheduling sessions. Review consent in child record."
- [ ] AC-10: Given Rahul saves while offline, then a banner reads "Schedule saved locally — sessions will be created when you reconnect" and the form queues the POST; conflict detection is suppressed offline with a warning: "Conflict detection requires a connection. Conflicts will be checked on sync."

**Edge Cases & Error States:**
- [ ] EC-01: If POST /schedules/recurring returns 5xx, the form shows "Couldn't create schedule — tap to retry" and no session records are created; the form retains all entered values
- [ ] EC-02: If the selected therapist has no availability configured (SCHED-002 not yet set up), then a warning appears: "Priya's availability is not yet configured. Conflicts cannot be checked. You can continue, but scheduling conflicts may occur." Rahul can proceed or cancel to set up availability first
- [ ] EC-03: If the child has no record in the system, the "Add Schedule" entry point is not accessible; the error cannot be reached from a valid flow
- [ ] EC-04: If "Custom" duration is selected, a numeric input accepts minutes (10–180 min range); values outside this range show inline validation

**Non-Functional Requirements:**
- Performance: Session series of 12 weeks (up to 36 sessions for 3x/week schedules) must be created server-side and calendar refreshed within 3 seconds on 4G
- Offline: Form fillable offline; POST queued locally; conflict detection requires connectivity; survives app close
- Accessibility: All touch targets >= 44px; day checkboxes individually tappable; form operable one-handed
- Privacy: Session records for a minor — DPDPA consent gate at AC-09; records encrypted at rest; access scoped by RBAC to assigned staff + admin

**Dependencies:**
- Blocked by: EMR-001 (child record exists), EMR-002 / INT-003 (DPDPA consent Active), AUTH-001 (Rahul authenticated as Center Director or Admin)
- Enables: SCHED-002 (availability prerequisite for conflict detection), SCHED-003 (reschedule/cancel), SCHED-004 (attendance marking), SCHED-005 (calendar view), SCHED-006 (reminder engine reads session records)

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android
- [ ] Conflict detection tested: therapist conflict, room conflict, no availability configured
- [ ] Edit series flow tested: single session, all future, full series
- [ ] DPDPA consent gate tested: blocked when consent not Active
- [ ] Offline queue behavior tested: save offline, restore connectivity, verify sessions created
- [ ] Code reviewed and merged

---

## Story SCHED-002: Therapist availability configuration

**As a** Rahul (Center Director)
**I want to** configure working days, working hours, and blocked slots for each therapist on my team
**So that** the scheduling system can accurately detect conflicts before sessions are created and I never accidentally double-book a therapist

**Inspired by:** Jane App staff schedule configuration; SimplePractice clinician availability settings; CentralReach staff management

**Context:** Rahul sets this up once per therapist during onboarding or when a therapist's schedule changes. It is a prerequisite for conflict detection in SCHED-001. Single-setup, admin action — not a daily workflow. Connectivity expected when completing this configuration.

**Acceptance Criteria:**
- [ ] AC-01: Given Rahul is logged in as Center Director or Admin and navigates to Settings > Staff > [Therapist name] > Availability, then he sees the availability configuration screen for that therapist
- [ ] AC-02: Given the availability screen is open, then Rahul can configure: Working days (multi-select checkboxes Mon–Sun), Work start time (time picker), Work end time (time picker); these apply as a default weekly pattern
- [ ] AC-03: Given Rahul saves working days and hours, then the system writes the therapist's base availability record; all future conflict detection for this therapist reads from this record
- [ ] AC-04: Given Rahul wants to add a blocked slot (e.g., therapist training day, doctor appointment, public holiday), when he taps "Add blocked slot", then a date/time picker allows him to specify: date, start time, end time, optional label (e.g., "Training"); the blocked slot overrides availability for that specific window
- [ ] AC-05: Given a blocked slot is saved, then any session in SCHED-001 that falls within that slot is flagged as a conflict in the conflict detection run
- [ ] AC-06: Given Rahul navigates to the availability screen for a therapist with no availability configured, then a banner reads: "Availability not configured — scheduling conflicts cannot be detected for this therapist. Set up availability to enable conflict detection."
- [ ] AC-07: Given availability is saved, then the saved configuration is visible immediately in a read-only summary: "Available: Mon–Fri, 9:00am–5:00pm | [N] blocked slots this month"
- [ ] AC-08: Given Rahul edits an existing availability record, then existing scheduled sessions are not affected; the new availability applies only to sessions created after the edit

**Edge Cases & Error States:**
- [ ] EC-01: If end time is set before start time, inline validation fires: "End time must be after start time"; form does not submit
- [ ] EC-02: If a blocked slot overlaps an existing blocked slot for the same therapist, a warning appears: "This overlaps with an existing block on [date]. Proceed?" Rahul can confirm overlap or cancel
- [ ] EC-03: If PATCH /staff/{id}/availability returns 5xx, the screen shows "Couldn't save availability — tap to retry"; existing availability record is unchanged
- [ ] EC-04: If no blocked slots are configured, the blocked slots section shows "No blocked slots — tap + to add one"

**Non-Functional Requirements:**
- Performance: Availability screen loads within 2 seconds on 4G
- Offline: Availability configuration requires connectivity; if offline, show "Connect to configure availability" prompt
- Accessibility: All touch targets >= 44px; time pickers use native Android time picker

**Dependencies:**
- Blocked by: AUTH-001 (Rahul authenticated), Staff onboarding (therapist account must exist)
- Enables: SCHED-001 (conflict detection depends on this), SCHED-005 (calendar can shade unavailable therapist hours)

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android
- [ ] Blocked slot conflict overlap warning tested
- [ ] Availability used by SCHED-001 conflict detection — integration test passes
- [ ] EC-01 (end before start) and EC-02 (overlapping blocks) tested
- [ ] Code reviewed and merged

---

## Story SCHED-003: Session reschedule and cancellation

**As a** Rahul (Center Director)
**I want to** reschedule a session to a new date and time — or cancel it — directly from the calendar, with the option to apply the change to a single session or all future sessions in the series, and have the parent notified automatically on reschedule
**So that** schedule changes are captured in the system before they are communicated informally on WhatsApp and every session has an accurate status for billing and dropout tracking

**Inspired by:** Jane App appointment reschedule flow; SimplePractice session cancellation with reason; CentralReach recurring appointment edit scope

**Context:** Parent requests a rescheduled session, or a therapist calls in sick. Rahul handles this from the center calendar by tapping the session card and selecting reschedule or cancel. Connectivity is expected for schedule changes; conflict detection on the new slot requires server access. Parent notification fires automatically on reschedule — not on cancellation (parent already requested it) unless cancellation is center-initiated.

**Acceptance Criteria:**
- [ ] AC-01: Given Rahul taps a session card in the center calendar (SCHED-005), then a bottom sheet appears with three actions: "Mark Attendance" (visible only to authorized roles), "Reschedule", "Cancel"
- [ ] AC-02: Given Rahul taps "Reschedule", then a Reschedule modal opens showing: current session details (child name, therapist, date/time), a date picker for the new date, a start time picker, and a therapist-filtered available-slots indicator
- [ ] AC-03: Given Rahul selects a new date and time and taps "Confirm Reschedule", then conflict detection runs for the new slot (same logic as SCHED-001 AC-04); if a conflict exists, an inline warning lists the conflict before the confirmation can proceed
- [ ] AC-04: Given no conflict is found and Rahul confirms, then: the original session record is updated (status = Cancelled, cancellation_reason = "Rescheduled", rescheduled_to = new session ID); a new session record is created at the new date/time (status = Scheduled); and a parent notification is queued (channel: configured reminder channel — same as SCHED-006)
- [ ] AC-05: Given a session is part of a recurring series, then the Reschedule modal presents a scope selector: "This session only" (default) / "All future sessions in this series"; selecting "All future sessions" cancels all future occurrences and creates a new series from the next occurrence with the updated schedule
- [ ] AC-06: Given Rahul taps "Cancel" on a session, then a bottom sheet appears with a cancellation reason selector: Centre cancelled / Parent requested / Child unwell / Therapist absent / Other; selecting a reason and tapping "Confirm Cancellation" sets the session status = Cancelled with the selected reason stored
- [ ] AC-07: Given a session is cancelled (not rescheduled), then no parent notification is sent automatically; Rahul may contact the parent manually via their preferred channel
- [ ] AC-08: Given "All future sessions" is selected for cancellation, then a confirmation dialog reads: "This will cancel [N] future sessions for [child name] from [date]. This cannot be undone. Confirm?" and requires an explicit confirm tap
- [ ] AC-09: Given a reschedule is saved, then the center calendar immediately reflects: the old slot shows as Cancelled, the new slot shows as Scheduled; the calendar refresh happens within 2 seconds

**Edge Cases & Error States:**
- [ ] EC-01: If POST /sessions/{id}/reschedule returns 5xx, the modal shows "Couldn't reschedule — tap to retry"; no session records are modified; original session remains in Scheduled status
- [ ] EC-02: If the new slot has a therapist conflict, the "Confirm Reschedule" button is disabled and the conflict is listed inline; Rahul must pick a different slot to proceed
- [ ] EC-03: If a session is already marked with an attendance status (Present / Absent / No-show), the "Reschedule" option is hidden; only "Cancel" remains, with a note: "This session has been marked as [status] and cannot be rescheduled."
- [ ] EC-04: If Rahul is offline when attempting a reschedule or cancellation, a banner reads: "Schedule changes require a connection. Connect and try again." No local queue for schedule structural changes (risk of sync conflicts is too high).

**Non-Functional Requirements:**
- Performance: Reschedule confirmation and calendar refresh within 2 seconds on 4G
- Offline: Reschedule and cancellation blocked offline (see EC-04); read-only calendar view still available
- Accessibility: All touch targets >= 44px; bottom sheet actions are full-width tappable rows

**Dependencies:**
- Blocked by: SCHED-001 (session records exist), SCHED-002 (therapist availability for conflict detection on new slot), SCHED-006 (reminder infrastructure for parent notification on reschedule)
- Enables: SCHED-006 EC-04 (reminder suppressed if session rescheduled before reminder fires)

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android
- [ ] Reschedule single session tested; original session Cancelled, new session Scheduled, parent notification queued
- [ ] Reschedule all future sessions tested; N sessions cancelled, new series created
- [ ] Cancel with reason tested; no parent notification sent
- [ ] Cancel all future sessions — confirmation dialog and bulk cancellation tested
- [ ] EC-03 (already-marked session cannot be rescheduled) tested
- [ ] EC-04 (offline blocked) tested
- [ ] Code reviewed and merged

---

## Story SCHED-004: Mark session attendance — Present / Absent / No-show / Cancelled

**As a** Priya (Special Educator)
**I want to** mark a child's session attendance as Present, Absent, No-show, or Cancelled in exactly 2 taps from my home screen — with haptic feedback confirming the mark — even when I have no internet connection in the session room
**So that** attendance is recorded accurately at the moment it happens, feeding into billing and flagging children at risk of dropping out, without interrupting my session or requiring me to remember to log it later

**Inspired by:** CentralReach attendance marking; Motivity session confirmation; Catalyst in-session status; Hi Rasmus check-in flow

**Context:** This is the highest-frequency data entry action in the platform. Priya marks attendance for every session she delivers — typically 4–8 per day. She is often in a small session room with an active child. She may be using her phone one-handed in a noisy environment. Connectivity cannot be guaranteed. The ≤ 2-tap requirement is a physical constraint — not a UX preference — driven by the in-session context. This constraint overrides any competing requirement.

**Tap path definition (required for QA):**
- Tap 1: Tap session card on Priya's Home Screen (My Sessions view)
- Tap 2: Tap an attendance chip (Present / Absent / No-show / Cancelled) on the Mark Attendance Screen
- Result: Attendance saved, haptic feedback fired, confirmation visible — without any third tap

**Acceptance Criteria:**
- [ ] AC-01: Given Priya is logged in and on her Home Screen (My Sessions view), when she taps a session card for any session assigned to her today, then the Mark Attendance Screen opens in under 1 second on minimum-spec Android; this is Tap 1
- [ ] AC-02: Given the Mark Attendance Screen is open, then four attendance chips are the dominant UI element — occupying the majority of the visible screen with no scrolling required: Present (green), Absent (amber), No-show (orange), Cancelled (grey); each chip has a text label alongside its color; each chip has a minimum touch target height of 88px
- [ ] AC-03: Given Priya taps any attendance chip, then: the attendance status is written to local storage immediately (offline-first — network state is irrelevant); a haptic pulse fires within 100ms of the tap; a "Saved" confirmation banner appears for 1.5 seconds; this is Tap 2 — the attendance mark is complete
- [ ] AC-04: Given the attendance status is written locally, then the system syncs to the server in the background when connectivity is available; the sync is idempotent and survives: app close, device restart, and extended offline periods of up to 72 hours
- [ ] AC-05: Given the device is online when the local write syncs, then: (a) an `attendance.confirmed` event is emitted to the billing queue (INV-002 dependency); (b) the no-show counter for the child is incremented if status = No-show (Journey 10 dependency); (c) Dr. Sunita's caseload dashboard (MPM-003) "Last session" field is updated
- [ ] AC-06: Given the attendance status is No-show, then after the local write and sync, the `no-show-follow-up-job` is triggered (see SCHED-007); this job fires server-side and does not depend on Priya taking any further action
- [ ] AC-07: Given the device is offline when Priya marks attendance, then: (a) the local write happens immediately with no user-visible delay; (b) haptic fires; (c) a persistent banner reads "Offline — attendance saved locally, will sync when connected"; (d) the session card on the home screen immediately reflects the marked status from local storage
- [ ] AC-08: Given a session is already marked, when Priya opens the Mark Attendance Screen for that session, then the current status is shown as the selected state; a "Change attendance" link is present; tapping it re-enables the chips for correction
- [ ] AC-09: Given sessions past their start time are still in "Scheduled" status at end of day, then an orange banner on Priya's Home Screen reads "[N] sessions need attendance marked" — tapping the banner filters the My Sessions list to unmarked sessions only
- [ ] AC-10: Given Priya marks a session as "Present" and the "Saved" banner clears, then a non-blocking prompt appears at the bottom of the screen: "Session marked. Add a session note?" with "Add Note" and "Skip" buttons; tapping "Skip" dismisses the prompt without any action; tapping "Add Note" navigates to the session note creation screen (SNOTE-001 — separate story)
- [ ] AC-11: Given Priya taps "Cancelled" as the attendance chip, then a cancellation reason bottom sheet appears immediately after the chip tap with options: Centre cancelled / Parent requested / Child unwell / Therapist absent / Other; selecting a reason completes the mark; this must still satisfy the ≤ 2-tap requirement — the reason sheet is triggered by the chip tap (Tap 2), not by a separate confirm action; selecting a reason is a single tap on the sheet (completing the flow in 3 taps total — exception documented)

**Edge Cases & Error States:**
- [ ] EC-01: If the local write fails (device storage full), the chip tap shows "Could not save — storage may be full. Free up space and try again." — the attendance is NOT marked; haptic does not fire
- [ ] EC-02: If a sync conflict occurs (same session marked by a different user — e.g., Rahul from admin — while Priya was offline), then the conflict is resolved server-side using last-write-wins with timestamp; the conflicting mark is logged to an audit trail; Priya is not notified at the time of sync
- [ ] EC-03: If Priya attempts to mark a session that has been cancelled by Rahul (session status = Cancelled from SCHED-003), then the Mark Attendance Screen shows a read-only state: "This session was cancelled by [admin name] on [date]. Attendance cannot be marked."
- [ ] EC-04: If the `attendance.confirmed` billing event fails to queue after sync, the event is retried with exponential backoff (3 attempts); if all retries fail, the failure is logged to the server error log and surfaced in Rahul's admin panel as "Billing sync failed for [child name] on [date]"

**Non-Functional Requirements:**
- Performance: Mark Attendance Screen opens in under 1 second from session card tap; local write completes in under 200ms; haptic fires within 100ms of tap
- Offline: Local-first write is the primary behavior, not a fallback; the flow must be fully testable without a server connection; offline mark must survive: (a) app close and reopen, (b) device restart, (c) 72 hours without connectivity
- Accessibility: All 4 attendance chips minimum 88px height (extra large — ensures one-handed accuracy with active child); text label required alongside color on every chip; haptic mandatory (never audio-only confirmation)
- Privacy: Attendance record is health-adjacent data for a minor; encrypted at rest; access scoped by RBAC to assigned therapist + center admin + supervisor; audit log written on every write and sync

**Dependencies:**
- Blocked by: SCHED-001 (session records exist), MPM-002 (Priya's My Sessions home screen — Priya sees only assigned children), AUTH-001 (Priya authenticated)
- Enables: INV-002 / Journey 9 (attendance.confirmed event feeds billing), Journey 10 (no-show counter increment), SNOTE-001 / Journey 5 (session note prompt after Present mark), SCHED-007 (no-show follow-up triggered by No-show status)

**Definition of Done:**
- [ ] All AC pass in QA on physical minimum-spec Android device (Redmi or Realme, 2GB RAM, Android 10+) — NOT emulator only
- [ ] QA tap count verified on physical device: home screen to confirmed mark = exactly 2 taps (or 3 for Cancelled with reason — documented exception)
- [ ] Offline survival tested: mark offline, kill app, restart device, restore connectivity, verify sync completes and billing event fires
- [ ] Haptic feedback confirmed on physical device (not emulator)
- [ ] EC-01 (storage full) and EC-02 (sync conflict) tested
- [ ] EC-03 (cancelled session) tested
- [ ] Billing event (AC-05a) integration tested: attendance.confirmed event received by billing queue after sync
- [ ] No-show counter increment (AC-05b) integration tested
- [ ] Code reviewed and merged

---

## Story SCHED-005: Center calendar view — day and week grid

**As a** Rahul (Center Director)
**I want to** see a color-coded day and week calendar grid showing all sessions across all therapists, children, and rooms — with filters for therapist, child, and room — loading within 2 seconds for a 7-day view
**So that** I have real-time operational visibility of the entire center's schedule and can immediately see which sessions have been marked, which are outstanding, and where there are gaps or conflicts

**Inspired by:** Jane App calendar grid view; SimplePractice schedule page; CentralReach center dashboard calendar

**Context:** Rahul's primary daily operational screen. He opens it every morning to review the day and periodically throughout the day to check attendance status. He needs to see at a glance: what is scheduled, who is delivering it, and whether attendance has been marked. The calendar must load fast even on a mid-range Android device.

**Acceptance Criteria:**
- [ ] AC-01: Given Rahul opens the Schedule tab, then the Center Calendar loads in Day view defaulting to today's date; all sessions for today are visible within 2 seconds on minimum-spec Android on a 4G connection
- [ ] AC-02: Given the Day view is active, then sessions are displayed as colored blocks in a time grid: vertical axis = time of day (7:00am–8:00pm, scrollable); horizontal axis = therapist columns (or room columns — configurable in Settings); each session block shows: child first name, time, room name, and status indicator
- [ ] AC-03: Given the status of any session, then it is rendered using both color and a text label (never color alone): Scheduled = white/outlined, Present = green, Absent = amber, No-show = orange, Cancelled = grey; a persistent legend is shown at the top of the calendar
- [ ] AC-04: Given Rahul taps the "Week" toggle, then the view switches to a 7-day week grid; all sessions for the current week load within 2 seconds on 4G; session blocks in week view are compressed but must remain readable (child first name + time visible without tapping)
- [ ] AC-05: Given a filter chip row is present below the legend, then Rahul can filter by: All (default) / individual therapist name / individual room; tapping a filter chip immediately re-renders the grid to show only matching sessions; filter chips are horizontally scrollable; each chip >= 44px touch target
- [ ] AC-06: Given Rahul taps any session block in the grid, then a bottom sheet opens with: session context (child name, therapist, room, time, current status) and action buttons appropriate to the session state (Mark Attendance if unfinished, Reschedule, Cancel, View Detail)
- [ ] AC-07: Given the calendar is offline, then the cached schedule for up to 7 days is shown with a banner: "Offline — showing schedule last synced [date/time]"; new session creation and rescheduling are blocked offline; attendance marking from the calendar bottom sheet routes to SCHED-004 and works offline
- [ ] AC-08: Given more than 10 therapists are configured at the center, then the calendar switches to a list-per-therapist accordion layout rather than expanding horizontally beyond screen width
- [ ] AC-09: Given sessions exist with an unmarked attendance status (still "Scheduled") after their scheduled end time, then their blocks in the grid are bordered in orange to signal outstanding marks; a badge count in the calendar header reads "[N] sessions need attendance marked"
- [ ] AC-10: Given Rahul navigates to a day with no sessions scheduled, then the grid shows an empty state: "No sessions scheduled for [date]." with an "+ Add Session" button

**Edge Cases & Error States:**
- [ ] EC-01: If GET /schedule/week?date=[date] fails, then the calendar shows the most recently cached data with a banner: "Could not refresh schedule. Showing cached data. Pull to refresh."
- [ ] EC-02: If a session block text would overflow its grid cell (very long child name), then text is truncated with an ellipsis; full name is visible in the bottom sheet on tap
- [ ] EC-03: If two sessions are scheduled in the same room at the same time (a booking conflict that slipped through), their blocks are rendered with a red "Conflict" badge; Rahul can tap to investigate and resolve

**Non-Functional Requirements:**
- Performance: Day view loads within 2 seconds on 4G on minimum-spec Android; week view loads within 2 seconds on 4G; calendar uses local cache for offline view; cache covers up to 7 days forward
- Offline: Read-only cached view for up to 7 days; attendance marking from bottom sheet works offline (routes to SCHED-004 offline flow); write actions (create, reschedule) blocked offline
- Accessibility: Status indicators always text + color; session blocks minimum 44px height; filter chips minimum 44px touch target; status legend always visible
- Privacy: RBAC enforced — Rahul (Center Director / Admin) sees all children and therapists; Priya (Special Educator) is not expected to access this view; calendar data includes child names and session times (health-adjacent); access logged

**Dependencies:**
- Blocked by: SCHED-001 (session records to display), SCHED-002 (therapist availability to shade unavailable hours optionally), AUTH-001
- Enables: SCHED-003 (reschedule/cancel initiated from this view), SCHED-004 (attendance mark accessible from bottom sheet)

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android
- [ ] 2-second load time verified on physical device on 4G for both day and week views with a realistic dataset (50 sessions in a week)
- [ ] Filter by therapist and by room tested
- [ ] Offline cached view tested: cache 7 days, disable network, verify calendar readable
- [ ] EC-03 (room conflict badge) tested
- [ ] More than 10 therapists layout tested (accordion)
- [ ] Code reviewed and merged

---

## Story SCHED-006: Automated pre-session reminders — T-24h and T-2h

**As a** Rahul (Center Director)
**I want to** have the system automatically send Meena (the parent) a reminder message 24 hours and again 2 hours before each scheduled session — via WhatsApp or SMS — using a DLT-registered sender ID, containing only logistics and no clinical data
**So that** no-show rates fall without requiring my staff to manually send a WhatsApp message before every session, and I have a delivery log showing which reminders were sent and which failed

**Inspired by:** Jane App automated appointment reminders; SimplePractice reminder engine; Theralytics pre-session notification; evidence: Psychiatric Services — 39% no-show without reminder vs. 3% with live contact

**Context:** Server-side background job. No user interaction required from Priya, Rahul, or Meena to trigger. Rahul's involvement is limited to: one-time per-child reminder opt-in (set at enrollment or in child record settings), and reviewing the delivery log when a reminder fails. All reminder messages must comply with TRAI DLT rules for transactional SMS in India and must contain logistics only — no clinical data of any kind.

**Acceptance Criteria:**
- [ ] AC-01: Given a session record exists with status = Scheduled, when the session start time is 24 hours away (within a 15-minute check window), then a pre-session reminder job fires: it reads the session record, child record, parent contact details, and the per-child reminder enable flag
- [ ] AC-02: Given the reminder job fires and the per-child reminder flag is enabled, then a message is dispatched containing exactly: child's first name, session date (DD/MM/YYYY format), session start time (12h format with AM/PM), center name, and center address; no diagnosis, therapy type, clinical goal, therapist name, or any other clinical or personal health data is included in the message body
- [ ] AC-03: Given the reminder job fires, then the delivery channel is: WhatsApp Business API (approved template) if configured for the center; SMS via DLT-registered sender ID otherwise; both channels are never used simultaneously for the same message
- [ ] AC-04: Given the 24h reminder has fired, then a second reminder job fires at T-2h using a separate approved template (shorter message format: "Reminder: [child first name]'s session at [center name] is in 2 hours — [time], [date].")
- [ ] AC-05: Given any reminder is dispatched, then a delivery log entry is written: session ID, reminder type (24h / 2h), channel used, timestamp, and delivery status (Delivered / Failed / Suppressed); Rahul can view this log in Settings > Reminders > Delivery Log
- [ ] AC-06: Given a reminder delivery fails (invalid number, carrier rejection, WhatsApp opt-out), then: the delivery log entry is set to Failed; a "Reminder failed" indicator appears on the session card in the center calendar (SCHED-005) for Rahul to action manually; no retry is automatic (Rahul chooses to retry or contact parent directly)
- [ ] AC-07: Given WhatsApp delivery fails and an SMS number is also on file for the parent, then the system automatically retries via SMS and logs the fallback attempt separately; the delivery log entry records both the WhatsApp failure and the SMS fallback result
- [ ] AC-08: Given a session is cancelled (SCHED-003) before the 24h reminder fires, then the reminder job checks session status before dispatching; if status = Cancelled, the reminder is suppressed and the delivery log entry is set to "Suppressed — session cancelled"
- [ ] AC-09: Given a session is rescheduled (SCHED-003) after a 24h reminder has already been sent, then the system sends a schedule change notification: "[Child first name]'s session at [center name] on [original date] has been rescheduled to [new date], [new time]." — using the same channel the original reminder was sent on
- [ ] AC-10: Given the per-child reminder flag is disabled (Rahul or admin turned it off for this child), then no reminders fire for any sessions for that child; the delivery log shows "Suppressed — reminders disabled for this child"

**Edge Cases & Error States:**
- [ ] EC-01: If neither WhatsApp Business API nor DLT-registered SMS is configured for the center, reminder jobs are created but immediately flagged "Undeliverable — no channel configured"; a persistent center-level warning banner in Rahul's admin settings reads: "Reminders are not configured. Set up SMS or WhatsApp Business to enable automated reminders."
- [ ] EC-02: If the session was created less than 25 hours before its start time, the 24h reminder fires immediately at job creation time; the 2h reminder still fires at T-2h as normal
- [ ] EC-03: If the parent contact has no mobile number on record, the reminder job is flagged "Undeliverable — no mobile number on file" and logged
- [ ] EC-04: If the reminder job executor runs twice for the same session and trigger time (infrastructure retry), the job is idempotent — exactly one message is dispatched; duplicate detection uses session ID + reminder type + trigger time as the dedup key

**Non-Functional Requirements:**
- Reliability: Reminder job must be idempotent (AC-04, EC-04); duplicate sends are unacceptable and must be covered by dedup logic
- Privacy: Reminder message body must never contain diagnosis, therapy type, clinical goals, session note content, or any information beyond logistics; this is a DPDPA compliance requirement — parent contact data is processed by an external messaging provider; TRAI DLT sender ID registration required before production launch
- Compliance: SMS sender IDs must be DLT-registered with TRAI under the Transactional category before any SMS is sent in production; WhatsApp Business API templates must be approved by Meta before use; both registrations are infrastructure prerequisites (INFRA-001, INFRA-002)

**Dependencies:**
- Blocked by: SCHED-001 (session records with status = Scheduled), EMR-001 (parent contact on child record), INT-003 (DPDPA consent Active — processing parent contact data), INFRA-001 (DLT-registered SMS provider), INFRA-002 (WhatsApp Business API — optional, falls back to SMS)
- Enables: SCHED-007 (no-show follow-up uses the same messaging infrastructure), SCHED-003 AC-09 (reschedule notification reuses this infrastructure)

**Definition of Done:**
- [ ] All AC pass in QA end-to-end (staging environment with test DLT sender ID or WhatsApp sandbox)
- [ ] 24h and 2h reminder dispatch confirmed in staging
- [ ] WhatsApp fallback to SMS tested
- [ ] Cancellation suppression tested (session cancelled before 24h, before 2h)
- [ ] Reschedule notification tested (rescheduled after 24h reminder sent)
- [ ] Idempotency tested: job run twice — only one message dispatched
- [ ] EC-01 (no channel configured warning) tested
- [ ] DLT-registered sender ID and WhatsApp template approved before production deploy
- [ ] Code reviewed and merged

---

## Story SCHED-007: No-show follow-up message — automated within 30 minutes of No-show mark

**As a** Rahul (Center Director)
**I want to** have the system automatically send Meena a follow-up message within 30 minutes of Priya marking a session as No-show — using a pre-approved template that contains no clinical data — and have a delivery log I can review
**So that** families who miss a session without notice receive a prompt, professional response from the center without requiring my staff to manually identify and follow up on every no-show

**Inspired by:** Theralytics no-show workflow; CentralReach missed appointment follow-up; SimplePractice cancellation notification

**Context:** Server-side event-driven job, triggered by the `session.status.updated` event emitted when Priya marks a session as No-show (SCHED-004 AC-06). The 30-minute delay gives the family time to arrive late before the follow-up fires. The job is cancellable if the session status changes back to Present within the delay window (late arrival). The message is informational and warm in tone — not punitive — and contains no clinical content.

**Acceptance Criteria:**
- [ ] AC-01: Given Priya marks a session as No-show (SCHED-004), then the system emits a `session.status.updated` event with status = No-show; the `no-show-follow-up-job` is queued with a 30-minute delay
- [ ] AC-02: Given the job fires after the 30-minute delay, then a message is dispatched to the parent's configured channel (same channel as pre-session reminders — SCHED-006) containing: child first name, center name, today's date, and center phone number; message text: "[Child first name] missed their session at [center name] today ([date]). We hope everything is okay. Please contact us to reschedule: [center phone number]." — no diagnosis, therapy content, absence reason, or health data included
- [ ] AC-03: Given the job is queued and the session status changes from No-show to Present within the 30-minute window (late arrival — Priya corrects the mark), then the job is cancelled and no follow-up message is sent
- [ ] AC-04: Given the follow-up message is dispatched, then a delivery log entry is written: session ID, job type = "no-show-follow-up", channel, timestamp, delivery status (Delivered / Failed); the delivery log is accessible to Rahul in Settings > Reminders > Delivery Log alongside SCHED-006 entries
- [ ] AC-05: Given the follow-up message fails to deliver (invalid number, carrier failure), then the delivery log entry is set to Failed; a "Follow-up failed" indicator appears on the session card in the center calendar for Rahul to follow up manually
- [ ] AC-06: Given a child has had 3 or more No-show marks in a rolling 30-day period, then the no-show counter increment (from SCHED-004 AC-05b) triggers a dropout risk badge visible in Rahul's calendar view and in Dr. Sunita's caseload dashboard; the automated follow-up message for the third no-show is the same as for prior no-shows — escalated intervention is Journey 10 scope, not this story
- [ ] AC-07: Given Rahul has customized the no-show follow-up message template in Settings > Reminders > Templates, then the customized template is used; customization is limited to: message body text; the system enforces that child first name, center name, date, and center phone number fields are always present in the template (not removable)

**Edge Cases & Error States:**
- [ ] EC-01: If the follow-up job fires but the session status has been changed to a non-No-show status (Present, Absent, Cancelled) in the 30-minute window, then the job checks session status at fire time and suppresses the message; logs "Suppressed — status changed before fire"
- [ ] EC-02: If the parent has no mobile number on record, the job is flagged "Undeliverable — no mobile number on file" and logged; Rahul sees the flag in the delivery log
- [ ] EC-03: If the no-show follow-up job runs twice for the same session (infrastructure retry), the job is idempotent — exactly one message is dispatched; dedup key: session ID + job type
- [ ] EC-04: If the messaging infrastructure (DLT SMS or WhatsApp Business API) is not configured, the job is flagged "Undeliverable — no channel configured" and logged; same infrastructure gate as SCHED-006

**Non-Functional Requirements:**
- Timing: 30-minute delay from No-show mark to message dispatch; the delay must be accurate to within 2 minutes
- Reliability: Job is idempotent (EC-03); no duplicate messages under any retry scenario
- Privacy: Message body contains logistics only — child first name (not full name), center name, date, and center phone number; no clinical data, no absence reason, no health information; DPDPA compliance same as SCHED-006
- Compliance: Same DLT and WhatsApp Business API prerequisites as SCHED-006 (INFRA-001, INFRA-002)

**Dependencies:**
- Blocked by: SCHED-004 (No-show mark emits the trigger event), SCHED-006 (messaging infrastructure and delivery log shared), INFRA-001, INFRA-002
- Enables: Journey 10 (no-show counter used for dropout risk signal; Journey 10 handles escalation beyond the first follow-up message)

**Definition of Done:**
- [ ] All AC pass in QA in staging environment
- [ ] 30-minute delay tested: No-show mark at T=0, message dispatched at T=30min (+/- 2 min)
- [ ] Cancellation within window tested: status changed to Present at T+15min, job cancelled, no message sent
- [ ] EC-01 (status changed before fire) tested
- [ ] Idempotency tested: job run twice, one message dispatched
- [ ] Custom template tested: fields enforced (child name, center name, date, phone cannot be removed)
- [ ] Code reviewed and merged

---

## Backlog Summary

| Story ID | Title | Persona | Complexity | Priority | Blocked by |
|---|---|---|---|---|---|
| SCHED-001 | Create recurring weekly session schedule | Rahul | L | P0 | EMR-001, EMR-002, AUTH-001 |
| SCHED-002 | Therapist availability configuration | Rahul | M | P0 | AUTH-001 |
| SCHED-003 | Session reschedule and cancellation | Rahul | M | P0 | SCHED-001, SCHED-002, SCHED-006 |
| SCHED-004 | Mark session attendance — Present / Absent / No-show / Cancelled | Priya | L | P0 | SCHED-001, MPM-002, AUTH-001 |
| SCHED-005 | Center calendar view — day and week grid | Rahul | L | P0 | SCHED-001, AUTH-001 |
| SCHED-006 | Automated pre-session reminders — T-24h and T-2h | System / Rahul | L | P1 | SCHED-001, EMR-001, INT-003, INFRA-001 |
| SCHED-007 | No-show follow-up message — automated within 30 minutes | System / Rahul | M | P1 | SCHED-004, SCHED-006, INFRA-001 |

**Sprint recommendation:** SCHED-002 and SCHED-001 are the foundation — build in this order (availability first so conflict detection is available at schedule creation). SCHED-004 and SCHED-005 can be built in parallel once SCHED-001 merges. SCHED-003 depends on both SCHED-001 and SCHED-005 being reviewable in the calendar. SCHED-006 and SCHED-007 have hard infrastructure dependencies (INFRA-001: DLT registration, 1–4 weeks; INFRA-002: WhatsApp Business API, 2–6 weeks) — start INFRA-001 and INFRA-002 immediately in parallel with SCHED-001 through SCHED-005 development.

SCHED-004 is the single most critical story in this epic. Its QA must be completed on a physical device, not an emulator. The 2-tap constraint and offline-survival test are non-negotiable before sprint sign-off.

---

## Pre-Build Decisions Required

| # | Decision | Owner | Needed by |
|---|---|---|---|
| PBD-01 | SMS provider and DLT registration (Exotel, MSG91, or Kaleyra) — takes 1–4 weeks | Rahul / Infra | Before SCHED-006 sprint |
| PBD-02 | WhatsApp Business API at launch or SMS-only: WABA setup requires Meta Business verification and a dedicated business number — 2–6 weeks; decision affects SCHED-006 and SCHED-007 scope | Product | Before SCHED-006 sprint |
| PBD-03 | Cancellation reason list: confirm the 5 reasons in SCHED-003 and SCHED-004 cover all real center scenarios; adding reasons post-launch requires data migration | Product | Before SCHED-003 sprint |
| PBD-04 | Room configuration: is room assignment required or optional at schedule creation? Single-room centers should not be forced to set up rooms. Confirm "optional if no rooms configured" is the right default | Product | Before SCHED-001 sprint |
| PBD-05 | Conflict detection behavior when therapist has no availability configured (SCHED-002 not set up): warn-and-proceed vs. block? Current spec is warn-and-proceed (EC-02 of SCHED-001) — confirm | Product / Engineering | Before SCHED-001 sprint |
| PBD-06 | No-show follow-up message template: requires legal review and DLT registration before production; draft message in SCHED-007 AC-02 is a working proposal — confirm wording before DLT filing | Legal / Product | Before INFRA-001 starts |
| PBD-07 | Offline sync conflict resolution strategy for SCHED-004: last-write-wins with timestamp is specified in EC-02; confirm this is acceptable for audit trail purposes | Engineering / Product | Before SCHED-004 sprint |
| PBD-08 | Billing queue event format: confirm the `attendance.confirmed` event schema (session ID, child ID, therapist ID, date, status) is compatible with INV-002 consumer before SCHED-004 ships | Engineering (billing team) | Before SCHED-004 sprint |

---

## Feature Factory Disclaimer

These stories were defined by competitive observation (Jane App, SimplePractice, CentralReach, Theralytics), journey document synthesis, and category assumptions — not by validated primary research with Indian autism therapy center staff.

**What we assumed but haven't validated:**
- [ASSUMPTION] Rahul currently manages scheduling through WhatsApp messages and paper registers and experiences this as a genuine operational pain point; whether scheduling complexity is a felt pain point or a workable WhatsApp system has not been confirmed in primary research with Indian center directors
- [ASSUMPTION] Priya will mark attendance on her Android phone during or immediately after a live session with an active child; the cognitive load of switching to a phone while managing a child's session may make even a 2-tap action feel disruptive in a real session room; the in-session usability of this flow has not been tested with actual therapists in actual Indian therapy centers
- [ASSUMPTION] Automated SMS or WhatsApp reminders will reduce no-show rates at Indian autism therapy centers; the 39% to 3% no-show reduction data is from a US psychiatric outpatient context (Psychiatric Services) and Indian autism therapy families may miss sessions for different reasons (transport costs, financial pressure, caregiver exhaustion) where a logistics reminder has no effect
- [ASSUMPTION] Indian therapy centers have rooms that require conflict management; many small centers (3–5 rooms, 5–10 staff) may find the room conflict detection feature irrelevant and the setup overhead annoying
- [ASSUMPTION] WhatsApp Business API reminders will be welcomed by parents as official center communications; the WABA setup burden for Rahul (Meta Business verification, dedicated business number) is non-trivial and the parent reception of automated WABA messages is unconfirmed in this context

**What a researcher would ask before building this:**
- Does Priya currently record attendance at all during sessions — on paper, on her phone, or not at all? What would interrupt her session workflow the least and what is her mental model of "confirming a session happened"?
- Why do families miss sessions in Indian autism therapy centers? Is it forgetfulness (addressable with a reminder), transport cost, financial pressure, or child behavior on that day? The intervention must match the actual cause to work.
- How does Rahul currently handle scheduling conflicts and same-slot requests? Is double-booking a recurring operational crisis or something handled with a quick WhatsApp message? Is the pain acute enough to justify the setup overhead?

**What the Product Consultant would challenge:**
- SCHED-001 through SCHED-005 together constitute a significant engineering investment that partially overlaps with tools the Indian market already patches together with WhatsApp and Excel. If the product's core differentiation is clinical (in-session data collection, supervision, reporting), scheduling should be scoped to the minimum viable version at launch — recurring schedule creation, attendance mark, no-show trigger — and room management, multi-filter calendars, and availability enforcement deferred until adoption is proven.
- The ≤ 2-tap attendance mark constraint (SCHED-004) is the single most important UX requirement in this entire journey. Everything else in this epic can be iterated post-launch. Validate the tap count and in-session usability on 3–5 therapists before committing to the full scheduling module.

**Risk level per story:**
- SCHED-001 (Recurring schedule creation): Low-Medium — table stakes; structural need clear; over-engineering risk for single-room centers
- SCHED-002 (Therapist availability): Medium — likely over-engineered for small centers at v1; consider making it optional with a warn-and-proceed default
- SCHED-003 (Reschedule / cancel): Low — well-defined state machine; moderate complexity
- SCHED-004 (Attendance mark): Low-Medium — core workflow; key constraint is in-session UX, not feature design; QA on physical device is non-negotiable
- SCHED-005 (Center calendar): Medium — performance requirement on low-end device is real; dense calendar rendering on 2GB Android requires careful implementation
- SCHED-006 (Pre-session reminders): Low-Medium — differentiator in India; no-show reduction effect on Indian autism families is assumed not confirmed; infrastructure dependency on DLT registration is a hard external blocker
- SCHED-007 (No-show follow-up): Low — well-defined; depends on SCHED-006 infrastructure being in place

Use the `/researcher` agent to validate attendance marking behavior, in-session phone use, and no-show root causes before sprint planning.
Use the `/product-consultant` agent to challenge the scheduling feature scope and define the true MVP cut before committing engineering capacity.
Use the `/design-critique` agent to review the Mark Attendance Screen and Center Calendar before prototyping — both have critical usability constraints on low-end Android.
