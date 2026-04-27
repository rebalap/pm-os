#  User Journey: Weekly Session Scheduling & Attendance Management

**Previously:** J6 | ✅ **IN SCOPE — MVP**
**Trigger:** Center director or admin sets up or reviews the weekly session schedule; sessions run and attendance is marked
**Primary actor:** Rahul (schedules and manages the calendar); Priya (marks attendance per session)
**Supporting actors:** Meena (receives pre-session reminders); Dr. Sunita (views session delivery for supervision and caseload oversight); System (sends automated reminders, updates billing records, triggers dropout risk flags)
**Entry condition:** Child record exists (EMR-001), DPDPA parental consent confirmed (EMR-002 / INT-003), therapist account created, at least one room configured (optional for single-room centers). For scheduling a new child: fee structure should ideally be configured (INV-001) before first session, so attendance marks immediately feed into billing.
**End state:** All sessions for the week are scheduled with assigned therapists and rooms; pre-session reminders sent to parents; attendance marked for each session (present/absent/no-show/cancelled); session records created; billing record updated; dropout risk signal generated for any no-shows.
**Journey source documents:**
- cluster-4-scheduling-communication.md — Stories SCHED-001 through SCHED-005, REMIND-001 through REMIND-004, WA-003 through WA-004
- cluster-3-billing-payments.md — Stories INV-002 (attendance feeds invoice), INV-001 (fee structure prerequisite)
- cluster-2-patient-records-intake.md — Stories MPM-001 through MPM-003 (staff assignment and caseload views)
- cluster-1-clinical-documentation.md — Story SNOTE-001 (session note attached after attendance mark), TMPL-003 (Priya views program on session screen)

---

## Discovery Context

**MVP Scope:** ✅ IN SCOPE — MVP

**Pain points & friction:**
- Scheduling managed in paper or Excel — no real-time visibility for staff or parents 🔵 Inferred
- Therapist assignment is verbal — coverage gaps appear when a therapist is absent and no contingency is documented 🔶 [HYPOTHESIS]
- Attendance marked on paper — data not available in real time for billing or dropout detection 🔵 Inferred
- No automated session reminder to parents — no-show rate is directly tied to reminder presence ✅ Psychiatric Services: 39% no-show without reminder vs. 3% with live contact
- Absence reason rarely captured — center cannot distinguish unavoidable absence from early-stage disengagement 🔶 [HYPOTHESIS]
- **Critical design constraint:** Attendance mark is the highest-frequency data entry action in the platform. Must be ≤ 2 taps on a low-end Android device and must function offline. ✅ Platform constraint defined in CLAUDE.md product context

**Emotional states:**
- Rahul: Schedule management is a daily operational overhead — managing changes, cancellations, and no-shows informally is a persistent context switch. 🔶 [HYPOTHESIS]
- Priya: Last-minute schedule changes and unclear therapist assignments disrupt session preparation. 🔶 [HYPOTHESIS]
- Meena: Absence of proactive appointment reminders increases missed sessions — WhatsApp-based reminder is expected but not guaranteed. 🔵 Inferred from no-show rate research

**Current workarounds:**
- WhatsApp group message used for daily schedule updates — informal, no audit trail 🔶 [HYPOTHESIS]
- Paper attendance registers serve as the billing source of truth at month end 🔵 Inferred
- Some centers send a WhatsApp reminder manually the day before each session 🔶 [HYPOTHESIS]

---

## Step-by-Step Flow

