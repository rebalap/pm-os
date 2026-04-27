# User Journey: Session Notes / Clinical Notes

**Previously:** J3 | ✅ **IN SCOPE — MVP**
**Trigger:** A therapy session ends — Priya needs to document what happened, and Dr. Sunita needs to review it, act on it, and communicate program changes back
**Primary actor:** Priya (Special Educator — session note author); Dr. Sunita (Clinical Supervisor — reviewer, SOAP note author, program updater)
**Supporting actors:** None (self-contained clinical workflow between therapist and supervisor)
**Entry condition:** A session has taken place and has been marked Present in the scheduling system (SCHED-004). The child's EMR exists with confirmed DPDPA parental consent (EMR-002 / CONSENT-001). Priya is assigned to this child's care team (MPM-001).
**End state:** Session note saved and synced to the child's EMR, Dr. Sunita has reviewed and co-signed the note, a SOAP note has been created or updated with program decisions, any program changes have been published and Priya has seen the updated program on her session screen.
**Journey source documents:**
- `cluster-1-clinical-documentation.md` — SNOTE-001 through SNOTE-005, SOAP-001 through SOAP-004, TMPL-001 through TMPL-003, EMR-004
- `cluster-2-patient-records-intake.md` — MPM-001 (care team assignment, RBAC gates), MPM-003 (supervisor caseload dashboard)
- `cluster-4-scheduling-communication.md` — SCHED-004 (attendance mark that precedes this journey), WA-006 (session summary to parent — downstream of this journey)

---

## Discovery Context

**MVP Scope:** ✅ IN SCOPE — MVP

**Pain points & friction:**
- No standard template for session notes — quality and completeness vary by therapist and by day 🔶 [HYPOTHESIS]
- Notes written on paper accumulate in a physical file with no search, filter, or trend analysis capability 🔵 Inferred
- WhatsApp-based session notes ⚠️ DPDPA — unencrypted transmission of child clinical data to supervisor's personal device 🔶 [HYPOTHESIS]
- Note writing competes with next session preparation — rushed or missed entries are common 🔶 [HYPOTHESIS]
- Session notes are the data foundation for progress reports (Journey 8, deferred post-MVP) — without structured digital notes, progress reporting cannot be semi-automated 🔵 Inferred structural dependency

**Emotional states:**
- Priya: Post-session note writing feels like administrative overhead — next child may already be waiting. Documentation motivation is low when the benefit (supervisor review, program update) is delayed by days or weeks. 🔶 [HYPOTHESIS]
- Dr. Sunita: Without structured session notes, her understanding of each session depends on Priya's verbal recall — which degrades quickly. Inconsistent note quality makes clinical decisions harder. 🔵 Inferred from documentation literature
- Rahul: Session notes are invisible to the director in the current workflow — no aggregated view of what is happening clinically across the center. 🔶 [HYPOTHESIS]

**Current workarounds:**
- Therapists send a WhatsApp voice note to supervisor instead of writing — reduces friction but creates an unstructured, unarchived record ⚠️ DPDPA 🔶 [HYPOTHESIS]
- End-of-day summary note written from memory covering all sessions — compressed and retrospective 🔶 [HYPOTHESIS]

**⚠️ DPDPA exposure:**
- Session notes transmitted via WhatsApp constitute unencrypted transmission of child clinical data to a supervisor's personal device — a DPDPA 2023 risk even before platform data storage is considered 🔶 [HYPOTHESIS]
- Archived paper session notes have no access control — any staff member with physical access to the file can read a child's clinical record; no consent tracking for data access exists 🔵 Inferred

**Dependency note:** Session notes are the data foundation for Progress Reports (Journey 8 — deferred post-MVP). Structured digital session notes are a prerequisite for semi-automated progress reporting when Journey 8 is built.

---

## Step-by-Step Flow

