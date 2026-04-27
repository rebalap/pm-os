# User Journey: Progress Reporting to Parents

> ❌ **OUT OF SCOPE — MVP**
> **Decision date:** 22 April 2026 | **Decision by:** Engineering + Product
> **Rationale:** Therapy-specific reporting requiring net-new build. Depends on structured session data and digital program records — both of which depend on deferred features (Journey 4, in-session data collection). Cannot be built meaningfully without the upstream data chain.
> **Deferred to:** Post-MVP release
> **Adoption risk:** Progress reports are the primary evidence families see of clinical value. Without structured reporting, parent engagement and retention may be harder to sustain at MVP. Monitor in primary research.
> **Reference:** `meetings/engineering/2026-04-22-engineering-alignment-meeting-summary.md`

**Previously:** J4 | ❌ **OUT OF SCOPE — MVP (Deferred post-MVP)**
**Trigger:** Dr. Sunita initiates a monthly or quarterly progress report for a child, OR Rahul flags in the caseload dashboard that a family's report is overdue
**Primary actor:** Dr. Sunita (Clinical Supervisor — writes the report)
**Supporting actors:** Rahul (Center Director — triggers overdue flag or reviews; has read access); Meena (Parent — receives report via WhatsApp message with PDF attachment or link)
**Entry condition:** The child has an active EMR with confirmed DPDPA parental consent (EMR-002). At least one billing period's worth of session notes and SOAP notes exist for this child (accumulated from Journey 6 instances). Dr. Sunita has an RCI-licensed clinician profile with her credential and license number configured (RX-004 / PROFILE-001). Center letterhead is configured (RX-005). WhatsApp Business API is connected and the parent has opted in to WhatsApp messaging (WA-001, WA-003).
**End state:** Progress report created, auto-populated from session data, reviewed and finalized by Dr. Sunita, saved in the child's EMR, exported as a PDF, delivered to Meena via WhatsApp Business API (with PDF attached), Meena's delivery status confirmed (Delivered / Read), and the share event logged in the child's audit trail.
**Journey source documents:**
- `cluster-1-clinical-documentation.md` — SNOTE-003 to SNOTE-005 (session note aggregation into report), SOAP-003 to SOAP-004 (SOAP content referenced in report), EMR-003 to EMR-004 (document storage and clinical timeline), TMPL-004 to TMPL-005 (home program generated alongside report)
- `cluster-2-patient-records-intake.md` — MPM-003 (supervisor caseload dashboard — overdue flag trigger), MPM-005 (director full caseload overview — Rahul trigger)
- `cluster-3-billing-payments.md` — RX-001 to RX-003 (e-prescription / referral document generation — same PDF + share mechanic reused), RX-004 to RX-005 (clinician profile and letterhead)
- `cluster-4-scheduling-communication.md` — WA-005 to WA-006 (WhatsApp Business API delivery mechanism), WA-001 to WA-003 (WABA setup and opt-in gate)

---

## Discovery Context

- **MVP Scope:** ❌ OUT OF SCOPE — Post-MVP

**Pain points & friction:**
- Report writing starts from scratch every reporting cycle — no carry-forward from previous reports or auto-population from session data 🔵 Inferred as structural gap
- Report language is often inaccessible to lay parents 🔶 [HYPOTHESIS] — no Indian data available; consistent with global finding that clinical documents are poorly understood by families
- Reports are sent via WhatsApp — unencrypted channel for sensitive child health data ⚠️ DPDPA 🔵 Inferred from WhatsApp-dominant communication pattern
- Home program instructions given verbally — Meena may not remember what to practice 🔶 [HYPOTHESIS]
- No structured mechanism for parents to ask questions or confirm understanding 🔶 [HYPOTHESIS]

**Emotional states:**
- Dr. Sunita: Report writing is effortful and competes with clinical time — likely experienced as administrative burden 🔶 [HYPOTHESIS] (supported directionally by 2–3 hours/day documentation figure)
- Meena: Wants to understand what progress her child has made. Report language may be too clinical; she may not know what questions to ask. ✅ Product context: "Receives clinical reports they don't understand"
- Rahul: Progress reports are a retention tool — families who see clear progress are more likely to continue. 🔵 Inferred

**Current workarounds:**
- Some supervisors dictate key points to parents verbally rather than relying on written reports 🔶 [HYPOTHESIS]
- WhatsApp voice notes used to explain report contents informally 🔶 [HYPOTHESIS]

**⚠️ DPDPA exposure:**
- Progress reports aggregate child health data across a reporting period and constitute a clinical document for a minor under DPDPA 2023. Parental consent (consent_status = Active) must be confirmed before report creation is permitted. Finalized reports must be encrypted at rest with an immutable audit trail entry stamped with the author's credentials. Sharing a report PDF via WhatsApp constitutes transmission of minor health data via Meta's infrastructure — this requires both confirmed DPDPA parental consent AND explicit parent opt-in for the WhatsApp channel (two separate gates). The delivery log must store only metadata (message ID, timestamps, delivery status), not report content. Any ABDM health record push at the end of this journey requires a separate ABDM consent artifact in addition to DPDPA consent.

---

## Step-by-Step Flow

