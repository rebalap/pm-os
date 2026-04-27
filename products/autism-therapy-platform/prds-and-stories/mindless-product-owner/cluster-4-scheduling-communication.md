# Cluster 4: Appointment Scheduling & Communication
**Product:** Autism Therapy Platform (India)
**Agent:** Mindless Product Owner
**Date:** 2026-04-16
**Cluster scope:** Appointment scheduling · SMS/email reminders · WhatsApp integration
**Out of scope (this cluster):** In-session trial-by-trial data collection (handled in separate cluster)
**Journey stages served:** Stage 1 (Inquiry), Stage 2 (Intake), Stage 4/5 (Ongoing sessions), Stage 7 (Billing), Stage 8 (Dropout Prevention)

---

## Competitor Research Notes

> Web search (Tavily/Bash) was not executable in this session. The Feature Inspiration Table
> below draws on: (1) the competitive analysis at
> `research/secondary/competitive-analysis-autism-therapy-software.md` (April 2026,
> 9 Tavily queries); (2) established public feature documentation for Jane App,
> SimplePractice, TherapEZ, PractiPal, and WhatsApp Business API; and (3) category-norm
> inference for scheduling SaaS in the healthcare/therapy vertical.
> Evidence labels applied consistently: ✅ confirmed | 🔵 inferred | 🔶 speculated.

---

## Feature Inspiration: Appointment Scheduling & Communication

| Feature | Competitor(s) | Prevalence | How it works | Evidence |
|---|---|---|---|---|
| Weekly recurring session scheduling per child | Jane App, SimplePractice, CentralReach, TherapEZ | Table stakes | A child's weekly schedule is set once (e.g., Mon/Wed/Fri 10 AM) and auto-populates forward. Staff can override individual occurrences without breaking the series. | ✅ Jane App, SimplePractice product docs confirmed |
| Therapist availability calendar | Jane App, SimplePractice, TherapEZ | Table stakes | Each therapist sets their working hours and blocked slots. Scheduling respects availability and warns on conflicts. | ✅ Jane App; 🔵 TherapEZ inferred from scheduling feature marketing |
| Session room / slot management | Jane App, CentralReach | Table stakes (in multi-room centers) | Rooms are named resources (Room 1, Sensory Room). Appointments are assigned to a room; double-booking is blocked. | 🔵 Inferred from Jane App multi-location feature set |
| Rescheduling and cancellation flows | Jane App, SimplePractice, PractiPal, TherapEZ | Table stakes | From the appointment, staff can reschedule to another slot or cancel. Cancellation reason is optionally recorded. Notification sent to parent. | ✅ SimplePractice; 🔵 PractiPal inferred |
| Attendance marking (present / absent / cancelled) | CentralReach, SimplePractice, TherapEZ, PractiPal | Table stakes | Each appointment has a status: Confirmed → Present / Absent / No-show / Cancelled. Status drives billing and dropout-risk tracking. | ✅ CentralReach; 🔵 TherapEZ inferred |
| Center director all-schedules view | CentralReach, Jane App, TherapEZ | Table stakes | A master calendar shows all children, all therapists, all rooms in a day/week grid. Director can filter by therapist, room, or child. | 🔵 Inferred from Jane App multi-provider view; ✅ CentralReach |
| Automated pre-session SMS/email reminders | SimplePractice, Jane App, TherapEZ, PractiPal | Table stakes | Reminders sent automatically at 24h and 2h before session. Message includes child name, date, time, and center name. Parent can confirm or cancel via reply. | ✅ SimplePractice; 🔵 PractiPal partially inferred |
| Missed session follow-up notification | TherapEZ, SimplePractice | Differentiator (in Indian market) | When a session is marked Absent/No-show, a follow-up message is automatically triggered to the parent asking if they want to reschedule. | 🔵 Inferred from TherapEZ's dropout-prevention marketing; 🔵 SimplePractice has "no-show" email template |
| Fee due / payment reminders | PractiPal, TherapEZ | Table stakes (India) | Automated messages when a fee is due or overdue. Sent via SMS or WhatsApp. May include a UPI payment link. | ✅ PractiPal (UPI payments); 🔵 TherapEZ inferred |
| Configurable reminder templates | SimplePractice, Jane App | Differentiator | Center can edit the default reminder message text, add center name/logo/contact. Templates saved and reused. | ✅ SimplePractice custom reminder templates confirmed |
| Delivery status tracking for reminders | SimplePractice, CentralReach | Differentiator | Log of which reminders were sent, delivered, and read. Staff can see if a parent received the reminder. | 🔵 Inferred from CentralReach communication logs; 🔵 SimplePractice |
| WhatsApp Business API — appointment reminders | Clinics and therapy centers in India (category norm) | Differentiator (in structured therapy software) | Appointment confirmation and reminder messages sent via WhatsApp Business API using pre-approved templates. Message appears to come from the center's WhatsApp Business number. | 🔵 Inferred from WhatsApp Business API category norms; no specific therapy software product has published this feature for India |
| WhatsApp Business API — payment links | Indian clinics (general) | Differentiator | A UPI payment link is embedded in a WhatsApp message to the parent. Parent taps the link and pays via UPI without logging into the platform. | 🔵 Inferred from WhatsApp Business API + UPI integration patterns in Indian SMB market |
| WhatsApp Business API — session summaries and progress updates | Hi Rasmus (parent portal), no India tool | Novel (India) | After a session, a templated summary is sent to the parent via WhatsApp: what was practiced, how the child did, what to reinforce at home. Structured, not free-text. | 🔵 Hi Rasmus has parent portal equivalent; WhatsApp delivery in India is 🔶 speculated |
| Opt-in / opt-out per parent for WhatsApp messaging | WhatsApp Business API requirement | Table stakes (regulatory) | Each parent must opt in to receive WhatsApp Business messages. Opt-out removes them from all templated messages. Required by WhatsApp Business API policy. | ✅ WhatsApp Business API policy confirmed |
| Approved template management for WhatsApp Business API | WhatsApp Business API requirement | Table stakes (regulatory) | All message templates must be pre-approved by Meta before sending. Platform stores approved templates; staff select from the approved library. | ✅ WhatsApp Business API policy confirmed |

---

## Feature Brief: Appointment Scheduling

**Inspired by:** Jane App, SimplePractice, TherapEZ, CentralReach
**Prevalence:** Table stakes — every competing therapy center management tool has this
**Target user:** Rahul (center director, scheduling owner), Priya (therapist, session attendance)
**What it does:** Allows Rahul to create and manage each child's recurring weekly therapy schedule, assign therapists and rooms, and view the full center calendar in one place. Priya can see her own daily schedule, mark attendance at the start or end of each session, and request reschedules.
**What "done" looks like:** Rahul can set up a new child's weekly schedule in under 3 minutes, view all active schedules across therapists and rooms in a single calendar, and mark all attendance for the day without opening a paper register. Priya can see her sessions for the day on her phone and mark each session attended in ≤ 2 taps.

**[ASSUMPTION — NOT VALIDATED]** This feature is assumed to replace the current paper/WhatsApp scheduling workflow for Rahul and that he experiences the current system as sufficiently painful to adopt new software for this function. No primary research has confirmed this assumption. Validate before committing engineering capacity.

---

## Feature Brief: SMS / Email Reminders

**Inspired by:** SimplePractice, Jane App, TherapEZ, PractiPal
**Prevalence:** Table stakes in the US market; differentiator in India (no Indian tool has confirmed structured automated reminders with delivery tracking)
**Target user:** Rahul (configures), Meena (recipient)
**What it does:** Automatically sends appointment reminders to parents 24 hours and 2 hours before each session via SMS and/or email. When a session is marked as a no-show, a follow-up message is triggered. Fee due dates trigger separate configurable reminders. Rahul can edit reminder templates and view delivery logs.
**What "done" looks like:** A parent (Meena) receives a reminder without any manual action from Rahul or Priya. Rahul can see in the admin panel which reminders were delivered and which failed. No-show follow-up is automatically sent within 30 minutes of a missed session. Fee reminders fire on the configured schedule without Rahul having to remember to message individually.

