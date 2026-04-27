# User Journey: Clinical Program Design

> ❌ **OUT OF SCOPE — MVP**
> **Decision date:** 22 April 2026 | **Decision by:** Engineering + Product
> **Rationale:** Therapy-specific feature requiring net-new build; existing EMR components cannot be reused. Deferred to post-MVP.
> **Deferred to:** Post-MVP release
> **Adoption risk:** Clinical program design is the core clinical value proposition for supervisors and therapists. Deferring this means the MVP launches without the features most likely to matter to clinical staff. If primary research confirms Journey 4 is an adoption blocker, this decision must be revisited before scope is locked. See: `meetings/engineering/2026-04-22-engineering-alignment-meeting-summary.md`
> **Reference:** `meetings/engineering/2026-04-22-engineering-alignment-meeting-summary.md`

**Previously:** J2 | ❌ **OUT OF SCOPE — MVP (Deferred post-MVP)**
**Trigger:** A child's intake assessment is complete (assessment sessions have been conducted and results are known); Dr. Sunita needs to design the child's individualized therapy program and assign the care team
**Primary actor:** Dr. Sunita (Clinical Supervisor)
**Supporting actors:** Rahul (assigns staff, configures scheduling), Priya (receives program assignment, accesses program from session screen)
**Entry condition:** Child has an active EMR record (EMR-001 complete); DPDPA parental consent is confirmed (EMR-002 — green badge on record; consent_status = "confirmed"); child has at least one completed assessment session in the calendar (from Journey 2, Step 17–18); Dr. Sunita is assigned as Supervisor in the child's Care Team (MPM-001); Dr. Sunita's clinical profile has her RCI license number and credentials saved (RX-004)
**End state:** Therapy program is created using platform templates (version 1.0 saved against child's record), all program targets documented in the EMR, a SOAP Note written documenting the clinical rationale for the program design, Dr. Sunita's supervisor assignment confirmed, Priya assigned as Primary Therapist with read access to the active program, Priya can access the program from her session screen in ≤ 2 taps, and the recurring session schedule is created for ongoing therapy
**Journey source documents:**
- `cluster-1-clinical-documentation.md` — TMPL-001 through TMPL-005, EMR-003, EMR-004, EMR-005, SOAP-001 through SOAP-004
- `cluster-2-patient-records-intake.md` — MPM-001 through MPM-005, ABDM-002 through ABDM-003
- `cluster-4-scheduling-communication.md` — SCHED-001, SCHED-002

---

## Discovery Context

- **MVP Scope:** ❌ OUT OF SCOPE — Post-MVP

**Pain points & friction:**
- Assessment data captured on paper — not readily usable for trend tracking or report generation 🔵 Inferred
- Program design-to-therapist handover gap: if the briefing is verbal, Priya may misremember prompt levels or reinforcement schedules 🔶 [HYPOTHESIS]
- Parent communication of the program is informal — Meena leaves without a clear written summary of what is being worked on and why 🔶 [HYPOTHESIS]
- No structured home program document produced at this stage 🔶 [HYPOTHESIS]
- RPWD Act 2016 mandates documentation of individualized programs — but no structured format or filing system confirmed in small Indian centers ✅ RPWD Act cited; compliance gap is 🔶 [HYPOTHESIS]

**Emotional states:**
- Dr. Sunita: This is the core clinical work — likely engaged and invested. Pressure point is time: assessment + program design competes with ongoing clinical caseload 🔶 [HYPOTHESIS]
- Meena: Anxious to understand the plan. May not fully comprehend clinical terminology used in verbal explanation 🔵 Inferred from caregiver burden research — educational gaps noted
- Priya: Receives program; may ask clarifying questions. 🔶 [HYPOTHESIS] Level of handover clarity varies

**Current workarounds:**
- Some supervisors maintain personal program binders per child — not shared across staff 🔶 [HYPOTHESIS]
- Parents receive WhatsApp voice notes summarizing the program 🔶 [HYPOTHESIS]

**⚠️ DPDPA exposure:**
- Therapy programs are health data of a minor under DPDPA 2023. Parental consent must be confirmed (consent_status = "confirmed") before any program is created or stored. Program data must be encrypted at rest and access-scoped to assigned care team members, supervisors, and directors. All program creation and modification events must be logged in an immutable audit trail. Home program PDFs containing clinical data require export logging. Any ABDM health record push requires both DPDPA consent and a separate ABDM consent artifact.

---

## Step-by-Step Flow

| Step | Actor | Action | Screen / State | Technical Note |
|---|---|---|---|---|
| 1 | Dr. Sunita | Opens app; views Caseload Dashboard; locates newly assessed child's record (flagged "No program set") | Supervisor Caseload Dashboard (MPM-003) | GET /supervisor/{id}/caseload — reads: all children with Supervisor assignment, last_session_date, last_program_update, open flags; "No program set" flag appears when no therapy program exists for child; dashboard filters: "Overdue flags only" surfaces this child immediately |
| 2 | Dr. Sunita | Taps child's row; lands on Program/Data tab (not Profile tab — default landing for supervisor) | Child Record — Program/Data Tab | GET /children/{id}/program — reads: active program version, version history; empty state: "No program yet — tap 'Create New Program' to get started"; consent_status checked: must = "confirmed" before program creation is enabled |
| 3 | Dr. Sunita | Reviews child's intake-populated profile for assessment context: diagnosis, developmental history, prior therapy, UDID status | Child Profile Tab (INT-004 populated) | GET /children/{id}/profile — reads all intake fields; prior assessment session notes visible in session history; UDID flag prompts if number missing; offline: profile readable from cache if previously loaded |
| 4 | Dr. Sunita | Reviews uploaded documents: prior diagnosis reports, previous therapy reports, school records | Child Record — Documents Tab (EMR-003) | GET /children/{id}/documents — reads: document list (type, upload date, uploader); PDF/image viewer for each document; offline: document list readable from cache; file content viewable offline only if previously opened |
| 5 | Dr. Sunita | (Optional) Reviews prior session notes from assessment sessions to understand baseline | Child Record — Session Notes History (SNOTE-005) | GET /children/{id}/session-notes — reads: all session notes sorted by date descending; filter by date range for assessment period; each note shows: date, therapist, review status, first line of key observations; offline: previously loaded note history readable from cache |
| 6 | Dr. Sunita | Taps "Create New Program" on Program/Data tab; template picker opens | Template Picker (TMPL-001) | GET /templates — reads: center's active templates (platform pre-built + any custom templates from TMPL-005); minimum 5 pre-built templates shown: (1) DTT Skill Program, (2) NET Activity Program, (3) Behavior Intervention Plan (BIP), (4) Session Summary Template, (5) Home Program Template; template picker loads in ≤ 1 second; DPDPA consent gate checked before picker is shown |
| 7 | Dr. Sunita | Selects template (e.g., "DTT Skill Program"); program creation form opens pre-filled with template structure | Program Creation Form (TMPL-001) | GET /templates/{id} — reads: template field structure; form pre-fills: Program name, Domain (dropdown), Teaching method, Target description, Baseline, Prompt level (dropdown), Reinforcement schedule, Mastery criterion, Teaching notes; form loads in ≤ 1.5 seconds on minimum-spec Android |
| 8 | Dr. Sunita | Fills in program details for first target: customizes domain, target behavior description, prompt level (e.g., "Gestural"), reinforcement schedule, mastery criterion | Program Creation Form — Target Block | Client-side: real-time field validation; "Add another target" button repeats the target block; up to 20 targets per program; offline: draft saves locally on each field change |
| 9 | Dr. Sunita | Taps "Add another target" repeatedly to build the full target list across developmental domains | Program Creation Form — Multi-Target State | Up to 20 target blocks rendered; "Add another target" button must be reachable without scrolling to page bottom on standard Android (≥ 5.5 inch); touch targets ≥ 44px; no minimum targets required for draft save, but at least 1 required for final save |
| 10 | Dr. Sunita | Reviews complete program; optionally adds a change note explaining the program design rationale | Program Creation Form — Change Note Field (TMPL-002) | Change note: free text, max 200 characters; example: "Initial program — baseline DTT targets across communication and adaptive domains, selected from assessment findings." |
| 11 | Dr. Sunita | Taps "Save Program"; program saved as version 1.0 against child's record | Program Saved Confirmation | POST /children/{id}/programs — writes: program object with all targets, version = 1.0, saved_by = Dr. Sunita ID, saved_at = timestamp, change_note; program immediately pushed to Priya's session screen for this child (if Priya is assigned); ⚠️ DPDPA — therapy program is child health data; consent_status must = "confirmed"; program stored encrypted at rest |
| 12 | Dr. Sunita | Creates a SOAP Note documenting the clinical rationale for the program design: assessment findings, program logic, planned targets, and next review date | SOAP Note Creation Screen (SOAP-001) | POST /children/{id}/clinical-notes — writes: note type = "SOAP", author_id, credential, timestamp, subjective, objective, assessment, plan sections; Assessment and Plan sections required before final submit; draft saves allowed with partial sections; offline: draft saves locally |
| 13 | Dr. Sunita | Fills in all four SOAP sections using ABA-specific guided prompts | SOAP Note — Four Section Form (SOAP-004) | Guided prompts (placeholder ghost text, disappears on typing): Subjective — "What did the therapist, parent, or child report this period?"; Objective — "What session data was observed?"; Assessment — "What is your clinical interpretation of progress?"; Plan — "What clinical actions will be taken? Include new targets, prompt fading, parent recommendations, next review date."; prompts are offline-available (part of template, not server-fetched) |
| 14 | Dr. Sunita | Taps "Submit" on SOAP note; note status changes to "Final"; optionally taps "Lock" | SOAP Note — Final / Locked State (SOAP-001) | PATCH /clinical-notes/{id} — updates: status = "Final" or "Locked"; lock requires connectivity (integrity requirement — same as note co-sign); locked notes cannot be edited; Dr. Sunita's name and RCI credential stamped automatically from her profile |
| 15 | Dr. Sunita | (If not yet assigned) Opens child's Care Team tab; confirms Priya is assigned as Primary Therapist with correct role | Care Team Tab (MPM-001) | GET /children/{id}/care-team — reads: current assignments; if Priya not yet assigned (possible if Journey 2 was done by Rahul and only Dr. Sunita was assigned initially), Dr. Sunita can view but Rahul must make the assignment (Director/Admin role required for staff assignment changes); Dr. Sunita sees "Add Staff Member" button only if she has admin rights |
| 16 | Rahul | (If triggered by Dr. Sunita's request) Opens Care Team tab; assigns Priya as Primary Therapist | Care Team Tab — Rahul (MPM-001) | POST /children/{id}/care-team — writes: Priya's assignment with role = "Primary Therapist"; Priya immediately gains access to child's record; her "My Children" list updates within 30 seconds of assignment sync |
| 17 | Priya | Opens app; sees new child appear in "My Children" list | Therapist Home Screen — My Children (MPM-002) | GET /therapist/{id}/caseload — reads: newly assigned child now visible; child card shows: first name, no session scheduled yet (if schedule not yet created), "Active" status indicator; list update is near real-time after assignment |
| 18 | Priya | Taps child card; lands on Session Tab; sees "Today's Program" card with "No sessions scheduled" and "View full program" button | Session Tab — Program Card (TMPL-003) | GET /children/{id}/active-program — reads: active program version; "Today's Program" card shows: program name, "View full program" button reachable in ≤ 2 taps from home screen; program loads from local cache if previously synced |
| 19 | Priya | Taps "View full program"; reads all current targets: name, teaching method, prompt level, reinforcement schedule, mastery criterion | Program View Screen (TMPL-003) | GET /children/{id}/active-program (full response) — reads: all target blocks; read-only scrollable list; loads in ≤ 1 second from cache; ≤ 2 seconds from network on 4G; offline: full program text available from last sync — this is a hard offline requirement |
| 20 | Dr. Sunita | Creates a Home Program document from the active therapy program; selects targets appropriate for home practice; adds parent-friendly instructions for each | Home Program Creation Screen (TMPL-004) | POST /children/{id}/home-programs — writes: selected_targets (subset of active program), parent_instructions per target (max 300 chars each), version, created_by, created_at; "Generate Home Program" button on Therapy Program tab; at least one target must be selected; PDF export available |
| 21 | Rahul | Sets up the recurring weekly therapy schedule for ongoing sessions (post-assessment): assigns Priya, sets time slots, room | Schedule Creation Screen (SCHED-001) | POST /schedules — writes: recurring schedule with recurrence_rule = weekly, child_id, therapist_id (Priya), room_id, start_time, duration; conflict detection runs against Priya's availability (SCHED-002); 12-week series created forward from next occurrence; offline: schedule creation queues locally |
| 22 | Dr. Sunita | Views child's Clinical Timeline; confirms all key events are present: intake documents, assessment sessions, program creation, SOAP note | Clinical Timeline View (EMR-004) | GET /children/{id}/timeline — reads: chronological feed of all events; event types: session, note, program_update, document_upload, consent, SOAP_note; "Program created — v1.0 by Dr. Sunita" entry visible; filter: All / Sessions / Notes / Program updates / Documents |
| 23 | Dr. Sunita | (Optional, if family has ABHA ID linked from Journey 2) Reviews ABDM consent status; if ABDM consent not yet captured, initiates ABDM consent flow with family | ABDM Section — Child Record (ABDM-002) | GET /children/{id}/abdm — reads: abha_id, abdm_consent_status; if abha_id = "Verified" but abdm consent not captured: "ABDM Consent: Not captured" with "Initiate consent" button; ABDM consent flow: OTP to ABHA-registered mobile, or via PHR app; consent artifact stored from ABDM gateway |
| 24 | Dr. Sunita | (End state check) Reviews Supervisor Caseload Dashboard; confirms child now shows: program updated today, next session scheduled, no open flags | Supervisor Caseload Dashboard (MPM-003) | GET /supervisor/{id}/caseload — dashboard now shows: child row with last_program_update = today, next_session = [scheduled date], no overdue flags; "No program set" flag cleared; journey complete |

---

## Decision Points

### Decision 1: Template selection — pre-built vs. custom
**At step:** 6–7
**Question:** Does the center have a custom template that matches Dr. Sunita's clinical workflow, or should she use a pre-built platform template?
- **Path A — Pre-built template selected (Happy path):** Dr. Sunita selects one of 5 pre-built templates (DTT, NET, BIP, Session Summary, Home Program); form opens with standard ABA field structure → Continue at Step 7
- **Path B — Custom center template selected:** Rahul has previously created a custom template (TMPL-005) matching the center's existing Word document structure; Dr. Sunita selects it from the template picker; form opens with center-specific fields → Continue at Step 7 with custom fields
- **Path C — No suitable template exists:** Dr. Sunita cannot find a template matching her clinical approach; she uses the closest pre-built template and customizes all fields manually → Continue at Step 7, but flag for Rahul to create a custom template (TMPL-005) for future use
- **Path D — Consent not confirmed (Edge case):** If consent_status ≠ "confirmed", "Create Program" button is disabled with tooltip: "Parental consent required before adding clinical records" → Journey blocked; return to Journey 2 Steps 5–7

### Decision 2: Multi-target program complexity
**At step:** 8–9
**Question:** How many targets does the child's program require, and across how many domains?
- **Path A — Standard complexity (3–8 targets, 1–2 domains — Happy path):** Dr. Sunita completes targets within a single session of form filling; all targets fit on one screen with scrolling → Continue at Step 10
- **Path B — High complexity (8–20 targets, multiple domains):** Dr. Sunita uses "Add another target" repeatedly; each domain may benefit from using a different template type (DTT for skill targets, BIP for maladaptive behaviors); she may save a draft mid-session and return → Draft saved locally at Step 8; continue at Step 10 on return
- **Path C — Target limit reached (20 targets):** "Add another target" button is disabled; message: "Maximum of 20 targets per program. Create a separate program for additional targets." → Dr. Sunita creates a second program (e.g., a BIP program separate from the DTT skill program) by repeating Steps 6–11 with a different template

### Decision 3: SOAP note completion and locking
**At step:** 12–14
**Question:** Does Dr. Sunita complete and lock the SOAP note in one sitting, or save as draft?
- **Path A — Complete in one sitting, submit and lock (Happy path):** All four SOAP sections filled; Dr. Sunita submits ("Final" status) and immediately locks; note is immutable → Continue at Step 15
- **Path B — Save as draft, complete later:** Dr. Sunita fills Subjective and Objective sections but runs out of time; saves draft; "1 unfinished draft" banner appears in SOAP history (SOAP-002) → Returns later to complete Assessment and Plan sections; submits on return → Continue at Step 15
- **Path C — Submit without locking:** Dr. Sunita submits to "Final" status but does not lock; note is visible to Rahul but editable by Dr. Sunita until she locks it; Rahul can view the note as clinical record → Continue at Step 15; lock can be applied later
- **Path D — Connectivity drops during submission:** SOAP note saves as draft locally; banner: "Saved offline — will submit when connected" → Submits automatically on reconnect; final submission requires connectivity (same requirement as co-sign)

### Decision 4: Priya already assigned (from Journey 2) vs. needs assignment now
**At step:** 15–16
**Question:** Was Priya assigned as Primary Therapist during Journey 2 (enrollment), or does she need to be assigned now?
- **Path A — Priya already assigned (Happy path):** Care Team tab shows Priya with "Primary Therapist" role and assignment date from Journey 2 → Skip Step 16; continue at Step 17
- **Path B — No Primary Therapist assigned:** Care Team shows "No Primary Therapist — this child's sessions cannot begin"; Dr. Sunita notifies Rahul; Rahul completes assignment → Steps 16; Priya receives access → Continue at Step 17
- **Path C — Primary Therapist is leaving / reassignment needed:** Rahul changes the Primary Therapist assignment (MPM-001 edit); structured handover workflow triggered (MPM-004): outgoing therapist has 48 hours to complete a handover note; incoming therapist sees "Handover note available" banner before first session; if outgoing therapist is deactivated before completing handover, Dr. Sunita is prompted to complete it
- **Path D — Child has no Primary Therapist and no incoming therapist identified yet:** Dr. Sunita is the only clinical contact; SOAP note is created; program is saved; scheduling (Step 21) cannot be completed until a Primary Therapist is assigned — SCHED-001 requires a therapist assignment

### Decision 5: Home program targets — scope and language
**At step:** 20
**Question:** Which of the therapy program targets are appropriate for home practice, and are the instructions in sufficiently plain language?
- **Path A — Subset of targets selected (Happy path):** Dr. Sunita checks 2–4 targets from the active program as appropriate for home practice; writes parent-friendly instructions for each → Home program saved; PDF available for sharing → Continue at Step 21
- **Path B — No active program exists yet:** "Generate Home Program" button shows error: "Create a therapy program first before generating a home program" → Journey must complete Steps 6–11 before this step is accessible
- **Path C — All targets deselected:** Dr. Sunita accidentally deselects all targets; inline validation fires: "Select at least one target for the home program" → Re-selection required before save

### Decision 6: ABDM consent for health record sharing
**At step:** 23
**Question:** Has the family's ABHA ID been linked (from Journey 2, Step 14), and has ABDM consent been captured?
- **Path A — No ABHA ID (most common at launch — Happy path for center operations):** ABDM section shows "ABHA: Not available"; Step 23 is skipped entirely; clinical journey completes without ABDM → Continue at Step 24
- **Path B — ABHA linked, ABDM consent not yet captured:** Dr. Sunita initiates ABDM consent flow (ABDM-002); OTP sent to parent's ABHA-registered mobile; consent artifact stored from ABDM gateway → ABDM consent confirmed; health record push (ABDM-003) unlocked for future use
- **Path C — ABDM consent captured, ABDM-003 push triggered:** Dr. Sunita can now push the SOAP note or progress report as an ABDM FHIR R4 document to the child's ABHA locker (ABDM-003); this is a separate, optional action and does not block the rest of the journey
- **Path D — ABDM gateway unavailable:** ABDM consent flow blocked; center operations not blocked; "ABDM consent service is temporarily unavailable" message shown → Step 23 deferred; journey continues to Step 24

---

## Screen Inventory

| Screen name | Purpose | Primary action | Personas who see it | Source story |
|---|---|---|---|---|
| Supervisor Caseload Dashboard | Dr. Sunita's single view of all supervised children, their therapist assignments, last session, and open flags | Filter by overdue flags; tap child row | Dr. Sunita | MPM-003 |
| Child Record — Program/Data Tab | Entry point for program creation; shows active program or empty state | Tap "Create New Program" | Dr. Sunita, Rahul | TMPL-001 |
| Child Profile Tab | Full intake-populated child profile: diagnosis, history, UDID, family background | Edit field; view UDID flag | Dr. Sunita, Rahul | INT-004 |
| Documents Tab | Upload and view prior documents for clinical context | View existing documents; upload additional | Dr. Sunita, Rahul | EMR-003 |
| Session Notes History | Chronological history of all session notes for assessment context | Tap note for full content; filter by date range | Dr. Sunita | SNOTE-005 |
| Template Picker | Selection screen for pre-built and custom templates | Select template type | Dr. Sunita | TMPL-001 |
| Program Creation Form | Full therapy program creation form with target blocks | Fill all target fields; save program | Dr. Sunita | TMPL-001 |
| Program Creation Form — Multi-Target State | Extended form with multiple target blocks for complex programs | Add/remove target blocks | Dr. Sunita | TMPL-001 |
| Program Version History | Read-only list of all saved program versions with change notes | View past version | Dr. Sunita | TMPL-002 |
| SOAP Note Creation Screen | Four-section SOAP note form with ABA-specific guided prompts | Complete all sections; submit | Dr. Sunita | SOAP-001, SOAP-004 |
| SOAP Note — Final / Locked State | View-only SOAP note after submission and optional locking | Lock note; view read-only | Dr. Sunita, Rahul | SOAP-001 |
| SOAP Note History | All SOAP notes for a child in date order; draft banner if unfinished draft exists | Tap to view; filter by note type | Dr. Sunita | SOAP-002 |
| Care Team Tab | View and modify staff assignments for the child | Add Staff Member (Rahul); view assignments (Dr. Sunita) | Rahul (edit), Dr. Sunita (view) | MPM-001 |
| Therapist Home Screen — My Children | Priya's personal caseload list filtered to her assignments | Tap child card → Session Tab | Priya | MPM-002 |
| Session Tab — Program Card | Priya's session-facing view with "Today's Program" card | Tap "View full program" | Priya | TMPL-003 |
| Program View Screen | Full read-only view of current active program for Priya | Read targets before/during session | Priya | TMPL-003 |
| Home Program Creation Screen | Select therapy targets for home practice; write parent-friendly instructions | Select targets; write instructions; save | Dr. Sunita | TMPL-004 |
| Custom Template Builder | Rahul creates center-specific note/program templates | Add fields; save and publish template | Rahul | TMPL-005 |
| Schedule Creation Screen | Create recurring weekly therapy session schedule | Configure recurrence; confirm | Rahul | SCHED-001 |
| Therapist Availability Screen | Set Priya's working hours and blocked slots | Set working days and hours | Rahul | SCHED-002 |
| Clinical Timeline View | Chronological feed of all clinical events for the child | Filter by event type; tap event for detail | Dr. Sunita, Rahul | EMR-004 |
| ABDM Section — Child Record | Link ABHA ID; capture ABDM consent; view ABDM consent status | Initiate ABDM consent flow | Dr. Sunita, Rahul | ABDM-002 |
| Children List / Search | Find a specific child record by name, diagnosis, or assigned therapist | Search; filter | Rahul, Dr. Sunita | EMR-005 |

---

## Designer Handoff

### Screen: Supervisor Caseload Dashboard

**Purpose:** Dr. Sunita's operational home screen — a glanceable view of all children under her supervision so she can prioritize review work and spot problems without opening individual records
**Primary action:** Tap child row to open child's Program/Data tab
**Entry point(s):** App home screen (auto-land for Supervisor role); left nav "Caseload" tab
**Exit point(s):** Tap child row → Child Record Program/Data Tab; "Filter: Overdue only" narrows list; tap "Filter by Therapist" → filtered view

**Key components:**
- Summary strip at top: count of supervised children, count with overdue flags (highlighted in amber if > 0)
- Child row: child name | assigned therapist name | last session date | last program update date | flag icons (orange dots) for overdue items
- Overdue flag types: session > 7 days ago (configurable), program update > 30 days ago (configurable)
- Filter controls: "Overdue flags only" toggle; "Filter by Therapist" dropdown
- "No sessions recorded" label when no sessions logged (not a blank date field)

**States:**
- **Empty state:** "No children are currently assigned to your supervision. Contact your center director." — with no child rows and a contact link
- **Loading state:** Skeleton rows while data fetches; 3-second maximum on 4G for up to 50 children
- **Error state:** "Could not load caseload — check your connection and try again."
- **Offline state:** Dashboard readable from last-synced data; amber banner: "Last updated [timestamp]" — flag calculations based on last-synced session data, not real-time

**Constraints:**
- Must be usable on a mid-range Android phone (not desktop-only) — compact row layout required
- Color-coded flags must also carry text labels ("7+ days since last session" — not color alone) for accessibility
- Access restricted to Supervisor and Director roles only (RBAC gate)

---

### Screen: Template Picker

**Purpose:** Let Dr. Sunita choose the right program template for the child's clinical needs before starting the creation form — reducing blank-page anxiety and structuring her input
**Primary action:** Select a template to open the Program Creation Form
**Entry point(s):** "Create New Program" button on Child Record Program/Data Tab
**Exit point(s):** Template selected → Program Creation Form pre-filled with that template's structure

**Key components:**
- Template cards (minimum 5): Template name, 1-line description of use case, visual icon (different icon per type: DTT / NET / BIP / Session Summary / Home Program)
- Center's custom templates (from TMPL-005) shown in a separate section below platform templates: "Your center's templates"
- "What's the difference?" collapsed help text explaining when to use each template type

**States:**
- **Loading state:** Template cards as skeletons while list fetches (≤ 1 second target)
- **Empty state (custom templates section):** "No custom templates yet — create one in Settings > Templates" (this section only)
- **Offline state:** Template picker available offline — template structures are bundled locally, not server-fetched; "Saved locally — will sync when connected" shown for custom templates if they haven't synced

**Constraints:**
- DPDPA consent gate checked before this screen is accessible; if consent not confirmed, "Create Program" button is disabled with tooltip — this screen is never shown
- Custom templates are center-scoped — Dr. Sunita only sees templates from her center
- Template picker must load in ≤ 1 second on minimum-spec Android

---

### Screen: Program Creation Form

**Purpose:** Dr. Sunita builds the child's individualized therapy program by filling in structured target blocks — replacing the blank Word document she uses today
**Primary action:** Fill all targets; tap "Save Program"
**Entry point(s):** Template selected in Template Picker → form opens pre-filled with template structure
**Exit point(s):** Save → Program saved as v1.0; confirmation shown; Priya's session screen updated; return to Program/Data Tab showing new version

**Key components:**
- Program header fields: Program name (editable), Domain (single-select dropdown: Communication / Social / Adaptive / Cognitive / Motor / Maladaptive Behavior), Teaching method (DTT / NET / Other)
- Target block (repeating, up to 20): Target behavior description (textarea), Baseline (short text), Prompt level (dropdown: Full Physical / Partial Physical / Gestural / Verbal / Independent), Reinforcement schedule (free text), Mastery criterion (free text — e.g., "4/5 correct across 3 consecutive sessions"), Teaching notes (free text, optional)
- "Add another target" button — must be reachable without scrolling to page bottom on a 5.5-inch Android screen
- Change note field (optional, max 200 characters): "Briefly describe why this program was created or what changed"
- "Save Draft" (top right) and "Save Program" (primary CTA bottom) buttons

**States:**
- **Empty state (new program):** All fields blank except those pre-filled from template (domain, teaching method may have defaults)
- **Draft state:** "Draft — not visible to therapists yet" banner at top; fields editable; program not yet pushed to Priya's session screen
- **Loading state (save):** "Saving program..." spinner on CTA; form locked
- **Error state — no targets:** Inline validation: "Add at least one target before saving"
- **Error state — consent missing:** "Parental consent required before adding clinical records" — form is not shown; user redirected to consent flow
- **Offline state:** Draft saves automatically to local storage on each field change; "Saved locally — will sync when connected" persistent banner; "Save Program" queues for sync; program is NOT pushed to Priya's session screen until online sync completes

**Constraints:**
- Touch targets ≥ 44px on all interactive elements
- "Add another target" button stays visible on screen without requiring full scroll on a standard Android 5.5-inch screen
- Prompt level dropdown must use native Android spinner for screen reader compatibility
- Target blocks are collapsible for easier navigation when 8+ targets are present
- Program pushed to Priya's session screen immediately on server-side save (within 30 seconds); if Priya is in an active session when program is saved, she sees a banner: "Program updated — tap to refresh"

---

### Screen: SOAP Note Creation Screen

**Purpose:** Dr. Sunita documents the clinical rationale for the therapy program design and her supervisory observations in a structured, four-section SOAP note — creating a durable clinical record meeting documentation standards
**Primary action:** Complete all sections; tap "Submit" to finalize
**Entry point(s):** "Add Clinical Note" → "SOAP Note" from note type picker on child profile
**Exit point(s):** Submit → note status = "Final"; optional Lock action available; return to Clinical Notes tab

**Key components:**
- Four section panels, each with label, sub-label, and guided placeholder text:
  - **Subjective:** "What did the therapist, parent, or child report this period?"
  - **Objective:** "What session data was observed? Include sessions attended, targets addressed, mastery %, behavioral incidents."
  - **Assessment** (required before submit): "What is your clinical interpretation? On track, plateauing, or regressing?"
  - **Plan** (required before submit): "What clinical actions are planned? New targets, prompt fading, parent recommendations, next review date."
- Auto-stamped fields (read-only): Dr. Sunita's name, credential/designation, RCI license number, date, time
- "Save Draft" button (saves partial note; Assessment and Plan can be blank in draft)
- "Submit" button (enabled only when Assessment and Plan are filled)
- "Lock" button (appears after Submit; irreversible)

**States:**
- **Draft state:** "Draft — not submitted" banner; all fields editable; note not visible in Rahul's admin views
- **Final state:** "Final" badge; Assessment and Plan locked from editing; Lock button visible
- **Locked state:** All sections read-only; "Locked by Dr. Sunita — [date/time]" footer; only Rahul can initiate unlock with a reason (which is logged)
- **Loading state:** "Saving SOAP note..." spinner
- **Error state — required sections blank:** Inline validation on Assessment and Plan fields: "Assessment is required before submitting"
- **Offline state (draft):** Draft saves locally; banner: "Saved offline — will submit when connected"; final Submit requires connectivity

**Constraints:**
- Placeholder text must NOT appear in saved note content (ghost text only, disappears on typing)
- Placeholder text contrast ratio meets WCAG AA for placeholder text (minimum 4.5:1 against field background)
- Text areas must be scrollable within the screen on Android without triggering full-page scroll conflicts
- Lock action requires connectivity (no offline locking — integrity requirement)
- SOAP note accessible only to clinical and admin roles with access to this child's record (RBAC)

---

### Screen: Program View Screen (Priya's session-facing view)

**Purpose:** Priya reads the current therapy program for a child before and during a session — her on-device reference for what to work on, at what prompt level, so she doesn't need to ask her supervisor
**Primary action:** Read all targets — no data entry on this screen
**Entry point(s):** "Today's Program" card on Session Tab → "View full program" button — reachable in ≤ 2 taps from app home screen
**Exit point(s):** Back to Session Tab; or stay on Program View during session (offline-cached)

**Key components:**
- Program name and version header
- Target list (scrollable): for each target: Target name / description, Teaching method (tag chip: DTT / NET), Current prompt level (visually prominent — e.g., bold text or colored chip), Reinforcement schedule, Mastery criterion
- "Last synced [date/time]" timestamp (shown always when offline; shown only when a new version is available when online)
- Update banner (when program has been updated by Dr. Sunita since last sync): "Program updated [X hours ago] — tap to refresh"

**States:**
- **Loading state (online):** Skeleton target rows while fetching; loads ≤ 2 seconds on 4G
- **Cached / offline state:** Full program text displayed from local cache; "Showing cached program — last synced [date/time]" banner; no functionality blocked; this is the PRIMARY state during in-session use
- **No program state:** "No program set yet. Contact your supervisor." — with supervisor's name shown if available
- **Update available state:** Amber banner at top: "Program updated [X hours/days ago] — tap to refresh" — Priya can choose when to refresh (do not force refresh during active session)
- **Access denied state (not assigned to child):** "You are not assigned to this child. Contact your center admin."

**Constraints:**
- ALL target fields must be readable at system default font size on a 5.5-inch Android screen without horizontal scrolling
- Offline load is a HARD REQUIREMENT — Priya enters a session room where connectivity is unreliable; program must be available without network
- This screen is read-only for Priya — no data entry; no edit access
- Touch targets ≥ 44px for back button and refresh action only (no other interactive elements)

---

### Screen: Home Program Creation Screen

**Purpose:** Dr. Sunita creates a simplified, parent-friendly version of selected therapy targets with plain-language instructions for Meena to practice at home between sessions
**Primary action:** Select targets + write parent-friendly instructions + save
**Entry point(s):** "Generate Home Program" button on Child Record Program/Data Tab
**Exit point(s):** Save → home program stored in child record; "Export as PDF" action available; return to Program/Data Tab

**Key components:**
- Pre-populated target list from active therapy program (checkboxes, all checked by default): target name and brief description from clinical program
- For each checked target: "Parent-friendly instruction" text field (max 300 characters) with character counter; example hint text: "When Arjun asks for something with a point, help him say the word. Repeat 5 times during snack time."
- "Check all / Uncheck all" toggle
- Save button (requires at least 1 target checked)
- "Export as PDF" button (appears after save; uses same mechanic as SOAP-003 export)

**States:**
- **Pre-filled state:** All targets checked; instruction fields blank (Dr. Sunita must write plain-language versions)
- **Loading state:** "Saving home program..."
- **Error state — no active program:** "Create a therapy program first before generating a home program" — button disabled
- **Error state — no targets selected:** Inline validation: "Select at least one target for the home program"
- **Offline state:** Draft saves locally; PDF export requires connectivity

**Constraints:**
- Instructions must be written in plain language — the screen should not show clinical jargon from the therapy program; the "Teaching notes" field from the therapy program is NOT auto-populated into instructions (Dr. Sunita must write fresh plain-language text)
- Character count indicator visible and live-updating for each instruction field
- PDF export: center name, child first name, date on header; parent instructions per target; no clinical prompt levels or mastery criteria in the PDF (parent-appropriate content only)

---

## Developer Handoff

### Step-level technical summary

| Step | Data written | Data read | API / event | Offline behavior | Regulatory gate |
|---|---|---|---|---|---|
| 1 | None | supervisor_id, assigned_children list, last_session_date, last_program_update, flag states | GET /supervisor/{id}/caseload | Read from last-synced cache; staleness banner if offline | RBAC: Supervisor role required; only assigned children visible |
| 3 | None | child profile fields (all INT-004 mapped fields), UDID status | GET /children/{id}/profile | Profile readable offline if previously cached | ⚠️ DPDPA — child profile is health data; access scoped to assigned staff + director/supervisor |
| 6 | None (template read only) | template list (platform + center custom) | GET /templates | Templates bundled locally for offline use (hard offline requirement) | DPDPA consent gate: consent_status must = "confirmed"; picker blocked if not |
| 11 | program_id, child_id, version = 1.0, template_type, all target objects (target_description, domain, teaching_method, prompt_level, reinforcement_schedule, mastery_criterion, teaching_notes), saved_by, saved_at, change_note | consent_status (must = "confirmed"), active_program_version | POST /children/{id}/programs | Draft saves locally on field change; POST queued offline; program NOT pushed to Priya's screen until server-side sync completes | ⚠️ DPDPA — therapy program is child health data; encrypted at rest; consent_status gate enforced server-side (not client-side only) |
| 11 (push event) | None (program already written) | program_id, therapist assignment (Priya's device token) | Server-side push: PROGRAM_UPDATED event → Priya's session screen | Priya's device receives update on next background sync | RBAC: event only pushed to staff assigned to this child |
| 12–14 | soap_note_id, child_id, author_id, author_credential, timestamp, subjective, objective, assessment (required), plan (required), status (Draft / Final / Locked), lock_timestamp | child_id, author profile (RCI number, credential), consent_status | POST /children/{id}/clinical-notes (type=SOAP); PATCH /clinical-notes/{id} for status updates | Draft saves locally; final Submit requires connectivity; Lock requires connectivity | ⚠️ DPDPA — SOAP note is child health data; access scoped to clinical + admin roles; audit trail on lock/unlock |
| 15–16 | care_team_assignment: staff_id, role = "Primary Therapist", assigned_by, assigned_at | Child care team current state | POST /children/{id}/care-team | Reads from cache; writes require connectivity | RBAC: assignment change logged in immutable audit trail; Priya's access to child record takes effect within 30 seconds of server sync |
| 20 | home_program_id, child_id, selected_target_ids, parent_instructions per target, version, created_by, created_at | active program targets (read for pre-population) | POST /children/{id}/home-programs | Draft saves locally; PDF export requires connectivity | ⚠️ DPDPA — home program is child health data; exported PDF logged in audit trail; parent-appropriate content only (no clinical mastery %) |
| 21 | session series: recurring_schedule_id, child_id, therapist_id, room_id, start_time, duration, recurrence_rule = weekly, status = "Scheduled", 12 session instances | Therapist availability (Priya's SCHED-002), room bookings | POST /schedules | Queue locally; sync on restore; reminder jobs created server-side on sync | ⚠️ DPDPA — session schedule is health-adjacent data; consent_status gate |
| 22 | None (read-only timeline) | All child events: sessions, notes, program updates, documents, consent | GET /children/{id}/timeline | Previously loaded timeline readable offline from cache | ⚠️ DPDPA — aggregated clinical events; access scoped to assigned staff + supervisor/director |
| 23 | abdm_consent_artifact_id, consent_scope, consent_timestamp, abdm_consent_id (from gateway) | abha_id (must be verified), abdm_consent_status | POST /abdm/consent → ABDM Consent Manager API | ABDM consent cannot be captured offline; center operations not blocked if unavailable | ⚠️ DPDPA + ABDM — dual consent requirement; ABDM consent stored separately from DPDPA consent; linked by child_id |

**Key state transitions:**
- program.status transitions: "none" → "v1.0 active" at Step 11
- soap_note.status transitions: "none" → "Draft" (any time after Step 12 starts) → "Final" (Step 14 submit) → "Locked" (Step 14 optional lock)
- care_team_assignment.role transitions: Dr. Sunita already "Supervisor" (from Journey 2); Priya "none" → "Primary Therapist" at Step 16
- child.caseload_dashboard_flags: "No program set" → cleared after Step 11; "No upcoming session" → cleared after Step 21
- recurring_session.status for each instance: auto-set to "Scheduled" at Step 21

**Background jobs / async events triggered by this journey:**
- PROGRAM_UPDATED push event: triggered at Step 11 (program save); delivers update notification to Priya's session screen within 30 seconds
- REMINDER_SCHEDULE jobs: triggered at Step 21 (recurring schedule creation); creates T-24h and T-2h reminder jobs for each session instance across 12 weeks
- VERSION_HISTORY_CREATE: triggered at Step 11 on every program save; increments version number; previous version stored read-only

**DPDPA compliance checkpoints:**
- Step 2: ⚠️ DPDPA — consent_status must = "confirmed" before Program/Data tab clinical content is shown; EMR gate enforced
- Step 6: ⚠️ DPDPA — "Create Program" button disabled if consent_status ≠ "confirmed"; tooltip explains; no template picker shown
- Step 11: ⚠️ DPDPA — therapy program is health data of a minor; consent gate enforced server-side; encrypted at rest (AES-256); access scoped by RBAC to care team members + supervisor + director
- Step 12–14: ⚠️ DPDPA — SOAP note is clinical health data; audit trail on all state transitions (draft → final → locked, plus any unlock events); retained for minimum 3 years
- Step 20: ⚠️ DPDPA — home program PDF contains health data; export action logged in audit trail with actor, timestamp, file ID; parent-appropriate content only in PDF
- Step 23: ⚠️ DPDPA + ABDM — pushing health records to ABDM requires both DPDPA consent (confirmed) AND ABDM consent artifact (separate consent flow); dual gate enforced before any ABDM push

---

## Cross-Journey Dependencies

| Depends on journey | Why | What breaks if missing |
|---|---|---|
| Journey 2: Child Enrollment & Onboarding | Child record must exist (EMR-001 complete); DPDPA consent must be confirmed (consent_status = "confirmed"); Dr. Sunita must be assigned as Supervisor (MPM-001) | Journey 4 cannot start at all; consent gate blocks program creation, SOAP note, and clinical timeline at Steps 2, 6, and 12 |
| Staff account creation & platform authentication (AUTH-001) | Dr. Sunita must have a Supervisor role account; her profile must have RCI license number saved (RX-004 equivalent — needed for SOAP note credentialing) | SOAP note cannot be submitted (no credentials to stamp); RBAC gates cannot function without role assignments |
| Priya's staff account + therapist availability configured (SCHED-002) | Priya must exist as a user account and have her availability configured before Step 16 (assignment) and Step 21 (scheduling conflict detection) | Care team assignment (Step 16) shows Priya in picker but scheduling (Step 21) may produce false conflict errors if availability is not set |
| Session data collection journey (future Journey 6) | Once this journey completes, Priya accesses the program from her session screen (Steps 18–19) and begins collecting session data; session notes (SNOTE-001) reference active program targets from Step 11 | Without this journey's end state, Priya has no program targets to reference in "Goals addressed" multi-select in SNOTE-001; session notes would be target-less |
| Progress reporting journey (future Journey 8) | Progress reports draw from: SOAP notes (this journey Step 12–14), session note history, clinical timeline (Step 22), and program version history (TMPL-002) | Progress reporting journey requires all clinical data created in this journey to be complete and properly versioned |
| Custom template configuration (TMPL-005 — Rahul) | If Rahul has not yet built a custom template, Dr. Sunita is limited to 5 pre-built templates (Step 6) | Dr. Sunita may find pre-built templates structurally misaligned with her clinical training; template adoption risk (see Feature Factory Disclaimer) |

---

## ⚠️ Feature Factory Disclaimer

These flows were defined by competitive observation, document synthesis, and category assumption — not by validated user research with Indian autism therapy clinical supervisors or therapists. Before committing engineering capacity or design effort:

**What we assumed but haven't validated:**
- [ASSUMPTION] Dr. Sunita will use platform-provided ABA template structures (DTT, NET, BIP) rather than her existing Word document format. Template adoption depends entirely on whether the field structure matches her clinical mental model — which is shaped by Indian RCI training programs, not US ABA certification frameworks (CentralReach's ABLLS-R templates are US-ABA-specific and may not transfer). Validate template field structure against 3–5 real therapy program documents from Indian centers before finalizing TMPL-001 field definitions. (Cluster 1 disclaimer, Journey Map H-17)
- [ASSUMPTION] Indian clinical supervisors are familiar with and use the SOAP note format (Subjective / Objective / Assessment / Plan). SOAP is a US/UK medical documentation format. Indian clinical training programs (RCI, NIMH) may not emphasize this structure. If the format is unfamiliar, consider renaming or restructuring the sections. Validate format familiarity with 5–10 clinical supervisors before building SOAP-001. (Cluster 1 disclaimer)
- [ASSUMPTION] Dr. Sunita experiences the current program-to-therapist handover (verbal briefing with paper handover, per Journey Map BP-07) as sufficiently problematic to adopt a digital program creation and access workflow. If the verbal briefing "works well enough," the platform's program access feature (TMPL-003) may see low adoption. (Journey Map H-05)
- [ASSUMPTION] Priya will access the therapy program from her phone before each session. This assumes she has her phone with her and charged, that the app loads fast enough to be useful in the 2–3 minutes before a session, and that the program format on screen is easier to reference than the paper printout she may currently use. (Journey Map H-01)
- [ASSUMPTION] Dr. Sunita is willing and able to write SOAP notes or therapy programs on a phone (minimum-spec Android). Supervisors may strongly prefer desktop/laptop for documentation tasks. The journey must be functional on both form factors, but phone-first may create friction. (Journey Map H-07)
- [ASSUMPTION] ABHA uptake among families at private Indian autism therapy centers is sufficient to make ABDM consent (Step 23) and health record push (ABDM-003) worth building in the same sprint as core clinical program design. (Cluster 2 disclaimer)

**What a researcher would ask before building this:**
- What does a real Indian autism therapy supervisor's program document look like today? Request 3–5 example programs from willing centers before finalizing the TMPL-001 field structure. Does the platform's template structure match, or is it over-engineered from US ABA frameworks?
- Does Dr. Sunita know what a SOAP note is? Run a 10-minute concept test with 5 supervisors: show them the four-section form (with Indian-specific prompts) and ask them to complete a mock note. If fewer than 3/5 complete it correctly without confusion, the format name and section labels need adaptation.
- How does Dr. Sunita communicate a new or updated program to Priya today? Observe this handover moment in 3–5 centers. If the handover is a brief verbal chat in the hallway, the platform's program creation workflow must be faster and less effortful than that chat to displace it.
- What happens when Priya enters a session room with the current paper program? Does she reference it during the session, or does she already have it memorized? This determines whether TMPL-003 (offline program access) is solving a real problem or a hypothetical one.

**What the Product Consultant would challenge:**
- The SOAP note (Steps 12–14) is a significant effort investment in an unvalidated format. Consider whether a simpler "Program Review Note" — a single free-text note with three guided prompts (What I observed, My clinical interpretation, What I'm changing) — delivers 80% of the compliance value with 20% of the format-adoption risk. Build the simpler version first; upgrade to full SOAP if supervisors want more structure.
- TMPL-005 (custom template builder for Rahul, Step 6 optional) is a P2 feature in the backlog for good reason — it requires Rahul to be both technically capable and motivated enough to configure templates. Do not block clinical program design on the existence of custom templates. Pre-built templates must be good enough for v1.
- The home program creation (Step 20) and ABDM consent (Step 23) steps add scope to this journey but are not on the critical path to the end state. Consider whether the journey end state should be: program created + SOAP note written + therapist assigned + schedule created — and whether home program and ABDM can be triggered asynchronously as optional downstream steps.

**Risk level:**
- Steps 1–11 (caseload dashboard, template selection, program creation): Medium–High risk — core clinical value proposition; template adoption assumption is the single highest-risk bet in the product
- Steps 12–14 (SOAP notes): High risk — format familiarity in Indian clinical training is unvalidated; may need format adaptation before v1
- Steps 15–21 (staff assignment + scheduling): Low–Medium risk — table stakes for clinical platforms; Indian adoption assumption is directionally sound
- Steps 22 (clinical timeline): Low risk — read-only aggregated view; no new data created; clear value for Dr. Sunita
- Step 23 (ABDM consent): High risk — depends on ABHA uptake in private therapy center families; optional step that should not block the critical path

Use the `/research` agent to validate SOAP format familiarity and template structure alignment with Indian clinical training before sprint planning.
Use the `/product-consultant` agent to challenge whether SOAP notes should be replaced with a simpler "Program Review Note" format for v1.
Use the `/design-critique` agent to review the Program Creation Form before prototyping — particularly the multi-target scrolling behavior on minimum-spec Android.
