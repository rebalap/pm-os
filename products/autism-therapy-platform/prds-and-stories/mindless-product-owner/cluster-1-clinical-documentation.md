# Cluster 1: Clinical Documentation
**Product:** Autism Therapy Platform (India)
**Agent:** Mindless Product Owner
**Date:** 2026-04-16
**Cluster covers:** Session / Clinical Notes · SOAP Notes · Mental Health / Therapy Templates · EMR / EHR
**Explicitly OUT OF SCOPE for this cluster:** In-session trial-by-trial data collection (DTT / NET recording) — that is a separate cluster.
**Journey stage alignment:**
- EMR/EHR → Stage 2 (Intake & Onboarding) and Stage 3 (Assessment & Program Design)
- Mental health / therapy templates → Stage 3 (Assessment & Program Design)
- SOAP Notes → Stage 3 and Stage 5 (Supervisor Review & Program Updates)
- Session / Clinical Notes → Stage 5 (Supervisor Review) and Stage 6 (Progress Reporting)

> ⚠️ Nothing in this document is validated by primary user research. All features are derived from competitor observation, category norms, and journey map inference. Read the Feature Factory Disclaimer at the end before committing engineering capacity.

---

## Feature Inspiration: Clinical Documentation

> Evidence labels: ✅ Confirmed from product page / docs | 🔵 Inferred from marketing | 🔶 Speculated from category norms

| Feature | Competitor(s) | Prevalence | How it works | Evidence |
|---|---|---|---|---|
| Structured post-session notes (templated fields) | SimplePractice, Jane App, TheraNest, Hi Rasmus, Raven Health | Table stakes | Therapist completes a structured note after each session — typically fields for session duration, goals addressed, client response, next steps. Separate from in-session trial recording. | ✅ SimplePractice, Jane App documented; 🔵 Hi Rasmus, Raven Health |
| SOAP note format (Subjective / Objective / Assessment / Plan) | SimplePractice, Jane App, TheraNest, CentralReach | Table stakes in US mental health / allied health SaaS | Four-section structured note. Supervisor or senior clinician fills each section. Commonly required for licensing, supervision documentation, and insurance audits in US context. | ✅ SimplePractice, Jane App confirmed with SOAP template; 🔵 CentralReach |
| Free-form session note (unstructured) | PractiPal, TheraNest, SimplePractice | Table stakes (basic tier) | Text area for clinician to write whatever they want per session. No structure enforced. PractiPal offers this as its only note type. | ✅ PractiPal confirmed (free-form notes only) |
| Note locking / co-sign workflow | SimplePractice, CentralReach, Jane App | Differentiator (mid-market) | Supervisor can review and co-sign a note submitted by a junior therapist. Locked notes cannot be edited post-sign. Relevant for clinical supervision compliance. | ✅ SimplePractice, CentralReach documented; 🔵 Jane App |
| Reusable clinical templates (pre-built and custom) | SimplePractice, Jane App, CentralReach, TheraNest | Table stakes | Center or platform provides a library of note/program templates. Clinicians fill in fields rather than writing from scratch. CentralReach has ABA-specific templates (ABLLS-R, VB-MAPP). | ✅ CentralReach ABA templates; ✅ SimplePractice general therapy templates; 🔵 Jane App |
| ABA-specific therapy program templates | CentralReach, Motivity, Catalyst, Hi Rasmus | Table stakes in ABA tools; absent from Indian market | DTT program template, NET program template, behavior intervention plan template. Target-level structure: goal, prompt level, reinforcement schedule, mastery criteria. | ✅ CentralReach, Motivity; 🔵 Catalyst, Hi Rasmus |
| EMR / child health record (diagnosis, assessments, uploaded docs) | CentralReach, Hi Rasmus, SimplePractice, Jane App | Table stakes in full-stack platforms | Central record per client: demographic info, diagnosis codes, assessment history, therapy program versions, uploaded documents (prior reports, school records). | ✅ CentralReach, SimplePractice, Jane App; 🔵 Hi Rasmus |
| Document upload to client record | SimplePractice, Jane App, CentralReach, PractiPal | Table stakes | Clinician or admin uploads PDFs, images, or documents (prior reports, UDID card, school records) and attaches to child's record. | ✅ SimplePractice, Jane App, PractiPal |
| Clinical timeline / activity log per client | Hi Rasmus, CentralReach, Jane App | Differentiator (fewer tools have this well) | Chronological view of all clinical events for a child — sessions, notes, program updates, assessments, uploaded docs — in one scrollable feed. | 🔵 Hi Rasmus, CentralReach; 🔶 Jane App |
| AI-assisted session note generation | Raven Health | Differentiator (1–2 tools only, as of 2026) | AI generates a draft session note from session metadata (targets run, trial outcomes, duration). Clinician reviews and edits before saving. | 🔵 Raven Health (AI notes confirmed in marketing); 🔶 applicable to post-session summary use case |
| Progress note auto-population from session data | CentralReach, Motivity, Hi Rasmus | Differentiator in ABA tools | Progress report or session note auto-fills fields from trial data already captured — mastery percentages, targets addressed, sessions attended. Reduces manual re-entry. | 🔵 CentralReach, Motivity, Hi Rasmus |
| Consent and intake form as part of EMR | SimplePractice, Jane App, CentralReach | Table stakes (full-stack platforms) | Digital intake forms and consent documents stored in the child's record. Verifiable consent record for compliance purposes. | ✅ SimplePractice, Jane App; 🔵 CentralReach |

---

## Feature Brief: Session / Clinical Notes

**Inspired by:** SimplePractice, Jane App, TheraNest, Hi Rasmus, Raven Health, PractiPal
**Prevalence:** Table stakes — every full-stack therapy platform has this
**Target user:** Priya (Special Educator — writes note post-session); Dr. Sunita (Clinical Supervisor — reviews and co-signs)
**What it does:** Allows a therapist to complete a structured note after each session documenting what was worked on, the child's response, any incidents or behavioral observations, and next steps. Notes are attached to the session record and visible to the clinical supervisor. Replaces the current workflow of paper notes, WhatsApp messages to supervisors, and retrospective recollection.
**What "done" looks like:** Priya can complete a session note in under 3 minutes on an Android phone immediately after a session. Dr. Sunita can review all notes for her caseload in a single view and mark them as reviewed.

**[ASSUMPTION — NOT VALIDATED]** This feature is assumed to solve the post-session documentation gap for Priya and the delayed data review problem for Dr. Sunita. No primary research has confirmed that Indian special educators currently write structured post-session notes at all, or that Dr. Sunita experiences reviewing them as a distinct workflow from reviewing trial data. Validate before committing engineering capacity.

---

## Feature Brief: SOAP Notes

**Inspired by:** SimplePractice, Jane App, TheraNest, CentralReach
**Prevalence:** Table stakes in US allied health / mental health SaaS; absent from all Indian tools reviewed
**Target user:** Dr. Sunita (Clinical Supervisor — primary author); Rahul (Center Director — may use for compliance documentation)
**What it does:** Provides a structured four-section note format (Subjective / Objective / Assessment / Plan) for clinical supervisors to document supervision sessions, program reviews, and clinical rationale for program changes. Each section has guided prompts appropriate for ABA therapy with autism.
**What "done" looks like:** Dr. Sunita can open a child's record, create a SOAP note from a template, complete all four sections, and save it as part of the child's clinical record — in under 10 minutes, on a laptop or Android phone.

**[ASSUMPTION — NOT VALIDATED]** This feature is assumed to solve the supervisor's documentation burden and provide a structured record meeting RPWD Act 2016 individualized program documentation requirements. Whether Indian clinical supervisors use or recognize the SOAP format is unvalidated — Indian clinical training may not emphasize SOAP structure. Validate the format familiarity before locking SOAP as the required structure.

---

## Feature Brief: Mental Health / Therapy Templates

**Inspired by:** CentralReach (ABLLS-R, VB-MAPP, BIP templates), SimplePractice (therapy note templates), Motivity (program templates), Hi Rasmus (program design tools)
**Prevalence:** Table stakes in ABA-specific tools; absent from Indian market entirely
**Target user:** Dr. Sunita (Clinical Supervisor — creates and edits programs using templates); Priya (Special Educator — reads and uses program templates during sessions)
**What it does:** Provides a library of pre-built, reusable templates for autism/ABA workflows — including individualized therapy program templates (DTT, NET, behavior intervention plan), session note templates, assessment summary templates, and home program templates. Dr. Sunita selects a template, customizes it for the child, and saves a version to the child's record. Priya can access the current program template from her phone.
**What "done" looks like:** Dr. Sunita can draft a new child's therapy program in under 30 minutes using a template rather than starting from a blank Word document. Priya can access the current program on her phone in 1 tap from the session screen.

**[ASSUMPTION — NOT VALIDATED]** This feature is assumed to solve the program design-to-therapist handover gap (Journey Map BP-07) and the report-writing-from-scratch problem (H-17). Whether Dr. Sunita will adopt a platform-provided template structure rather than her own Word document format is unvalidated. Template adoption requires that the platform's structure matches her mental model of what a therapy program looks like.

---

## Feature Brief: EMR / EHR (Child Health Record)

