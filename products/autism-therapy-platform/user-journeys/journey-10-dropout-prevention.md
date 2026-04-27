# User Journey: Appointment Follow-Up & Dropout Prevention

**Previously:** J7 | ✅ **IN SCOPE — MVP**
**Trigger:** A child misses a scheduled session (attendance marked No-show by Priya) OR a child has not attended for 2+ consecutive sessions (system detects pattern)
**Primary actor:** Rahul (receives alert and initiates or oversees follow-up)
**Supporting actors:** Priya (marks absence that triggers detection); Meena (receives follow-up outreach); System (auto-detects pattern, surfaces alert, dispatches initial follow-up message); Dr. Sunita (sees dropout risk in caseload dashboard, may participate in clinical re-assessment if child returns)
**Entry condition:** At least one session exists for the child (SCHED-001 complete). Attendance has been marked as No-show or the system has detected 2+ consecutive missed sessions. The child's record is active (not already marked Discharged or On Hold).
**End state:** Missed session documented; parent contacted via WhatsApp or SMS; session either rescheduled or family status updated (At Risk / On Hold / Discharged); dropout risk flag visible in Rahul's center director dashboard and Dr. Sunita's caseload dashboard.
**Journey source documents:**
- cluster-4-scheduling-communication.md — Stories SCHED-004 (attendance → no-show), SCHED-005 (calendar view — dropout risk visibility), REMIND-002 (no-show follow-up), WA-002 (template management), WA-004 (WhatsApp reminder delivery), WA-005 (payment link in follow-up)
- cluster-3-billing-payments.md — Stories INV-002 (attendance gap affects billing), INV-005 (overdue reminders intersect with dropout)
- cluster-2-patient-records-intake.md — Stories MPM-003 (Dr. Sunita caseload — last session date flag), MPM-005 (Rahul full caseload — sort by last session to surface at-risk families)
- journey-map.md — Journey 10: Appointment Follow-up & Dropout Prevention; Break points BP-05, BP-10; Hypotheses H-10, H-18

---

## Discovery Context

**MVP Scope:** ✅ IN SCOPE — MVP

### Pain Points & Friction

- No systematic attendance tracking — dropout is invisible until it has already happened 🔵 Inferred
- Single WhatsApp message is insufficient as a dropout intervention — evidence suggests live contact reduces no-shows dramatically ✅ Psychiatric Services: 3% no-show with live call vs. 39% with no reminder
- Dropout driven by financial pressure and caregiver exhaustion — not addressable by reminders alone ✅ Tandfonline 2025 and PMC research on caregiver burden
- No structured re-engagement protocol: what happens if a family returns after a gap? Does the program need updating? 🔶 [HYPOTHESIS]

### Emotional States

- **Meena (if dropping out):** Exhausted, financially strained, possibly ashamed. "Invisible exit" — she may simply stop responding to WhatsApp messages. ✅ Tandfonline 2025 — "invisible exits" is a documented phenomenon in Indian autism care
- **Rahul:** Dropout feels inevitable rather than preventable — because there's no system to surface it early 🔶 [HYPOTHESIS]
- **Dr. Sunita:** May not be aware a child has dropped out until the schedule reveals a persistent gap 🔶 [HYPOTHESIS]

### Current Workarounds

- Staff informally "check in" on families they're close to — relationship-based retention only 🔶 [HYPOTHESIS]
- Some centers WhatsApp parent groups where community pressure informally encourages continued attendance 🔶 [HYPOTHESIS]

### Evidence Highlight

The no-show rate finding is the sharpest evidence point in the research: 39% no-show without any reminder vs. 3% with live contact. ✅ Psychiatric Services study.

---

## Journey Map Context

This journey directly addresses Journey 10 of the therapy center lifecycle: the "invisible exit" pattern documented in the journey map. Key documented behaviors:

- Families go quiet and dropout is detected only weeks later (journey map Journey 10, Step 5)
- A single WhatsApp message is the only current intervention when a child misses a session (H-10)
- No systematic attendance tracking exists — dropout is invisible until it has fully happened (BP-05)
- Dropout is driven by financial pressure, caregiver exhaustion, and transport difficulty — not always forgetfulness (Tandfonline 2025)
- 39% no-show rate without reminders vs. 3% with live contact (Psychiatric Services) — but Indian context is unvalidated

The product can only address the detection and communication layer. It cannot resolve financial pressure or caregiver exhaustion. This journey must not over-promise what a notification system can do.

---

## Step-by-Step Flow

