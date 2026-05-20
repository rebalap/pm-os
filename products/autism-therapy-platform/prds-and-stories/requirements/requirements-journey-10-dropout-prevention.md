# Requirements: Journey 10 — Appointment Follow-Up & Dropout Prevention

**Product:** Autism Therapy Platform (India)
**Journey:** Journey 10 — Appointment Follow-Up & Dropout Prevention
**MVP status:** IN SCOPE — MVP
**Primary actor:** Rahul (Center Director — receives alerts and manages follow-up)
**Supporting actors:** Priya (marks No-show attendance that triggers detection); Meena (receives follow-up outreach); Dr. Sunita (sees dropout risk in caseload dashboard); System (detects patterns, queues messages, clears flags)
**Date:** 2026-05-06
**Story ID prefix:** DROPOUT-
**Source documents:**
- `user-journeys/journey-10-dropout-prevention.md`
- `user-journeys/journey-map.md` — Journey 10

---

## Epic: DROPOUT — Dropout Detection, Follow-Up & Enrollment Status Management

**Goal:** Give Rahul a systematic, early-warning system that converts dropout from an invisible event detected weeks after it has happened into a visible, actionable signal he can act on within 24–48 hours of the first missed session. By the end of this epic, no child can silently drop out without the system surfacing a structured alert to Rahul, and every follow-up action taken is logged.

**Copied from:** CentralReach (attendance gap alerts, client status management), Motivity (session attendance tracking and risk flagging), SimplePractice (automated follow-up messaging after no-shows), Theralytics (attendance pattern reporting). No Indian competitor has any equivalent feature. This is a differentiator in the Indian market — TherapEZ and PractiPal cover admin and billing only; neither has dropout detection or follow-up automation.

**Target user(s):** Rahul (Center Director), Priya (session attendance marking — trigger role), Dr. Sunita (caseload visibility), Meena (follow-up message recipient)

**Definition of Done:**
- A No-show attendance mark by Priya triggers a 30-minute delayed follow-up message job; the job is idempotent and cancelled if attendance is re-marked to Present or Absent within the window
- The daily attendance gap scan runs at end of business day and flags any child with 2+ consecutive sessions in non-Present status (No-show, Absent, or session time passed without a mark)
- Rahul receives a named, actionable in-app alert for each flagged child — not a batched summary
- Dropout risk badge (3+ no-shows in 30 days) appears on child records, session calendar cards, and Rahul's caseload overview; badge never appears on any parent-facing UI
- Dr. Sunita sees an overdue flag in her caseload dashboard for any child with a session gap > 7 days
- Rahul can send a manual WhatsApp follow-up from the child's profile using an approved WABA template, with optional UPI payment link; delivery is logged; inbound replies are not handled (v1)
- Rahul can update a child's enrollment status to At Risk / On Hold / Discharged; Discharged requires a reason code and triggers cascade cancellation of future sessions with a confirmation dialog
- Auto-resolution fires when an At Risk child attends 4 consecutive sessions; Rahul receives a named in-app notification; risk flag is cleared in the dashboard
- All stories pass QA on minimum-spec Android (Redmi/Realme, 2GB RAM, Android 10+)
- Offline behavior confirmed for all data-write steps
- All outbound messages confirmed to contain logistics fields only — no clinical data

**Out of scope (this epic):**
- Inbound WhatsApp reply handling — v1 is send-only; replies handled on center's personal WhatsApp outside platform
- Automated second or third follow-up messages — one automated message only; all subsequent contact is Rahul's active decision
- Auto-discharge based on attendance pattern — discharge is always a human decision; no automated discharge trigger
- Parent-facing enrollment status display — status fields are internal staff tools only
- Bulk status updates across multiple children simultaneously
- Re-engagement clinical re-assessment flow — handled in Journey 5 (Treatment Plan design) when child returns after a significant gap
- Multi-center or cross-branch dropout analytics
- A/B testing of follow-up message templates

**[ASSUMPTION — NOT VALIDATED]** This epic is built on the assumption that Rahul currently has no systematic visibility into dropout-in-progress and that surfacing structured alerts will cause him to take more consistent follow-up action than his current single-WhatsApp-message behavior (H-18). No primary research with Indian center directors has confirmed this. The 39% → 3% no-show reduction data (Psychiatric Services) is from a US psychiatric outpatient context and has not been validated for Indian autism therapy families. Validate via center director interviews and observational fieldwork before committing the full detection engine. See disclaimer at end of document.

---

## Story DROPOUT-001: Automated no-show follow-up message

**As a** Rahul (Center Director)
**I want to** have the system automatically send a follow-up WhatsApp or SMS message to a parent 30 minutes after Priya marks their child as No-show — but only if the attendance status has not been corrected in the meantime
**So that** a warm, logistics-only first contact goes out to every family that missed a session without me having to remember to send it manually, while protecting families from receiving a message when the attendance mark was a data entry error

**Inspired by:** SimplePractice automated no-show follow-up; Theralytics session reminder and follow-up engine; Jane App missed appointment messaging

**Context:** Priya marks attendance in session — including No-show — on her Android device. She may correct a No-show mark to Present within the session window if the child arrived late. Rahul manages multiple children across the center and cannot reliably send individual follow-up messages for every no-show. The follow-up message must be soft-toned and contain logistics only — no clinical data, no payment reference, no urgency language. The 30-minute delay is intentional: it creates a correction window without delaying the follow-up to a point where it loses warmth. This idempotency requirement is non-negotiable, not a nice-to-have.