**Inspired by:** CentralReach, Hi Rasmus, SimplePractice, Jane App
**Prevalence:** Table stakes in full-stack platforms; absent from Indian therapy tools
**Target user:** Rahul (Center Director / Admin — creates and maintains child records); Dr. Sunita (Clinical Supervisor — adds clinical content); Priya (reads program and session history)
**What it does:** Creates and maintains a structured health record per enrolled child, covering: demographic information, diagnosis and history, uploaded prior documents (assessment reports, school records, UDID card), therapy program version history, session history, clinical notes, and consent records. Serves as the single source of truth for each child across the center's staff.
**What "done" looks like:** When a new child is enrolled, Rahul or admin can create a complete record in under 10 minutes. Any staff member can access the current program and session history for any child on their caseload from their phone. All records are stored and transmitted in compliance with DPDPA 2023 consent requirements.

**[ASSUMPTION — NOT VALIDATED]** This feature is assumed to replace the paper file and Excel/WhatsApp patchwork used today. The core risk is that small centers may not have digitized any prior records — so the EMR starts empty and requires a migration effort that could block adoption. The DPDPA consent flow is a dependency that must be built before any child health data can be stored.

---

## Epic: Session / Clinical Notes

**Goal:** Priya can write a structured post-session note in under 3 minutes on Android, and Dr. Sunita can review all pending notes for her caseload in a single screen.
**Copied from:** SimplePractice, Jane App, TheraNest, Hi Rasmus, PractiPal
**Target user(s):** Priya (author), Dr. Sunita (reviewer / co-signer)
**Definition of Done:**
- Priya can create, complete, and save a session note from her Android phone with no more than 4 taps to reach the note screen
- Dr. Sunita has a queue view showing all notes awaiting her review
- Notes are attached to the correct session and child record
- Notes written offline are saved locally and sync to the server when connectivity restores
- All session notes storing child health data are gated behind confirmed DPDPA parental consent

**Out of scope (this epic):** In-session trial-by-trial recording; AI-generated note drafts (Phase 2); note export to PDF for parent sharing (covered in progress reporting epic); billing note integration

**[ASSUMPTION — NOT VALIDATED]** Indian special educators (Priya) currently write or are willing to write structured post-session notes. This behavior may not exist today in most centers — the product may need to create the habit, not just digitize it.

---

### Story SNOTE-001: Create a structured session note after completing a session

**As a** Priya (Special Educator)
**I want to** quickly complete a structured session note on my phone right after a session ends
**So that** my supervisor can see what happened in the session without me having to send a WhatsApp message or fill out a paper form

**Inspired by:** SimplePractice post-session note flow; PractiPal session note screen

**Context:** Priya has just finished a 45-minute session with a child. She is in the therapy room or hallway, next session may start in 10 minutes. She is using a low-to-mid-range Android phone (Redmi/Realme, Android 10+). Connectivity may be weak.