**[ASSUMPTION — NOT VALIDATED]** This feature is assumed to reduce the 39% no-show rate observed in studies where no reminders exist. The applicability of the Psychiatric Services no-show study (US psychiatric outpatient context) to Indian autism therapy sessions has not been validated in primary research.

---

## Feature Brief: WhatsApp Integration

**Inspired by:** WhatsApp Business API category norms, Hi Rasmus (parent portal equivalent), Indian SMB clinic WhatsApp practices
**Prevalence:** Novel for structured therapy software in India; category norm for general Indian SMB communications
**Target user:** Rahul (configures and sends), Meena (receives via WhatsApp)
**What it does:** Connects the platform to a WhatsApp Business API account so that appointment reminders, payment links, session summaries, and progress update snippets can be sent to parents as structured WhatsApp messages that appear to come from the center's WhatsApp Business number. Does not replace WhatsApp — adds structured, record-keeping-enabled messages alongside existing WhatsApp usage. Parents opt in per message type; opt-out is respected immediately.
**What "done" looks like:** Meena receives a WhatsApp message that looks like it's from "Sunshine Therapy Center" (not a random number), confirming her child's session tomorrow. The platform logs that the message was sent and delivered. Rahul never manually copied and pasted a single appointment detail into WhatsApp to send this.

**[ASSUMPTION — NOT VALIDATED]** This feature assumes that (a) Indian therapy center directors are willing to set up and pay for a WhatsApp Business API account, (b) parents will opt in to receive structured WhatsApp messages from the platform, and (c) parents will perceive platform-generated WhatsApp messages as equivalent or superior to manually typed center messages. None of these have been validated.

---

## Epic 1: Appointment Scheduling

**Goal:** Rahul can create, manage, and view all therapy session schedules from a single interface, replacing paper registers and WhatsApp-based scheduling coordination. Priya can view her daily sessions and mark attendance from her phone.
**Copied from:** Jane App (recurring scheduling, room management, multi-provider calendar), SimplePractice (reschedule/cancel flows), TherapEZ (center-level scheduling view), CentralReach (attendance marking tied to billing)
**Target user(s):** Rahul (primary), Priya (secondary)
**Definition of Done:**
- [ ] Recurring weekly schedules can be created and edited for any child
- [ ] Therapist availability is enforced; double-booking is blocked
- [ ] Room/slot management prevents room double-booking
- [ ] Rescheduling and cancellation flows work end-to-end with parent notification
- [ ] Attendance can be marked (Present / Absent / No-show / Cancelled) per session
- [ ] Center director calendar shows all therapists, children, and rooms in one view
- [ ] All flows tested on minimum-spec Android (Redmi/Realme, 2GB RAM, Android 10+)
- [ ] Offline attendance marking works; syncs on connection restore

**Out of scope (this epic):** Automated reminder sending (Epic 2), WhatsApp message dispatch (Epic 3), billing calculation from attendance (Cluster 5 — Billing), in-session data collection (separate cluster), parent-facing schedule view

**[ASSUMPTION — NOT VALIDATED]** Center directors in Indian autism therapy centers currently manage scheduling through WhatsApp and paper, and this creates sufficient pain to motivate adoption of a structured scheduling tool.

---

### Story SCHED-001: Create a recurring weekly schedule for a child

**As a** Rahul
**I want to** create a recurring weekly therapy schedule for a child (e.g., Mon/Wed/Fri at 10:00 AM, 45 minutes, with Priya in Room 1)
**So that** the child's sessions are automatically populated in the calendar for the next 12 weeks without me entering them one by one

**Inspired by:** Jane App recurring appointment series; SimplePractice recurring events

**Context:** Rahul is onboarding a new child or changing an existing child's schedule. He is on his Android phone or desktop browser. The child record already exists in the system.

**Acceptance Criteria:**
- [ ] AC-01: Given Rahul is on a child's profile and taps "Add Schedule", when he selects day(s) of week, start time, duration, assigned therapist, and room, then the system creates recurring sessions from the next occurrence through 12 weeks forward
- [ ] AC-02: Given a recurring schedule exists, when Rahul edits a single occurrence, the system asks "Edit this session only / Edit all future sessions / Edit all sessions" before saving
- [ ] AC-03: Given a recurring schedule is active, when the assigned therapist's availability conflicts with any session in the series, the system displays a warning listing the conflicting dates before saving
- [ ] AC-04: Given a schedule is created, when Rahul views the center calendar, all recurring sessions appear with child name, therapist name, and room visible
- [ ] AC-05: Given a session is in the past, when Rahul edits the series, past sessions are not modified

**Edge Cases & Error States:**
- [ ] EC-01: If the selected room is already booked for a time slot in the series, the system shows which specific dates conflict and asks Rahul to resolve them before saving
- [ ] EC-02: If the child record has no assigned therapist, the therapist field is required before saving
- [ ] EC-03: If the center has no rooms configured, the room field is optional (single-room centers)

**Non-Functional Requirements:**
- Performance: Schedule creation for a 12-week series must complete in < 3 seconds on a 4G connection
- Offline: If offline, the schedule creation queues locally and syncs when connection is restored; Rahul is shown a "Saved locally — will sync" confirmation
- Accessibility: All form fields have labels ≥ 44px touch targets; date/time pickers are native Android/browser controls
- Privacy: ⚠️ DPDPA — child schedule data is health-adjacent data for a minor; parental consent must be confirmed before any child record is created (dependency on consent flow)

**Dependencies:**
- Blocked by: Child record creation flow (intake cluster); therapist account creation; room configuration
- Enables: SCHED-002 (therapist calendar view), SCHED-003 (room conflict detection), SCHED-004 (rescheduling), SCHED-005 (attendance marking), REMIND-001 (reminder triggers)

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android (Redmi/Realme, 2GB RAM, Android 10+)
- [ ] Offline queue and sync tested with airplane mode simulation
- [ ] Conflict detection tested with intentionally overlapping schedules
- [ ] Code reviewed and merged

---

### Story SCHED-002: View and manage therapist availability

**As a** Rahul
**I want to** set each therapist's working days, hours, and blocked slots (e.g., Priya is off on Thursdays; blocked 12–1 PM every day)
**So that** the scheduling system never allows me to book a session in a slot the therapist is unavailable, and I can see Priya's current availability before booking

**Inspired by:** Jane App provider availability settings; SimplePractice clinician schedule blocks

**Context:** Rahul is setting up a new therapist's availability or updating an existing one. Done on desktop or Android. Happens at onboarding and whenever availability changes.

**Acceptance Criteria:**
- [ ] AC-01: Given Rahul opens a therapist's profile, when he navigates to "Availability", he can set working days (checkboxes: Mon–Sun) and working hours (start/end time per day)
- [ ] AC-02: Given availability is set, when Rahul tries to schedule a child session during a blocked slot for that therapist, the system prevents saving and shows "Priya is not available at this time"
- [ ] AC-03: Given a therapist has a one-off leave day (e.g., a holiday), when Rahul marks that date as blocked, no new sessions can be booked and existing sessions on that date show a conflict warning
- [ ] AC-04: Given a therapist's availability changes, when Rahul updates it, existing sessions outside the new availability are flagged (not auto-deleted) with a "Review conflict" badge

**Edge Cases & Error States:**
- [ ] EC-01: If Rahul tries to save an availability window shorter than any existing session duration (e.g., sets end time to 11 AM but a session runs 10:30–11:15 AM), the system warns before saving
- [ ] EC-02: If all therapists are unavailable for a requested slot, the system shows a message suggesting the nearest available slot rather than a blank error

**Non-Functional Requirements:**
- Offline: Availability reads from local cache; writes queue locally and sync on restore
- Accessibility: Touch targets ≥ 44px; day checkboxes have visible labels

