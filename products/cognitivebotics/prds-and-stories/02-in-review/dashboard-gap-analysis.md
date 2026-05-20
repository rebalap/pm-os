# Gap Analysis: JIRA Ticket vs. Requirements Document
# CB-DASH-001 — Therapy Center Dashboard

**Compared:** `JIRA document` vs. `dashboard-attention-panel.md`
**Date:** 2026-05-12 (updated after JIRA revision)
**Scope exclusions:** DPDPA and timezone requirements are out of scope for this analysis

---

## What Was Fixed in the Updated JIRA

The following gaps from the previous version are now resolved:

| # | Was missing | Now present in JIRA |
| --- | --- | --- |
| 1 | EC-01 conflict: dash vs. zero | Correctly shows `"0"` for zero counts |
| 2 | DoD contradiction on `New` status in "On track" | DoD now correctly references "All Recently Active", not the On track card |
| 3 | Manage plan AC | AC-12 added |
| 4 | Role-based table columns | AC-13 (therapist view) and AC-14 (supervisor view) added |
| 5 | RBAC scoping on list for therapist | AC-15 added |

---

## Remaining Gaps

### ~~Critical — will cause wrong behavior or fail QA if not resolved before development~~

#### ~~C-01: Card click filtering the list — no AC~~

~~The requirements specify that clicking a metric card filters the children list below (clicking "Need attention" activates the Needs attention list; clicking "Recently active" activates All recently active). No AC in JIRA covers this interaction. Without it, engineering may treat the cards as display-only and not wire up the click behaviour at all.~~

**~~Add to JIRA:~~**
> ~~AC-XX: Given a user clicks any metric card, then the children list below filters to the corresponding segment: clicking "Need attention" activates the "Needs attention" list view; clicking "Recently active" activates the "All recently active" list view.~~

---

#### C-02: Admin / Supervisor RBAC scoping on the list — no AC

~~JIRA has AC-15 confirming that a Therapist sees only their assigned children in the list. There is no corresponding AC confirming that an Admin / Supervisor sees ~~*~~all~~*~~ children across the center. Without this, the list-scoping behaviour for the admin role is unspecified and untested.~~

**~~Add to JIRA:~~**
> ~~AC-XX: Given either filter is active, when a Supervisor / Admin views the list, then all children in the center matching the filter criteria appear, regardless of which therapist they are assigned to.~~

---

#### C-03: Status badge specification — no AC

~~JIRA's AC-13 and AC-14 reference a "status badge" column but do not specify colours, text label content, or the requirement that a text label must always accompany the colour. Without this AC, engineering will make its own colour choices and may implement colour-only badges.~~

**~~Add to JIRA:~~**
> ~~AC-XX: Given either filter is active, when status badges render: ~~~~`Plan ended`~~~~ is red with white text "Plan ended"; ~~~~`Limited progress`~~~~ is amber with white text "Limited progress"; ~~~~`Plan ending soon`~~~~ is teal with white text "Plan ending soon" — text label must always be present alongside colour and must not be replaced by colour alone.~~

---

### ~~High — important behaviour left unspecified~~

#### ~~H-01: "Not yet played" display for null last\_played\_date — no AC~~

~~No AC specifies what the last played column shows when ~~~~`last_played_date`~~~~ is null. Without this, engineers will handle it inconsistently (blank cell, dash, null, or a rendering error).~~

**~~Add to JIRA:~~**
> ~~AC-XX: Given a child row is displayed and ~~~~`last_played_date`~~~~ is null, then the last played field shows "Not yet played" — the row is not suppressed or hidden.~~

---

#### H-02: "Needs attention" empty state — no EC

JIRA has EC-04 for the empty state of "All recently active" but has no corresponding EC for when the "Needs attention" list is empty.

**Add to JIRA:**
> EC-XX: If the "Needs attention" list is empty (no children with attention statuses in scope), the list shows "No children need attention right now." with no data rows rendered.

---

#### H-03: List data fetch failure — no EC

JIRA has EC-02 for metric card data fetch failure but has no EC covering a failure to load the children list itself. A blank panel on list fetch failure is not acceptable.

**Add to JIRA:**
> EC-XX: If the data fetch for the children list fails, the list panel shows "Unable to load children — refresh" with a retry button; a blank panel is not acceptable.

---

#### H-04: Non-functional requirements entirely absent

JIRA has no performance, offline, or accessibility requirements. These are the most common source of engineering ambiguity and rework. Minimum additions needed:

