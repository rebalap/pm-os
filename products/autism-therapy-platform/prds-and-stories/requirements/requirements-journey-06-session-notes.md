# Requirements: Journey 6 — Session Notes / Clinical Notes

**Product:** Autism Therapy Platform (India)
**Journey:** Journey 6 — Session Notes / Clinical Notes
**MVP status:** ✅ IN SCOPE — MVP
**Author:** Mindless Product Owner Agent
**Date:** 2026-04-29
**Story prefix:** NOTE-
**Source documents:**
- `user-journeys/journey-06-session-notes-clinical-notes.md`
- `user-journeys/journey-map.md` (Part 2, Journey 6 section)

**Upstream dependencies:**
- Journey 0 (DPDPA Consent Management) — consent gate; must be Active before any note can be created
- Journey 2 (Intake & Enrollment) — child EMR must exist; Priya must be assigned to care team
- Journey 3 (Scheduling & Attendance Management) — session record must exist and be marked Present before "Add Note" is enabled

**Downstream dependencies:**
- Journey 8 (Progress Reports, deferred post-MVP) — session notes created here are the primary data source for report auto-population; note structure must be designed with this in mind from day one

---

## Epic: Session Notes and Supervisor Review

**Goal:** Enable Priya (Special Educator) to write structured post-session notes on her Android phone, and enable Dr. Sunita (Clinical Supervisor) to review, act on, and co-sign those notes — replacing the current WhatsApp voice-note and paper-file workflow with a secure, structured, and searchable clinical record.

**Target users:** Priya (primary note author); Dr. Sunita (reviewer, co-signer, SOAP note author)

**Copied from:** CentralReach (session notes + supervisor co-sign), Motivity (structured note templates, supervisor review queue), SimplePractice (SOAP note editor, draft persistence), Notate (offline-first data write, sync-on-restore)

**Definition of Done:**
- [ ] Priya can create a structured session note from a session detail screen in 4 taps or fewer from the home screen
- [ ] Notes save offline and sync without data loss when connectivity restores
- [ ] Notes are linked to the correct child, session date, therapist, and attendance record
- [ ] Dr. Sunita has a consolidated review queue scoped to her assigned caseload
- [ ] Dr. Sunita can mark notes as reviewed and optionally co-sign and lock them
- [ ] Dr. Sunita can write and submit a SOAP note linked to any child's clinical record
- [ ] All clinical data is encrypted at rest (AES-256) and in transit (HTTPS/TLS 1.2+)
- [ ] DPDPA consent gate enforced before any note creation screen opens
- [ ] Session note fields are structured to support future progress report auto-population (Journey 8)
- [ ] All features pass QA on minimum-spec Android (Redmi/Realme, 2GB RAM, Android 10+)

**Out of scope (this epic):**
- In-session trial-by-trial data collection (Journey 5 — out of scope, India MVP)
- Therapy program design and target management (Journey 4 — deferred post-MVP)
- Structured supervisor program update workflow (Journey 7 — deferred post-MVP)
- Progress report generation from session note data (Journey 8 — deferred post-MVP)
- Multi-language note templates (Phase 2+)

**[ASSUMPTION — NOT VALIDATED]** This epic assumes Indian special educators are willing to write structured digital post-session notes. Whether this behavior exists in Indian therapy centers has not been validated by primary research.

---

## Story NOTE-001: Post-Session Note Creation

**As a** Priya (Special Educator)
**I want to** open a structured note form from my session detail screen and record what happened in a session immediately after it ends
**So that** the clinical record of every session is documented in a consistent, searchable format that my supervisor can review without relying on my verbal recall

**Inspired by:** CentralReach session notes; Motivity post-session documentation screen

**Context:** Priya has just ended a session. The session is marked Present in the schedule (SCHED-004). She is on her low-end Android phone, possibly in a hallway, with approximately 10 minutes before her next child.