**Dependencies:**
- Blocked by: Therapist account creation
- Enables: SCHED-001 (conflict detection during scheduling)

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android
- [ ] Conflict flagging tested with overlapping schedule scenarios
- [ ] Code reviewed and merged

---

### Story SCHED-003: Reschedule or cancel a session

**As a** Priya or Rahul
**I want to** reschedule a session to a different date/time, or cancel it with an optional reason
**So that** the calendar stays accurate and the parent is notified of the change without Rahul having to manually send a WhatsApp message

**Inspired by:** SimplePractice reschedule/cancel flows; Jane App appointment management

**Context:** A session needs to change because the child is sick, the therapist has an emergency, or the parent requested it. Can happen from the calendar view or from the child's session list. On Android.

**Acceptance Criteria:**
- [ ] AC-01: Given a session exists in the calendar, when Rahul or Priya taps "Reschedule", they are shown a date/time picker pre-filtered to the therapist's available slots
- [ ] AC-02: Given a new date/time is selected, when Rahul confirms the reschedule, the old session is removed from the calendar and the new session is created; a notification is queued to the parent (via the configured reminder channel)
- [ ] AC-03: Given a session is cancelled, when Rahul selects "Cancel", a dropdown of cancellation reasons appears (Child sick / Parent request / Center holiday / Other); selecting one and confirming marks the session Cancelled
- [ ] AC-04: Given a cancellation, when the reason is recorded, it appears in the session history for that child (visible to Rahul and Dr. Sunita, not to the parent by default)
- [ ] AC-05: Given a session is part of a recurring series, when Rahul cancels it, the system asks "Cancel this session only / Cancel all future sessions" before proceeding

**Edge Cases & Error States:**
- [ ] EC-01: If the reschedule target slot has a conflict (room or therapist), the system blocks and explains which resource conflicts
- [ ] EC-02: If the parent notification channel (SMS/WhatsApp) is not configured, the system shows "Session rescheduled — reminder not sent (no notification channel configured)" and prompts Rahul to set one up

**Non-Functional Requirements:**
- Offline: Reschedule and cancellation actions queue locally; sync on restore
- Accessibility: Touch targets ≥ 44px; cancellation reason dropdown uses native Android spinner
- Privacy: ⚠️ DPDPA — cancellation reason involving health data (e.g., "Child sick") is health-adjacent data for a minor; stored with appropriate access control

**Dependencies:**
- Blocked by: SCHED-001 (recurring schedule), SCHED-002 (therapist availability)
- Enables: REMIND-001 (reschedule notification trigger), SCHED-005 (attendance status)

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android
- [ ] Recurring series cancel tested (single vs. all)
- [ ] Notification fallback when channel not configured tested
- [ ] Code reviewed and merged

---

### Story SCHED-004: Mark session attendance

**As a** Priya
**I want to** mark each session as Present, Absent, No-show, or Cancelled at the start or end of the session
**So that** Rahul has an accurate attendance record for billing and dropout-risk tracking without relying on a paper register

**Inspired by:** CentralReach attendance/billing status; SimplePractice session status; TherapEZ attendance tracking

**Context:** Priya is about to start a session or has just finished. She is on her Android phone. The child may be present and active — this action must be ≤ 2 taps.

**Acceptance Criteria:**
- [ ] AC-01: Given Priya opens her daily schedule view, when she taps on a session card, she sees a large "Mark attendance" button with four options: Present / Absent / No-show / Cancelled — each as a distinct tappable chip
- [ ] AC-02: Given Priya taps "Present", the session is marked Present with a timestamp; haptic feedback confirms the action; the session card updates visually (green indicator)
- [ ] AC-03: Given a session is marked Present, when Rahul views the center calendar, the session shows a green "P" status indicator
- [ ] AC-04: Given a session is marked No-show, when the center has SMS/email reminders enabled, a follow-up notification is queued to the parent automatically (within 30 minutes) — this depends on REMIND-002
- [ ] AC-05: Given it is end of day and Priya has sessions still at "Scheduled" status (not yet marked), the app shows a badge count on her home screen reminding her to mark outstanding attendance

**Edge Cases & Error States:**
- [ ] EC-01: If Priya marks a session Present but the child's billing plan requires a confirmed attendance window, and the session is outside that window (e.g., session started 45 minutes late), the system still accepts the mark but flags it for Rahul's review
- [ ] EC-02: If a session was already marked by Rahul (e.g., Rahul marked it Cancelled because the room was unavailable), Priya sees the status but cannot override without Rahul-level permissions

**Non-Functional Requirements:**
- Performance: Attendance mark must register in < 1 second on a 4G connection
- Offline: Attendance mark writes locally immediately; syncs in background; Priya sees "Saved" confirmation even offline
- Accessibility: Touch targets ≥ 44px; haptic feedback on confirmation; chips use high-contrast color + label (not color alone)
- Privacy: ⚠️ DPDPA — attendance data linked to a child's health program; stored with appropriate access control

**Dependencies:**
- Blocked by: SCHED-001 (session must exist), Priya's therapist account
- Enables: REMIND-002 (no-show follow-up trigger), Cluster 5 billing (session count for invoice), Stage 8 dropout risk tracking

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android
- [ ] Offline write and sync tested with airplane mode
- [ ] Haptic confirmed on physical test device
- [ ] ≤ 2 taps from daily schedule to confirmed attendance mark (tested in QA)
- [ ] Code reviewed and merged

---

### Story SCHED-005: Center director all-schedules calendar view

**As a** Rahul
**I want to** see every therapist's sessions, every child's schedule, and every room's occupancy in a single calendar view — filterable by therapist, child, or room
**So that** I can manage the center's capacity, spot gaps, and see at a glance whether today's schedule is running as planned

**Inspired by:** Jane App multi-provider calendar; CentralReach staff scheduling dashboard; TherapEZ center-level calendar view

**Context:** Rahul checks the calendar at the start of each day on his Android phone or desktop. He may also check mid-session to see if a room is running late.

**Acceptance Criteria:**
- [ ] AC-01: Given Rahul opens the Schedule tab, the default view shows today's sessions in a vertical time-grid with columns per therapist or room (configurable: group by therapist / group by room)
- [ ] AC-02: Given the default day view, when Rahul switches to Week view, all sessions across the week are shown in the same grid format
- [ ] AC-03: Given the calendar is in any view, when Rahul applies a filter (e.g., "Priya only" or "Room 2 only"), only matching sessions are shown; other sessions are greyed out (not hidden, so capacity is still visible)
- [ ] AC-04: Given a session in the calendar has an attendance status set, the session card shows the status visually (green = Present, amber = Absent, red = No-show, grey = Cancelled, white = not yet marked)
- [ ] AC-05: Given Rahul taps any session card in the calendar, a bottom sheet opens showing: child name, therapist, room, time, status, and quick actions (Mark attendance / Reschedule / Cancel)

**Edge Cases & Error States:**
- [ ] EC-01: If the center has more than 10 therapists, the calendar switches to a list-per-therapist accordion layout rather than a side-by-side column grid (columns exceed screen width)
- [ ] EC-02: If no sessions exist for the selected day, the view shows "No sessions scheduled for [date]" with a shortcut to add a session

**Non-Functional Requirements:**
- Performance: Calendar must render today's view in < 2 seconds on a 4G connection for a center with up to 50 sessions/day
- Offline: Calendar loads from local cache when offline; shows "Last synced [time]" banner; cached data is up to 7 days
- Accessibility: Status indicators use color + text label, never color alone

**Dependencies:**
- Blocked by: SCHED-001 (sessions must exist), SCHED-004 (attendance status)
- Enables: Rahul's dropout-risk monitoring (Stage 8 workstream)

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android and desktop browser (Chrome)
- [ ] 50-session calendar renders in < 2 seconds on test device
- [ ] Filter tested with all filter combinations
- [ ] Code reviewed and merged

---

## Backlog: Epic 1 — Appointment Scheduling

