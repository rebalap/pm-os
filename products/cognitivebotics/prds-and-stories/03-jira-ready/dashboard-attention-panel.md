# Cognitivebotics — Therapy Center Dashboard: Key Metrics & Attention Panel

**Product:** Cognitivebotics
**Epic prefix:** CB-DASH
**Author:** Mindless Product Owner Agent
**Date:** 2026-05-11
**Last updated:** 2026-05-12
**Stage:** Build — Engineering Ready
**Target users:** Priya (Special Educator / Therapist), Dr. Sunita (Clinical Supervisor / Admin)

---

## Feature Brief: Therapy Center Dashboard — Key Metrics & Attention Panel

**Inspired by:** Category norms across clinical management SaaS (SimplePractice, Jane App, Motivity); internal design mock observed in Cognitivebotics product review

**Prevalence:** Table stakes — any clinical or case management tool landing page surfaces a summary + triage view. The differentiator is urgency-ranked triage tied to ILP status with role-aware table columns.

**Target user:** Priya (Therapist) and Dr. Sunita (Clinical Supervisor / Admin) — desktop web, clinic or home-office context, beginning-of-workday triage

**What it does:** Provides a clinically actionable landing page. The user sees four metric cards summarising caseload health, then drills into a prioritised list of children needing attention. Supervisors and admins see a therapist name column in the table. From each row, quick actions (View journal, View reports, Manage plan) navigate directly to the child's record with the relevant section open.

**What "done" looks like:** A user logs in, sees four role-scoped metric cards with unambiguous inclusion criteria, sees the attention list sorted by urgency, can toggle to "All recently active", and navigates to any child's record in one click — landing on the correct section.

**[ASSUMPTION — NOT VALIDATED]** This feature is assumed to solve the "where do I start my day" problem for therapists and supervisors. No primary research has confirmed that dashboard triage is a felt pain point over the current workflow of navigating child records individually.

---

## Epic: CB-DASH — Therapy Center Dashboard

**Goal:** Therapists and supervisors can assess their caseload health and navigate to any child needing attention within 60 seconds of logging in.

**Target user(s):** Priya (Therapist), Dr. Sunita (Clinical Supervisor / Admin)

**Definition of Done:**
- Four metric cards render with role-scoped data and correct inclusion criteria within 2 seconds
- Children list defaults to "Needs attention" on load, sorted: Plan ended → Limited progress → Plan ending soon
- Filter toggle switches between "Needs attention" and "All recently active"
- Supervisor / admin table view includes a Therapist name column; therapist table view does not
- View journal, View reports, and Manage plan each navigate to the child's record with the correct section open
- RBAC enforced: Priya sees only her assigned children; Dr. Sunita sees all children in the center
- DPDPA consent gates display of any child data
- All interactive elements meet 44px minimum target; status badges include text label alongside colour

**Out of scope (this epic):**
- Parent nudge / in-app messaging to parents from the dashboard
- Inline write actions from the dashboard (plan extension, plan creation)
- Any additional metric cards beyond the confirmed four
- Bulk actions on multiple children simultaneously
- Customisable dashboard layout or card reordering
- Export of dashboard data to CSV or PDF
- Mobile / tablet views (desktop web only)
- Cross-center dashboards for multi-center operators

---

## Story CB-DASH-001: Therapy Center Dashboard — Metrics, Attention List, and Child Navigation

**As a** Priya (Therapist) or Dr. Sunita (Clinical Supervisor / Admin)
**I want to** see a dashboard with four metric summary cards and a filterable, sorted list of children, with quick actions that take me directly to the relevant section of a child's record
**So that** I can assess my caseload health at a glance and act on any child without manual sidebar navigation

**Inspired by:** SimplePractice, Jane App, Motivity dashboard patterns; internal Cognitivebotics design mock

**Context:** This is the landing page after login. Desktop web only. Priya sees data scoped to her assigned children. Dr. Sunita and any admin role see data across all children in the center. The page has two regions: a metric card row at the top, and a children list panel below with a filter control.

---

### Section A — Metric Cards

**Metric definitions (authoritative — implement exactly as stated):**