**Acceptance Criteria:**
- [ ] AC-01: Given a session is marked Present, when Priya taps "Add Note" on the Session Detail screen, the Note Creation screen opens in 1 second or less
- [ ] AC-02: Given the Note Creation screen opens, when the system checks DPDPA consent status for this child, if consent status is not Active the "Add Note" button is disabled with tooltip "Parental consent required before adding clinical records."
- [ ] AC-03: Given the Note Creation screen is open, the session date, session time, child name, and therapist name are pre-filled from the session record and are read-only
- [ ] AC-04: Given the Note Creation screen is open, when Priya taps the Goals Addressed field, a multi-select chip picker loads the active program targets for this child via GET `/children/{id}/program/active/targets`; if no active program exists, the field shows "No active targets — contact your supervisor" and remains optional
- [ ] AC-05: Given Priya has filled in Goals Addressed (at least one selection) and Child's Response / Mood (one of: Engaged / Partially Engaged / Dysregulated), the Save button becomes active
- [ ] AC-06: Given Priya taps Save with an active internet connection, a POST request is made to `/sessions/{id}/notes`; note status is set to Submitted; haptic feedback fires; Priya is returned to Session Detail with a "Note saved" confirmation banner
- [ ] AC-07: Given Priya taps Save with no internet connection, when the device has available storage, the note is written to device local storage with sync_status=pending; haptic feedback fires; a persistent banner shows "Saved offline — will sync when connected"; the note is not lost on app close
- [ ] AC-08: Given a note is saved offline, when internet connectivity is restored, the note syncs to the server automatically in the background; note status transitions to Submitted; Dr. Sunita's review queue is updated within 30 seconds of sync completion
- [ ] AC-09: Given the Note Creation screen is open, when Priya navigates away without saving, a confirmation dialog asks "Discard note?" with "Discard" and "Keep editing" options

**Edge Cases & Error States:**
- [ ] EC-01: Given a session is not marked Present, the "Add Note" button is disabled with tooltip "Mark attendance before adding a note"
- [ ] EC-02: Given Priya taps Save while offline and device storage is full, a full-screen error card shows "Could not save note — device storage full." No partial write occurs.
- [ ] EC-03: Given a note is in pending_sync state and the session record changes before sync, the sync fails gracefully with in-app notification: "Session note for [child name] on [date] could not be synced — session record changed."
- [ ] EC-04: Given Priya attempts to create a second note for the same session, the system blocks creation: "A note already exists for this session. Tap to view or edit it."

**Non-Functional Requirements:**
- Performance: Note Creation screen opens in 1 second or less; Goals chip picker loads from cache while network fetch runs in background
- Offline: Full form functionality without network; saves to device DB (not memory); syncs on restore; no data loss on app close
- Accessibility: All touch targets 44px minimum; haptic feedback on Save; Save button anchored at bottom reachable with thumb; one-handed operation achievable
- Privacy: ⚠️ DPDPA — session note contains child health data; encrypted at rest (AES-256) and in transit (HTTPS/TLS 1.2+); access scoped to assigned therapist and supervisors; consent gate enforced at screen open
- Future dependency: Goals Addressed, Child's Response/Mood, Key Observations, and Next Session Focus fields stored as discrete structured fields (not a single free-text blob) to enable Journey 8 auto-population

**Dependencies:**
- Blocked by: DPDPA-002 (consent Active), SCHED-004 (attendance mark Present), ENR-001 (Priya assigned to care team)
- Enables: NOTE-002, NOTE-003, NOTE-005

**Definition of Done:**
- [ ] All AC pass QA on Redmi/Realme 2GB RAM, Android 10+
- [ ] Offline save and sync verified
- [ ] DPDPA consent gate blocks creation when consent is not Active
- [ ] EC-02 (storage full) tested
- [ ] Code reviewed and merged

---

## Story NOTE-002: Note Template and Structured Fields

**As a** Priya (Special Educator)
**I want to** fill in a structured note template with predefined fields rather than a blank text box
**So that** my notes are consistent across sessions and contain the specific information Dr. Sunita needs

**Inspired by:** Motivity structured session note template; CentralReach note field library