| Step | Actor | Action | Screen / State | Technical Note |
| --- | --- | --- | --- | --- |
| 1 | Rahul | Opens the Schedule tab. Reviews the current week's calendar — all therapists, children, and rooms in a time-grid view. | Center Calendar — Day/Week view (SCHED-005) | Reads: all session records for current week, therapist availability, room assignments. Default: Day view on today. Cached for offline viewing (up to 7 days). |
| 2 | Rahul | Creates a recurring weekly schedule for a new child (or modifies existing). Taps "Add Schedule" from child's profile. Enters: day(s) of week, start time, duration, assigned therapist (Priya), room. | Add Schedule form (SCHED-001) | Writes: recurring session series — 12 weeks forward from next occurrence. Conflict detection: checks therapist availability (SCHED-002) and room double-booking. Warns on any conflicting dates before save. |
| 3 | System | Sessions are auto-populated in the calendar for the next 12 weeks. Therapist conflict flags shown if applicable. | Center Calendar — updated with new sessions | Server-side write of session records (status = Scheduled) for all 12 weeks. Sessions are linked to child record, therapist ID, room ID. |
| 4 | Rahul | Reviews the full week calendar. Sees all active children's sessions displayed as color-coded cards. Each card shows: child name, therapist, room, time, status (Scheduled / Present / Absent / No-show / Cancelled). | Center Calendar — Week view (SCHED-005) | Reads: session records for the week. Calendar groups by therapist (default) or by room (configurable). Filter by therapist, child, or room available. |
| 5 | System | T-24 hours before each session: automated reminder sent to Meena (parent) via configured channel (SMS or WhatsApp). | Background — REMIND-001 trigger | Reads: session record (status = Scheduled or Confirmed), parent contact details, per-child reminder enable flag. Writes: delivery log entry. Uses DLT-registered SMS sender ID or WhatsApp Business API approved template. Message content: child name, date, time, center name — no clinical data. |
| 6 | System | T-2 hours before each session: second reminder sent to Meena. | Background — REMIND-001 (2h trigger) | Same infrastructure as Step 5. Separate template text for 2h reminder. If session is rescheduled after 24h reminder sent, a "Schedule change" message fires instead. |
| 7 | Meena | Receives WhatsApp or SMS reminder. Session is confirmed. Meena arrives at center with child. | Parent's phone — WhatsApp or SMS | No platform interaction from Meena required. Message is one-way (no two-way reply handling in scope). |
| 8 | Priya | Opens app on her Android phone. Sees "My Children" list (MPM-002) with today's sessions. Taps child's session card. | Priya's Home Screen → Session Card (MPM-002, SCHED-004) | Reads: assigned children list (RBAC-filtered — Priya sees only her assigned children). Session card shows: child name, time, room, current status. |
| 9 | Priya | Taps session card. Sees "Mark attendance" screen with four large tappable chips: Present / Absent / No-show / Cancelled. Taps "Present". Haptic feedback confirms. | Mark Attendance Screen (SCHED-004) | Writes: session status = Present, timestamp. ≤ 2 taps from home screen to confirmed mark. Haptic on confirmation (noisy environment). Write happens locally immediately (offline-first); syncs in background. |
| 10 | System | Session status = Present confirmed. Attendance record created. Billing module notified: one confirmed session for this child on this date. | Background — attendance → billing bridge | Writes: attendance confirmation event to billing queue. INV-002 job will read this at billing cycle end. Dr. Sunita's caseload dashboard (MPM-003) "Last session" field updated. |
| 11 | Priya | After session completes, opens the session detail and adds a session note (optional but encouraged). Taps "Add Note" on session detail screen. | Session Detail → Add Session Note (SNOTE-001) | Navigates to session note creation screen. Pre-fills: session date, therapist name, child's active program targets (TMPL-003 — Goals addressed multi-select). Priya completes note in ≤ 3 minutes. |
| 12 | Priya | Saves session note. Receives haptic confirmation. Returns to home screen. | Session Note saved (SNOTE-001) | Writes: session note record (status = Pending review) linked to session and child record. Offline save if no connectivity. Syncs to server; appears in Dr. Sunita's review queue (SNOTE-002) within 30 seconds of sync. |
| 13 | Dr. Sunita | Checks caseload dashboard (MPM-003) at end of day or next morning. Reviews sessions delivered, last session dates, and any pending session notes. | Supervisor Caseload Dashboard (MPM-003) | Reads: all children assigned to Dr. Sunita's supervision, last session date, last program update, overdue flags (session > 7 days, program update > 30 days). Filters by "Overdue flags only" or by therapist. |
| 14 | Rahul | Reviews center calendar at end of day. Sees final attendance status across all sessions. Any sessions still in "Scheduled" status at end of day are flagged for follow-up. | Center Calendar — Day view (SCHED-005) | Badge count on Priya's home screen also surfaces unmarked attendance (SCHED-004 AC-05). Rahul sees center-wide outstanding marks from his calendar view. |
| 15 | Rahul | For sessions marked "No-show" by Priya: automatic follow-up message fires within 30 minutes to parent (REMIND-002). | Background — REMIND-002 trigger | Reads: sessions with status = No-show. Writes: follow-up SMS sent; delivery log entry. Template: "[Child name] missed their session at [Center name] today. We hope everything is okay. Please contact us to reschedule: [center phone number]." |
| 16 | Rahul | If a session needs rescheduling (parent request, child sick, therapist emergency): opens session from calendar. Taps "Reschedule". Selects new date/time from therapist-filtered available slots. | Reschedule flow (SCHED-003) | Writes: old session status = Cancelled; new session created at new date/time. Parent notification queued (reschedule notification via configured channel). Conflict detection re-applied for new slot. |
| 17 | System | At end of week, Rahul's calendar shows a complete picture: all sessions with confirmed statuses. No-show count per child is a visible input to dropout risk monitoring (Journey 10). | Center Calendar — Week review | Reads: all session records for the week. No-show sessions with follow-up status visible. Dropout risk badge displayed if child has had 3+ no-shows in 30 days (REMIND-002 EC-02). |