| Card label | Inclusion criteria |
|---|---|
| Recently active | Children whose `last_played_date` OR `created_date` falls within the last 30 calendar days (rolling window from today) |
| Need attention | Children with ILP status `Plan ended`, `Limited progress`, or `Plan ending soon` |
| On track | Children with ILP status `On track` only |
| Journal entries in past day | Children for whom at least one parent journal entry was submitted on the previous calendar day (yesterday 00:00–23:59 in the center's configured timezone) |

**Acceptance Criteria — Metric Cards:**
- [ ] AC-01: Given Priya (Therapist) is logged in, when the dashboard loads, then all four cards display counts scoped to her assigned children only
- [ ] AC-02: Given Dr. Sunita (Supervisor / Admin) is logged in, when the dashboard loads, then all four cards display counts scoped to all children in the center
- [ ] AC-03: Given the dashboard has loaded, when a user views the cards, then exactly four cards appear in this fixed order: Recently active, Need attention, On track, Journal entries in past day
- [ ] AC-04: Given the "Recently active" card, when the count is calculated, then any child whose `last_played_date` OR `created_date` is within the last 30 calendar days is included; a child with only a `created_date` in the window and no play history is included
- [ ] AC-05: Given the "Need attention" card, when the count is calculated, then only children with ILP status `Plan ended`, `Limited progress`, or `Plan ending soon` are included; all other statuses are excluded
- [ ] AC-06: Given the "On track" card, when the count is calculated, then only children with ILP status `On track` are included; children with status `New` or any attention status are excluded
- [ ] AC-07: Given the "Journal entries in past day" card, when the count is calculated, then only children with a parent journal entry submitted yesterday (in the center's configured timezone) are included; entries from today or two or more days ago are excluded
- [ ] AC-08: Given a user clicks any metric card, then the children list below filters to the corresponding segment: "Need attention" card activates "Needs attention" list; "Recently active" card activates "All recently active" list
- [ ] AC-09: Given DPDPA consent has not been confirmed for a child, when the dashboard loads, then that child is excluded from all card counts and does not appear in any list view

**Edge Cases — Metric Cards:**
- [ ] EC-01: If a card count is zero, the card displays "0" — it does not hide or collapse
- [ ] EC-02: If the data fetch for metric cards fails, each card displays "Unable to load — refresh" rather than a stale or zero count without indication
- [ ] EC-03: If Priya has no assigned children, all four cards display 0 and the list shows: "No children assigned to you yet. Contact your supervisor."
- [ ] EC-04: If the center's timezone is not configured, "Journal entries in past day" falls back to UTC and displays a tooltip: "Showing entries based on UTC — configure your timezone in settings"
- [ ] EC-05: If a child's `last_played_date` and `created_date` are both null, that child is excluded from "Recently active" and a backend data integrity alert is logged

---

### Section B — Children List: Filter and Sort

**Filter and sort definitions (authoritative):**

| Filter | Children shown | Sort order |
|---|---|---|
| Needs attention (default) | ILP status = `Plan ended`, `Limited progress`, or `Plan ending soon` | Fixed: Plan ended → Limited progress → Plan ending soon; alphabetical by first name within each group |
| All recently active | All children matching the "Recently active" metric definition | `last_played_date` descending (most recently active first); children with null `last_played_date` appear first, sorted by `created_date` descending |

**Acceptance Criteria — Filter and Sort:**
- [ ] AC-10: Given the dashboard loads, when the children list renders, then it defaults to the "Needs attention" filter; the filter control shows "Needs attention" as the active state with no user interaction required
- [ ] AC-11: Given the "Needs attention" filter is active, when the list renders, then children appear in this fixed order: `Plan ended` first, `Limited progress` second, `Plan ending soon` third; within each group, children are sorted alphabetically by first name (A→Z)
- [ ] AC-12: Given the user selects "All recently active" from the filter control, when the list refreshes, then children are sorted by `last_played_date` descending; children with null `last_played_date` appear at the top sorted by `created_date` descending
- [ ] AC-13: Given either filter is active, when Priya views the list, then only children assigned to Priya appear
- [ ] AC-14: Given either filter is active, when Dr. Sunita views the list, then all children in the center matching the filter criteria appear regardless of assigned therapist
- [ ] AC-15: Given DPDPA consent has not been confirmed for a child, when the list renders under either filter, then that child does not appear

**Edge Cases — Filter and Sort:**
- [ ] EC-06: If the "Needs attention" list is empty, the list shows "No children need attention right now." with no data rows
- [ ] EC-07: If the "All recently active" list is empty, the list shows "No children have been active in the last 30 days."
- [ ] EC-08: If a child has multiple ILP status values simultaneously (data model edge case), the highest urgency status takes precedence for sort and badge: `Plan ended` > `Limited progress` > `Plan ending soon`
- [ ] EC-09: If the data fetch fails, the list shows "Unable to load children — refresh" with a retry button; a blank panel is not acceptable

---

### Section C — Table Columns: Role-Based View

**Column definitions by role:**

| Column | Therapist view (Priya) | Supervisor / Admin view (Dr. Sunita) |
|---|---|---|
| Child name | Yes | Yes |
| Therapist name | No | Yes — shown adjacent to child name |
| Status badge | Yes | Yes |
| Last played | Yes | Yes |
| View journal | Yes | Yes |
| View reports | Yes | Yes |
| Manage plan | Yes | Yes |

**Acceptance Criteria — Table Columns:**
- [ ] AC-16: Given Priya (Therapist) is logged in, when the list renders, then each row shows: child name, status badge, last played date, and three quick-action buttons (View journal, View reports, Manage plan) — no therapist name column is present
- [ ] AC-17: Given Dr. Sunita (Supervisor / Admin) is logged in, when the list renders, then each row shows: child name, therapist name (the therapist assigned to that child), status badge, last played date, and three quick-action buttons — the therapist name appears adjacent to the child name
- [ ] AC-18: Given either filter is active, when status badges render, then: `Plan ended` is red with white text "Plan ended"; `Limited progress` is amber with white text "Limited progress"; `Plan ending soon` is teal with white text "Plan ending soon" — text label is always present alongside colour
- [ ] AC-19: Given a child row is displayed and `last_played_date` is null, then the last played field shows "Not yet played" — the row is not suppressed

---

### Section D — Quick Action Navigation

**Navigation targets (authoritative):**

| Button | Destination |
|---|---|
| View journal (book icon) | Children tab → child record → Journal section |
| View reports | Children tab → child record → Reports section |
| Manage plan | Children tab → child record → Plan / ILP section |

**Acceptance Criteria — Quick Actions:**
- [ ] AC-20: Given a child row is displayed, when the user clicks "View journal" or the book icon, then the app navigates to the Children tab in the left pane and opens that child's record with the Journal section active
- [ ] AC-21: Given a child row is displayed, when the user clicks "View reports", then the app navigates to the Children tab and opens that child's record with the Reports section active
- [ ] AC-22: Given a child row is displayed, when the user clicks "Manage plan", then the app navigates to the Children tab and opens that child's record with the Plan / ILP section active
- [ ] AC-23: Given any quick-action navigation has occurred, when the child's record opens, then "Children" is highlighted as the active item in the left navigation pane and the child's name is visible as the active record
- [ ] AC-24: Given any quick-action navigation has occurred, when the user clicks the browser back button, then the user returns to the dashboard with the same filter state and scroll position they left
- [ ] AC-25: Given a child has no parent journal entries, when the user clicks "View journal", then navigation still occurs and the Journal section handles its own empty state — the View journal button is never disabled on the dashboard due to missing entries

**Edge Cases — Quick Actions:**
- [ ] EC-10: If the child record cannot be loaded after navigation (data fetch failure), the Children tab displays an error state within the record — the navigation itself succeeds
- [ ] EC-11: If the user is offline when clicking a quick action, navigation proceeds; the child record displays cached data or an offline message if no cache exists

---

### Non-Functional Requirements

- **Performance:** Metric cards render within 2 seconds of page load; first 10 list rows render within 2 seconds; subsequent pages load within 1 second; child record opens within 2 seconds of quick-action click
- **Offline:** Metric cards and list display cached data with a "Last updated [timestamp]" label; quick-action navigation remains functional offline; no write operations occur from this page
- **Accessibility:**
  - Each metric card has `aria-label` including metric name and count (e.g., `aria-label="Need attention: 5 children"`)
  - Each quick-action button has `aria-label` including the child's name (e.g., `aria-label="View reports for Aditya Pranav"`)
  - Status badges pass WCAG AA contrast ratio; text label always present alongside colour
  - All cards, filter controls, and row actions are keyboard-operable with visible focus states
- **Privacy:** ⚠️ DPDPA 2023 — child name, ILP status, last-played date, and therapist assignment are personal and health-adjacent data; DPDPA parental consent must be confirmed at the data layer before any child's data is surfaced anywhere on this page

**Dependencies:**
- Blocked by: RBAC role system (Therapist / Supervisor / Admin tags at login); child-therapist assignment mapping in the data model; ILP status field with values `Plan ended`, `Limited progress`, `Plan ending soon`, `On track`, `New`; `last_played_date` and `created_date` fields on the child record; parent journal entry model with submission timestamps and timezone support; Children tab deep-link support for Journal, Reports, and Plan sections via route state or URL parameter
- Enables: Nothing in this epic — this is the complete dashboard feature

**Definition of Done:**
- [ ] All AC (AC-01 through AC-25) pass in QA on Chrome (latest) and Safari (latest) at 1280px+ viewport
- [ ] All EC (EC-01 through EC-11) tested
- [ ] Metric definitions verified with test data for all four cards including edge cases (null dates, timezone fallback)
- [ ] "On track" card verified to include `On track` status only — `New` status children are excluded
- [ ] Sort order verified with mixed-status test dataset for both filter views
- [ ] Therapist view vs. supervisor / admin view verified: therapist name column present only for supervisor / admin role
- [ ] All three quick actions verified to land on the correct section of the child record
- [ ] Browser back verified: filter state and scroll position preserved on return to dashboard
- [ ] RBAC verified: Priya sees only assigned children; Dr. Sunita sees all children
- [ ] DPDPA exclusion verified: child without confirmed consent excluded from all counts and list views
- [ ] Badge accessibility verified: WCAG AA contrast; text label present on all badges
- [ ] Keyboard navigation verified: metric cards, filter control, and all row quick-action buttons reachable by keyboard
- [ ] Code reviewed and merged

---

## Backlog: CB-DASH — Therapy Center Dashboard

| Story ID | Title | Persona | Complexity | Priority | Blocked by |
|---|---|---|---|---|---|
| CB-DASH-001 | Therapy Center Dashboard — Metrics, Attention List, and Child Navigation | Priya, Dr. Sunita | L | P0 | RBAC role system; ILP status field; child-therapist assignment; parent journal model with timestamps; Children tab deep-link support |

**Complexity note:** Rated L (3–5 days) due to four distinct metric queries, two filter/sort modes, role-based column rendering, and three deep-link navigation targets. Engineering may split into two tasks during sprint planning — metric cards + list rendering as one task, quick-action navigation as a second — since the AC map cleanly to two halves.

---

## ⚠️ Feature Factory Disclaimer

These features and stories were defined by PM-confirmed design decisions, observed product mocks, and category norms — not by validated primary research with therapists or supervisors at Indian therapy centers.

**What we assumed but have not validated:**
- That therapists begin their workday by triaging a dashboard list — the "start of day review" workflow is assumed, not observed
- That the four metric card definitions (as specified) are the most clinically relevant signals; therapists may weight different criteria
- That "Plan ended → Limited progress → Plan ending soon" is the correct urgency order from the therapist's clinical perspective
- That "most recently active first" is the right sort for "All recently active" — an alternative (most overdue first) may be more useful for follow-up triage

**What a researcher would ask before building this:**
- How do therapists currently decide which child to follow up with first? Is urgency ranking a concept they already apply, or do they triage differently?
- When a plan ends, who in the center is responsible for renewal — therapist, supervisor, or admin? Are we surfacing this alert to the right person?
- Do therapists navigate to child records from a dashboard, or do they go directly to the Children tab by habit?

**What the Product Consultant would challenge:**
- "Need attention" mixes administrative cases (Plan ended, Plan ending soon) with a clinical case (Limited progress) in one list. These require different owners and different next actions — confirm one list serves both before building.
- `New` status children are excluded from "On track" but don't appear in any attention status either. They are invisible on this dashboard. Confirm this is intentional or whether `New` children should surface somewhere on this page.

**Risk level:**
- CB-DASH-001: Low-to-medium. The dashboard concept and navigation pattern are table stakes. The main risks are metric definition precision (high AC specificity reduces this) and Children tab deep-link support (must be confirmed as a dependency before sprint planning).

Use the /researcher agent to validate the triage workflow assumption before shipping. Use the /product-consultant agent to confirm `New` status handling and whether a single triage list serves both therapist and admin needs.