**Acceptance Criteria:**
- [ ] AC-01: The following fields are present in this order: (1) Goals Addressed — multi-select chip picker; (2) Child's Response / Mood — single-select: Engaged / Partially Engaged / Dysregulated; (3) Key Observations — free text, 500-character limit with live counter; (4) Incidents or Behaviors of Concern — yes/no toggle; (5) Next Session Focus — free text, 200-character limit
- [ ] AC-02: Given Priya selects "Yes" on the Incidents toggle, an Incidents Detail free-text field expands below (300-character limit); required only if toggle is Yes
- [ ] AC-03: Given no Goals Addressed chips are selected, the Save button is disabled with hint "Select at least one goal to save this note"
- [ ] AC-04: Given no Child's Response / Mood option is selected, the Save button is disabled with hint "Select child's response to save this note"
- [ ] AC-05: Given Priya types beyond 500 characters in Key Observations, further input is blocked; counter turns red at 480 characters
- [ ] AC-06: Given Priya is typing in any free-text field and rotates the device or switches apps and returns, all entered text is preserved
- [ ] AC-07: The template structure is embedded in the app and available offline — no network fetch required
- [ ] AC-08: All note fields are stored as discrete database columns — Goals as array, Mood as enum, Incidents as boolean + text, Observations and Next Focus as text — not as a single serialized string

**Edge Cases & Error States:**
- [ ] EC-01: Given the active program has no targets, Goals picker shows "No active targets"; Priya can save by confirming "Save note without goals?"
- [ ] EC-02: Given the Goals chip picker fails to load, picker shows "Could not load targets — tap to retry"

**Non-Functional Requirements:**
- Performance: Template renders in 1 second or less from local cache
- Future dependency: All structured field values must be individually queryable by Journey 8 Progress Report engine

**Dependencies:**
- Blocked by: NOTE-001
- Enables: NOTE-003, Journey 8

**Definition of Done:**
- [ ] All AC pass QA on minimum-spec Android
- [ ] Fields stored as discrete DB columns confirmed in code review
- [ ] Offline template availability verified
- [ ] Code reviewed and merged

---

## Story NOTE-003: Supervisor Notes Review Queue

**As a** Dr. Sunita (Clinical Supervisor)
**I want to** see a consolidated list of all session notes submitted by my therapists, filtered to my assigned caseload
**So that** I can review every session note without chasing WhatsApp messages or walking to a paper file

**Inspired by:** CentralReach supervisor data review queue; SimplePractice notes inbox

**Acceptance Criteria:**
- [ ] AC-01: Given Dr. Sunita navigates to the Notes tab (Supervisor role), the queue displays all notes with status=Submitted scoped to her assigned caseload; notes outside her caseload are never visible
- [ ] AC-02: Default filter is Last 7 days; each row shows: child name, session date, therapist name, review status badge (Pending Review / Reviewed / Co-signed), first line of Key Observations as preview
- [ ] AC-03: Filter controls for: date range, child name, therapist name, review status; can be combined; state preserved during session
- [ ] AC-04: When queue contains no pending notes, empty state shows "No notes pending review — you are up to date"
- [ ] AC-05: Notes saved offline and synced show a "Synced from offline" chip on the row
- [ ] AC-06: Given Dr. Sunita has no internet connection, last-cached queue is displayed with a "Last synced [timestamp]" banner
- [ ] AC-07: Tapping any note row opens the Note Detail screen
- [ ] AC-08: The queue loads in 2 seconds or less on 4G; skeleton rows shown during load; pagination at 20 rows
- [ ] AC-09: Tapping a push notification deep-links directly to that note in the Note Detail screen

**Edge Cases & Error States:**
- [ ] EC-01: Given Dr. Sunita's role is not Supervisor, the review queue is not accessible
- [ ] EC-02: Given connectivity drops while viewing the queue, "Mark as reviewed" actions queue offline and sync on restore
- [ ] EC-03: Given a note is edited by Priya after Dr. Sunita has opened it, when the note re-enters the queue an "Edited" badge is shown and Dr. Sunita receives an in-app notification

**Non-Functional Requirements:**
- Privacy: ⚠️ DPDPA — queue scoped to assigned caseload; no cross-caseload access; enforced server-side (not UI-only)

**Dependencies:**
- Blocked by: NOTE-001, ENR-001 (caseload assignment)
- Enables: NOTE-004