**Acceptance Criteria:**
- [ ] AC-01: Given Priya marks a session as No-show, when the `session.status.updated` event fires with status = `no_show`, then a delayed follow-up job is queued server-side with: job ID, session ID, child ID, parent ID, trigger time (event timestamp + 30 minutes), delivery channel (WhatsApp via WABA if configured, DLT SMS fallback), template ID, and status `Queued`
- [ ] AC-02: Given the follow-up job is in `Queued` state and the 30-minute window has not elapsed, when Priya changes the session status from No-show to Present, then the queued job is cancelled and its status updated to `Cancelled — attendance re-marked: Present`; no message is sent to Meena
- [ ] AC-03: Given the follow-up job is in `Queued` state and the 30-minute window has not elapsed, when Priya changes the session status from No-show to Absent, then the queued job is also cancelled and its status updated to `Cancelled — attendance re-marked: Absent`; no message is sent (Absent indicates advance communication; an automated message is not appropriate)
- [ ] AC-04: Given 30 minutes have elapsed and the session status is still No-show, when the follow-up job fires, then the system re-reads the current session status from the database before sending; if status is still No-show at this re-check point, the message is dispatched
- [ ] AC-05: Given the message is dispatched, then the message body contains exactly: child's first name, session date in DD MMM YYYY format, center name, center contact phone number. No diagnosis, therapy type, session notes, behavioral data, outstanding fees, or payment references. Default template: "[Child name] missed their session at [Center name] on [date]. We hope everything is okay. Please contact us to reschedule: [center phone number]."
- [ ] AC-06: Given Rahul has customized the follow-up template in Settings > Reminders, then the customized template is used at dispatch time — provided the customized template is within approved WABA template constraints (logistics fields only; no clinical or financial fields)
- [ ] AC-07: Given the message is dispatched, then a delivery log entry is created with: job ID, child ID, message type = `no_show_followup`, channel, timestamp, delivery status (Sent / Delivered / Read via WABA webhook; Sent only for SMS); this log is visible to Rahul in Settings > Reminders > Delivery Log
- [ ] AC-08: Given a per-family follow-up disable toggle is active for this family (set by Rahul), then the job is created but immediately cancelled at queue time with status `Cancelled — family opted out`; no message is sent
- [ ] AC-09: Given the WABA integration is not configured, then the system falls back to DLT-registered SMS automatically; if neither WABA nor DLT SMS is configured, the job fails with status `Undeliverable — no channel configured` and Rahul sees a center-level configuration warning
- [ ] AC-10: Given the follow-up job fires and delivery fails (network error, invalid number, WABA rejection), then the system retries up to 3 times at 5-minute intervals; after 3 failures the job status is set to `Failed` and Rahul sees "Follow-up message failed — [Child name], [date]" in the Delivery Log with a manual retry option

**Edge Cases & Error States:**
- [ ] EC-01: If the session record is deleted or child record is archived between job queuing and job execution, the job is cancelled automatically with status `Cancelled — record not found`; no error is surfaced to Meena
- [ ] EC-02: If Priya marks No-show offline and the event syncs to the server more than 30 minutes after the actual mark timestamp, the job fires immediately on sync arrival (the 30-minute window is measured from mark timestamp, not sync timestamp); the status re-check still runs before sending
- [ ] EC-03: If the same session is marked No-show, corrected to Present, then marked No-show again, a second follow-up job is queued; the system does not suppress a new job based on prior job history for the same session — only the status re-check at fire time governs dispatch
- [ ] EC-04: If the parent mobile number is missing from the child's record, the job fails at queue time with status `Undeliverable — no parent contact` and Rahul sees an inline warning on the child's profile: "No parent contact number — automated follow-ups cannot be sent"

**Non-Functional Requirements:**
- Performance: Job queuing completes within 2 seconds of the No-show event; job execution is asynchronous and does not block the Priya's attendance marking flow
- Reliability: The delayed job is server-side persistent — it survives server restarts; duplicate job execution for the same session must be idempotent (deduplicated by session ID + job type)
- Offline (Priya): No-show mark writes locally and syncs in background; follow-up job is queued on server when sync completes; haptic confirmation fires on Priya's device at mark time regardless of connectivity
- Offline (message dispatch): Cannot send if no connectivity at fire time; job retries 3 times at 5-minute intervals then fails as above
- Accessibility: Follow-up template editor in Settings uses touch targets >= 44px; free-text input is labeled
- Privacy: ⚠️ DPDPA 2023 — parent contact data (mobile number, child first name) is transmitted to a third-party channel (Meta WABA or SMS provider); message body must contain no clinical or health data for the child; WhatsApp opt-in is required per WABA terms of service; SMS requires TRAI DLT transactional sender ID registration; transmission event is logged in audit trail with actor = System, timestamp

**Dependencies:**
- Blocked by: SCHED-004 (No-show attendance mark — the trigger event), INFRA-001 (DLT SMS or WABA configuration — at least one channel required), WA-003 (parent WhatsApp opt-in management)
- Enables: DROPOUT-002 (no-show counter feeds consecutive session detection), DROPOUT-003 (no-show counter feeds risk badge), DROPOUT-004 (manual follow-up — separate but parallel path)

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android
- [ ] Idempotency tested: same session marked No-show twice produces exactly two jobs, both governed by independent status re-checks
- [ ] Correction window tested: No-show marked, corrected to Present within 30 minutes — confirm zero messages sent
- [ ] Correction window tested: No-show marked, corrected to Absent within 30 minutes — confirm zero messages sent
- [ ] Offline sync tested: No-show marked offline, synced >30 minutes later — confirm message fires immediately on sync with status re-check
- [ ] Per-family disable toggle tested: job created and immediately cancelled
- [ ] SMS fallback tested when WABA not configured
- [ ] Delivery log entry confirmed for Sent, Delivered, Failed states
- [ ] Message body confirmed to contain logistics fields only — clinical and financial fields confirmed absent
- [ ] TRAI DLT sender ID confirmed before production deployment
- [ ] Code reviewed and merged

---

## Story DROPOUT-002: Consecutive missed session detection and alert

**As a** Rahul (Center Director)
**I want to** receive a named, actionable in-app alert when a child has missed 2 or more consecutive scheduled sessions — whether each session was marked No-show, Absent, or simply never marked after the session time passed
**So that** I discover attendance gaps early and proactively, rather than noticing them weeks later when reviewing the calendar

**Inspired by:** CentralReach attendance gap reporting and alert engine; Motivity session attendance tracking; Hi Rasmus caseload monitoring dashboard

**Context:** The current state (Journey 10, BP-05 in the journey map) is that dropout is "detected only weeks later." The daily attendance gap scan is the mechanism that converts reactive discovery into proactive alerting. An unmarked session is not a neutral state — a session whose scheduled time has passed without an attendance mark is a data gap that may indicate dropout. The scan must treat unmarked-past-session-time the same as No-show for consecutive gap detection purposes. This cron runs server-side at end of business day (8 PM IST). Each child generates at most one alert per 7-day period to prevent alert fatigue.