| Step | Actor | Action | Screen / State | Technical Note |
|---|---|---|---|---|
| 1 | Priya | Marks session as "No-show" for a child who did not arrive. (This is the primary trigger for single-missed-session detection.) | Mark Attendance Screen — taps "No-show" chip (SCHED-004) | Writes: session status = No-show; timestamp; Priya's user ID. Offline-first write. No-show event emitted to dropout risk service. Haptic confirmation fires. |
| 2 | System | No-show event received. Dropout risk counter for this child incremented. 30-minute delayed follow-up message job queued. | Background — event handler + delayed job | Reads: no-show history for this child (rolling 30-day window). Writes: no-show counter updated; follow-up job queued with 30-minute delay. |
| 3 | System | After 30-minute delay: checks session status (if Priya re-marked to Present in the interim, job is cancelled). If still No-show: sends automated follow-up SMS or WhatsApp to Meena. | Background — REMIND-002 triggered | Reads: session status (re-check before send), parent contact number, per-family remind enable flag, WhatsApp opt-in status. Writes: delivery log entry (type = No-show follow-up). Template (editable by Rahul): "[Child name] missed their session at [Center name] today. We hope everything is okay. Please contact us to reschedule: [center phone number]." — No clinical data in message. |
| 4 | Meena | Receives WhatsApp or SMS message. May respond via WhatsApp to center's personal number (outside platform), or may not respond at all. | Meena's phone — WhatsApp or SMS | Platform sends message. Platform does not handle inbound WhatsApp replies (out of scope for v1). Delivery status (Sent / Delivered / Read) logged in delivery log. |
| 5 | Rahul | Reviews center calendar or center director dashboard. Sees No-show indicator on the session card. Sees dropout risk badge on child's record if 3+ no-shows in 30 days. | Center Calendar (SCHED-005) + Center Director Caseload (MPM-005) | Reads: session statuses; no-show counter per child. Dropout risk badge appears when no-show count ≥ 3 in rolling 30-day window. MPM-005 "Sort by Last Session" surfaces children with longest absence first. |
| 6 | System | Parallel detection path: System runs daily attendance pattern scan. Flags any child who has not attended for 2+ consecutive scheduled sessions (regardless of whether each was marked No-show or simply remained Scheduled/unmarked). | Background — attendance gap detection job (daily cron) | Reads: session records for all active children — compares scheduled sessions vs. confirmed attendance. Flags children with ≥ 2 consecutive sessions in non-Present status (No-show, Absent, or unmarked after session time has passed). |
| 7 | Rahul | Receives in-app notification (or sees badge on dashboard): "[Child name] has missed [N] consecutive sessions. Last attended: [date]." | In-app notification + Center Director Dashboard | Writes: dropout risk alert record linked to child. Dashboard shows alert badge. Notification is actionable — tap to open child's attendance history. |
| 8 | Rahul | Opens child's attendance history. Reviews recent session pattern: how many sessions scheduled, how many attended, no-show vs. absent vs. cancelled breakdown. | Child's Session History Screen (SCHED-005 → child record → Sessions tab) | Reads: all session records for this child, sorted by date descending. Filters available: last 30 days / last 90 days / all time. Shows each session's status, therapist, date. |
| 9 | Rahul | Decides on follow-up action. Options: (A) Send manual WhatsApp message directly from platform; (B) generate a UPI payment link to include in follow-up (if outstanding fees are also a factor); (C) call the family directly (outside platform); (D) update child's enrollment status to "On Hold" or flag as "At Risk." | Action selection — from child's profile | This is a decision point (see Decision Points below). Platform surfaces the options; Rahul chooses. |
| 10A | Rahul | Sends a manual follow-up WhatsApp message via platform using an approved template. Optionally includes a UPI payment link if outstanding fees exist. | WA-005 (payment link) / WA-004 flow | Reads: parent opt-in, approved templates. Writes: delivery log entry. Message is one-way. If fees are outstanding, WA-005 payment link included in message (configurable). |
| 10B | Rahul | Updates child's enrollment status to "At Risk" or "On Hold" in the child's profile. Adds an internal note on why. | Child Profile — Enrollment Status field | Writes: enrollment_status = At_Risk or On_Hold; internal note record (visible to Rahul, Dr. Sunita — not to Priya or parent). Status visible in center director caseload overview (MPM-005). |
| 11 | Meena | Responds to follow-up (outside platform — via personal WhatsApp or phone call). Explains reason for absence. Rahul records outcome. | Rahul's phone — personal WhatsApp (external to platform) | Platform cannot capture inbound WhatsApp responses (v1). Rahul manually updates the child's record with the outcome of the conversation (internal note). |
| 12 | Rahul | If session is to be rescheduled: opens child's schedule and creates a new session or reschedules the missed one (SCHED-003). | Reschedule flow (SCHED-003) | Writes: new session record. Parent notification queued via configured reminder channel. |
| 13 | Rahul | If family confirms they are discontinuing: updates child's enrollment status to "Discharged" with a reason code (Family withdrew / Financial / No contact / Transferred / Clinical graduation). | Child Profile — Enrollment Status | Writes: enrollment_status = Discharged; discharge_reason; discharge_date. Child removed from active session schedule (sessions beyond discharge date cancelled). Child moves off Priya's My Children list and Dr. Sunita's caseload. |
| 14 | Dr. Sunita | Reviews caseload dashboard. Sees dropout risk flags on children assigned to her supervision. Opens child records as needed. May decide a returning child needs a program review or clinical re-assessment before sessions resume. | Supervisor Caseload Dashboard (MPM-003) | Reads: caseload data including last session date, dropout risk flags. Overdue flags (session > 7 days) fire for children with gaps. Dr. Sunita can add a SOAP note or initiate a program review for returning children. |
| 15 | System | Ongoing: Daily attendance pattern scan continues. If a child's status was updated to "At Risk" and they return to regular attendance, risk flag is downgraded automatically after 4 consecutive attended sessions. | Background — risk resolution job | Reads: recent attendance for "At Risk" children. Writes: dropout risk level updated. Notification to Rahul: "[Child name] has attended 4 consecutive sessions. Dropout risk flag cleared." |