---

## Decision Points

### Decision 1: Is the selected therapist available for the requested slot?
**At step:** 2 (schedule creation)
**Question:** Does the requested day/time/duration fall within Priya's configured working hours with no conflicts?
- **Path A — Available:** Session series created. → Continue at Step 3
- **Path B — Conflict with availability:** System displays warning listing specific conflicting dates in the series before save. Rahul can resolve individually (skip those dates, pick a different therapist, adjust time). Must resolve conflicts before saving the full series.
- **Path C — Room conflict:** Selected room already booked for one or more slots in the series. System shows which specific dates conflict. Rahul resolves per conflict before saving.

### Decision 2: Is the child a new child or an existing child with an existing schedule?
**At step:** 2 (schedule creation / modification)
**Question:** Does the child already have a recurring schedule in the system?
- **Path A — New child, no schedule:** Create new recurring series. → Continue at Step 2
- **Path B — Existing child, existing schedule:** Rahul modifies the schedule. System prompts: "Edit this session only / Edit all future sessions / Edit all sessions in the series." Choosing "all future sessions" creates a new series from the next occurrence; prior sessions are unmodified.

### Decision 3: Did Meena attend the session?
**At step:** 9 (attendance marking)
**Question:** What status does Priya mark for the session?
- **Path A — Present:** Session confirmed. Attendance record created. Billing record updated. Session note creation available (Step 11). → Continue at Step 10
- **Path B — Absent:** Session status = Absent. Billing record updated (absent session not billed per per-session plans; monthly flat is unaffected). No automatic follow-up message for "Absent" (follow-up is No-show only). Rahul can optionally follow up manually.
- **Path C — No-show:** Session status = No-show. Billing record updated (no-show not billed). Automatic follow-up message fires within 30 minutes (REMIND-002). Dropout risk counter incremented (3+ no-shows in 30 days → dropout risk badge). → Continue at Step 15
- **Path D — Cancelled:** Session status = Cancelled. Priya selects cancellation reason. No follow-up message. Billing: not counted. If parent-requested cancellation, no dropout risk signal. If recurring cancellation pattern, visible to Rahul in calendar view.
- **Path E (Edge case) — Priya forgets to mark attendance:** Session remains in "Scheduled" status. Badge count on Priya's home screen at end of day prompts unmarked sessions. Rahul sees unmarked sessions in his calendar view.

### Decision 4: Is there connectivity when Priya marks attendance?
**At step:** 9 (attendance marking — offline scenario)
**Question:** Does Priya have network connectivity in the session room?
- **Path A — Online:** Attendance writes to server immediately. Billing notification fired. Dr. Sunita's dashboard updated in real time.
- **Path B — Offline:** Attendance written locally immediately. Haptic confirmation still fires (offline-first). Syncs to server in background when connection restores. Billing and supervision systems updated after sync. No data loss.

### Decision 5: Does the session need to be rescheduled or cancelled?
**At step:** 16 (reschedule/cancel flow)
**Question:** Is this a one-time change or a change to the entire recurring series?
- **Path A — Single session rescheduled:** One session moved to new date/time. Rest of series unchanged. Parent notified. Conflict detection applied to new slot.
- **Path B — All future sessions cancelled:** Entire series from current session forward cancelled. Typically used when a child's schedule changes long-term or they go on hold.
- **Path C — Recurring series needs a permanent schedule change:** Rahul modifies the series (new days, new time, new therapist). "Edit all future sessions" creates a new series; previous sessions unaffected.

### Decision 6: Did the parent receive the pre-session reminder?
**At step:** 5–6 (reminder delivery)
**Question:** Was the reminder delivered successfully?
- **Path A — Delivered (SMS or WhatsApp):** Log shows Delivered status. No action needed.
- **Path B — Failed (invalid number, carrier rejected):** Logged as Failed in delivery log. Rahul sees flag in admin panel. Can retry manually or contact parent directly.
- **Path C — WhatsApp delivery failed, SMS fallback:** System auto-falls back to SMS if WhatsApp delivery fails and an SMS number is on file. Fallback attempt logged.
- **Path D — Session cancelled before reminder fires:** Reminder job checks session status before sending. If status = Cancelled, reminder is suppressed. Logged as "Suppressed — session cancelled."

