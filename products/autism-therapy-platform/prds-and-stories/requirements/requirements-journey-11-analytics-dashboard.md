# Requirements: Journey 11 — Analytics Dashboard

**Product:** Autism Therapy Platform (India)
**Journey:** Journey 11 — Analytics Dashboard
**MVP status:** ✅ IN SCOPE — MVP
**Primary actor:** Rahul (Center Director / Founder)
**Supporting actor:** Dr. Sunita (Clinical Supervisor — views her own caseload slice via the Therapist Caseload Detail screen; no access to revenue, billing, or center-wide analytics)
**Date:** 2026-05-05
**Story ID prefix:** ANALYTICS-
**Source documents:**
- `user-journeys/journey-11-analytics-dashboard.md`
- `user-journeys/journey-map.md` — Journey 11 section

---

## Epic: ANALYTICS — Center Operations Analytics Dashboard

**Goal:** Give Rahul a single place to see how his center is performing — attendance, revenue, staff utilization, and dropout risk — without assembling data manually from paper and Excel. By the end of this epic, Rahul can open the platform on his phone or laptop, see the five numbers that matter most at a glance, drill into any area that needs attention, and act on that information without leaving the platform.

**Copied from:** CentralReach (director-level operations dashboard, utilization reporting), Motivity (caseload and attendance analytics), Jane App (revenue and collection-rate summary, staff utilization view), SimplePractice (outstanding balance visibility, practice health metrics). No Indian competitor (TherapEZ, PractiPal) has any analytics capability. This is a differentiator in the Indian market, not table stakes for the Indian segment — though it is table stakes in the US ABA market.

**Target user(s):** Rahul (Center Director / Founder) — primary. Dr. Sunita (Clinical Supervisor) — secondary, limited scope (caseload view only; no revenue data).