| Story ID | Title | Persona | Complexity | Priority | Blocked by |
|---|---|---|---|---|---|
| SCHED-001 | Create recurring weekly schedule for a child | Rahul | L | P0 | Child record, therapist account, room config |
| SCHED-002 | View and manage therapist availability | Rahul | M | P0 | Therapist account |
| SCHED-003 | Reschedule or cancel a session | Rahul, Priya | M | P0 | SCHED-001, SCHED-002 |
| SCHED-004 | Mark session attendance | Priya | S | P0 | SCHED-001 |
| SCHED-005 | Center director all-schedules calendar view | Rahul | L | P0 | SCHED-001, SCHED-004 |

---

## Epic 2: SMS / Email Reminders

**Goal:** Parents receive automated appointment reminders and missed-session follow-up messages without any manual action from Rahul or Priya, reducing no-show rates and eliminating the time Rahul spends manually sending WhatsApp reminders.
**Copied from:** SimplePractice (automated reminders, configurable templates, delivery logs), Jane App (multi-channel reminder timing), TherapEZ (appointment reminders as a marketed feature), PractiPal (fee due reminders)
**Target user(s):** Rahul (configures), Meena (recipient)
**Definition of Done:**
- [ ] 24h and 2h pre-session reminders fire automatically for all confirmed sessions
- [ ] No-show follow-up fires within 30 minutes of a session being marked No-show
- [ ] Fee due reminders fire on the configured day/time relative to invoice due date
- [ ] Rahul can edit reminder templates without engineering involvement
- [ ] Delivery status (sent / delivered / failed) is visible in a log
- [ ] All reminder types tested end-to-end in staging with a real SMS provider (e.g., Twilio, MSG91) and email provider
- [ ] Unsubscribe/opt-out from SMS is supported per telecom regulations (TRAI DLT compliance)

**Out of scope (this epic):** WhatsApp message delivery (Epic 3), in-app push notifications, parent portal, two-way SMS replies triggering automated rescheduling, multi-language templates (Phase 2)

**[ASSUMPTION — NOT VALIDATED]** Automated reminders will reduce no-show rates at Indian autism therapy centers. The 39% → 3% no-show reduction data from Psychiatric Services is from a US psychiatric outpatient context. Whether this effect size translates to Indian autism therapy families has not been validated.

---

### Story REMIND-001: Send automated pre-session reminder (24h and 2h)

**As a** Meena
**I want to** receive a reminder message 24 hours and 2 hours before my child's therapy session
**So that** I don't forget the appointment and can plan my day accordingly without needing to scroll through old WhatsApp chats to find the session time

**Inspired by:** SimplePractice automated appointment reminders; Jane App multi-timing reminder system

**Context:** Meena is at home or commuting. The reminder arrives on her phone via SMS or email (configured by Rahul). She does not need to be logged into any app.

**Acceptance Criteria:**
- [ ] AC-01: Given a session is in Scheduled or Confirmed status and the child's parent contact (mobile number or email) is on file, when the system clock reaches T-24h before session start, an SMS or email is sent to the parent using the configured template
- [ ] AC-02: Given the 24h reminder fires, when the system clock reaches T-2h before session start, a second reminder fires using the 2h template (distinct from the 24h template text)
- [ ] AC-03: Given the reminder fires, when the SMS/email is sent, the system logs: message type (24h / 2h), channel (SMS / email), timestamp, and delivery status (sent / delivered / failed)
- [ ] AC-04: Given a session is cancelled or rescheduled before the reminder fires, when the scheduled reminder job runs, it checks session status and skips sending if status is Cancelled
- [ ] AC-05: Given Rahul has disabled reminders for a specific child (per-child toggle), when reminder jobs run, that child's sessions are excluded

**Edge Cases & Error States:**
- [ ] EC-01: If the parent's mobile number is missing or invalid, the reminder fails silently for that session; Rahul's delivery log shows "Failed — invalid number" and the session is flagged in the admin panel
- [ ] EC-02: If both SMS and email are configured and one channel fails, the system retries on the other channel and logs the fallback attempt
- [ ] EC-03: If a session is rescheduled within the 24h window (i.e., the 24h reminder has already fired), the system sends a "Schedule change" message to the parent rather than a second reminder

**Non-Functional Requirements:**
- Performance: Reminder dispatch for all sessions due in the next 2 hours must complete within 5 minutes of the scheduled job run time (for a center with up to 50 sessions/day)
- Reliability: SMS delivery must use a provider with DLT-registered sender ID (TRAI DLT compliance for transactional SMS in India — mandatory for SMS delivery)
- Privacy: ⚠️ DPDPA — parent mobile number and email are personal data; reminder message must not include clinical data (diagnosis, session content) — only logistics (child name, date, time, center name)