---

## Screen Inventory

| Screen name | Purpose | Primary action | Personas who see it | Source story |
| --- | --- | --- | --- | --- |
| Center Calendar — Day view | Rahul's daily operational view of all sessions, therapists, rooms, attendance status | Tap session card → quick actions (mark / reschedule / cancel) | Rahul | SCHED-005 |
| Center Calendar — Week view | Rahul's weekly capacity and schedule overview | Switch view / apply filters | Rahul | SCHED-005 |
| Add Schedule form | Create a recurring weekly session series for a child | Tap "Save" to create recurring sessions | Rahul | SCHED-001 |
| Therapist Availability Settings | Configure working hours and blocked slots per therapist | Tap "Save" | Rahul | SCHED-002 |
| Reschedule / Cancel modal | Reschedule session to a new slot or cancel with a reason | Tap "Confirm reschedule" or "Confirm cancel" | Rahul, Priya | SCHED-003 |
| Priya's Home Screen — My Sessions | Priya's daily view of sessions assigned to her | Tap session card | Priya | MPM-002, SCHED-004 |
| Mark Attendance Screen | Priya marks a session as Present / Absent / No-show / Cancelled | Tap attendance chip (≤ 2 taps from home) | Priya | SCHED-004 |
| Session Detail Screen | View session metadata; quick-access to session note and program | Tap "Add Note" / "View Program" | Priya, Rahul, Dr. Sunita | SCHED-004, SNOTE-001 |
| Session Note creation screen | Priya writes post-session note after marking Present | Tap "Save" | Priya | SNOTE-001 |
| Supervisor Caseload Dashboard | Dr. Sunita's overview of all children under supervision | Filter by overdue flags / by therapist | Dr. Sunita | MPM-003 |
| Settings > Reminders | Edit reminder templates (24h, 2h, no-show follow-up), enable/disable per channel | Tap "Save template" | Rahul | REMIND-004 |
| Reminder Delivery Log | Audit log of all reminders sent — delivery status per message | Tap "Retry" on failed messages | Rahul | REMIND-005 |

---

## Designer Handoff

### Screen: Center Calendar — Day View (Rahul)

**Purpose:** Give Rahul a real-time operational view of every session happening today — who is seeing whom, in which room, and whether they've arrived.
**Primary action:** Tap a session card to open its bottom sheet with quick actions.
**Entry point(s):** Bottom nav "Schedule" tab → defaults to Day view for today.
**Exit point(s):** Tap session card → bottom sheet with actions (Mark attendance / Reschedule / Cancel); tap "Add Session" FAB → Add Schedule form.

**Key components:**
- Time grid: Vertical axis = time of day (7AM–7PM, scrollable). Horizontal axis = therapist columns (or room columns — configurable). Each session displayed as a colored block within the grid.
- Session card (within grid): Child first name, time, room name, status indicator (color + text label). Minimum height: 44px for touch target.
- Status legend: Persistent at top of screen. Color + text: White/Outlined = Scheduled, Green = Present, Amber = Absent, Red = No-show, Grey = Cancelled.
- Filter chip row (below legend): "All" / by therapist name / by room — horizontal scroll row, each chip ≥ 44px.
- Day navigation: Swipe left/right or arrow buttons to move between days. Date shown prominently.
- "Week" toggle: Switches to Week view.

**States:**
- **Empty state:** "No sessions scheduled for [date]." + "Add Session" button.
- **Loading state:** Skeleton blocks in the grid while data fetches. Show "Last synced [time]" banner.
- **Error state:** "Could not load schedule. Pull to refresh." Grid shows cached data with a staleness banner.
- **Offline state:** Cached schedule for up to 7 days shown with "Offline — last synced [date/time]" banner. New session creation and rescheduling blocked offline. Attendance marking allowed offline (writes locally).

**Constraints:**
- Must be usable one-handed on a 5.5–6.5 inch Android screen.
- Session cards in the grid must be large enough to read child name + time without tapping — minimum readable font size 12px even in a dense schedule.
- If >10 therapists: switch to list-per-therapist accordion layout rather than exceeding screen width with columns.
- Status indicators: always text + color. Never color alone.

---

### Screen: Mark Attendance Screen (Priya)