**Definition of Done:**
- [ ] All AC pass QA on minimum-spec Android
- [ ] RBAC scoping verified: supervisor cannot see notes outside her caseload
- [ ] Offline queue cache and stale banner verified
- [ ] Code reviewed and merged

---

## Story NOTE-004: Supervisor Note Review — Mark as Reviewed and Co-Sign

**As a** Dr. Sunita (Clinical Supervisor)
**I want to** open a session note, read it in full, mark it as reviewed, and optionally co-sign and lock it
**So that** Priya knows her notes have been seen and the clinical record has a formal supervisory endorsement

**Inspired by:** CentralReach supervisor co-sign; Motivity note review workflow; SimplePractice note lock

**Context:** "Mark as reviewed" is a lightweight acknowledgement. "Co-sign and lock" is a formal clinical endorsement that makes the note immutable. Co-sign requires active connectivity — it cannot be done offline.

**Acceptance Criteria:**
- [ ] AC-01: Given Dr. Sunita opens a note, the Note Detail screen displays all fields in read-only mode: session metadata, Goals Addressed, Child's Response/Mood, Key Observations, Incidents, Next Session Focus
- [ ] AC-02: Given Dr. Sunita taps "Mark as reviewed", a PATCH is made to `/notes/{id}` with status=Reviewed; note is removed from Pending Review queue
- [ ] AC-03: Given Dr. Sunita taps "Co-sign and lock", a confirmation dialog shows: "Co-signing locks this note permanently. Proceed?"; on confirm, POST `/notes/{id}/cosign` is called; note status transitions to Co-signed; Dr. Sunita's name, credential, date, and time are stamped; an immutable audit trail entry is written
- [ ] AC-04: Given a note is co-signed and locked, when Priya opens the note, the Edit button is replaced with "View only — this note has been locked by [Dr. Sunita's name]"
- [ ] AC-05: Given a note is Reviewed but not co-signed, Priya can still edit it; if she edits, the "Edited" badge appears and the note re-enters the review queue

**Edge Cases & Error States:**
- [ ] EC-01: Given Dr. Sunita taps "Co-sign and lock" while offline, the action is blocked: "Co-signing requires an internet connection."
- [ ] EC-02: Given Priya edits the note between when Dr. Sunita opened it and when she taps "Mark as reviewed", an "Edited — note was updated after you opened it" banner is shown
- [ ] EC-03: Given the co-sign POST fails, the note is not co-signed; Dr. Sunita sees: "Co-sign failed — tap to retry. Your review has been saved."

**Non-Functional Requirements:**
- Offline: Mark as reviewed can queue offline; co-sign requires active connectivity (integrity requirement)
- Privacy: ⚠️ DPDPA — co-sign creates an immutable clinical record; audit trail retained minimum 3 years; RBAC: Supervisor role only for co-sign

**Dependencies:**
- Blocked by: NOTE-003
- Enables: NOTE-005, NOTE-006

**Definition of Done:**
- [ ] All AC pass QA on minimum-spec Android
- [ ] Co-sign blocked offline confirmed
- [ ] Audit trail entry verified in DB after co-sign
- [ ] Lock state: Priya's edit button replaced with view-only label confirmed
- [ ] Code reviewed and merged

---

## Story NOTE-005: Session Note History View

**As a** Dr. Sunita (Clinical Supervisor)
**I want to** view a chronological history of all session notes for a specific child
**So that** I can see patterns across sessions without scrolling through a paper file

**Inspired by:** CentralReach child-level data history; Motivity session timeline view

**Acceptance Criteria:**
- [ ] AC-01: Given Dr. Sunita navigates to a child's profile and taps the Session Notes tab, the note history loads sorted newest-first; each row shows: session date, therapist name, Child's Response/Mood badge, review status badge, first line of Key Observations
- [ ] AC-02: Date range filter available: Last 7 days, Last 30 days, Last 90 days, All time, Custom range; default is Last 30 days
- [ ] AC-03: Tapping a note row opens the full Note Detail screen in read-only mode
- [ ] AC-04: Co-signed and locked notes are read-only with a lock icon and "Co-signed by [name] on [date]"
- [ ] AC-05: Pagination applied at 20 entries per page
- [ ] AC-06: Given Dr. Sunita has no internet connection, cached note history entries are displayed with a "Last synced [timestamp]" banner