**Definition of Done:**
- Rahul can open the analytics dashboard on minimum-spec Android (Redmi/Realme, 2GB RAM, Android 10+) and see all five key metric areas — home summary, attendance, billing overview, staff utilization, and dropout risk — with data loading in ≤ 3 seconds on 4G
- Dashboard renders correctly in desktop Chrome (Rahul's end-of-day laptop review) with no horizontal scroll or broken layout
- All charts and visualizations use text labels alongside visual elements — color is never the sole means of conveying information
- Offline: last-cached dashboard data is shown with a "Data as of [date/time]" indicator; no empty or error state when offline
- All analytics screens are read-only — no data entry flows exist within the analytics module
- DPDPA: aggregate metrics shown at center level without individual child names or clinical data; individual child data accessible only via drill-down, with RBAC check and audit log entry at the point of access
- Dr. Sunita can access a caseload view scoped to her assigned children from within the analytics module; she cannot see revenue, billing, or center-wide metrics
- All stories pass QA on minimum-spec Android and desktop Chrome
- Background metric computation is server-side — no real-time aggregation on page load

**Out of scope (this epic):**
- In-app data entry, editing, or status changes — analytics screens are read-only throughout
- Child-level progress report generation — Journey 8 (Progress Reporting to Parents)
- Invoice creation or payment recording — Journey 9 (Billing & Fee Collection)
- Follow-up messaging to at-risk families — Journey 10 (Dropout Prevention); the "Contact now" action in ANALYTICS-005 links out to Journey 10, not a new messaging flow
- RPWD Act compliance report export — separate compliance export story (post-MVP)
- Multi-branch or multi-center analytics (single center only at MVP)
- Custom date range picker beyond the three preset periods (this week / this month / last 3 months)
- Role-based analytics customization or dashboard configuration by Rahul
- Real-time data push or WebSocket updates — polling or cached data only at MVP

**[ASSUMPTION — NOT VALIDATED]** This epic is built on the assumption that Rahul currently assembles center health data from disconnected sources (Excel, WhatsApp, paper) and that a unified digital dashboard would change how quickly he identifies and acts on attendance drops, outstanding fees, and utilization problems. No primary research has confirmed the frequency with which Indian center directors check any kind of operational summary, what specific metrics they prioritize, or whether they use a structured review cadence at all. Validate via H-09 and H-18 fieldwork before sprint planning.

---

## Story ANALYTICS-001: Center director home dashboard

**As a** Rahul (Center Director)
**I want to** open the platform and immediately see a single-screen operational summary — active children, sessions this week, attendance rate this week, outstanding invoices, dropout risk flags, and session notes pending review — without tapping into any sub-section
**So that** I know at a glance what needs my attention today and whether the center is running normally

**Inspired by:** CentralReach director home dashboard; Jane App practice health summary card; SimplePractice outstanding balance banner

**Context:** Rahul opens the app at the start of his workday or between clinical sessions. He is on his Android phone 70% of the time and on a laptop browser at end of day. He has 30–60 seconds to get a picture of where things stand. All summary metrics on this screen are pre-computed server-side on a background schedule — no real-time aggregation fires on page load.

**Acceptance Criteria:**
- [ ] AC-01: Given Rahul is logged in with the Director role, when he opens the platform, then the Home Dashboard screen renders within 3 seconds on minimum-spec Android (Redmi/Realme, 2GB RAM, Android 10+) on a 4G connection, and within 2 seconds on desktop Chrome on Wi-Fi
- [ ] AC-02: Given the Home Dashboard has loaded, then it displays all six operational summary tiles in a single viewport without requiring vertical scroll on a 360×640dp Android screen: (1) Active children — count; (2) Sessions this week — count delivered / count scheduled; (3) Attendance rate this week — percentage; (4) Outstanding invoices — ₹ total and count of families with overdue balance; (5) Dropout risk flags — count of children flagged amber or red; (6) Session notes pending review — count of notes submitted but not yet reviewed by a supervisor
- [ ] AC-03: Given the Outstanding Invoices tile is rendered, then the ₹ figure is displayed in large type (≥ 28sp on Android / ≥ 22px on desktop) and the tile is tappable — tapping navigates to the Billing Overview screen (ANALYTICS-003)
- [ ] AC-04: Given the Dropout Risk Flags tile is rendered with a count > 0, then the tile is tappable — tapping navigates to the Dropout Risk Indicators screen (ANALYTICS-005)
- [ ] AC-05: Given the Session Notes Pending Review tile is rendered with a count > 0, then the tile is tappable — tapping navigates to the session notes pending review list (Journey 6 screen, filtered to pending review status)
- [ ] AC-06: Given the Home Dashboard is loading, then skeleton tiles render immediately in all six tile positions — no blank screen flash before data arrives
- [ ] AC-07: Given Rahul opens the app with no connectivity, then the Home Dashboard shows the last-cached metric values with a "Data as of [date] [time]" label on the summary header; no empty state or error state is shown
- [ ] AC-08: Given the `GET /director/home-summary` API returns an error, then each tile shows the last-cached value with a staleness timestamp; a "Could not refresh — pull down to retry" banner appears at the top of the screen; the cached values remain visible and readable
- [ ] AC-09: Given the platform is rendered in desktop Chrome, then the six tiles render in a 2×3 or 3×2 grid layout without horizontal scroll or overflow; all tiles are visible without scrolling on a 1024px wide viewport

**Edge Cases & Error States:**
- [ ] EC-01: If no sessions have been scheduled for the current week, the Sessions This Week tile shows "0 / 0 — no sessions scheduled this week" and the Attendance Rate tile shows "—" (not 0%), to prevent false zero-attendance alerts
- [ ] EC-02: If no children are enrolled, all six tiles show "0" or "—" with a single CTA: "Enroll your first child to start seeing center metrics"
- [ ] EC-03: If the last-cached data is more than 24 hours old, the staleness label renders in amber text to signal that the data may be materially stale; text reads "Data as of [date] [time] — more than 24 hours ago"
- [ ] EC-04: If Rahul's session token has expired, the app redirects to the login screen before any dashboard data is shown; no metrics are visible without an authenticated Director session

**Non-Functional Requirements:**
- Performance: All six tiles must load from a single API call (`GET /director/home-summary`) — no per-tile individual API calls on page load; total payload ≤ 5KB; renders ≤ 3s on 4G, minimum-spec Android
- Offline: Last-cached payload stored in device-local cache; shown with staleness indicator on reconnect; no empty state
- Accessibility: All tiles include a text label and a numeric value — color is not used as the sole differentiator for any metric; touch targets ≥ 44dp; screen reader should read tile label + value as a single accessible element
- Privacy: Home summary payload contains aggregate counts only — no child names, parent contact details, or clinical data; RBAC-001: Director role required; access to any child-level data requires a secondary tap and separate RBAC check
- Responsive: Layout must adapt gracefully to both 360dp-wide Android viewports and 1024px+ desktop Chrome viewports

**Dependencies:**
- Blocked by: AUTH-001 (Director role authentication), Journey 3 (attendance data must exist for attendance metrics), Journey 9 (invoice data must exist for billing tile)
- Enables: ANALYTICS-002 (Attendance Analytics — reachable from tile), ANALYTICS-003 (Billing Overview — reachable from tile), ANALYTICS-005 (Dropout Risk — reachable from tile)

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android (Redmi/Realme, 2GB RAM, Android 10+)
- [ ] All AC pass in QA on desktop Chrome (1024px viewport minimum)
- [ ] Offline cached display tested: disable network, open app, confirm last-cached values shown with staleness label
- [ ] EC-01 (no sessions this week), EC-02 (no enrolled children), EC-03 (stale cache), EC-04 (expired session) tested
- [ ] Skeleton loading state tested on throttled connection (3G simulation)
- [ ] Code reviewed and merged

---

## Story ANALYTICS-002: Attendance analytics

**As a** Rahul (Center Director)
**I want to** view session delivery rates over a selected period — broken down by therapist and by individual child — and see the center's no-show rate so I can identify attendance problems before they become dropout
**So that** I can spot which therapists have low delivery rates and which children are at risk of disengaging, and act on that information before it becomes a crisis

**Inspired by:** Motivity attendance trend reporting; CentralReach session delivery rate by staff; Jane App appointment delivery summary; Theralytics attendance dashboards

**Context:** Rahul reviews attendance analytics weekly or at month-end, typically on his phone during a planning window or on his laptop after hours. Dr. Sunita may access a caseload-scoped version of attendance data from her own dashboard — but the center-wide attendance breakdown in this story is Director-only. Period selection defaults to "This week" on mobile; Rahul can change it.

**Acceptance Criteria:**
- [ ] AC-01: Given Rahul opens the Attendance Analytics screen, then the screen loads within 3 seconds on 4G and displays: (a) a center-level session delivery rate for the selected period (sessions delivered as a percentage of sessions scheduled), (b) a therapist-level delivery breakdown table, and (c) a child-level attendance trend list
- [ ] AC-02: Given the Attendance Analytics screen is displayed, then a period selector is visible at the top with three options: "This week" (default) / "This month" / "Last 3 months"; tapping any option re-fetches and re-renders all three data sections for the selected period within 3 seconds on 4G
- [ ] AC-03: Given the therapist-level breakdown table is rendered, then each row shows: therapist name, sessions scheduled (count), sessions delivered (count), delivery rate (%), and a text-labeled flag if delivery rate is below 70% — flag text reads "Below target" alongside a warning icon; color is not the sole indicator
- [ ] AC-04: Given the child-level attendance trend list is rendered, then each row shows: child first name (no surname in list view — surname visible only on individual child record drill-down), last 4-week attendance indicator (number of sessions attended / number scheduled in the last 4 weeks), and a text-labeled risk badge if 2 or more consecutive sessions were missed — badge text reads "Missed [N] in a row"
- [ ] AC-05: Given Rahul taps a therapist row in the breakdown table, then the screen navigates to the Therapist Caseload Detail screen for that therapist (same destination as ANALYTICS-004 drill-down)
- [ ] AC-06: Given Rahul taps a child row in the attendance trend list, then the screen navigates to that child's record on the Attendance tab (read-only view)
- [ ] AC-07: Given the no-show rate metric is displayed, then it is shown as a percentage alongside a plain-text label: "No-show rate: [N]% of scheduled sessions were no-shows this [period]"; center-initiated cancellations are excluded from the no-show calculation and counted separately
- [ ] AC-08: Given Rahul opens the Attendance Analytics screen with no connectivity, then the last-cached data for the last-selected period is shown with a "Data as of [date] [time]" indicator; the period selector is visible but switching periods while offline shows "Period data not available offline — showing last cached view"

**Edge Cases & Error States:**
- [ ] EC-01: If no sessions have been scheduled in the selected period, all three sections show a period-specific empty state: "No sessions scheduled for [period]. Check the Schedule screen to add sessions."
- [ ] EC-02: If a therapist has zero sessions scheduled in the selected period, their row still appears in the breakdown table with "0 / 0" and "—" for delivery rate — they are not silently dropped from the table
- [ ] EC-03: If the attendance data API returns an error, each section shows "Could not load attendance data — pull down to retry"; last-cached data is shown if available with a staleness label
- [ ] EC-04: If "Last 3 months" is selected and the center has been live for fewer than 3 months, the table renders with data for the available period and a note: "Showing [N] weeks of data — center launched [date]"

**Non-Functional Requirements:**
- Performance: All three sections render from a single API response (`GET /analytics/attendance?period={period}`); no per-section individual calls; renders ≤ 3s on 4G on minimum-spec Android
- Offline: Last-cached response for the last-selected period displayed with staleness label; period switching requires connectivity
- Accessibility: Delivery rate and attendance trend use text values and text labels — no chart where a label is color-only; touch targets ≥ 44dp; the "Below target" and "Missed N in a row" flags must be readable by a screen reader
- Privacy: Child first names visible in the attendance list are personal data of minors under DPDPA 2023 — RBAC-001: Director role required; access to full child record (on tap) triggers a separate RBAC check and AUDIT-001 access log entry; therapist-level delivery rates are personal data (staff as data principals under DPDPA) — access restricted to Director role; not surfaced to other roles
- Read-only: No attendance data can be edited from this screen

**Dependencies:**
- Blocked by: ANALYTICS-001 (home dashboard foundation), Journey 3 (Scheduling & Attendance — attendance data must exist)
- Enables: ANALYTICS-005 (Dropout Risk — shares attendance trend data); cross-links to Therapist Caseload Detail (ANALYTICS-004)

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android and desktop Chrome
- [ ] Period selector tested: all three periods render correct data; switching periods re-fetches within 3 seconds
- [ ] Therapist row tap and child row tap navigation tested
- [ ] EC-01 (no sessions in period), EC-02 (therapist with zero sessions), EC-04 (center < 3 months old) tested
- [ ] "Below target" flag and "Missed N in a row" badge text confirmed accessible (not color-only)
- [ ] Offline cached view tested
- [ ] Code reviewed and merged

---

## Story ANALYTICS-003: Billing and revenue overview

**As a** Rahul (Center Director)
**I want to** see at a glance how much revenue was generated this month, how much has been collected, how much is outstanding, and which families are overdue — without leaving the analytics module to piece this together from individual invoice records
**So that** I have financial visibility across the center and can quickly identify which families need a payment follow-up

**Inspired by:** Jane App revenue summary and collection rate card; SimplePractice practice health billing section; CentralReach financial dashboard. No Indian competitor has this feature; TherapEZ and PractiPal have billing management but no aggregate revenue analytics view.

**Context:** Rahul checks billing status at the start of the month and after invoice runs. He is on his phone most of the time but also reviews on his laptop. This screen is financial visibility only — invoice creation, payment recording, and UPI link generation happen in Journey 9 (Billing & Fee Collection), which is a separate module. This story provides the read-only financial summary and the overdue list with a direct link to the billing action screens.

**Acceptance Criteria:**
- [ ] AC-01: Given Rahul opens the Billing and Revenue Overview screen, then the screen loads within 3 seconds on 4G and displays a revenue summary card showing: total sessions delivered this month (count), total invoiced this month (₹ with ₹ symbol), total collected this month (₹), total outstanding this month (₹), and collection rate (% — calculated as collected / invoiced)
- [ ] AC-02: Given the revenue summary card is displayed, then the collection rate is shown as both a percentage text value and a visual fill bar (0–100% width) — the fill bar is accompanied by a percentage label so color and bar width are not the sole means of conveying the value
- [ ] AC-03: Given the screen is displayed, then a monthly revenue trend section shows the last 6 months as a plain number table — columns: Month | Invoiced (₹) | Collected (₹) | Collection Rate (%) — with the current month in the first row; no SVG or canvas chart library is used for this table; it renders as a styled HTML table with alternating row shading
- [ ] AC-04: Given the screen is displayed, then an overdue invoice list shows all families with an outstanding balance, sorted by days overdue descending — each row displays: child first name, parent name, outstanding amount (₹), invoice date, and days overdue as a text label ("Overdue by [N] days" — not color-coded only); the list header shows total outstanding and family count
- [ ] AC-05: Given Rahul taps a family row in the overdue list, then the screen navigates to that family's billing record screen in Journey 9 where Rahul can send a reminder, generate a UPI payment link, or record a manual payment
- [ ] AC-06: Given the total outstanding figure is displayed in the summary card, a "View all outstanding" link directly below the outstanding ₹ figure navigates to the full Outstanding Balance Dashboard (Journey 9)
- [ ] AC-07: Given Rahul opens the screen with no connectivity, then the last-cached revenue summary and overdue list are shown with a "Data as of [date] [time]" indicator; all action buttons that require connectivity (e.g., links to Journey 9 billing actions) are disabled with tooltip text: "Requires internet connection"
- [ ] AC-08: Given the screen is rendered in desktop Chrome, then the revenue summary card and overdue list render in a two-column layout (summary card left, overdue list right) on viewports ≥ 1024px; on narrower viewports the layout stacks vertically

**Edge Cases & Error States:**
- [ ] EC-01: If no invoices exist for the current month, the revenue summary card shows "No invoices this month" with ₹0 for all monetary fields and "—" for collection rate; the overdue list shows an empty state: "All families are up to date — no outstanding balances"
- [ ] EC-02: If total invoiced is ₹0 (no invoices issued), collection rate displays "—" rather than 0% to avoid a misleading metric
- [ ] EC-03: If the billing API returns an error, the screen shows "Could not load billing data — pull down to retry"; last-cached values shown with staleness label if available
- [ ] EC-04: If an overdue family has had their invoice voided or marked paid since the last cache sync, their row is still shown (from cache) with a staleness label; the stale row is not silently dropped — it remains visible until the next sync

**Non-Functional Requirements:**
- Performance: Revenue summary and overdue list render from a single API response (`GET /analytics/revenue?period=current_month`); ≤ 3s on 4G on minimum-spec Android
- Offline: Last-cached data shown with staleness indicator; navigation to Journey 9 billing action screens requires connectivity
- Accessibility: All monetary values include the ₹ symbol; collection rate uses both text and fill bar; days overdue uses text labels alongside any visual indicators; touch targets ≥ 44dp
- Privacy: Financial data (family names, outstanding amounts) is personal data under DPDPA 2023 — RBAC-001: Director and Admin/Billing roles only; Clinical Supervisor (Dr. Sunita) and Therapist (Priya) roles do not have access to this screen; all access logged in AUDIT-001
- Read-only: No payments, invoice creation, or status changes can be initiated from this screen; all actions link out to Journey 9

**Dependencies:**
- Blocked by: ANALYTICS-001 (home dashboard foundation), Journey 9 (Billing & Fee Collection — invoices must exist for any data to appear)
- Enables: Journey 9 screens (drill-through from overdue list rows)

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android and desktop Chrome
- [ ] Revenue summary card values verified against known test invoice dataset
- [ ] Collection rate fill bar confirmed accessible (text label present alongside fill bar)
- [ ] Monthly trend table confirmed as HTML table — no SVG/canvas chart library
- [ ] Overdue list sort order (days overdue descending) confirmed
- [ ] EC-01 (no invoices), EC-02 (₹0 invoiced) tested
- [ ] Drill-through to Journey 9 billing record screen confirmed
- [ ] RBAC: Dr. Sunita and Priya roles confirmed unable to access this screen
- [ ] Offline cached view tested
- [ ] Code reviewed and merged

---

## Story ANALYTICS-004: Staff utilization view

**As a** Rahul (Center Director)
**I want to** see how many sessions each therapist delivered this period, how many hours they worked, and how large their current caseload is — so I can identify therapists who are overloaded or underutilized and rebalance work before it creates a quality or retention problem
**So that** the center's clinical capacity is distributed evenly and no single therapist becomes a bottleneck or burnout risk

**Inspired by:** CentralReach staff utilization report; Jane App therapist schedule utilization view; Motivity staff productivity metrics. No Indian competitor has this feature.

**Context:** Rahul reviews staff utilization at least monthly, or when he notices a therapist seems stretched or has gaps in their schedule. He is on his phone most days but uses his laptop for deeper review. This is a read-only view — caseload assignment changes happen via the child record's Care Team tab, not from this screen.

**Acceptance Criteria:**
- [ ] AC-01: Given Rahul opens the Staff Utilization View, then the screen loads within 3 seconds on 4G and displays a therapist list showing for each therapist: therapist name, sessions delivered this month (count), hours delivered this month (calculated from session duration data), and current active caseload size (number of children assigned to them as primary therapist); list is sorted by caseload size descending by default
- [ ] AC-02: Given the therapist list is displayed, then a period selector at the top allows switching between "This month" (default) and "Last 3 months"; switching re-fetches and re-renders the sessions delivered and hours delivered figures within 3 seconds on 4G; caseload size always reflects current assignment (not period-specific)
- [ ] AC-03: Given a therapist's sessions delivered count is rendered, then a text-labeled flag appears if their delivery rate (sessions delivered / sessions scheduled) is below 70% — flag text: "Low delivery rate — [N]% this month" alongside a warning icon; the flag uses icon + text, not color alone
- [ ] AC-04: Given Rahul taps a therapist row, then the screen navigates to the Therapist Caseload Detail screen for that therapist, showing the full list of children assigned to them with last session date and overdue flags
- [ ] AC-05: Given the screen is displayed, then a summary header shows: total therapists on staff (count), total sessions delivered across all therapists this month (count), total clinical hours delivered this month (sum), and average caseload size (mean active children per therapist)
- [ ] AC-06: Given Rahul opens the screen with no connectivity, then the last-cached utilization data is shown with a "Data as of [date] [time]" indicator; the period selector is visible but switching periods while offline shows "Period data not available offline — showing last cached view"

**Edge Cases & Error States:**
- [ ] EC-01: If a therapist has been added to the staff roster but has no sessions scheduled in the selected period, they still appear in the list with sessions delivered = 0, hours delivered = 0h, and their current caseload count; they are not silently dropped
- [ ] EC-02: If a therapist has no children assigned to their caseload, their caseload count shows 0 (not "—") and a note "No active caseload" in the row
- [ ] EC-03: If the utilization API returns an error, the screen shows "Could not load utilization data — pull down to retry"; last-cached data shown with staleness label if available
- [ ] EC-04: If "Last 3 months" is selected and the center has fewer than 3 months of data, the view renders with available data and a note: "Showing [N] weeks of data — center launched [date]"

**Non-Functional Requirements:**
- Performance: Therapist list and summary header render from a single API response (`GET /analytics/utilization?period={period}`); ≤ 3s on 4G on minimum-spec Android
- Offline: Last-cached data for last-selected period shown with staleness indicator
- Accessibility: All utilization figures are text values — no chart where a number is color-coded only; "Low delivery rate" flag uses icon + text; touch targets ≥ 44dp
- Privacy: Therapist performance data (sessions delivered, hours worked, delivery rate) is personal data under DPDPA 2023 (staff as data principals) — RBAC-001: Director role only; not accessible to Dr. Sunita, Priya, or Admin/Billing roles; purpose limitation: internal operations use only; not to be exported or shared externally without staff consent
- Read-only: No caseload reassignment, scheduling changes, or staff edits can be initiated from this screen

**Dependencies:**
- Blocked by: ANALYTICS-001 (home dashboard foundation), Journey 3 (Scheduling & Attendance — session delivery data must exist)
- Enables: Therapist Caseload Detail screen (drill-through from therapist row tap)

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android and desktop Chrome
- [ ] Period selector tested for both "This month" and "Last 3 months"
- [ ] "Low delivery rate" flag confirmed as icon + text (not color-only)
- [ ] Therapist row tap navigates to correct Therapist Caseload Detail screen
- [ ] EC-01 (therapist with zero sessions) and EC-02 (therapist with empty caseload) tested
- [ ] RBAC: Dr. Sunita and Priya roles confirmed unable to access this screen
- [ ] Offline cached view tested
- [ ] Code reviewed and merged

---

## Story ANALYTICS-005: Dropout risk indicators

**As a** Rahul (Center Director)
**I want to** see a list of children who have missed N consecutive sessions or who have not attended in more than X days — with configurable thresholds — so I can identify families at risk of quietly withdrawing and contact them before dropout becomes permanent
**So that** I can act early enough for outreach to make a difference, rather than discovering dropout after the family has already gone silent

**Inspired by:** CentralReach dropout risk alerts; Motivity attendance risk flags; Hi Rasmus caseload health indicators. No Indian competitor has automated dropout risk detection. This is a differentiator in the Indian market.

**Context:** Rahul reviews dropout risk at the start of each week and at month-end. On the home dashboard, a "Dropout risk flags" tile surfaces the count of flagged children (ANALYTICS-001). This story is the detail screen behind that tile — the full list with drill-down and a quick-action link to Journey 10 (Dropout Prevention). Dr. Sunita does not have access to this screen. Risk flag thresholds are configurable at the center level by Rahul.

**Acceptance Criteria:**
- [ ] AC-01: Given Rahul opens the Dropout Risk Indicators screen, then the screen loads within 3 seconds on 4G and displays a list of all children who meet either of two risk conditions: (a) N or more consecutive sessions missed (default threshold: 2), or (b) gap since last attended session is > X days (default threshold: 14 days); children meeting both conditions appear once, not twice
- [ ] AC-02: Given the risk list is displayed, then each row shows: child first name, primary therapist name, last attended session date (or "No sessions attended yet"), consecutive missed sessions count (if applicable), days since last attended session (integer), and a risk level badge — badge displays icon + text: amber badge = "At risk" (2–3 consecutive missed), red badge = "High risk" (4+ consecutive missed or > 30 days gap); badge is never color-only
- [ ] AC-03: Given a child row is displayed, then a "Contact now" quick action button is visible in the row; tapping "Contact now" navigates directly to the child's contact screen in Journey 10 (Dropout Prevention follow-up flow), passing the child ID and last session context so Rahul does not need to re-identify the child; tapping the child name row itself opens the child's full record
- [ ] AC-04: Given Rahul wants to adjust risk thresholds, when he taps "Settings" or a threshold indicator at the top of the screen, then a threshold configuration panel opens with two configurable fields: (a) "Flag after [N] consecutive missed sessions" (integer input, default 2, minimum 1, maximum 10); (b) "Flag if no session in [X] days" (integer input, default 14, minimum 7, maximum 90); tapping "Save" persists the thresholds at the center level and immediately re-computes the list
- [ ] AC-05: Given thresholds are saved, then the new threshold values are stored as center-level configuration; all subsequent risk flag computations (including the home dashboard tile count in ANALYTICS-001) use the updated thresholds; threshold changes are logged in AUDIT-001 with: changed_by, changed_at, old_value, new_value
- [ ] AC-06: Given the risk list is rendered, then a summary header shows: total children flagged (count), children flagged amber (count), children flagged red (count), and the currently active threshold values ("Flagging after [N] consecutive missed sessions or [X]+ day gap")
- [ ] AC-07: Given a child has been formally placed on a planned leave of absence (logged in the system by Rahul or admin), then that child does not appear in the dropout risk list, regardless of how many sessions have been missed; a center-initiated cancellation is not counted toward the consecutive-missed threshold
- [ ] AC-08: Given Rahul opens the screen with no connectivity, then the last-cached risk list is shown with a "Data as of [date] [time]" indicator; "Contact now" buttons are visible but the Journey 10 navigation requires connectivity — tapping while offline shows a toast: "You need an internet connection to view contact details"

**Edge Cases & Error States:**
- [ ] EC-01: If no children currently meet the risk thresholds, the screen shows an empty state: "No children are currently flagged at your threshold settings. Thresholds: [N] consecutive missed / [X]+ day gap." — not a blank screen
- [ ] EC-02: If Rahul enters an invalid threshold value (e.g., 0 or non-integer), inline validation appears: "Enter a number between 1 and 10" (for consecutive missed) or "Enter a number between 7 and 90" (for day gap); the Save button is disabled until valid values are entered
- [ ] EC-03: If a child's last attended session date is unknown (no sessions ever recorded), they appear in the risk list only if they have been enrolled for more than X days; they are not flagged if they were enrolled within the last X days
- [ ] EC-04: If the risk list API returns an error, the screen shows "Could not load risk data — pull down to retry"; last-cached list shown with staleness label if available
- [ ] EC-05: If "Contact now" is tapped for a child whose parent contact details have not been entered in the system, the Journey 10 contact screen opens with a prompt: "No contact number on file for this family — add it from the child's profile"

**Non-Functional Requirements:**
- Performance: Risk list renders from a single API response (`GET /analytics/dropout-risk`); risk flags are pre-computed by the PROG-004 background job — not calculated on page load; list renders ≤ 3s on 4G on minimum-spec Android; threshold save and list re-computation triggered via `PATCH /center/risk-thresholds`; re-computation background job runs asynchronously — screen shows "Recalculating..." spinner while the updated list is being computed (typically ≤ 5 seconds server-side)
- Offline: Last-cached risk list shown with staleness indicator; threshold configuration requires connectivity; "Contact now" navigation requires connectivity
- Accessibility: Risk badges use icon + text label alongside any color — amber = warning icon + "At risk" text, red = alert icon + "High risk" text; touch targets ≥ 44dp; threshold fields are labeled inputs, not bare number fields
- Privacy: Child first names and last session dates are personal data of minors under DPDPA 2023 — RBAC-001: Director role only; parent contact details surfaced via "Contact now" → Journey 10 are lazy-loaded at Journey 10 entry point with a separate RBAC check and AUDIT-001 log entry; threshold configuration changes logged in AUDIT-001
- Read-only: This screen displays risk data only; dropout follow-up actions happen in Journey 10, not here

**Dependencies:**
- Blocked by: ANALYTICS-001 (home dashboard, which surfaces the risk count tile), Journey 3 (attendance data must exist for risk computation), PROG-004 background job (dropout-risk flag computation — must be operational before this screen has data)
- Enables: Journey 10 (Dropout Prevention follow-up flow — "Contact now" links directly into that journey)

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android and desktop Chrome
- [ ] Threshold configuration tested: change both thresholds, save, confirm list re-computes with new values
- [ ] Risk badge confirmed as icon + text + color (not color-only) for both amber and red levels
- [ ] "Contact now" tap navigates to correct child in Journey 10 with child ID passed correctly
- [ ] EC-01 (empty state), EC-02 (invalid threshold input), EC-03 (child with no sessions), EC-05 (no contact on file) tested
- [ ] Planned leave exclusion tested: child on leave does not appear in risk list
- [ ] Center-initiated cancellations excluded from consecutive-missed count confirmed
- [ ] AUDIT-001 log entries for threshold changes verified
- [ ] RBAC: Dr. Sunita and Priya roles confirmed unable to access this screen
- [ ] Offline cached view tested; "Contact now" offline toast confirmed
- [ ] Code reviewed and merged

---

## Backlog Summary

| Story ID | Title | Persona | Complexity | Priority | Blocked by |
|---|---|---|---|---|---|
| ANALYTICS-001 | Center director home dashboard | Rahul | M | P0 | AUTH-001, Journey 3, Journey 9 |
| ANALYTICS-002 | Attendance analytics | Rahul | M | P0 | ANALYTICS-001, Journey 3 |
| ANALYTICS-003 | Billing and revenue overview | Rahul | M | P0 | ANALYTICS-001, Journey 9 |
| ANALYTICS-004 | Staff utilization view | Rahul | M | P1 | ANALYTICS-001, Journey 3 |
| ANALYTICS-005 | Dropout risk indicators | Rahul | L | P0 | ANALYTICS-001, Journey 3, PROG-004 |

**Complexity:**
- S: Single element, single call, ≤ 1 day
- M: Single screen or flow, 2–3 days
- L: Multi-screen or complex state, 3–5 days
- XL: Should be split before sprint planning

**Priority:**
- P0: Core path — product doesn't function without this
- P1: Important — ships with v1
- P2: Enhancement — next iteration

**Sprint recommendation:** ANALYTICS-001 is the foundation — it must be built and merged first. ANALYTICS-002, ANALYTICS-003, and ANALYTICS-005 can be built in parallel once ANALYTICS-001 is merged. ANALYTICS-004 has no hard dependency on the other analytics stories and can be built in parallel with ANALYTICS-002/003/005, but is P1 rather than P0 because center directors can operate without utilization data if attendance and billing are live. PROG-004 (dropout risk background job) is a hard dependency for ANALYTICS-005 — confirm it is in the same sprint or the one prior.

---

## Pre-Build Decisions Required

| # | Decision | Owner | Needed by |
|---|---|---|---|
| PBD-01 | Confirm the six home dashboard tiles are the correct priority and ordering — specifically whether Outstanding Invoices should be tile 1 or whether another metric (sessions today, attendance rate) should lead | Product | Before ANALYTICS-001 sprint |
| PBD-02 | Confirm default risk thresholds (currently: 2 consecutive missed sessions, 14-day gap) — validate these against any field data before hardcoding defaults | Product | Before ANALYTICS-005 sprint |
| PBD-03 | Confirm whether Dr. Sunita should see any analytics screens beyond the Therapist Caseload Detail — currently she is scoped to caseload-only; if she needs attendance trend data for her caseload, scope this explicitly before sprint | Product | Before ANALYTICS-002 sprint |
| PBD-04 | Confirm background job schedule for PROG-004 dropout-risk computation (every 6 hours, on attendance mark, or on page load for first open of the day) — determines staleness of risk flags on the home tile | Engineering | Before ANALYTICS-001 sprint |
| PBD-05 | Confirm whether the 6-month revenue trend table should extend to the full life of the center (not capped at 6 months) once the center passes the 6-month mark — product decision on data retention window for analytics | Product | Before ANALYTICS-003 sprint |
| PBD-06 | Confirm the responsive layout breakpoints for desktop Chrome — specifically whether desktop is treated as a fully separate layout or an adaptive version of the mobile layout | Engineering / Design | Before ANALYTICS-001 sprint |

---

## ⚠️ Feature Factory Disclaimer

These stories were defined by journey document synthesis, competitive observation, and category assumption — not by validated primary research with Indian autism therapy center directors.

**What we assumed but have not validated:**
- [ASSUMPTION] Rahul checks a digital operational summary on a regular cadence (daily or weekly). If his center has fewer than 15 children and he knows every family personally, a formal analytics screen may not change his behavior at all — he may already have the mental model without needing a dashboard. Validate via director interviews (H-09, H-18).
- [ASSUMPTION] The six home dashboard tiles in ANALYTICS-001 reflect Rahul's actual priority hierarchy. "Outstanding invoices" is placed as the financially prominent tile based on the inference that BP-06 (billing pain) is the primary operational tension for Indian center directors. This ordering has not been confirmed by asking Rahul directly what number he wants to see first when he opens the app.
- [ASSUMPTION] The default risk thresholds (2 consecutive missed sessions, 14-day gap) in ANALYTICS-005 are operationally meaningful for Indian autism therapy families. These values are modeled on US ABA dropout literature, where early intervention at 2 missed sessions is cited. Whether Indian families have a similar dropout pattern — or whether the threshold should be higher or lower given cultural norms around communication and re-engagement — has not been validated in primary research.
- [ASSUMPTION] Rahul will use the "Contact now" quick action in ANALYTICS-005 to reach families directly from the dropout risk list. This assumes he is comfortable using the platform to initiate family contact rather than using his personal WhatsApp. The platform must complement, not compete with, his existing WhatsApp behavior.
- [ASSUMPTION] Staff utilization metrics (sessions delivered, hours worked, delivery rate per therapist) will be received neutrally by Rahul as management information, not as surveillance data that creates trust issues with his clinical staff. In a small founder-led center where Rahul works alongside his team daily, framing this data as operational health rather than performance monitoring will be important. This has not been tested with Indian center directors.
- [ASSUMPTION] The analytics dashboard provides value at launch when the platform has only weeks of data. If a center starts using the platform at month 1 and the trend tables show "Not enough data yet" for 3 of the 5 analytics screens, the perceived value of the analytics module will be low until sufficient data history accumulates. The onboarding experience for analytics (empty states, "check back next month" messages) needs particular design attention.

**What a researcher would ask before building this:**
- What does Rahul's Monday morning or month-end actually look like today? Does he open Excel, call a staff member, scroll WhatsApp, or simply know the numbers in his head? The dashboard entry point hierarchy must reflect real behavior, not a product manager's assumption about what matters most. (H-09, H-18 are the closest hypotheses but do not address the analytics workflow specifically.)
- Would Rahul use a "Contact now" button from a risk list, or would he prefer to WhatsApp the parent himself from his personal phone? If he sees the dropout risk list as a trigger to open WhatsApp rather than use an in-app contact flow, the Journey 10 integration design needs to account for this handoff behavior.
- How does Dr. Sunita currently prioritize her weekly caseload review? If she already has a weekly check-in cadence with Priya or a written schedule, a digital caseload view may add to her process rather than replace anything. Understanding whether the supervisor caseload detail screen (reachable from ANALYTICS-004) fits into a real workflow is critical before investing in its flags and overdue indicators.

**What the Product Consultant would challenge:**
- The analytics cluster is downstream of Journey 3 (attendance), Journey 9 (billing), and PROG-004 (dropout risk background job). If those modules are not live and generating reliable data, the analytics dashboard will be empty or misleading at launch. This is not just a sprint-planning dependency — it is a go-live gate. The analytics module should not be positioned as a launch feature until at least 4–6 weeks of upstream data exists in the system. Consider a soft-launch strategy where analytics is live but the home tile directs to an "analytics available in [N] weeks" message until minimum data thresholds are met.
- ANALYTICS-005 (dropout risk) includes configurable thresholds and a background computation job. For a v1, consider whether a simpler version — a manually-sorted list of children with the longest gap since their last session, with no automated flagging — delivers equivalent director value with half the engineering complexity. The threshold configuration panel and background job infrastructure in ANALYTICS-005 can be deferred if field validation confirms that a sorted list is sufficient for the first 90 days of use.

**Risk level per output:**

| Story | Risk level | Primary risk |
|---|---|---|
| ANALYTICS-001 Home Dashboard | Low-Medium | Five of six tiles depend on upstream data quality from Journey 3 and Journey 9; risk is data availability at launch, not build complexity |
| ANALYTICS-002 Attendance Analytics | Low-Medium | Upstream dependency on Journey 3; value is directly proportional to how reliably Priya marks attendance; if attendance marking adoption is low, this screen is inaccurate |
| ANALYTICS-003 Billing and Revenue Overview | Low | Directly mirrors invoice and payment data from Journey 9; financial metrics are well-defined; risk is upstream data completeness, not analytics logic |
| ANALYTICS-004 Staff Utilization View | Medium | Therapist performance data creates DPDPA staff-as-data-principal considerations; framing risk (surveillance vs. operations) may affect adoption; not validated with Indian center directors |
| ANALYTICS-005 Dropout Risk Indicators | Medium-High | Background job dependency (PROG-004); threshold defaults are not validated for Indian context; "Contact now" integration with Journey 10 adds cross-journey complexity; effectiveness of automated risk flagging in changing Rahul's behavior is assumed, not confirmed |

Use the `/researcher` agent to validate H-09 (director metric-checking behavior and priority hierarchy) and H-18 (dropout detection cadence) before sprint planning.
Use the `/product-consultant` agent to pressure-test the upstream data dependency gating strategy and to challenge whether ANALYTICS-005 threshold configuration belongs in v1 or a later iteration.
Use the `/design-critique` agent to review the home dashboard tile layout on a 360dp-wide viewport and the dropout risk list on both mobile and desktop before prototyping.
