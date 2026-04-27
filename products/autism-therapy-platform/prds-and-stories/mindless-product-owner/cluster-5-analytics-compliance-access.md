# Cluster 5: Analytics, Reporting, Compliance & Access Control
**Product:** Autism Therapy Platform (India)
**Author:** Mindless Product Owner Agent
**Date:** 2026-04-17
**Cluster covers:** Progress/outcome tracking, analytics & reporting, data export, DPDPA compliance, two-factor authentication, role-based access control, audit trails
**Journey stages served:** Stage 2 (Intake — consent), Stage 5 (Supervisor Review), Stage 6 (Progress Reporting), Stage 7 (Billing), Stage 8 (Dropout Prevention) — plus cross-cutting security and compliance
**In-session DTT/NET data collection:** EXPLICITLY OUT OF SCOPE for this cluster

> ⚠️ **HIPAA CORRECTION — READ BEFORE PROCEEDING**
> The original feature request included "HIPAA compliant" as a feature name. **HIPAA (Health Insurance Portability and Accountability Act) is a US law. It does not apply in India.** There is no HIPAA in India — and writing HIPAA stories for an Indian product is not just wrong, it is actively misleading. The correct governing framework is **DPDPA 2023 (Digital Personal Data Protection Act, 2023)**, India's data protection law. The features in this cluster have been rewritten under DPDPA 2023. References to HIPAA have been removed entirely. Any engineering or legal team member reading this document should treat DPDPA 2023 as the sole data protection compliance reference.

---

## Feature Inspiration Table

> Source: competitive analysis at `/products/autism-therapy-platform/research/secondary/competitive-analysis-autism-therapy-software.md`, supplemented by category knowledge of SimplePractice, Jane App, CentralReach, Hi Rasmus, Theralytics, PractiPal, TherapEZ.

| Feature | Competitor(s) | Prevalence | How it works | Evidence |
|---|---|---|---|---|
| Child-level progress dashboard | CentralReach, Motivity, Hi Rasmus, Catalyst | Table stakes (US ABA tools) | Displays goal mastery status, trial accuracy trends, attendance by domain — supervisor and director view | ✅ Confirmed on product pages |
| Center-level operations dashboard | CentralReach, Theralytics, TherapEZ | Table stakes (practice mgmt tools) | Revenue collected vs. outstanding, session utilization, caseload view, enrollment vs. attrition | 🔵 Inferred from feature marketing |
| Dropout / attendance risk flags | No tool confirmed — potential differentiator | Differentiator | Attendance trend analysis to surface children with declining session frequency before full dropout | 🔶 Speculated from category gap (Competitive Analysis Finding 6) |
| Exportable PDF / CSV reports | CentralReach, Hi Rasmus, SimplePractice, Jane App | Table stakes | Download progress reports, invoices, session notes as PDF or CSV; bulk export option | ✅ Confirmed on SimplePractice, Jane App product pages |
| Parental consent management | Hi Rasmus (consent at intake), SimplePractice | Partial coverage — DPDPA equivalent is a differentiator in India | Consent capture at intake, consent version tracking, consent withdrawal flow — DPDPA-specific is novel | 🔵 Inferred; DPDPA-specific is 🔶 speculated for Indian market |
| Two-factor authentication (2FA) | SimplePractice, Jane App, CentralReach | Table stakes (any health data SaaS) | SMS OTP or authenticator app on login; session timeout after inactivity | ✅ Confirmed across health SaaS category |
| Role-based access control (RBAC) | CentralReach, Theralytics, SimplePractice, Jane App | Table stakes | Director sees all; supervisor sees assigned caseload; therapist sees own children; parent is read-only | ✅ Confirmed on CentralReach, SimplePractice docs |
| Audit trail / access log | CentralReach, SimplePractice, Jane App | Table stakes (any regulated health SaaS) | Immutable log: who accessed, created, edited, or deleted any record; timestamps; exportable | ✅ Confirmed on SimplePractice, CentralReach; required under DPDPA 2023 for sensitive data processors |
| Mobile-first analytics | Raven Health (partial), Hi Rasmus | Differentiator | Analytics dashboard designed for mobile phone use, not desktop — lightweight, card-based UI | 🔵 Inferred from category; mobile-first analytics for directors is underserved |
| Data localization / India-resident storage | No current competitor addresses India DPDPA specifically | Differentiator / Compliance | Storage of child health data in India-resident servers; DPDPA 2023 Section 16 data localization principle | ✅ DPDPA 2023 public documentation; 🔶 competitor gap is speculated |

---

---

## Feature Brief 1: Progress & Outcome Tracking

**Inspired by:** CentralReach (supervisor dashboards), Motivity (goal mastery views), Hi Rasmus (parent-visible progress), TherapEZ (attendance trends)
**Prevalence:** Table stakes (US ABA market) — Differentiator (India market, where nothing comparable exists)
**Target user:** Dr. Sunita (clinical supervisor), Rahul (center director)
**What it does:** Gives supervisors and the center director a single screen showing each child's attendance trend, goal completion rate, and a dropout risk flag if attendance drops below a configurable threshold. This is aggregate progress visibility — not in-session trial graphs. Dr. Sunita uses it to prioritize which children need program review. Rahul uses it to see center-wide retention health.
**What "done" looks like:** Dr. Sunita can open the dashboard on her Android phone, see all her assigned children's attendance and goal status at a glance, and identify the two children most at risk of dropout — in under 60 seconds, without needing a laptop.

**[ASSUMPTION — NOT VALIDATED]** This feature assumes Dr. Sunita and Rahul would use a dashboard as a regular workflow tool, not just as a report. No primary research has confirmed that supervisors in Indian centers habitually check a digital overview of their caseload. Validate before committing to complex charting infrastructure.

---

## Feature Brief 2: Analytics & Reporting (Center Operations)

**Inspired by:** Theralytics (practice analytics), CentralReach (operations reporting), TherapEZ (center management metrics), PractiPal (revenue view)
**Prevalence:** Table stakes (US practice management) — largely absent in India
**Target user:** Rahul (center director / economic buyer)
**What it does:** Gives Rahul a center operations dashboard showing: revenue collected vs. outstanding this month, sessions scheduled vs. delivered (utilization rate), therapist caseload (sessions per therapist), monthly enrollment vs. attrition, and overall dropout rate. Reports are exportable. Dashboard loads on a mid-range Android phone.
**What "done" looks like:** Rahul opens the app on his phone on the 1st of the month and sees last month's collection rate, utilization, and which therapist is overloaded — all without opening Excel.

**[ASSUMPTION — NOT VALIDATED]** This feature assumes Rahul tracks these metrics and would change decisions based on them. If Rahul's centers are small enough that he knows the numbers intuitively, a formal dashboard may not change behavior. Validate need intensity in director interviews.

---

## Feature Brief 3: Data Export

**Inspired by:** SimplePractice (PDF export of clinical records), Jane App (bulk export, CSV), CentralReach (export for compliance audits)
**Prevalence:** Table stakes (any health data SaaS)
**Target user:** Rahul (bulk export for compliance), Dr. Sunita (progress report export), Meena (data portability — right of data principal under DPDPA)
**What it does:** Allows export of individual child records, session notes, invoices, and progress reports as PDF or CSV. Includes bulk export for center transitions or compliance audits. All exports are logged in the audit trail. DPDPA-compliant: parent/guardian data subjects can request export of their child's records, and all exports require consent verification before bulk download.
**What "done" looks like:** Rahul can bulk-export all child records to a ZIP file for a compliance audit in under 5 minutes. Meena can download her child's full progress history as a PDF directly from the parent portal.

**[ASSUMPTION — NOT VALIDATED]** Bulk export for compliance audits assumes center directors are concerned enough about compliance to proactively request this. The assumption that RPWD Act / DPDPA compliance drives export behavior has not been validated in Indian therapy center context.

---

## Feature Brief 4: DPDPA Compliance

> ⚠️ **HIPAA CORRECTION — CRITICAL**
> The original feature cluster request listed this feature as "HIPAA compliant." **This is incorrect for an Indian product.** HIPAA is a US law (45 CFR Parts 160 and 164) and has no force in India. Applying HIPAA to an Indian product would mislead engineering, legal, and operations teams, create non-compliant consent flows, and potentially expose the company to regulatory risk under the actual applicable Indian law.
>
> **The correct framework is DPDPA 2023 (Digital Personal Data Protection Act, 2023).** Every story in this epic has been written against DPDPA 2023 requirements. There is no HIPAA story in this document. If any downstream document (PRD, engineering spec, legal review) references HIPAA for this product, it must be corrected.

**Inspired by:** Hi Rasmus (consent management at intake), SimplePractice (consent tracking), DPDPA 2023 public documentation
**Prevalence:** Differentiator in India — no Indian therapy software is confirmed to have DPDPA-compliant consent flows
**Target user:** Rahul (data fiduciary / center operator), Meena (data principal / parent of data subject)
**What it does:** Implements DPDPA 2023-required features for a platform processing health data of minors: verifiable parental consent at intake with purpose statement, consent version tracking, right-to-erasure workflow, consent withdrawal, data processing purpose limitation, privacy notice in accessible language, and India-resident data storage confirmation.
**What "done" looks like:** A parent can see exactly what data is held about their child, withdraw consent for specific processing purposes, and request erasure — all from the parent portal. The center can produce a consent audit log for any regulator inspection.

**[ASSUMPTION — NOT VALIDATED]** This feature assumes DPDPA 2023 compliance is a real operational concern for Indian therapy center directors. Primary research has not confirmed whether Indian center directors are aware of DPDPA obligations for minor health data. The compliance gap may be real but not yet felt as a pain point. Validate urgency in director interviews before building the full consent management flow.

---

## Feature Brief 5: Two-Factor Authentication (2FA)

**Inspired by:** SimplePractice (2FA), Jane App (2FA for practitioners), CentralReach (session security)
**Prevalence:** Table stakes (any health SaaS accessing sensitive data)
**Target user:** All staff roles (Priya, Dr. Sunita, Rahul); admin/billing role
**What it does:** Requires a second authentication factor (SMS OTP or authenticator app) for all staff logins accessing child health records. Sessions time out after a configurable inactivity period. OTP fallback via SMS is available for staff without authenticator app access.
**What "done" looks like:** Every staff login to the platform — on Android or web — prompts for OTP on first login from a new device, and re-prompts after a configurable inactivity timeout. No child health record is accessible without verified identity.

**[ASSUMPTION — NOT VALIDATED]** This feature assumes staff will tolerate the friction of OTP-based login for a tool they use multiple times per day. For Priya, who may be opening the app mid-session, 2FA friction could be a significant adoption barrier. Validate whether session-level timeout (vs. per-login OTP) is sufficient for the in-session use case.

---

## Feature Brief 6: Role-Based Access Control (RBAC)

**Inspired by:** CentralReach (role-based permissions), SimplePractice (clinician vs. admin roles), Jane App (multi-role permissions), Theralytics (supervisor vs. therapist access)
**Prevalence:** Table stakes (any multi-user health SaaS)
**Target user:** Rahul (configures roles), all staff and Meena (subject to role permissions)
**What it does:** Enforces data access boundaries by role. Center Director (Rahul) has full access to all clinical and financial data. Supervisor (Dr. Sunita) sees assigned children's records and can supervise assigned therapists. Therapist (Priya) sees only her assigned children — no access to other children's records, billing, or staff data. Parent (Meena) has read-only access limited to her own child's records. Admin/Billing role sees financial data but not clinical records.
**What "done" looks like:** Priya logs in and sees only her three assigned children. Dr. Sunita sees only children assigned to her supervision caseload. Rahul sees everything. Meena sees only Arjun's records, read-only.

**[ASSUMPTION — NOT VALIDATED]** This feature assumes Indian therapy centers have clear enough role boundaries to map to a formal RBAC model. Small centers (5–10 staff) may have significant role overlap — a therapist who also does admin, a supervisor who also delivers sessions. Validate role structure in director interviews before finalizing the role taxonomy.

---

## Feature Brief 7: Audit Trails

**Inspired by:** SimplePractice (access log), Jane App (audit log), CentralReach (activity history), DPDPA 2023 compliance requirements
**Prevalence:** Table stakes (any regulated health SaaS) — required under DPDPA 2023 for data processors handling sensitive personal data of minors
**Target user:** Rahul (compliance owner), regulators / auditors (indirect)
**What it does:** Maintains an immutable log of every access, creation, modification, and deletion event across all child records, session notes, invoices, consent records, and user accounts. Log entries include: actor, action type, record affected, timestamp, IP/device ID. Log is queryable and exportable. Log entries cannot be edited or deleted by any user — including center directors.
**What "done" looks like:** Rahul can pull a full audit log for a specific child, showing every person who accessed or modified that child's records, with timestamps — in under 2 minutes. The log is exportable as CSV for a regulator inspection.

**[ASSUMPTION — NOT VALIDATED]** This feature assumes audit trails are required by regulators or center directors. Primary research has not confirmed whether Indian autism therapy center directors are subject to, or concerned about, regulatory inspection of record access. The DPDPA requirement is real but enforcement maturity in India is early-stage.

---
---

## Epic 1: Progress & Outcome Tracking Dashboard