**Edge Cases & Error States:**
- [ ] EC-01: Given a child has no session notes, the tab shows "No session notes yet."
- [ ] EC-02: Given Rahul (Director role) accesses the note history, the full history is visible; Priya can only see notes for her assigned care team children

**Dependencies:**
- Blocked by: NOTE-001, NOTE-004
- Enables: NOTE-006

**Definition of Done:**
- [ ] All AC pass QA
- [ ] RBAC access scoping verified for Priya, Dr. Sunita, and Rahul roles
- [ ] Code reviewed and merged

---

## Story NOTE-006: SOAP Note Creation (Supervisor)

**As a** Dr. Sunita (Clinical Supervisor)
**I want to** write a structured SOAP note for a child after reviewing session notes
**So that** there is a formal supervisory clinical record linked to the child's EMR that captures my assessment and decisions

**Inspired by:** SimplePractice SOAP note editor; CentralReach supervisor clinical note; TheraNest structured note templates

**[ASSUMPTION — NOT VALIDATED]** SOAP note format familiarity among RCI-licensed Indian clinical supervisors is unconfirmed. Section labels may require adaptation to Indian clinical vocabulary.

**Acceptance Criteria:**
- [ ] AC-01: Given Dr. Sunita navigates to a child's profile and taps "Add Clinical Note", a type picker offers "Session Note" and "Supervisor Note (SOAP)"; tapping SOAP loads the editor in 1.5 seconds or less
- [ ] AC-02: The SOAP editor contains four sections: Subjective (therapist and parent reports), Objective (session attendance, goals addressed), Assessment (required), Plan (required)
- [ ] AC-03: Each section has a text area with ABA-specific guided placeholder text available offline (embedded in app)
- [ ] AC-04: When Dr. Sunita taps "Submit" with Assessment or Plan empty, inline validation fires; Submit does not make a server request
- [ ] AC-05: Given Dr. Sunita taps "Save Draft", the note is saved with status=Draft; no validation fires; "Draft saved" banner shown
- [ ] AC-06: Given Dr. Sunita taps "Submit" with both required fields filled, the note is saved with status=Final; Dr. Sunita's name, credential, date, and time are auto-stamped
- [ ] AC-07: Given Dr. Sunita navigates away without saving, a dialog asks "Save as draft?"; "Save as draft" writes a draft; "Discard" exits without saving
- [ ] AC-08: Given Dr. Sunita opens the SOAP editor while offline, the template loads from embedded app assets; draft saves work offline; submission requires connectivity

**Edge Cases & Error States:**
- [ ] EC-01: Given Dr. Sunita attempts to submit a SOAP note while offline, submit is blocked; banner: "Submitting a final note requires an internet connection. Your content has been saved as a draft."
- [ ] EC-02: Given a draft SOAP note exists for a child, a "Resume draft" banner is shown on the child profile
- [ ] EC-03: Given the SOAP editor is open and Dr. Sunita is inactive for 10 minutes, form state is auto-saved to local storage

**Non-Functional Requirements:**
- Privacy: ⚠️ DPDPA — SOAP note contains clinical assessment of a minor; encrypted at rest and in transit; RBAC: Supervisor role required

**Dependencies:**
- Blocked by: NOTE-005, DPDPA-002
- Enables: NOTE-007, Clinical Timeline

**Definition of Done:**
- [ ] All AC pass QA on minimum-spec Android and Chrome desktop
- [ ] Offline draft save and "submit blocked offline" behavior verified
- [ ] Author stamp auto-populated confirmed
- [ ] Code reviewed and merged

---

## Story NOTE-007: SOAP Note Lock

**As a** Dr. Sunita (Clinical Supervisor)
**I want to** lock a Final SOAP note to make it immutable
**So that** the clinical record is protected from modification after it has been formally completed