**Purpose:** Let Priya confirm or deny a child's session attendance with a single clear tap — ideally without looking away from the child for more than 2 seconds.
**Primary action:** Tap an attendance chip (Present / Absent / No-show / Cancelled). Exactly 1 tap after arriving at this screen.
**Entry point(s):** Priya taps a session card from her home screen "My Sessions" view. ≤ 2 taps from home to this screen.
**Exit point(s):** Tap chip → haptic confirmation → return to session detail (or prompt to add session note if "Present" selected).

**Key components:**
- Session context banner: Child name, session time, therapist name. Read-only. Small, top of screen.
- Attendance chips: 4 large chips arranged in a 2×2 grid (or vertical stack if screen is narrow). Each chip: label text (≥18px), icon, distinctive color. Chips are the dominant UI element — fill most of the screen.
  - Present: Green background
  - Absent: Amber background
  - No-show: Orange background
  - Cancelled: Grey background
  - All chips: text label alongside color. Touch targets: full chip width/height, minimum 88px height each.
- Confirmation feedback: On tap — immediate haptic pulse; chip fills/highlights; "Saved" banner appears for 1.5 seconds.
- "Add Note" prompt: After marking "Present", a non-blocking prompt appears: "Session marked. Add a session note?" with "Add Note" and "Skip" buttons. Dismissable.

**States:**
- **Already marked state:** If session already has a status, screen shows the current status with "Change attendance" option. Does not allow change if session was marked by a user with higher privileges than Priya (EC-02 of SCHED-004).
- **Loading state:** Brief spinner (< 1 second) while session context loads. Should be near-instant from cache.
- **Error state:** If save fails: "Could not save attendance. Try again." Chip reverts to unselected state. No data loss.
- **Offline state:** Chip tap writes to local storage immediately. "Saved offline — will sync when connected" banner. Haptic still fires. The offline-first write is the primary behavior, not a fallback.

**Constraints:**
- This screen must function in a noisy environment with one hand. No scrolling should be required to see all 4 chips.
- Haptic feedback is mandatory — do not use audio-only confirmation.
- ≤ 2 taps from home screen: (1) tap session card from My Sessions, (2) tap attendance chip. This path must be QA-verified on physical device.
- Touch targets: each chip minimum 88px height (extra large — exceeds 44px minimum — to ensure one-handed accuracy while managing an active child).

---

### Screen: Priya's Home Screen — My Sessions

**Purpose:** Give Priya her personal daily session list — only her assigned children, only today's sessions — so she can see what's next without navigating through records that aren't hers.
**Primary action:** Tap a session card to open Mark Attendance Screen (or Session Detail if attendance already marked).
**Entry point(s):** App launch or home screen — this is Priya's default view after login.
**Exit point(s):** Tap session card → Mark Attendance Screen; tap child name → child's session detail.

**Key components:**
- Date header: Today's date, prominent. "Today" label.
- Session list: Chronological. Each card shows: child first name, session time, room (if applicable), status chip (Scheduled / Present / Absent / No-show / Cancelled).
- Unmarked attendance badge: If any sessions are past their start time and still in "Scheduled" status, a persistent orange banner appears: "X sessions need attendance marked." Tap → filters list to unmarked sessions.
- "My Children" quick-access row: Horizontally scrollable row of assigned child avatars/initials at top. Tap to navigate to a child's full record.

**States:**
- **Empty state:** "No sessions for you today." + "View this week" link.
- **Loading state:** Skeleton cards while list loads. Should load within 2 seconds on 4G; from cache offline.
- **Error state:** "Could not load your sessions. Pull to refresh." Show cached sessions if available.
- **Offline state:** Cached session list shown. Attendance marking works offline (writes locally). Banner: "Offline — attendance changes will sync when connected."

**Constraints:**
- This is Priya's primary daily workflow screen. It must be the first thing she sees after login — not a generic dashboard with billing data, supervisor tools, or admin settings.
- Child names shown as first names only (or initials if privacy mode enabled — configurable by Rahul).
- Color-coded status on session cards: always text label + color. Never color alone.

---

### Screen: Add Schedule Form (Rahul)

**Purpose:** Let Rahul create a recurring weekly therapy schedule for a child by specifying day(s), time, duration, therapist, and room.
**Primary action:** Tap "Save" to create the recurring session series.
**Entry point(s):** Tap "+ Add Schedule" from a child's profile, or tap "+" FAB on the center calendar.
**Exit point(s):** Tap "Save" → recurring series created; returns to calendar (new sessions visible). Tap "Cancel" → discards form; returns to previous screen.