| Step | Actor | Action | Screen / State | Technical Note |
|---|---|---|---|---|
| 1A | Rahul | Sees "Report overdue" flag on a child row in the full caseload overview and taps "Notify supervisor" | Center Director Caseload Overview (MPM-005) | `MPM-005 AC-02/AC-03`: GET `/center/children?include_flags=true`; overdue flag calculated from last report date vs. configurable cycle threshold (default: 30 days monthly, 90 days quarterly); Rahul taps flag → in-app notification sent to Dr. Sunita |
| 1B | Dr. Sunita | Opens the supervisor caseload dashboard and sees a child flagged with overdue report badge | Supervisor Caseload Dashboard (MPM-003) | `MPM-003 AC-02/AC-03`: GET `/supervisor/caseload`; overdue report flag appears alongside "last program update" and "last session" flags; Dr. Sunita taps child row to open record |
| 2 | Dr. Sunita | Opens the child's clinical timeline to review the reporting period's session notes and SOAP entries | Child Profile → Timeline tab (EMR-004) | `EMR-004 AC-01/AC-04`: GET `/children/{id}/timeline?date_from={period_start}&date_to={period_end}`; filter by "Notes only" and "SOAP only" to review the period's documentation; timeline entries link to full note detail |
| 3 | Dr. Sunita | Reviews the session notes from the reporting period in aggregate | Child Profile → Session Notes tab (SNOTE-005) | `SNOTE-005 AC-01/AC-02`: GET `/children/{id}/notes?date_from={period_start}&date_to={period_end}&sort=date_asc`; views each note: goals addressed, mood, observations, incidents; identifies attendance count, key behavioral trends, and mastery events across the period |
| 4 | Dr. Sunita | Reviews the SOAP notes from the reporting period to extract clinical interpretations and program decisions | Child Profile → Clinical Notes tab (SOAP-002) | `SOAP-002 AC-01/AC-03`: GET `/children/{id}/clinical-notes?type=SOAP&date_from={period_start}`; reads Assessment and Plan sections for each SOAP note in the period; these inform the progress summary narrative |
| 5 | Dr. Sunita | Navigates to "Generate Progress Report" from the child's profile | Child Profile → Progress Report tab | Report generation entry point; DPDPA consent gate rechecked before report creation opens; GET `/children/{id}/consent` — must be Active |
| 6 | System | Auto-populates the progress report draft from aggregated session data | Progress Report editor (auto-populated draft) | Report engine calls GET `/children/{id}/report-data?period_start={date}&period_end={date}` — aggregates: total sessions attended, session attendance rate, goals addressed across all notes in the period (multi-select from notes), key observations (concatenated from session note "Key observations" fields), mastery events (targets marked mastered in program version history), behavioral incident count; maps aggregated data into report sections |
| 7 | Dr. Sunita | Reviews the auto-populated draft and writes the progress narrative sections | Progress Report editor | Each report section is editable: Dr. Sunita fills in or edits — Session Summary (attendance, targets addressed — pre-populated), Progress by Domain (narrative per domain, partially pre-populated from SOAP Assessment sections), Behavior Summary (incident frequency from session notes), Home Program Recommendations (new — see Step 8), Next Period Goals (drawn from SOAP Plan sections), Clinician's observations (free text) |
| 8 | Dr. Sunita | Generates or attaches a Home Program document for Meena alongside the report | Therapy Program tab → Generate Home Program (TMPL-004) | `TMPL-004 AC-01/AC-02/AC-03`: Dr. Sunita selects targets from active therapy program to include in home program; writes parent-friendly instructions per target (free text, 300 char limit); home program stored as a separate document in the child's record, timestamped; will be bundled with or referenced in the progress report PDF |
| 9 | Dr. Sunita | Finalizes the report and taps **Save & Finalize** | Progress Report editor → confirmation | Report status → Final; PATCH `/children/{id}/reports/{report_id}` `{status: "final"}`; report is linked to the reporting period date range; author name, credential, date auto-stamped from PROFILE-001 / RX-004 |
| 10 | System | Generates a PDF of the finalized report with center letterhead | Background PDF generation | Server-side PDF generation using center letterhead (RX-005): center name/logo header, child's first name + record ID (not full name in filename — DPDPA privacy), report period, author name + RCI license number, all sections, home program section or attachment reference, footer: "Generated by [Platform name] — Confidential clinical record"; completes in ≤ 5 seconds; PDF stored encrypted in child's record |
| 11 | Dr. Sunita | Reviews the PDF preview, confirms it looks correct | Progress Report PDF preview screen | PDF preview rendered inline (Android WebView or browser PDF viewer); "Looks good — share with parent" button; "Edit report" button (returns to editor) |
| 12 | Dr. Sunita | Taps **Send to Parent via WhatsApp** | Report share screen (WA / download options) | ⚠️ DPDPA gate: confirms parental consent is Active AND parent has opted in to WhatsApp (WA-003); checks both before proceeding |
| 13 | System | Sends progress report PDF to Meena via WhatsApp Business API | Background WhatsApp Business API dispatch | `WA-005 / WA-006 mechanic reused for report`: POST to WhatsApp Business API using approved "Progress Report" template; message: "Dear [Parent Name], please find [Child Name]'s therapy progress report for [period] from [Center Name]. — Dr. [Sunita's name], [Center Name]"; PDF attached as WhatsApp document; delivery status webhook received |
| 14 | System | Logs delivery status (Sent / Delivered / Read) in child's record | Background status update | WhatsApp delivery receipt webhook → PATCH `/reports/{report_id}/delivery_status`; Delivered confirmed when parent's WhatsApp client returns delivery receipt; Read confirmed when read receipt returned (if recipient has read receipts enabled) |
| 15 | Dr. Sunita / Rahul | Can view the report in the child's Documents tab and verify delivery status | Child Profile → Documents tab (EMR-003/EMR-004) | `EMR-003 AC-04/AC-05`: report PDF listed under Documents with document type "Progress Report", date, author, and WhatsApp delivery status badge (Delivered / Read / Failed); tapping opens the PDF viewer |
| 16 | Meena | Receives the WhatsApp message, taps to open the PDF | Meena's WhatsApp app (outside platform) | No platform screen; Meena's standard WhatsApp interface; PDF opens in device PDF viewer; no login required |
| 17 | Meena | (Optional) Replies to the center's WhatsApp Business number with a question | Meena's WhatsApp app (outside platform) | Inbound message handling is out of scope for v1 (WA epic out of scope note); reply arrives at center's WABA inbox but the platform does not process inbound messages in v1 |