| Step | Actor | Action | Screen / State | Technical Note |
|---|---|---|---|---|
| 1 | Priya | Taps "Mark attendance" on today's session card and selects **Present** | Daily Schedule screen → Session Card | `SCHED-004`: PATCH `/sessions/{id}/attendance` with status=Present; haptic feedback fires; timestamp recorded; writes locally first (offline-first) — syncs in background |
| 2 | Priya | Taps "Add Note" on the session detail screen (≤ 4 taps from home screen) | Session Detail screen | `SNOTE-001 AC-01`: opens Note Creation screen in ≤ 1 second; DPDPA gate checked — consent must be Active (EMR-002); if not Active, block with error |
| 3 | Priya | Fills in the session note form: Goals addressed (multi-select from active program targets), Child's response/mood (structured options), Key observations (free text), Incidents toggle, Next session focus | Note Creation screen | Session date/time and therapist name are pre-filled from session record; Goals addressed field pulls from `TMPL-001` active program targets for this child via GET `/children/{id}/program/active/targets`; all form state held in local storage |
| 4 | Priya | Taps **Save** | Note Creation screen → success state | `SNOTE-001 AC-03/AC-04`: if online, POST `/sessions/{id}/notes`; if offline, note saved to device local storage with status=pending_sync; haptic confirmation fires regardless; banner shows "Saved offline — will sync when connected" if no connectivity |
| 5 | System (background) | Note syncs to server when connectivity restores | Background sync process | On sync: note status transitions Draft → Submitted; note appears in Dr. Sunita's review queue within 30 seconds; push notification or queue badge increments on Dr. Sunita's device |
| 6 | Dr. Sunita | Opens the Notes review queue — sees all pending session notes across her caseload, sorted by child and date | Supervisor Notes Queue screen | `SNOTE-002 AC-01`: GET `/supervisor/notes/pending` scoped to Dr. Sunita's assigned caseload (RBAC: Supervisor role, MPM-001); default filter: last 7 days |
| 7 | Dr. Sunita | Taps a note to open it in full | Note Detail screen (read view) | `SNOTE-002 AC-02`: GET `/notes/{id}`; displays all fields Priya filled in; session date, time, and therapist name shown; "Synced from offline" indicator shown if applicable |
| 8 | Dr. Sunita | Reviews the note content and taps **Mark as reviewed** | Note Detail screen | `SNOTE-002 AC-03`: PATCH `/notes/{id}` status → Reviewed; note removed from pending queue; if note was edited by Priya after loading, "Edited" badge shown and note re-enters queue (`SNOTE-002 EC-02`) |
| 9 | Dr. Sunita | (Optional) Taps **Co-sign and lock** | Note Detail screen → Confirmation dialog | `SNOTE-003 AC-01/AC-02`: requires active connectivity (no offline co-sign); confirmation dialog: "Co-signing locks this note permanently. Proceed?"; on confirm: POST `/notes/{id}/cosign` — stamps Dr. Sunita's name, credential (from PROFILE-001), date, time; note status → Co-signed; audit trail entry written |
| 10 | Dr. Sunita | Opens the child's profile to view the full session note history | Child Profile → Session Notes tab | `SNOTE-005 AC-01/AC-02`: GET `/children/{id}/notes?sort=date_desc`; date range filter available; paginates at 20 entries; co-signed and reviewed notes visible in read-only mode |
| 11 | Dr. Sunita | Opens "Add Clinical Note" and selects **SOAP Note** to document her supervisory review | Child Profile → Clinical Note type picker | `SOAP-001 AC-01`: SOAP note template loads in ≤ 1.5 seconds; DPDPA gate re-checked; template available offline (embedded in app, not fetched from server — `SOAP-004 NFR`) |
| 12 | Dr. Sunita | Fills in SOAP note sections: Subjective (therapist/parent reports), Objective (session data, mastery %), Assessment (clinical interpretation), Plan (program changes, next steps) | SOAP Note editor screen | `SOAP-001 AC-02` + `SOAP-004 AC-01–AC-05`: guided prompts in each section are placeholder text only — not saved as content; Assessment and Plan are required; S and O are optional; author credential auto-stamped from PROFILE-001 |
| 13 | Dr. Sunita | Taps **Save Draft** or **Submit** | SOAP Note editor screen | `SOAP-001 AC-03/AC-04`: Draft: POST `/children/{id}/clinical-notes` with status=draft; Submit: status → Final; if offline during submit, saves as draft locally with banner "Saved offline — will submit when connected"; final submission requires connectivity |
| 14 | Dr. Sunita | (Optional) Taps **Lock** on a Final SOAP note | SOAP Note detail screen | `SOAP-001 AC-05`: POST `/clinical-notes/{id}/lock`; note becomes immutable; same lock mechanic as SNOTE-003; requires active connectivity; audit trail entry written |
| 15 | Dr. Sunita | If the SOAP Plan section indicates program changes, navigates to Therapy Program tab and opens the active program | Child Profile → Therapy Program tab | `TMPL-001/TMPL-002`: GET `/children/{id}/program/active`; current program and version history both accessible; version history shows all previous versions with change notes |
| 16 | Dr. Sunita | Edits the therapy program — modifies targets, prompt levels, or mastery criteria — and saves with an optional change note | Therapy Program editor screen | `TMPL-001 AC-03/TMPL-002 AC-05`: PATCH `/children/{id}/program`; new version created (e.g., v2.0); previous version retained in history; change note saved (e.g., "Removed target 3 — mastered. Faded prompts on target 1 per SOAP plan.") |
| 17 | System | Updated program immediately available to Priya on her session screen | Priya's Session Screen (background update) | `TMPL-003 AC-04`: push notification or banner appears on Priya's device: "Program updated — tap to refresh"; GET `/children/{id}/program/active` returns new version; new version cached locally for offline access |
| 18 | Priya | Sees "Program updated" banner on the child's session card and taps to refresh | Priya's Session Screen → Program view | `TMPL-003 AC-01/AC-02/AC-03`: loads updated program targets in ≤ 2 seconds (network) or from cache (offline); all targets show with current prompt level, reinforcement schedule, and mastery criterion |
| 19 | System | All clinical events for this journey (session note, SOAP note, program update) appear in the child's clinical timeline | Child Profile → Timeline tab | `EMR-004 AC-01/AC-02`: GET `/children/{id}/timeline`; timeline shows event type icon, date/time, one-line summary for each event; filterable by event type; soft-deleted items excluded from normal view |