**Acceptance Criteria:**
- [ ] AC-01: Given a daily cron job (`attendance_gap_scan_job`) runs at 8:00 PM IST, then for every active child (enrollment_status = Active or At Risk), it reads all sessions with a scheduled_start_time before the job execution time and evaluates consecutive session status
- [ ] AC-02: Given the scan runs, then a session counts as non-Present for gap detection purposes if its status is: No-show, Absent, or Scheduled (i.e., the session time has passed and no attendance mark has been recorded); Present and Cancelled sessions do not count toward the consecutive gap count
- [ ] AC-03: Given a child's last N consecutive sessions (N >= 2) are all non-Present by the above definition, then the scan creates a dropout risk alert record linked to that child with: child ID, consecutive non-present count, last attended date (or null if never attended), scan timestamp, and alert status `Unread`
- [ ] AC-04: Given a dropout risk alert record is created, then an in-app notification is sent to Rahul's device with text: "[Child name] has missed [N] consecutive sessions. Last attended: [date in DD MMM format, or 'Never' if no prior attendance]. Review their attendance." Notification is not batched with alerts for other children — each child generates a separate named notification
- [ ] AC-05: Given Rahul taps the notification, then the app opens directly to that child's Session History tab (SCHED-005 equivalent), pre-filtered to show the last 90 days, sorted newest first
- [ ] AC-06: Given the same child has an existing Unread dropout risk alert less than 7 days old, then the scan does not generate a new alert for that child on subsequent daily runs; it updates the existing alert's consecutive count and last scan timestamp instead
- [ ] AC-07: Given an alert is Unread and Rahul taps "Mark as reviewed" or takes an action on the child's record (sends follow-up, updates status, reschedules session), then the alert status transitions to `Reviewed`; reviewed alerts are moved to a "Resolved Alerts" archive accessible from the notification center
- [ ] AC-08: Given the scan detects an unmarked past session, then the session record is not auto-updated to No-show — the scan reads session status as-is; only Priya can update attendance status; the scan's classification of "unmarked = data gap" is used only for alert logic, not written back to the session record
- [ ] AC-09: Given a child's enrollment_status is On Hold, Discharged, or Inactive, then the scan excludes that child from gap detection entirely — alerts only fire for Active and At Risk children
- [ ] AC-10: Given the cron job fails to complete (server error), then the failure is logged with timestamp and an engineering alert is triggered; no partial alerts are emitted; the job retries the following day

**Edge Cases & Error States:**
- [ ] EC-01: If a child has only one session ever scheduled and it was missed, the scan does not fire an alert (threshold is 2 consecutive; a single session does not constitute a pattern); DROPOUT-001 handles single no-show follow-up
- [ ] EC-02: If a child has sessions scheduled but all future-dated (no past sessions without an attendance mark), the scan has no data to evaluate and produces no alert for that child
- [ ] EC-03: If Priya marks a past session as Present after the scan has already flagged it (retroactive attendance correction), the existing alert is not automatically withdrawn; Rahul must manually mark it as reviewed; no retroactive alert suppression
- [ ] EC-04: If a center has a large number of children (100+), the cron job must complete within 5 minutes; if not, engineering receives a latency alert

**Non-Functional Requirements:**
- Performance: Scan completes within 5 minutes for a center with up to 200 active children; alerts are delivered within 60 seconds of scan completion
- Reliability: Cron job is idempotent — if re-run on the same day (e.g., after a failure), it does not create duplicate alerts; deduplication key is child ID + scan date
- Offline: Alert delivery is asynchronous; Rahul sees the in-app notification badge when his device reconnects; push notification may be delayed if device is offline at scan time
- Accessibility: Notification text includes child name (no ID numbers or codes); action on notification goes directly to that child's record
- Privacy: ⚠️ DPDPA 2023 — the scan processes session records for all active children in the center; access is scoped by center ID and RBAC role (scan runs with system/service account privileges); alert records are stored encrypted; child names in push notifications are subject to device lock screen visibility — Rahul should be advised to enable device lock screen privacy settings

**Dependencies:**
- Blocked by: SCHED-004 (attendance marking — the input data for the scan), AUTH-RBAC (center-scoped data access), INFRA-003 (server-side cron infrastructure)
- Enables: DROPOUT-003 (alert badge in caseload dashboard), DROPOUT-005 (status update action accessible from the alert tap-through)

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android
- [ ] Cron runs at 8 PM IST confirmed in staging environment
- [ ] Consecutive gap detection tested with No-show, Absent, and unmarked past session — all three count as non-Present
- [ ] Alert de-duplication tested: same child, consecutive scans within 7 days — confirm no duplicate alert created
- [ ] Alert reviewed state tested: confirm alert moves to archive after Rahul takes action
- [ ] Child exclusion tested: On Hold and Discharged children confirmed excluded from scan
- [ ] Cron idempotency tested: re-run same day — confirm no duplicate alerts
- [ ] Code reviewed and merged

---

## Story DROPOUT-003: Dropout risk badge and caseload visibility

**As a** Rahul (Center Director) and Dr. Sunita (Clinical Supervisor)
**I want to** see a dropout risk badge on any child who has 3 or more no-shows in the rolling 30-day window, visible in the child's record, on the session calendar card, and in the caseload overview sorted by last session — and I want Dr. Sunita to see an overdue flag for any child with a session gap greater than 7 days
**So that** dropout risk is visible at a glance during daily and weekly center review, without needing to open each child's record individually

**Inspired by:** CentralReach caseload health dashboard; Motivity attendance reporting; Hi Rasmus at-risk client flagging in supervisor view; MPM-003 and MPM-005 from cluster-2-patient-records-intake

**Context:** The dropout risk badge is a computed, system-generated signal based on the rolling no-show counter. It is distinct from the enrollment status that Rahul sets manually (At Risk). A child can have a dropout risk badge without being manually set to At Risk, and vice versa. This badge is an internal staff tool and must never appear on any parent-facing UI or in any outbound communication. The badge threshold defaults to 3 no-shows in 30 days and is configurable by Rahul in Settings > Reminders.