**Key components:**
- Day selector: Multi-select checkboxes for Mon–Sun. Most common selection: 2–3 days.
- Time picker: Start time. Duration dropdown (30 min / 45 min / 60 min / 90 min / custom).
- Therapist picker: Single select from active therapist list. Filtered by availability for the selected time slot.
- Room picker: Optional (required only if center has rooms configured). Single select.
- Series preview: "This schedule will create X sessions over 12 weeks starting [date]." — updates live as fields change.
- Conflict summary: If any slots in the series conflict, a red-bordered summary shows conflicting dates. Rahul must resolve before saving.

**States:**
- **Empty state (fresh form):** All fields blank. Day selector shows Mon–Sun with none selected. Helpful placeholder text.
- **Loading state:** Conflict detection runs on field change — show a micro-spinner in the conflict area while checking.
- **Error state (conflict):** Conflict details shown inline. Save button disabled until conflicts resolved.
- **Offline state:** Form can be filled offline. "Saved locally — will sync when connected" on save. Conflict detection requires connectivity (cannot check therapist availability offline).

**Constraints:**
- Conflict warnings must be specific — "Priya is not available on these 3 dates: [list]" — not a generic "conflict detected."
- For single-room centers: room picker is optional and can be hidden by Rahul in Settings.

---

### Screen: Supervisor Caseload Dashboard (Dr. Sunita)

**Purpose:** Give Dr. Sunita a glanceable oversight of her entire caseload — who was seen recently, whose program is overdue for an update, and which children may need her attention.
**Primary action:** Tap a child row to open their clinical record (lands on Program/Data tab, not Profile tab).
**Entry point(s):** Bottom nav or sidebar "Caseload" or "Supervision" tab.
**Exit point(s):** Tap child row → child's clinical record (Program/Data tab). Tap filter → filtered view.

**Key components:**
- Caseload summary bar: Total children supervised (N), children with overdue flags (N). Prominent at top.
- "Overdue flags only" toggle: Filter chip. When active, list shows only flagged children.
- Child rows: Child name, assigned Primary Therapist, date of last session ("X days ago"), date of last program update ("X days ago"), flag indicator (one or more colored flags for overdue conditions).
- Flag types: Session overdue (no session in >7 days), Program overdue (no program update in >30 days). Both configurable by Rahul in Settings.
- "Filter by Therapist" control: Dropdown. Shows only children assigned to selected therapist.

**States:**
- **Empty state:** "No children are currently assigned to your supervision. Contact your center director."
- **Loading state:** Skeleton rows (5 rows) while data fetches.
- **Error state:** "Could not load caseload. Pull to refresh." Cached data shown if available.
- **Offline state:** Dashboard readable from cached data. Staleness timestamp shown. Flag calculations based on last-synced session data.

**Constraints:**
- This screen must be usable on a mid-range Android phone — not desktop-only.
- Overdue flags: text labels ("No session in 8 days") alongside color indicators. Never color alone.
- Date format: Prefer "3 days ago" / "2 weeks ago" over absolute dates — more glanceable for a caseload view.

---

## Developer Handoff

### Step-level technical summary

