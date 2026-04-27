# User Journey: Analytics Dashboard

**Previously:** J8 | ✅ **IN SCOPE — MVP**
**Trigger:** Rahul opens the platform at the start of the week (or at month-end) to get a picture of how the centre is performing — attendance, revenue, caseload, and dropout risk
**Primary actor:** Rahul — Centre Director / Founder
**Supporting actors:** System (aggregates data from attendance, billing, session notes, and caseload records); Dr. Sunita (secondary — sees her own caseload slice within the same dashboard entry point)
**Entry condition:** At least one billing cycle has been run (invoices exist), at least one week of attendance has been marked, and at least one child is enrolled and active with DPDPA consent confirmed
**End state:** Rahul has reviewed centre-level KPIs, identified children at dropout risk or with outstanding fees, drilled into at least one therapist's caseload, and either exported a monthly summary report or queued a background export for download
**Journey source documents:**
- `cluster-5-analytics-compliance-access.md` — Stories PROG-001 through PROG-005, ANLT-001 through ANLT-005 (as ANALYTICS-001 through ANALYTICS-004), EXPORT-001 through EXPORT-005
- `cluster-3-billing-payments.md` — Stories INV-004, INV-005, UPI-004
- `cluster-4-scheduling-communication.md` — Story REMIND-002
- `cluster-2-patient-records-intake.md` — Stories MPM-003, MPM-005

---

## Discovery Context

**MVP Scope:** ✅ IN SCOPE — MVP

**Pain points & friction:**
- No single view of center health exists today — revenue, attendance, and clinical status are held in separate, incompatible sources 🔵 Inferred from product context
- Key operational metrics (collection rate, utilization, dropout risk) are invisible until they become crises 🔵 Inferred
- Manual Excel reconciliation of attendance and fees is backward-looking — by the time it is assembled, the data is stale 🔵 Inferred
- No enrollment pipeline view: Rahul has no structured way to track the inquiry → enrolled → active → at-risk → dropout funnel 🔶 [HYPOTHESIS]

**Emotional states:**
- Rahul: Currently operating on intuition and retrospective data — problems are discovered after they have already escalated. A real-time dashboard is a qualitative shift in how the center is managed. 🔵 Inferred from "no single system" context
- Rahul: Risk of dashboard overload — he needs a prioritised summary that flags what needs action, not a raw data grid. 🔶 [HYPOTHESIS]

**Current workarounds:**
- Rahul maintains a mental model of which families are "at risk" based on personal relationships and gut instinct 🔶 [HYPOTHESIS]
- Monthly Excel spreadsheet reconciling attendance and payments is the closest current approximation of a center dashboard 🔶 [HYPOTHESIS]

**⚠️ DPDPA exposure:**
- Exported reports containing child names, attendance records, and clinical data must be handled under DPDPA 2023 — session-bound download links and audit logging are required; bulk export without per-child consent checks is a compliance risk 🔵 Inferred structural gap
- Parent contact data surfaced from dropout-risk flags (child contact screen) is personal data under DPDPA — access must be RBAC-gated and logged even when the use is operationally justified 🔵 Inferred

---

## Step-by-Step Flow