**Acceptance Criteria:**
- [ ] AC-01: Given the system maintains a rolling 30-day no-show counter per child (updated on every attendance status change event), when the counter reaches 3 or more within the rolling window, then a `dropout_risk_flag` is set to true on the child record; when the counter drops below 3 (due to the 30-day window rolling forward past older no-shows), the flag is automatically cleared
- [ ] AC-02: Given a child's `dropout_risk_flag` is true, then an amber risk badge labeled "Dropout risk" appears in: (a) the child's profile header card, (b) the session card for that child on the center calendar day/week view, and (c) the child's row in Rahul's center director caseload overview
- [ ] AC-03: Given Rahul opens his Center Director Caseload Overview, then a "Sort by Last Session" option is available; when selected, children are sorted from longest absence (most days since last Present session) to most recent, surfacing at-risk families at the top of the list
- [ ] AC-04: Given the caseload overview is loaded, then each child row displays: child name, enrollment status badge (Active / At Risk / On Hold / Discharged), last session date expressed as "X days ago" or "Today", no-show count in the rolling 30-day window, assigned therapist name, and a fee outstanding indicator (Rs. icon, amber) if the child has any unpaid invoice
- [ ] AC-05: Given Dr. Sunita opens her Supervisor Caseload Dashboard, then any child assigned to her supervision with a last Present session more than 7 days ago displays an overdue flag labeled "Overdue — [N] days since last session"
- [ ] AC-06: Given the dropout risk badge threshold is configurable, when Rahul sets a custom threshold (e.g., 2 or 4 no-shows in 30 days) in Settings > Reminders > Dropout Risk Threshold, then the badge computation uses the custom threshold for all children in that center
- [ ] AC-07: Given the dropout risk badge is computed and displayed, then the badge and its underlying counter must never appear on any parent-facing screen, in any message sent to Meena, or in any exported report intended for parent distribution; the badge is internal-only
- [ ] AC-08: Given the caseload overview is loaded offline from cache, then a "Attendance data may be outdated — last synced [timestamp]" banner is shown if the device has been offline for more than 1 hour; badge states and counters reflect last-synced data
- [ ] AC-09: Given the caseload overview is empty of at-risk children, then the view shows: "No children are currently flagged as at risk." with the last scan timestamp

**Edge Cases & Error States:**
- [ ] EC-01: If a child is manually set to enrollment_status = At Risk by Rahul but has fewer than 3 no-shows in 30 days, the manual At Risk status badge is shown independently of the system dropout risk badge; the two signals use distinct visual language (enrollment status = pill label; system risk badge = amber icon + label) to prevent confusion
- [ ] EC-02: If the rolling counter computation lags (e.g., sync delay), the badge may briefly show stale data; a "Refreshing..." indicator must appear while counter recomputation is in progress after a sync event
- [ ] EC-03: If a child has no sessions in the last 30 days (e.g., newly enrolled, no sessions yet scheduled), the no-show counter displays "0" and no badge appears; the overdue flag in Dr. Sunita's view fires if a session has been scheduled with a start time more than 7 days ago and was not attended — not simply based on time since enrollment

**Non-Functional Requirements:**
- Performance: Caseload overview loads within 2 seconds on 4G for a center with up to 200 active children; badge state is a cached computed field, not a live query on each load
- Offline: Caseload overview reads from local cache; badge states reflect last-synced data with staleness indicator
- Accessibility: Risk badge must include a text label alongside any color indicator — never color alone; "Dropout risk" label must be present; touch targets on sort/filter controls >= 44px
- Privacy: ⚠️ DPDPA 2023 — the caseload overview aggregates health-adjacent data (session history, attendance gaps) for all children in the center; access is RBAC-gated: Rahul sees all children; Dr. Sunita sees only her supervised caseload; Priya has no access to caseload overview; parent has no access to any risk badge or counter; session lock after 5 minutes of inactivity is a platform-wide requirement

**Dependencies:**
- Blocked by: DROPOUT-001 (no-show counter is updated by the event that triggers DROPOUT-001), DROPOUT-002 (alert badge links to the same child record), SCHED-005 (center calendar session card — badge displayed here), MPM-005 (caseload overview — Rahul's view), MPM-003 (supervisor caseload — Dr. Sunita's view)
- Enables: DROPOUT-004 (send follow-up shortcut on child row), DROPOUT-005 (update enrollment status action accessible from child profile)

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android
- [ ] Badge appears at threshold and clears automatically when rolling window advances past old no-shows
- [ ] Manual At Risk status and system dropout risk badge confirmed visually distinct in design review
- [ ] Badge confirmed absent from all parent-facing screens — verified by QA on parent account login
- [ ] Sort by Last Session tested with mixed Active / At Risk children
- [ ] Dr. Sunita overdue flag tested with 7-day gap threshold
- [ ] Offline staleness banner tested: device offline >1 hour
- [ ] Custom threshold configuration tested
- [ ] Code reviewed and merged

---

## Story DROPOUT-004: Manual follow-up from child profile

**As a** Rahul (Center Director)
**I want to** send a manual WhatsApp message to a parent directly from the child's profile using an approved template — and optionally attach a UPI payment link if the family has outstanding fees — with the send logged in the delivery record
**So that** I can initiate a personal follow-up with context (session history visible on the same screen) without leaving the platform or picking up my personal WhatsApp

**Inspired by:** SimplePractice client messaging; CentralReach portal messaging; WA-004 and WA-005 from cluster-4-scheduling-communication

**Context:** This is a human-initiated follow-up — distinct from the automated DROPOUT-001 message. Rahul initiates it from the child's profile after reviewing the attendance pattern. The platform sends outbound only in v1 — Meena's reply goes to the center's personal WhatsApp number (outside platform). The UPI payment link is optional and must only be offered to Rahul as a choice — not auto-included. Including a payment link in a follow-up to a family that just missed a session may damage the relationship; Rahul must make this judgment call consciously. The message must contain no clinical data per DPDPA 2023 and relationship-sensitivity requirements.

**Acceptance Criteria:**
- [ ] AC-01: Given Rahul opens a child's profile and the parent has WhatsApp opt-in status = true, then a "Send Follow-up" button is visible in the child profile action menu; if opt-in status = false or unknown, the button is hidden and replaced with: "Parent not opted in to WhatsApp messages"
- [ ] AC-02: Given Rahul taps "Send Follow-up", then a send confirmation sheet opens displaying: the selected template text (pre-filled with child name, center name, center phone number), a preview of the final message as it will appear to Meena, and a "Send" CTA
- [ ] AC-03: Given the send confirmation sheet is open, then a "Add payment link" toggle is visible if and only if the child has at least one unpaid invoice; toggling it on appends a UPI payment link to the message template; the default state is OFF; Rahul must consciously opt in
- [ ] AC-04: Given Rahul confirms "Send", then the message is dispatched via WhatsApp Business API; a delivery log entry is created with: child ID, message type = `manual_followup`, template used, payment link included (boolean), timestamp, delivery status (Sent / Delivered / Read)
- [ ] AC-05: Given the message is dispatched, then the message body contains: child's first name, session context (e.g., "We noticed [Child name] hasn't been in recently"), center name, center contact phone number, and optionally the UPI payment link if toggled on; no diagnosis, therapy type, behavioral data, clinical notes, or session observation content in any field
- [ ] AC-06: Given the message is sent, then Rahul sees a "Message sent" confirmation toast; the child's profile shows a "Last manual follow-up sent: [date/time]" label; delivery status updates asynchronously via WABA webhook
- [ ] AC-07: Given Meena replies to the WhatsApp message, then her reply is received by the center's personal WABA number or personal WhatsApp — not by the platform; v1 does not handle inbound replies; Rahul must take action on the reply outside the platform
- [ ] AC-08: Given Rahul attempts to send from an account without Center Director or Admin role, then the "Send Follow-up" button is not shown; manual follow-up is a Rahul-only action