---

## Decision Points

### Decision 1: Connectivity at note save time (Step 4)
**At step:** 4
**Question:** Does Priya have network connectivity when she taps Save?
- **Path A — Online:** Note saved directly to server; status → Submitted; appears in Dr. Sunita's queue within 30 seconds. → Continue at Step 5 (immediate)
- **Path B — Offline:** Note saved to device local storage with status=pending_sync; banner: "Saved offline — will sync when connected"; Priya's UI shows note as saved with no data loss. → Continue at Step 5 (deferred, when connectivity restores)
- **Path C (Edge case) — Device storage full:** Note cannot be saved; error: "Could not save note — device storage full. Free up space and try again." → Journey blocked; Priya must free storage before saving

### Decision 2: DPDPA consent gate (Step 2)
**At step:** 2
**Question:** Is parental consent confirmed for this child (EMR-002 status = Active)?
- **Path A — Consent Active:** Note creation screen opens normally. → Continue at Step 3
- **Path B — Consent not confirmed:** "Add Note" button is disabled; tooltip: "Parental consent required before adding clinical records. Complete consent first." → Journey blocked until consent is confirmed by Rahul

### Decision 3: Note edit after review (Step 8)
**At step:** 8
**Question:** Did Priya edit the note after Dr. Sunita loaded it?
- **Path A — Note unedited:** Dr. Sunita reviews and marks as reviewed normally. → Continue at Step 9
- **Path B — Note edited:** "Edited" badge appears; note re-enters review queue; Dr. Sunita receives in-app notification: "Session note for [Child name] on [date] was edited." → Return to Step 7

### Decision 4: Co-sign decision (Step 9)
**At step:** 9
**Question:** Does Dr. Sunita want to co-sign and lock the note?
- **Path A — Co-sign:** Note locked; status → Co-signed; Priya's Edit button replaced with "View only — note is locked." → Continue at Step 10
- **Path B — Review only (no co-sign):** Note status stays Reviewed; remains editable by Priya; Dr. Sunita continues. → Continue at Step 10
- **Path C (Edge case) — Offline at co-sign time:** Co-sign blocked (requires connectivity); banner: "Co-signing requires an internet connection." → Deferred until connectivity restored

### Decision 5: Program changes needed (Step 14 → 15)
**At step:** 14–15
**Question:** Does the SOAP Plan section indicate program changes for this child?
- **Path A — Program changes needed:** Dr. Sunita navigates to Therapy Program tab, makes edits, saves new version. → Continue at Step 16
- **Path B — No program changes:** SOAP note complete and submitted/locked; journey ends without a program update. → End state: note reviewed, SOAP saved; program unchanged
- **Path C (Edge case) — No active program exists:** Therapy Program tab shows "No program set yet." → Dr. Sunita must create a program first via TMPL-001 before this step can complete