| Step | Actor | Action | Screen / State | Technical Note |
|---|---|---|---|---|
| 1 | Rahul | Opens the platform app on Android phone | Home screen / App launch | RBAC-001 gate: Director role authenticated. Session token checked. If session expired, 2FA re-prompt fires before any data loads. |
| 2 | System | Renders the Home screen with a persistent outstanding-fees banner | Home screen — Director view | API: `GET /director/home-summary`. Response payload includes: total outstanding fees this month, count of dropout-risk children (amber + red flags), count of unresolved admin flags. This summary must render within 3 seconds on 4G. Outstanding fees figure is the first number surfaced — no tap required to see it. |
| 3 | Rahul | Reads the outstanding fees banner and taps "View outstanding" | Home screen → Billing Outstanding screen | The banner surfaces the total outstanding amount (₹ figure) and a count of families with overdue balances. Tap navigates to UPI-004 outstanding balance dashboard. RBAC: Admin/Billing and Director roles only. |
| 4 | System | Renders the Outstanding Balance dashboard | Outstanding Balance screen | API: `GET /billing/outstanding`. Returns list of families sorted by days overdue (default). Summary row at top: total outstanding, family count, count > 30 days overdue. Performance: ≤ 3s for up to 100 families. |
| 5 | Rahul | Reviews overdue list, taps a high-priority family row | Child billing profile screen | Navigates to the family's billing record. Actions available: Send Reminder (WhatsApp via WA-005 or SMS via REMIND-003), Generate Payment Link (UPI-001), View Payment History (UPI-003). |
| 6 | Rahul | Taps "Send Reminder" for one or more overdue families | WhatsApp share intent / Reminder confirmation | If parent is WhatsApp-opted-in (WA-003), WhatsApp Business API template fires (WA-005). If not opted in, REMIND-003 SMS fallback is used. Delivery logged in REMIND-005 log. |
| 7 | Rahul | Navigates back to Home screen, taps the dropout-risk section | Progress Dashboard — Centre Summary screen | Dropout-risk children are surfaced proactively in a "Needs attention" section at the top of the Progress Dashboard. No secondary navigation required — this section is visible without scrolling on a 5–6 inch screen. API: `GET /progress/centre-summary`. |
| 8 | System | Renders centre-level attendance and goal health summary | Progress Dashboard — Centre Summary screen | PROG-002: Director sees all active children. Amber and red risk flags calculated by PROG-004 background job (consecutive missed sessions against configurable threshold). Chart rendering must complete in ≤ 4s on 4G. All charts are lightweight — number tables and simple bar indicators, no heavy chart library. |
| 9 | Rahul | Reviews "Needs attention" section — children flagged amber or red | Progress Dashboard — Needs Attention section | PROG-004: Amber flag = 2+ consecutive missed sessions (default). Red flag = 4+ consecutive missed sessions. Flags show icon + text + color (not color alone). Centre-initiated cancellations excluded from threshold count. |
| 10 | Rahul | Taps a high-risk child's dropout flag badge | Child contact screen — surfaced from dropout flag | PROG-004 AC-04: Tapping the risk badge goes directly to the child's contact screen with parent WhatsApp number as the primary action. One tap to initiate contact via WhatsApp. DPDPA: RBAC check before exposing parent contact data. |
| 11 | Rahul | Navigates to the Analytics tab | Analytics tab | Analytics tab is a persistent bottom-nav item. Contains: Revenue section, Utilization section, Caseload / Enrollment section. |
| 12 | System | Renders the Revenue dashboard | Analytics — Revenue screen | ANALYTICS-001: Total invoiced this month, total collected, total outstanding, collection rate (%). Renders in ≤ 4s on 4G. Outstanding figure here cross-references the billing dashboard from Step 4. |
| 13 | Rahul | Reviews revenue metrics, optionally taps "By therapist" on Utilization section | Analytics — Utilization screen | ANALYTICS-002: Sessions scheduled vs. delivered, cancellations (centre vs. family), utilization rate per therapist. Therapists with < 70% utilization flagged amber. |
| 14 | Rahul | Reviews therapist caseload, taps enrollment vs. attrition section | Analytics — Caseload / Enrollment screen | ANALYTICS-003: Active child count per therapist, 6-month rolling enrollment vs. exits as a number table (not a chart). Children with last session > 30 days and no formal exit show as "Likely inactive — confirm status." |
| 15 | Rahul | Drills into a specific therapist's caseload | Dr. Sunita's caseload slice (or any therapist) | Rahul taps a therapist row from the caseload view. This navigates to the supervisor-style caseload dashboard (MPM-003 / MPM-005) scoped to that therapist's assigned children. Rahul as Director has full access — no RBAC restriction. |
| 16 | System | Renders the selected therapist's caseload view | Therapist caseload detail screen | MPM-003 + MPM-005: Child name, last session date, last program update date, overdue flags (session > 7 days, program update > 30 days). Filter by "Overdue flags only" available. Performance: ≤ 3s for up to 50 children. |
| 17 | Rahul | Taps a child row to confirm details or review record | Child record — Program/Data tab | Rahul lands on the Program/Data tab (most relevant for operational review). Full read and edit access per MPM-005 AC-05. DPDPA: RBAC check confirmed at record open. Access logged in AUDIT-001. |
| 18 | Rahul | Returns to Analytics tab, taps "Export monthly report" | Analytics — Export modal | ANALYTICS-004: Rahul selects month/year and toggles which sections to include (Revenue, Utilization, Enrollment). Export triggers a background job — Rahul does not wait on-screen. |
| 19 | System | Background job generates the monthly operations report PDF | Background job — PDF generation | ANALYTICS-004 + AUDIT-001: PDF generated server-side. Contains: centre name, selected month, all toggled sections with metrics, footer with generation date and "Confidential." Audit log entry created immediately on export initiation. Performance: ≤ 10s. |
| 20 | System | Delivers in-app notification when export is ready | In-app notification | Rahul receives a push notification: "Your monthly report for [Month] is ready — tap to download." Download link is session-bound and expires after 24 hours (same pattern as EXPORT-003). |
| 21 | Rahul | Taps notification, downloads PDF | Download screen / native share sheet | PDF downloaded to device Downloads folder. Android share sheet triggered (can share to WhatsApp, email, Drive). Audit log entry updated: export completed, download confirmed. |
| 22 | System | Journey complete | — | Rahul has reviewed outstanding fees, actioned at least one overdue family, reviewed dropout-risk children, drilled into a therapist's caseload, and has a monthly report downloaded or in progress. |

---

## Decision Points

### Decision 1: Outstanding fees — does Rahul need to take action?
**At step:** 4–6
**Question:** Are there families with outstanding balances, and does Rahul want to act on them now or defer?
- **Path A — Act now (happy path):** Outstanding balances exist. Rahul reviews the list, taps one or more families, sends a reminder or payment link. → Continue at Step 7.
- **Path B — No outstanding balances:** Outstanding balance dashboard shows empty state: "All families are up to date. No outstanding balances." Rahul returns to home screen. → Skip to Step 7.
- **Path C — Defers action:** Rahul sees the list but chooses not to act. Returns to home screen without sending any reminders. → Skip to Step 7. (No system consequence; outstanding balances remain and automated overdue reminders from INV-005 / REMIND-003 continue to run on schedule.)

---

### Decision 2: Dropout risk — are at-risk children present?
**At step:** 7–10
**Question:** Does the "Needs attention" section contain any flagged children?
- **Path A — Flagged children present (happy path):** At least one amber or red flag exists. Rahul reviews, taps the contact shortcut for one or more children, and initiates outreach. → Continue at Step 11.
- **Path B — No flagged children:** "Needs attention" section is absent or shows "No children at risk this week." Rahul scrolls past to the full child list. → Continue at Step 11.
- **Path C — Child is on confirmed leave:** Admin has previously flagged the child as on a planned leave of absence. Risk flag is suppressed (PROG-004 EC-02). Rahul sees no flag for this child even if sessions were missed. → Rahul continues with other children; no outreach action required.

---