**Goal:** Dr. Sunita can see all her assigned children's attendance trends, goal completion rates, and dropout risk flags in one mobile-optimized screen — without manually collating data from session notes or paper files. Rahul can see center-wide attendance and goal health in the same interface.
**Copied from:** CentralReach, Motivity, Hi Rasmus
**Target user(s):** Dr. Sunita (primary), Rahul (secondary)
**Definition of Done:**
- [ ] Child-level attendance trend card renders on minimum-spec Android (Redmi/Realme, 2GB RAM) in under 3 seconds on 4G
- [ ] Dropout risk flag surfaces correctly for any child with attendance below threshold (configurable: default 2 consecutive missed sessions)
- [ ] Goal completion rate displays correctly aggregated from session data (not from in-session trial data — aggregate only)
- [ ] Dashboard is accessible without desktop — full functionality on Android mobile
- [ ] RBAC gates are enforced: Dr. Sunita sees only assigned children; Rahul sees all children
- [ ] All AC in stories PROG-001 through PROG-005 pass QA

**Out of scope (this epic):**
- In-session trial-by-trial data graphs (out of scope for entire cluster)
- Automated program modification suggestions
- Benchmarking against other children or population norms
- iOS-native version (Phase 2)
- AI-generated risk explanations

**[ASSUMPTION — NOT VALIDATED]** This epic assumes that session attendance and goal completion data is being captured digitally by other features in the product. If Cluster 1 (clinical documentation) or Cluster 2 (intake/records) are not live, this dashboard has no data to display. This epic is downstream of the core data capture pipeline.

---

### Story PROG-001: View child-level attendance trend card

**As a** Dr. Sunita (clinical supervisor)
**I want to** see a card for each of my assigned children showing their session attendance over the last 4 weeks
**So that** I can quickly identify which children have decreasing attendance and prioritize outreach before they drop out

**Inspired by:** Hi Rasmus supervisor view, Motivity caseload dashboard

**Context:** Dr. Sunita opens the app on her Android phone during a break between clinical sessions. She has 12 assigned children. She needs to identify attendance concerns in under 60 seconds without scrolling through individual records.

**Acceptance Criteria:**
- [ ] AC-01: Given Dr. Sunita is logged in with Supervisor role, when she opens the Progress Dashboard, then she sees a card list of all children assigned to her supervision caseload — no other children are visible
- [ ] AC-02: Given a child card is rendered, when Dr. Sunita views it, then it shows: child's first name, last initial, number of sessions attended in the last 4 weeks, number of sessions scheduled in the last 4 weeks, and attendance percentage
- [ ] AC-03: Given a child has attended fewer than 60% of scheduled sessions in the last 4 weeks, when their card renders, then the card displays a visual dropout risk indicator (amber badge) — no additional tap required
- [ ] AC-04: Given the card list loads, when the connection is slow (3G simulation), then the list renders in under 4 seconds with a skeleton loading state — not a blank screen
- [ ] AC-05: Given Dr. Sunita taps a child card, when the detail view opens, then she sees that child's last 8 sessions with attended/missed/cancelled status in a compact timeline — no raw trial data is shown

**Edge Cases & Error States:**
- [ ] EC-01: If a child has zero scheduled sessions in the past 4 weeks (e.g., newly enrolled), their card shows "No sessions scheduled yet" — not 0% attendance (which would trigger a false risk flag)
- [ ] EC-02: If session data is not yet synced (offline state), the card shows the last cached attendance data with a "Data as of [date]" label
- [ ] EC-03: If a child is assigned to multiple supervisors, both supervisors see the child's card; neither sees the other supervisor's assigned children

**Non-Functional Requirements:**
- Performance: Card list for up to 20 children renders in ≤ 3s on 4G; ≤ 6s on 3G
- Offline: Cached attendance data displayed with staleness label; no functionality blocked
- Accessibility: Touch targets ≥ 44px; dropout risk badge uses both color and icon (not color alone)
- Privacy: ⚠️ DPDPA — displays child health data; RBAC check must be enforced on every render; parental consent for data storage must be confirmed before this data exists in the system

**Dependencies:**
- Blocked by: RBAC-001 (role enforcement must exist before dashboard can filter by role), DPDPA-001 (consent must be captured before child records display)
- Enables: PROG-002 (center-level view aggregates from this child-level data), PROG-004 (dropout flag logic extends this view)

**Definition of Done:**
- [ ] All AC pass in QA on Redmi Note (2GB RAM, Android 10+)
- [ ] Edge cases tested including zero-session and offline states
- [ ] RBAC gate confirmed in integration test (supervisor cannot see unassigned children)
- [ ] Code reviewed and merged

---

### Story PROG-002: View center-level attendance and goal health summary

**As a** Rahul (center director)
**I want to** see a single-screen summary of all children's attendance and goal health across the entire center
**So that** I can have a 60-second Monday morning read on center retention health without opening Excel or calling staff

**Inspired by:** CentralReach operations dashboard, Theralytics practice analytics

**Context:** Rahul checks the app on his Android phone at the start of the week. He is often in back-to-back clinical or admin meetings. He needs a glanceable, no-scroll overview.

**Acceptance Criteria:**
- [ ] AC-01: Given Rahul is logged in with Director role, when he opens the Progress Dashboard, then he sees a center summary header with: total active children, center-wide attendance rate (this month), number of children with dropout risk flag, and number of children with no session in the last 14 days
- [ ] AC-02: Given the center summary renders, when Rahul views it, then below the header he sees the same child card list as the supervisor view — but including ALL active children, not filtered by supervisor assignment
- [ ] AC-03: Given there are children with dropout risk flags, when Rahul views the summary, then a "Needs attention" section at the top groups those children before the full list
- [ ] AC-04: Given Rahul taps on any child card, when the detail view opens, then he sees the same attendance timeline a supervisor sees for that child

**Edge Cases & Error States:**
- [ ] EC-01: If the center has zero active children (e.g., new center setup), the summary screen shows an empty state: "No active children enrolled yet — add your first child to get started"
- [ ] EC-02: If session data is partially synced for some children, the center summary shows data for synced children and a banner: "[N] children's data is syncing — summary may be incomplete"

**Non-Functional Requirements:**
- Performance: Center summary for up to 50 children renders in ≤ 4s on 4G
- Offline: Show last-cached summary with staleness label
- Accessibility: Summary metric cards use text labels, not just numbers; color-coded risk uses icon + text
- Privacy: ⚠️ DPDPA — Director-role RBAC check required; this screen shows aggregate data across all children

**Dependencies:**
- Blocked by: PROG-001 (center view aggregates child cards), RBAC-001
- Enables: PROG-004 (dropout risk flags visible here), ANALYTICS-001 (center operations adds revenue/utilization to this view)

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android
- [ ] Director cannot be blocked from any child card by a supervisor RBAC scope
- [ ] Code reviewed and merged

---

### Story PROG-003: View goal completion rate per child

**As a** Dr. Sunita (clinical supervisor)
**I want to** see each child's goal completion rate — the percentage of active therapy targets currently at or above mastery — at a glance
**So that** I can prioritize which children's programs need review this week without spending time manually counting mastered targets

**Inspired by:** Motivity goal mastery tracking, CentralReach target status view

**Context:** Dr. Sunita has 12 children on her caseload. She reviews programs weekly. She is on her phone between sessions — not at a desktop.

**Acceptance Criteria:**
- [ ] AC-01: Given a child's therapy program has active targets, when Dr. Sunita views that child's card, then she sees a goal completion indicator: number of targets at mastery / total active targets, displayed as "X of Y goals at mastery"
- [ ] AC-02: Given a child has 0 targets at mastery out of 5+ active targets, when the card renders, then a "Program needs review" indicator is shown on the card
- [ ] AC-03: Given Dr. Sunita taps the goal completion indicator, when the goal detail view opens, then she sees a list of all active targets with their current status: Mastered / In Progress / Not Yet Started — no trial-level data is shown in this view

**Edge Cases & Error States:**
- [ ] EC-01: If no therapy program exists for a child yet, goal completion shows "No program set up" — not 0%
- [ ] EC-02: If session note data has not been entered for more than 7 days, goal completion shows the last known status with a "Last updated [date]" label

**Non-Functional Requirements:**
- Performance: Goal status loads within the child card load time (≤ 3s total)
- Offline: Cached goal status shown with staleness label
- Privacy: ⚠️ DPDPA — goal data is part of child's health record; RBAC and consent checks apply

**Dependencies:**
- Blocked by: Cluster 1 (clinical documentation) stories that capture goal status; RBAC-001
- Enables: PROG-005 (supervisor review trigger uses this data)

**Definition of Done:**
- [ ] All AC pass in QA
- [ ] Goal status renders correctly when program exists vs. no program state
- [ ] Code reviewed and merged

---

### Story PROG-004: Dropout risk flag with configurable threshold

**As a** Rahul (center director)
**I want to** see an automated dropout risk flag on any child who has missed more than a configurable number of consecutive sessions
**So that** I can prompt outreach to at-risk families before they silently disengage — not after they've already left

**Inspired by:** No direct competitor — this is a differentiator identified in competitive analysis (Finding 6: "no tool uses attendance trend data to surface at-risk families proactively")

**Context:** Rahul is on his phone. He doesn't have time to review every child's history. He needs the system to surface the 2–3 children who need urgent follow-up.

**Acceptance Criteria:**
- [ ] AC-01: Given a child has missed 2 or more consecutive scheduled sessions, when the dashboard refreshes, then an amber "At risk" badge appears on that child's card
- [ ] AC-02: Given a child has missed 4 or more consecutive scheduled sessions, when the dashboard refreshes, then a red "High risk" badge appears on that child's card — distinct from the amber badge
- [ ] AC-03: Given Rahul (Director role) has access to center settings, when he opens notification settings, then he can configure the consecutive-miss threshold for amber flag (default: 2) and red flag (default: 4) — values between 1 and 10
- [ ] AC-04: Given a risk flag is shown, when Rahul taps the flag badge, then he is taken directly to that child's contact screen with the parent's WhatsApp number surfaced as the primary action — one tap to initiate contact

**Edge Cases & Error States:**
- [ ] EC-01: If a session is marked "Cancelled — center initiated" (not family no-show), the cancellation does not count toward the dropout risk threshold
- [ ] EC-02: If a family has communicated a planned leave of absence (flagged by admin), risk flags are suppressed for that period
- [ ] EC-03: If session data is not synced (offline), risk flags show based on last synced data with a staleness warning

**Non-Functional Requirements:**
- Performance: Risk flag calculation runs as a background job — does not block dashboard render
- Offline: Last-calculated flags shown from cache; recalculates on sync
- Accessibility: Risk flags use icon + text + color — not color alone
- Privacy: ⚠️ DPDPA — accessing family contact data from risk flag tap requires RBAC check; parent contact data is personal data under DPDPA

**Dependencies:**
- Blocked by: PROG-001, RBAC-001, session scheduling data from Cluster 4
- Enables: Center director follow-up workflows (Stage 8 of journey map)

**Definition of Done:**
- [ ] All AC pass in QA
- [ ] Flag suppression for cancelled-by-center and planned leave tested
- [ ] Threshold configuration saves and persists correctly
- [ ] Code reviewed and merged

---

### Story PROG-005: Export progress summary for a child as PDF

**As a** Dr. Sunita (clinical supervisor)
**I want to** export a one-page progress summary for a specific child as a PDF
**So that** I can share it with the family at a review meeting without printing from a desktop

**Inspired by:** Hi Rasmus (progress reports), SimplePractice (PDF export)

**Context:** Dr. Sunita is preparing for a monthly parent review meeting. She has her phone. She needs to produce a shareable summary.

**Acceptance Criteria:**
- [ ] AC-01: Given Dr. Sunita is viewing a child's progress dashboard, when she taps "Export summary," then she is shown a preview of a one-page PDF containing: child name, reporting period, attendance summary, goal completion rate, goals at mastery (list), goals in progress (list)
- [ ] AC-02: Given the preview is shown, when Dr. Sunita taps "Download," then a PDF file is saved to her device's Downloads folder and a share sheet is triggered (standard Android share)
- [ ] AC-03: Given a PDF is exported, when the export completes, then an audit log entry is created: actor, timestamp, child record, export type = "Progress Summary PDF"
- [ ] AC-04: Given the PDF is opened, when any user views it, then it contains a footer: "Generated by [Platform name] on [Date]. Confidential — for authorized recipients only."

**Edge Cases & Error States:**
- [ ] EC-01: If the child has no session data for the selected reporting period, the PDF shows "No session data recorded for this period" — not a blank document
- [ ] EC-02: If the PDF generation fails (server error), Dr. Sunita sees an error state: "Export failed — try again" with a retry button

**Non-Functional Requirements:**
- Performance: PDF generation completes in ≤ 5 seconds for a standard one-page summary
- Offline: Export requires connectivity; if offline, show "Export requires internet connection"
- Privacy: ⚠️ DPDPA — export of child health data must be logged in audit trail; RBAC must confirm Dr. Sunita is assigned to this child before export is permitted
- Accessibility: Export button ≥ 44px touch target

**Dependencies:**
- Blocked by: AUDIT-001 (audit log must exist before export logging works), RBAC-001
- Enables: EXPORT-001 (this is the single-child export; bulk export is a separate story)

**Definition of Done:**
- [ ] All AC pass in QA
- [ ] PDF renders correctly on mobile screen (readable without zooming)
- [ ] Audit log entry confirmed in integration test
- [ ] Code reviewed and merged

---

## Backlog: Epic 1 — Progress & Outcome Tracking