**Edge Cases & Error States:**
- [ ] EC-01: If the WABA API call fails (network error, API rejection), the platform shows "Message not sent — tap to retry"; delivery log entry records status = `Failed`; Rahul can retry from the delivery log
- [ ] EC-02: If the child has no parent mobile number on record, the "Send Follow-up" button is hidden and replaced with: "No parent contact — add contact to send messages"; links to the parent contact field on the child's profile
- [ ] EC-03: If the child's enrollment_status is Discharged, the "Send Follow-up" button remains visible (Rahul may still need to contact a discharged family for administrative purposes); a banner displays "This child is discharged" above the send form
- [ ] EC-04: If the WABA template used has not been approved by Meta or has expired, the dispatch fails immediately with a platform error: "Message template not approved — contact support"; delivery log records status = `Template not approved`

**Non-Functional Requirements:**
- Performance: Send confirmation sheet opens within 1.5 seconds; message dispatch is asynchronous and does not block the UI
- Offline: Manual follow-up requires connectivity; if offline, the "Send Follow-up" button shows "Connect to send messages"; no offline queue for manual messages
- Accessibility: Touch targets >= 44px; "Add payment link" toggle is labeled; send confirmation sheet is operable one-handed; message preview is readable at default system font size
- Privacy: ⚠️ DPDPA 2023 — manual message transmits parent contact data (mobile number) and child first name to Meta WABA infrastructure; parent WhatsApp opt-in is required as a prerequisite (AC-01 gate); message body must contain no clinical or health data; payment link URL must not contain clinical identifiers in query parameters; transmission event logged in audit trail

**Dependencies:**
- Blocked by: DROPOUT-003 (child profile — entry point for this action), WA-003 (parent WhatsApp opt-in status), INFRA-002 (WhatsApp Business API), INV-002 (outstanding invoice check — for payment link eligibility)
- Enables: No direct downstream story dependency; audit trail feeds center-level follow-up reporting

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android
- [ ] Payment link toggle tested: off by default, enabled only when unpaid invoice exists, toggles UPI link in message preview
- [ ] Opt-in gate tested: parent with opt-in = false — "Send Follow-up" button hidden
- [ ] Message body confirmed to contain logistics fields only — clinical and financial content confirmed absent (except optional UPI link when Rahul enables it)
- [ ] Delivery log entry confirmed for Sent, Delivered, Failed states
- [ ] Inbound reply handling confirmed absent — verified no reply capture or processing exists in v1
- [ ] Code reviewed and merged

---

## Story DROPOUT-005: Enrollment status update — At Risk, On Hold, Discharged

**As a** Rahul (Center Director)
**I want to** update a child's enrollment status from Active to At Risk, On Hold, or Discharged — with a mandatory reason code for Discharged, a cascade cancellation of future sessions on Discharge, and an internal audit log of every status change
**So that** my center director dashboard reflects the true state of each child's enrollment, Priya's My Children list stays current with only active children, and Dr. Sunita's caseload stays accurate — without deleting any historical data for the discharged child

**Inspired by:** CentralReach client status management and discharge workflow; SimplePractice client archive; Motivity enrollment status

**Context:** Enrollment status is an internal administrative classification — it is never shown to Meena or surfaced in any parent-facing UI. The Discharged state has the most consequential cascade: it removes the child from Priya's active list, removes them from Dr. Sunita's active caseload, and cancels future sessions beyond the discharge date. This cascade must be presented to Rahul in a confirmation dialog before committing. Discharge is always a human decision — there is no auto-discharge trigger in this product. The child's historical record (past sessions, notes, reports) remains fully accessible to Rahul for audit and reporting after discharge.

**Acceptance Criteria:**
- [ ] AC-01: Given Rahul opens a child's profile with role Center Director or Admin, then an "Update Status" button is visible in the profile header; tapping it opens the Enrollment Status Update screen
- [ ] AC-02: Given the Enrollment Status Update screen is open, then it displays a radio selector with options: Active / At Risk / On Hold / Discharged; the current status is pre-selected; the screen also shows a read-only status change log below the form: each entry shows status_from, status_to, changed_by user name, changed_at timestamp
- [ ] AC-03: Given Rahul selects At Risk or On Hold, then an optional internal note field is shown (free text, max 500 characters, labeled "Internal note — not shared with family"); Rahul can save without entering a note; saving writes the new status and note to the child record and logs the change in the status history
- [ ] AC-04: Given Rahul selects Discharged, then a mandatory reason code dropdown appears: Family withdrew / Financial reasons / No contact — no response / Transferred to another center / Clinical graduation (goals met) / Other (free text required if Other selected); the "Save" CTA is disabled until a reason code is selected
- [ ] AC-05: Given Rahul has selected Discharged and a reason code, when Rahul taps "Save", then a confirmation dialog fires before any data is written: "This will discharge [Child name] and cancel [N] upcoming sessions scheduled after [discharge date]. This action removes [Child name] from active schedules. Proceed?" with "Confirm Discharge" and "Cancel" CTAs
- [ ] AC-06: Given Rahul confirms discharge, then: enrollment_status is set to Discharged; discharge_reason and discharge_date are written to the child record; all sessions with scheduled_start_time after discharge_date are cancelled (session status set to Cancelled — Discharged); child record is removed from Priya's My Children list; child record is removed from Dr. Sunita's active supervised caseload; new session creation for this child is blocked (SCHED-001 gate — "Cannot schedule sessions for a discharged child")
- [ ] AC-07: Given a child is discharged, then the child's full historical record remains readable to Rahul and Dr. Sunita (past sessions, attendance history, notes, reports, invoices); the record is not deleted and not hidden; it appears in a "Discharged" filter category in the center director's full child list
- [ ] AC-08: Given Rahul updates status to At Risk, then the manual At Risk status badge appears on the child's profile and caseload row (distinct from the system dropout risk badge — see DROPOUT-003 AC-01); the automated billing reminder system (INV-005) respects a per-family disable toggle for any child flagged At Risk
- [ ] AC-09: Given any enrollment status change is saved, then a status history log entry is written with: child ID, status_from, status_to, changed_by user ID and name, changed_at timestamp, note text (if entered), reason code (if Discharged); this log is visible on the Enrollment Status Update screen and accessible to Rahul and Dr. Sunita only