### Decision 6: Priya's connectivity at program update notification (Step 17–18)
**At step:** 17–18
**Question:** Is Priya online when Dr. Sunita saves the program update?
- **Path A — Priya online:** Push notification delivered within 60 seconds; Priya sees "Program updated" banner immediately. → Continue at Step 18
- **Path B — Priya offline:** Update queued; on next app open or connectivity restore, cached version is marked stale with banner: "Showing cached program — last synced [date/time]." → Continue at Step 18 (deferred)

---

## Screen Inventory

| Screen name | Purpose | Primary action | Personas who see it | Source story |
|---|---|---|---|---|
| Daily Schedule (Priya) | Priya's list of today's sessions with attendance status | Mark attendance | Priya | SCHED-004 |
| Session Detail | Full session record including attendance status and note link | Tap "Add Note" | Priya, Dr. Sunita (read) | SNOTE-001 |
| Note Creation | Priya's structured post-session note form | Save note | Priya | SNOTE-001 |
| Supervisor Notes Queue | Dr. Sunita's inbox of all pending session notes across her caseload | Mark as reviewed | Dr. Sunita | SNOTE-002 |
| Note Detail (Review view) | Full note content in read-only mode with review/co-sign actions | Co-sign and lock | Dr. Sunita | SNOTE-002, SNOTE-003 |
| Session Notes History | Chronological list of all notes for a specific child | View note history | Dr. Sunita | SNOTE-005 |
| SOAP Note Editor | Four-section structured note with ABA-specific guided prompts | Submit SOAP note | Dr. Sunita | SOAP-001, SOAP-004 |
| SOAP Note Detail | Final/locked SOAP note in read-only mode with export/lock actions | Lock / Export as PDF | Dr. Sunita, Rahul | SOAP-001, SOAP-003 |
| Therapy Program Editor | Structured program editor with targets, prompt levels, mastery criteria | Save new program version | Dr. Sunita | TMPL-001 |
| Program Version History | Read-only list of all program versions with change notes | View previous version | Dr. Sunita | TMPL-002 |
| Today's Program (Priya view) | Priya's read-only view of active targets, prompt levels, and mastery criteria | View full program | Priya | TMPL-003 |
| Clinical Timeline | Chronological feed of all clinical events for a child | Tap event to view detail | Dr. Sunita, Rahul | EMR-004 |

---

## Designer Handoff

### Screen: Note Creation

**Purpose:** Priya documents what happened in a session immediately after it ends — quickly, on her phone, possibly in a hallway with 10 minutes before the next child.
**Primary action:** Save note (offline-capable)
**Entry point(s):** Tap "Add Note" on Session Detail screen (≤ 4 taps from home screen per SNOTE-001 epic DoD)
**Exit point(s):** On save → returns to Session Detail screen with "Note saved" confirmation; on discard → confirmation dialog, then back to Session Detail

**Key components:**
- **Session metadata bar** (top, non-editable): session date/time, child name, therapist name — pre-filled, read-only
- **Goals addressed**: multi-select chip picker pulling from active program targets; "No active targets" fallback state (SNOTE-001 EC-02)
- **Child's response/mood**: three-option selector — Engaged / Partially engaged / Dysregulated; optional free-text below (expandable)
- **Key observations**: free-text area, 500-character limit with live counter
- **Incidents or behaviors of concern**: yes/no toggle; if yes, free-text field expands below
- **Next session focus**: free-text area, 200-character limit
- **Save button**: large, full-width, bottom of screen; haptic on confirm
- **Offline banner** (conditionally shown): "Saved offline — will sync when connected"

**States:**
- **Empty state:** All fields blank except pre-filled metadata; save button disabled until Goals addressed + Child's response are filled
- **Loading state:** Note Creation screen opens in ≤ 1 second (SNOTE-001 NFR); skeleton shimmer for goals multi-select if targets are loading
- **Error state:** If device storage full on offline save: full-screen error card with message and retry; if DPDPA consent not active: note creation blocked before this screen is reached
- **Offline state:** Screen fully functional; Save writes to local storage; banner "Saved offline" shown persistently until sync completes

**Constraints:**
- Touch targets ≥ 44px on all interactive elements (SNOTE-001 NFR)
- Haptic feedback on Save confirmation — no audio cue (noisy session room environment)
- One-handed operation must be achievable: Save button anchored at bottom, reachable with thumb; no critical actions requiring two-handed interaction
- Must be operable with minimal cognitive load — Priya has 10 minutes between sessions and may have had a demanding session with an active child

---

### Screen: Supervisor Notes Queue