| Story ID | Title | Persona | Complexity | Priority | Blocked by |
|---|---|---|---|---|---|
| PROG-001 | View child-level attendance trend card | Dr. Sunita | M | P0 | RBAC-001, DPDPA-001 |
| PROG-002 | View center-level attendance and goal health summary | Rahul | M | P0 | PROG-001, RBAC-001 |
| PROG-003 | View goal completion rate per child | Dr. Sunita | M | P1 | Cluster 1 clinical data, RBAC-001 |
| PROG-004 | Dropout risk flag with configurable threshold | Rahul | L | P1 | PROG-001, RBAC-001, Cluster 4 scheduling |
| PROG-005 | Export progress summary for a child as PDF | Dr. Sunita | M | P1 | AUDIT-001, RBAC-001 |

---
---

## Epic 2: Analytics & Reporting (Center Operations)

**Goal:** Rahul can open the app on his Android phone and see — in under 60 seconds — his center's revenue collected vs. outstanding, session utilization rate, therapist caseload, and monthly enrollment vs. attrition. Reports are exportable. He does not need Excel or a desktop to get this picture.
**Copied from:** Theralytics, CentralReach operations dashboard, TherapEZ center management
**Target user(s):** Rahul (center director — sole primary user)
**Definition of Done:**
- [ ] Revenue dashboard renders on minimum-spec Android in ≤ 4s on 4G
- [ ] All metrics (revenue, utilization, caseload, attrition) are calculated correctly against test data
- [ ] Export of monthly report to PDF completes in ≤ 10 seconds
- [ ] RBAC enforced: only Director role and Admin/Billing role can access financial metrics
- [ ] All AC in stories ANALYTICS-001 through ANALYTICS-004 pass QA

**Out of scope (this epic):**
- Insurance billing or claims management (not applicable in India)
- Staff payroll calculation
- Multi-center / chain management (Phase 2)
- Real-time financial reconciliation with UPI gateway (Phase 2 — initial version uses manual payment confirmation)
- Predictive revenue forecasting

**[ASSUMPTION — NOT VALIDATED]** This epic assumes Rahul checks operational metrics regularly enough to make a dashboard useful. If center sizes are small enough (5–15 children) that Rahul knows the numbers in his head, a formal analytics dashboard may not change behavior. Validate metric-checking frequency in director interviews.

---

### Story ANALYTICS-001: View monthly revenue dashboard

**As a** Rahul (center director)
**I want to** see this month's total revenue collected, outstanding fees, and collection rate on one screen
**So that** I can know whether my cash flow is healthy without tallying WhatsApp payment notifications or scrolling Excel

**Inspired by:** PractiPal (revenue view), TherapEZ (invoicing summary), Jane App (financial dashboard)

**Context:** Rahul checks his phone on the 1st of the month. He wants a fast financial read before calling outstanding families.

**Acceptance Criteria:**
- [ ] AC-01: Given Rahul is logged in as Director, when he opens the Analytics tab, then he sees a Revenue card showing: total invoiced this month, total collected this month, total outstanding this month, and collection rate as a percentage
- [ ] AC-02: Given the Revenue card is displayed, when Rahul taps "View outstanding," then he sees a list of families with outstanding balances, sorted by amount owed (highest first), with each family's name, outstanding amount, and number of days overdue
- [ ] AC-03: Given Rahul views the outstanding list, when he taps a family row, then he is taken to that family's billing record with a "Send reminder" action surfaced
- [ ] AC-04: Given Rahul wants to export the month's revenue summary, when he taps "Export," then a PDF report is generated with: center name, month, invoiced/collected/outstanding totals, and a list of all invoices with payment status

**Edge Cases & Error States:**
- [ ] EC-01: If no invoices have been created this month, the Revenue card shows "No invoices this month — get started by creating your first invoice"
- [ ] EC-02: If invoice data is not synced (offline), the dashboard shows last-synced data with a staleness banner
- [ ] EC-03: If Rahul is also using Admin/Billing role for a staff member, that staff member sees the revenue dashboard but cannot see clinical records — the financial view is the same for both Director and Admin/Billing roles

**Non-Functional Requirements:**
- Performance: Revenue dashboard renders in ≤ 4s on 4G; ≤ 8s on 3G
- Offline: Show cached data with staleness label; export requires connectivity
- Privacy: ⚠️ DPDPA — financial data includes personal data (family names, amounts); RBAC check required; this data is not child health data but is personal data under DPDPA
- Accessibility: All monetary values include currency label (₹); collection rate shown as text percentage + visual bar

**Dependencies:**
- Blocked by: RBAC-001, Cluster 3 (billing/invoices must exist), AUDIT-001
- Enables: ANALYTICS-004 (monthly report export pulls from this data)

**Definition of Done:**
- [ ] All AC pass in QA
- [ ] Non-Director role cannot access this screen (confirmed in integration test)
- [ ] Outstanding list correctly sorted and filtered
- [ ] Code reviewed and merged

---

### Story ANALYTICS-002: View session utilization rate

**As a** Rahul (center director)
**I want to** see how many sessions were scheduled vs. actually delivered this month, broken down by therapist
**So that** I can identify therapists who are underutilized or overloaded, and whether no-shows are eating into center capacity

**Inspired by:** CentralReach utilization reports, Theralytics staff performance analytics

**Context:** Rahul is managing 4 therapists. He suspects one therapist has a high no-show rate but doesn't have the data to confirm it.

**Acceptance Criteria:**
- [ ] AC-01: Given Rahul opens the Analytics tab, when he scrolls to the Utilization section, then he sees: total sessions scheduled this month, total sessions delivered, total cancellations (center-initiated vs. family-initiated), and utilization rate as a percentage
- [ ] AC-02: Given the utilization summary is displayed, when Rahul taps "By therapist," then he sees a list of all therapists with their individual: sessions scheduled, sessions delivered, cancellations, and utilization rate — sorted by utilization rate (lowest first)
- [ ] AC-03: Given a therapist has a utilization rate below 70% for the month, when Rahul views the therapist breakdown, then that therapist's row is visually flagged (e.g., amber indicator)

**Edge Cases & Error States:**
- [ ] EC-01: If a therapist has zero scheduled sessions (e.g., on leave), their utilization shows "On leave" — not 0% utilization
- [ ] EC-02: If session data is partially synced, utilization shows with a "Partial data" warning and the number of unsynced sessions

**Non-Functional Requirements:**
- Performance: Utilization data renders in ≤ 4s on 4G
- Offline: Cached data with staleness label
- Privacy: ⚠️ DPDPA — therapist performance data is personal data under DPDPA (staff are data principals); Rahul as employer/data fiduciary processes this data; purpose limitation applies

**Dependencies:**
- Blocked by: RBAC-001, Cluster 4 (scheduling data must exist)
- Enables: Staff caseload view (ANALYTICS-003)

**Definition of Done:**
- [ ] All AC pass in QA
- [ ] On-leave state tested correctly
- [ ] Partial-sync warning tested
- [ ] Code reviewed and merged

---

### Story ANALYTICS-003: View therapist caseload and enrollment vs. attrition

**As a** Rahul (center director)
**I want to** see each therapist's current active caseload and the center's monthly enrollment vs. attrition trend
**So that** I can rebalance caseloads before a therapist burns out, and see whether the center is growing or shrinking

**Inspired by:** CentralReach caseload management, Theralytics enrollment analytics

**Context:** Rahul is doing monthly center operations review. He is on his phone.

**Acceptance Criteria:**
- [ ] AC-01: Given Rahul views the Analytics tab, when he scrolls to Caseload, then he sees a list of all therapists with their current active child count — sorted by count (highest first)
- [ ] AC-02: Given Rahul views the Enrollment section, when he views the current month, then he sees: new children enrolled this month, children who have exited/dropped out this month, and net change
- [ ] AC-03: Given Rahul taps on the enrollment trend, when the detail view opens, then he sees a 6-month rolling view of monthly enrollment vs. exits as a simple bar or number table — not a heavy chart library

**Edge Cases & Error States:**
- [ ] EC-01: If a child's exit is unconfirmed (last session was 30+ days ago with no formal exit recorded), they show in a "Likely inactive — confirm status" section, not counted in attrition until confirmed

**Non-Functional Requirements:**
- Performance: Caseload list renders in ≤ 3s; 6-month trend table renders in ≤ 4s
- Offline: Cached view with staleness label
- Device: 6-month trend must render as a lightweight number table on 2GB RAM Android — no heavy chart rendering library

**Dependencies:**
- Blocked by: RBAC-001, Cluster 2 (enrollment records), Cluster 4 (scheduling)
- Enables: ANALYTICS-004 (monthly report)

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android
- [ ] Likely-inactive edge case tested
- [ ] 6-month trend renders without performance degradation on 2GB RAM device
- [ ] Code reviewed and merged

---

### Story ANALYTICS-004: Export monthly operations report as PDF

**As a** Rahul (center director)
**I want to** export a one-page monthly operations report as PDF
**So that** I can share it with a co-founder, bank, or advisor without copying numbers from the app into a document

**Inspired by:** Jane App (monthly summary export), SimplePractice (report export)

**Context:** Rahul shares a monthly operations summary with his spouse (co-founder) and an external accountant. He does this on the last day of each month.

**Acceptance Criteria:**
- [ ] AC-01: Given Rahul is on the Analytics tab, when he taps "Export monthly report," then he is prompted to select the month/year and report sections to include (Revenue, Utilization, Enrollment — each toggleable)
- [ ] AC-02: Given Rahul confirms the export, when the PDF generates, then it contains: center name, selected month, all selected sections with their metrics, and a footer with generation date and "Confidential"
- [ ] AC-03: Given the PDF is generated, when the export completes, then an audit log entry is created: actor, timestamp, export type = "Operations Report PDF," period exported
- [ ] AC-04: Given the PDF generation fails, when Rahul sees the error state, then the message is: "Export failed — check your connection and try again" with a retry button

**Edge Cases & Error States:**
- [ ] EC-01: If no data exists for the selected month, the PDF includes a section marked "No data recorded for this period" — it does not generate a blank document

**Non-Functional Requirements:**
- Performance: PDF generation completes in ≤ 10 seconds
- Offline: Export requires connectivity; show error with retry if offline
- Privacy: ⚠️ DPDPA — exported report contains personal data (financial, staff data); export logged in audit trail; only Director and Admin/Billing roles may export

**Dependencies:**
- Blocked by: ANALYTICS-001, ANALYTICS-002, ANALYTICS-003, AUDIT-001
- Enables: None (terminal action)

**Definition of Done:**
- [ ] All AC pass in QA
- [ ] PDF renders correctly on all selected/deselected section combinations
- [ ] Audit log entry confirmed
- [ ] Code reviewed and merged

---

## Backlog: Epic 2 — Analytics & Reporting

| Story ID | Title | Persona | Complexity | Priority | Blocked by |
|---|---|---|---|---|---|
| ANALYTICS-001 | View monthly revenue dashboard | Rahul | M | P0 | RBAC-001, Cluster 3 billing, AUDIT-001 |
| ANALYTICS-002 | View session utilization rate | Rahul | M | P1 | RBAC-001, Cluster 4 scheduling |
| ANALYTICS-003 | View therapist caseload and enrollment vs. attrition | Rahul | M | P1 | RBAC-001, Cluster 2 records, Cluster 4 scheduling |
| ANALYTICS-004 | Export monthly operations report as PDF | Rahul | M | P1 | ANALYTICS-001, ANALYTICS-002, ANALYTICS-003, AUDIT-001 |

---
---

## Epic 3: Data Export

**Goal:** Rahul can bulk-export all child records for a compliance audit in one action. Dr. Sunita can export a child's records as PDF for a family meeting. Meena can download her child's records exercising her right to data portability under DPDPA 2023. All exports are logged in the audit trail.
**Copied from:** SimplePractice, Jane App, CentralReach
**Target user(s):** Rahul (bulk export, compliance), Dr. Sunita (per-child export), Meena (data portability)
**Definition of Done:**
- [ ] Single-child PDF export completes in ≤ 5 seconds
- [ ] Bulk export of all center records generates ZIP in ≤ 2 minutes for a center with up to 50 children
- [ ] All exports create an audit log entry (actor, timestamp, scope of export)
- [ ] DPDPA consent check required before bulk export — export cannot proceed if consent is withdrawn for any included child
- [ ] RBAC enforced: Priya (therapist) cannot trigger bulk export; only Director role can
- [ ] All AC in stories EXPORT-001 through EXPORT-004 pass QA

**Out of scope (this epic):**
- Real-time API data export / webhooks (Phase 2)
- Export to external EHR systems
- Automatic scheduled exports
- Anonymized / de-identified export for research purposes

**[ASSUMPTION — NOT VALIDATED]** This epic assumes center directors need bulk export for compliance audits (RPWD Act, DPDPA). The frequency and formality of such audits in Indian autism therapy centers has not been confirmed by primary research.

---

### Story EXPORT-001: Export a child's complete record as PDF

**As a** Dr. Sunita (clinical supervisor) or Rahul (center director)
**I want to** export a specific child's complete record — intake form, session notes, therapy program, and progress reports — as a single PDF
**So that** I can share it with a new therapist, another center, or the family at a transition without manually assembling documents

**Inspired by:** SimplePractice (full client record export), Jane App (client export)

**Context:** A family is transitioning to a different therapy center. Dr. Sunita needs to export everything about the child in one document.