---

## Decision Points

### Decision 1: Report trigger source (Step 1A vs 1B)
**At step:** 1A / 1B (journey entry)
**Question:** Who initiates the report cycle?
- **Path A — Rahul triggers via caseload flag:** Rahul sees overdue badge in MPM-005, taps "Notify supervisor" → Dr. Sunita receives in-app notification → Dr. Sunita opens child record from notification. → Continue at Step 2
- **Path B — Dr. Sunita self-initiates:** Dr. Sunita opens caseload dashboard, sees overdue flag for a child in her supervised caseload (MPM-003), opens child record directly. → Continue at Step 2
- **Path C — Dr. Sunita proactively initiates (no flag):** Dr. Sunita opens a child's profile to initiate a report at cycle end before any flag fires. → Continue at Step 2 (no notification involved; begins at child profile directly)

### Decision 2: Sufficiency of auto-populated data (Step 6)
**At step:** 6
**Question:** Is there enough session note and SOAP data in the period to auto-populate a meaningful draft?
- **Path A — Sufficient data:** Report draft auto-populated with session count, attendance rate, goals addressed, observations, and SOAP-derived clinical narrative. Dr. Sunita supplements and finalizes. → Continue at Step 7
- **Path B — Sparse data (few or no notes):** Report sections partially empty; system shows per-section indication of data completeness: "3 sessions attended — 0 session notes on file. Complete session notes before generating this report." Dr. Sunita can still create the report manually, but must fill all sections herself. → Continue at Step 7 (with empty fields)
- **Path C (Edge case) — No sessions in period:** Report generation is blocked with message: "No sessions recorded for [Child Name] in this period. Check the attendance records before generating a progress report." → Journey blocked until sessions or attendance data exists

### Decision 3: Home program generation (Step 8)
**At step:** 8
**Question:** Does Dr. Sunita include a home program with this report?
- **Path A — Home program generated:** Dr. Sunita taps "Generate Home Program", selects targets, writes parent-friendly instructions, saves. Home program bundled into report PDF or referenced as separate document. → Continue at Step 9
- **Path B — No home program this cycle:** Dr. Sunita skips home program generation; progress report proceeds without home program attachment. → Continue at Step 9
- **Path C (Edge case) — No active therapy program:** "Generate Home Program" button disabled; message: "Create a therapy program first before generating a home program." → Dr. Sunita must create a program (TMPL-001) before home program is possible

### Decision 4: DPDPA and WhatsApp opt-in gate (Step 12)
**At step:** 12
**Question:** Is the parent DPDPA-consented AND opted in to WhatsApp messaging?
- **Path A — Both confirmed:** WhatsApp delivery proceeds normally. → Continue at Step 13
- **Path B — DPDPA consent not confirmed:** Share button disabled; "Parental consent required before sharing clinical records. Complete consent first." → Journey blocked
- **Path C — WhatsApp opt-in not recorded:** "Send via WhatsApp" button greyed out; tooltip: "Parent has not opted in to WhatsApp messaging. Send link another way or record opt-in first." → Dr. Sunita uses "Copy Shareable Link" or "Download PDF" instead. → Alternative path to Step 15 (skip Steps 13–14 for WhatsApp; share via alternative method)
- **Path D (Edge case) — WABA not connected:** All WhatsApp share options hidden; fallback to PDF download only; Rahul sees prompt in admin panel to connect WABA. → Alternative path

### Decision 5: WhatsApp delivery outcome (Step 13–14)
**At step:** 13–14
**Question:** Was the WhatsApp message successfully delivered?
- **Path A — Delivered and Read:** Delivery status: "Read — [timestamp]"; report considered successfully received. → Continue at Step 15 (end state confirmed)
- **Path B — Delivered, not read:** Delivery status: "Delivered — [timestamp]"; message reached device but not yet opened. Journey end state partially met (delivered but not read); no action required.
- **Path C — Failed (API error or parent not on WhatsApp Business):** Delivery status: "Failed"; Dr. Sunita is notified in-app: "WhatsApp delivery failed for [Parent Name]. Use 'Copy Shareable Link' to share manually." → Dr. Sunita shares via secure link (RX-002 mechanic) or downloads PDF for manual sharing
- **Path D (Edge case) — Meta API unavailable at send time:** Message queued for retry (up to 3 retries over 30 minutes); if all retries fail, fallback to SMS with a plain-text notification of the available download link

### Decision 6: ABDM health record push (optional, after Step 15)
**At step:** After Step 15 (optional extension)
**Question:** Does the center have ABDM HIP registration and does the child have a verified ABHA ID with active ABDM consent?
- **Path A — All ABDM conditions met:** "Share to ABHA Locker" button available on finalized report; Dr. Sunita can push FHIR R4-compliant health record to child's ABHA health locker (ABDM-003). → Optional terminal action; audit log entry created
- **Path B — ABDM not set up:** "Share to ABHA Locker" button not shown or greyed out; no impact on core journey. → Journey ends at Step 15

---

## Screen Inventory