**Purpose:** Dr. Sunita's consolidated inbox of all session notes submitted by her therapists, so she can review her full caseload without chasing individual WhatsApp messages.
**Primary action:** Tap a note to open it for review
**Entry point(s):** Home screen (supervisor role) → Notes tab; or direct deep-link from push notification
**Exit point(s):** Tap note → Note Detail screen; "Mark as reviewed" → note leaves queue; filter controls → filtered queue view

**Key components:**
- **Default filter bar**: Last 7 days (default), filter by child, filter by therapist
- **Note list rows**: child name, session date, therapist name, review status badge (Pending review / Reviewed / Co-signed), first line of Key observations as preview
- **"Synced from offline" indicator**: small chip on notes that were saved offline and synced
- **Empty state card**: "No notes pending review — you're up to date" (SNOTE-002 EC-01)
- **"Mark as reviewed" action**: available from within Note Detail (not inline on queue row — requires deliberate review)

**States:**
- **Empty state:** "No notes pending review — you're up to date"
- **Loading state:** List loads in ≤ 2 seconds on 4G; skeleton rows shown during load (SNOTE-002 NFR)
- **Error state:** If connectivity drops while reviewing: previously loaded notes remain readable; "Mark as reviewed" queues offline (SNOTE-002 EC-03)
- **Offline state:** Last-cached note list shown; "Last synced [timestamp]" banner; reviewed status action queued locally

**Constraints:**
- Notes scoped to Dr. Sunita's assigned caseload only — no cross-caseload visibility without explicit admin grant (SNOTE-002 DPDPA)
- Touch targets ≥ 44px; notes must be readable at standard Android font size without zoom

---

### Screen: SOAP Note Editor

**Purpose:** Dr. Sunita writes a structured clinical record of her supervisory review, program decisions, and clinical interpretation — guided by ABA-specific prompts in each section.
**Primary action:** Submit SOAP note (or save draft for later completion)
**Entry point(s):** Child Profile → "Add Clinical Note" → select "SOAP Note" from type picker
**Exit point(s):** Submit → note saved as Final, appears in clinical timeline; Save Draft → note saved, draft banner on SOAP history; navigate away without saving → "Save as draft?" dialog (SOAP-001 EC-01)

**Key components:**
- **Section tabs or accordion**: Subjective, Objective, Assessment (required), Plan (required) — each collapsible for navigation
- **Guided prompt text**: ABA-specific placeholder text per section (SOAP-004); disappears on typing; meets WCAG AA contrast for placeholder text
- **Required field indicators**: Assessment and Plan marked required; inline validation fires if submit attempted with these blank
- **Author stamp preview** (bottom of form): Dr. Sunita's name, credential, date — auto-populated from PROFILE-001; read-only
- **Save Draft / Submit buttons**: both visible; Submit triggers validation; Save Draft saves without validation
- **Draft persistence banner**: "Draft saved — tap to continue" shown on SOAP history if a draft exists

**States:**
- **Empty state:** All section text areas blank with placeholder prompts visible; submit blocked until Assessment and Plan are filled
- **Loading state:** Template loads in ≤ 1.5 seconds (SOAP-001 NFR); prompts are embedded in app (available offline)
- **Error state:** Required fields blank on submit → inline validation: "Assessment is required before submitting"; connectivity drop during submit → "Saved offline — will submit when connected" (SOAP-001 EC-03)
- **Offline state:** Draft save works offline; final submission requires connectivity (same rule as co-sign); offline draft persists until sync

**Constraints:**
- Text areas must be scrollable within the screen without full-page scroll conflicts on Android (SOAP-001 NFR accessibility note)
- Section labels and guided prompts must be screen-reader readable
- Touch targets ≥ 44px; accessible on both desktop (Chrome) and Android

---

### Screen: Today's Program (Priya view)

**Purpose:** Priya views the current active therapy program before or during a session — what targets to work on, at what prompt level, and what the mastery criteria are.
**Primary action:** View full program (read-only)
**Entry point(s):** Home screen → child card → "Today's Program" card (≤ 2 taps from home); or direct link from session screen
**Exit point(s):** Back to session screen; or "Program updated — tap to refresh" banner → refreshes to latest version

**Key components:**
- **Program name and version**: shown at top; version number + last updated date
- **Target list**: each target shown as a card with: target name, teaching method (DTT/NET), current prompt level, reinforcement schedule, mastery criterion
- **Staleness banner** (conditional): "Showing cached program — last synced [date/time]" if offline
- **Update available banner** (conditional): "Program updated [X hours ago] — tap to refresh" if a newer version exists
- **"No program set yet" state**: shown with prompt "Contact your supervisor" (TMPL-003 EC-01)