**Edge Cases & Error States:**
- [ ] EC-01: If the API call to PATCH /children/{id}/enrollment-status fails, the UI reverts the optimistic status change, shows "Status update failed — tap to retry", and makes no changes to session records or caseload lists
- [ ] EC-02: If the child has zero upcoming sessions after discharge date, the confirmation dialog text reads: "This will discharge [Child name]. No upcoming sessions will be affected. Proceed?" (no mention of cancellations when there are none)
- [ ] EC-03: If a child is On Hold and Rahul changes status back to Active, then the child reappears on Priya's My Children list and Dr. Sunita's active caseload; no sessions are auto-restored (sessions cancelled while On Hold must be rescheduled manually by Rahul)
- [ ] EC-04: If the discharge cascade session cancellation partially fails (e.g., some sessions cancelled, server error mid-cascade), the cascade is rolled back entirely; the discharge is not committed; Rahul sees: "Discharge could not be completed — please retry"; the child's status remains as it was before the attempt

**Non-Functional Requirements:**
- Performance: Status update and cascade commit within 3 seconds on 4G for a child with up to 50 upcoming sessions; cascade is server-side transactional (all sessions cancelled or none)
- Offline: Status change requires connectivity; if offline, "Connect to update status" is shown; no offline queue for enrollment status changes (cascade risk is too high to commit locally)
- Accessibility: Radio selector chips >= 44px touch targets; reason code dropdown is accessible via native Android controls; confirmation dialog is dismissible with hardware back button (mapped to "Cancel")
- Privacy: ⚠️ DPDPA 2023 — enrollment status (At Risk, On Hold, Discharged) and internal notes are health-adjacent records for a minor; access restricted to Center Director and Clinical Supervisor roles (not Priya, not parent-facing); stored encrypted; discharge triggers a data retention review obligation — discharged children's records must be retained for a minimum period post-discharge (suggest minimum 3 years, pending legal review of DPDPA 2023 applicability to health records of minors in private therapy settings); records must not be permanently deleted without an explicit written data deletion request from the parent or guardian

**Dependencies:**
- Blocked by: DROPOUT-003 (child profile — entry point), AUTH-RBAC (Center Director / Admin role gate), SCHED-001 (session creation gate that checks enrollment_status before allowing scheduling)
- Enables: DROPOUT-006 (auto-resolution checks enrollment_status = At Risk), center-level discharge reporting (analytics workstream)

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android
- [ ] Discharge cascade tested: future sessions confirmed cancelled after discharge date; historical sessions confirmed untouched
- [ ] Rollback tested: partial cascade failure — confirm no discharge committed and no sessions partially cancelled
- [ ] Discharged child confirmed absent from Priya's My Children list
- [ ] Discharged child confirmed absent from Dr. Sunita's active caseload
- [ ] New session creation for discharged child confirmed blocked
- [ ] Historical record confirmed accessible to Rahul after discharge
- [ ] At Risk status tested: manual At Risk badge confirmed distinct from system dropout risk badge in visual review
- [ ] Status history log confirmed written for every status change
- [ ] Code reviewed and merged

---

## Story DROPOUT-006: Dropout risk auto-resolution

**As a** Rahul (Center Director)
**I want to** receive an in-app notification when a child who was flagged At Risk returns to regular attendance — specifically after 4 consecutive attended sessions — and have the dropout risk flag automatically cleared from the caseload dashboard
**So that** the risk dashboard reflects reality and I don't continue treating a re-engaged family as at risk long after they've returned

**Inspired by:** CentralReach caseload health auto-refresh; Motivity engagement tracking; risk flag lifecycle management in SimplePractice

**Context:** The risk resolution scan runs daily alongside the gap detection scan. It evaluates only children with enrollment_status = At Risk. The threshold of 4 consecutive Present sessions is the resolution signal — chosen to be meaningful (one week of sessions) without being punishingly slow to clear. The notification must name the child — not a generic "N children returned" summary. Once cleared, the child's status is not automatically changed from At Risk to Active — Rahul must make that manual decision; the system only clears the risk flag and notifies him.

**Acceptance Criteria:**
- [ ] AC-01: Given a daily cron job (`risk_resolution_scan_job`) runs (same cadence as the gap detection scan at 8 PM IST), then for every child with enrollment_status = At Risk, it reads the most recent session records and evaluates whether the last 4 consecutive sessions all have attendance status = Present
- [ ] AC-02: Given a child with enrollment_status = At Risk has 4 or more consecutive sessions in Present status (most recent 4 sessions), then the system clears the dropout risk flag (`dropout_risk_flag` = false) on the child record and records a risk resolution event with: child ID, resolution timestamp, trigger = `4_consecutive_present`
- [ ] AC-03: Given the risk flag is cleared, then Rahul receives an in-app notification: "[Child name] has attended 4 consecutive sessions — dropout risk flag cleared." The notification is named (child-specific), not batched with other children
- [ ] AC-04: Given the risk flag is cleared, then the dropout risk badge is immediately removed from: the child's profile header, the session calendar card for that child, and Rahul's caseload overview row; the badge removal is reflected within 60 seconds of the scan completing
- [ ] AC-05: Given the risk flag is cleared, then the child's enrollment_status field is NOT automatically changed from At Risk to Active; enrollment status remains At Risk until Rahul manually updates it; the cleared risk flag only removes the system-computed badge — it does not change Rahul's manual classification
- [ ] AC-06: Given the risk resolution notification is delivered, then Rahul can tap it to open the child's Session History tab, confirming the attendance pattern that triggered the resolution
- [ ] AC-07: Given a child is At Risk and attends 3 consecutive sessions but then misses the 4th, then the resolution threshold resets; the child remains At Risk with the risk flag active; the scan counts only unbroken consecutive Present sessions from the most recent session backward
- [ ] AC-08: Given the risk resolution scan runs and no At Risk children have reached the 4-consecutive threshold, then no notifications are sent and no flags are changed; the scan completes silently