---

## Decision Points

### Decision 1: Was the no-show mark a data entry error?
**At step:** 2–3 (30-minute delay before follow-up fires)
**Question:** Does Priya change the attendance status from No-show to Present within 30 minutes (child arrived late)?
- **Path A — Status remains No-show after 30 minutes:** Follow-up message fires. → Continue at Step 3
- **Path B — Status changed to Present within 30 minutes:** Queued follow-up job is cancelled. No message sent to Meena. Dropdown risk counter is decremented (the no-show was erroneous). Delivery log shows "Suppressed — attendance re-marked."
- **Path C — Status changed to Absent (child did not attend, but parent communicated in advance):** Follow-up job is also cancelled (follow-up is No-show specific — Absent means the absence was anticipated). No automatic message sent.

### Decision 2: Is this an isolated missed session or a pattern?
**At step:** 5–7 (dropout risk evaluation)
**Question:** How many no-shows / consecutive absences does this child have in the last 30 days?
- **Path A — First or second no-show (count < 3 in 30 days):** Single follow-up message sent (Step 3). Dropout risk badge not yet displayed. Rahul sees the no-show on the calendar but no special alert.
- **Path B — Third or subsequent no-show (count ≥ 3 in 30 days):** Dropout risk badge appears on child's record in Rahul's dashboard and Dr. Sunita's caseload. Rahul receives in-app alert. More urgent action expected. → Continue at Step 7
- **Path C — 2+ consecutive sessions missed (detected by daily scan):** System generates proactive alert regardless of total count. This catches cases where attendance was marked Absent or simply not marked, not just No-show. → Continue at Step 7