**Acceptance Criteria:**
- [ ] AC-01: Given Dr. Sunita is viewing a child's record, when she taps "Export full record," then she is shown a checklist of record sections to include: Intake form, Therapy programs, Session notes (with date range selector), Progress reports, Invoices (if Director role only)
- [ ] AC-02: Given Dr. Sunita selects sections and taps "Generate PDF," when the export completes, then a PDF is downloaded to her device and a share sheet is triggered
- [ ] AC-03: Given any export is initiated, when it completes, then an audit log entry is created: actor, role, child record, sections exported, timestamp
- [ ] AC-04: Given the child has a DPDPA consent record, when the export is initiated, then the system confirms consent is active for the "share with external party" purpose — if consent for this purpose is not recorded, a warning is shown: "Consent for sharing records externally has not been confirmed. Proceed only if you have verbal consent from the parent."
- [ ] AC-05: Given the PDF is generated, when it is opened, then it includes a cover page with: child first name, last initial, center name, export date, "CONFIDENTIAL — Health record of a minor"

**Edge Cases & Error States:**
- [ ] EC-01: If a section has no data (e.g., no invoices), that section is excluded from the PDF with a note: "[Section] — No records found for this period"
- [ ] EC-02: If the child's record is incomplete (missing mandatory intake fields), the export proceeds but includes a notice on the cover: "Record may be incomplete — verify with center before clinical use"
- [ ] EC-03: If the PDF generation fails, a retry option is shown; the audit log entry records the failed attempt

**Non-Functional Requirements:**
- Performance: PDF generation for a full record (12 months, 50 session notes) completes in ≤ 15 seconds
- Offline: Export requires connectivity
- Privacy: ⚠️ DPDPA — child health record export is a high-risk data operation; audit trail entry is mandatory; consent check for external sharing purpose required
- Accessibility: Touch targets ≥ 44px on section checklist

**Dependencies:**
- Blocked by: AUDIT-001 (export logging), DPDPA-001 (consent status check), RBAC-001
- Enables: EXPORT-003 (bulk export is the multi-child version of this)

**Definition of Done:**
- [ ] All AC pass in QA
- [ ] Consent warning tested with child who has no external-sharing consent recorded
- [ ] Failed export audit log entry confirmed
- [ ] Code reviewed and merged

---

### Story EXPORT-002: Export invoices as CSV for accounting

**As a** Rahul (center director) or Admin/Billing role
**I want to** export all invoices for a selected date range as a CSV file
**So that** I can import it into my accountant's spreadsheet without manually copying numbers

**Inspired by:** Jane App (CSV invoice export), PractiPal (invoice records)

**Context:** Rahul sends his accountant a monthly CSV of all transactions. He does this on the last day of each month.

**Acceptance Criteria:**
- [ ] AC-01: Given Rahul is on the Billing section, when he taps "Export invoices," then he selects a date range and format (CSV or PDF list)
- [ ] AC-02: Given the export request is confirmed, when the CSV is generated, then it contains one row per invoice: invoice ID, child name, invoice date, amount billed, amount paid, outstanding, payment date (if paid), payment method (Cash/UPI)
- [ ] AC-03: Given the CSV is exported, when the export completes, then an audit log entry is created
- [ ] AC-04: Given the CSV is opened in a spreadsheet app, when rows are viewed, then child names appear as "First name, Last initial" only — not full name — to minimize personal data exposure in plain-text CSV

**Edge Cases & Error States:**
- [ ] EC-01: If no invoices exist in the selected date range, the CSV contains only the header row and a note row: "No invoices in selected period"

**Non-Functional Requirements:**
- Performance: CSV export for up to 500 invoice rows completes in ≤ 5 seconds
- Privacy: ⚠️ DPDPA — financial data with child identifiers is personal data; export logged; only Director and Admin/Billing roles may export

**Dependencies:**
- Blocked by: AUDIT-001, RBAC-001, Cluster 3 billing
- Enables: None (terminal action)

**Definition of Done:**
- [ ] All AC pass in QA
- [ ] CSV format validated by importing into Google Sheets
- [ ] Audit log entry confirmed
- [ ] Code reviewed and merged

---

### Story EXPORT-003: Bulk export all center records (compliance audit pack)

**As a** Rahul (center director)
**I want to** export all child records, session notes, consent forms, and invoices as a single ZIP file
**So that** I can respond to a RPWD Act or DPDPA regulator audit request without manually assembling hundreds of documents

**Inspired by:** CentralReach (bulk export), SimplePractice (account data export)

**Context:** A center receives an external audit notice. Rahul needs to produce all records for the past 2 years within 48 hours.

**Acceptance Criteria:**
- [ ] AC-01: Given Rahul is in Settings > Data Management, when he initiates "Bulk Export All Records," then he is shown a confirmation screen with: scope (all children, all date range), estimated file size, and a warning: "This export contains sensitive health data of minors. Ensure it is handled securely. Only proceed if you have a valid compliance reason."
- [ ] AC-02: Given Rahul confirms, when the bulk export runs, then a background job generates a structured ZIP file: one folder per child, each containing their intake form (PDF), therapy programs (PDF), session notes (PDF), consent records (PDF), and invoices (CSV)
- [ ] AC-03: Given the export is complete, when Rahul is notified, then he receives an in-app notification with a download link valid for 24 hours — the download link is not shareable (tied to his session)
- [ ] AC-04: Given the bulk export is initiated, when the process starts, then an audit log entry is created immediately: actor, timestamp, export scope, "Compliance bulk export"
- [ ] AC-05: Given any child in the export has withdrawn consent for data processing, when the export runs, then that child's records are flagged in a "Consent withdrawn — records excluded per DPDPA right to erasure" subfolder

**Edge Cases & Error States:**
- [ ] EC-01: If the bulk export exceeds 500MB, the job splits into multiple ZIP files (Part 1, Part 2, etc.) and notifies Rahul accordingly
- [ ] EC-02: If the export job fails mid-way, Rahul receives an error notification and the partial export is discarded — no partial ZIP is made available

**Non-Functional Requirements:**
- Performance: Bulk export for 50 children × 2 years of records completes in ≤ 10 minutes (background job)
- Offline: Export initiation requires connectivity; cannot be initiated offline
- Privacy: ⚠️ DPDPA — highest-risk operation in the platform; mandatory audit log; Director-role only; consent withdrawal exclusion is mandatory, not optional; download link must expire
- Security: Download link must be one-time-use or session-bound — cannot be emailed without encryption

**Dependencies:**
- Blocked by: AUDIT-001, DPDPA-001 (consent status check per child), RBAC-001
- Enables: None (terminal compliance action)

**Definition of Done:**
- [ ] All AC pass in QA
- [ ] Consent-withdrawn child exclusion confirmed in integration test
- [ ] Download link expiry confirmed (24h)
- [ ] Bulk export size split confirmed for large datasets
- [ ] Code reviewed and merged

---

### Story EXPORT-004: Parent data portability — download child's records from parent portal

**As a** Meena (parent / data principal under DPDPA 2023)
**I want to** download all data held about my child from the parent portal
**So that** I can exercise my right to data portability under DPDPA 2023 Section 12, and verify what the center has recorded about Arjun

**Inspired by:** DPDPA 2023 data principal rights, GDPR-equivalent data portability patterns (for UX reference only — GDPR does not apply in India)

**Context:** Meena has heard concerns from another parent about data privacy. She wants to see exactly what the center has stored about her child.

**Acceptance Criteria:**
- [ ] AC-01: Given Meena is logged into the parent portal, when she navigates to Account > My Child's Data, then she sees an option "Download all records" with a plain-language explanation: "You have the right to a copy of all information we hold about [child name]. This will include session records, progress reports, and intake information."
- [ ] AC-02: Given Meena requests a download, when the request is processed, then she receives a PDF within 24 hours (or immediately if the record is small) containing all records the center holds about her child — in plain, non-clinical language where possible
- [ ] AC-03: Given the download is requested, when it is processed, then an audit log entry is created: actor (parent), child record, timestamp, "Data portability request — DPDPA S.12"
- [ ] AC-04: Given Meena's download is available, when she opens the PDF, then it includes a cover note: "This document contains all personal and health data recorded about [child name] by [Center name]. If you believe any information is inaccurate, please contact [Center name] directly."

**Edge Cases & Error States:**
- [ ] EC-01: If the child's records are currently under a DPDPA erasure request processing, the download shows records as of the date prior to the erasure request with a notice that the request is being processed

**Non-Functional Requirements:**
- Performance: For small records (< 12 months), PDF available immediately. For large records (> 2 years), within 24 hours via in-app notification
- Privacy: ⚠️ DPDPA — this is a mandatory right under DPDPA 2023 Section 12; the platform must not block, delay, or require justification for this request; response must be within 30 days (DPDPA requirement) though the product target is 24 hours
- Accessibility: Plain-language cover note is essential; clinical terminology must be explained

**Dependencies:**
- Blocked by: DPDPA-001 (consent and data principal rights framework), RBAC-001 (parent portal role)
- Enables: DPDPA-004 (right to erasure — natural follow-on after parent reviews their data)

**Definition of Done:**
- [ ] All AC pass in QA
- [ ] Audit log entry confirmed for parent-initiated export
- [ ] Plain-language cover note reviewed by a non-clinical person (readability check)
- [ ] Code reviewed and merged

---

## Backlog: Epic 3 — Data Export

| Story ID | Title | Persona | Complexity | Priority | Blocked by |
|---|---|---|---|---|---|
| EXPORT-001 | Export a child's complete record as PDF | Dr. Sunita, Rahul | M | P1 | AUDIT-001, DPDPA-001, RBAC-001 |
| EXPORT-002 | Export invoices as CSV for accounting | Rahul | S | P1 | AUDIT-001, RBAC-001, Cluster 3 |
| EXPORT-003 | Bulk export all center records (compliance audit pack) | Rahul | XL | P2 | AUDIT-001, DPDPA-001, RBAC-001 |
| EXPORT-004 | Parent data portability — download child's records | Meena | M | P1 | DPDPA-001, RBAC-001 |

---
---

## Epic 4: DPDPA 2023 Compliance

> ⚠️ **HIPAA DOES NOT APPLY HERE — REREAD THE CORRECTION NOTE AT THE TOP OF THIS DOCUMENT BEFORE PROCEEDING.** Every story in this epic is written against DPDPA 2023 only. No HIPAA requirement appears anywhere in this epic. If a developer, legal reviewer, or engineering manager raises HIPAA in the context of this product, direct them to the DPDPA 2023 public documentation and the India-specific context section in the product CLAUDE.md file.

**Goal:** The platform captures verifiable parental consent for minors' health data at intake, tracks consent versions, enables consent withdrawal, surfaces the right-to-erasure flow, and provides parents with a plain-language privacy notice. The center director can produce a consent audit log for any DPDPA inspection. Data is stored in India-resident infrastructure.
**Copied from:** Hi Rasmus (consent management), SimplePractice (consent tracking), DPDPA 2023 public documentation
**Target user(s):** Rahul (data fiduciary), Meena (data principal), platform compliance (non-user)
**Definition of Done:**
- [ ] Consent capture flow completed at intake for every new child — no child record can be activated without parental consent confirmation
- [ ] Consent withdrawal flow tested end-to-end (consent withdrawn → data processing flagged → erasure workflow triggered)
- [ ] Consent audit log exportable by Director role
- [ ] Privacy notice accessible from parent portal with plain-language content (reviewed by a non-clinical reader)
- [ ] Data localization: all child health data stored in India-resident cloud storage (confirmed with infrastructure team)
- [ ] All AC in stories DPDPA-001 through DPDPA-005 pass QA

**Out of scope (this epic):**
- Multi-language privacy notice (Hindi, regional languages — Phase 2)
- Automated DPDPA compliance reports for regulators (Phase 2)
- Data processing agreements with third-party vendors (legal team scope, not product scope)
- Cross-border data transfer controls (Phase 2 — only relevant if data is shared with international tools)

**[ASSUMPTION — NOT VALIDATED]** This epic assumes center directors understand they are data fiduciaries under DPDPA 2023 and bear legal obligations for consent management. Primary research has not confirmed awareness of DPDPA obligations among Indian therapy center directors (Hypothesis H-06 in journey map — high uncertainty, high risk).

---

### Story DPDPA-001: Capture verifiable parental consent at intake