**Acceptance Criteria:**
- [ ] AC-01: Given a SOAP note has status=Final, the Note Detail screen shows a "Lock Note" button
- [ ] AC-02: Given Dr. Sunita taps "Lock Note", a confirmation dialog shows: "Locking this note is permanent. Proceed?"; on confirm, POST `/clinical-notes/{id}/lock` is called; audit trail entry written
- [ ] AC-03: Given a SOAP note is Locked, all text areas are read-only; "Edit" and "Lock" buttons are replaced with a lock icon and "Locked by [name] on [date/time]"
- [ ] AC-04: Given a SOAP note is Locked, no user can edit or delete it

**Edge Cases & Error States:**
- [ ] EC-01: Given Dr. Sunita taps "Lock Note" while offline, the action is blocked: "Locking a note requires an internet connection."
- [ ] EC-02: Given the lock POST fails, the note remains in Final (unlocked) status; "Lock failed — tap to retry"

**Dependencies:**
- Blocked by: NOTE-006 (SOAP note must exist with status=Final)

**Definition of Done:**
- [ ] All AC pass QA on minimum-spec Android
- [ ] Lock blocked offline confirmed
- [ ] Audit trail entry verified in DB
- [ ] Code reviewed and merged

---

## Story NOTE-008: Clinical Timeline

**As a** Dr. Sunita (Clinical Supervisor)
**I want to** see a chronological feed of all clinical events for a child — session notes, SOAP notes, program updates — in a single view
**So that** I have complete clinical context in one place without switching between tabs

**Inspired by:** CentralReach client data timeline; SimplePractice client activity feed

**Acceptance Criteria:**
- [ ] AC-01: Given Dr. Sunita navigates to a child's profile Timeline tab, all clinical events load via GET `/children/{id}/timeline`, sorted newest-first; each row shows: event type icon, event date and time, one-line summary
- [ ] AC-02: Filter control for event type (All / Session Notes / Supervisor Notes / Program Updates); default is All
- [ ] AC-03: Tapping a timeline event deep-links to the detail screen for that event in read-only mode
- [ ] AC-04: Soft-deleted events are excluded from normal view; Director-role users can enable "Show deleted items"
- [ ] AC-05: Given Dr. Sunita has no internet connection, previously loaded timeline entries remain readable with a "Last synced [timestamp]" banner

**Edge Cases & Error States:**
- [ ] EC-01: Given a child has no clinical events, the timeline shows "No clinical events yet."
- [ ] EC-02: Supervisors and directors read all events for children in their scope regardless of which therapist authored them

**Dependencies:**
- Blocked by: NOTE-001, NOTE-006

**Definition of Done:**
- [ ] All AC pass QA on minimum-spec Android
- [ ] Filter control works for each event type
- [ ] Code reviewed and merged

---

## Backlog Summary

| Story ID | Title | Primary Persona | Complexity | Priority | Blocked by |
|---|---|---|---|---|---|
| NOTE-001 | Post-Session Note Creation | Priya | L | P0 | DPDPA-002, SCHED-004, ENR-001 |
| NOTE-002 | Note Template and Structured Fields | Priya | M | P0 | NOTE-001 |
| NOTE-003 | Supervisor Notes Review Queue | Dr. Sunita | M | P0 | NOTE-001, ENR-001 |
| NOTE-004 | Supervisor Note Review — Mark as Reviewed and Co-Sign | Dr. Sunita | M | P0 | NOTE-003 |
| NOTE-005 | Session Note History View | Dr. Sunita | S | P1 | NOTE-001, NOTE-004 |
| NOTE-006 | SOAP Note Creation (Supervisor) | Dr. Sunita | L | P1 | NOTE-005, DPDPA-002 |
| NOTE-007 | SOAP Note Lock | Dr. Sunita | S | P1 | NOTE-006 |
| NOTE-008 | Clinical Timeline | Dr. Sunita, Rahul | M | P1 | NOTE-001, NOTE-006 |

**Sprint planning notes:**
- NOTE-001 and NOTE-002 should be built and tested together — they are one screen
- NOTE-004 is the payoff for Dr. Sunita — do not defer it if NOTE-003 ships
- NOTE-006 (SOAP) is the highest-complexity story; confirm SOAP format with a Dr. Sunita representative before development begins