### Decision 3: Analytics depth — does Rahul drill into therapist caseload?
**At step:** 14–17
**Question:** Does Rahul want to drill into a specific therapist's caseload after reviewing aggregate metrics?
- **Path A — Drills in (happy path):** Rahul taps a therapist row to see their caseload detail. Reviews individual children. May open one or two child records. → Continue at Step 18.
- **Path B — Skips drill-down:** Rahul is satisfied with aggregate-level metrics and does not drill into any therapist. → Continue at Step 18.
- **Path C — Dr. Sunita independently opens Supervisor Dashboard:** Dr. Sunita enters the platform separately and lands on the MPM-003 Supervisor Caseload Dashboard filtered to her own assigned children. This is a parallel path — not dependent on Rahul's session. She sees the same data Rahul would see for her caseload, scoped to her RBAC role (her children only). Dr. Sunita cannot see revenue data or centre-wide metrics.

---

### Decision 4: Export — immediate or background?
**At step:** 18–21
**Question:** Is the export for immediate use, or can Rahul trigger it and come back?
- **Path A — Background export (happy path):** Rahul taps "Export monthly report," confirms section selection, and leaves the screen. Job runs in background. Notification arrives when done. → Continue at Step 20.
- **Path B — No export needed:** Rahul reviews analytics on-screen and does not trigger an export this session. Journey ends at Step 17.
- **Path C — Export fails:** PDF generation fails on the server. Rahul sees in-app error: "Export failed — check your connection and try again" with a retry button. Audit log records the failed attempt. Rahul retries. → Retry at Step 18.
- **Path D — Child progress export (separate path):** Dr. Sunita, within this same session or independently, triggers PROG-005 (Export progress summary for a child as PDF) from a child's progress card. This is a single-child export, not a centre operations report. It runs as a foreground job (≤ 5s for a one-page summary). Audit log entry created. PDF saved to device and share sheet triggered.

---

### Decision 5: Empty data states (newly onboarded centre)
**At step:** 2, 7, 12
**Question:** Has the centre produced any data yet? (Relevant for new centre onboarding or first-time use.)
- **Path A — No invoices yet:** Revenue dashboard shows empty state: "No invoices this month — get started by creating your first invoice." → Revenue section non-actionable. Rahul returns to other sections.
- **Path B — No attendance data yet:** Progress dashboard shows empty state: "No active children enrolled yet — add your first child to get started." → Dropout risk section does not render. Rahul exits to child enrollment flow.
- **Path C — No session data but children enrolled:** Children are enrolled and have DPDPA consent, but no sessions have been marked attended yet. Dashboard renders with child cards showing "No sessions scheduled yet" (PROG-001 EC-01) — no false 0% attendance risk flags. Caseload shows children with "No sessions recorded" (MPM-003 EC-02).

---

## Screen Inventory

| Screen name | Purpose | Primary action | Personas who see it | Source story |
|---|---|---|---|---|
| Home screen — Director view | First surface Rahul sees; shows outstanding fees and dropout-risk alerts without any tap | Tap outstanding fees banner or tap dropout-risk section | Rahul (Director) | PROG-002, ANALYTICS-001, PROG-004 |
| Outstanding Balance Dashboard | Lists all families with open balances, sorted by days overdue, with total outstanding summary | Send reminder or tap family row to drill in | Rahul (Director), Admin/Billing role | UPI-004, INV-004 |
| Child Billing Profile | Per-family fee record showing invoice history, outstanding amount, payment history, and action buttons | Send payment link or record manual payment | Rahul (Director), Admin/Billing role | UPI-003, INV-003, INV-004, WA-005 |
| Progress Dashboard — Centre Summary | Centre-wide view: total active children, centre attendance rate, dropout-risk count, Needs Attention section with flagged children | Tap at-risk child card or tap "View all children" | Rahul (Director) | PROG-002, PROG-004 |
| Progress Dashboard — Supervisor View (Dr. Sunita) | Caseload-scoped version of the Progress Dashboard for Dr. Sunita; shows only her assigned children | Tap child card to open record | Dr. Sunita (Supervisor) | PROG-001, PROG-003, MPM-003 |
| Child Progress Card | Single-child attendance trend (last 4 weeks), goal completion rate indicator, dropout-risk badge | Tap to open attendance timeline detail or tap risk badge for contact shortcut | Rahul (Director), Dr. Sunita (Supervisor) | PROG-001, PROG-003, PROG-004 |
| Child Contact Screen (from risk flag) | Surfaces parent WhatsApp number as primary action when tapped from a dropout-risk badge | Tap WhatsApp number to initiate contact | Rahul (Director) | PROG-004 |
| Analytics Tab — Revenue Screen | Monthly revenue: invoiced, collected, outstanding, collection rate | Tap "View outstanding" or "Export" | Rahul (Director), Admin/Billing role | ANALYTICS-001 |
| Analytics Tab — Utilization Screen | Session delivery vs. scheduled by therapist; utilization rate; cancellation breakdown | Tap "By therapist" to see individual breakdown | Rahul (Director) | ANALYTICS-002 |
| Analytics Tab — Caseload / Enrollment Screen | Therapist caseload counts, 6-month enrollment vs. attrition table, likely-inactive list | Tap therapist row to drill into caseload detail | Rahul (Director) | ANALYTICS-003 |
| Therapist Caseload Detail Screen | Children assigned to a specific therapist; last session date, program update date, overdue flags | Tap child row to open child record | Rahul (Director), Dr. Sunita (Supervisor — own caseload only) | MPM-003, MPM-005 |
| Export Modal (Monthly Operations Report) | Section selection and month picker for centre operations PDF export | Confirm export (triggers background job) | Rahul (Director) | ANALYTICS-004 |
| Export Notification / Download Screen | In-app notification that export is ready; tapping opens download with native share sheet | Download PDF | Rahul (Director) | ANALYTICS-004, EXPORT-003 |
| Child Progress Export (PDF) | Single-child export: attendance summary, goal mastery list, reporting period | Download PDF (foreground, ≤ 5s) | Dr. Sunita (Supervisor), Rahul (Director) | PROG-005, EXPORT-001 |