| Step | Data written | Data read | API / event | Offline behavior | Regulatory gate |
| --- | --- | --- | --- | --- | --- |
| 1 | None (read-only) | Session records for current week, therapist availability, room assignments | `GET /schedule/week?date=[YYYY-MM-DD]` | Cached response; up to 7 days of schedule cached locally | RBAC: Rahul sees all; Priya sees only assigned children |
| 2 | Recurring session series (12 sessions × selected days, status = Scheduled) | Therapist availability, room bookings for conflict detection | `POST /schedules/recurring` | Queues locally if offline; syncs on restore; conflict detection requires connectivity | ⚠️ DPDPA — session data for a minor; consent must be Active |
| 3 | Session records (one per occurrence) | None | Part of Step 2 POST response | N/A (server creates records on sync) | DPDPA consent check per child |
| 5–6 | Delivery log entry (type, channel, timestamp, status) | Session records (status check before send), parent contact, per-child enable flag, reminder templates | `POST /reminders/pre-session-job` — cron triggered at T-24h and T-2h | Server-side only; cannot send offline | ⚠️ DPDPA — parent contact data processed; message must not include clinical data; TRAI DLT sender ID for SMS |
| 8 | None (read-only) | Priya's assigned children, today's sessions | `GET /my-sessions?date=today` | Cached list; offline-available | RBAC: Priya sees only assigned children (caseload scope) |
| 9 | Session status = Present (or Absent / No-show / Cancelled); attendance timestamp | Session record | `PATCH /sessions/{id}/attendance` | Write locally immediately; sync in background; haptic fires offline | ⚠️ DPDPA — attendance is health-adjacent data; stored encrypted; access scoped to assigned staff + admin |
| 10 | Attendance confirmation event to billing queue | Session record (newly = Present) | Event: `attendance.confirmed` → billing queue | Event queued locally; fires on sync | None (billing system picks up event; consent already checked) |
| 11–12 | Session note record (status = Pending review) | Session record, child's active program targets | `POST /session-notes` | Write locally; sync on restore; session note survives app close | ⚠️ DPDPA — session note is child health data; consent must be Active |
| 13 | None (read-only) | All supervised children, last session date, last program update date, overdue thresholds | `GET /caseload/supervisor?supervisor_id=[id]` | Cached response; staleness shown | RBAC: Supervisor sees only assigned caseload |
| 15 | Delivery log entry (type = No-show follow-up) | Session record (status = No-show), parent contact, 30-min trigger timestamp | `POST /reminders/no-show-follow-up-job` — event triggered by No-show status write | Server-side; cannot send offline | DPDPA: message must not reference clinical content; "missed session" only |
| 16 | Old session status = Cancelled; new session record at new date/time | Therapist availability, room availability for new slot | `POST /sessions/{id}/reschedule` | Queues locally; syncs on restore; conflict detection requires connectivity | DPDPA: cancellation reason may be health-adjacent; stored with access control |

**Key state transitions:**
- Session transitions from `Scheduled` → `Present` / `Absent` / `No-show` / `Cancelled` at Step 9
- Session transitions from `Scheduled` → `Cancelled` + new session `Scheduled` at Step 16 (reschedule)
- No-show counter per child increments at Step 9 when status = No-show; triggers dropout risk badge at count ≥ 3 in rolling 30 days

**Background jobs / async events triggered by this journey:**
- `pre-session-reminder-job`: Cron, runs every 30 minutes. Checks for sessions with start time in next 24h or 2h. Dispatches SMS/WhatsApp reminders for sessions not yet reminded. Skips cancelled or rescheduled sessions.
- `no-show-follow-up-job`: Event-triggered by `session.status.updated` to No-show. 30-minute delay before firing. Cancellable if status changes back to Present within the delay window.
- `attendance-billing-event-handler`: Event-triggered by `attendance.confirmed`. Pushes attendance record to billing queue for INV-002 consumption at billing cycle end.
- `overdue-flag-job`: Cron, daily. Recalculates overdue flags for all children (last session > N days, last program update > N days). Updates caseload dashboard data.

**DPDPA compliance checkpoints:**
- Step 2: ⚠️ DPDPA — creating a session record for a minor requires Active consent on their record; `POST /schedules/recurring` must check `consent_status = Active` before writing
- Step 5–6: ⚠️ DPDPA — reminder messages transmit parent contact details to SMS/WhatsApp infrastructure; message body must contain only logistics (name, date, time, center name) — no clinical data; TRAI DLT sender ID registration required for transactional SMS
- Step 9: ⚠️ DPDPA — attendance record is health-adjacent data; encrypted at rest; access scoped by RBAC; audit log on write
- Step 12: ⚠️ DPDPA — session note contains clinical content for a minor; DPDPA consent Active required; encrypted at rest; note accessible only to assigned staff + supervisor + admin

---

## Cross-Journey Dependencies