### Decision 3: What is the reason for the absence?
**At step:** 9–11 (Rahul's follow-up decision)
**Question:** When Rahul or Meena communicates the reason, what category does it fall into?
- **Path A — Child sick / temporary:** Session rescheduled. No risk flag escalation. → Continue at Step 12
- **Path B — Financial pressure / fees outstanding:** Rahul reviews billing record. May choose to include payment link in follow-up, offer a fee waiver or extension, or schedule a conversation. This is relationship management — not automatable. Outstanding balance visible in Rahul's dashboard. → Internal note recorded; optional billing action.
- **Path C — Family disengaging (no response, vague answers, consistently cancelling):** Rahul updates enrollment status to "At Risk." Records internal note. Continues monitoring. → Continue at Step 10B
- **Path D — Family explicitly withdrawing:** Rahul updates enrollment status to "Discharged" with reason code. → Continue at Step 13
- **Path E — No response from Meena:** Rahul has no information. Family remains active with "At Risk" flag. Second follow-up attempt is Rahul's discretion — platform has no automated second message (to avoid pressure on financially stressed families). → Rahul decides manually.

### Decision 4: Does the family return?
**At step:** 14–15 (re-engagement)
**Question:** After Rahul's follow-up, does Meena bring the child back?
- **Path A — Child returns within 1–2 weeks:** Session rescheduled or next scheduled session occurs. Attendance marked Present. Dropout risk counter begins resetting. After 4 consecutive attended sessions, risk flag cleared automatically (Step 15).
- **Path B — Child returns after a longer gap (4+ weeks):** Dr. Sunita should assess whether the therapy program needs updating. Child's program targets may be stale. Platform flags program as overdue for update in Dr. Sunita's caseload dashboard. Clinical re-assessment recommended before resuming.
- **Path C — Child does not return (silent dropout):** No platform action after Rahul's manual follow-up. If no session attendance for 30+ days and no response to follow-up, Rahul should manually update status to Discharged. There is no auto-discharge trigger — discharge is always a human decision.

### Decision 5: Are outstanding fees contributing to dropout risk?
**At step:** 9 (follow-up action selection)
**Question:** Does this child have an outstanding unpaid invoice at the time of the dropout risk alert?
- **Path A — No outstanding fees:** Follow-up is purely attendance-focused. No payment link needed.
- **Path B — Outstanding fees exist:** Rahul must use judgment. Including a payment link in a follow-up message to a family that just missed a session may feel transactional and damage the relationship. Platform surfaces the fee status as context — Rahul decides whether to include it.
- **Path C — Fees are significantly overdue (30+ days):** This child appears in both the dropout risk list AND the overdue payments list. Rahul is managing two overlapping problems. The product should surface this co-occurrence clearly — do not treat them as independent alerts.

---

## Screen Inventory

| Screen name | Purpose | Primary action | Personas who see it | Source story |
|---|---|---|---|---|
| Mark Attendance Screen | Priya marks session as No-show (trigger for this journey) | Tap "No-show" chip | Priya | SCHED-004 |
| Center Director Dashboard | Rahul's view of all active children with status flags — sort by last session to surface at-risk families | Sort by "Last Session" / filter by "At Risk" status | Rahul | MPM-005 |
| Center Calendar — Day/Week view | Rahul's operational view — no-show indicators visible on session cards | Tap session → quick actions | Rahul | SCHED-005 |
| Child's Session History (Sessions tab) | Detailed attendance timeline for a specific child — all sessions, statuses, dates | Filter by date range / status | Rahul, Dr. Sunita | SCHED-005 → child record |
| Dropout Risk Alert (in-app notification) | Proactive alert when 3+ no-shows or 2+ consecutive missed sessions detected | Tap to open child's session history | Rahul | REMIND-002, MPM-005 |
| Child Profile — Enrollment Status | Update a child's enrollment status (Active / At Risk / On Hold / Discharged) and add internal notes | Update status dropdown + save | Rahul | MPM-005 |
| Reminder Delivery Log | Audit log showing no-show follow-up message delivery status | Retry failed messages | Rahul | REMIND-005 |
| Supervisor Caseload Dashboard | Dr. Sunita's view of all supervised children — overdue flags include session gaps | Filter by overdue flags | Dr. Sunita | MPM-003 |
| Settings > Reminders | Edit no-show follow-up template; configure dropout risk thresholds (no-shows per 30 days = N) | Edit template text and save | Rahul | REMIND-004 |
| Reschedule modal | Reschedule a missed session to a new slot | Confirm new date/time | Rahul | SCHED-003 |

---

## Designer Handoff

### Screen: Center Director Dashboard (dropout risk view)

**Purpose:** Give Rahul a prioritized view of children who are at dropout risk — either flagged by the system (no-show pattern) or flagged by the Rahul (manual "At Risk" status). This is a secondary view within the broader caseload management dashboard.
**Primary action:** Tap a child row to open their session history.
**Entry point(s):** Bottom nav "Children" tab → filter by "At Risk" or sort by "Last Session date".
**Exit point(s):** Tap child row → child's record (Sessions tab); tap "Send Follow-up" shortcut → WhatsApp send flow.

**Key components:**
- Filter: "At Risk / On Hold" filter chip alongside existing status filters (Active / Discharged). When active, shows only children in At Risk or On Hold status.
- Sort: "Sort by Last Session" option. Children sorted from longest absence (top) to most recent session (bottom).
- Child row with risk context: Child name, enrollment status badge ("At Risk" — amber; "On Hold" — grey), last session date ("X days ago"), no-show count (rolling 30 days), assigned therapist name, outstanding fee indicator (₹ icon if fees outstanding — color-coded).
- "Send Follow-up" shortcut on each row: Single tap opens WhatsApp send flow (WA-004 / WA-005) pre-loaded for this child/parent. Only visible if parent is opted in.
- Dropout risk badge: On child rows with system-generated risk flag (3+ no-shows). Distinct visual from manually-set "At Risk" status.

**States:**
- **Empty state (no at-risk children):** "No children are currently flagged as at risk. Great work." Positive reinforcement; shows last time the dashboard was checked.
- **Loading state:** Skeleton rows.
- **Error state:** "Could not load caseload data. Pull to refresh."
- **Offline state:** Last-synced data shown; no-show counters based on last-synced attendance. Risk calculations may be stale — show "Attendance data may be outdated" if offline >1 hour.

**Constraints:**
- This view is critical for Rahul's weekly review — must be accessible in ≤ 2 taps from the app home screen.
- Outstanding fee indicator must be informational only — Rahul decides whether to act on it in the context of dropout risk. Do not auto-link billing follow-up to dropout follow-up without Rahul's explicit action.
- Risk badges must be clearly distinguished from enrollment status labels — use different visual language (badge vs. pill vs. icon) to avoid confusion.
- Data on this screen is sensitive (child names, attendance gaps, fee status) — session lock after 5 minutes of inactivity (configurable by admin) is a platform-wide requirement.

---

### Screen: Child's Session History (Sessions tab)

**Purpose:** Give Rahul and Dr. Sunita a complete attendance timeline for a specific child — every scheduled session, its status, and the pattern of attendance over time. The primary evidence base for a dropout risk assessment.
**Primary action:** Review attendance pattern; optionally tap a session to reschedule or add context.
**Entry point(s):** Tap child row on Center Director Dashboard; tap child from Supervisor Caseload Dashboard; tap notification alert for this child.
**Exit point(s):** Tap session row → session detail (reschedule / note view); tap "Update Status" → Enrollment Status screen; tap "Send Follow-up" → WhatsApp send flow.

**Key components:**
- Attendance summary bar: Total sessions scheduled (this period), total Present, total Absent/No-show, attendance rate % as a number. Date range selector (last 30 days / last 90 days / all time).
- Session list: Chronological, newest first. Each row: date, day of week, status chip (Present / Absent / No-show / Cancelled), therapist name, time. No-show rows visually distinct (amber left border or icon).
- Consecutive absence indicator: If 2+ consecutive sessions are non-Present, a visual separator or banner between those sessions: "2 consecutive sessions without attendance — risk flag."
- "Update Status" button: Opens Enrollment Status update flow. Visible to Rahul only.
- "Send Follow-up" button: Opens WhatsApp send flow. Visible if parent opted in to WhatsApp.

**States:**
- **Empty state:** "No sessions have been scheduled for [Child name] yet." — visible only if child has no schedule. Should not appear in this journey (trigger requires sessions to exist).
- **Loading state:** Skeleton list.
- **Error state:** "Could not load session history. Pull to refresh."
- **Offline state:** Previously cached session history readable. New sessions or attendance updates not visible until sync.

**Constraints:**
- Session history for a child at dropout risk may be emotionally sensitive context. Language in the UI should be neutral and factual — avoid alarm language like "DANGER" or "FAILING" — use "At risk" and "Missed sessions" as measured, professional language.
- The attendance rate percentage should be visible without scrolling — pin in the summary bar at the top.
- This screen is shared between Rahul (who can take action) and Dr. Sunita (who can add clinical notes). Action buttons (Update Status, Send Follow-up) should be visible only to the appropriate role.

---

### Screen: Child Profile — Enrollment Status

**Purpose:** Let Rahul update a child's enrollment status (Active → At Risk → On Hold → Discharged) and record the reason for the change, creating an administrative audit trail.
**Primary action:** Select new status, optionally enter a note, tap "Save."
**Entry point(s):** Tap "Update Status" from Child's Session History or from child's profile header.
**Exit point(s):** Tap "Save" → child profile updated, returns to child's profile. Child's card in center director dashboard updated.

**Key components:**
- Enrollment status selector: Large radio chips or a segmented control. Options: Active / At Risk / On Hold / Discharged. Current status highlighted.
- Discharge reason dropdown (appears only when "Discharged" is selected): Family withdrew / Financial reasons / No contact — no response / Transferred to another center / Clinical graduation (goals met) / Other (free text).
- Internal note field: Free text, max 500 characters. Visible only to Rahul, Dr. Sunita, and admin. Not visible to Priya or parent. Label: "Internal note — not shared with family."
- Status change log (below form): Chronological list of all previous status changes — date, old status, new status, who changed it. Read-only.

**States:**
- **Default state:** Current status shown selected. Note field empty.
- **Loading state:** Spinner on "Save" button.
- **Error state:** "Could not save status update. Try again." No state committed.
- **Offline state:** Status change queued locally. Syncs on restore. Child's card in dashboard updates on device immediately (optimistic update).

**Constraints:**
- "Discharged" status triggers a cascade: future sessions beyond discharge date should be flagged for cancellation — present a confirmation: "This will remove [Child name] from active schedules. X upcoming sessions will be cancelled. Proceed?"
- Discharge is always a human decision. No auto-discharge based on attendance pattern — the product surfaces risk, Rahul decides.
- Internal note is explicitly labeled as internal — design must make this unmistakably clear to Rahul to prevent accidental sharing of sensitive internal observations.

---

### Screen: In-App Notification — Dropout Risk Alert

**Purpose:** Proactively notify Rahul when the system detects a concerning attendance pattern (3+ no-shows in 30 days, or 2+ consecutive missed sessions) before he discovers it manually.
**Primary action:** Tap notification to open the child's session history.
**Entry point(s):** System-generated; appears as in-app notification badge or push notification.
**Exit point(s):** Tap notification → child's Session History tab.

**Key components:**
- Notification text: "[Child name] has missed [N] consecutive sessions. Last attended: [relative date]. Review their attendance." — factual, non-alarming.
- Notification type: In-app banner (persistent until dismissed) + optional push notification to Rahul's device.
- Dismiss: Rahul can dismiss the notification after reviewing. Dismissed notifications archived in a "Resolved alerts" section, not deleted.

**States:**
- **Unread:** Full prominence — amber banner in dashboard, unread badge on notification bell icon.
- **Read:** Reduced prominence but still visible until Rahul takes an action (updates status, sends follow-up, or explicitly marks as resolved).
- **Resolved:** Moved to "Resolved alerts" archive. Visible if Rahul wants to review past alerts.

**Constraints:**
- Notifications must not fire during session hours for the same child (if a session is currently in progress, hold the alert until after the session). Avoid distracting Priya or Rahul during an active session.
- Do not batch multiple child alerts into a single generic "X children at risk" notification — each alert should name the specific child so Rahul can triage.
- Maximum alert frequency: one alert per child per 7 days. Do not spam Rahul with repeated alerts for the same pattern.

---

## Developer Handoff

### Step-level technical summary

| Step | Data written | Data read | API / event | Offline behavior | Regulatory gate |
|---|---|---|---|---|---|
| 1 | Session status = No-show; attendance timestamp; Priya user ID | Session record | `PATCH /sessions/{id}/attendance` body: `{status: "no_show"}` | Write locally; sync in background; haptic fires offline | ⚠️ DPDPA — attendance data for a minor; encrypted; access scoped |
| 2 | No-show counter incremented; follow-up job queued (30-min delay) | Child's no-show history (rolling 30 days) | Event: `session.status.updated` → `dropout_risk.evaluate`; delayed job: `no_show_followup.queue(delay=30m)` | Event queued locally; fires on sync | None |
| 3 | Delivery log entry (type = no_show_followup, channel, timestamp, delivery status) | Session status (re-check before send), parent contact, opt-in status, follow-up template | `POST /communications/no-show-followup` → WhatsApp Business API or SMS provider | Cannot send offline; if offline at fire time, job retries 3× then logs failure | ⚠️ DPDPA — parent contact data transmitted to third-party (Meta / SMS provider); message must contain no clinical data; TRAI DLT sender ID for SMS; WhatsApp opt-in required |
| 5 | None (read-only) | Session records with no-show status, no-show counter per child | `GET /children/{id}/sessions?status=no_show` + dashboard aggregation | Cached; stale data shown offline | RBAC: Rahul (full center), Dr. Sunita (caseload scope) |
| 6 | Dropout risk alert record; child risk flag updated | All active children's session records — consecutive absence detection | `POST /jobs/attendance-gap-scan` — daily cron; reads sessions ordered by date per child | Server-side only | DPDPA consent check: only scan children with Active consent records |
| 7 | In-app notification record; push notification queued | Alert record from Step 6 | `POST /notifications` → push notification service | Push notification delivered when client connects; in-app badge visible on reconnect | None — notification is internal (Rahul), contains child name but no clinical data |
| 8 | None (read-only) | All session records for child, sorted by date descending | `GET /children/{id}/sessions?sort=date_desc&limit=50` | Cached session history readable offline | RBAC: assigned staff only |
| 10A | WhatsApp delivery log entry | Parent opt-in status, approved template, WABA connection | WhatsApp Business API `POST /messages` | Cannot send offline | ⚠️ DPDPA + WhatsApp opt-in required; template must be Meta-approved |
| 10B | Enrollment status update; internal note record; status change log entry | Child's current enrollment status | `PATCH /children/{id}/enrollment-status` | Queues locally; optimistic UI update | ⚠️ DPDPA — enrollment status + internal note is health-adjacent data; access scoped to admin + supervisor |
| 13 | Enrollment status = Discharged; discharge reason; discharge date; future sessions cancelled | Child's session schedule (future sessions) | `POST /children/{id}/discharge` — cascades to cancel future sessions | Queues locally; syncs on restore | DPDPA: discharge triggers data retention review (how long to retain records for a discharged minor; suggest minimum 3 years post-discharge, pending legal review) |
| 15 | Dropout risk flag level updated (At Risk → Cleared) | Child's recent attendance (last 4 sessions = Present) | `POST /jobs/risk-resolution-scan` — daily cron | Server-side | None |

**Key state transitions:**
- Session transitions from `Scheduled` → `No-show` at Step 1 (Priya's mark)
- Child `no_show_counter` increments at Step 2; triggers `dropout_risk_alert` when counter ≥ configured threshold (default: 3 in 30 days)
- Child `enrollment_status` transitions from `Active` → `At_Risk` → `On_Hold` → `Discharged` at Step 10B / 13 (Rahul's action)
- Child `enrollment_status` dropout risk flag transitions from `Flagged` → `Cleared` at Step 15 (4 consecutive Present marks)
- Follow-up job transitions from `Queued` → `Fired` or `Cancelled` at Step 2–3 (cancelled if re-marked to Present/Absent within 30 minutes)

**Background jobs / async events triggered by this journey:**
- `no_show_followup_job`: Event-triggered by `session.status.updated` = No-show. 30-minute delay. Cancellable by status re-mark. Sends follow-up SMS/WhatsApp.
- `attendance_gap_scan_job`: Daily cron. Scans all active children for 2+ consecutive non-Present sessions. Generates dropout risk alerts. Runs at end of business day (e.g., 8 PM IST).
- `risk_resolution_scan_job`: Daily cron. Checks "At Risk" children for 4 consecutive attended sessions. Clears risk flag and notifies Rahul.
- `dropout_risk_evaluator`: Triggered by any attendance status change event. Updates rolling no-show counter. Fires alert notification if threshold crossed.

**DPDPA compliance checkpoints:**
- Step 1: ⚠️ DPDPA — No-show attendance record is health-adjacent data for a minor; encrypted at rest; write action logged in audit trail with actor, timestamp
- Step 3: ⚠️ DPDPA — automated SMS/WhatsApp to parent contains child name; no clinical content permitted in message body; WhatsApp transmission routes through Meta infrastructure (parent opt-in required per WA-003); SMS requires TRAI DLT transactional sender ID registration
- Step 10B: ⚠️ DPDPA — enrollment status (At Risk, On Hold) and internal notes are health-adjacent records for a minor; access restricted to admin + supervisor (not Priya, not parent-facing); stored encrypted; included in data retention calculation
- Step 13: ⚠️ DPDPA — discharge triggers a data retention review obligation; discharged children's records must be retained for a minimum period post-discharge (exact period pending legal review for DPDPA 2023 applicability to health records of minors in a private therapy setting; suggest 3 years minimum); records must not be permanently deleted without explicit data deletion request from the parent/guardian

---

## Cross-Journey Dependencies

| Depends on journey | Why | What breaks if missing |
|---|---|---|
| Journey 3 — Weekly Session Scheduling & Attendance Management | No-show status mark (SCHED-004) is the primary trigger for this entire journey. Without attendance being marked digitally by Priya, the system has no signal to detect missed sessions. | Dropout detection is entirely invisible — exactly the current state (journey map Journey 10, BP-05). The product cannot surface risk it cannot detect. Attendance marking in Journey 3 is the non-negotiable prerequisite for Journey 10. |
| Journey 9 — Monthly Billing, Invoicing & UPI Payment Collection | Families at dropout risk often have outstanding fees. Billing data (outstanding balance) must be visible in the dropout risk view so Rahul can assess whether financial pressure is contributing. Without this context, Rahul may send a fee reminder to a family in crisis — worsening dropout. | Rahul sees dropout risk and billing risk as separate, disconnected problems. Cannot make a coordinated decision about whether to follow up on fees or grant flexibility. |
| Intake & Enrollment — DPDPA consent (EMR-002 / INT-003) | Discharge triggers a data retention review. Consent withdrawal during active enrollment is handled by the intake/consent module. | Cannot determine correct data retention period or respond to a parent's consent withdrawal request without the consent record from the intake module. |
| Clinical documentation — SOAP notes, program updates (TMPL-001, SOAP-001) | When a child returns after a significant absence (Path B of Decision 4), Dr. Sunita must assess whether the therapy program is still appropriate. The SOAP note flow and program update flow are the clinical tools for this. | Returning children may resume sessions against an outdated program. Clinical continuity gap — therapy quality risk. |

---

## Design Principles for This Journey

The dropout prevention journey operates in emotionally sensitive territory. Several design principles must be applied beyond standard UX conventions:

**1. Measure and report; do not automate follow-up past the first message.**
The first automated follow-up (REMIND-002) is defensible — it is a single, soft-tone "are you okay?" message. Beyond that, all communication must be Rahul's active decision. Automated second and third messages to a family in financial or emotional distress can accelerate disengagement. Surface the risk; let a human act.

**2. Tone of all system-generated messages: warm and non-threatening.**
Default follow-up template: "[Child name] missed their session at [Center name] today. We hope everything is okay. Please contact us to reschedule: [phone]." No mention of payment, no clinical language, no urgency cues. Rahul can edit templates — but the platform should not default to a transactional or clinical tone.

**3. Co-occurrence of dropout risk and outstanding fees must be visible — but handled separately.**
Do not conflate dropout risk alerts with billing reminders. If a child has both an attendance gap and outstanding fees, surface both pieces of context to Rahul. Let him decide how to handle them together or separately. The automated billing reminder system (INV-005) should respect a per-family disable toggle specifically for families flagged as "At Risk."

**4. Discharge is always a human decision.**
There is no automated discharge trigger in this product. The system surfaces risk; Rahul acts. Any pattern that could theoretically trigger an auto-discharge (e.g., no attendance for 60 days) should instead send Rahul an escalating alert and prompt him to decide. Families who are struggling may eventually return — the product should make it easy to reactivate a child record, not just to close it.

**5. The invisible exit problem requires proactive surfacing, not reactive alerting.**
The current state (journey map Journey 10) is that dropout "is detected only weeks later." The daily attendance gap scan (Step 6) and the "Sort by Last Session" view (MPM-005) are the two mechanisms that convert reactive to proactive. Both must be prominently accessible — not buried in a reports section Rahul never visits.

---

## ⚠️ Feature Factory Disclaimer

These flows were defined by competitive observation, document synthesis, and journey map inference — not by validated user research. Before committing engineering capacity, a real product thinker should ask:

**What we assumed but haven't validated:**
- [ASSUMPTION] Indian autism therapy families miss sessions primarily because of forgetfulness, transport difficulty, or scheduling conflicts — problems where a follow-up message is useful. Tandfonline 2025 research identifies "financial pressure and caregiver exhaustion" as primary drivers of the "invisible exit." If this is the dominant reason for dropout, a notification system will have minimal impact on retention. The follow-up message may need to be accompanied by a human phone call or a flexible fee arrangement — neither of which the platform can automate.
- [ASSUMPTION] Rahul currently has no systematic visibility into which children are approaching dropout. H-18 in the hypothesis register is rated as having medium uncertainty — whether center directors experience dropout as "invisible" or whether they track attendance in Excel has not been confirmed in primary research.
- [ASSUMPTION] Automated follow-up messaging after a missed session (REMIND-002) will improve re-engagement rates at Indian autism therapy centers. The Psychiatric Services 39% → 3% no-show data is from a US psychiatric outpatient context. Its applicability to Indian autism therapy families — who are in a different cultural, economic, and care context — has not been validated.
- [ASSUMPTION] A "dropout risk badge" and dashboard view will cause Rahul to take more consistent follow-up action than he does today. Rahul's current behavior (H-10: single WhatsApp message after a no-show) may already be his maximum practical follow-up given center management workload. The product can surface risk; it cannot guarantee Rahul has time to act on every alert.
- [ASSUMPTION] Outstanding fees and attendance dropout are sufficiently correlated that they should be visible together in the dropout risk dashboard. The connection between fee arrears and dropout risk is logical (both are signals of family stress) but has not been confirmed with data.

**What a researcher would ask before building this:**
- What actually causes Indian autism therapy families to drop out? Are the causes mostly financial, transport, child behavior, lack of visible progress, or something else? The answer determines what interventions (if any) are effective.
- What does Rahul's current follow-up process look like when a child misses a session? How much time does he spend on this? Does he feel it's effective?
- Has Rahul ever tried to track dropout systematically (Excel, calendar notes)? Why or why not? What's the actual friction point — time, information, or process?
- Would a structured dropout risk dashboard make Rahul more likely to act, or would it create alert fatigue (too many flagged children)?

**What the Product Consultant would challenge:**
- This journey layers significant system intelligence on top of a data foundation (attendance marking) that is itself unvalidated for Indian therapy centers. If Priya does not reliably mark attendance in the app, the dropout detection engine has no input and produces no value. The prerequisite is not a dashboard — it is consistent attendance marking behavior. Build and validate Journey 3 first; build Journey 10 second.
- The "3 no-shows in 30 days" threshold for a dropout risk alert is speculative. Some children legitimately have more variable attendance (illness, school schedules, family events). Before hardcoding thresholds, define what configurable looks like — Rahul should be able to set his own thresholds based on his center's norms.
- Consider whether the MVP dropout prevention feature is just: (1) "Sort by Last Session" in the children list (MPM-005) + (2) the automated first follow-up message (REMIND-002). Together, these give Rahul both proactive visibility and an automated first response — without building a risk scoring engine and status management system that requires significant engineering investment.

**Risk level:**
- Automated no-show follow-up message (REMIND-002): Low — simple, soft-touch. Low risk of relationship damage if tone is right.
- Dropout risk badge and counter (3+ no-shows): Low-Medium — useful signal; threshold needs to be configurable to avoid alert fatigue.
- Daily attendance gap scan (Step 6): Medium — depends entirely on attendance data quality from Journey 3.
- Enrollment status management (At Risk / On Hold / Discharged with cascade): Medium — useful administrative feature; risk is in the cascade logic (auto-cancelling future sessions on discharge must be a careful, confirmed action).
- The claim that this journey will meaningfully reduce dropout: High risk — the product can surface risk and facilitate first contact; it cannot address financial pressure, caregiver exhaustion, or transport barriers that are the documented root causes of Indian autism therapy dropout.

Use the `/researcher` agent to validate H-10 and H-18 — the root causes of dropout and Rahul's current follow-up behavior — before committing to the full dropout detection feature set.
Use the `/product-consultant` agent to define the MVP for dropout prevention and challenge the sequencing assumption that Journey 10 can deliver value without Journey 3 being mature.