---

## Designer Handoff

### Screen: Home screen — Director view

**Purpose:** Give Rahul the one number he needs in under 3 seconds (total outstanding fees this month) and surface dropout-risk alerts without requiring any navigation.
**Primary action:** Tap outstanding fees banner → navigate to Outstanding Balance Dashboard
**Entry point(s):** App launch (authenticated Director session)
**Exit point(s):** Tap outstanding fees banner → Outstanding Balance Dashboard; tap dropout-risk section → Progress Dashboard Centre Summary; tap Analytics tab → Analytics tab

**Key components:**
- Outstanding fees banner (persistent, top of screen, prominent ₹ figure): total outstanding this month + family count with overdue balances. Must be the first data element rendered.
- Dropout-risk alert strip: count of amber-flagged children and red-flagged children with a "Review now" tap target. Renders below the fees banner.
- Bottom navigation bar: Home / Schedule / Children / Analytics / Settings (standard Director navigation)
- Secondary summary strip (below alerts): total active children, centre attendance rate this month (single percentage), sessions today (count)

**States:**
- **Empty state:** Centre has zero invoices and zero sessions marked yet. Banner reads "No fee data yet — create your first invoice to start tracking revenue." Dropout-risk strip reads "No children enrolled yet." Secondary summary reads "0 active children."
- **Loading state:** Skeleton cards render in the banner and alert strip positions while the API call resolves. Skeleton must be visible for the minimum — no flash of blank screen.
- **Error state:** If the `GET /director/home-summary` API fails, banner reads "Could not load summary — pull down to retry" with a manual refresh handle. Last-cached values are shown with a staleness timestamp.
- **Offline state:** Cached home summary shown with a "Last updated [date/time]" label in the banner strip. Outstanding fees and dropout-risk counts reflect last-synced data. No payment or reminder actions available while offline.

**Constraints:**
- The outstanding fees ₹ figure must be legible at a glance on a 5–6 inch screen without any tap. Use large type (≥ 28sp). Do not hide this behind a "Finance" or "Billing" navigation label.
- Dropout-risk alert strip must be visible without scrolling on a 360dp-wide screen. If both amber and red flags exist, show both counts in one strip — do not require two separate elements.
- Touch targets for all interactive elements ≥ 44dp.

---

### Screen: Outstanding Balance Dashboard

**Purpose:** Give Rahul a ranked list of families who owe money, with the total receivables figure at the top, so he can decide who to follow up with and trigger a reminder in one tap.
**Primary action:** Tap "Send Reminder" shortcut on a family row (opens WhatsApp intent or SMS confirmation)
**Entry point(s):** Tap from home screen banner; tap from Analytics Revenue screen "View outstanding"
**Exit point(s):** Tap family row → Child Billing Profile; tap "Send Reminder" → WhatsApp intent or SMS send confirmation; tap back → previous screen

**Key components:**
- Summary row (pinned at top): total outstanding across all families (₹), family count with outstanding balance, count with balance > 30 days overdue
- Family rows (sorted by days overdue descending): child name, parent name, outstanding amount (₹), invoice date, days overdue label (text, not color only), "Send Reminder" chip
- Aging indicator on each row: text labels — "Current," "1–30 days overdue," "30+ days overdue" — displayed alongside any color coding
- Sort controls: default is "Days overdue" (most overdue first). Secondary sort by outstanding amount available via sort icon.

**States:**
- **Empty state:** All families paid up. Screen reads: "All families are up to date. No outstanding balances." Positive language — no warning chrome. Single action: "View payment history" link.
- **Loading state:** Skeleton list with 5 placeholder rows. Summary row skeleton at top.
- **Error state:** API failure. "Could not load outstanding balances — pull down to retry." Last-cached list shown with staleness label.
- **Offline state:** Last-synced data shown with "Last updated [timestamp]" banner. "Send Reminder" and "Generate Link" actions are disabled with tooltip: "Sending requires an internet connection."

**Constraints:**
- Color cannot be the only indicator of overdue status. Text labels ("30+ days overdue") must appear in the row. Colorblind users and low-contrast Android screen modes must be accounted for.
- "Send Reminder" chip must be reachable with one thumb for right-handed use (row chip on right edge, or accessible via row tap).

---

### Screen: Progress Dashboard — Centre Summary

**Purpose:** Give Rahul a centre-wide view of attendance health and dropout-risk, with the highest-risk children surfaced at the top without requiring a scroll or a filter tap.
**Primary action:** Tap a dropout-risk child's amber/red badge → navigate to Child Contact Screen
**Entry point(s):** Tap dropout-risk alert strip on Home screen; tap Progress Dashboard tab
**Exit point(s):** Tap risk badge → Child Contact Screen; tap child card → Child Progress Detail; tap back → Home screen

**Key components:**
- Centre summary header (4 metric chips in 2×2 grid): total active children, centre attendance rate this month (%), dropout-risk count (amber + red total), children with no session in last 14 days
- "Needs attention" section (appears only if flagged children exist): grouped list of amber and red flagged children, sorted by severity (red first). Each row shows child name, risk badge (icon + color + text), consecutive missed sessions count, and a parent contact shortcut.
- Full child list (below "Needs attention"): same child card format as PROG-001. Each card shows child name, 4-week attendance bar, goal completion indicator, risk badge if applicable.