| Screen name | Purpose | Primary action | Personas who see it | Source story |
|---|---|---|---|---|
| Center Director Caseload Overview | Rahul's full-center view with overdue report flags | Flag child as report overdue; notify supervisor | Rahul | MPM-005 |
| Supervisor Caseload Dashboard | Dr. Sunita's supervised-caseload view with overdue flags | Open child record for report | Dr. Sunita | MPM-003 |
| Child Profile → Timeline tab | Chronological feed of all clinical events for the child | Review period events before starting report | Dr. Sunita, Rahul | EMR-004 |
| Session Notes History | Chronological list of all session notes for a child, filterable by date range | Review session-level observations across the period | Dr. Sunita | SNOTE-005 |
| SOAP Note History | List of all SOAP notes for a child, filterable by type and date | Review clinical interpretations before writing report | Dr. Sunita | SOAP-002 |
| Progress Report Editor | Auto-populated report editor; Dr. Sunita reviews, edits, and finalizes all sections | Save & Finalize report | Dr. Sunita | (REPORT-001 implied by SNOTE-005, SOAP-002, EMR-004 enabling notes) |
| Home Program Generator | Template-driven form for selecting therapy targets and writing parent-friendly instructions | Save home program | Dr. Sunita | TMPL-004 |
| Progress Report PDF Preview | Full-screen preview of the generated PDF with letterhead | Confirm and share | Dr. Sunita | RX-001 (PDF mechanic reused) |
| Report Share Screen | Options: Send via WhatsApp, Copy shareable link, Download PDF | Send to parent via WhatsApp | Dr. Sunita | RX-002 (share mechanic reused), WA-005/WA-006 |
| Child Documents tab | All documents stored for the child including reports, with delivery status | View and reshare documents | Dr. Sunita, Rahul | EMR-003 |
| WhatsApp (Meena's device) | Meena receives report PDF via WhatsApp Business message | Open PDF | Meena | WA-005/WA-006 (external — not a platform screen) |
| ABDM Push Confirmation (optional) | Confirm push of FHIR-compliant health record to ABHA locker | Share to ABHA locker | Dr. Sunita | ABDM-003 |

---

## Designer Handoff

### Screen: Progress Report Editor

**Purpose:** Dr. Sunita creates and finalizes the child's periodic progress report — starting from an auto-populated draft drawn from session data, editing narrative sections, and adding her clinical interpretation — so the final document reflects the full reporting period without requiring her to start from a blank page.
**Primary action:** Save & Finalize report
**Entry point(s):** Child Profile → Progress Report tab → "New Report" (or "Continue draft" if a draft exists); or deep-link from overdue notification
**Exit point(s):** Save & Finalize → PDF generation → Report Preview screen; Save Draft → remains on editor with draft banner; Cancel → confirmation dialog ("Save draft or discard?")

**Key components:**
- **Report period selector**: date range picker (default: last 30 days for monthly, last 90 days for quarterly); determines which session data is aggregated
- **Auto-populated data banner** (top of editor): "This report was pre-filled from [N] session notes and [M] SOAP notes in this period. Review and edit each section." — explains provenance of pre-populated content to build trust
- **Section 1 — Session Summary** (partially pre-populated): sessions attended / total scheduled, attendance rate %; list of goals addressed across the period (from session note multi-selects); Dr. Sunita can edit
- **Section 2 — Progress by Domain** (partially pre-populated from SOAP Assessment sections): one expandable text area per active therapy domain (Communication, Social, Adaptive, Cognitive, Motor, Behavior); partial pre-fill from SOAP Assessment text; Dr. Sunita adds narrative
- **Section 3 — Behavior Summary** (partially pre-populated): incident frequency count from session notes; behavioral trend (Dr. Sunita writes narrative)
- **Section 4 — Home Program Recommendations**: link/button to open Home Program Generator (TMPL-004); once generated, summary appears here
- **Section 5 — Next Period Goals** (partially pre-populated from SOAP Plan sections): Dr. Sunita edits and confirms targets for next cycle
- **Section 6 — Clinician's Observations**: free text; Dr. Sunita's overall clinical commentary; no pre-population
- **Author stamp** (bottom, non-editable): Dr. Sunita's name, designation, RCI license number, date — from PROFILE-001 / RX-004
- **Section completeness indicators**: each section has a small indicator (checkmark / warning) showing whether it has content; helps Dr. Sunita track what remains to fill
- **Save Draft / Save & Finalize buttons**: both always visible at bottom; Save & Finalize triggers validation (no empty required sections) then PDF generation

**States:**
- **Empty state:** New report — auto-population has run but no session notes exist: each section shows "No data available for this period — fill in manually" in grey placeholder text
- **Loading state:** Auto-population takes ≤ 3 seconds; skeleton rows shown per section while aggregation runs; "Pulling data from [N] session notes..." loading message
- **Error state:** Auto-population failed (server error): "Could not load session data. The report has been opened without pre-filled data. Fill in manually or retry." — report remains functional; Save Draft remains available; finalization blocked until required sections are complete
- **Offline state:** Draft saves locally; final submission requires connectivity; "Saved locally — connect to finalize and generate PDF" banner

**Constraints:**
- Report editor must work on both desktop (Dr. Sunita's laptop for extended writing) and Android (for in-between-sessions review and editing)
- On Android: each section should be collapsible to avoid overwhelming scroll depth; "domain cards" with expand/collapse per domain
- Text areas in each section must scroll independently without interfering with full-page scroll (same Android constraint as SOAP editor)
- Section completeness indicators must not use color alone — icon + text required (accessibility)

---

### Screen: Home Program Generator

**Purpose:** Dr. Sunita creates a parent-facing home practice document alongside the progress report — selecting relevant therapy targets and writing plain-language instructions that Meena can actually follow, without clinical jargon.
**Primary action:** Save home program
**Entry point(s):** Progress Report Editor → Section 4 "Home Program Recommendations" → tap "Generate Home Program"; or directly from Therapy Program tab → "Generate Home Program" button
**Exit point(s):** Save → home program stored in child's record; returns to Progress Report Editor with home program summary populated in Section 4; or back-navigate without saving → "Discard home program?" confirmation

**Key components:**
- **Target picker**: list of all active therapy program targets; each shown as a checkbox row (target name + domain); Dr. Sunita selects which targets to include in home program (not all clinical targets are appropriate for home practice)
- **Per-target instruction field**: for each selected target, a free-text field (300 char limit with live counter) labeled "Parent instruction" with placeholder: e.g., "When Arjun points at something, help him say the word. Repeat 5 times during snack time."
- **Plain-language hint**: small tip above each instruction field: "Write this as you would explain it to a parent, not a therapist. Avoid clinical terms."
- **Select-all / deselect-all controls**: for centers with many targets
- **Preview button**: shows a formatted preview of what Meena will see in the PDF
- **Save button**: saves to child's record; triggers PDF inclusion on next report generation

**States:**
- **Empty state (no active program):** "Create a therapy program first before generating a home program." with link to Therapy Program tab (TMPL-004 EC-01)
- **Loading state:** Target list loads in ≤ 1 second; skeleton rows
- **Error state:** If no targets selected on save: "Select at least one target for the home program" inline validation (TMPL-004 EC-02)
- **Offline state:** Home program draft saves locally; PDF generation and export require connectivity (TMPL-004 NFR)

**Constraints:**
- Character count for instruction fields must be visible at all times — Meena needs concise, scannable instructions
- Touch targets ≥ 44px on checkboxes; enough vertical spacing for one-handed checkbox selection
- Preview must show the parent-facing view, not the clinical fields — helps Dr. Sunita assess whether instructions are genuinely parent-friendly

---

### Screen: Report Share Screen

**Purpose:** Dr. Sunita chooses how to deliver the finalized report PDF to Meena — via WhatsApp (primary), via a secure shareable link, or via download.
**Primary action:** Send to parent via WhatsApp
**Entry point(s):** Report PDF Preview screen → "Looks good — share with parent"
**Exit point(s):** WhatsApp send → dispatch confirmation, then to Child Documents tab; Copy shareable link → clipboard copy with confirmation toast; Download PDF → device downloads folder; ABDM push (if available) → ABDM push confirmation screen

**Key components:**
- **"Send via WhatsApp" button** (primary, most prominent): pre-populated with parent's registered WhatsApp number; shows parent name next to number for confirmation; greyed out with tooltip if parent not opted in to WhatsApp (WA-003)
- **Pre-filled WhatsApp message preview**: shows the exact message Meena will receive: "Dear [Parent Name], please find [Child Name]'s therapy progress report for [period] from [Center Name]. — Dr. [Sunita's name]"; with PDF attachment shown as document preview
- **"Copy Shareable Link" button**: generates a UUID-based secure link (valid 30 days per RX-002 mechanic); link can be pasted into any channel by Dr. Sunita; link access logged in audit trail
- **"Download PDF" button**: downloads to device Downloads folder; system notification confirms path
- **"Share to ABHA Locker" button** (conditional): shown only if ABDM HIP registered and child has verified ABHA ID with active ABDM consent (ABDM-003); greyed with tooltip if conditions not met
- **Delivery status indicator** (post-send): "Sent [timestamp]" → "Delivered [timestamp]" → "Read [timestamp]" updated in real-time from WhatsApp webhook; visible on this screen before navigating away
- **Share history**: "Previously shared: [N] times — last [date]" shown below buttons for re-share awareness

**States:**
- **Pre-send state:** All share options available; parent name and number shown for confirmation; ABDM button conditional
- **Loading state:** WhatsApp dispatch in progress — button shows spinner; completes within 3 seconds normally
- **Success state:** "Sent to [Parent Name] via WhatsApp" confirmation; delivery status polling begins
- **Error state:** WhatsApp failed — error card: "WhatsApp delivery failed. Use 'Copy Shareable Link' to share manually." with retry and link options (WA pattern EC-01)
- **Offline state:** All network-dependent share options disabled; offline indicator; "Download PDF" still works if PDF is already generated and cached

**Constraints:**
- DPDPA gate must visually communicate why certain options are blocked (not just greyed out silently) — parent needs to know consent or opt-in is missing
- WhatsApp option must not fire automatically — Dr. Sunita must tap explicitly (compliance: opt-in required; no accidental sends)
- Share link must have 128-bit entropy minimum (UUID-based, not guessable) per RX-002 security NFR

---

### Screen: Supervisor Caseload Dashboard (progress reporting lens)

**Purpose:** Dr. Sunita can see at a glance which children in her supervised caseload have overdue progress reports — so she can prioritize report writing without opening individual records.
**Primary action:** Tap child row to open record and start report
**Entry point(s):** Home screen (supervisor role) → Caseload tab; or notification deep-link from Rahul's overdue flag action
**Exit point(s):** Tap child row → Child Profile (lands on Progress Report tab if overdue flag is present)

**Key components:**
- **Overdue report flag indicator**: per child row — "Report overdue: [N] days" in amber/red depending on severity; text + icon (not color alone)
- **Filter: "Overdue flags only"**: filters list to show only children with at least one overdue flag; count of flagged children shown at top
- **Child row data**: child name, assigned Primary Therapist, date of last completed session, date of last progress report (or "Never" if no report exists), overdue flag count
- **"Filter by Therapist" control**: Dr. Sunita can filter to see overdue reports for a specific therapist's caseload

**States:**
- **Empty state (no overdue flags):** "All progress reports are up to date" with no flag rows (shown when filter is "Overdue only")
- **Loading state:** Dashboard loads in ≤ 3 seconds for up to 50 children (MPM-003 NFR); skeleton rows shown
- **Error state:** Connectivity unavailable → last-synced data shown with "Last updated [timestamp]" banner; flag calculations may be stale
- **Offline state:** Readable from cache; flag calculations based on last-synced report dates; staleness indicator shown

**Constraints:**
- Dashboard must be usable on mid-range Android, not desktop-only (MPM-003 NFR)
- Row height must accommodate all status fields without truncation on 5.5-inch screen
- Color-coding for overdue severity must also carry text labels ("7 days overdue", "14+ days overdue") — not color alone

---

## Developer Handoff

### Step-level technical summary

| Step | Data written | Data read | API / event | Offline behavior | Regulatory gate |
|---|---|---|---|---|---|
| 1A — Rahul flags overdue report | In-app notification record | `children.last_report_date`, `overdue_threshold_config` | POST `/notifications/supervisor` with child_id and flag_type=report_overdue | Dashboard readable from cache; notification queued for delivery | RBAC: Center Director role; overdue flag calculation uses configured thresholds |
| 1B — Dr. Sunita sees overdue flag | None | `supervisor_caseload` with flag data | GET `/supervisor/caseload?include_flags=true` | Readable from last-synced cache with staleness indicator | RBAC: Supervisor role; caseload scoped to assigned children |
| 2 — Review timeline | None | `children.{id}.timeline` filtered by period and event type | GET `/children/{id}/timeline?date_from={}&date_to={}&event_types=notes,soap` | Previously loaded entries readable from cache | ⚠️ DPDPA — aggregated child health data; RBAC: assigned clinical staff and supervisors only |
| 3 — Review session notes | None | `session_notes` for child, filtered by date range | GET `/children/{id}/notes?date_from={}&date_to={}&sort=date_asc` | Previously loaded notes readable from cache | ⚠️ DPDPA — child health data; RBAC: assigned staff |
| 4 — Review SOAP notes | None | `clinical_notes` type=SOAP for child, filtered by date range | GET `/children/{id}/clinical-notes?type=SOAP&date_from={}&date_to={}` | Previously loaded SOAP notes readable from cache | ⚠️ DPDPA — clinical assessments of minor; RBAC: supervisor and director only |
| 5 — Open report generation | None | `children.{id}.consent_status` | GET `/children/{id}/consent` | Consent check requires connectivity (fresh check); if offline show "Cannot verify consent — connect to proceed" | ⚠️ DPDPA — report creation opens clinical health data processing for a minor; consent must be confirmed Active before proceeding |
| 6 — Auto-populate report | `progress_reports: {child_id, period_start, period_end, status=draft, auto_populated_sections, source_note_ids[], source_soap_ids[], created_by, created_at}` | All `session_notes` and `clinical_notes` for child in the period; `therapy_programs.mastery_events` | POST `/children/{id}/reports/generate` with period dates; server aggregates all notes in period; maps to report sections | Report draft saved locally if offline aggregation fails; requires connectivity for full auto-population from server | ⚠️ DPDPA — aggregation of child health data across reporting period; encrypted at rest; source note IDs logged for audit trail; consent Active confirmed at generation time |
| 7 — Edit report sections | `progress_reports.sections` (all editable fields) | Auto-populated draft from Step 6 | PATCH `/reports/{report_id}` (periodic auto-save every 60 seconds; also on explicit save) | Auto-save writes to local storage; sync on restore | ⚠️ DPDPA — health data of minor; RBAC: author (Dr. Sunita) and admin (Rahul read-only) |
| 8 — Generate home program | `home_programs: {child_id, report_id (linked), targets_selected[], parent_instructions[], created_by, created_at}` | `therapy_programs.{id}.active.targets` | POST `/children/{id}/home-programs` | Draft saves locally; submit requires connectivity | ⚠️ DPDPA — therapy data of minor; export action logged in audit trail (TMPL-004 NFR) |
| 9 — Save & Finalize | `progress_reports.status=Final`, `progress_reports.finalized_at`, author stamp applied | None | PATCH `/reports/{report_id}` `{status: "final"}`; triggers PDF generation job | Final submission requires connectivity (same rule as SOAP submit and co-sign) | ⚠️ DPDPA — finalizing clinical document of minor; author credential stamped from PROFILE-001; audit trail entry written at finalization |
| 10 — PDF generation | `report_pdfs: {report_id, file_path, generated_at, file_hash}` | Report content, `center_letterhead` (RX-005), author profile (RX-004) | Background job: `/reports/{report_id}/generate-pdf` triggered by finalization; completes in ≤ 5 seconds | PDF generation is server-side; no offline behavior; client polls for completion status | ⚠️ DPDPA — PDF contains child health data; stored encrypted; file_hash for integrity verification; export action logged with actor, timestamp, file ID |
| 12 — DPDPA + opt-in gate check | None | `children.{id}.consent_status`, `parents.{id}.whatsapp_optin_status` | GET `/children/{id}/consent`, GET `/parents/{id}/whatsapp-optin` | Both checks require connectivity; if offline, share buttons disabled | ⚠️ DPDPA — child health report sharing to parent requires confirmed parental consent AND explicit parent opt-in for the WhatsApp channel |
| 13 — WhatsApp send | `report_delivery_log: {report_id, parent_id, channel=whatsapp, sent_at, delivery_status=sent}` | Approved WhatsApp template, parent WABA opt-in, parent WhatsApp number, report PDF | POST to WhatsApp Business API using approved report template with PDF attachment; delivery status webhook received asynchronously | Retry queue (3 retries over 30 minutes) on Meta API failure; fallback to shareable link option surfaced to Dr. Sunita | ⚠️ DPDPA — child health report transmitted via Meta's infrastructure (WhatsApp Business API); parent opt-in confirmed; transmission is encrypted; delivery event logged in audit trail with WABA message ID |
| 14 — Delivery status update | `report_delivery_log.delivery_status` updated (Sent → Delivered → Read) | WhatsApp delivery/read receipt webhook payload | Webhook: POST `/webhooks/whatsapp/delivery` → PATCH `/report-delivery-log/{id}` | Server-side webhook processing; client reflects on next load | RBAC: delivery log accessible to Dr. Sunita and Rahul (admin) only; not visible to Priya |
| 15 — View in Documents tab | None | `progress_reports` with delivery status, `report_pdfs` | GET `/children/{id}/documents?type=progress_report` | Previously loaded document list readable from cache; PDF content requires connectivity if not cached | ⚠️ DPDPA — document list contains child health data references; RBAC: assigned clinical staff and directors |

**Key state transitions:**
- `progress_reports` transitions: (none) → **Draft** (local, Step 6) → **Draft** (synced, Step 6–7) → **Final** (Step 9) → **PDF generated** (Step 10) → **Delivered** (Step 13–14)
- `home_programs` transitions: (none) → **Draft** (Step 8) → **Saved** (Step 8 confirm) → **Included in report PDF** (Step 10)
- `report_delivery_log` transitions: (none) → **Sent** (Step 13) → **Delivered** (Step 14 webhook) → **Read** (Step 14 read receipt, if enabled)
- `ABDM health record` (optional): (none) → **Pushed to ABHA locker** (Step 15 optional extension) → ABDM document ID stored

**Background jobs / async events triggered by this journey:**
- **Report data aggregation job**: triggered at Step 6 (POST `/children/{id}/reports/generate`); pulls session notes, SOAP notes, mastery events for the period; maps to report sections; completes synchronously (user waits ≤ 3 seconds) or with skeleton loading state
- **PDF generation job**: triggered at Step 9 (finalization); server-side; completes in ≤ 5 seconds; client polls `/reports/{report_id}/pdf-status` until complete; report preview available only after completion
- **WhatsApp delivery status polling**: WhatsApp Business API sends delivery receipt webhooks asynchronously; no client polling required; platform webhook endpoint updates delivery log on each status change (Sent → Delivered → Read)
- **Overdue report flag calculation**: background cron job runs daily; compares `last_report_date` per child against configured cycle thresholds; updates `overdue_flag` on child record; surfaces in MPM-003 and MPM-005 dashboards

**DPDPA compliance checkpoints:**
- Step 5: ⚠️ DPDPA — consent gate enforced before report creation; consent.status must = Active for this child; if not, report creation blocked
- Step 6: ⚠️ DPDPA — auto-population aggregates child health data across multiple notes; all aggregated data encrypted at rest; source note IDs logged for audit trail; consent Active confirmed at generation time
- Step 9: ⚠️ DPDPA — finalized clinical document of a minor; author credential stamped; audit trail entry immutable; document retained for minimum duration per DPDPA guidance (suggest: duration of therapeutic relationship + 3 years, pending legal review)
- Step 12: ⚠️ DPDPA — double gate: (1) parental consent for data processing (EMR-002) AND (2) parent's explicit opt-in for WhatsApp messaging (WA-003) must both be confirmed before the report PDF is transmitted via Meta's WhatsApp Business API infrastructure
- Step 13: ⚠️ DPDPA — child health report transmitted via WhatsApp Business API (Meta infrastructure); transmission is end-to-end encrypted on WhatsApp; platform-side delivery log stores only metadata (message ID, timestamps, delivery status) — not report content; report content stored server-side encrypted, not in Meta's storage
- Step 10 (PDF export): ⚠️ DPDPA — export action logged in child's audit trail with actor, timestamp, and file ID; PDF file stored encrypted at rest; access scoped to clinical staff and directors

---

## Cross-Journey Dependencies

| Depends on journey | Why | What breaks if missing |
|---|---|---|
| Journey 2: Child Enrollment & Intake | Child's EMR must exist (EMR-001), DPDPA consent confirmed (EMR-002), parent WhatsApp number on file, and parent opted in to WhatsApp (WA-003) | Steps 5 and 12 are gated by consent; Step 13 is gated by WhatsApp opt-in; without these, report can be created but cannot be shared digitally |
| Journey 6: Post-Session Documentation | All session notes (SNOTE-001 to SNOTE-005) and SOAP notes (SOAP-001 to SOAP-004) from the reporting period are the primary input data for Step 6 auto-population | Without accumulated session notes and SOAP notes, auto-population returns empty sections and Dr. Sunita must write the entire report manually — eliminating the key time-saving proposition of this journey |
| Journey 5: In-Session Data Collection (separate cluster) | Attendance records (SCHED-004 marking sessions Present) determine the sessions-attended count and attendance rate in the report's Session Summary section | Without confirmed attendance data, the report cannot accurately state how many sessions the child attended; auto-population of attendance metrics fails |
| WhatsApp Business API setup (WA-001, WA-002, WA-003) | The Step 13 WhatsApp delivery requires an active WABA connection and approved message templates | Without WABA setup, progress report sharing falls back to secure shareable link or PDF download — still functional but loses the WhatsApp-native delivery experience that makes it accessible to Meena |
| ABDM setup (ABDM-004, ABDM-001, ABDM-002) | Optional ABHA locker push at Step 15 requires center HIP registration, child ABHA ID, and ABDM consent | ABDM push is optional and fails gracefully — core journey completes without it; flag surfaces in admin settings |

---

## ⚠️ Feature Factory Disclaimer

These flows were defined by document synthesis from competitive observation and story engineering — not by validated user research. Before committing design effort or engineering capacity, a real product thinker should ask:

**What we assumed but haven't validated:**
- [ASSUMPTION — NOT VALIDATED] Progress report writing at Indian autism therapy centers currently starts from scratch every reporting cycle — with no carry-forward from previous reports or auto-population from session data (Journey Map H-17, HIGH risk). The auto-population mechanic (Step 6) is the primary time-saving proposition of this journey. If Indian supervisors currently write reports in 15–20 minutes using existing templates, the time savings may not justify the engineering complexity of the aggregation engine.
- [ASSUMPTION — NOT VALIDATED] Dr. Sunita will adopt the platform-provided report structure over her existing Word document format. If her current format is deeply embedded in her clinical practice and trusted by families, she may continue using Word and only use the platform for delivery — eliminating the auto-population value.
- [ASSUMPTION — NOT VALIDATED] Meena wants to receive a structured digital progress report via WhatsApp rather than a verbal update. Some parents may find a PDF document intimidating or inaccessible — particularly if written in clinical language (Journey Map BP-10; Journey Map H-13, medium-high risk). The report's value to Meena depends entirely on whether it is written in language she can understand.
- [ASSUMPTION — NOT VALIDATED] Meena has opted in to receiving WhatsApp Business messages from the center's WABA number, and will engage with a message from a business account differently from a personal number. The WhatsApp Business API opt-in requirement adds friction to the delivery path that does not exist in the current informal WhatsApp workflow (WA epic disclaimer).
- [ASSUMPTION — NOT VALIDATED] The overdue report flag mechanism (Step 1A/1B) will drive Dr. Sunita to prioritize report writing. If Dr. Sunita already knows which reports are overdue (through relationship awareness), the flag adds no value. If she is overwhelmed with clinical caseload, a flag may increase stress without changing behavior.
- [ASSUMPTION — NOT VALIDATED] Indian clinical supervisors will use or recognize the SOAP note format as the basis for progress narrative (Step 4). The progress report editor draws from SOAP Assessment and Plan sections to pre-populate domain progress. If SOAP notes are not written in Indian centers (see Journey 6 disclaimer), this pre-population source does not exist.

**What a researcher would ask before building this:**
- What does a real Indian autism therapy center progress report look like today? Reviewing 3–5 actual progress reports from willing centers would reveal the section structure, language register, and length that Indian supervisors and families are accustomed to — before the template is designed.
- How much time does Dr. Sunita currently spend writing a progress report? (Journey Map H-07, HIGH priority hypothesis) If the current process is 30 minutes per report and auto-population saves 15 minutes, is that a compelling proposition? If it is 3 hours, the answer is very different.
- Does Meena read the progress reports she currently receives? Sending a PDF via WhatsApp assumes Meena will open and read it. Research in the journey map (BP-10, H-13) suggests she may not understand clinical language — which means the document design (plain language, visual elements) is as important as the delivery mechanism.
- Would Meena prefer a brief WhatsApp message summary over a full PDF report? Some parents may want a 3-sentence summary with a link to the full report rather than a dense PDF landing in WhatsApp. Understanding this preference before committing to the PDF-attachment model would save a design cycle.

**What the Product Consultant would challenge:**
- The auto-population engine (Step 6) is the highest engineering-complexity element of this journey. It requires aggregating structured data from session notes, SOAP notes, and program version history — which themselves depend on Journey 6 being adopted first. If Journey 6 note adoption is low (which is the primary risk), the auto-population produces empty sections and the time-saving rationale for this journey collapses. Consider whether the MVP should be: "structured report template + manual fill" (no auto-population), ship that, prove adoption, then add auto-population in v2 once there is data to aggregate.
- The WhatsApp delivery path (Steps 12–14) carries the most regulatory and operational risk of any step in this journey. It requires: DPDPA consent Active (gate 1), parent WhatsApp opt-in (gate 2), WABA connected and approved templates (gate 3). If any of these three conditions fails, the delivery falls back to a shareable link — which is less accessible to Meena. The MVP for delivery could be "copy shareable link + download PDF" first, with WhatsApp Business API delivery added as a v2 upgrade once WABA setup is simplified for center directors.
- ABDM integration (optional extension at Step 15) is a significant engineering investment for an optional, conditional action at the very end of the journey. The Product Consultant challenge from Cluster 2 applies here: build core report creation and sharing first; add ABDM push as a Phase 2 feature after validating demand with center directors.

**Risk level:**
- Report creation with auto-population (Steps 5–9): **High** — depends on Journey 6 adoption (session notes + SOAP notes must exist); auto-population aggregation engine is novel; Indian format preferences are unvalidated
- Home program generation (Step 8): **Medium** — table stakes in US ABA tools; India-specific need is inferred; parent-language quality is a design risk
- PDF generation and delivery (Steps 10–15): **Medium** — PDF mechanic is reused from RX-001/RX-002 (lower risk); WhatsApp delivery path has three gate conditions that must all be met (higher risk for end-to-end completion)
- WhatsApp Business API delivery to Meena (Steps 12–16): **High** — WABA setup complexity, opt-in friction, and parent engagement with business-account messages are all unvalidated for this user segment
- Overdue report flagging trigger (Steps 1A/1B): **Low** — straightforward cron job + dashboard flag; low engineering complexity; well-precedented in US tools

Use the `/researcher` agent to validate H-17 (progress report writing behavior), H-07 (documentation time burden), and H-13 (parent report comprehension) before sprint planning.
Use the `/product-consultant` agent to challenge the auto-population engine scope and the WhatsApp delivery sequencing before committing engineering capacity.
Use the `/design-critique` agent to review the Progress Report Editor for Android usability and the Home Program Generator for plain-language instruction quality before prototyping.