**States:**
- **Empty state:** "No program set yet. Contact your supervisor." with supervisor contact option
- **Loading state:** Program loads in ≤ 1 second from cache; ≤ 2 seconds from network (TMPL-003 NFR); skeleton cards shown
- **Error state:** If not assigned to this child: "You are not assigned to this child. Contact your center admin." (TMPL-003 EC-02)
- **Offline state:** Full program text from local cache — hard offline requirement (TMPL-003 NFR); staleness banner shown with last sync timestamp

**Constraints:**
- Hard offline requirement: program must load without network in session rooms (TMPL-003 NFR)
- All target fields readable at system default font size on a 5.5-inch Android screen without horizontal scrolling
- 2-tap navigation from home screen confirmed in QA (TMPL-003 DoD)

---

## Developer Handoff

### Step-level technical summary

| Step | Data written | Data read | API / event | Offline behavior | Regulatory gate |
|---|---|---|---|---|---|
| 1 — Mark attendance | `sessions.attendance_status=Present`, `sessions.attendance_timestamp` | `sessions.{id}` | PATCH `/sessions/{id}/attendance` | Write to local queue; sync on restore | RBAC: Priya must be Primary Therapist or Co-Therapist on this child (MPM-001) |
| 2 — Open note creation | None written | `children.{id}.consent_status`, `children.{id}.program.active.targets` | GET `/children/{id}/consent`, GET `/children/{id}/program/active/targets` | Read consent from cache; targets from cache | ⚠️ DPDPA — consent must be Active; block if not; child health data access gate |
| 3 — Fill note form | Local form state only (not yet persisted) | Active program targets (from Step 2 cache) | None | Full form state held in local storage | None at this step |
| 4 — Save note | `session_notes: {session_id, child_id, therapist_id, goals_addressed[], mood, observations, incidents_flag, incidents_text, next_focus, status=Submitted, created_at}` | None | POST `/sessions/{id}/notes` | Write to local DB with `sync_status=pending`; background sync on connectivity restore | ⚠️ DPDPA — child health data written; consent gate must be Active; encrypted at rest (AES-256) and in transit (HTTPS/TLS 1.2+) |
| 5 — Background sync | `session_notes.sync_status=synced`, `session_notes.server_id` populated | None | POST `/notes/sync` (batch or individual) | Retry on connection restore; no data loss on app close (SNOTE-001 NFR) | RBAC: sync endpoint validates therapist-to-child assignment |
| 6 — Load review queue | None | `session_notes` for Dr. Sunita's caseload, filtered by `status=Submitted`, last 7 days | GET `/supervisor/notes/pending?supervisor_id={id}` | Last-cached queue readable offline; stale data indicator shown | RBAC: Supervisor role; caseload-scoped query — no cross-caseload access (SNOTE-002 DPDPA) |
| 7 — Open note detail | None | Full `session_notes.{id}` record | GET `/notes/{id}` | Previously loaded notes readable from cache | RBAC: Supervisor assigned to this child |
| 8 — Mark as reviewed | `session_notes.status=Reviewed`, `session_notes.reviewed_by={dr_sunita_id}`, `session_notes.reviewed_at` | None | PATCH `/notes/{id}` `{status: "reviewed"}` | Action queued offline; syncs on restore | RBAC: Supervisor role only |
| 9 — Co-sign | `session_notes.status=Co-signed`, `session_notes.cosigned_by={name+credential}`, `session_notes.cosigned_at`; audit trail entry | `profiles.{dr_sunita_id}.credential` | POST `/notes/{id}/cosign` | Blocked offline — requires connectivity (integrity requirement) | ⚠️ DPDPA — clinical record of minor; audit trail retained minimum 3 years (SNOTE-003 NFR); RBAC: Supervisor role |
| 11 — Open SOAP template | None | `soap_template` (embedded in app), `profiles.{dr_sunita_id}` | None (template is local); GET `/profiles/{id}` for author stamp | Template available offline (embedded) | ⚠️ DPDPA — health data of minor; consent Active required |
| 12 — Fill SOAP sections | Local form state | None | None | Full form state in local storage | None at this step |
| 13 — Save SOAP note | `clinical_notes: {child_id, author_id, author_credential, note_type=SOAP, subjective, objective, assessment, plan, status, created_at, version_id}` | None | POST `/children/{id}/clinical-notes` (draft or final) | Draft saves locally; final submit requires connectivity | ⚠️ DPDPA — child health data; consent Active required; access scoped to assigned clinical staff; encrypted at rest and in transit |
| 14 — Lock SOAP note | `clinical_notes.status=Locked`, audit trail entry | None | POST `/clinical-notes/{id}/lock` | Blocked offline | ⚠️ DPDPA — audit trail entry immutable; RBAC: Supervisor |
| 16 — Update program | `therapy_programs: new version record {child_id, version_number, targets[], prompt_levels, mastery_criteria, change_note, updated_by, updated_at}`; previous version retained | `therapy_programs.{id}.current` | PATCH `/children/{id}/program` (creates new version) | Draft save offline; sync on restore | ⚠️ DPDPA — child health data; RBAC: Supervisor or Director role; consent Active |
| 17 — Program update notification | Push notification record | None | Push notification service event (triggered by program version save) | Notification delivered on next connectivity restore | RBAC: notification sent only to staff assigned to this child |
| 18 — Priya views updated program | `therapy_programs` cached locally | `therapy_programs.{id}.current` (latest version) | GET `/children/{id}/program/active` | Cached locally for offline access; version staleness calculated from `updated_at` vs local cache timestamp | RBAC: Priya must be assigned to this child |
| 19 — Clinical timeline updated | None (populated from events written in prior steps) | All events for `child_id` from timeline aggregate view | GET `/children/{id}/timeline` | Previously loaded entries readable from cache | ⚠️ DPDPA — aggregated child health data; access scoped to assigned staff and supervisors |