**States:**
- **Empty state (no active children):** Header chips all show 0. "Needs attention" section absent. Full child list shows: "No active children enrolled yet — add your first child to get started."
- **Empty state (children enrolled, no attendance data):** Header chips show child count but attendance rate shows "—" (not 0%). "Needs attention" section absent. Child cards show "No sessions scheduled yet" (per PROG-001 EC-01). No false 0% risk flags.
- **Loading state:** Header chips render as skeleton chips. Child card list renders as skeleton cards (3–4 visible). Loading must complete in ≤ 4s on 4G.
- **Error state:** "Could not load dashboard — pull down to retry." Last-cached data shown with staleness label.
- **Offline state:** Cached dashboard shown. Risk flags from last sync displayed. "Data as of [date]" label on each card. No contact actions available while offline.

**Constraints:**
- The "Needs attention" section must be visible above the fold on a 5-inch screen (360×640dp equivalent) without scrolling. Limit this section to a maximum of 3–4 rows before collapsing behind a "View all [N] at-risk children" expand control.
- Risk badges must use icon + text + color. Amber = warning icon + "At risk" label. Red = alert icon + "High risk" label.
- Charts on child cards must be lightweight (CSS/canvas, not a full chart library). Target: ≤ 50ms render per card on 2GB RAM Android.

---

### Screen: Analytics Tab — Revenue Screen

**Purpose:** Show Rahul the centre's financial health for the current month in one card: invoiced, collected, outstanding, collection rate.
**Primary action:** Tap "View outstanding" to drill into the outstanding balance list, or tap "Export" to generate the monthly report
**Entry point(s):** Analytics bottom-nav tab
**Exit point(s):** Tap "View outstanding" → Outstanding Balance Dashboard; tap "Export" → Export Modal; tap "By therapist" → Utilization Screen; tap "Enrollment" → Caseload / Enrollment Screen

**Key components:**
- Revenue card (top): total invoiced this month (₹), total collected this month (₹), total outstanding this month (₹), collection rate (% with a simple fill bar below the number — not a pie chart)
- "View outstanding" link below the outstanding figure (direct link to Outstanding Balance Dashboard)
- Section navigation (horizontal scroll or accordion): Revenue (current) | Utilization | Caseload/Enrollment
- "Export monthly report" button (fixed at bottom of screen or in section header)

**States:**
- **Empty state (no invoices this month):** Revenue card reads "No invoices this month — create your first invoice to start tracking revenue." Export button disabled.
- **Loading state:** Revenue card renders as a skeleton (4 metric placeholders). Renders in ≤ 4s on 4G.
- **Error state:** "Could not load revenue data — pull down to retry." Last-cached values with staleness label.
- **Offline state:** Last-synced revenue data with "Last updated [timestamp]." Export button disabled with tooltip "Export requires internet connection."

**Constraints:**
- Currency label (₹) must appear alongside every monetary value — no bare numbers.
- Collection rate must be shown as both a percentage text AND a visual fill bar. Single-metric only. Do not add multiple chart types on one card (mobile performance constraint).
- Admin/Billing role sees this screen. Clinical records tab is not accessible to Admin/Billing role — navigation must enforce this RBAC boundary.

---

### Screen: Analytics Tab — Caseload / Enrollment Screen

**Purpose:** Show Rahul how many children each therapist is managing and whether the centre is growing or shrinking month over month.
**Primary action:** Tap a therapist row to drill into their caseload detail
**Entry point(s):** Scroll from Revenue screen, or tap section nav link
**Exit point(s):** Tap therapist row → Therapist Caseload Detail Screen

**Key components:**
- Caseload list (top): therapist name, active child count, sorted by count descending. Simple number-and-name list, no chart.
- Enrollment vs. attrition table (below caseload): 6-month rolling table. Columns: Month | New | Exited | Net. Plain text table — no bar chart rendering. "Likely inactive — confirm status" row at bottom of enrollment table for unconfirmed exits.
- "Filter by therapist" control (top right of caseload section)

**States:**
- **Empty state (no therapists assigned any children):** "No active caseloads yet — assign children to therapists to start tracking."
- **Empty state (enrollment table, < 1 month data):** Enrollment table shows current month only with partial data. "Not enough data for a trend yet — check back next month."
- **Loading state:** Skeleton list rows for caseload. Table renders as 6 placeholder rows.
- **Error state:** Standard retry pattern. Last-cached data with staleness label.
- **Offline state:** Cached data shown. Note: enrollment data may be stale for recently exited or enrolled children. Staleness label required.

**Constraints:**
- 6-month enrollment trend must render as a plain number table — not a chart library. Reasoning: heavy SVG/canvas chart rendering causes jank on 2GB RAM Android (Redmi Note / Realme C series). Use a styled HTML table with alternating row shading instead.
- "Likely inactive" children are explicitly not counted in the "Exited" figure until Rahul confirms exit status. The distinction must be visible in the UI — do not conflate likely-inactive with confirmed exits.

---

### Screen: Therapist Caseload Detail Screen

**Purpose:** Give Rahul (or Dr. Sunita, for her own caseload) a per-therapist drill-down: which children are assigned, when each child was last seen, and whether any program reviews or sessions are overdue.
**Primary action:** Tap child row → open child's record on Program/Data tab
**Entry point(s):** Tap therapist row from Caseload/Enrollment screen; direct entry for Dr. Sunita via MPM-003 Supervisor Dashboard (same underlying screen, different RBAC scope)
**Exit point(s):** Tap child row → Child Record (Program/Data tab); tap back → Caseload/Enrollment screen