---

## Pre-Build Decisions Required

| # | Decision | Options | Owner | Deadline |
|---|---|---|---|---|
| PBD-01 | Offline conflict resolution when note edited offline and also edited online before sync | (A) Last-write-wins. (B) Offline rejected if server version is newer. (C) Both saved — Dr. Sunita chooses. | PM + Engineering | Before NOTE-001 development starts |
| PBD-02 | SOAP note section labels adapted for Indian/RCI vocabulary or ship with standard SOAP labels as MVP | (A) Ship as-is. (B) Concept test with 2 Indian supervisors before building. | PM + Research | Before NOTE-006 development starts |
| PBD-03 | Can Priya edit a note after Dr. Sunita has marked it Reviewed (not co-signed)? | (A) Yes — note re-enters queue. (B) Reviewed creates a soft lock. | PM | Before NOTE-004 development starts |
| PBD-04 | Goals Addressed chip picker source: structured active program targets (Journey 4, deferred) or free-form goals? | Needs fallback design if Journey 4 data not available at MVP. | PM + Engineering | Before NOTE-002 development starts |
| PBD-05 | What is the minimum session note data structure that satisfies Journey 8 progress report auto-population queries? | Architecture decision — schema must be correct at NOTE-001 build time. | PM + Engineering | Before NOTE-001 schema is finalized |

---

## ⚠️ Feature Factory Disclaimer

These features and stories were defined by document synthesis and competitive observation — not by validated primary research with Indian therapy center staff.

**What we assumed but haven't validated:**
- [ASSUMPTION — NOT VALIDATED] Indian special educators (Priya) currently write structured post-session notes, or are willing to start. This is the core behavioral assumption. If Priya does not adopt note writing, Dr. Sunita's review queue has no value.
- [ASSUMPTION — NOT VALIDATED] Dr. Sunita reviews individual session notes as a distinct, structured workflow — not bundled with informal verbal debrief.
- [ASSUMPTION — NOT VALIDATED] Indian clinical supervisors are familiar enough with the SOAP note format to adopt it without training. SOAP is a US/UK medical documentation standard; RCI training may use different frameworks.
- [ASSUMPTION — NOT VALIDATED] The Goals Addressed multi-select chip picker can draw from structured active program targets. If Journey 4 is deferred and no structured target records exist, this field may need to degrade to free-text input.

**What a researcher would ask before building this:**
- Do special educators at Indian autism centers write any structured post-session documentation today? Observing 3–5 centers would reveal whether this epic is digitizing an existing behavior or introducing a new one.
- Does Dr. Sunita review session notes as a distinct task? A 45-minute contextual interview would reveal whether a dedicated review queue matches her mental model.
- Does Dr. Sunita know what a SOAP note is? A 10-minute concept test before NOTE-006 development would surface whether section labels need to be renamed.

**What the Product Consultant would challenge:**
- NOTE-006 (SOAP) and NOTE-007 (SOAP lock) depend on Priya adopting note writing first. If adoption is not confirmed by the time NOTE-003 ships, hold NOTE-006 and NOTE-007 in the backlog.
- PBD-01 (offline conflict resolution) must be resolved before development starts — getting this wrong means a clinical note is silently overwritten.

**Risk level:**
- NOTE-001, NOTE-002: Medium — core behavioral assumption (Priya writes notes) is unvalidated
- NOTE-003, NOTE-004: Medium — depends on NOTE-001 adoption; co-sign has zero tolerance for data integrity error
- NOTE-005: Low — straightforward read view once upstream notes exist
- NOTE-006: High — SOAP format familiarity in Indian clinical training is unvalidated
- NOTE-007: Low — mirrors session note co-sign technically
- NOTE-008: Low — aggregate read view from existing data

Use the `/researcher` agent to validate note-writing behavior (H-01, H-05) and SOAP format familiarity before committing NOTE-006 to a sprint.
Use the `/product-consultant` agent to challenge whether NOTE-006/007 should ship in the same release as NOTE-001/004.