**Edge Cases & Error States:**
- [ ] EC-01: If a child is manually moved from At Risk to Active by Rahul before the resolution scan runs, the scan skips that child (enrollment_status is no longer At Risk); no duplicate notification is sent
- [ ] EC-02: If session attendance data for a child is partially synced (some sessions not yet written from Priya's offline device), the scan evaluates only synced sessions; it may not fire the resolution event until all 4 consecutive sessions are confirmed in the database; this is acceptable — resolution should never fire prematurely
- [ ] EC-03: If the same child's risk flag is cleared and re-set multiple times (child returns, lapses again, returns again), each cycle is recorded independently in the risk resolution event log; the audit trail shows the full history

**Non-Functional Requirements:**
- Performance: Resolution scan completes within 5 minutes for a center with up to 200 active children; runs in the same server-side cron window as the gap detection scan (sequential, not concurrent, to avoid database contention)
- Reliability: Resolution scan is idempotent — re-running on the same day does not re-send the resolution notification or re-clear an already-cleared flag; deduplication key is child ID + resolution date
- Offline: Resolution notification is delivered when Rahul's device reconnects; badge update is reflected on next sync; Rahul's dashboard does not show stale risk badge beyond the next app launch with connectivity
- Privacy: No DPDPA regulatory gate on this story specifically — the resolution scan reads attendance data already processed under DPDPA consent (DROPOUT-002 gate); notification to Rahul contains child name only, no clinical data

**Dependencies:**
- Blocked by: DROPOUT-005 (enrollment_status = At Risk is the precondition; DROPOUT-005 sets this status), SCHED-004 (Present attendance marks are the input to the resolution scan), INFRA-003 (server-side cron infrastructure — shared with DROPOUT-002)
- Enables: No direct downstream story dependency; feeds center-level re-engagement analytics (analytics workstream, future)

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android
- [ ] Resolution threshold tested: 4 consecutive Present sessions — flag cleared and notification fires
- [ ] Threshold reset tested: 3 consecutive Present, then 1 No-show — confirm flag not cleared, threshold resets
- [ ] Enrollment status confirmed unchanged after auto-resolution (At Risk remains At Risk until Rahul manually updates)
- [ ] Badge removal confirmed within 60 seconds of scan completion on child profile, calendar card, and caseload row
- [ ] Idempotency tested: re-run scan same day — confirm no duplicate notification
- [ ] Manual status change before scan confirmed to skip resolution for that child
- [ ] Code reviewed and merged

---

## Backlog Summary

| Story ID | Title | Persona | Complexity | Priority | Blocked by |
|---|---|---|---|---|---|
| DROPOUT-001 | Automated no-show follow-up message | Rahul, Priya (trigger), Meena (recipient) | L | P0 | SCHED-004, INFRA-001, WA-003 |
| DROPOUT-002 | Consecutive missed session detection and alert | Rahul | L | P0 | SCHED-004, AUTH-RBAC, INFRA-003 |
| DROPOUT-003 | Dropout risk badge and caseload visibility | Rahul, Dr. Sunita | M | P0 | DROPOUT-001, DROPOUT-002, SCHED-005, MPM-003, MPM-005 |
| DROPOUT-004 | Manual follow-up from child profile | Rahul | M | P1 | DROPOUT-003, WA-003, INFRA-002, INV-002 |
| DROPOUT-005 | Enrollment status update — At Risk, On Hold, Discharged | Rahul | L | P0 | DROPOUT-003, AUTH-RBAC, SCHED-001 |
| DROPOUT-006 | Dropout risk auto-resolution | Rahul | M | P1 | DROPOUT-005, SCHED-004, INFRA-003 |

**Sprint recommendation:** DROPOUT-001 and DROPOUT-002 are the detection and communication foundation — build in parallel once SCHED-004 (attendance marking) is stable. DROPOUT-003 (badge and caseload view) depends on both and should be the second sprint. DROPOUT-005 (status management) can be built in parallel with DROPOUT-003 once the child profile foundation is in place. DROPOUT-004 (manual follow-up) and DROPOUT-006 (auto-resolution) are P1 — important for v1 but do not block the core detection loop.

**Hard infrastructure dependency:** DROPOUT-001 requires at least one outbound channel to be configured (WABA or DLT SMS). Start INFRA-001 (DLT registration) and INFRA-002 (WABA onboarding) immediately — both have 1–4 week vendor timelines outside engineering control.

**Prerequisite for all DROPOUT stories:** Journey 3 (Weekly Session Scheduling and Attendance Management, specifically SCHED-004 — attendance marking) must be stable and adopted before the dropout detection engine has reliable input data. If Priya does not consistently mark attendance in the app, the detection engine has no signal and produces no value. Build and validate Journey 3 first.

---

## Pre-Build Decisions Required

| # | Decision | Owner | Needed by |
|---|---|---|---|
| PBD-01 | Outbound channel for DROPOUT-001: WABA only at launch, or DLT SMS fallback required from day one | Product / Infra | Before DROPOUT-001 sprint |
| PBD-02 | Default no-show follow-up template text requires legal and clinical review before DLT registration or WABA template submission | Legal / Clinical Lead | Before INFRA-001 / INFRA-002 starts |
| PBD-03 | Dropout risk badge threshold: is 3 no-shows in 30 days the right default, or should it launch configurable with no default (Rahul sets on onboarding) | Product | Before DROPOUT-003 sprint |
| PBD-04 | Consecutive gap detection threshold: is 2 consecutive missed sessions the right alert threshold, or does this produce too many false alerts for centers with high illness-related absences | Product | Before DROPOUT-002 sprint |
| PBD-05 | Auto-resolution threshold: is 4 consecutive Present sessions the right signal — or should it be calendar-time based (e.g., attended for 2 consecutive weeks) | Product | Before DROPOUT-006 sprint |
| PBD-06 | Discharge data retention period: minimum retention for health-adjacent records of discharged minors under DPDPA 2023 — requires legal review | Legal | Before DROPOUT-005 sprint |
| PBD-07 | Parent WhatsApp opt-in mechanism for DROPOUT-001 and DROPOUT-004 — is opt-in confirmed at intake (Journey 2) or does it require a separate WABA opt-in flow | Product / Legal | Before DROPOUT-001 sprint |

---

## ⚠️ Feature Factory Disclaimer

These stories were defined by journey document synthesis, competitive observation, and category assumptions — not by validated primary research with Indian autism therapy center directors or families.

**Evidence cited in this document:**

- 39% no-show rate without a structured reminder vs. 3% no-show rate with live contact — source: Psychiatric Services journal. ✅ This evidence is confirmed from the research literature. However, it is from a US psychiatric outpatient context. Its direct applicability to Indian autism therapy families — who are in a different cultural, economic, and care environment — has not been validated. The 3% figure specifically reflects live telephone contact, not an automated WhatsApp message. The automated follow-up in DROPOUT-001 is a weaker intervention than a live call.

- "Invisible exits" — Indian families experiencing dropout driven by financial pressure and caregiver exhaustion tend to stop responding to WhatsApp rather than formally withdrawing — source: Tandfonline 2025. ✅ This behavior pattern is confirmed in the research literature. It is the basis for the design principle that only one automated follow-up message is sent (DROPOUT-001), with all subsequent contact being Rahul's active human decision. The platform cannot resolve financial pressure or caregiver exhaustion. Stories must not over-promise what a notification system can do.

**What we assumed but haven't validated:**

- [ASSUMPTION] Rahul currently has no systematic visibility into which children are approaching dropout (H-18 — medium uncertainty). Whether center directors currently track attendance patterns in Excel, WhatsApp, or paper notebooks has not been confirmed in primary research. The value of the dropout detection dashboard depends entirely on this being true.
- [ASSUMPTION] An automated WhatsApp follow-up message (DROPOUT-001) after a missed session will improve re-engagement rates at Indian autism therapy centers. The Psychiatric Services evidence involves live telephone contact, not automated messaging. Indian families may respond differently to automated messages given cultural norms around WhatsApp communication.
- [ASSUMPTION] Rahul's current follow-up behavior is a single informal WhatsApp message (H-10) — and that a structured platform tool would cause him to take more consistent action. His current behavior pattern has not been directly observed.
- [ASSUMPTION] The 3 no-shows in 30 days threshold is the right signal level for dropout risk. This threshold is speculative. Some centers may serve children with legitimately variable attendance (seasonal illness, school exam periods, transport challenges). Alert fatigue from a threshold set too low may cause Rahul to ignore the alerts entirely.
- [ASSUMPTION] Outstanding fees and attendance dropout are correlated enough to surface together in DROPOUT-003. The connection is logically grounded in the Tandfonline 2025 finding on financial pressure, but the co-occurrence rate in Indian autism therapy centers has not been quantified.

**What a researcher would ask before building this:**

- What actually causes Indian autism therapy families to stop attending? Are the causes primarily financial, transport-related, caregiver exhaustion, or child behavior challenges? The answer determines whether any detection-and-messaging system can meaningfully reduce dropout — or whether the product is solving the symptom (no-show) rather than the root cause (financial or emotional crisis).
- What does Rahul's current follow-up process look like when a child misses a session? How much time does he spend? Does he feel his current intervention is effective? Does he even recognize dropout as a systematic problem or accept it as inevitable?
- Would a dropout risk dashboard make Rahul more likely to act, or would a center with 15–20 at-risk flags active simultaneously produce alert fatigue that results in no action?

**What the Product Consultant would challenge:**

- This entire epic delivers zero value if SCHED-004 (attendance marking) is not consistently adopted by Priya. The dropout detection engine is only as good as its input data. Consider whether the MVP dropout prevention feature is simply: (a) "Sort by Last Session" in the children list (DROPOUT-003 / MPM-005) combined with (b) the automated first follow-up message (DROPOUT-001). Together, these give Rahul proactive visibility and an automated first response — without building a full risk scoring engine, status management cascade, and resolution scan. Validate the minimal version before committing to the full epic.
- DROPOUT-005 (discharge cascade) carries meaningful engineering risk. The cascade transaction (cancel all future sessions on discharge) must be atomic and rollback-safe. This is a non-trivial engineering concern for a v1 feature in a center-management product. Consider whether On Hold (soft pause, no cascade) covers the majority of real use cases and whether Discharged (hard cascade) can be deferred to v1.1.

**Risk level per story:**

- DROPOUT-001 (automated no-show follow-up): Low — simple, soft-tone, single message. Low risk of relationship damage if tone is right. Primary risk is infrastructure dependency (WABA / DLT) and the overpromise that a message reduces dropout in an Indian context where financial pressure is the root cause.
- DROPOUT-002 (consecutive gap detection): Medium — depends entirely on attendance data quality from Journey 3. If Priya does not mark attendance consistently, the scan produces noise. Threshold calibration (2 sessions) is speculative and may require post-launch tuning.
- DROPOUT-003 (dropout risk badge and caseload view): Low-Medium — useful signal; threshold configurability mitigates alert fatigue risk. Risk is that center directors with many at-risk children become desensitized to the badge.
- DROPOUT-004 (manual follow-up from profile): Low — lightweight WhatsApp send with logging. Risk is platform dependency on WABA approval latency.
- DROPOUT-005 (enrollment status and discharge cascade): Medium-High — cascade transaction is the highest-risk engineering component in this epic. Rollback logic must be airtight. Discharge is irreversible from a session-cancellation standpoint.
- DROPOUT-006 (auto-resolution): Low — computed from existing attendance data; no new data written to external systems. Risk is threshold calibration and user expectation that "dropout risk cleared" means the family is fully re-engaged.
- The claim that this journey will meaningfully reduce dropout at Indian autism therapy centers: High risk — the product can surface risk and facilitate first contact. It cannot address financial pressure, caregiver exhaustion, or transport barriers that are the documented root causes of dropout in this population. Do not use dropout rate reduction as a launch success metric without first validating that forgetfulness and lack of follow-up are the dominant causes in Indian centers.

Use the `/researcher` agent to validate H-10 (Rahul's current follow-up behavior) and H-18 (Rahul's visibility into dropout) before committing to the full detection engine.
Use the `/product-consultant` agent to define the true MVP for dropout prevention and to challenge whether DROPOUT-005 (discharge cascade) belongs in v1 or v1.1.
Use the `/design-critique` agent to review the caseload overview and the Enrollment Status Update screen before prototyping — specifically to confirm that the manual At Risk badge and the system dropout risk badge are visually unambiguous.