**Key components:**
- Screen header: therapist name, active child count
- Filter control: "Overdue flags only" toggle (filters to children with at least one flag)
- Child rows: child name, last session date (or "No sessions recorded"), last program update date (or "No program set"), overdue flag indicators (session overdue: amber dot + "Session > 7 days"; program overdue: amber dot + "Program > 30 days")
- Overdue flag count badge in screen header (e.g., "3 overdue flags")

**States:**
- **Empty state (no children assigned):** "No children are currently assigned to [therapist name]'s caseload. Assign children via the child's Care Team tab."
- **Empty state for Dr. Sunita (no supervision assignments):** "No children are currently assigned to your supervision. Contact your centre director."
- **Loading state:** Skeleton rows (5 placeholders). Renders in ≤ 3s.
- **Error state:** Standard retry. Cached data with staleness label.
- **Offline state:** Cached caseload shown. Overdue flag calculations based on last-synced session and program data. Staleness label visible.

**Constraints:**
- Dr. Sunita accessing this screen sees only her assigned children (MPM-003 RBAC scope). Rahul accessing it sees the full therapist's caseload. The screen header must indicate whose caseload is shown and which role is viewing.
- Overdue flag indicators must use text labels alongside visual indicators — not color-coded dots alone.

---

### Screen: Export Modal (Monthly Operations Report)

**Purpose:** Let Rahul configure and trigger the monthly PDF export with minimal friction, then let him leave the screen immediately — the job runs in the background.
**Primary action:** Confirm export (triggers background job)
**Entry point(s):** Tap "Export monthly report" from Analytics Revenue screen
**Exit point(s):** Tap "Confirm export" → dismiss modal, background job queued; tap "Cancel" → return to Revenue screen

**Key components:**
- Month/year selector (picker — defaults to current month)
- Section toggles: Revenue (default on) | Utilization (default on) | Enrollment (default on). Each toggle shows a one-line description of what will be included.
- Estimated generation time indicator ("Usually ready in under 30 seconds")
- Confirm Export button (prominent, full-width)
- Cancel link (secondary, above the button)

**States:**
- **Standard state:** Month defaulted to current month. All sections toggled on. Confirm button active.
- **Empty state (no data for selected month):** Confirm button is still enabled (export will generate a "no data" PDF per ANALYTICS-004 EC-01). A warning label appears: "No data recorded for [month] — the report will note this."
- **In-progress state:** After tapping Confirm, modal closes and a toast message appears on the Analytics screen: "Your report is generating in the background. You'll get a notification when it's ready." No spinner occupying the screen.
- **Error state (generation failure):** In-app notification fires: "Export failed — check your connection and try again." Retry from Analytics screen.

**Constraints:**
- The modal must close immediately after the user taps Confirm — the user must not be blocked on-screen while the PDF generates. Background job pattern is mandatory for this export.
- Do not auto-download the PDF to the device without user confirmation. Deliver via notification with a "Download" action.

---

## Developer Handoff

### Step-level technical summary

| Step | Data written | Data read | API / event | Offline behavior | Regulatory gate |
|---|---|---|---|---|---|
| 1 | Session token refreshed | User role, session state | `POST /auth/refresh` (silent) | Block on auth failure; show login screen | RBAC-001: Director role check on session token |
| 2 | None | `director_home_summary` (outstanding fees total, dropout-risk counts, admin flag counts) | `GET /director/home-summary` | Show cached home summary with staleness label | RBAC-001: Director role required; DPDPA-001: no child health data in this payload — aggregate counts only |
| 3–4 | None | Outstanding balance list per family (child name, outstanding amount, invoice date, days overdue) | `GET /billing/outstanding?sort=days_overdue` | Show last-synced outstanding list with staleness label; action buttons disabled | RBAC-001: Director or Admin/Billing role only; DPDPA: financial personal data — access logged in AUDIT-001 |
| 5 | None | Per-family billing record (invoice history, payment history, UPI link status) | `GET /billing/family/{family_id}` | Show cached billing profile; action buttons disabled offline | RBAC-001: Director or Admin/Billing only; DPDPA: payment data stored encrypted server-side |
| 6 | Reminder event logged (channel, timestamp, status) | Parent WhatsApp opt-in status (WA-003), reminder template (REMIND-003/INV-005) | `POST /reminders/send` or `POST /whatsapp/send` → WhatsApp Business API or SMS gateway (MSG91/Twilio) | Queue reminder for when online (show "Will send when connected" state) | DPDPA: message must not include clinical content; parent must have opted in to WhatsApp if WhatsApp channel selected; REMIND-005 delivery log entry written |
| 7–8 | None | Centre-level attendance summary, dropout-risk flag calculations | `GET /progress/centre-summary` | Show cached summary with staleness label; PROG-004 risk flags from last background job run | RBAC-001: Director sees all children; DPDPA: aggregate counts only in summary response — no clinical detail until child record is opened |
| 9–10 | None | Child risk status, parent contact details (surfaced on tap) | `GET /children/{child_id}/contact` (lazy-loaded on risk badge tap) | Contact data not available offline | RBAC-001: RBAC check before exposing parent contact; DPDPA: parent mobile number is personal data — access logged in AUDIT-001 |
| 11–12 | None | Revenue metrics (invoiced, collected, outstanding, collection rate) | `GET /analytics/revenue?period=current_month` | Show cached data with staleness label | RBAC-001: Director or Admin/Billing role only; not visible to Supervisor or Therapist roles |
| 13 | None | Utilization metrics per therapist (scheduled, delivered, cancellation breakdown) | `GET /analytics/utilization?period=current_month` | Cached data with staleness label | RBAC-001: Director only for per-therapist data; DPDPA: therapist performance data is personal data — purpose limitation: internal operations only |
| 14 | None | Caseload counts per therapist, 6-month enrollment vs. exits table | `GET /analytics/caseload` | Cached data with staleness label | RBAC-001: Director only |
| 15–16 | None | Children assigned to selected therapist (name, last session, last program update, overdue flags) | `GET /therapist/{therapist_id}/caseload` | Cached caseload with staleness label | RBAC-001: Director sees full caseload; Supervisor sees own caseload only; DPDPA: child names in caseload view are personal data — access logged |
| 17 | Access event logged | Child full record (Profile, Program, Sessions, Documents, Billing tabs) | `GET /children/{child_id}/record` | Child record readable offline if previously loaded; edits queue locally and sync on restore | RBAC-001: Director full access; DPDPA-001: consent must be confirmed before record activates; AUDIT-001: access event logged on record open |
| 18–19 | Export initiation logged in AUDIT-001 immediately | Revenue, utilization, enrollment data for selected month | `POST /reports/operations-export` → background job queued | Export cannot be initiated offline | RBAC-001: Director and Admin/Billing only; DPDPA: exported report contains personal data; AUDIT-001: audit log entry created at initiation, updated at completion |
| 20–21 | Download event logged in AUDIT-001 | Generated PDF (served from signed, session-bound download URL) | `GET /reports/{job_id}/download` (served via CDN with signed URL, expiry 24h) | PDF must be downloaded online; share from device is offline-capable once downloaded | RBAC-001: session-bound link — not shareable; DPDPA: download logged in audit trail; link expiry enforced server-side |