| Area | Requirement |
| --- | --- |
| Performance | Metric cards and first 10 list rows render within 2 seconds on standard broadband; subsequent pages load within 1 second |
| Offline | Cards and list display cached data with a "Last updated [timestamp]" label when offline; no write operations occur from this page |
| Accessibility | `aria-label` on each metric card including its count; `aria-label` on each quick-action button including the child's name; status badges pass WCAG AA contrast ratio; all controls keyboard-operable |

---

### Medium — gaps that will surface during QA or handoff

#### M-01: Navigation landing state — no AC

~~No AC confirms that after a quick-action click, "Children" is highlighted in the left navigation pane and the child's name is visible as the active record. Without this, QA has no way to verify the user lands in the correct state.~~

**~~Add to JIRA:~~**
> ~~AC-XX: Given any quick-action navigation has occurred, when the child's record opens, then "Children" is highlighted as the active item in the left navigation pane and the child's name is visible as the active record.~~

---

#### M-02: Browser back preserves dashboard state — no AC

No AC specifies that pressing the browser back button from a child record returns the user to the dashboard with the same filter state and scroll position.

**Add to JIRA:**
> AC-XX: Given any quick-action navigation has occurred, when the user clicks the browser back button, then the user returns to the dashboard with the same filter state and scroll position they left.

---

#### M-03: View journal on a child with no journal entries — no AC

No AC specifies what happens when View journal is clicked for a child with no entries. Without this, engineering may disable the button at dashboard level, shifting the empty state responsibility to the wrong layer.

**Add to JIRA:**
> AC-XX: Given a child has no parent journal entries, when the user clicks "View journal", then navigation still occurs; the View journal button is never disabled at the dashboard level. The Journal section in the child record handles the empty state.

---

#### M-04: EC-04 copy mismatch

The "All recently active" empty state message differs between the two documents.

|  | Message |
| --- | --- |
| **JIRA (EC-04)** | "No recently active children to show." |
| **Requirements (EC-07)** | "No children have been active in the last 30 days." |

Align to a single string before development.

---

#### M-05: EC for child record load failure after navigation — missing

If the child record cannot be loaded after a quick-action click, the expected behaviour (Children tab shows an error state; navigation itself succeeds) is not specified in JIRA.

**Add to JIRA:**
> EC-XX: If the child record cannot be loaded after a quick-action navigation (data fetch failure), the Children tab displays an error state within the record — the navigation itself succeeds and does not redirect back to the dashboard.

---

### Low — structural and completeness issues

#### L-01: AC-06 merges two separate requirements into one

JIRA AC-06 combines the "On track" card definition and the "Journal entries in past day" card definition into a single AC. These are independent requirements for two different cards and should be separate ACs. As written, a tester checking AC-06 must test two different cards — and a failure in one does not clearly identify which card failed.

**Fix:** Split JIRA AC-06 into two ACs (one for On track, one for Journal entries in past day). Renumber subsequent ACs accordingly.

---

#### L-02: Definition of Done is incomplete

JIRA's DoD has 2 items. The requirements DoD has 13. Key checks missing from JIRA's DoD:

- Sort order verified with mixed-status test dataset for both filter views
- Therapist view vs. supervisor view column layout verified
- All three quick actions verified to land on the correct section of the child record
- Browser back verified: filter state and scroll position preserved
- Badge WCAG AA contrast and text label verified
- Keyboard navigation through cards, filter control, and all row quick-action buttons verified

---

## Summary

| ID | Gap | Severity | Action |
| --- | --- | --- | --- |
| C-01 | Card click → list filter: no AC | Critical | Add AC |
| C-02 | Admin / Supervisor list scoping: no AC | Critical | Add AC |
| C-03 | Status badge colours and text label: no AC | Critical | Add AC |
| H-01 | "Not yet played" for null last played: no AC | High | Add AC |
| H-02 | "Needs attention" empty state: no EC | High | Add EC |
| H-03 | List data fetch failure: no EC | High | Add EC |
| H-04 | Non-functional requirements absent | High | Add NFRs section |
| M-01 | Navigation landing state: no AC | Medium | Add AC |
| M-02 | Browser back preserves state: no AC | Medium | Add AC |
| M-03 | View journal on empty journal: no AC | Medium | Add AC |
| M-04 | Empty state copy mismatch (EC-04) | Medium | Align string |
| M-05 | Child record load failure EC missing | Medium | Add EC |
| L-01 | AC-06 merges two ACs | Low | Split AC-06 |
| L-02 | DoD incomplete | Low | Expand DoD |