**Acceptance Criteria:**
- [ ] AC-01: Given Priya is on the session detail screen, when she taps "Add Note", the note creation screen opens in ≤ 1 second on minimum-spec Android (2GB RAM, Android 10+)
- [ ] AC-02: Given the note creation screen is open, the form presents these fields in order: Session date and time (pre-filled from session record), Therapist name (pre-filled), Goals addressed (multi-select from child's current program targets), Child's response/mood (structured options: Engaged / Partially engaged / Dysregulated, with optional free-text), Key observations (free text, max 500 characters), Incidents or behaviors of concern (yes/no toggle; if yes, free-text field appears), Next session focus (free text, max 200 characters)
- [ ] AC-03: Given all required fields are filled (Goals addressed + Child's response are required; all others optional), when Priya taps "Save", the note is saved and she receives haptic confirmation
- [ ] AC-04: Given connectivity is unavailable at save time, the note is saved locally to device storage and a banner reads "Saved offline — will sync when connected"
- [ ] AC-05: Given the note syncs to the server, the session record is updated and the note appears in Dr. Sunita's review queue within 30 seconds of sync completing
- [ ] AC-06: Given Priya attempts to leave the note screen with unsaved content, a confirmation dialog appears: "Discard this note?" with options Keep editing / Discard

**Edge Cases & Error States:**
- [ ] EC-01: If the session record is not yet created (session not logged), the note cannot be created — show inline error: "Create the session record first before adding a note"
- [ ] EC-02: If the child's program has no active targets, the Goals addressed field shows a placeholder: "No active targets — contact your supervisor" with a prompt to continue using free text
- [ ] EC-03: If the device runs out of storage during offline save, show an error: "Could not save note — device storage full. Free up space and try again." Do not silently lose data.
- [ ] EC-04: If Priya attempts to create a second note for the same session, the app warns: "A note already exists for this session. Edit the existing note?" — do not allow duplicate notes per session

**Non-Functional Requirements:**
- Performance: Note screen must load in ≤ 1 second on minimum-spec Android (2GB RAM, Android 10+, 4G or offline)
- Offline: Write locally when offline; sync on background restore; no data loss on app close
- Accessibility: Touch targets ≥ 44px on all interactive elements; haptic feedback on save; no audio-only confirmation
- Privacy: ⚠️ DPDPA — session notes contain child health data; the child's parental consent record must be in "Active" state before any note can be created or saved

**Dependencies:**
- Blocked by: CONSENT-001 (DPDPA parental consent flow must exist before health data can be written); SESSION-001 (Session record creation story — note must attach to a session)
- Enables: SNOTE-002 (supervisor review queue), SNOTE-003 (note co-sign), REPORT-001 (progress report auto-population)

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android (Redmi/Realme, 2GB RAM, Android 10+)
- [ ] Offline save and sync tested with airplane mode simulation
- [ ] DPDPA consent gate tested — note creation blocked when consent is not confirmed
- [ ] Edge cases EC-01 through EC-04 tested
- [ ] Code reviewed and merged

---

### Story SNOTE-002: Review pending session notes as a supervisor

**As a** Dr. Sunita (Clinical Supervisor)
**I want to** see all session notes submitted by my team in a single queue, sorted by child and date
**So that** I can review what happened across all sessions today or this week without chasing WhatsApp messages or paper sheets

**Inspired by:** SimplePractice note review; CentralReach supervisor dashboard; Hi Rasmus supervision tools

**Context:** Dr. Sunita is reviewing notes at the end of the day or start of the next day, on a laptop or Android phone. She manages 3–6 therapists delivering sessions to 15–25 children.

**Acceptance Criteria:**
- [ ] AC-01: Given Dr. Sunita is on the Notes screen, she sees a list of all session notes submitted in the last 7 days (default view), sorted by date descending, grouped by child name
- [ ] AC-02: Given she taps any note in the list, she sees the full note content including all fields Priya filled in, the session date and time, and the therapist's name
- [ ] AC-03: Given she has reviewed a note, she can tap "Mark as reviewed" and the note status changes from "Pending review" to "Reviewed" — the note is then removed from the default queue view
- [ ] AC-04: Given she filters by child name, the list shows only notes for that child, in chronological order
- [ ] AC-05: Given she filters by therapist name, the list shows only notes submitted by that therapist
- [ ] AC-06: Given a note was saved offline by Priya and has synced, it appears in the queue with a small indicator "Synced from offline"

**Edge Cases & Error States:**
- [ ] EC-01: If there are no pending notes, show empty state: "No notes pending review — you're up to date"
- [ ] EC-02: If a note was edited by Priya after Dr. Sunita already marked it as reviewed, the note re-enters the queue with an "Edited" badge
- [ ] EC-03: If Dr. Sunita's connectivity drops while reviewing, previously loaded notes remain readable; the "Mark as reviewed" action queues and syncs when connection restores

**Non-Functional Requirements:**
- Performance: Note queue must load in ≤ 2 seconds on 4G; ≤ 4 seconds on 2G/slow connection
- Offline: Note list readable if previously cached; "reviewed" status action queued offline
- Accessibility: Touch targets ≥ 44px; notes readable without zoom on standard Android display
- Privacy: ⚠️ DPDPA — Dr. Sunita can only view notes for children assigned to her caseload; no cross-caseload access without explicit admin grant

**Dependencies:**
- Blocked by: SNOTE-001 (notes must exist before they can be reviewed)
- Enables: SNOTE-003 (co-sign flow), REPORT-001 (progress reporting pulls from reviewed notes)

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android (Redmi/Realme, 2GB RAM, Android 10+) and Chrome desktop
- [ ] Caseload-scoped data access tested — Dr. Sunita cannot see notes outside her assigned children
- [ ] Edge cases tested
- [ ] Code reviewed and merged

---

### Story SNOTE-003: Co-sign and lock a session note

**As a** Dr. Sunita (Clinical Supervisor)
**I want to** co-sign a session note written by a junior therapist and lock it from further editing
**So that** the clinical record is tamper-proof and I have a documented supervisory sign-off for compliance purposes

**Inspired by:** SimplePractice co-sign workflow; CentralReach note locking; Jane App supervisor sign-off

**Context:** This is a compliance and clinical governance story. Co-signing creates an immutable record. Relevant for centers that have formal supervision structures or that produce documentation for external parties (RPWD Act compliance, school reports, UDID applications).

**Acceptance Criteria:**
- [ ] AC-01: Given Dr. Sunita is viewing a reviewed session note, she can tap "Co-sign and lock" — a confirmation dialog appears: "Co-signing locks this note permanently. It cannot be edited. Proceed?"
- [ ] AC-02: Given she confirms, the note is marked with her name, credential (as stored in her profile), date, and time of co-sign — displayed at the bottom of the note
- [ ] AC-03: Given a note is locked, Priya's "Edit" button is replaced with "View only — note is locked"
- [ ] AC-04: Given a note is locked, an admin with center director access can request an unlock by submitting a reason — the unlock request is logged in the note's audit trail
- [ ] AC-05: Given the co-sign action completes, the note status updates to "Co-signed" in the review queue

**Edge Cases & Error States:**
- [ ] EC-01: If Dr. Sunita attempts to co-sign a note she did not review (status still "Pending"), prompt her to mark it as reviewed first
- [ ] EC-02: If Priya edits a note that Dr. Sunita has already reviewed but not yet co-signed, Dr. Sunita receives an in-app notification: "Session note for [Child name] on [date] was edited"

**Non-Functional Requirements:**
- Performance: Co-sign action must complete and lock in ≤ 2 seconds
- Offline: Co-sign action must require active connectivity — do not allow offline co-signing (integrity risk)
- Privacy: ⚠️ DPDPA — co-sign creates a clinical record of a minor; audit trail of lock/unlock events must be retained for minimum 3 years
- Accessibility: Confirmation dialog must be dismissible without a secondary tap on first focus; touch targets ≥ 44px

**Dependencies:**
- Blocked by: SNOTE-001 (note creation), SNOTE-002 (review queue), PROFILE-001 (therapist credential profile — needed to stamp co-signer's name and credentials)
- Enables: REPORT-001 (progress report can pull from co-signed notes with higher confidence)

**Definition of Done:**
- [ ] All AC pass in QA
- [ ] Lock state prevents edit — verified in QA with both Priya and Dr. Sunita role sessions
- [ ] Audit trail entry created on co-sign — verified in database
- [ ] Code reviewed and merged

---

### Story SNOTE-004: Edit or delete a draft session note before submission

**As a** Priya (Special Educator)
**I want to** edit a session note I've written before my supervisor sees it, and delete it if I created it by mistake
**So that** I can correct errors without needing to ask my supervisor to make changes

**Inspired by:** Standard note draft management in SimplePractice, Jane App

**Context:** Priya may save a note while offline, then realize she made an error or filled in the wrong child. This is a basic data integrity story.

**Acceptance Criteria:**
- [ ] AC-01: Given a note is in "Draft" or "Submitted — pending review" state, Priya sees an "Edit" button when viewing the note
- [ ] AC-02: Given she taps Edit, the note form opens pre-filled with all previously saved content — she can modify any field and save
- [ ] AC-03: Given she saves the edited note, the updated content is reflected immediately; if Dr. Sunita had already loaded the note, she sees a "This note was recently edited" badge on next load
- [ ] AC-04: Given Priya wants to delete a note that has NOT been co-signed, she taps "Delete" — a confirmation dialog appears: "Delete this note? This cannot be undone."
- [ ] AC-05: Given she confirms deletion, the note is soft-deleted (marked as deleted in the database, not permanently removed) — it is no longer visible to Priya or Dr. Sunita in normal views, but remains in the audit trail accessible to Rahul

**Edge Cases & Error States:**
- [ ] EC-01: If Priya attempts to delete a note that Dr. Sunita has already co-signed, the delete button is hidden and replaced with "Locked — contact your supervisor to request a correction"
- [ ] EC-02: If the edit is made while offline, save locally; sync and overwrite server version on reconnect with a merge-safe approach (last-write-wins, timestamp-based)

**Non-Functional Requirements:**
- Offline: Edit and draft delete work offline; sync on reconnect
- Privacy: ⚠️ DPDPA — soft delete only; audit trail preserved; data not permanently destroyed without explicit data deletion request under DPDPA erasure provisions
- Accessibility: Touch targets ≥ 44px; destructive actions (delete) use a visually distinct color (red) and require a confirmation step

**Dependencies:**
- Blocked by: SNOTE-001
- Enables: None (housekeeping story)

**Definition of Done:**
- [ ] All AC pass in QA
- [ ] Soft delete confirmed — note not visible in UI but present in database with deleted flag
- [ ] Edit-after-co-sign block confirmed
- [ ] Code reviewed and merged

---

### Story SNOTE-005: View all session notes for a child in chronological order

**As a** Dr. Sunita (Clinical Supervisor)
**I want to** see the complete history of session notes for a specific child in date order
**So that** I can understand how the child has progressed over time and write a progress report without manually pulling paper files

**Inspired by:** CentralReach client record timeline; Hi Rasmus clinical history view; Jane App client notes history

**Context:** Dr. Sunita is preparing a quarterly progress report or reviewing a child's case after a period of absence. This is a read-only history story, used on laptop or Android.

**Acceptance Criteria:**
- [ ] AC-01: Given Dr. Sunita is on a child's profile, she can tap "Session Notes" and see a full list of all session notes for that child, sorted by date descending
- [ ] AC-02: Given she selects a date range filter (last 30 days / last 90 days / custom), the list updates to show only notes within that range
- [ ] AC-03: Given she taps any note in the history, the full note content is displayed in read-only mode
- [ ] AC-04: The list shows for each note entry: date, therapist name, review status (Pending / Reviewed / Co-signed), and the first line of the "Key observations" field as a preview
- [ ] AC-05: Given the list has more than 20 entries, results paginate in groups of 20 with a "Load more" button

**Edge Cases & Error States:**
- [ ] EC-01: If no notes exist yet for the child, show empty state: "No session notes yet for [Child name]. Notes will appear here after sessions are documented."
- [ ] EC-02: If a note was soft-deleted, it does not appear in this list — the audit trail view (admin only) shows deleted items

**Non-Functional Requirements:**
- Performance: List must load in ≤ 2 seconds for up to 100 notes; ≤ 4 seconds for larger histories
- Offline: Previously loaded note history is readable offline from cache
- Privacy: ⚠️ DPDPA — only staff with assigned access to this child's record can view note history

**Dependencies:**
- Blocked by: SNOTE-001, CHILD-PROFILE-001 (child profile / record must exist)
- Enables: REPORT-001 (progress report generation draws from this history)

**Definition of Done:**
- [ ] All AC pass in QA
- [ ] Access control tested — no cross-caseload access
- [ ] Pagination tested at 20+ note entries
- [ ] Code reviewed and merged

---

## Backlog: Session / Clinical Notes (SNOTE)

| Story ID | Title | Persona | Complexity | Priority | Blocked by |
|---|---|---|---|---|---|
| SNOTE-001 | Create a structured session note after a session | Priya | M | P0 | CONSENT-001, SESSION-001 |
| SNOTE-002 | Review pending session notes as a supervisor | Dr. Sunita | M | P0 | SNOTE-001 |
| SNOTE-003 | Co-sign and lock a session note | Dr. Sunita | M | P1 | SNOTE-001, SNOTE-002, PROFILE-001 |
| SNOTE-004 | Edit or delete a draft session note | Priya | S | P1 | SNOTE-001 |
| SNOTE-005 | View all session notes for a child in chronological order | Dr. Sunita | M | P1 | SNOTE-001, CHILD-PROFILE-001 |

---

## Epic: SOAP Notes

**Goal:** Dr. Sunita can write and save a structured SOAP note against a child's record for any clinical event — program review, supervision session, behavioral incident — using a template that guides each section, in under 10 minutes.
**Copied from:** SimplePractice, Jane App, TheraNest, CentralReach
**Target user(s):** Dr. Sunita (primary author); Rahul (read access for compliance purposes)
**Definition of Done:**
- Dr. Sunita can create a SOAP note from the child's profile in ≤ 3 taps
- All four sections (S/O/A/P) present with guided prompts relevant to autism/ABA therapy
- SOAP note is stored in the child's clinical record and linked to the relevant date
- Notes are exportable as PDF (for RPWD Act compliance documentation)
- Access limited to staff with clinical or admin roles

**Out of scope (this epic):** Auto-population of O section from trial data (Phase 2 enhancement); AI draft generation; billing code integration; SOAP notes in any language other than English (Phase 2)

**[ASSUMPTION — NOT VALIDATED]** Indian clinical supervisors use or are familiar with the SOAP note format. This is standard in US/UK allied health training but is not confirmed as part of Indian RCI-licensed training programs. The format name and section labels may need to be adapted to match Indian clinical training vocabulary. Validate this before locking section labels.

---

### Story SOAP-001: Create a SOAP note from a child's clinical record

**As a** Dr. Sunita (Clinical Supervisor)
**I want to** create a structured SOAP note for a child using a pre-built template with guided prompts for each section
**So that** I have a consistent clinical record of my supervisory observations and program decisions that meets documentation standards

**Inspired by:** SimplePractice SOAP note template; Jane App clinical notes; CentralReach supervision documentation

**Context:** Dr. Sunita is conducting a program review after reviewing two weeks of session data. She is on a laptop at the center or on an Android phone during a brief break.

**Acceptance Criteria:**
- [ ] AC-01: Given Dr. Sunita is on a child's profile, she can tap "Add Clinical Note" and select "SOAP Note" from a note type picker
- [ ] AC-02: Given the SOAP note template is open, it presents four labeled sections: **Subjective** (guided prompt: "What did the therapist, parent, or child report this period?"), **Objective** (guided prompt: "What data was observed — session attendance, targets worked, mastery percentages?"), **Assessment** (guided prompt: "What is your clinical interpretation of the child's progress?"), **Plan** (guided prompt: "What program changes, new targets, or actions are planned?")
- [ ] AC-03: Given she fills one or more sections and taps "Save Draft", the note is saved as a draft linked to the child's record and today's date — she can return and complete it later
- [ ] AC-04: Given she fills all required sections (Assessment and Plan are required; S and O are optional) and taps "Submit", the note status changes to "Final" and it appears in the child's clinical timeline
- [ ] AC-05: Given the note is in "Final" status, a "Lock" button is available — on tap, the note is locked and can no longer be edited (same lock mechanic as SNOTE-003)
- [ ] AC-06: Given the note is saved (draft or final), it is tagged with Dr. Sunita's name, credential, date, and time automatically

**Edge Cases & Error States:**
- [ ] EC-01: If Dr. Sunita leaves the SOAP note screen with content in any field and the note is unsaved, a dialog prompts: "Save as draft?" with options Save draft / Discard / Cancel
- [ ] EC-02: If she attempts to submit a note with Assessment and Plan blank, inline validation fires on both fields: "Assessment is required before submitting"
- [ ] EC-03: If connectivity drops during submission, the note saves as a draft locally with a banner: "Saved offline — will submit when connected"

**Non-Functional Requirements:**
- Performance: SOAP template must load in ≤ 1.5 seconds on minimum-spec Android
- Offline: Draft save works offline; final submission requires connectivity (same as co-sign)
- Accessibility: Each section label and its guided prompt are screen-reader readable; touch targets ≥ 44px; text areas must be scrollable within the screen without full-page scroll conflicts on Android
- Privacy: ⚠️ DPDPA — SOAP notes are child health data; parental consent must be active; notes are accessible only to clinical staff assigned to the child

**Dependencies:**
- Blocked by: CHILD-PROFILE-001 (child record must exist), CONSENT-001 (DPDPA consent gate), PROFILE-001 (author credential stored in profile)
- Enables: SOAP-002 (view history), SOAP-003 (export to PDF), REPORT-001 (progress report can reference SOAP plan section)

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android and Chrome desktop
- [ ] Draft save and return flow tested
- [ ] Lock after submit tested
- [ ] DPDPA gate tested
- [ ] Code reviewed and merged

---

### Story SOAP-002: View SOAP note history for a child

**As a** Dr. Sunita (Clinical Supervisor)
**I want to** see all SOAP notes I (and other supervisors) have written for a child in date order
**So that** I can review the clinical reasoning trail before writing a new note or starting a progress report

**Inspired by:** CentralReach clinical history; Jane App notes timeline

**Context:** Dr. Sunita is preparing a quarterly review and wants to see what was documented in the previous SOAP note before writing a new one.

**Acceptance Criteria:**
- [ ] AC-01: Given Dr. Sunita is on a child's clinical record, the "Clinical Notes" tab shows all SOAP notes (and other note types — see SNOTE-005) sorted by date descending
- [ ] AC-02: Each entry in the list shows: date, note type (SOAP), author name, status (Draft / Final / Locked), and the first sentence of the Assessment section as a preview
- [ ] AC-03: Given she taps a note, all four sections are displayed in full in read-only mode (for Locked or Final notes)
- [ ] AC-04: Given a note is in Draft status, she sees an "Edit" button alongside the note entry
- [ ] AC-05: The list can be filtered by note type (SOAP / Session note / All)

**Edge Cases & Error States:**
- [ ] EC-01: If no SOAP notes exist, show empty state: "No SOAP notes yet. Tap 'Add Clinical Note' to create the first one."
- [ ] EC-02: If a draft note exists from a previous session, a banner at the top of the list reads: "You have 1 unfinished draft — tap to continue"

**Non-Functional Requirements:**
- Offline: Previously loaded note list readable from cache
- Privacy: ⚠️ DPDPA — access scoped to staff with assigned access to this child

**Dependencies:**
- Blocked by: SOAP-001
- Enables: SOAP-003 (export), REPORT-001

**Definition of Done:**
- [ ] All AC pass in QA
- [ ] Draft banner tested when draft exists
- [ ] Filter by note type tested
- [ ] Code reviewed and merged

---

### Story SOAP-003: Export a SOAP note as a PDF

**As a** Dr. Sunita (Clinical Supervisor)
**I want to** export a finalized SOAP note as a PDF with the center's name and the child's name on the header
**So that** I can include it in compliance documentation for the RPWD Act or share it with external stakeholders such as a school or government agency

**Inspired by:** SimplePractice note export; Jane App document export; CentralReach report generation

**Context:** A family needs clinical documentation for a school inclusion application or UDID renewal. Dr. Sunita exports the SOAP note as a PDF to provide formal documentation.

**Acceptance Criteria:**
- [ ] AC-01: Given a SOAP note is in Final or Locked status, Dr. Sunita sees an "Export as PDF" button on the note detail screen
- [ ] AC-02: Given she taps Export, the PDF is generated with: center name and logo in the header, child's first name and record ID (not full name in the file name — privacy), note date, author name and credential, all four SOAP sections with section labels, and a footer reading "Generated by [Platform name] — Confidential clinical record"
- [ ] AC-03: Given the PDF is generated, it is offered as a download on Android (system share sheet) and as a browser download on desktop
- [ ] AC-04: Draft notes cannot be exported — the Export button is hidden on draft status notes

**Edge Cases & Error States:**
- [ ] EC-01: If PDF generation fails (server error), show an error: "Could not generate PDF — try again. If this persists, contact support."
- [ ] EC-02: If the note is locked and export is requested on a slow connection, show a loading indicator; do not timeout silently

**Non-Functional Requirements:**
- Performance: PDF generation must complete in ≤ 5 seconds for a standard note
- Privacy: ⚠️ DPDPA — exported PDF contains child health data; the export action is logged in the child's audit trail with actor, timestamp, and file ID
- Offline: Export requires connectivity — show "Export requires an internet connection" if offline

**Dependencies:**
- Blocked by: SOAP-001 (note must exist and be Final/Locked)
- Enables: None (terminal output action)

**Definition of Done:**
- [ ] All AC pass in QA
- [ ] PDF output inspected manually — all sections, header, footer render correctly
- [ ] Export blocked for draft notes confirmed
- [ ] Audit log entry created on export — verified in database
- [ ] Code reviewed and merged

---

### Story SOAP-004: Add structured prompts to each SOAP section for autism/ABA context

**As a** Dr. Sunita (Clinical Supervisor)
**I want to** see guided prompts within each SOAP section that are specific to autism therapy and ABA (not generic medical SOAP)
**So that** I don't have to figure out what to write in each section — the prompts tell me what clinical information belongs where

**Inspired by:** CentralReach ABA-specific documentation; SimplePractice specialty-specific templates

**Context:** This is a content and UX story — not a data structure story. The SOAP form already exists (SOAP-001); this story defines what the prompts say.

**Acceptance Criteria:**
- [ ] AC-01: Subjective section prompt reads: "What did the therapist, parent, or school report this period? Include the child's mood, engagement patterns, and any parent-reported changes at home."
- [ ] AC-02: Objective section prompt reads: "What session data was observed this period? Include: number of sessions attended, targets addressed, mastery % for key targets, and any behavioral incident data."
- [ ] AC-03: Assessment section prompt reads: "Based on session data and observations, what is your clinical interpretation? Is the child on track, plateauing, or regressing? What is driving the pattern?"
- [ ] AC-04: Plan section prompt reads: "What clinical actions will be taken? Include: program changes (new targets, modified procedures, prompt fading), staff instructions, parent recommendations, and next review date."
- [ ] AC-05: Each prompt text is displayed as placeholder/ghost text inside the input area — it disappears when the user starts typing and does not appear in the saved note content

**Edge Cases & Error States:**
- [ ] EC-01: Prompt text must not be included in the saved note if the user does not type anything in a section (do not save the placeholder as content)

**Non-Functional Requirements:**
- Accessibility: Placeholder text meets WCAG AA contrast ratio for placeholder text (minimum 4.5:1 against field background)
- Offline: Prompt text is part of the template, not fetched from the server — available offline

**Dependencies:**
- Blocked by: SOAP-001
- Enables: None (content enhancement to existing form)

**Definition of Done:**
- [ ] All AC pass in QA — each section prompt verified correct
- [ ] Placeholder text does not save as content — verified in database
- [ ] Contrast ratio of placeholder text verified
- [ ] Code reviewed and merged

---

## Backlog: SOAP Notes (SOAP)

| Story ID | Title | Persona | Complexity | Priority | Blocked by |
|---|---|---|---|---|---|
| SOAP-001 | Create a SOAP note from a child's clinical record | Dr. Sunita | M | P0 | CHILD-PROFILE-001, CONSENT-001, PROFILE-001 |
| SOAP-002 | View SOAP note history for a child | Dr. Sunita | S | P0 | SOAP-001 |
| SOAP-003 | Export a SOAP note as a PDF | Dr. Sunita | M | P1 | SOAP-001 |
| SOAP-004 | Add ABA-specific guided prompts to each SOAP section | Dr. Sunita | S | P1 | SOAP-001 |

---

## Epic: Mental Health / Therapy Templates

**Goal:** Dr. Sunita can create a complete, individualized therapy program for a new child in under 30 minutes by selecting from a library of pre-built ABA/autism templates, customizing target details, and publishing it to Priya's session screen — replacing the current blank-Word-document workflow.
**Copied from:** CentralReach (ABA curriculum templates, ABLLS-R, VB-MAPP structure), Motivity (program template management), Hi Rasmus (program design tools), SimplePractice (general therapy note templates)
**Target user(s):** Dr. Sunita (creates and manages templates); Priya (reads and uses the active program during sessions)
**Definition of Done:**
- Platform includes ≥ 5 pre-built templates relevant to autism/ABA: DTT program, NET program, Behavior Intervention Plan (BIP), Session Summary, Home Program
- Dr. Sunita can customize any template and save a child-specific version to the child's record
- Priya can access the current active program for any child on her caseload in ≤ 2 taps
- Template versions are tracked — each save creates a new version; previous versions remain accessible
- Templates and child programs are accessible offline (read-only)

**Out of scope (this epic):** ABLLS-R or VB-MAPP full curriculum libraries (Phase 2 — licensing complexity); AI-generated program suggestions; template sharing across centers (multi-tenant, Phase 2); translation to Hindi or regional languages (Phase 2)

**[ASSUMPTION — NOT VALIDATED]** Dr. Sunita will use platform-provided template structures rather than her own Word document formats. Template adoption depends entirely on the platform's structure matching her clinical mental model. If the templates do not match how she was trained to write programs, she will ignore them and continue using Word. Validate template structure against 3–5 actual program documents from Indian centers before finalizing field definitions.

---

### Story TMPL-001: Select and customize a pre-built therapy program template for a child

**As a** Dr. Sunita (Clinical Supervisor)
**I want to** choose a pre-built ABA therapy program template (e.g., DTT program, NET program, BIP) and customize it with a specific child's targets, prompt levels, and reinforcement schedule
**So that** I can create a complete, structured therapy program for a new child in under 30 minutes instead of writing it from scratch in Word

**Inspired by:** CentralReach treatment plan templates; Motivity program creation; Hi Rasmus program design

**Context:** Dr. Sunita is designing a program for a newly assessed child. She is at the center, on a laptop or Android phone. The child's intake record and assessment summary are already in the system.

**Acceptance Criteria:**
- [ ] AC-01: Given Dr. Sunita is on a child's profile and the "Therapy Program" tab is selected, she sees a "Create New Program" button; tapping it opens a template picker showing ≥ 5 pre-built templates: (1) DTT Skill Program, (2) NET Activity Program, (3) Behavior Intervention Plan, (4) Session Summary Template, (5) Home Program Template
- [ ] AC-02: Given she selects a template (e.g., DTT Skill Program), the program creation form opens pre-filled with the template structure — she can edit all fields; pre-filled fields include: Program name, Domain (Communication / Social / Adaptive / Cognitive / Motor / Maladaptive Behavior), Teaching method (DTT / NET / Other), Target behavior description, Baseline, Prompt level (Full Physical / Partial Physical / Gestural / Verbal / Independent), Reinforcement schedule (description), Mastery criterion (e.g., "4/5 correct across 3 consecutive sessions"), Teaching notes (free text)
- [ ] AC-03: Given she completes the form and taps "Save Program", the program is saved as version 1.0 against the child's record with a timestamp and her name
- [ ] AC-04: The program immediately appears in Priya's session screen for that child under "Active Program" after Dr. Sunita saves it
- [ ] AC-05: Given she wants to add multiple skill targets to one program, she can tap "Add another target" and the target block repeats — up to 20 targets per program

**Edge Cases & Error States:**
- [ ] EC-01: If she attempts to save a program with no targets filled in (all target description fields empty), show inline validation: "Add at least one target before saving"
- [ ] EC-02: If Priya is currently in an active session when the program is updated by Dr. Sunita, Priya's session screen shows the previous version until she refreshes; a banner on Priya's screen reads: "Program updated — tap to refresh"
- [ ] EC-03: If the child has no confirmed DPDPA consent, the "Create Program" button is disabled with a tooltip: "Parental consent required before adding clinical records"

**Non-Functional Requirements:**
- Performance: Template picker must load in ≤ 1 second; program form in ≤ 1.5 seconds on minimum-spec Android
- Offline: Saved programs are cached and readable offline by Priya; Dr. Sunita can draft a program offline and sync on reconnect
- Accessibility: Touch targets ≥ 44px; "Add another target" button reachable without scrolling to page bottom on standard Android screen (≥ 5.5 inch)
- Privacy: ⚠️ DPDPA — therapy programs are child health data; consent gate required before creation

**Dependencies:**
- Blocked by: CHILD-PROFILE-001, CONSENT-001, PROFILE-001
- Enables: TMPL-002 (version history), TMPL-003 (program access for Priya), TMPL-004 (home program), SNOTE-001 (session note "Goals addressed" field references active program targets)

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android and Chrome desktop
- [ ] All 5 pre-built templates present in template picker and load correctly
- [ ] Program visible in Priya's session screen immediately after save — verified in end-to-end test with two active role sessions
- [ ] Target count limit (20) tested
- [ ] DPDPA consent gate tested
- [ ] Code reviewed and merged

---

### Story TMPL-002: View therapy program version history for a child

**As a** Dr. Sunita (Clinical Supervisor)
**I want to** see all previous versions of a child's therapy program, with timestamps and change notes
**So that** I can understand how the program has evolved over time and explain clinical decisions to parents or external reviewers

**Inspired by:** CentralReach program version history; Hi Rasmus program update tracking

**Context:** A child has been in therapy for 6 months. Dr. Sunita is preparing a progress report or responding to a parent's question about why a particular target was removed.

**Acceptance Criteria:**
- [ ] AC-01: Given Dr. Sunita is on the Therapy Program tab, she sees a "Version history" link showing the count of saved versions (e.g., "Version history — 4 versions")
- [ ] AC-02: Given she taps Version history, a list shows all program versions in reverse chronological order: version number, date saved, saved by (name), and an optional "Change note" (free text the editor can add at save time)
- [ ] AC-03: Given she taps any version in the list, the full program as it was at that version is displayed in read-only mode
- [ ] AC-04: The current version is clearly labeled "Current — v4.0" at the top of the version list
- [ ] AC-05: At save time (TMPL-001), Dr. Sunita can optionally add a change note (free text, max 200 characters) — e.g., "Removed target 3 — mastered. Added NET social targets per parent feedback."

**Edge Cases & Error States:**
- [ ] EC-01: If only one version exists, show: "Version 1.0 — current. No previous versions."
- [ ] EC-02: If a program is accidentally overwritten, the previous version remains accessible in version history — data is never permanently lost via a save action

**Non-Functional Requirements:**
- Offline: Version history list readable from cache if previously loaded
- Privacy: ⚠️ DPDPA — version history is part of the child's clinical record; access scoped to assigned staff

**Dependencies:**
- Blocked by: TMPL-001
- Enables: None directly (read-only view)

**Definition of Done:**
- [ ] All AC pass in QA
- [ ] Version increment on each save confirmed — verified in database
- [ ] Previous version read-only access tested
- [ ] Code reviewed and merged

---

### Story TMPL-003: Access the active therapy program from the session screen

**As a** Priya (Special Educator)
**I want to** open the current therapy program for a child I'm about to see, from my session screen, in ≤ 2 taps
**So that** I know exactly what targets to work on, at what prompt level, before the session starts — without needing to ask my supervisor

**Inspired by:** Motivity session setup; Catalyst session screen; Hi Rasmus therapist-facing program view

**Context:** Priya is about to start a session. She is outside the session room, on her Android phone. She has 2–3 minutes to review the program before the child arrives.

**Acceptance Criteria:**
- [ ] AC-01: Given Priya is on her session screen for a specific child, she sees a "Today's Program" card showing the program name and a "View full program" button — reachable in ≤ 2 taps from the app home screen
- [ ] AC-02: Given she taps "View full program", all current targets are displayed: target name, teaching method, current prompt level, reinforcement schedule, and mastery criterion — in a read-only, scrollable list
- [ ] AC-03: Given connectivity is unavailable, the program loads from local cache — the last synced version is shown with a banner: "Showing cached program — last synced [date/time]"
- [ ] AC-04: If Dr. Sunita has updated the program since Priya last loaded it, a banner reads: "Program updated [X hours/days ago] — tap to refresh" on the Today's Program card

**Edge Cases & Error States:**
- [ ] EC-01: If no program has been created for this child yet, show: "No program set yet. Contact your supervisor."
- [ ] EC-02: If Priya is not assigned to this child's caseload, she cannot access the program — show: "You are not assigned to this child. Contact your center admin."

**Non-Functional Requirements:**
- Performance: Program view must load in ≤ 1 second from cache; ≤ 2 seconds from network on 4G
- Offline: Full program text available from cache — this is a hard offline requirement (Priya may enter session room with no connectivity)
- Accessibility: Touch targets ≥ 44px; all target fields readable at system default font size on a 5.5-inch Android screen without horizontal scrolling

**Dependencies:**
- Blocked by: TMPL-001 (program must exist), SESSION-001 (session screen must exist)
- Enables: SNOTE-001 (Goals addressed multi-select references active program targets)

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android (Redmi/Realme, 2GB RAM, Android 10+)
- [ ] Offline load from cache tested with airplane mode — program loads without network
- [ ] 2-tap navigation path from home screen to program view confirmed in QA
- [ ] Code reviewed and merged

---

### Story TMPL-004: Create and assign a home program from a template

**As a** Dr. Sunita (Clinical Supervisor)
**I want to** create a simple home program document for a child by selecting targets from their therapy program and adding parent-friendly instructions
**So that** Meena receives clear, written guidance on what to practice at home — not just verbal instructions she may forget

**Inspired by:** Hi Rasmus home program feature; CentralReach caregiver-facing content; SimplePractice treatment summary

**Context:** At the end of a program review or progress report cycle, Dr. Sunita creates a home program that Meena can read and follow. This document must be in plain language, not clinical terminology.

**Acceptance Criteria:**
- [ ] AC-01: Given Dr. Sunita is on the Therapy Program tab, she sees a "Generate Home Program" button
- [ ] AC-02: Given she taps it, a simplified form opens pre-filled from the active therapy program — she selects which targets to include (not all clinical targets are appropriate for home practice; she checks the ones to include)
- [ ] AC-03: For each selected target, she can write a "Parent-friendly instruction" field (free text, max 300 characters) — e.g., "When Arjun asks for something with a point, help him say the word. Repeat 5 times during snack time."
- [ ] AC-04: Given she saves the home program, it is stored in the child's record and timestamped
- [ ] AC-05: The home program is shareable as a PDF (same export mechanic as SOAP-003) — with the center name, child's first name, and date on the header

**Edge Cases & Error States:**
- [ ] EC-01: If no active therapy program exists for the child, show: "Create a therapy program first before generating a home program"
- [ ] EC-02: If she selects no targets (deselects all), show inline validation: "Select at least one target for the home program"

**Non-Functional Requirements:**
- Privacy: ⚠️ DPDPA — home program PDF contains child health data; export action logged in audit trail
- Accessibility: Parent-friendly instruction fields have sufficient character count indicators visible
- Offline: Home program draft saves locally; PDF export requires connectivity

**Dependencies:**
- Blocked by: TMPL-001 (active therapy program must exist), SOAP-003 (PDF export mechanic reused here)
- Enables: PARENT-001 (parent portal can display the home program)

**Definition of Done:**
- [ ] All AC pass in QA
- [ ] PDF output inspected — center name, child first name, date, parent instructions render correctly
- [ ] Target selection tested — deselect-all validation fires
- [ ] Code reviewed and merged

---

### Story TMPL-005: Build a custom note or program template (center-level)

**As a** Rahul (Center Director)
**I want to** create a custom template for session notes or program documents that matches how my center already documents therapy
**So that** my staff don't have to adapt to a rigid external format — they use a structure that matches their training and existing practice

**Inspired by:** SimplePractice custom intake form builder; Jane App custom form templates; CentralReach configurable program templates

**Context:** Rahul's center uses a specific session note format they developed over years of practice. He wants to replicate it in the platform rather than forcing therapists to learn a new structure.

**Acceptance Criteria:**
- [ ] AC-01: Given Rahul is in Settings > Templates, he sees a "Create custom template" button
- [ ] AC-02: Given he creates a template, he can add: a template name, a template type (Session Note / Program Document / SOAP Note variant / Home Program), and up to 15 custom fields of the following types: Short text, Long text (textarea), Number, Date, Dropdown (he defines the options), Yes/No toggle, Section header (non-input, for visual grouping)
- [ ] AC-03: Given he saves the template, it appears alongside the platform's pre-built templates in the template picker for all staff in his center
- [ ] AC-04: Given he deactivates a template, it no longer appears in the picker — but existing notes/programs created using that template are not affected
- [ ] AC-05: Custom templates are center-scoped — they do not appear in any other center's template picker

**Edge Cases & Error States:**
- [ ] EC-01: If he attempts to create a template with no fields (empty), show validation: "Add at least one field before saving"
- [ ] EC-02: If a custom template name duplicates an existing template name, show inline error: "A template with this name already exists. Choose a different name."

**Non-Functional Requirements:**
- Performance: Template builder must load in ≤ 2 seconds on desktop; field add/remove interactions instantaneous
- Offline: Template builder requires connectivity (admin function, not session-time)
- Accessibility: Field type picker must be keyboard navigable on desktop

**Dependencies:**
- Blocked by: TMPL-001 (base template system must exist)
- Enables: No direct dependency — standalone enhancement

**Definition of Done:**
- [ ] All AC pass in QA
- [ ] Custom template appears in picker for all center staff — not visible to other centers (multi-tenancy verified)
- [ ] Deactivate template does not affect existing notes using that template — verified in QA
- [ ] Code reviewed and merged

---

## Backlog: Mental Health / Therapy Templates (TMPL)

| Story ID | Title | Persona | Complexity | Priority | Blocked by |
|---|---|---|---|---|---|
| TMPL-001 | Select and customize a pre-built therapy program template | Dr. Sunita | L | P0 | CHILD-PROFILE-001, CONSENT-001 |
| TMPL-002 | View therapy program version history | Dr. Sunita | M | P1 | TMPL-001 |
| TMPL-003 | Access active therapy program from session screen | Priya | M | P0 | TMPL-001, SESSION-001 |
| TMPL-004 | Create and assign a home program from a template | Dr. Sunita | M | P1 | TMPL-001, SOAP-003 |
| TMPL-005 | Build a custom note or program template (center-level) | Rahul | L | P2 | TMPL-001 |

---

## Epic: EMR / EHR (Child Health Record)

**Goal:** Every enrolled child has a single, structured digital health record in the platform — covering demographics, diagnosis history, uploaded documents, consent status, therapy program history, session history, and clinical notes — replacing the paper file and Excel patchwork used today.
**Copied from:** CentralReach (client record), Hi Rasmus (child profile + clinical history), SimplePractice (client record + file uploads), Jane App (EMR), PractiPal (basic client record)
**Target user(s):** Rahul (creates and maintains records, admin); Dr. Sunita (adds clinical content, reads full record); Priya (read-only access to relevant program and session history)
**Definition of Done:**
- Rahul (or admin) can create a complete new child record in ≤ 10 minutes
- All four record sections are populated: Demographics, Clinical history, Documents, Consent
- DPDPA parental consent is captured and stored as a verifiable record before any health data is added
- Priya can access any child record assigned to her caseload in ≤ 2 taps from the home screen
- All records are encrypted at rest and in transit; access is role-scoped
- The system supports uploading and viewing PDFs, images, and standard document formats

**Out of scope (this epic):** Electronic prescriptions; insurance claims; UDID auto-generation (Phase 2); integration with external hospital EMR systems (Phase 2); multi-center record sharing (Phase 2); biometric authentication

**[ASSUMPTION — NOT VALIDATED]** Small Indian therapy centers will create and maintain digital health records if the platform makes it easy enough. The key risk is onboarding inertia — centers have years of paper files and no forcing function to digitize them. Whether Rahul will invest time in data entry at enrollment is unvalidated. The product may need to design for incremental record completion (minimum required fields at creation, optional fields filled over time) to avoid abandonment on first use.

---

### Story EMR-001: Create a new child health record at enrollment

**As a** Rahul (Center Director / Admin)
**I want to** create a complete digital health record for a newly enrolled child by filling in a structured intake form
**So that** all child information is in one place from day one, accessible to all authorized staff, instead of scattered across paper files and WhatsApp

**Inspired by:** SimplePractice new client intake; Jane App patient onboarding; CentralReach client creation; PractiPal client record

**Context:** A family has agreed to enroll. Rahul or admin staff sit down with the family to complete the intake. This may happen on a laptop at the center or on an Android phone if no laptop is available.

**Acceptance Criteria:**
- [ ] AC-01: Given Rahul is logged in as admin or center director, he can tap "Add New Child" from the home screen or children list
- [ ] AC-02: The intake form is organized into sections, and only the following fields are required at creation (all others are optional and can be completed later): Child's first name (required), Date of birth (required), Primary diagnosis (required — dropdown: Autism Spectrum Disorder / ASD with intellectual disability / ADHD / Cerebral Palsy / Multiple disabilities / Other), Parent/guardian name (required), Parent/guardian mobile number (required)
- [ ] AC-03: The following fields are optional at creation but available in the full form: Child's full name, Gender, Address, Second parent/guardian name and number, Preferred language at home (dropdown: English / Hindi / Tamil / Telugu / Kannada / Other), Diagnosis date, Diagnosing doctor/hospital, Co-occurring conditions (multi-select), Prior therapy history (yes/no + free text), UDID number and expiry date, School name and class (if applicable), Emergency contact name and number
- [ ] AC-04: Given the required fields are filled and he taps "Create Record", the child's record is created and he is taken to the new record's profile screen
- [ ] AC-05: The record creation screen warns at the top: "Complete parental consent before adding clinical records" with a link to the consent flow (CONSENT-001)
- [ ] AC-06: Given the record is created, it appears immediately in the children list, searchable by first name

**Edge Cases & Error States:**
- [ ] EC-01: If a record already exists with the same child first name and date of birth, a warning appears before saving: "A record for a child with this name and birthdate already exists. Are you sure this is a different child?" — with options Confirm duplicate / Review existing record
- [ ] EC-02: If Rahul's connectivity drops mid-form, form data is saved locally as a draft; on reconnect, he can complete and submit

**Non-Functional Requirements:**
- Performance: Intake form must load in ≤ 1.5 seconds on minimum-spec Android
- Offline: Form draft saved locally; submission requires connectivity (record must sync to server on creation)
- Accessibility: Touch targets ≥ 44px; all dropdown pickers use native Android picker component for screen reader compatibility
- Privacy: ⚠️ DPDPA — even creating a record constitutes processing personal data of a minor; the consent prompt at AC-05 must be prominent and must block clinical data entry (not just warn)
- Security: Child records encrypted at rest (AES-256); all API calls transmitting child data over HTTPS/TLS 1.2+

**Dependencies:**
- Blocked by: AUTH-001 (user login and role system must exist); no other epic dependencies
- Enables: CONSENT-001 (consent flow ties to this record), SNOTE-001, SOAP-001, TMPL-001 (all clinical documentation requires the child record to exist), EMR-002, EMR-003, EMR-004, EMR-005

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android and Chrome desktop
- [ ] Duplicate detection tested — warning fires on name + DOB match
- [ ] Draft save on connectivity drop tested
- [ ] DPDPA consent prompt visible and prominent — verified in QA
- [ ] Encryption at rest and in transit — verified with engineering sign-off
- [ ] Code reviewed and merged

---

### Story EMR-002: Capture and store DPDPA-compliant parental consent

**As a** Rahul (Center Director / Admin)
**I want to** collect verifiable digital consent from a parent or guardian for storing and processing their child's health data
**So that** the center is compliant with India's DPDPA 2023 before any clinical records are created or shared

**Inspired by:** SimplePractice digital consent forms; Jane App consent management; no Indian tool reviewed has this feature (confirmed gap)

**Context:** This is the most important compliance story in the entire product. DPDPA 2023 Section 9 requires verifiable consent for processing data of minors. No Indian therapy tool reviewed has this implemented. This is a hard dependency for all clinical data stories.

**Acceptance Criteria:**
- [ ] AC-01: Given a child record exists without confirmed consent, a prominent orange banner on the child's profile reads: "Parental consent required — clinical records cannot be added until consent is confirmed. Add consent now." — this banner is not dismissible
- [ ] AC-02: Given Rahul taps "Add consent", a consent form screen opens showing: center name, child's name, a plain-language summary of what data will be collected and how it will be used (max 150 words — written in plain English; Hindi option Phase 2), a checkbox: "I confirm that I am the legal parent/guardian of [child name] and consent to the collection and processing of their health data as described above", a signature field (on-screen finger/stylus signature capture), date (auto-populated)
- [ ] AC-03: Given the parent signs and Rahul taps "Confirm consent", the consent record is saved with: timestamp, GPS coordinates (optional, with user permission), parent name (as typed by Rahul), signature image, the consent text version number (so future consent text changes are tracked)
- [ ] AC-04: Given consent is confirmed, the orange banner is replaced with a green indicator: "Consent confirmed — [date]" with a "View consent record" link
- [ ] AC-05: Given consent is confirmed, clinical data entry (notes, programs, SOAP notes) is unblocked for this child
- [ ] AC-06: Rahul can view the full consent record at any time from the child's profile under the "Consent" tab — it is read-only after confirmation

**Edge Cases & Error States:**
- [ ] EC-01: If the parent is not present (Rahul is completing the record remotely), provide an alternative: "Send consent request via WhatsApp" — this generates a link the parent can open on their own phone to sign; the consent is marked "Remote consent — parent signed via link" in the record
- [ ] EC-02: If consent is withdrawn by the parent (future state), a "Withdraw consent" option is available to Rahul — triggering a data deletion review workflow (not auto-delete; flagged for manual review)
- [ ] EC-03: If the consent form fails to save (server error), do not lose the signature image — save locally and retry on reconnect

**Non-Functional Requirements:**
- Offline: Remote consent link flow requires connectivity; in-person signature can be saved locally with sync
- Privacy: ⚠️ DPDPA — the consent record is itself sensitive data; it must be encrypted at rest and in transit; retained for the full duration of the therapeutic relationship plus a minimum retention period (suggest 3 years post-discharge, pending legal review)
- Security: Consent signature image stored securely; consent record immutable after confirmation (no edit, only view)
- Accessibility: Signature field must work with both finger and stylus; minimum signature area 200×100px on a 5.5-inch Android screen

**Dependencies:**
- Blocked by: EMR-001 (child record must exist)
- Enables: SNOTE-001, SOAP-001, TMPL-001, EMR-003, EMR-004, EMR-005 — this is the master gate for all clinical data

**Definition of Done:**
- [ ] All AC pass in QA
- [ ] Orange banner blocks all clinical data entry — tested end-to-end with SNOTE-001, SOAP-001
- [ ] Consent record saved with all required fields — verified in database
- [ ] Remote consent link flow tested — parent can sign on a separate device, consent reflects in Rahul's view
- [ ] Consent record immutable after confirmation — edit attempt returns error
- [ ] Code reviewed and merged

---

### Story EMR-003: Upload and store documents to a child's record

**As a** Rahul (Center Director / Admin)
**I want to** upload prior documents for a child — diagnosis report, previous therapy reports, school records, UDID card — and attach them to their record
**So that** all relevant documentation for a child is in one place and accessible to the clinical team without digging through paper files or WhatsApp photo albums

**Inspired by:** SimplePractice file uploads; Jane App document management; PractiPal (basic file attach)

**Context:** A family brings paper documents at intake. Rahul photographs them or uploads scanned PDFs. Or Dr. Sunita receives a school report by email and wants to attach it to the child's record.

**Acceptance Criteria:**
- [ ] AC-01: Given Rahul is on a child's profile, the "Documents" tab shows an "Upload document" button
- [ ] AC-02: Given he taps Upload, the system file picker opens — he can select a file from device storage or take a photo using the device camera; supported file types: PDF, JPG, PNG, HEIC
- [ ] AC-03: Given a file is selected, he must provide: a document type (dropdown: Diagnosis Report / Previous Therapy Report / School Record / UDID Card / Consent Form / Assessment Report / Other), an optional document date, an optional note (free text, max 200 characters)
- [ ] AC-04: Given he taps Upload and the upload completes, the document appears in the Documents tab with: document type label, upload date, uploader name, file size, and a thumbnail or PDF icon
- [ ] AC-05: Given any authorized staff member taps a document, it opens in a full-screen viewer (PDF viewer for PDFs, image viewer for photos)
- [ ] AC-06: Maximum file size per upload: 20MB. If a file exceeds this, show an error: "File is too large. Maximum size is 20MB. Try compressing the PDF or reducing the photo size."
- [ ] AC-07: Given Rahul taps a document and selects "Delete", a confirmation dialog appears — on confirmation, the document is soft-deleted (not visible in UI, retained in audit trail)

**Edge Cases & Error States:**
- [ ] EC-01: If the upload fails (network error mid-transfer), show: "Upload failed — tap to retry" — do not silently discard the file
- [ ] EC-02: If no documents have been uploaded yet, show empty state: "No documents yet. Tap 'Upload document' to add the child's diagnosis report or prior assessments."
- [ ] EC-03: If the device camera permission is not granted, show a prompt explaining why camera access is needed and linking to Settings

**Non-Functional Requirements:**
- Performance: Documents tab must load (list only, not file content) in ≤ 2 seconds; large PDF viewing may take ≤ 5 seconds — show a loading indicator
- Offline: Upload requires connectivity; previously uploaded documents list is readable offline from cache; file content (PDF/image) viewable offline only if previously opened and cached
- Privacy: ⚠️ DPDPA — uploaded documents are child health data; all uploads encrypted in transit and at rest; document access scoped to assigned staff; upload action logged in audit trail with uploader, timestamp, and file type
- Security: File type validation server-side (not client-side only) to prevent malicious file uploads; no executable file types permitted

**Dependencies:**
- Blocked by: EMR-001, CONSENT-001 (DPDPA gate)
- Enables: EMR-005 (clinical timeline shows document upload events)

**Definition of Done:**
- [ ] All AC pass in QA
- [ ] File type validation tested — non-permitted types rejected with clear error
- [ ] 20MB limit tested — oversized file shows correct error
- [ ] Upload retry on failure tested
- [ ] Soft delete confirmed — document not visible in UI but retained in audit trail
- [ ] Code reviewed and merged

---

### Story EMR-004: View a child's complete clinical timeline

**As a** Dr. Sunita (Clinical Supervisor)
**I want to** see a chronological timeline of all clinical events for a child — sessions attended, notes written, program versions saved, documents uploaded, consent recorded — in one scrollable feed
**So that** I have a complete clinical picture of the child's history without opening multiple separate tabs

**Inspired by:** Hi Rasmus clinical history timeline; CentralReach client activity feed; Jane App activity log

**Context:** Dr. Sunita is preparing a progress report or responding to a parent's query about the child's history. She wants one view that shows the full story.

**Acceptance Criteria:**
- [ ] AC-01: Given Dr. Sunita is on a child's profile, the "Timeline" tab shows a chronological feed (newest first) of all clinical events for that child
- [ ] AC-02: Each timeline entry shows: event type icon (session, note, program update, document upload, consent, SOAP note), event date and time, a one-line summary (e.g., "Session note added by Priya", "Program updated to v3.0 by Dr. Sunita", "Diagnosis report uploaded")
- [ ] AC-03: Given she taps any timeline entry, she is taken to the full detail of that event (the note, the program version, the document viewer, etc.)
- [ ] AC-04: Given she applies a filter (dropdown: All / Sessions only / Notes only / Program updates / Documents), the timeline updates to show only that event type
- [ ] AC-05: Given the timeline has more than 30 entries, it paginates — showing 30 at a time with a "Load older events" button at the bottom

**Edge Cases & Error States:**
- [ ] EC-01: If the child was just enrolled and no events exist yet, show: "Timeline is empty — events will appear here as sessions, notes, and programs are added."
- [ ] EC-02: Soft-deleted items (deleted notes, deleted documents) do not appear in the timeline in the normal view — they are only visible in the admin audit trail view

**Non-Functional Requirements:**
- Performance: Timeline list (30 entries) must load in ≤ 2 seconds on 4G
- Offline: Previously loaded timeline entries readable from cache
- Privacy: ⚠️ DPDPA — timeline contains aggregated child health data; access scoped to assigned staff only
- Accessibility: Event type icons must have text labels (not icon-only) for screen reader users

**Dependencies:**
- Blocked by: EMR-001, CONSENT-001, SNOTE-001, SOAP-001, TMPL-001, EMR-003 (all the events that populate the timeline must exist)
- Enables: REPORT-001 (progress report generation can draw date ranges from the timeline)

**Definition of Done:**
- [ ] All AC pass in QA
- [ ] Timeline events confirmed for each event type: session, note, program update, document upload
- [ ] Filter by event type tested
- [ ] Pagination tested at 30+ entries
- [ ] Code reviewed and merged

---

### Story EMR-005: Search and filter the children list by name, diagnosis, or assigned therapist

**As a** Rahul (Center Director)
**I want to** quickly find a specific child's record by searching their name, or filter the list by diagnosis type or assigned therapist
**So that** I can locate any child's record in under 10 seconds, without scrolling through a list of 30–50 children

**Inspired by:** SimplePractice client list search; Jane App patient search; PractiPal client list

**Context:** Rahul or Dr. Sunita is looking up a specific child. This is the most basic navigation story for the EMR. A center with 30–50 active children needs functional search.

**Acceptance Criteria:**
- [ ] AC-01: Given any authorized user is on the Children list screen, a search bar is visible at the top of the list — tapping it opens the keyboard and the list filters in real-time as the user types
- [ ] AC-02: Search matches on: child first name, child last name (if entered), parent name, parent mobile number (last 4 digits match)
- [ ] AC-03: Given no search query is active, the list defaults to all active enrolled children, sorted alphabetically by first name
- [ ] AC-04: Given she taps "Filter", a filter panel opens with: Assigned therapist (multi-select from staff list), Diagnosis (multi-select from diagnosis types used in the center), Enrollment status (Active / On hold / Discharged)
- [ ] AC-05: Given filters are applied, the count of matching records is shown: "Showing 8 of 34 children"
- [ ] AC-06: Search and filter results update within 300ms of input on device (client-side filtering for lists ≤ 200 children)

**Edge Cases & Error States:**
- [ ] EC-01: If the search query returns no results, show: "No children match '[query]'. Check the spelling or try a different name."
- [ ] EC-02: If the children list is empty (no records created yet), show: "No children enrolled yet. Tap 'Add New Child' to get started."

**Non-Functional Requirements:**
- Performance: Search results in ≤ 300ms for lists up to 200 children (client-side); for larger lists, server-side search in ≤ 1 second
- Offline: Children list (names and IDs) cached locally; search works offline against the cached list; full record requires connectivity if not previously cached
- Privacy: ⚠️ DPDPA — search results are personal data; access scoped by user role (Priya sees only her assigned children; Dr. Sunita and Rahul see all)

**Dependencies:**
- Blocked by: EMR-001 (child records must exist to search)
- Enables: No direct dependency (navigation utility)

**Definition of Done:**
- [ ] All AC pass in QA
- [ ] Real-time filtering tested with 30+ records
- [ ] Role-scoped search tested — Priya cannot find children outside her caseload
- [ ] Offline search against cached list tested
- [ ] Code reviewed and merged

---

## Backlog: EMR / EHR (EMR)

| Story ID | Title | Persona | Complexity | Priority | Blocked by |
|---|---|---|---|---|---|
| EMR-001 | Create a new child health record at enrollment | Rahul | M | P0 | AUTH-001 |
| EMR-002 | Capture and store DPDPA-compliant parental consent | Rahul | L | P0 | EMR-001 |
| EMR-003 | Upload and store documents to a child's record | Rahul | M | P1 | EMR-001, CONSENT-001 |
| EMR-004 | View a child's complete clinical timeline | Dr. Sunita | L | P1 | EMR-001, SNOTE-001, SOAP-001, TMPL-001, EMR-003 |
| EMR-005 | Search and filter the children list | Rahul / Dr. Sunita | M | P0 | EMR-001 |

---

## Cross-Epic Dependency Map

```
AUTH-001 (login + roles)
  └── EMR-001 (child record creation)
        └── EMR-002 / CONSENT-001 (DPDPA consent gate) ← MASTER GATE
              ├── SNOTE-001 (session notes)
              │     ├── SNOTE-002 (supervisor review queue)
              │     │     └── SNOTE-003 (co-sign + lock)
              │     ├── SNOTE-004 (edit/delete draft)
              │     └── SNOTE-005 (note history)
              ├── SOAP-001 (SOAP note creation)
              │     ├── SOAP-002 (SOAP note history)
              │     ├── SOAP-003 (PDF export)
              │     └── SOAP-004 (ABA-specific prompts)
              ├── TMPL-001 (therapy program from template)
              │     ├── TMPL-002 (version history)
              │     ├── TMPL-003 (program on session screen)
              │     ├── TMPL-004 (home program)
              │     └── TMPL-005 (custom center templates)
              ├── EMR-003 (document upload)
              └── EMR-004 (clinical timeline) ← all of the above feed this
                    └── REPORT-001 (progress reporting — next cluster)
```

---

## ⚠️ Feature Factory Disclaimer

These features were defined by competitive observation, journey map inference, and category assumption — not by validated user research. Before committing engineering capacity, a real product thinker should ask:

**What we copied but haven't validated:**

- **Session / Clinical Notes:** Whether Indian special educators (Priya) currently write any structured post-session notes at all. PractiPal and SimplePractice have this feature, but they serve Western-trained therapists who are already documenting sessions. In Indian autism centers, post-session documentation may be verbal or nonexistent. Building a note feature assumes a behavior that does not yet exist.

- **SOAP Notes:** Whether RCI-licensed special educators and clinical supervisors in India are trained in or use the SOAP format. SOAP is a US/UK medical note format. Indian clinical training programs (RCI, NIMH, AIIMS) may not teach SOAP structure. The format may be unfamiliar and create friction rather than reducing it.

- **Therapy Templates:** Whether Dr. Sunita will use a platform-provided template over her existing Word document structure. Template adoption requires that the field definitions match her clinical mental model — which is trained in Indian RCI curricula, not US ABA credential programs. CentralReach's ABLLS-R templates are US-ABA-specific and may not transfer.

- **EMR / EHR:** Whether small Indian therapy centers will invest time in creating digital records at enrollment. The risk is that record creation feels like more work than the current paper system at the point of enrollment — before the clinical benefits (automated reports, timeline view) are visible. If the first-use experience is a blank, empty form, centers may abandon the product before they see value.

**What a researcher would ask before building this:**

- Do any of the therapists or supervisors in target Indian centers currently use anything resembling structured clinical notes? (Even informal, handwritten — what format?) Observing 3–5 note examples from actual Indian centers would tell us more than any competitive analysis.
- Does Dr. Sunita know what a SOAP note is? Run a 10-minute concept test before building the SOAP template. If the format is unfamiliar, consider an alternative structure (e.g., "Program Review Note" with the same four functional sections but different labels).
- What does a real Indian autism center therapy program document look like today? Request 2–3 example programs from willing centers before defining the TMPL-001 field structure. The current field list is inferred from US ABA frameworks (CentralReach, Motivity) — it may be over-engineered or mis-structured for Indian practice.

**What the Product Consultant would challenge:**

- The EMR is a large foundational investment that must be built before any clinical features work (it is the master dependency). Before building the full EMR, consider whether a lighter "child profile" (first name, DOB, assigned therapist, consent flag) is sufficient to unlock v1 of clinical notes — and whether the full demographics, document upload, and timeline can be Phase 2 once there is evidence that therapists are actually using session notes.
- The DPDPA consent story (EMR-002) is a compliance requirement — but it is also a potential adoption blocker. A parent who is unfamiliar with digital consent flows may refuse to sign a screen during intake, blocking the entire record from being used clinically. The consent UX needs to be tested with actual Indian parents before go-live, not just QA'd against AC.

**Risk level by feature:**

| Feature | Risk level | Rationale |
|---|---|---|
| EMR / Child Health Record | Medium | Table stakes for a clinical platform; structural need is clear; Indian market has no competing solution; risk is adoption friction at enrollment not feature design |
| Session / Clinical Notes | Medium | Table stakes in US/global platforms; core behavioral assumption (Priya writes notes) is unvalidated for India |
| SOAP Notes | High | Differentiator; format familiarity in Indian clinical training is unvalidated; may need format adaptation |
| Therapy Templates | High | Differentiator; template structure derived from US ABA frameworks; field definitions need validation against real Indian program documents |

Use the `/research` agent to validate SOAP format familiarity and existing note-taking behaviors before sprint planning.
Use the `/product-consultant` agent to challenge whether the full EMR must be built before v1 or whether a lighter child profile unblocks enough.

---