---

**Key state transitions:**
- Invoice object transitions from `Outstanding` → `Paid` / `Partially Paid` at Step 6 when a payment is recorded (UPI-002 callback or INV-003 manual entry — this may happen in a parallel billing session, not necessarily this analytics session).
- Child status transitions from `Active` → `At risk (amber)` → `At risk (red)` based on PROG-004 background job run (server-side, runs on schedule, not triggered by this journey). Dashboard reflects the last-computed flag state.
- Export job transitions from `Queued` → `Generating` → `Complete` / `Failed` between Steps 18 and 20. Client polls or receives push notification on completion.

---

**Background jobs / async events triggered by this journey:**
- **PROG-004 dropout-risk flag job:** Not triggered by this journey — runs on a scheduled background job (e.g., every 6 hours or on new attendance marks). Dashboard reflects the last computed result. No real-time recalculation on Rahul's page load.
- **ANALYTICS-004 PDF export job:** Triggered at Step 18. Server-side PDF generation. Completion notification pushed to Rahul's device. Download link valid for 24 hours after completion.
- **INV-005 / REMIND-003 automated overdue reminders:** Not triggered by this journey (they run on a daily job). Rahul's manual reminder send (Step 6) fires independently and immediately.

---

**DPDPA compliance checkpoints:**
- Step 1: RBAC-001 — Director role confirmed before any data loads. No child health data accessible without authenticated Director session.
- Step 2: Home summary uses aggregate counts only (no child names, no clinical data in the summary payload). DPDPA risk: low for the summary payload; medium when the user taps through to child-level data.
- Steps 3–6: ⚠️ DPDPA — financial personal data (family names, payment amounts). Access restricted to Director and Admin/Billing roles. All access logged in AUDIT-001.
- Steps 7–10: ⚠️ DPDPA — child health data accessed at the child card level (attendance trend is clinical data for a minor). RBAC must confirm role before rendering child cards. Parent contact data (Step 10) is personal data — lazy-loaded only on explicit tap, with RBAC check.
- Steps 11–14: DPDPA — financial and operational personal data. Director and Admin/Billing only. Therapist performance data (Step 13) is personal data under DPDPA (staff as data principals) — purpose limitation applies (internal operations, not shared externally without consent).
- Steps 17: ⚠️ DPDPA — child health record opened. DPDPA-001 consent must be confirmed. AUDIT-001 access event logged on every record open.
- Steps 18–21: ⚠️ DPDPA — exported report contains personal and financial data. Export initiation and completion logged. Session-bound download link. No bulk export without explicit Director confirmation. Bulk export (EXPORT-003) separately requires consent-withdrawal check per child before inclusion in ZIP.

---

## Cross-Journey Dependencies

| Depends on journey | Why | What breaks if missing |
|---|---|---|
| Journey 2 — Child Enrollment & Onboarding | Child records must exist with confirmed DPDPA consent before any analytics data can exist | Progress Dashboard shows empty state; outstanding balance dashboard has no families; dropout-risk flags cannot compute |
| Journey 9 — Billing & UPI Payments | Invoices must have been generated and sent before revenue dashboard has data; outstanding balance list depends on invoice records existing | Revenue card shows ₹0 / empty state; outstanding balance dashboard empty; collection rate cannot be calculated |
| Journey 3 — Scheduling & Attendance | Attendance must have been marked (Present / Absent / No-show) by Priya before dropout-risk flags can compute; session utilization rate depends on scheduled vs. delivered sessions data | Dropout-risk flags absent; utilization rate shows 0% or empty; attendance trend cards on child cards are blank |
| Journey 10 — Appointment Follow-Up & Dropout Prevention | REMIND-002 (no-show follow-up) generates the follow-up log that feeds into the dropout-risk signal | Dropout-risk flag logic has no follow-up history; PROG-004 flag calculation is attendance-only without the follow-up context |
| Journey 6 — Post-Session Documentation | Session notes and goal status updates feed PROG-003 (goal completion rate on child cards) | Goal completion indicator shows "No program set up" or stale data; supervisor review trigger in MPM-003 cannot compute program-update overdue flags |
| Journey 8 — Progress Reporting | Progress reports must exist for EXPORT-001 (full child record export) and ANALYTICS-004 (monthly report can reference progress status) | Full child record export is incomplete (progress reports section missing); monthly report contains only financial and attendance sections |