**Key state transitions:**
- `session_notes` transitions: (none) → **Draft** (local) → **Submitted** (on sync) → **Reviewed** (Step 8) → **Co-signed** (Step 9, optional)
- `clinical_notes (SOAP)` transitions: (none) → **Draft** → **Final** (Step 13 submit) → **Locked** (Step 14, optional)
- `therapy_programs` transitions: **v1.0** → **v2.0** (new version created at Step 16; v1.0 retained in history)
- `program availability on Priya's device` transitions: **cached v1.0** → **stale v1.0 (banner shown)** → **cached v2.0** (after refresh at Step 18)

**Background jobs / async events triggered by this journey:**
- **Note sync job**: triggered when device connectivity restores after offline save (Step 4→5); completes when server confirms write and note status updates to Submitted
- **Push notification — program updated**: triggered immediately when Dr. Sunita saves a new program version (Step 16); delivered to all assigned therapists (including Priya)
- **Clinical timeline aggregation**: event records for note creation, SOAP creation, and program update are written to the timeline aggregate at each respective write step; no separate batch job required

**DPDPA compliance checkpoints:**
- Step 2: ⚠️ DPDPA — consent gate enforced before note creation screen opens; consent.status must = Active for this child
- Step 4: ⚠️ DPDPA — session note written contains child health data; encrypted at rest (AES-256); access scoped to assigned staff and supervisors; consent Active confirmed at write time
- Step 9: ⚠️ DPDPA — co-sign creates immutable clinical record; audit trail retained minimum 3 years post-event (SNOTE-003 NFR)
- Step 13: ⚠️ DPDPA — SOAP note written contains clinical assessment of a minor; consent Active confirmed; encrypted at rest and in transit; access scoped to clinical staff assigned to this child
- Step 16: ⚠️ DPDPA — therapy program is child health data; encrypted at rest; access scoped by RBAC (Supervisor and Director roles for write; all assigned staff for read)

---

## Cross-Journey Dependencies

| Depends on journey | Why | What breaks if missing |
|---|---|---|
| Journey 2: Child Enrollment & Intake | Child's EMR must exist (EMR-001), DPDPA consent must be confirmed (EMR-002), and Priya must be assigned to the care team (MPM-001) before any note can be created | Steps 2 and 4 are blocked by missing DPDPA consent gate; Step 3 goals multi-select has no targets to show without an active therapy program created in intake/program design |
| Journey 3: Scheduling & Attendance Management | Step 1 (attendance mark) is the pre-condition for this journey; session must exist and be marked Present | Without a confirmed attendance mark, "Add Note" may not be enabled (session record must exist — SNOTE-001 EC-01) |
| Journey 8: Progress Report Creation | All session notes created in this journey (Step 4) and SOAP notes (Step 13) are the primary data sources for Journey 8 progress report auto-population (REPORT-001); co-signed notes (Step 9) provide higher-confidence data to the report | Without session notes and SOAP notes accumulated from multiple Journey 6 instances, progress report auto-population in Journey 8 has no data to draw from |
| WhatsApp Session Summary (WA-006) | Session note (Step 4) is the prerequisite for sending a session summary to Meena via WhatsApp; summary fields are drawn from the "What we practiced" and "Try at home" fields in the session note | Without a session note, WA-006 shows "Session note not complete — summary fields will be blank" warning |