**Dependencies:**
- Blocked by: SCHED-001 (session must exist with status), SCHED-002 (therapist availability confirms session validity), parent contact data in child record, SMS/email provider integration, DLT sender ID registration
- Enables: REMIND-002 (no-show follow-up depends on REMIND-001's delivery log), Rahul's dropout monitoring

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android (Rahul side); end-to-end SMS delivery tested with live test number
- [ ] DLT-registered sender ID confirmed in staging
- [ ] Failed reminder flagged in admin log tested
- [ ] Session cancellation suppresses reminder tested
- [ ] Code reviewed and merged

---

### Story REMIND-002: Send missed-session follow-up notification

**As a** Rahul
**I want to** have a follow-up message automatically sent to Meena when her child's session is marked as a No-show
**So that** I don't have to remember to message every no-show family manually, and Meena gets a prompt to reschedule before the gap becomes a dropout

**Inspired by:** TherapEZ missed-session follow-up; SimplePractice no-show messaging templates

**Context:** Priya marked the session No-show (SCHED-004). The system should trigger the follow-up within 30 minutes. Rahul configured the follow-up template during onboarding.

**Acceptance Criteria:**
- [ ] AC-01: Given a session is marked No-show, when 30 minutes elapse after the mark, an SMS (or email) is sent to the parent using the missed-session follow-up template
- [ ] AC-02: Given the follow-up is sent, when Rahul views the delivery log, the follow-up entry is logged separately from appointment reminders with type "No-show follow-up"
- [ ] AC-03: Given the follow-up template is the default, it reads: "[Child name] missed their session at [Center name] today. We hope everything is okay. Please contact us to reschedule: [center phone number]" — with Rahul able to edit this template
- [ ] AC-04: Given Rahul manually marks a session Cancelled (not No-show), no follow-up message fires — follow-up is No-show only
- [ ] AC-05: Given a parent has previously opted out of SMS reminders, the follow-up message is also suppressed

**Edge Cases & Error States:**
- [ ] EC-01: If the session is re-marked from No-show to Present (e.g., the child arrived 45 minutes late), and the 30-minute follow-up has not yet fired, the scheduled follow-up is cancelled
- [ ] EC-02: If a family receives 3+ no-show follow-ups in 30 days, Rahul's dashboard shows a "Dropout risk" badge on the child's record (this is a UI-only flag; the more advanced dropout risk scoring is out of scope for this Epic)

**Non-Functional Requirements:**
- Performance: Follow-up dispatch must execute within 30 minutes ± 5 minutes of the No-show mark
- Privacy: ⚠️ DPDPA — message must not reference clinical content; "missed session" only, no diagnosis or therapy details

**Dependencies:**
- Blocked by: SCHED-004 (no-show status must exist), REMIND-001 (shared SMS delivery infrastructure), parent contact data
- Enables: Stage 8 dropout prevention workstream (attendance trend + follow-up history as input signals)

**Definition of Done:**
- [ ] All AC pass in QA
- [ ] Re-mark cancellation of pending follow-up tested
- [ ] Dropout risk badge at 3+ no-shows tested
- [ ] 30-minute timing tested with mocked clock in staging
- [ ] Code reviewed and merged

---

### Story REMIND-003: Fee due reminders

**As a** Rahul
**I want to** have automated fee due reminder messages sent to Meena before and on the invoice due date
**So that** I don't have to personally send uncomfortable fee messages, payment is not delayed, and Meena has advance notice to arrange the payment

**Inspired by:** PractiPal fee reminders + UPI payment integration; TherapEZ invoice notifications

**Context:** End of month (or per center's billing cycle). A fee is due from Meena. Rahul has configured a fee reminder schedule (e.g., 3 days before due, on due date, 3 days after if unpaid).

**Acceptance Criteria:**
- [ ] AC-01: Given an invoice is created for a family, when the due date is 3 days away, an SMS is sent to the parent: "[Center name]: Your therapy fee of ₹[amount] is due on [date]. [Optional: UPI ID / contact to pay]"
- [ ] AC-02: Given the 3-day reminder fires and the invoice is still unpaid on the due date, a second reminder fires on the due date
- [ ] AC-03: Given the invoice remains unpaid 3 days after the due date, a third "overdue" reminder fires — with configurable overdue language set by Rahul
- [ ] AC-04: Given a payment is marked as received (manual mark by Rahul), when subsequent reminders are scheduled, they are cancelled and no further reminders fire for that invoice
- [ ] AC-05: Given Rahul wants to send a payment link in the reminder, the template supports a [PAYMENT_LINK] variable that injects a UPI deep link or a URL to the center's payment page (actual UPI payment processing is out of scope for this story — link is a static field Rahul configures)

**Edge Cases & Error States:**
- [ ] EC-01: If the invoice amount is ₹0 (fully written off or waived by Rahul), no reminders fire
- [ ] EC-02: If multiple invoices are due for the same family in the same billing cycle, a single consolidated reminder lists all outstanding amounts (not separate messages per invoice)

**Non-Functional Requirements:**
- Privacy: ⚠️ DPDPA — financial amount tied to a specific child is personal data; message not to include clinical details
- Regulatory: DLT registered transactional sender ID required for fee reminder SMS in India (same as REMIND-001)

**Dependencies:**
- Blocked by: Invoice creation flow (Cluster 5 — Billing), REMIND-001 (shared SMS infrastructure)
- Enables: Cluster 5 billing — payment tracking and collection rate reporting

**Definition of Done:**
- [ ] All AC pass in QA
- [ ] Payment received → reminder cancellation tested
- [ ] ₹0 invoice suppression tested
- [ ] Consolidated multi-invoice reminder tested
- [ ] Code reviewed and merged

---

### Story REMIND-004: Configure and manage reminder templates

**As a** Rahul
**I want to** view and edit the text of each reminder template (24h reminder, 2h reminder, no-show follow-up, fee due, fee overdue)
**So that** the messages sound like they come from my center, use my center's name and phone number, and match the tone I want to use with families

**Inspired by:** SimplePractice custom reminder templates; Jane App message template editor

**Context:** Rahul is setting up the platform for the first time, or wants to update reminder language. He is on desktop or Android. This is a low-frequency admin task (set once, rarely changed).

**Acceptance Criteria:**
- [ ] AC-01: Given Rahul navigates to Settings > Reminders, he sees a list of all template types (24h appointment, 2h appointment, no-show follow-up, fee due, fee overdue) with their current text and channel (SMS / email)
- [ ] AC-02: Given Rahul taps Edit on a template, he sees a text editor with the current template text and a list of available variables: [CHILD_NAME], [SESSION_DATE], [SESSION_TIME], [CENTER_NAME], [CENTER_PHONE], [AMOUNT_DUE], [DUE_DATE]
- [ ] AC-03: Given Rahul saves a template, when the next reminder fires using that template, it uses the updated text with variables substituted correctly
- [ ] AC-04: Given Rahul edits an SMS template to exceed 160 characters, the editor shows a character count and warns "This message will be sent as 2 SMS segments — additional cost may apply"
- [ ] AC-05: Given Rahul wants to preview a template, a "Preview" button substitutes dummy values ([CHILD_NAME] → "Arjun") and shows the rendered message before saving

**Edge Cases & Error States:**
- [ ] EC-01: If Rahul deletes all text from a template and tries to save, the system blocks with "Template cannot be empty — reminders will not send without a message"
- [ ] EC-02: If Rahul uses an undefined variable (e.g., types [THERAPIST_NAME] which is not a supported variable), the editor underlines it in red and shows "Unsupported variable — will appear as-is in the message"

**Non-Functional Requirements:**
- Accessibility: Text editor uses ≥ 16px font; character count updates live

**Dependencies:**
- Blocked by: REMIND-001 (reminder system must exist for templates to apply)
- Enables: All reminder stories (templates are the content layer)

**Definition of Done:**
- [ ] All AC pass in QA
- [ ] Variable substitution tested with all supported variables
- [ ] Invalid variable warning tested
- [ ] Empty template block tested
- [ ] Character count overflow warning tested
- [ ] Code reviewed and merged

---

### Story REMIND-005: View reminder delivery log

**As a** Rahul
**I want to** see a log of all reminders sent — including delivery status (sent / delivered / failed) — for any child or for the whole center
**So that** I know which parents were actually reached, can identify families whose contact details are broken, and have a record if a parent claims they weren't reminded

**Inspired by:** SimplePractice communication log; CentralReach message delivery tracking

**Context:** Rahul checks this periodically — daily or weekly. He may also check it when a parent claims they didn't receive a reminder.

**Acceptance Criteria:**
- [ ] AC-01: Given Rahul navigates to Reports > Communication Log, he sees a filterable table: columns are Date, Child, Parent, Message Type, Channel, Status (Sent / Delivered / Failed)
- [ ] AC-02: Given Rahul filters by child name, only messages for that child are shown
- [ ] AC-03: Given a message status is Failed, the row shows a failure reason (e.g., "Invalid number", "Carrier rejected", "Email bounced") and a "Retry" button
- [ ] AC-04: Given Rahul taps Retry on a failed message, the system re-attempts delivery and updates the log row with the new attempt status
- [ ] AC-05: Given the log contains > 100 entries, pagination is applied (25 per page); Rahul can also export the full log as a CSV

**Edge Cases & Error States:**
- [ ] EC-01: If a reminder was suppressed (cancelled because session was rescheduled before it fired), it appears in the log with status "Suppressed — session rescheduled" so Rahul can audit why no message was sent
- [ ] EC-02: If an SMS delivery receipt is not returned by the provider within 1 hour, status shows "Sent — delivery unconfirmed"

**Non-Functional Requirements:**
- Performance: Log must load within 2 seconds for up to 1,000 log entries
- Privacy: ⚠️ DPDPA — log contains parent contact data linked to child; access restricted to Rahul-level roles only

**Dependencies:**
- Blocked by: REMIND-001 (log is populated by the reminder system)
- Enables: Rahul's operational reporting; dropout risk monitoring

**Definition of Done:**
- [ ] All AC pass in QA
- [ ] Retry tested with simulated failed delivery
- [ ] Suppressed entry tested with rescheduled session scenario
- [ ] CSV export tested
- [ ] Code reviewed and merged

---

## Backlog: Epic 2 — SMS / Email Reminders

| Story ID | Title | Persona | Complexity | Priority | Blocked by |
|---|---|---|---|---|---|
| REMIND-001 | Send automated pre-session reminders (24h and 2h) | Meena (recipient), Rahul (configures) | L | P0 | SCHED-001, parent contact data, SMS/email provider, DLT registration |
| REMIND-002 | Send missed-session follow-up notification | Rahul, Meena | M | P0 | SCHED-004, REMIND-001 |
| REMIND-003 | Fee due reminders | Rahul, Meena | M | P1 | Billing/invoice flow (Cluster 5), REMIND-001 |
| REMIND-004 | Configure and manage reminder templates | Rahul | S | P0 | REMIND-001 |
| REMIND-005 | View reminder delivery log | Rahul | M | P1 | REMIND-001 |

---

## Epic 3: WhatsApp Integration

**Goal:** The platform can send structured, template-compliant WhatsApp messages to parents on behalf of the therapy center — covering appointment confirmations, payment links, session summaries, and progress update snippets — using WhatsApp Business API. Parents receive messages that appear to come from the center's WhatsApp Business number, not from a product the center uses.
**Copied from:** WhatsApp Business API category norms (Indian SMB market), Hi Rasmus parent portal (session summary delivery), PractiPal + TherapEZ (payment/reminder in Indian context)
**Target user(s):** Rahul (configures and triggers), Meena (receives on WhatsApp), Priya (session summary content originates from her session note)
**Definition of Done:**
- [ ] Platform is connected to a WhatsApp Business API account (center-owned WABA)
- [ ] Approved message templates stored and selectable in platform
- [ ] Appointment reminder (24h / 2h) can be sent via WhatsApp channel in addition to or instead of SMS
- [ ] Payment link message can be sent via WhatsApp
- [ ] Session summary message can be sent via WhatsApp after session
- [ ] Progress update snippet can be sent via WhatsApp
- [ ] Per-parent opt-in recorded before any WhatsApp message is sent
- [ ] Per-parent opt-out removes parent from all WhatsApp messaging immediately
- [ ] All messages sent through approved templates only (no free-text outside template)
- [ ] WABA setup guide provided to Rahul in onboarding docs (setup involves Meta Business Manager — this is not in-platform)

**Out of scope (this epic):** Two-way WhatsApp conversation (inbound message handling), free-text messaging from platform staff to parents via WhatsApp, WhatsApp group messaging, replacing existing WhatsApp personal number usage by center staff, parent-facing app/portal, Hindi/regional language templates (Phase 2)

**[ASSUMPTION — NOT VALIDATED]** Three core assumptions drive this epic, none validated: (1) Indian therapy center directors are willing to set up a WhatsApp Business API account (requires Meta Business Manager, Facebook Business verification, and a dedicated business phone number — non-trivial for a small center founder); (2) parents will opt in to receive structured WhatsApp messages from a business number rather than a personal number; (3) parents will perceive business-account WhatsApp messages as coming "from the center" rather than as impersonal automated messages.

---

### Story WA-001: Connect center's WhatsApp Business API account

**As a** Rahul
**I want to** connect my center's WhatsApp Business API account to the platform so that messages can be sent from my center's business WhatsApp number
**So that** all WhatsApp messages parents receive appear to come from my center — not from a random unknown number

**Inspired by:** WhatsApp Business API embedded sign-up flow (Meta); used by booking and clinic platforms across India

**Context:** Rahul is setting up the platform for the first time. He has (or needs to create) a Meta Business Manager account and a WhatsApp Business API account. This is a one-time setup. Done on desktop.

**Acceptance Criteria:**
- [ ] AC-01: Given Rahul navigates to Settings > WhatsApp, he sees a "Connect WhatsApp Business Account" button with a plain-English explanation of what is required (Meta Business account, verified business phone number)
- [ ] AC-02: Given Rahul clicks Connect, the platform initiates the Meta embedded sign-up flow (WhatsApp Business API onboarding via Meta's OAuth); on completion, the platform stores the WABA ID and phone number ID
- [ ] AC-03: Given the connection is successful, the Settings > WhatsApp page shows: connected phone number, WABA display name, account status (Active / Pending verification / Suspended)
- [ ] AC-04: Given the connection fails (e.g., Meta rejects verification), Rahul sees a specific error message with a link to Meta's Business Help Center and the error code returned by the Meta API
- [ ] AC-05: Given the WABA account is connected, Rahul can disconnect it from Settings; disconnection stops all WhatsApp message dispatch immediately

**Edge Cases & Error States:**
- [ ] EC-01: If the phone number provided during WABA setup is already registered as a personal WhatsApp account, Meta's verification will fail; the platform shows "This number is already a personal WhatsApp account — use a different business number"
- [ ] EC-02: If the Meta API token expires (tokens expire after 60 days without refresh), the platform sends Rahul an in-app notification and email: "WhatsApp connection expired — reconnect to resume messaging"

**Non-Functional Requirements:**
- Security: Meta API access token stored encrypted at rest; never exposed in client-side code
- Privacy: ⚠️ DPDPA — the WABA connection enables transmission of parent contact data to Meta's infrastructure; consent for this must be covered in the center's DPDPA-compliant parent consent form (dependency on consent flow from intake cluster)

**Dependencies:**
- Blocked by: Rahul has a valid Meta Business Manager account (external dependency — not in-platform); parent consent flow (intake cluster)
- Enables: WA-002 (template management), WA-003 (opt-in flow), WA-004/005/006/007 (all message sending)

**Definition of Done:**
- [ ] All AC pass in QA using a Meta test WABA account
- [ ] Token expiry notification tested with mocked expiry date
- [ ] Disconnect tested — confirms no messages sent after disconnect
- [ ] Code reviewed and merged

---

### Story WA-002: Manage approved WhatsApp message templates

**As a** Rahul
**I want to** view all approved WhatsApp message templates available for the platform, see their approval status, and understand which template is used for which message type
**So that** I know what messages parents will receive and can submit new templates to Meta for approval if I want to customize the message text

**Inspired by:** WhatsApp Business API template management; required by Meta policy for all business-initiated messages

**Context:** WhatsApp Business API requires all outbound messages to use pre-approved templates. The platform ships with a default set of approved templates for appointment reminders, payment links, session summaries, and progress updates. Rahul cannot edit these templates freely — any change requires re-submission to Meta for approval (which can take 24–72 hours). Done on desktop.

**Acceptance Criteria:**
- [ ] AC-01: Given Rahul navigates to Settings > WhatsApp > Templates, he sees a table of all templates with: template name, message type (Appointment Reminder / Payment Link / Session Summary / Progress Update), approval status (Approved / Pending / Rejected), and a preview of the template text
- [ ] AC-02: Given a template shows Rejected status, Rahul sees the rejection reason provided by Meta and a "Resubmit" option after editing the template to comply
- [ ] AC-03: Given Rahul wants a custom template (e.g., in a regional language), he can create a new template entry, write the template text with supported variables, and submit it to Meta via the platform — the platform calls the Meta API to register the template
- [ ] AC-04: Given a template is Pending approval, no messages using that template are sent until Meta approves it; existing approved templates continue to be used for that message type
- [ ] AC-05: Given a template uses variables, the platform validates that all variable placeholders are in the correct WhatsApp format ({{1}}, {{2}}, etc.) before submission

**Edge Cases & Error States:**
- [ ] EC-01: If Meta rejects a default platform template (rare, but possible if Meta's policies change), Rahul is notified in-app and the affected message type falls back to SMS/email until the template is re-approved
- [ ] EC-02: If Rahul submits a custom template and it has been pending for more than 72 hours, the platform shows a "Submission delayed" flag and a link to Meta's template manager for manual follow-up

**Non-Functional Requirements:**
- Compliance: Template content must comply with WhatsApp Business messaging policy; platform must not allow submission of templates containing marketing content, promotional language, or clinical health data in the message body

**Dependencies:**
- Blocked by: WA-001 (WABA must be connected)
- Enables: WA-003, WA-004, WA-005, WA-006, WA-007

**Definition of Done:**
- [ ] All AC pass in QA with Meta sandbox environment
- [ ] Template rejection + resubmit flow tested
- [ ] Custom template submission and variable format validation tested
- [ ] Code reviewed and merged

---

### Story WA-003: Collect and manage parent opt-in / opt-out for WhatsApp messaging

**As a** Rahul
**I want to** record each parent's opt-in consent for receiving WhatsApp messages from the center, and honor opt-out requests immediately
**So that** the platform only sends WhatsApp messages to parents who have agreed to receive them, and the center complies with WhatsApp Business API policy requirements

**Inspired by:** WhatsApp Business API opt-in requirements (mandatory per Meta policy); DPDPA 2023 consent requirements for personal data processing

**Context:** Opt-in must be recorded before any WhatsApp message is sent to a parent. This can happen at intake (center staff asks the parent to opt in on the intake form) or via a WhatsApp opt-in message. Opt-out can happen at any time.

**Acceptance Criteria:**
- [ ] AC-01: Given a parent's profile is being created or edited, Rahul sees a "WhatsApp messaging" toggle with three states: Not asked / Opted in / Opted out; the default state is Not asked
- [ ] AC-02: Given the toggle is set to "Opted in", when any WhatsApp message is triggered for that parent's child, the message is sent
- [ ] AC-03: Given the toggle is set to "Opted out" or "Not asked", when any WhatsApp message is triggered, it is silently suppressed (not sent) and logged in the delivery log as "Suppressed — WhatsApp opt-out"
- [ ] AC-04: Given a parent sends "STOP" as a reply to a WhatsApp Business message, the platform receives the webhook from Meta and immediately sets the parent's WhatsApp toggle to Opted out without any action required from Rahul
- [ ] AC-05: Given Rahul views the parent's profile, the opt-in status shows the date and method of consent (e.g., "Opted in — 2026-04-15 — Staff recorded at intake")

**Edge Cases & Error States:**
- [ ] EC-01: If a parent's STOP webhook is received but the parent is not found in the system (number mismatch), the platform logs the unmatched opt-out for Rahul to review manually
- [ ] EC-02: If a parent opts out and then contacts the center wanting to opt back in, Rahul can re-set the toggle to "Opted in" only after confirming with the parent — the platform shows a confirmation prompt: "Confirm that [Parent name] has re-consented to receive WhatsApp messages"

**Non-Functional Requirements:**
- Privacy: ⚠️ DPDPA — WhatsApp opt-in is consent to process personal data (mobile number) via Meta's platform; this consent must be stored with timestamp and method; must be deletable on data deletion request
- Compliance: Opt-in must be verifiable; the platform must not send a first WhatsApp message before opt-in is recorded (no "opt-in via first message" pattern — not permitted under WhatsApp Business API policy for India)

**Dependencies:**
- Blocked by: WA-001 (WABA connected), parent profile / child intake record
- Enables: WA-004, WA-005, WA-006, WA-007 (all message sending depends on opt-in check)

**Definition of Done:**
- [ ] All AC pass in QA
- [ ] STOP webhook suppression tested end-to-end with Meta test environment
- [ ] Opt-out suppression in delivery log tested
- [ ] Re-consent confirmation prompt tested
- [ ] Code reviewed and merged

---

### Story WA-004: Send appointment reminders via WhatsApp

**As a** Meena
**I want to** receive appointment reminders on WhatsApp — from the center's business number — rather than (or in addition to) SMS
**So that** I see the reminder in the same app I use to communicate with the center, on a number I recognize, and can easily reach out to reschedule if needed

**Inspired by:** Indian SMB clinic WhatsApp reminder patterns; WhatsApp Business API appointment reminder templates used by Practo and other Indian health platforms

**Context:** The reminder fires at T-24h and T-2h (same triggers as REMIND-001). If Rahul has selected WhatsApp as a reminder channel for this parent, the WhatsApp message fires instead of (or in addition to) SMS, using the approved WhatsApp appointment reminder template.

**Acceptance Criteria:**
- [ ] AC-01: Given a session reminder is due and the parent is opted in to WhatsApp, when the reminder job runs, a WhatsApp message is sent using the approved "Appointment Reminder" template
- [ ] AC-02: Given the WhatsApp message is sent, the delivery log shows: channel = WhatsApp, status = Sent / Delivered / Read (using WhatsApp delivery receipts)
- [ ] AC-03: Given Rahul's notification settings for a child are set to "WhatsApp only", when the reminder fires, only the WhatsApp message is sent (not SMS + WhatsApp)
- [ ] AC-04: Given the WhatsApp delivery status returns "Failed" (e.g., parent has not opened WhatsApp Business messages), the system falls back to SMS if an SMS number is on file, and logs the fallback
- [ ] AC-05: Given the parent is not opted in to WhatsApp, the reminder falls back to SMS/email as per REMIND-001 behavior

**Edge Cases & Error States:**
- [ ] EC-01: If the Meta API is unavailable when the reminder fires, the message is queued for retry (up to 3 retries over 30 minutes); if all retries fail, SMS fallback fires and the failure is logged
- [ ] EC-02: If the 24h WhatsApp reminder was delivered but the 2h reminder cannot be delivered (parent opts out between the two), only the 2h reminder is suppressed

**Non-Functional Requirements:**
- Performance: WhatsApp dispatch must complete within the same 5-minute window as SMS dispatch (REMIND-001 NFR)
- Privacy: ⚠️ DPDPA — template must not include clinical content; appointment logistics only

**Dependencies:**
- Blocked by: WA-001 (WABA), WA-002 (approved template), WA-003 (opt-in), REMIND-001 (shared reminder trigger infrastructure)
- Enables: Reduces friction vs. SMS-only; underpins Meena's perception that center communication is via WhatsApp

**Definition of Done:**
- [ ] All AC pass in QA with Meta test environment
- [ ] Read receipt in delivery log tested
- [ ] SMS fallback on WhatsApp failure tested
- [ ] Opt-out suppression tested
- [ ] Code reviewed and merged

---

### Story WA-005: Send payment link via WhatsApp

**As a** Rahul
**I want to** send a payment link to Meena via WhatsApp when a fee is due
**So that** Meena can tap the link and pay via UPI without me having to call her or have an awkward fee conversation

**Inspired by:** PractiPal UPI payment integration; Indian SMB WhatsApp payment link pattern; WhatsApp Business API payment message templates

**Context:** End of billing cycle. Rahul has generated an invoice. He wants to notify Meena via WhatsApp with the amount due and a link to pay. Done from the billing section of the platform, on Android or desktop.

**Acceptance Criteria:**
- [ ] AC-01: Given an invoice is generated for a family and the parent is opted in to WhatsApp, Rahul sees a "Send via WhatsApp" button on the invoice detail view
- [ ] AC-02: Given Rahul taps "Send via WhatsApp", the platform sends a WhatsApp message using the approved "Fee Due" template: "[Center name]: Your therapy fee of ₹[amount] is due by [date]. Pay here: [payment link]"
- [ ] AC-03: Given the payment link variable, the platform allows Rahul to configure a static UPI ID or a URL (e.g., center's Razorpay/Cashfree payment page) — actual UPI payment processing is NOT in scope for this story; the link is a configurable static field
- [ ] AC-04: Given the message is sent, the delivery log shows the entry with channel = WhatsApp and the invoice ID referenced
- [ ] AC-05: Given the parent is not opted in to WhatsApp, the "Send via WhatsApp" button is greyed out with tooltip "Parent has not opted in to WhatsApp messaging"

**Edge Cases & Error States:**
- [ ] EC-01: If the payment link field is blank (Rahul has not configured a UPI ID/payment URL), the message sends without the link and shows a note to Rahul: "Payment link not configured — message sent without link"
- [ ] EC-02: If the fee amount is ₹0 (waived), the "Send via WhatsApp" button is hidden

**Non-Functional Requirements:**
- Privacy: ⚠️ DPDPA — fee amount and family name are personal financial data; WhatsApp delivery routes through Meta's servers; parent must have opted in explicitly

**Dependencies:**
- Blocked by: WA-001, WA-002, WA-003, Invoice/billing flow (Cluster 5)
- Enables: Reduces Rahul's fee collection discomfort; increases on-time payment rate (assumed, not validated)

**Definition of Done:**
- [ ] All AC pass in QA
- [ ] Missing payment link fallback message tested
- [ ] ₹0 invoice button hidden tested
- [ ] Opted-out button state tested
- [ ] Code reviewed and merged

---

### Story WA-006: Send session summary via WhatsApp after session

**As a** Meena
**I want to** receive a brief session summary on WhatsApp after my child's therapy session — what was practiced, any key observations, what I should reinforce at home
**So that** I know what happened in the session without having to ask, and I have a simple guide for what to do at home that evening

**Inspired by:** Hi Rasmus parent portal (session summary delivery); structured post-session parent communication as a category best practice; Indian parent preference for WhatsApp-based updates (HYPOTHESIS)

**Context:** After Priya completes a session and writes a session note (session note feature is in a separate clinical cluster), Rahul or Dr. Sunita can trigger a WhatsApp summary to the parent. The summary is drawn from the session note — a structured excerpt, not the full clinical note.

**Acceptance Criteria:**
- [ ] AC-01: Given a session is marked Present and a session note exists for that session, Rahul or Dr. Sunita sees a "Send summary to parent via WhatsApp" button on the session detail view
- [ ] AC-02: Given the button is tapped, the platform auto-fills a summary message using the approved "Session Summary" template with: child name, session date, a configurable 1–3 line "What we practiced" field, and a configurable 1–2 line "Try at home" field — both editable by Dr. Sunita before sending
- [ ] AC-03: Given Dr. Sunita reviews and confirms the summary, the WhatsApp message is sent to the parent and logged in the delivery log with type "Session Summary"
- [ ] AC-04: Given the parent has not opted in to WhatsApp, the "Send summary" button is greyed out with tooltip "Parent has not opted in to WhatsApp messaging"
- [ ] AC-05: Given a summary has already been sent for a session, the button changes to "Resend summary" with a warning "A summary was already sent on [date/time] — send again?"

**Edge Cases & Error States:**
- [ ] EC-01: If the session note does not exist yet (Priya has marked attendance but not written a note), the "Send summary" button is visible but shows a warning: "Session note not complete — summary fields will be blank. Fill in manually before sending."
- [ ] EC-02: If the "What we practiced" and "Try at home" fields are both left blank, the system blocks sending: "Summary cannot be empty — at least one field must be filled before sending"

**Non-Functional Requirements:**
- Privacy: ⚠️ DPDPA — session summary is health data for a minor; WhatsApp delivery routes through Meta; opt-in required; template must not include diagnosis, detailed clinical targets, or trial data
- Compliance: Template must comply with WhatsApp policy — no clinical data in template body; summary is a general update, not a clinical record

**Dependencies:**
- Blocked by: WA-001, WA-002, WA-003, SCHED-004 (attendance mark Present), Session note feature (clinical cluster)
- Enables: Meena's engagement with home program; reduces parent WhatsApp messages asking "how did Arjun do today?"

**Definition of Done:**
- [ ] All AC pass in QA
- [ ] Empty fields block tested
- [ ] Resend warning tested
- [ ] Missing session note warning tested
- [ ] Code reviewed and merged

---

## Backlog: Epic 3 — WhatsApp Integration

| Story ID | Title | Persona | Complexity | Priority | Blocked by |
|---|---|---|---|---|---|
| WA-001 | Connect center's WhatsApp Business API account | Rahul | L | P0 | Meta Business account (external) |
| WA-002 | Manage approved WhatsApp message templates | Rahul | M | P0 | WA-001 |
| WA-003 | Collect and manage parent opt-in / opt-out | Rahul, Meena | M | P0 | WA-001, parent profile |
| WA-004 | Send appointment reminders via WhatsApp | Meena (recipient), Rahul | M | P0 | WA-001, WA-002, WA-003, REMIND-001 |
| WA-005 | Send payment link via WhatsApp | Rahul, Meena | M | P1 | WA-001, WA-002, WA-003, Billing cluster |
| WA-006 | Send session summary via WhatsApp | Meena (recipient), Dr. Sunita (triggers) | L | P1 | WA-001, WA-002, WA-003, SCHED-004, Session note feature |

---

## Cross-Epic Dependencies Summary

| Cluster dependency | Required by | Notes |
|---|---|---|
| Child record / intake flow | SCHED-001, WA-003 | Child must exist with parent contact before scheduling or messaging |
| Parent consent flow (DPDPA) | SCHED-001, WA-001, WA-003 | DPDPA consent for data processing must be in place before any PII is stored or transmitted |
| Therapist account creation | SCHED-001, SCHED-002 | Therapists must exist as users before availability can be set |
| Session note feature (clinical cluster) | WA-006 | Session summary depends on structured session note existing |
| Billing / invoice flow (Cluster 5) | REMIND-003, WA-005 | Fee reminders and payment links depend on invoice creation |
| SMS/email provider integration (Twilio / MSG91) | REMIND-001 | External provider; DLT registration required for India transactional SMS |
| Meta Business Manager account (external) | WA-001 | Center director must complete external setup; platform cannot do this for them |

---

## ⚠️ Feature Factory Disclaimer

These features were defined by competitive observation and category assumption —
not by validated user research. Before committing engineering capacity, a real
product thinker should ask:

**What we copied but haven't validated:**
- **Appointment Scheduling:** That Rahul and Priya currently manage scheduling through WhatsApp/paper and find it painful enough to switch to structured software; that therapist availability conflicts are a frequent enough problem to warrant enforcement logic (vs. manual coordination); that room/slot management is needed (relevant only for multi-room centers — many small Indian centers may have 1–2 rooms)
- **SMS/Email Reminders:** That the 39% → 3% no-show reduction from reminder research applies to Indian autism therapy families; that Indian parents read and respond to SMS reminders from unknown sender IDs; that Rahul would pay for SMS credit to send automated reminders rather than continuing to send manual WhatsApp messages for free
- **WhatsApp Integration:** That Indian therapy center directors are willing to set up a WhatsApp Business API account (this requires Facebook/Meta business verification — non-trivial for a small center); that parents will opt in to receiving WhatsApp messages from a business account rather than a personal number; that parents distinguish between "a robot message from the center's system" and "a real message from the center" positively rather than negatively

**What a researcher would ask before building this:**
- Do Indian autism therapy parents actually miss sessions because they forgot, or for other reasons (financial pressure, transport difficulty, child behavior)? If it's the latter, reminders won't move the needle on no-show rates.
- How do center directors currently handle rescheduling and cancellations? Is the current WhatsApp-based method experienced as painful, or is it "good enough" given the personal relationship with families?
- Have any Indian therapy centers tried WhatsApp Business API integration before? What happened — did parents engage with the business account messages, or did they continue messaging the center's personal WhatsApp number?
- What is Rahul's actual technical capacity to set up Meta Business Manager and a WABA account? Has he ever done anything comparable? Would the platform need a white-glove onboarding service for WABA setup?

**What the Product Consultant would challenge:**
- **Scope of Epic 3 (WhatsApp Integration) is high-risk for a v1:** WABA setup requires significant onboarding lift from the center director and external Meta verification. This is a feature that may have low adoption even if built correctly. Consider whether WhatsApp integration should be v2, with v1 using SMS/email reminders only and proving reminder value first.
- **Epic 1 (Scheduling) alone is a significant engineering investment** and overlaps with tools the Indian market already has (TherapEZ, PractiPal). If the product's core differentiation is clinical (Stages 3–6), scheduling should be scoped to the minimum viable version (recurring schedule, attendance mark, no-show trigger) and not over-engineered with room management and multi-filter calendars until adoption is proven.

**Risk level:**
- **Epic 1 — Appointment Scheduling:** Low–Medium risk. Table-stakes feature; not having it is a clear disadvantage. Risk is over-engineering before adoption is proven.
- **Epic 2 — SMS/Email Reminders:** Low–Medium risk. Table stakes in the US market; differentiator in India. Core value proposition (no-show reduction) is supported by research but Indian applicability is assumed, not confirmed.
- **Epic 3 — WhatsApp Integration:** High risk. Novel for structured therapy software in India. Both the setup path (WABA onboarding) and the user behavior assumption (parents opting in to business WhatsApp) are speculative. Build SMS first, validate, then add WhatsApp as a channel upgrade.

Use the `/researcher` agent to validate assumptions before sprint planning.
Use the `/product-consultant` agent to challenge scope and strategy — particularly on Epic 3 sequencing and Epic 1 depth.