---

## ⚠️ Feature Factory Disclaimer

These flows were synthesized from competitive observation and document-level story logic — not from validated user research with Indian therapy centre directors. Before committing design and engineering effort, a real product thinker should ask:

**What we assumed but have not validated:**

- [ASSUMPTION] Rahul checks a digital dashboard regularly enough to make a centre operations screen valuable. If his centre has fewer than 15 children and he knows the financial picture intuitively, a formal analytics screen may not change behaviour. Validate metric-checking frequency and mental model of "centre health" in director interviews (ANALYTICS-002 brief).
- [ASSUMPTION] The most important number Rahul needs in under 3 seconds is outstanding fees. This is a reasonable inference from BP-06 (billing is the key operational pain) but has not been confirmed by asking Rahul directly what he wants to see first on opening the app.
- [ASSUMPTION] Dropout-risk flags surfaced proactively on the home screen will prompt Rahul to act on at-risk families earlier. The assumption is that early contact prevents dropout. The 39% → 3% no-show research (Psychiatric Services) is from a US psychiatric outpatient context. Whether proactive outreach at the point of attendance drop (not the point of already being no-show) changes dropout rates in Indian autism therapy families is not confirmed.
- [ASSUMPTION] Rahul needs a monthly export PDF to share with a co-founder, bank, or accountant. The use case is plausible for founder-led centres but unconfirmed. Whether Rahul currently produces any monthly summary at all, and in what format, has not been validated.
- [ASSUMPTION] Dr. Sunita regularly checks a caseload dashboard to prioritise her review work. If her caseload is small (5–8 children) and she knows their status from memory or daily verbal check-ins, a digital dashboard may add friction rather than value.
- [ASSUMPTION] The mobile-first analytics design constraint (no desktop-first port) is correct for this persona. Rahul's primary device is assumed to be a low-end Android phone based on the broader market context. This has not been confirmed by direct observation of Rahul's device usage in Indian centre context.

**What a researcher would ask before building this:**

- What does Rahul actually do on a Monday morning or month-end today? Does he open Excel, call a staff member, look at a WhatsApp chat, or simply know the numbers in his head? Understanding the current workflow in detail is essential before designing the dashboard entry point. (H-09, H-12 from the journey map hypothesis register are the closest existing hypotheses but do not address the analytics workflow specifically.)
- What is the one number Rahul actually cares about most? Is it outstanding fees (our assumption), number of children at risk of dropping out, whether he is understaffed, or something else? The home screen hierarchy must reflect the actual priority, not a product manager's guess.
- Does Rahul share financial or operational summaries with anyone today (co-founder, accountant, bank)? And in what format? If he uses WhatsApp voice messages or verbal briefings, a PDF export may not be the right output format for this workflow.
- How does Dr. Sunita currently prioritise which child's program to review on a given day? Is it a weekly schedule, a conversation with Priya, or something she tracks mentally? The supervisor caseload dashboard (MPM-003) design depends heavily on whether a digital view adds to or disrupts an existing workflow.

**What the Product Consultant would challenge:**

- The analytics cluster is downstream of three other clusters (clinical documentation, billing, scheduling). If those clusters are not live and generating reliable data, every screen in this journey is either empty or inaccurate. The analytics journey should be explicitly gated on confirmed data quality from upstream modules before it ships — shipping an empty dashboard is worse than not shipping it.
- The dropout-risk flag (PROG-004) is a differentiator identified in the competitive analysis but it is one of the more complex background job features in this cluster. For a v1, consider whether a simpler version — a list of children who have not attended in the last 14 days, manually surfaced — delivers the same director value without background job complexity. Validate whether Rahul needs automated risk scoring or simply a sorted list he can glance at.

**Risk level per output:**

| Feature / screen | Risk level | Primary risk |
|---|---|---|
| Outstanding balance dashboard (UPI-004, home banner) | Low | Table stakes billing visibility; dependent on invoices existing upstream |
| Centre attendance summary + child cards (PROG-001, PROG-002) | Low-Medium | Dependent on attendance data being captured (Cluster 4 upstream); value only if data is reliable |
| Dropout-risk flags (PROG-004) | Medium | Background job complexity; effectiveness of proactive outreach is assumed, not validated; Indian dropout driver may not be attendance-detectable |
| Revenue / utilization / caseload analytics (ANALYTICS-001 to -003) | Medium | Director metric-checking behaviour is assumed; small-centre directors may not need a formal dashboard |
| Monthly PDF export (ANALYTICS-004) | Medium | Use case plausible but unconfirmed; export format preference (PDF vs. WhatsApp summary vs. CSV) not validated |
| Therapist caseload drill-down (MPM-003, MPM-005) | Low-Medium | Supervisor and director use cases are clear; risk is over-engineering the flag logic before data quality is confirmed |

Use the `/research` agent to validate H-09 (director metric-checking behaviour), the home screen priority hierarchy assumption (outstanding fees as primary KPI), and the dropout-risk outreach assumption before sprint planning.
Use the `/product-consultant` agent to challenge the upstream data dependency gating strategy and the v1 scope of the dropout-risk background job.
Use the `/design-critique` agent to review the mobile-first analytics screen layouts before prototyping — particularly the home screen banner hierarchy and the caseload detail screen on a 360dp-wide viewport.