---

## ⚠️ Feature Factory Disclaimer

These flows were defined by document synthesis from competitive observation and story engineering — not by validated user research. Before committing design effort or engineering capacity, a real product thinker should ask:

**What we assumed but haven't validated:**
- [ASSUMPTION — NOT VALIDATED] Indian special educators (Priya) currently write or are willing to write structured post-session notes. This behavior may not exist in Indian centers today — the product may need to create this habit from scratch rather than digitize an existing one. (SNOTE epic disclaimer; Journey Map H-01 related)
- [ASSUMPTION — NOT VALIDATED] Dr. Sunita experiences reviewing session notes as a distinct, structured workflow — separate from reviewing raw trial data. In the current paper workflow, she may receive both together and not distinguish between "session note review" and "data review."
- [ASSUMPTION — NOT VALIDATED] Indian clinical supervisors are familiar with the SOAP note format. SOAP is a US/UK medical documentation standard. RCI training programs may use different structures. The SOAP section labels and prompts may need adaptation to Indian clinical vocabulary before adoption occurs. (SOAP epic disclaimer)
- [ASSUMPTION — NOT VALIDATED] Dr. Sunita will adopt platform-provided program templates over her existing Word document format. Template adoption depends entirely on the field structure matching her clinical mental model — which is trained in Indian RCI curricula, not US ABA frameworks. (TMPL epic disclaimer)
- [ASSUMPTION — NOT VALIDATED] Priya will check the updated program on her phone before her next session rather than relying on verbal instruction from Dr. Sunita. The "program on session screen" feature only delivers value if Priya adopts the behavior of consulting it.

**What a researcher would ask before building this:**
- Do Indian special educators currently write any structured post-session documentation at all? Observing 3–5 centers would reveal whether a session note feature is introducing a new behavior or digitizing an existing one — the design implications are very different.
- Does Dr. Sunita currently review session notes as a distinct task, or does she receive data and notes together informally? Understanding her actual review workflow would reveal whether a dedicated review queue is the right interface model or whether a per-child feed is more natural.
- Does Dr. Sunita know what a SOAP note is? A 10-minute concept test before building the SOAP template would reveal whether the four-section structure is intuitive or alien. If the format is unfamiliar, the labels need to change even if the underlying structure is sound.

**What the Product Consultant would challenge:**
- The SOAP note and program update sub-flows (Steps 11–17) are significant features added to what starts as a simple note-writing journey. If Priya adoption of session notes is not yet proven, building the full supervisor-side SOAP + program versioning workflow in the same sprint increases scope risk substantially. Consider building SNOTE-001 + SNOTE-002 (note creation and review queue) first, proving that therapists write notes, then adding co-sign and SOAP notes in a second iteration.
- The offline-first requirement is the highest technical risk in this journey — specifically the conflict resolution at Step 4 (offline save → sync → potential overwrite if note was also edited online). The last-write-wins approach in SNOTE-004 EC-02 is the simplest resolution but needs careful QA to avoid data loss.

**Risk level:**
- Session note creation (Steps 1–5): **Medium** — core behavioral assumption (Priya writes notes) unvalidated for India; technical risk is manageable (standard offline sync pattern)
- Supervisor review queue (Steps 6–9): **Medium** — depends entirely on Priya using step 1–5; if notes don't exist, this screen has no value
- SOAP note creation (Steps 11–14): **High** — SOAP format familiarity in Indian clinical training is unvalidated; format adaptation may be needed
- Program update + Priya notification (Steps 15–18): **Medium** — technically straightforward; adoption depends on Dr. Sunita using the program editor rather than continuing to use Word

Use the `/researcher` agent to validate session note behavior and SOAP format familiarity before sprint planning.
Use the `/product-consultant` agent to challenge whether the full supervisor review workflow should ship in v1 or be sequenced after note-writing adoption is confirmed.
Use the `/design-critique` agent to review the Note Creation screen and SOAP editor before prototyping — particularly the one-handed constraint for Priya and the section navigation pattern for Dr. Sunita.