| Depends on journey | Why | What breaks if missing |
| --- | --- | --- |
| Journey 9 — Monthly Billing, Invoicing & UPI Payment Collection | Attendance marks (SCHED-004, Step 9) are the input data for INV-002 (invoice auto-generation). Each confirmed "Present" attendance feeds the billing engine. | If attendance is not captured digitally, the core billing differentiator (attendance-driven auto-invoicing) cannot function. Rahul must manually count sessions for invoices — removes primary value over PractiPal. |
| Journey 10 — Missed Session Detection, Dropout Prevention | No-show status marks (from this journey, Step 9) are the primary trigger for Journey 10. The dropout risk badge (3+ no-shows in 30 days) and the initial follow-up message (REMIND-002, Step 15) are initiated here. | Without attendance marking in this journey, Journey 10 has no trigger. Dropout detection is invisible until it has already happened. |
| Intake & Enrollment (EMR-001, EMR-002, INT-003) | DPDPA parental consent must be Active before any session record is created or attendance data is written. Child record must exist before a schedule can be attached. | Cannot schedule sessions for a child without an existing record. Cannot write attendance data without confirmed consent — creates DPDPA compliance risk if this gate is bypassed. |
| Staff assignment (MPM-001, MPM-002) | Priya sees only her assigned children in the "My Sessions" view. Therapist assignment is required for conflict detection in scheduling. | Without assignment, Priya sees all children (privacy violation) or no children (usability failure). Conflict detection in scheduling cannot work without therapist availability records. |
| Clinical documentation (SNOTE-001, TMPL-003) | After marking attendance as Present (Step 9), Priya is prompted to add a session note (Step 11). The "Goals addressed" field in the session note references the child's active therapy program (TMPL-003). | Without the session note prompt, clinical documentation happens less consistently. Without the active program reference, Priya cannot quickly confirm what targets to document against — reduces note quality and clinical continuity. |

---

## ⚠️ Feature Factory Disclaimer

These flows were defined by competitive observation (Jane App, SimplePractice, CentralReach, TherapEZ) and document synthesis — not by validated user research. Before committing engineering capacity, a real product thinker should ask:

**What we assumed but haven't validated:**
- [ASSUMPTION] Rahul currently manages scheduling through WhatsApp and paper, and finds it painful enough to adopt structured scheduling software. Whether scheduling complexity is a felt pain point or a "good enough" WhatsApp workflow has not been confirmed in primary research.
- [ASSUMPTION] Priya can and will mark attendance on her Android phone during or immediately after a live session with an active child. The cognitive load of switching to a phone while managing a child's session may make even a 2-tap action feel disruptive. The one-handed, haptic-only design is meant to minimize this — but its effectiveness with actual therapists in actual Indian therapy session rooms has not been tested.
- [ASSUMPTION] Automated SMS reminders will reduce no-show rates at Indian autism therapy centers. The 39% → 3% no-show reduction data is from a US psychiatric outpatient context (Psychiatric Services study). Indian autism therapy families may miss sessions for different reasons (transport, financial pressure, caregiver exhaustion) where a reminder text has no effect.
- [ASSUMPTION] Indian therapy centers have rooms that need conflict management. Many small centers may have only 1–2 rooms, making the room conflict feature irrelevant. Over-engineering this for a single-room center adds setup friction with no payoff.
- [ASSUMPTION] WhatsApp Business API reminders will be welcomed by parents as "official center communications" rather than perceived as impersonal automated messages. The WABA setup burden for Rahul (Meta Business verification, dedicated business number) is non-trivial.

**What a researcher would ask before building this:**
- Does Priya currently record any attendance at all during sessions — on paper, on her phone? What would interrupt her flow the least?
- Why do families miss sessions in Indian autism therapy centers? Is it forgetfulness (addressable with reminders), transport, financial pressure, or child behavior? The intervention needs to match the actual cause.
- How does Rahul currently handle scheduling conflicts when two families want the same slot? Is it a real pain point or something he handles with a quick WhatsApp message?

**What the Product Consultant would challenge:**
- Epic 1 (Scheduling) is a significant engineering investment that overlaps with tools the Indian market already has. If the product's core differentiation is clinical (in-session data collection, supervision, reporting), scheduling should be scoped to the minimum viable version — recurring schedule creation, attendance mark, no-show trigger — and not over-engineered with room management, multi-filter calendars, and SCHED-002 availability enforcement until adoption is proven.
- The ≤ 2-tap attendance mark constraint (SCHED-004) is the single most important UX requirement in this journey. Everything else can be Phase 2. Validate the tap count and in-session usability with 3–5 therapists before building the full scheduling module.

**Risk level:**
- Recurring schedule creation (SCHED-001): Low — table stakes; structural need clear
- Attendance marking (SCHED-004): Low-Medium — core workflow; key constraint is in-session UX, not feature design
- Therapist availability and room management (SCHED-002, SCHED-003): Medium — likely over-engineered for small centers at v1
- Automated SMS reminders (REMIND-001, REMIND-002): Low-Medium — differentiator in India; no-show reduction effect on Indian autism families is assumed not confirmed
- WhatsApp Business API reminders (WA-004): High — setup burden and parent behavior assumptions unvalidated

Use the `/researcher` agent to validate attendance marking behavior and no-show root causes before sprint planning.
Use the `/product-consultant` agent to challenge the scheduling feature scope and define the true MVP before committing engineering capacity.