**As a** Rahul (center director / data fiduciary)
**I want to** capture a parent's consent for their child's health data to be processed by the platform at the time of intake
**So that** the center is compliant with DPDPA 2023 Section 9 (processing of children's data requires verifiable parental consent) and I have a timestamped consent record

**Inspired by:** Hi Rasmus (digital consent at intake), SimplePractice (consent forms), DPDPA 2023 Section 9

**Context:** A new family arrives for intake. Rahul or admin is creating the child's record in the system.

**Acceptance Criteria:**
- [ ] AC-01: Given admin is creating a new child's record, when they reach the "Consent" step of the intake flow, then they cannot complete intake and activate the child's record without completing the consent capture step
- [ ] AC-02: Given the consent step is shown, when admin presents it to the parent, then the consent form displays in plain English (Phase 2: Hindi/regional): the purpose of data collection ("We collect your child's health and therapy records to provide therapy services and track progress"), who can access it (named roles only), how long it is retained, and the parent's rights (access, correction, erasure, withdrawal)
- [ ] AC-03: Given the parent reviews the consent form, when admin records consent, then the system captures: parent's full name, relationship to child, date and time, platform version of the consent notice, method of consent (in-person digital signature or checkbox confirmation), and the admin who recorded it
- [ ] AC-04: Given consent is captured, when the child's record is activated, then the consent record is stored as an immutable entry — it cannot be edited or deleted by any user, including the director
- [ ] AC-05: Given an existing child's record was created before this feature shipped, when an admin opens that record, then a "Consent pending" banner is shown prompting them to complete the consent capture at the next family visit

**Edge Cases & Error States:**
- [ ] EC-01: If a parent refuses to give consent, the child's record remains in a "Pending consent" state — session data cannot be entered until consent is given, but the record itself can exist for scheduling purposes
- [ ] EC-02: If a parent is not present at intake (child brought by a guardian), the guardian's name and relationship to the child are captured instead, with a flag: "Guardian consent — verify against DPDPA Section 9 if legal guardianship is not formally established"

**Non-Functional Requirements:**
- Performance: Consent capture screen loads in ≤ 2s
- Offline: Consent capture requires connectivity (immutable record must be server-confirmed, not just queued locally)
- Privacy: ⚠️ DPDPA — this story IS the DPDPA compliance gate for the entire platform. Without it, no child health data should be stored or processed. It is a P0 dependency for every other data story in the product.
- Accessibility: Consent text must be at a reading level accessible to non-clinical adults; font size ≥ 16px on mobile

**Dependencies:**
- Blocked by: RBAC-001 (admin and director roles needed to run intake)
- Enables: EVERY OTHER STORY IN THIS PRODUCT that stores or processes child health data. This is the root dependency for the entire data pipeline.

**Definition of Done:**
- [ ] All AC pass in QA
- [ ] Consent record confirmed as immutable in database (no update/delete endpoint exists for consent records)
- [ ] Pending-consent state correctly blocks session data entry
- [ ] Code reviewed and merged

---

### Story DPDPA-002: Consent withdrawal and data processing suspension

**As a** Meena (parent / data principal)
**I want to** withdraw my consent for my child's data to be processed
**So that** I can exercise my right under DPDPA 2023 Section 6(4) (right to withdraw consent) and stop new data being created about my child — even if I do not request full erasure

**Inspired by:** DPDPA 2023 Section 6(4), SimplePractice consent management

**Context:** Meena decides to move her child to a different center. Before leaving, she wants to stop new data being recorded.

**Acceptance Criteria:**
- [ ] AC-01: Given Meena is logged into the parent portal, when she navigates to Account > Privacy > My Consent, then she sees her current active consent with the date it was given and the purposes it covers
- [ ] AC-02: Given Meena taps "Withdraw consent," when the withdrawal flow is shown, then she sees a plain-language explanation of what withdrawal means: "If you withdraw consent, no new therapy or session records will be created for [child name]. Existing records will remain unless you also request erasure. The center will be notified."
- [ ] AC-03: Given Meena confirms withdrawal, when it is processed, then: the child's record is moved to "Consent withdrawn" status, new session notes and progress entries cannot be created for the child, existing records remain accessible to authorized staff but no new data is written, and Rahul receives an in-app notification: "[Child first name]'s parent has withdrawn data processing consent."
- [ ] AC-04: Given consent is withdrawn, when the withdrawal is confirmed, then an audit log entry is created: actor (parent), child record, timestamp, "Consent withdrawal — DPDPA S.6(4)"

**Edge Cases & Error States:**
- [ ] EC-01: If a session is in progress at the moment consent is withdrawn, the in-progress session note is allowed to complete but flagged; no new sessions can be started after withdrawal is confirmed
- [ ] EC-02: If Rahul re-contacts the family and they re-consent, a new consent record is created (no modification of the withdrawal record — all events are immutable); a new consent record supersedes the withdrawal

**Non-Functional Requirements:**
- Offline: Withdrawal requires connectivity — must be server-confirmed immediately
- Privacy: ⚠️ DPDPA — this is a mandatory right under DPDPA 2023. The platform must not require justification, charge for it, or delay it beyond the session. Response within 24 hours is the platform target.

**Dependencies:**
- Blocked by: DPDPA-001, RBAC-001 (parent portal role)
- Enables: DPDPA-004 (right to erasure is the follow-on from withdrawal)

**Definition of Done:**
- [ ] All AC pass in QA
- [ ] "Consent withdrawn" status correctly blocks new session note creation
- [ ] Re-consent flow tested (withdrawal → new consent record)
- [ ] Audit log entries confirmed for both withdrawal and re-consent
- [ ] Code reviewed and merged

---

### Story DPDPA-003: Privacy notice — accessible, plain-language, parent portal

**As a** Meena (parent / data principal)
**I want to** read a plain-language privacy notice that tells me what data is collected about my child, why, who can access it, and how long it is kept
**So that** I can make an informed decision about consent — as required by DPDPA 2023 Section 6(2) (consent must be informed and specific to a purpose)

**Inspired by:** DPDPA 2023 Section 6(2), Hi Rasmus (privacy-first parent communication)

**Context:** Meena is at intake. Admin shows her the consent form on a tablet or phone. She needs to understand it.

**Acceptance Criteria:**
- [ ] AC-01: Given the consent form is presented, when Meena views it, then it contains — in plain English — the following sections: (1) What data we collect, (2) Why we collect it (purposes, each listed separately), (3) Who can see it (roles listed plainly), (4) How long we keep it, (5) Your rights (access, correction, erasure, withdrawal), (6) How to contact us about your data
- [ ] AC-02: Given Meena is logged into the parent portal, when she navigates to Account > Privacy, then she can access the current privacy notice at any time — not just at intake
- [ ] AC-03: Given the privacy notice is updated (e.g., new processing purposes added), when Meena next logs into the parent portal, then she is shown a banner: "Our privacy notice has been updated. Please review and re-confirm your consent." She cannot dismiss this banner without tapping "Review" (she can choose not to re-consent, which triggers the withdrawal flow)
- [ ] AC-04: Given the consent notice is displayed, when admin presents it on a mobile device, then the text is ≥ 16px, with adequate line spacing — readable without pinch-zooming on a mid-range Android

**Edge Cases & Error States:**
- [ ] EC-01: If a parent cannot read English, admin can present the verbal explanation and check "Explained verbally in [language]" — this is captured in the consent record but a Phase 2 item to produce a translated notice

**Non-Functional Requirements:**
- Accessibility: Minimum 16px font; line height ≥ 1.5; WCAG AA contrast
- Privacy: ⚠️ DPDPA — the privacy notice IS a DPDPA compliance requirement, not a UX nicety

**Dependencies:**
- Blocked by: DPDPA-001 (consent capture flow is where notice is presented)
- Enables: DPDPA-001 (notice must be reviewed before consent can be validly given)

**Definition of Done:**
- [ ] Privacy notice content reviewed by a non-clinical adult for comprehension
- [ ] All AC pass in QA
- [ ] Update notification banner tested with a simulated notice update
- [ ] Code reviewed and merged

---

### Story DPDPA-004: Right to erasure — parent-initiated data deletion request

**As a** Meena (parent / data principal)
**I want to** request that all data about my child be erased from the platform
**So that** I can exercise my right to erasure under DPDPA 2023 Section 12(c) when I no longer want the center to hold my child's records

**Inspired by:** DPDPA 2023 Section 12(c), GDPR erasure UX patterns (reference only — GDPR does not apply in India)

**Context:** Meena's child has completed therapy and she wants all records removed. Or she is withdrawing from the center entirely.

**Acceptance Criteria:**
- [ ] AC-01: Given Meena is in Account > Privacy, when she taps "Request data erasure," then she sees a plain-language confirmation: "Requesting erasure will permanently delete all records about [child name] from our system. This cannot be undone. The center will no longer have access to your child's therapy history. Are you sure you want to continue?"
- [ ] AC-02: Given Meena confirms the erasure request, when it is submitted, then Rahul receives an in-app notification: "[Child name]'s parent has requested data erasure. You have 30 days to complete this under DPDPA 2023." A task is created in Rahul's admin queue.
- [ ] AC-03: Given Rahul processes the erasure, when he confirms completion, then all of the child's records — session notes, therapy programs, intake form, consent record, invoices — are deleted from active storage. The audit log retains only: child ID (anonymized), erasure date, actor who processed it, "DPDPA erasure request." No clinical data is retained.
- [ ] AC-04: Given the erasure is complete, when Meena logs into the parent portal, then her child no longer appears in her account and she sees: "Your erasure request has been completed. No data about [child name] is held by this system."

**Edge Cases & Error States:**
- [ ] EC-01: If the center has a legal obligation to retain records (e.g., under RPWD Act 2016 documentation requirements), Rahul is shown a warning: "Certain records may need to be retained under RPWD Act 2016. Consult your legal advisor before proceeding with full erasure." The system does not automatically block erasure — legal review is the center's responsibility.
- [ ] EC-02: If the erasure request is not processed within 30 days, the system sends Rahul an escalating reminder: day 15 (in-app), day 25 (in-app + email), day 30 (in-app + email + flagged in admin dashboard)

**Non-Functional Requirements:**
- Privacy: ⚠️ DPDPA — right to erasure is mandatory under Section 12(c). The platform must not block, unduly delay, or require justification beyond the confirmation step. 30-day processing window is the DPDPA-compliant target.
- Irreversibility: Erasure is permanent. A confirmation dialog with typed confirmation ("Type DELETE to confirm") is required before the request is submitted.

**Dependencies:**
- Blocked by: DPDPA-001, DPDPA-002 (consent withdrawal is typically the precursor), RBAC-001
- Enables: EXPORT-003 (bulk export must exclude children with erasure-in-progress)

**Definition of Done:**
- [ ] All AC pass in QA
- [ ] Post-erasure: confirmed that no child health data remains in active database tables
- [ ] Audit log retention confirmed (anonymized entry only — no clinical data retained)
- [ ] 30-day escalation reminders tested
- [ ] Code reviewed and merged

---

### Story DPDPA-005: Consent audit log — director view and export

**As a** Rahul (center director / data fiduciary)
**I want to** view and export a complete consent audit log for any child
**So that** I can produce evidence of DPDPA-compliant consent management if the center receives a regulator inspection or a formal data subject complaint

**Inspired by:** SimplePractice (consent records), DPDPA 2023 accountability principle

**Context:** A parent lodges a formal complaint with India's Data Protection Board (DPB) claiming consent was never given for her child's data to be processed. Rahul needs to produce the consent record within the DPB's specified timeframe.

**Acceptance Criteria:**
- [ ] AC-01: Given Rahul is viewing any child's record, when he taps "Consent history," then he sees a timeline of all consent events for that child: initial consent (date, time, admin who recorded it, notice version), any updates, any withdrawals, any re-consents
- [ ] AC-02: Given Rahul views the consent timeline, when he taps "Export consent log," then a PDF is generated containing all consent events for that child with timestamps, actor names, and notice version numbers
- [ ] AC-03: Given Rahul exports the consent log, when it is generated, then an audit trail entry is created for the export: actor, timestamp, child record, "Consent log exported"
- [ ] AC-04: Given Rahul wants the consent log for all children (e.g., for a center-wide audit), when he navigates to Settings > Compliance, then he can export a center-wide consent status report: for each child — consent status (Active / Withdrawn / Pending), date of last consent event

**Edge Cases & Error States:**
- [ ] EC-01: If a child's consent was captured before this feature shipped (retroactive gap), their consent log shows "Pre-digital consent — paper record" with a flag for admin to upload a scanned copy

**Non-Functional Requirements:**
- Privacy: ⚠️ DPDPA — consent audit log is itself a record of personal data processing; access restricted to Director role only
- Immutability: Consent log entries cannot be edited or deleted — confirmed at database level

**Dependencies:**
- Blocked by: DPDPA-001, DPDPA-002, AUDIT-001
- Enables: Regulatory compliance responses

**Definition of Done:**
- [ ] All AC pass in QA
- [ ] Consent log immutability confirmed (no update endpoint in API)
- [ ] Center-wide export tested with mixed consent states
- [ ] Code reviewed and merged

---

## Backlog: Epic 4 — DPDPA Compliance

| Story ID | Title | Persona | Complexity | Priority | Blocked by |
|---|---|---|---|---|---|
| DPDPA-001 | Capture verifiable parental consent at intake | Rahul, Meena | L | **P0 — gates entire product** | RBAC-001 |
| DPDPA-002 | Consent withdrawal and data processing suspension | Meena, Rahul | L | P0 | DPDPA-001, RBAC-001 |
| DPDPA-003 | Privacy notice — plain-language, parent portal | Meena | M | P0 | DPDPA-001 |
| DPDPA-004 | Right to erasure — parent-initiated deletion | Meena, Rahul | L | P1 | DPDPA-001, DPDPA-002, RBAC-001 |
| DPDPA-005 | Consent audit log — director view and export | Rahul | M | P1 | DPDPA-001, DPDPA-002, AUDIT-001 |

---
---

## Epic 5: Two-Factor Authentication (2FA)

**Goal:** All staff logins to the platform require a second factor (SMS OTP or authenticator app) when accessing child health records. Sessions time out after inactivity. No child health data is accessible via a stolen or shared credential alone.
**Copied from:** SimplePractice (2FA), Jane App (2FA for practitioners), CentralReach (session security)
**Target user(s):** All staff roles (Priya, Dr. Sunita, Rahul, Admin/Billing); Meena (parent portal with lighter 2FA)
**Definition of Done:**
- [ ] 2FA is enforced for all staff logins from a new device or after a configurable inactivity timeout
- [ ] SMS OTP delivery confirmed working on Indian mobile networks (Airtel, Jio, Vi) in QA
- [ ] Session timeout triggers re-authentication (not full logout) after configurable inactivity period
- [ ] Authenticator app (TOTP — Google Authenticator, Microsoft Authenticator) supported as an alternative to SMS
- [ ] All AC in stories AUTH-001 through AUTH-004 pass QA

**Out of scope (this epic):**
- Biometric authentication (fingerprint/face unlock — Phase 2)
- Hardware security keys (enterprise Phase 2)
- Single Sign-On (SSO) with Google / Microsoft (Phase 2)
- 2FA for parent portal (lighter requirement — Phase 1 uses strong password + session management)

**[ASSUMPTION — NOT VALIDATED]** This epic assumes staff will tolerate 2FA friction on a tool they use multiple times daily. For Priya accessing the app during a live therapy session, repeated OTP prompts could be a significant adoption barrier. The configurable session timeout is the mitigation — but the right timeout duration has not been validated with users.

---

### Story AUTH-001: Enable 2FA on first login from a new device

**As a** Priya / Dr. Sunita / Rahul (any staff user)
**I want to** be required to verify my identity with an OTP when I log in from a new device
**So that** a stolen or guessed password alone cannot give an attacker access to child health records

**Inspired by:** SimplePractice 2FA, Jane App two-step verification

**Context:** Priya has just downloaded the app on a new phone. She enters her username and password. The system prompts for OTP before granting access.

**Acceptance Criteria:**
- [ ] AC-01: Given a staff user logs in with correct credentials from a device not previously verified, when credentials are accepted, then the system prompts for a 6-digit OTP before granting access to any child record
- [ ] AC-02: Given the OTP prompt is shown, when the user selects "Send OTP via SMS," then an OTP is sent to the phone number registered against their account within 30 seconds on Indian networks (Jio, Airtel, Vi)
- [ ] AC-03: Given the OTP is sent, when the user enters the correct 6-digit code, then access is granted, the device is marked as trusted, and no further OTP is required from this device until the session times out or the device trust is manually revoked
- [ ] AC-04: Given the OTP is entered incorrectly 3 times, when the third failure occurs, then the login is blocked for 15 minutes and the staff user's account admin (Rahul) receives an in-app notification: "Failed login attempts detected for [staff name]"
- [ ] AC-05: Given a staff user has set up an authenticator app (TOTP), when they are prompted for OTP, then they can choose "Use authenticator app" as an alternative to SMS OTP

**Edge Cases & Error States:**
- [ ] EC-01: If the SMS OTP does not arrive within 60 seconds, a "Resend OTP" button becomes active
- [ ] EC-02: If the user's registered phone number has changed and they cannot receive the SMS OTP, an "I can't receive this OTP" link is shown that triggers an admin-mediated recovery flow (Rahul manually resets the user's device trust)
- [ ] EC-03: OTP codes expire after 10 minutes — expired OTPs show an error: "This code has expired. Request a new one."

**Non-Functional Requirements:**
- Performance: OTP delivery within 30 seconds on Indian mobile networks
- Offline: 2FA cannot be bypassed offline; if no connectivity exists, login is not possible (child health data is not accessible without verified identity)
- Security: OTPs are single-use; rate-limited to 5 requests per 15 minutes per account; not logged in plaintext

**Dependencies:**
- Blocked by: User account and role management (RBAC-001 must exist first — users must exist before 2FA can be enforced)
- Enables: AUTH-002 (session timeout), AUTH-003 (TOTP setup)

**Definition of Done:**
- [ ] All AC pass in QA
- [ ] OTP delivery tested on Jio, Airtel, and Vi SIM cards
- [ ] 3-failed-attempt lockout confirmed
- [ ] Device trust persisted correctly across app restarts
- [ ] Code reviewed and merged

---

### Story AUTH-002: Session timeout and re-authentication after inactivity

**As a** Rahul (center director, security owner)
**I want to** configure an inactivity timeout after which staff sessions expire and require re-authentication
**So that** an unlocked phone left unattended cannot expose child health records

**Inspired by:** CentralReach session management, SimplePractice auto-logout

**Context:** A therapist leaves her phone on a table at the center. Another staff member picks it up. Session timeout prevents unauthorized access.

**Acceptance Criteria:**
- [ ] AC-01: Given a staff user has been inactive on the app for the configured timeout period, when the timeout is reached, then the app shows a locked screen: "Session expired. Re-enter your PIN or OTP to continue." — the locked screen does not reveal any child record data
- [ ] AC-02: Given Rahul has Director role, when he opens Security Settings, then he can set the inactivity timeout (options: 5 min, 15 min, 30 min, 1 hour; default: 15 min)
- [ ] AC-03: Given the session lock screen is shown, when the user enters their PIN (4–6 digit PIN set at onboarding — distinct from their login password) correctly, then access is restored without requiring a full OTP re-authentication
- [ ] AC-04: Given the user enters the PIN incorrectly 5 times, when the fifth failure occurs, then the session is fully terminated and the user must log in again from the login screen (full 2FA required)

**Edge Cases & Error States:**
- [ ] EC-01: If the user is in the middle of filling in a session note when the timeout triggers, the in-progress note is saved as a draft before the lock screen appears — the draft is recoverable after re-authentication
- [ ] EC-02: If the app is backgrounded (minimized), the timeout clock continues running — app backgrounding does not reset the timer

**Non-Functional Requirements:**
- Security: Lock screen must not expose any personal data (no child names, no record previews visible on lock screen)
- Performance: Lock screen renders within 1 second of timeout detection

**Dependencies:**
- Blocked by: AUTH-001 (2FA infrastructure must exist for re-auth flow)
- Enables: AUTH-004 (admin can view active sessions)

**Definition of Done:**
- [ ] All AC pass in QA
- [ ] Draft save-on-timeout confirmed
- [ ] App-backgrounded timeout tested (not reset by backgrounding)
- [ ] Lock screen confirmed to show no child data
- [ ] Code reviewed and merged

---

### Story AUTH-003: Set up authenticator app (TOTP) as 2FA method

**As a** Dr. Sunita or Rahul (security-conscious staff user)
**I want to** register an authenticator app (Google Authenticator, Microsoft Authenticator) as my 2FA method instead of SMS OTP
**So that** I can log in securely even when my mobile data is unreliable, without depending on SMS delivery

**Inspired by:** SimplePractice authenticator app support, Jane App TOTP

**Context:** Dr. Sunita travels to a rural area for a home visit where SMS delivery is unreliable. She has set up Google Authenticator as her 2FA method.

**Acceptance Criteria:**
- [ ] AC-01: Given Dr. Sunita navigates to Profile > Security, when she taps "Set up authenticator app," then she is shown a QR code to scan with Google Authenticator or Microsoft Authenticator
- [ ] AC-02: Given she scans the QR code and enters the first 6-digit TOTP to confirm setup, when the code is verified, then authenticator app is enabled and a set of 8 one-time backup codes is generated and shown once — she is prompted to save them
- [ ] AC-03: Given authenticator app is set up, when Dr. Sunita next logs in from a new device, then the 2FA prompt shows both options: "Send SMS OTP" and "Use authenticator app"
- [ ] AC-04: Given she selects authenticator app, when she enters the 6-digit TOTP, then if the code is valid (within 30-second TOTP window), access is granted

**Edge Cases & Error States:**
- [ ] EC-01: If Dr. Sunita loses her phone and cannot access her authenticator app, she can enter a backup code from her saved set — each backup code is single-use
- [ ] EC-02: If all backup codes are used, an admin (Rahul) can reset her 2FA method from the Admin > Staff panel

**Non-Functional Requirements:**
- Security: TOTP uses TOTP-HOTP standard (RFC 6238); codes are not sent over the network — validated server-side; backup codes are hashed at storage

**Dependencies:**
- Blocked by: AUTH-001 (2FA infrastructure)
- Enables: None (enhances AUTH-001)

**Definition of Done:**
- [ ] All AC pass in QA
- [ ] TOTP verified against RFC 6238 standard
- [ ] Backup code single-use behavior confirmed
- [ ] Admin reset flow for lost authenticator tested
- [ ] Code reviewed and merged

---

### Story AUTH-004: Admin view of active staff sessions and device management

**As a** Rahul (center director)
**I want to** see which devices are currently logged into the platform with each staff member's credentials, and revoke device trust remotely
**So that** I can respond to a security incident (lost phone, departed staff member) by immediately terminating their access

**Inspired by:** SimplePractice device management, Jane App session management

**Context:** A therapist leaves the center on short notice. Rahul needs to revoke her platform access immediately.

**Acceptance Criteria:**
- [ ] AC-01: Given Rahul navigates to Admin > Staff > [Staff member], when he views their profile, then he sees a "Trusted devices" list showing: device name (model if available), last active date, and city/region of last login
- [ ] AC-02: Given Rahul sees a suspicious or outdated device, when he taps "Revoke," then that device's session is terminated immediately — the next time the app is opened on that device, a full login + 2FA is required
- [ ] AC-03: Given a staff member's account is deactivated (e.g., they have left the center), when the deactivation is confirmed, then all active sessions for that account are terminated immediately across all devices

**Edge Cases & Error States:**
- [ ] EC-01: If Rahul revokes his own device by mistake, the in-app confirmation warns: "You are about to revoke your current device. You will be logged out immediately."

**Non-Functional Requirements:**
- Security: Session revocation must take effect within 5 seconds — not lazily on next request
- Privacy: ⚠️ DPDPA — device/IP data used for session management is personal data under DPDPA; retained only for the active session period; not used for tracking

**Dependencies:**
- Blocked by: AUTH-001, RBAC-001
- Enables: None (security maintenance feature)

**Definition of Done:**
- [ ] All AC pass in QA
- [ ] Revocation confirmed to take effect within 5 seconds in integration test
- [ ] Account deactivation terminates all sessions confirmed
- [ ] Code reviewed and merged

---

## Backlog: Epic 5 — Two-Factor Authentication

| Story ID | Title | Persona | Complexity | Priority | Blocked by |
|---|---|---|---|---|---|
| AUTH-001 | Enable 2FA on first login from new device | All staff | L | P0 | RBAC-001 |
| AUTH-002 | Session timeout and re-authentication after inactivity | Rahul (config), all staff | M | P0 | AUTH-001 |
| AUTH-003 | Set up authenticator app (TOTP) as 2FA method | Dr. Sunita, Rahul | M | P1 | AUTH-001 |
| AUTH-004 | Admin view of active sessions and device management | Rahul | M | P1 | AUTH-001, RBAC-001 |

---
---

## Epic 6: Role-Based Access Control (RBAC)

**Goal:** The platform enforces strict data access boundaries by role. No therapist can see another therapist's children. No parent can see another child's data. No billing staff can read clinical records. Every data access decision is mediated by the RBAC engine — which itself is the gate that every other story in this product depends on.
**Copied from:** CentralReach (role permissions), SimplePractice (clinician/admin roles), Jane App (multi-role), Theralytics
**Target user(s):** All users — enforced system-wide
**Definition of Done:**
- [ ] Five roles implemented: Center Director, Clinical Supervisor, Therapist, Admin/Billing, Parent
- [ ] RBAC rules enforced at the API layer — not just UI layer (a user who bypasses the UI cannot access unauthorized records via direct API call)
- [ ] Role assignment is Center Director-only action
- [ ] RBAC boundary tests pass for each role: confirmed cannot access out-of-scope records
- [ ] All AC in stories RBAC-001 through RBAC-005 pass QA

**Out of scope (this epic):**
- Custom role creation (Phase 2 — e.g., a "shadow teacher" role)
- Per-child permission overrides within a role (Phase 2)
- Temporary elevated access grants (Phase 2)
- Multi-center role management (Phase 2)

**[ASSUMPTION — NOT VALIDATED]** This epic assumes Indian therapy centers have clean enough role boundaries to map to these five roles without significant overlap. In small centers (5–8 staff), role overlap is common — a therapist who also does admin, a supervisor who also delivers sessions. The role taxonomy has not been validated with real center directors.

---

### Story RBAC-001: Define and assign user roles (Director only)

**As a** Rahul (center director)
**I want to** assign each staff member a role when I create their account
**So that** the system automatically enforces the right data access boundaries without me having to manually configure permissions for each user

**Inspired by:** SimplePractice role management, Jane App user roles

**Context:** Rahul is onboarding the platform. He creates accounts for Priya (Therapist), Dr. Sunita (Supervisor), and a billing admin. He assigns each their role.

**Acceptance Criteria:**
- [ ] AC-01: Given Rahul is in Admin > Staff > Add Staff, when he creates a new staff account, then he is required to select exactly one role from: Center Director, Clinical Supervisor, Therapist, Admin/Billing — the role field is mandatory and has no default
- [ ] AC-02: Given a staff account has been created, when Rahul views the staff member's profile, then he can change their role — and the change takes effect on their next login
- [ ] AC-03: Given a staff member's role is changed, when the change is saved, then an audit log entry is created: actor (Rahul), staff member, old role, new role, timestamp
- [ ] AC-04: Given any user other than a Center Director role views Admin > Staff, when they attempt to access staff management, then they receive an "Access denied" message — role assignment is Director-only

**Edge Cases & Error States:**
- [ ] EC-01: If Rahul attempts to downgrade his own Director role, the system blocks it: "You cannot change your own role. Ask another Director to do this."
- [ ] EC-02: If no Director account exists (e.g., first-time setup), the first account created is automatically assigned Director role during platform onboarding

**Non-Functional Requirements:**
- Security: Role changes must take effect within one login cycle — no grace period where an old role persists
- Privacy: ⚠️ DPDPA — role assignment controls who can access child health data; this is a high-consequence action; audit trail is mandatory

**Dependencies:**
- Blocked by: None (this is the root dependency for the entire RBAC system and for AUTH-001)
- Enables: Every story in this product that enforces a role-based data access check. RBAC-001 is the most critical story in this cluster.

**Definition of Done:**
- [ ] All AC pass in QA
- [ ] Role change takes effect on next login confirmed
- [ ] Director self-downgrade blocked confirmed
- [ ] Audit log entry for role change confirmed
- [ ] Code reviewed and merged

---

### Story RBAC-002: Therapist sees only assigned children

**As a** Priya (therapist)
**I want to** see only the children assigned to my caseload when I open the app
**So that** I cannot accidentally view, modify, or export another therapist's child's health records

**Inspired by:** CentralReach therapist-scoped views, Motivity therapist assignment

**Context:** Priya has 4 assigned children. Ananya is assigned to a different therapist. Priya should never see Ananya's records.

**Acceptance Criteria:**
- [ ] AC-01: Given Priya is logged in with Therapist role, when she opens the Children list, then she sees only children assigned to her — not all children at the center
- [ ] AC-02: Given Priya is viewing her child list, when she attempts to navigate directly to a URL or child ID belonging to a child not assigned to her, then she receives a 403 response: "You don't have permission to view this record"
- [ ] AC-03: Given Priya uses the search function, when she searches for a child name belonging to another therapist, then no result is returned — other children are not discoverable
- [ ] AC-04: Given a child is reassigned from Priya to another therapist, when the reassignment is saved, then Priya loses access to that child's records immediately (within the same session)

**Edge Cases & Error States:**
- [ ] EC-01: If Priya is temporarily asked to cover a session for another therapist's child (substitution), the Director or Supervisor can grant her temporary access to that specific child for a defined date range — implemented as a special assignment, not a role elevation

**Non-Functional Requirements:**
- Security: Access control enforced at API layer — UI filter alone is not sufficient; API must return 403 for unauthorized child IDs regardless of how the request is formed

**Dependencies:**
- Blocked by: RBAC-001
- Enables: DPDPA-001 (consent check is RBAC-gated), every clinical story in Cluster 1

**Definition of Done:**
- [ ] All AC pass in QA
- [ ] API-layer 403 confirmed via direct API call test (not just UI test)
- [ ] Search non-discoverability confirmed
- [ ] Immediate access revocation on reassignment confirmed
- [ ] Code reviewed and merged

---

### Story RBAC-003: Supervisor sees assigned caseload and their therapists' data

**As a** Dr. Sunita (clinical supervisor)
**I want to** see all children assigned to my supervision caseload — including children assigned to therapists I supervise — and be able to view but not modify session records created by those therapists
**So that** I can fulfill my clinical supervision role without needing Director-level access to the entire center's records

**Inspired by:** CentralReach supervisor permissions, Theralytics supervision access model

**Context:** Dr. Sunita supervises Priya and one other therapist. She should see all their assigned children's records for review. She should not see records for therapists she does not supervise.

**Acceptance Criteria:**
- [ ] AC-01: Given Dr. Sunita is logged in with Supervisor role, when she opens the Children list, then she sees all children assigned to therapists under her supervision — plus any children directly assigned to her
- [ ] AC-02: Given Dr. Sunita views a session note created by Priya, when she opens the note, then she can read it and add a supervision comment — she cannot edit or delete Priya's session note directly
- [ ] AC-03: Given Dr. Sunita navigates to the Staff section, when she views it, then she sees only the therapists she supervises — not all center staff, not billing or admin staff

**Edge Cases & Error States:**
- [ ] EC-01: If a therapist is not assigned to any supervisor, that therapist's children are visible only to the Director — not to any supervisor

**Non-Functional Requirements:**
- Security: API layer enforces supervisor scope — a supervisor cannot query records outside their assigned supervision chain

**Dependencies:**
- Blocked by: RBAC-001
- Enables: PROG-001 (supervisor dashboard), Cluster 1 supervision workflows

**Definition of Done:**
- [ ] All AC pass in QA
- [ ] API scope confirmed: supervisor cannot access unassigned therapists' records
- [ ] Supervision comment (not edit) confirmed
- [ ] Code reviewed and merged

---

### Story RBAC-004: Admin/Billing role sees financial data only — no clinical records

**As a** Rahul (center director)
**I want to** be able to create an Admin/Billing role account for a staff member who handles invoicing
**So that** the billing admin can manage invoices and payments without ever being able to read therapy session notes or clinical program data

**Inspired by:** Jane App admin/billing role separation, SimplePractice front-desk role

**Context:** Rahul has a part-time admin who sends invoices and records payments. She should not be able to see session notes or therapy programs.

**Acceptance Criteria:**
- [ ] AC-01: Given a staff member has Admin/Billing role, when they log in, then their navigation shows only: Billing, Invoices, Payments, and basic Child list (name, contact, attendance count only — no clinical data)
- [ ] AC-02: Given the billing admin views the Child list, when she taps a child's name, then she sees only: name, contact details, upcoming session schedule, outstanding balance — no session notes, no therapy programs, no clinical assessments
- [ ] AC-03: Given the billing admin attempts to navigate directly to a clinical record URL, when the request is made, then she receives a 403: "You don't have access to clinical records"

**Edge Cases & Error States:**
- [ ] EC-01: If Rahul himself is the sole person managing billing (no separate billing staff), he uses his Director role — which already includes financial access — without needing a second account

**Non-Functional Requirements:**
- Security: Clinical data separation enforced at API layer — billing role API token must not be able to access clinical endpoints

**Dependencies:**
- Blocked by: RBAC-001
- Enables: ANALYTICS-001 (billing admin can also view revenue dashboard)

**Definition of Done:**
- [ ] All AC pass in QA
- [ ] API-layer 403 for clinical endpoints confirmed with billing role token
- [ ] Billing admin navigation confirmed to exclude all clinical sections
- [ ] Code reviewed and merged

---

### Story RBAC-005: Parent portal — read-only access to own child only

**As a** Meena (parent)
**I want to** log into the parent portal and see only my child's records — nothing about other children at the center
**So that** I can review Arjun's progress reports and session attendance without any risk of accidentally seeing another family's private data

**Inspired by:** Hi Rasmus parent portal, SimplePractice client portal

**Context:** Meena has been given login credentials to the parent portal. She should see Arjun's records only. She should not be able to create, edit, or delete any records.

**Acceptance Criteria:**
- [ ] AC-01: Given Meena logs in with Parent role, when she views the portal, then she sees only records associated with her linked child — no other children's records are discoverable
- [ ] AC-02: Given Meena views Arjun's session records, when she opens any record, then all fields are read-only — no edit, delete, or create action is available to her
- [ ] AC-03: Given Meena navigates to any section, when she views it, then staff information (other therapists' names, their caseloads, billing for other families) is not visible
- [ ] AC-04: Given Meena attempts to access any URL outside her child's record scope, when the request is made, then she receives a 403: "You don't have permission to view this."

**Edge Cases & Error States:**
- [ ] EC-01: If a family has multiple children at the center, Meena's parent portal shows all her children (linked to her account) — but not children from other families

**Non-Functional Requirements:**
- Security: Parent role token cannot access any clinical or financial endpoint other than the linked child's read-only records
- Privacy: ⚠️ DPDPA — parent portal access is a data principal right; the platform must not show a parent data about other children under any circumstances

**Dependencies:**
- Blocked by: RBAC-001
- Enables: DPDPA-002 (parent consent withdrawal), DPDPA-004 (right to erasure), EXPORT-004 (data portability)

**Definition of Done:**
- [ ] All AC pass in QA
- [ ] Multi-child family tested (Meena sees both her children but not others')
- [ ] API-layer 403 for any non-linked child confirmed
- [ ] Read-only enforcement confirmed (no create/update/delete for parent role)
- [ ] Code reviewed and merged

---

## Backlog: Epic 6 — Role-Based Access Control

| Story ID | Title | Persona | Complexity | Priority | Blocked by |
|---|---|---|---|---|---|
| RBAC-001 | Define and assign user roles (Director only) | Rahul | M | **P0 — gates entire product** | None |
| RBAC-002 | Therapist sees only assigned children | Priya | M | P0 | RBAC-001 |
| RBAC-003 | Supervisor sees assigned caseload and supervised therapists | Dr. Sunita | M | P0 | RBAC-001 |
| RBAC-004 | Admin/Billing role sees financial data only | Rahul (config), Admin | M | P0 | RBAC-001 |
| RBAC-005 | Parent portal — read-only access to own child only | Meena | M | P0 | RBAC-001 |

---
---

## Epic 7: Audit Trails

**Goal:** Every access, creation, modification, and deletion event across the platform is logged in an immutable audit trail. The log is queryable, filterable, and exportable. It satisfies DPDPA 2023 accountability requirements for sensitive personal data processors and supports RCI/RPWD Act documentation standards.
**Copied from:** SimplePractice (activity log), Jane App (audit log), CentralReach (activity history)
**Target user(s):** Rahul (compliance owner), platform integrity (system-level)
**Definition of Done:**
- [ ] All data write, update, delete, and sensitive read events are logged with: actor ID, role, action type, record type, record ID, timestamp, device/IP
- [ ] Audit log entries cannot be modified or deleted by any user — confirmed at database level (append-only table or equivalent)
- [ ] Rahul can query the audit log by child record, staff member, date range, and event type
- [ ] Audit log is exportable as CSV
- [ ] Log retention: minimum 5 years (configurable by Director — default 5 years per RPWD Act documentation expectations)
- [ ] All AC in stories AUDIT-001 through AUDIT-003 pass QA

**Out of scope (this epic):**
- Real-time security alerting (anomaly detection — Phase 2)
- Automated compliance reporting to regulators (Phase 2)
- Log streaming to external SIEM tools (Phase 2)

**[ASSUMPTION — NOT VALIDATED]** This epic assumes DPDPA 2023 creates a real, felt compliance requirement for Indian therapy centers. The accountability principle under DPDPA 2023 requires data fiduciaries to demonstrate compliance — but enforcement maturity (whether regulators actually inspect small therapy centers) has not been confirmed by primary research.

---

### Story AUDIT-001: Log all data write and delete events

**As a** the platform (system-level story)
**I need to** automatically create an immutable audit log entry every time any user creates, updates, or deletes any record
**So that** there is always a complete, tamper-proof history of every change made to every piece of data in the system

**Inspired by:** SimplePractice activity log, CentralReach activity history, DPDPA 2023 accountability principle

**Context:** This is a system-level story — no user-facing UI. Every other story in the product depends on this working correctly.

**Acceptance Criteria:**
- [ ] AC-01: Given any staff user creates a new record (child record, session note, invoice, consent form, therapy program, user account), when the record is saved, then an audit log entry is created containing: actor user ID, actor role, action = "CREATE", record type, record ID, timestamp (UTC), device identifier
- [ ] AC-02: Given any staff user updates an existing record, when the update is saved, then an audit log entry is created with: actor, action = "UPDATE", record type, record ID, fields changed (field names only — not the values, to avoid logging clinical data content in the audit table), timestamp
- [ ] AC-03: Given any staff user or system process deletes a record, when the deletion is confirmed, then an audit log entry is created with: actor, action = "DELETE", record type, record ID, timestamp — the deleted record's ID is retained in the log even after the record itself is gone
- [ ] AC-04: Given an audit log entry is created, when any user (including Director) attempts to update or delete that audit log entry, then the operation returns a 403 error: "Audit log entries cannot be modified"
- [ ] AC-05: Given a DPDPA high-risk data access event occurs (bulk export, consent withdrawal, erasure request, RBAC role change), when the event occurs, then the audit log entry is additionally tagged with a "DPDPA high-risk" flag for easy filtering

**Edge Cases & Error States:**
- [ ] EC-01: If the audit log write fails (e.g., database unavailability), the originating data write is rolled back — data is not saved if the audit log cannot be written (the log is not optional)
- [ ] EC-02: Offline data writes (locally queued) are logged when they sync to the server — the audit log entry uses the server-confirmed timestamp, not the local write timestamp; both timestamps are stored

**Non-Functional Requirements:**
- Performance: Audit log write must not add more than 50ms latency to any data write operation
- Storage: Audit log is stored in a separate, append-only database table or equivalent immutable store — physically separate from operational data
- Retention: Minimum 5 years retention; configurable to 7+ years if required by center
- Privacy: ⚠️ DPDPA — the audit log itself contains personal data (staff identity, record IDs); access to the audit log is restricted to Director role only

**Dependencies:**
- Blocked by: RBAC-001 (actor role must be resolvable for every log entry)
- Enables: Every other story that creates an audit entry (EXPORT-001, EXPORT-002, EXPORT-003, DPDPA-002, DPDPA-004, DPDPA-005, ANALYTICS-004, RBAC-001)

**Definition of Done:**
- [ ] All AC pass in QA
- [ ] Audit log immutability confirmed at database level (no UPDATE or DELETE endpoint exists for audit table)
- [ ] Rollback-on-audit-failure confirmed in integration test
- [ ] Offline sync timestamp handling confirmed
- [ ] Code reviewed and merged

---

### Story AUDIT-002: Rahul can query and export the audit log

**As a** Rahul (center director)
**I want to** search the audit log by child, staff member, date range, and event type — and export the results as CSV
**So that** I can produce a complete activity history for any record in response to a DPDPA inspection, RCI documentation request, or internal security concern

**Inspired by:** SimplePractice audit log view, Jane App activity log

**Context:** A parent has formally complained that a staff member accessed their child's records without authorization. Rahul needs to produce a complete access log for that child within 48 hours.

**Acceptance Criteria:**
- [ ] AC-01: Given Rahul navigates to Admin > Audit Log, when the view loads, then he sees a filterable log list with columns: Timestamp, Actor name, Actor role, Action type, Record type, Record ID / name
- [ ] AC-02: Given Rahul applies a filter (child name, staff name, date range, or action type), when the filter is applied, then the log list updates to show only matching entries — no page reload required
- [ ] AC-03: Given Rahul wants to export the filtered results, when he taps "Export CSV," then a CSV file is generated containing all filtered audit entries with all columns — including the "DPDPA high-risk" flag column
- [ ] AC-04: Given the audit log export is initiated, when it completes, then an audit log entry is created for the export itself: actor, action = "AUDIT LOG EXPORT", filter parameters, timestamp

**Edge Cases & Error States:**
- [ ] EC-01: If the date range filter spans more than 12 months, a warning is shown: "Large date range — export may take up to 30 seconds" — the export proceeds
- [ ] EC-02: If no entries match the filter, the view shows: "No audit events found for this filter" — not a blank table

**Non-Functional Requirements:**
- Performance: Filtered audit log query for up to 10,000 entries returns in ≤ 3 seconds
- Privacy: ⚠️ DPDPA — audit log access restricted to Director role; accessing the audit log itself is logged (the meta-log entry is created by AUDIT-001)
- Accessibility: Filter controls ≥ 44px touch targets on mobile; table is scrollable on Android

**Dependencies:**
- Blocked by: AUDIT-001, RBAC-001
- Enables: DPDPA-005 (consent audit log is a filtered view of this), compliance responses

**Definition of Done:**
- [ ] All AC pass in QA
- [ ] Filter combinations tested (child + date range, staff + action type, DPDPA flag only)
- [ ] Export CSV confirmed importable into Google Sheets
- [ ] Meta-audit entry for log export confirmed
- [ ] Code reviewed and merged

---

### Story AUDIT-003: Sensitive read event logging (who accessed a child's record)

**As a** the platform (system-level story) — auditable by Rahul
**I need to** log every time any user opens a child's clinical record, session note, therapy program, or consent record
**So that** Rahul can answer the question "who has accessed Arjun's records in the last 30 days?" — required for DPDPA accountability

**Inspired by:** CentralReach activity history, DPDPA 2023 accountability principle for sensitive personal data

**Context:** Beyond write events (AUDIT-001), the platform must also log read access to sensitive records — because under DPDPA 2023, unauthorized access to data (even without modification) is a privacy breach.

**Acceptance Criteria:**
- [ ] AC-01: Given any staff user opens a child's clinical record (full record view, session note view, therapy program view, consent record view), when the record is rendered, then an audit log entry is created: actor, action = "READ", record type, record ID, timestamp
- [ ] AC-02: Given Rahul filters the audit log by action type = "READ" for a specific child, when the filter is applied, then he sees a chronological list of every staff member who opened that child's records — with timestamps and their role at time of access
- [ ] AC-03: Given a read event is logged, when Rahul views it, then the entry shows which record was accessed (e.g., "Session note — 2026-03-12") without logging the content of the record itself

**Edge Cases & Error States:**
- [ ] EC-01: High-frequency legitimate read events (e.g., Dr. Sunita opening a child's record 15 times in one session) are logged individually — no deduplication or rate-limiting of read log entries, as every access is independently significant for audit purposes
- [ ] EC-02: Background system reads (e.g., a cron job generating a progress report) are logged with actor = "System", action = "SYSTEM READ", and the trigger context (e.g., "Scheduled report generation")

**Non-Functional Requirements:**
- Performance: Read event logging must not add more than 30ms latency to record load
- Storage: Read events will be high-volume; ensure audit table is indexed on (child_id, timestamp) for query performance
- Privacy: ⚠️ DPDPA — read log access restricted to Director role; the log entries themselves do not contain clinical data content — only record identifiers

**Dependencies:**
- Blocked by: AUDIT-001 (same infrastructure), RBAC-001
- Enables: AUDIT-002 (read events are queryable through the same audit log view)

**Definition of Done:**
- [ ] All AC pass in QA
- [ ] Read logging latency measured and confirmed ≤ 30ms in load test
- [ ] System read actor correctly attributed in logs
- [ ] High-frequency read scenario tested (no deduplication occurring)
- [ ] Code reviewed and merged

---

## Backlog: Epic 7 — Audit Trails

| Story ID | Title | Persona | Complexity | Priority | Blocked by |
|---|---|---|---|---|---|
| AUDIT-001 | Log all data write and delete events | System | L | **P0 — required before any data story ships** | RBAC-001 |
| AUDIT-002 | Rahul can query and export the audit log | Rahul | M | P1 | AUDIT-001, RBAC-001 |
| AUDIT-003 | Sensitive read event logging | System | M | P1 | AUDIT-001, RBAC-001 |

---
---

## Cross-Epic Dependency Table

> DPDPA consent (DPDPA-001) and RBAC role enforcement (RBAC-001) are not merely upstream dependencies — they are compliance gates. If either is missing, no child health data should exist in the system, and no feature in the product can be ethically or legally deployed. Both must ship in Sprint 1.

| Downstream Epic / Story | Blocked by | Why it is a hard gate | What fails if missing |
|---|---|---|---|
| **Every story in Cluster 1–5** | RBAC-001 | Without role enforcement, any user can access any record — no data isolation exists | Complete absence of access control; all child health records exposed to all users |
| **Every story that stores or reads child health data** | DPDPA-001 | DPDPA 2023 Section 9 requires verifiable parental consent before health data of a minor is processed | Processing child health data without consent is a DPDPA violation; legal and regulatory exposure for the center |
| PROG-001, PROG-002, PROG-003, PROG-004 | RBAC-001, DPDPA-001 | Dashboard displays child health data; must be consent-gated and role-gated | Dashboard shows data for children who haven't consented; supervisors see all children regardless of assignment |
| ANALYTICS-001, ANALYTICS-002, ANALYTICS-003 | RBAC-001, Cluster 3 (billing), Cluster 4 (scheduling) | Analytics aggregates data from billing and scheduling; no data to aggregate without upstream clusters | Empty dashboards; misleading metrics if partial data exists |
| EXPORT-001, EXPORT-002, EXPORT-003, EXPORT-004 | AUDIT-001, DPDPA-001, RBAC-001 | Every export must be logged (DPDPA accountability); every export must confirm consent status; every export must be role-authorized | Exports with no audit trail violate DPDPA accountability principle; bulk export could include data for children who withdrew consent |
| DPDPA-002 (consent withdrawal) | DPDPA-001 | Cannot withdraw consent that was never captured | Consent withdrawal flow has nothing to withdraw against |
| DPDPA-004 (right to erasure) | DPDPA-001, DPDPA-002 | Erasure is the end-state of a consent withdrawal; requires consent records to exist to confirm what was covered | Erasure has no consent record to reference; cannot confirm what data was processed under which consent |
| DPDPA-005 (consent audit log) | DPDPA-001, DPDPA-002, AUDIT-001 | Consent log is a filtered view of consent events that must have been written by earlier DPDPA stories | No consent events to display |
| AUTH-001 (2FA) | RBAC-001 | 2FA enforces identity; identity is only meaningful if roles are already defined | 2FA verifies "this is Priya" but if RBAC doesn't exist, being Priya has no access-control consequence |
| AUTH-002, AUTH-003, AUTH-004 | AUTH-001 | Session management, TOTP, and device management all depend on the 2FA infrastructure from AUTH-001 | No session to manage; no device to trust |
| AUDIT-002, AUDIT-003 | AUDIT-001 | The query/export UI and read-event logging are downstream of the core audit infrastructure | No log to query; no read events being captured |
| PROG-005 (PDF export) | AUDIT-001, RBAC-001 | Export must be logged; must be role-authorized | Unlogged exports; therapist could export any child's records |
| ANALYTICS-004 (operations report export) | ANALYTICS-001–003, AUDIT-001 | Report aggregates metrics; export must be logged | No data to aggregate; export unlogged |
| EXPORT-003 (bulk compliance export) | DPDPA-001 consent status per child | Bulk export must exclude children with withdrawn consent | Exporting records of children who withdrew consent is a DPDPA violation |

### Critical path summary

The minimum viable compliance baseline before any data can be stored in production:

```
RBAC-001 → AUTH-001 → AUDIT-001 → DPDPA-001
```

These four stories must ship together in Sprint 1. No child health data should enter production infrastructure before all four are live and confirmed in integration testing.

---

## ⚠️ Feature Factory Disclaimer

These features and stories were defined by competitive observation, document synthesis (journey map, competitive analysis), and category assumption — not by validated user research. Before committing engineering capacity or design effort, a real product thinker should ask:

**What we assumed but haven't validated:**

- [ASSUMPTION] Indian therapy center directors (Rahul) will use a mobile analytics dashboard as a regular workflow tool — not just a report they check once a month. The frequency and nature of metric-checking behavior has not been confirmed in primary research.
- [ASSUMPTION] Clinical supervisors (Dr. Sunita) will use a digital progress dashboard as part of their weekly caseload review workflow. Paper-based review patterns may persist even if a digital tool is available.
- [ASSUMPTION] Center directors are aware of DPDPA 2023 obligations for minor health data and will actively implement consent management workflows. H-06 in the journey map rates this as high-uncertainty, high-risk.
- [ASSUMPTION] Staff will tolerate 2FA friction on a tool used multiple times daily. For Priya during a live session, OTP prompts could kill adoption. The configurable session timeout is the mitigation — but the right timeout duration is untested.
- [ASSUMPTION] Role boundaries in real Indian therapy centers are clean enough to map to the five RBAC roles defined here. Small centers with heavy role overlap (therapist + admin, supervisor + session deliverer) may require a more flexible permission model.
- [ASSUMPTION] Bulk export for compliance audits is a real use case that center directors need. The frequency and formality of RPWD Act / DPDPA audits in small Indian therapy centers has not been confirmed.
- [ASSUMPTION] Audit trails are a meaningful compliance feature for Indian therapy centers today. DPDPA 2023 is real law — but enforcement maturity and whether small therapy centers are being inspected is unconfirmed.
- [ASSUMPTION] Dropout risk flags based on attendance data will prompt Rahul to take action. If the underlying cause of dropout (financial strain, caregiver exhaustion) is not addressable by a flag, the feature surfaces information without enabling intervention.

**What a researcher would ask before building this:**

- How frequently does Rahul currently check any kind of operational metric? What does his existing Excel or WhatsApp-based metric-checking look like — and will a dashboard genuinely displace that behavior or run alongside it?
- Are Indian therapy center directors aware of DPDPA 2023 as a live compliance obligation? Do they know they are data fiduciaries? Has any center received a formal DPDPA inquiry or complaint?
- What is the actual role structure in a typical 5–15 staff Indian therapy center? Is a clean Therapist / Supervisor / Director / Admin separation realistic, or are hybrid roles the norm?

**What the Product Consultant would challenge:**

- RBAC-001, DPDPA-001, AUTH-001, and AUDIT-001 are all P0 stories that must ship before the product can go live — that is four significant engineering efforts as table stakes before any visible product value is delivered. Is the scope right for Phase 1, or should the team ship a simpler access model (single-role MVP) and add granular RBAC in Phase 2?
- The analytics cluster (ANALYTICS-001–004) depends on data from Clusters 1–4 being reliably filled in. If therapists are not consistently logging session data and supervisors are not updating goals, the dashboards will show empty or misleading metrics. Analytics is only valuable if the upstream data collection pipeline is working. Sequencing matters: don't ship analytics before confirming data quality from clinical documentation.

**Risk level per output:**

- **Low risk (table stakes):** 2FA (AUTH-001, AUTH-002), RBAC role enforcement (RBAC-001–005), basic audit trail (AUDIT-001) — these are non-negotiable for any health data SaaS; not having them is a clear gap regardless of user research
- **Medium risk (differentiator or compliance-driven but uncertain):** DPDPA compliance features (DPDPA-001–005), data export (EXPORT-001–004), audit log query (AUDIT-002, AUDIT-003) — DPDPA obligation is real but enforcement urgency and director awareness are unvalidated
- **High risk (valuable if the data pipeline works, speculative if it doesn't):** Progress/outcome tracking (PROG-001–005), center analytics (ANALYTICS-001–004), dropout risk flags (PROG-004) — these features are only useful if upstream data capture (Clusters 1–4) is working reliably and staff have actually adopted the core product

Use the `/research` agent to validate assumptions before sprint planning — particularly H-06 (DPDPA awareness), the RBAC role taxonomy, and director metric-checking frequency.
Use the `/scope` (Product Consultant) agent to challenge whether RBAC + DPDPA + 2FA + Audit Trail must all ship in Sprint 1 or whether a phased compliance approach is viable.
Use the `/design-critique` agent to review the analytics dashboard and DPDPA consent flow screens before prototyping — both involve high-stakes interactions on low-end Android hardware.

---

*File saved:* `/products/autism-therapy-platform/prds-and-stories/mindless-product-owner/cluster-5-analytics-compliance-access.md`
*Date:* 2026-04-17
*Agent:* Mindless Product Owner
*Source documents read:* journey-map.md, competitive-analysis-autism-therapy-software.md, mindless-product-owner.md (agent instructions), product CLAUDE.md
