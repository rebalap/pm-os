# Requirements: Journey 4 — Clinical Program Design

> **❌ OUT OF SCOPE — POST-MVP**
>
> Therapy-specific feature requiring net-new build; existing EMR components cannot be reused. Deferred to post-MVP release.
>
> **Decision date:** 22 April 2026 | **Decision by:** Engineering + Product
> **Rationale:** Clinical program design is the core clinical value proposition for supervisors and therapists. Deferring this means the MVP launches without the features most likely to matter to clinical staff. If primary research confirms Journey 4 is an adoption blocker, this decision must be revisited before scope is locked. Requirements are documented now because the data model defined in this epic (program targets, prompt level enum, program versioning, program_version_id on the trial record) is a hard dependency for Journey 5 (In-Session Data Collection), Journey 7 (Supervisor Review), and blocks resolution of PROG-XXX dependency references in Journey 3 (scheduling) and Journey 6 (session notes). Engineering must align on schema decisions in the Pre-Build Decisions section before touching any of those in-scope stories.
> **Future scope:** Build after MVP core (enrollment, scheduling, billing) is validated with Indian therapy centers.
> **Reference:** `meetings/engineering/2026-04-22-engineering-alignment-meeting-summary.md`

---

**Product:** Autism Therapy Platform (India)
**Journey:** Journey 4 — Clinical Program Design
**MVP status:** ❌ OUT OF SCOPE — POST-MVP
**Primary actor:** Dr. Sunita (Clinical Supervisor — designs programs)
**Supporting actor:** Priya (Special Educator — reads programs during sessions; read-only access)
**Date:** 2026-05-05
**Story ID prefix:** PROG-
**Source documents:**
- `user-journeys/journey-04-clinical-program-design.md`
- `user-journeys/journey-map.md` — Part 2, Journey 4

---

## Epic: PROG — Clinical Program Design

**Goal:** Give Dr. Sunita a structured, Android-native tool to build individualized therapy programs — defining domains, skill targets, prompt hierarchies, and maladaptive behavior targets — and assign them to a child's record as the versioned source of truth for in-session data collection. By the end of this epic, Priya can open the active program for any assigned child in ≤ 2 taps, read all current targets and prompt levels from cached storage in a session room without connectivity, and Dr. Sunita can update a program mid-month with automatic version creation so no historical trial data is retroactively mis-attributed.

**Copied from:** CentralReach (program templates, skill acquisition targets, prompt level configuration, program versioning), Motivity (target-level prompt hierarchy, mastery criteria), Catalyst (program builder UI, in-session target display for therapist), Hi Rasmus (simplified program creation for non-BCBA clinical staff). No Indian competitor has any clinical program design capability — TherapEZ and PractiPal cover admin and billing only.

**Target user(s):** Dr. Sunita (Clinical Supervisor); Priya (Special Educator — read-only)

**Definition of Done:**
- Dr. Sunita can create a therapy domain structure with goals nested under domains
- Dr. Sunita can create skill targets with baseline, trial count, and mastery criteria under any goal
- Dr. Sunita can define a prompt hierarchy per target using a typed enum (Full Physical / Partial Physical / Gestural / Verbal / Independent) and set the current active prompt level
- Dr. Sunita can create maladaptive behavior reduction targets with behavior type, baseline frequency, and per-behavior ABC dropdown options
- Dr. Sunita can assign a completed program to a specific child's EMR record; the program becomes the source of truth for in-session data collection (Journey 5)
- Every program update creates a new program version automatically; prior trial data remains linked to the version under which it was collected
- Priya can view the active program for any assigned child in read-only mode; she can access it in ≤ 2 taps from the home screen; program loads from local cache when offline
- prompt_level is stored as a typed enum at the schema level — never as free text
- program_version_id is written to every trial record (Journey 5 INSESSION-001)
- All stories pass QA on minimum-spec Android (Redmi/Realme, 2GB RAM, Android 10+)
- DPDPA consent gate enforced server-side on all clinical data writes

**Out of scope (this epic):**
- SOAP note creation — covered in the full Journey 4 flow; out of scope for the PROG- story set (separate story prefix required when that work is scheduled)
- Home program PDF generation (TMPL-004) — post-MVP; depends on this epic completing first
- Custom template builder for Rahul (TMPL-005) — P2; deferred beyond this epic
- ABDM health record push — out of scope until ABHA uptake in Indian private therapy centers is validated
- Progress report generation — Journey 8 (post-MVP)
- Target mastery auto-calculation from trial data — requires Journey 5 trial data pipeline to be live first
- Program sharing between child records / program library — post-MVP
- iOS — Phase 1 Android only

**[ASSUMPTION — NOT VALIDATED]** This epic assumes Dr. Sunita will adopt platform-provided ABA template structures (DTT, NET, BIP) rather than her existing Word document format. Template adoption depends on whether the platform's field structure matches her clinical mental model — which is shaped by Indian RCI training programs, not US ABA certification frameworks. Validate template field structure against 3–5 real therapy program documents from Indian centers before finalizing schema and field definitions.

---

## Story PROG-001: Therapy domain and goal setup

**As a** Dr. Sunita (Clinical Supervisor)
**I want to** create named therapy domains (such as Communication, Self-care, Social Skills, Adaptive Behavior, Cognitive, Motor) and nest one or more therapy goals under each domain
**So that** the program has a logical clinical hierarchy that reflects how I organize my therapy work, and individual skill targets (PROG-002) have a structured location to live within

**Inspired by:** CentralReach program structure (domain → goal → target hierarchy); Motivity domain grouping; Catalyst program builder

**Context:** Dr. Sunita is on her Android phone or tablet in her office or a quiet space at the center. She has completed the child's intake assessment and is starting the therapy program for the first time (program status = "none" on the child's record). The child must have an active EMR record with DPDPA consent confirmed (consent_status = "confirmed") before this story is accessible. Domain and goal setup is the scaffold for all subsequent target creation (PROG-002 through PROG-004).

**Acceptance Criteria:**
- [ ] AC-01: Given Dr. Sunita opens a child's Program/Data tab and the child has no active program, then an empty state is shown: "No program yet — tap 'Create New Program' to get started" with a single full-width CTA
- [ ] AC-02: Given Dr. Sunita taps "Create New Program" and consent_status = "confirmed", then the Program Builder opens showing: a "Program name" field (required, max 100 characters) and an "Add Domain" button; no domains are pre-created
- [ ] AC-03: Given Dr. Sunita taps "Create New Program" and consent_status ≠ "confirmed", then the CTA is disabled with a tooltip: "Parental consent required before adding clinical records" — the Program Builder is never shown
- [ ] AC-04: Given the Program Builder is open, when Dr. Sunita taps "Add Domain", then a domain name input field appears (free text, max 60 characters, required); a pre-filled dropdown of common domain names is shown as suggestions: Communication / Social Skills / Adaptive Behavior / Self-care / Cognitive / Motor / Maladaptive Behavior; Dr. Sunita may accept a suggestion or type a custom name
- [ ] AC-05: Given a domain is named and saved, then an "Add Goal" button appears nested under that domain; tapping it opens a goal name input field (free text, max 100 characters, required) nested visually under the parent domain
- [ ] AC-06: Given at least one domain and one goal exist, then Dr. Sunita can add further domains (no maximum), add further goals under any existing domain (no maximum per domain), and reorder domains by long-press drag
- [ ] AC-07: Given Dr. Sunita taps "Save Program Structure", then the program is created with status "Draft", version = "1.0-draft", saved against the child's record with: program_id, child_id, created_by, created_at, program_name, and the domain/goal hierarchy; no targets exist yet; program is NOT yet visible to Priya
- [ ] AC-08: Given Dr. Sunita changes device orientation or navigates away mid-build, then all entered domain and goal data is auto-saved as a local draft on every field change; returning to the Program Builder within 24 hours restores the draft with a banner: "Draft restored — continue where you left off"

**Edge Cases & Error States:**
- [ ] EC-01: If Dr. Sunita taps "Save Program Structure" with a program name but no domains, inline validation fires: "Add at least one domain before saving"
- [ ] EC-02: If a domain is created but has no goals, inline validation fires on save attempt: "Add at least one goal to each domain before saving"
- [ ] EC-03: If the POST /children/{id}/programs call fails, the screen shows "Couldn't save program — tap to retry"; all entered data is preserved in local draft storage; no silent data loss
- [ ] EC-04: If two domains are given the same name within the same program, an inline warning fires: "You already have a domain named [name] — are you sure?" with "Keep both" and "Rename" options; not a hard block

**Non-Functional Requirements:**
- Performance: Program Builder opens in ≤ 1.5 seconds on minimum-spec Android; each domain/goal addition renders in ≤ 300ms
- Offline: All field input auto-saves to device local storage; POST /children/{id}/programs is queued offline; program is not pushed to any session screen until server-side sync completes
- Accessibility: All touch targets ≥ 44px; domain name suggestions list operable with single tap; drag-to-reorder has a long-press alternative for users who cannot drag
- Privacy: ⚠️ DPDPA — program is health data of a minor; consent_status gate enforced server-side (not client-side only); program stored encrypted at rest (AES-256); access scoped to assigned care team + supervisor + director

**Dependencies:**
- Blocked by: EMR-001 (child EMR record must exist), EMR-002 (DPDPA consent must be confirmed, consent_status = "confirmed"), AUTH-001 (Dr. Sunita authenticated as Supervisor role)
- Enables: PROG-002 (skill target creation requires domain/goal structure), PROG-003 (prompt level config requires a target to exist), PROG-004 (maladaptive behavior targets require a domain), PROG-005 (program assignment to child requires at least a saved draft program)

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android (Redmi/Realme, 2GB RAM, Android 10+)
- [ ] Consent gate tested: CTA disabled when consent_status ≠ "confirmed"
- [ ] Offline draft: navigate away mid-form, return, confirm draft restores
- [ ] EC-01 through EC-04 tested
- [ ] DPDPA gate confirmed server-side (not client-side flag only)
- [ ] Code reviewed and merged

---

## Story PROG-002: Skill target creation

**As a** Dr. Sunita (Clinical Supervisor)
**I want to** create a specific skill training target within a goal — defining the target behavior description, baseline performance, number of trials per session, and mastery criterion
**So that** each target is a complete, unambiguous clinical instruction that Priya can execute during a session and that Journey 5 (in-session data collection) can reference by target_id to record trial outcomes against

**Inspired by:** CentralReach skill acquisition target builder; Motivity target creation (baseline, trial count, mastery criterion fields); Catalyst program target card

**Context:** Dr. Sunita is building the therapy program for a child (PROG-001 complete; at least one domain and goal exist). She is creating skill acquisition targets — behaviors to increase through structured teaching. This story does NOT cover maladaptive behavior reduction targets (those are PROG-004). Targets created here are the primary data objects that in-session data collection (Journey 5) writes trial records against. The target_id generated here is the foreign key on the trial record schema.

**Acceptance Criteria:**
- [ ] AC-01: Given a domain and goal exist in the Program Builder (PROG-001), when Dr. Sunita taps "Add Target" under a goal, then a Target Creation form opens with the following required fields: Target name (short text, max 80 characters), Target behavior description (textarea, max 500 characters)
- [ ] AC-02: Given the Target Creation form is open, then optional fields are also shown: Baseline (short text, max 200 characters — e.g., "0/5 correct across 3 sessions"), Trials per session (numeric input, integer, minimum 1, maximum 50, defaults to 10), Mastery criterion (free text, max 200 characters — e.g., "4/5 correct across 3 consecutive sessions"), Teaching notes (free text, max 400 characters, optional)
- [ ] AC-03: Given Dr. Sunita taps "Save Target", then the target is saved as a child object of the parent goal with: target_id (UUID, system-generated), goal_id (parent), program_id, target_name, target_description, baseline, trials_per_session, mastery_criterion, teaching_notes, created_by, created_at, status = "Active"
- [ ] AC-04: Given a target is saved, then the target card appears in the goal's target list showing: target name, baseline (if provided), mastery criterion (if provided), and the current prompt level chip (initially empty — prompt level is set in PROG-003)
- [ ] AC-05: Given multiple targets exist under a goal, then Dr. Sunita can reorder them by long-press drag; order is persisted on save
- [ ] AC-06: Given Dr. Sunita taps a saved target card, then the Target Edit form opens with all fields pre-filled and editable; saving an edit does NOT create a new program version — version increment only occurs when Dr. Sunita explicitly saves the full program (PROG-006)
- [ ] AC-07: Given Dr. Sunita taps the delete icon on a target, then a confirmation dialog appears: "Delete this target? Trial data already collected will not be deleted." Confirming removes the target from the program draft

**Edge Cases & Error States:**
- [ ] EC-01: If "Save Target" is tapped with no target name, inline validation fires: "Target name is required"
- [ ] EC-02: If trials_per_session is set to a non-integer or value outside 1–50, inline validation fires: "Enter a number between 1 and 50"
- [ ] EC-03: If the program already has 20 targets across all goals, the "Add Target" button is disabled with a message: "Maximum of 20 targets per program. Create a separate program for additional targets."
- [ ] EC-04: If the target save API call fails, the target is held in local draft state; "Couldn't save target — stored locally until you reconnect" banner appears; no data loss

**Non-Functional Requirements:**
- Performance: Target Creation form opens in ≤ 500ms; save and render target card in ≤ 1 second
- Offline: Target creation saves to local draft on every field change; syncs on restore; target_id is pre-generated client-side (UUID v4) so downstream references can be written while offline
- Accessibility: All inputs ≥ 44px touch target; textarea fields scrollable within the form without triggering full-page scroll on Android
- Privacy: ⚠️ DPDPA — target data is child health data; same encryption and access-scoping as PROG-001

**Dependencies:**
- Blocked by: PROG-001 (domain/goal structure must exist; target is a child of a goal)
- Enables: PROG-003 (prompt level is configured per target; requires target_id to exist), PROG-005 (program assignment requires at least one active target), INSESSION-001 (Journey 5 trial record writes target_id from this story's generated UUID)

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android
- [ ] target_id (UUID) confirmed as the foreign key written to the trial record schema — engineering sign-off required before merging
- [ ] 20-target limit enforced and tested
- [ ] Offline target creation: disconnect, create target, reconnect, confirm sync
- [ ] EC-01 through EC-04 tested
- [ ] Code reviewed and merged

---

## Story PROG-003: Prompt level configuration per target

**As a** Dr. Sunita (Clinical Supervisor)
**I want to** define the prompt hierarchy for each skill target — selecting which prompt levels are in use for this target and setting the current active prompt level — using a fixed typed list, not free text
**So that** Priya knows exactly what level of prompting to use when delivering a trial, and the trial record can store prompt_level as a typed enum (never free text) so that cross-session and cross-version prompt level data is consistently queryable

**Inspired by:** CentralReach prompt level configuration per target (typed hierarchy); Motivity in-session prompt level display; Catalyst prompt fading tracking

**Context:** Dr. Sunita is in the Program Builder, reviewing a skill target she has just created (PROG-002 complete; target_id exists). Prompt level configuration is a sub-action within the Target Edit form. The prompt level enum defined here is the same enum used as the data type of the prompt_level field on the in-session trial record (Journey 5 INSESSION-001). This story is the place where that enum is canonically defined. Prompt levels are the standard ABA prompt hierarchy.

**Acceptance Criteria:**
- [ ] AC-01: Given a skill target exists (PROG-002), when Dr. Sunita opens the target's detail/edit view, then a "Prompt Level" section is shown with two controls: (a) a multi-select checklist of prompt level options — Full Physical / Partial Physical / Gestural / Verbal / Independent — to indicate which levels are in the prompt fading hierarchy for this target; (b) a single-select "Current active prompt level" picker from the same fixed list
- [ ] AC-02: Given Dr. Sunita configures the prompt hierarchy, then she can check any subset of the five levels to indicate the fading plan (e.g., checks: Full Physical, Partial Physical, Gestural — indicating the target starts at Full Physical and will fade toward Gestural before moving to Verbal); the active level must be one of the checked levels
- [ ] AC-03: Given the "Current active prompt level" is set, then the target card in the program view displays the active prompt level as a visually prominent chip or badge (e.g., bold text or a color-coded chip); Priya sees this chip on the Program View Screen (PROG-007)
- [ ] AC-04: Given Dr. Sunita saves the target with a prompt level configuration, then the following fields are written to the target record: prompt_hierarchy (array of PromptLevel enum values, min length 1), active_prompt_level (single PromptLevel enum value — must be one of the values in prompt_hierarchy), prompt_level_set_by (user_id), prompt_level_set_at (timestamp)
- [ ] AC-05: Given the prompt level enum, then the schema-level definition is: `enum PromptLevel { FULL_PHYSICAL, PARTIAL_PHYSICAL, GESTURAL, VERBAL, INDEPENDENT }` — this exact enum must be used on both the program target record (active_prompt_level field) and the in-session trial record (prompt_level field in Journey 5); no free-text prompt level fields exist anywhere in the data model
- [ ] AC-06: Given Dr. Sunita updates the active prompt level on a target (e.g., fading from Full Physical to Partial Physical), then the update is recorded with a prompt_level_history entry: previous_level, new_level, changed_by, changed_at; this history is queryable for the supervisor review journey (Journey 7)
- [ ] AC-07: Given a target has no prompt level configured, then the target card shows a "Prompt: Not set" chip; Priya's Program View Screen shows the same "Not set" state; the session can still proceed (prompt level is strongly recommended but not a hard blocker for program assignment)

**Edge Cases & Error States:**
- [ ] EC-01: If Dr. Sunita sets the active prompt level to a value not in the prompt_hierarchy array, client-side validation fires: "Active prompt level must be one of the selected hierarchy levels"
- [ ] EC-02: If no prompt levels are checked in the hierarchy but the "Current active level" picker is activated, the picker is disabled with a helper text: "Select at least one prompt level from the hierarchy first"
- [ ] EC-03: If the target update API call fails on prompt level save, the previous prompt level is restored in the UI; a retry banner appears; no partial write accepted

**Non-Functional Requirements:**
- Performance: Prompt level section renders inline within the target edit form; no separate screen load required; toggle changes render in ≤ 200ms
- Offline: Prompt level changes save to local draft immediately; sync on restore; prompt_level_history entry is queued and written server-side on sync
- Accessibility: Checklist items ≥ 44px touch targets; active prompt level picker uses native Android spinner for screen reader compatibility; color chip on target card must also carry a text label (not color-only)
- Privacy: ⚠️ DPDPA — prompt level is a component of clinical health data; same access controls as parent target record

**Dependencies:**
- Blocked by: PROG-002 (target must exist; prompt level is configured on a target)
- Enables: PROG-007 (Program View Screen shows active prompt level chip per target), INSESSION-001 (Journey 5 trial record prompt_level field uses the PromptLevel enum defined in AC-05 of this story)

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android
- [ ] PromptLevel enum definition (AC-05) reviewed and signed off by engineering lead before merge — this enum is shared across program and trial record schemas
- [ ] prompt_level_history tested: change active level, confirm history entry written
- [ ] EC-01 (invalid active level selection) and EC-03 (API failure with rollback) tested
- [ ] prompt_level chip on target card verified to carry text label (not color only)
- [ ] Code reviewed and merged

---

## Story PROG-004: Maladaptive behavior target setup

**As a** Dr. Sunita (Clinical Supervisor)
**I want to** create a behavior reduction target for a child — defining the behavior type, a baseline frequency or intensity, and the ABC (Antecedent / Behavior / Consequence) dropdown options specific to that behavior — so that Priya has a structured prompt when recording a behavioral incident during a session (Journey 5) and the data is consistent enough to analyze across sessions
**So that** maladaptive behavior data is structured and queryable from day one, not entered as free text that cannot be aggregated

**Inspired by:** CentralReach Behavior Intervention Plan (BIP) builder — ABC data collection options per behavior; Motivity behavior reduction target with per-behavior antecedent/consequence taxonomy; Hi Rasmus simplified behavior logging for non-BCBA staff

**Context:** Dr. Sunita is building or editing a therapy program (PROG-001 domain structure exists). A maladaptive behavior target lives under a domain (typically a "Maladaptive Behavior" domain created in PROG-001). This story is distinct from skill targets (PROG-002) — the data structure is different (frequency/intensity baseline instead of correct/incorrect trial data; ABC fields instead of prompt levels) and the in-session recording UI for these targets differs from skill acquisition trials. The target_id generated here is the foreign key on the behavior incident record in Journey 5.

**Acceptance Criteria:**
- [ ] AC-01: Given a domain exists in the Program Builder, when Dr. Sunita taps "Add Behavior Target" (distinct from "Add Target" for skill targets — separate button or type selector), then a Behavior Target Creation form opens with: Behavior name (short text, max 80 characters, required — e.g., "Self-injurious behavior — head hitting"), Behavior type (single-select enum: SELF_INJURIOUS / AGGRESSION / PROPERTY_DESTRUCTION / ELOPEMENT / STEREOTYPY / TANTRUM / NON_COMPLIANCE / OTHER), Behavior description (textarea, max 300 characters, optional)
- [ ] AC-02: Given the behavior type is selected, then additional fields appear: Baseline measurement (short text, max 200 characters — e.g., "Avg 8 incidents per 60-min session, observed across 3 baseline sessions"), Measurement type (single-select enum: FREQUENCY / DURATION / INTENSITY — default FREQUENCY), Target direction (read-only, always set to DECREASE for behavior reduction targets)
- [ ] AC-03: Given Dr. Sunita reaches the ABC Configuration section, then she can define per-behavior dropdown options for each ABC component by entering free-text options in three separate lists: Antecedent options (list of short text items, max 10 items, max 60 characters each — e.g., "Transition between activities", "Demand presented", "Peer proximity"), Behavior description options (auto-populated from Behavior name — editable, max 5 items), Consequence options (list of short text items, max 10 items, max 60 characters each — e.g., "Redirected to task", "Ignore and wait", "Removed from activity")
- [ ] AC-04: Given Dr. Sunita saves the behavior target, then the record is written with: behavior_target_id (UUID, system-generated), program_id, domain_id, behavior_name, behavior_type (BehaviorType enum), behavior_description, baseline_measurement, measurement_type (MeasurementType enum), target_direction = "DECREASE", abc_antecedent_options (array of strings), abc_behavior_options (array of strings), abc_consequence_options (array of strings), created_by, created_at, status = "Active"
- [ ] AC-05: Given the behavior target is saved, then the behavior target card is shown in the domain's target list with: behavior name, behavior type chip, baseline measurement, and a "ABC configured" badge if at least one antecedent and one consequence option exist
- [ ] AC-06: Given Dr. Sunita has not entered any ABC options, then the behavior target is still saved; a "ABC not configured — therapist will record free text" warning badge appears on the target card; this is allowed (not a hard block) but surfaced to Dr. Sunita as a data quality issue
- [ ] AC-07: Given a behavior target is saved, then during in-session data collection (Journey 5), when Priya logs a behavioral incident against this target, the ABC dropdowns shown to Priya are populated from abc_antecedent_options, abc_behavior_options, and abc_consequence_options on this record — not from a generic list

**Edge Cases & Error States:**
- [ ] EC-01: If "Save Behavior Target" is tapped with no behavior name, inline validation fires: "Behavior name is required"
- [ ] EC-02: If an ABC option text field is left blank within a configured list (e.g., 3 antecedents but one is empty), inline validation fires: "Each option must have a label"
- [ ] EC-03: If the behavior target save API call fails, the target is held in local draft; retry banner appears; no data loss
- [ ] EC-04: If Dr. Sunita attempts to add more than 10 options to any ABC list, the "Add option" button for that list is disabled with a message: "Maximum 10 options per ABC field"

**Non-Functional Requirements:**
- Performance: Behavior Target Creation form opens in ≤ 500ms; ABC list updates render in ≤ 200ms per item added
- Offline: All field input auto-saves to local draft; POST queued offline; behavior_target_id pre-generated client-side (UUID v4) so Journey 5 can reference it while offline
- Accessibility: All touch targets ≥ 44px; ABC option list items individually deletable with a visible delete affordance; BehaviorType and MeasurementType pickers use native Android spinners
- Privacy: ⚠️ DPDPA — behavior data is sensitive health data of a minor; same encryption and access controls as skill targets; behavior target records included in immutable audit trail

**Dependencies:**
- Blocked by: PROG-001 (domain must exist for the behavior target to be nested under)
- Enables: PROG-005 (program assignment requires at least one target — behavior target qualifies), INSESSION-001 (Journey 5 behavior incident records reference behavior_target_id from this story; abc_antecedent_options / abc_consequence_options are the source of the in-session ABC dropdowns)

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android
- [ ] behavior_target_id (UUID) confirmed as the foreign key written to the behavior incident record schema — engineering sign-off required before merging
- [ ] BehaviorType and MeasurementType enums reviewed and signed off by engineering lead before merge
- [ ] AC-06 tested: behavior target with no ABC config saves with warning badge
- [ ] AC-07 verified: in-session ABC dropdowns for a behavior incident use the options from this target's abc_*_options arrays (integration test required across PROG-004 and INSESSION-001)
- [ ] EC-01 through EC-04 tested
- [ ] Code reviewed and merged

---

## Story PROG-005: Assign therapy program to child

**As a** Dr. Sunita (Clinical Supervisor)
**I want to** link a completed therapy program — with all its domains, goals, skill targets, and behavior targets — to a specific child's EMR record, and have that program become the active, versioned source of truth for in-session data collection
**So that** when Priya opens the session screen for this child (Journey 5 INSESSION-001), the correct program targets are available for trial recording, and the program version is captured on every trial so that mid-month program updates do not corrupt historical data

**Inspired by:** CentralReach program assignment to client; Motivity program-to-child linking with version snapshot; Catalyst session target list drawn from assigned program

**Context:** Dr. Sunita has completed building a program (PROG-001 domain/goal structure + at least one skill target from PROG-002 or one behavior target from PROG-004). The program is currently in "Draft" status and is not visible to Priya. Assigning the program to the child transitions it from Draft to Active and assigns the current version as program_version_id = 1. DPDPA parental consent must be confirmed before assignment. This story is the pivot point between program authoring (PROG-001 through PROG-004) and in-session use (Journey 5).

**Acceptance Criteria:**
- [ ] AC-01: Given a program exists in Draft status with at least one active target, when Dr. Sunita taps "Assign Program to Child" on the Program Builder or Program/Data tab, then a confirmation dialog appears: "Assign [Program name] to [Child first name]? This will make the program visible to [Child first name]'s care team and available for session data collection." with "Confirm" and "Cancel" buttons
- [ ] AC-02: Given Dr. Sunita confirms the assignment and consent_status = "confirmed", then: program.status transitions from "Draft" → "Active"; program_version_id = 1 is assigned and written to the program record; the program becomes visible to Priya on her Program View Screen (PROG-007) within 30 seconds of server sync; a PROGRAM_ASSIGNED event is written to the child's clinical timeline (EMR-004)
- [ ] AC-03: Given the assignment is confirmed, then the program record stores: program_version_id (integer, starting at 1), version_assigned_at (timestamp), assigned_by (Dr. Sunita user_id), child_id; all targets within the program store a reference to this program_version_id
- [ ] AC-04: Given Priya next opens her session screen for this child (Journey 5 INSESSION-001), then the active program is available; every trial record written by Priya in Journey 5 includes: target_id (from PROG-002 or PROG-004), program_version_id (from this story's AC-03), prompt_level (PromptLevel enum from PROG-003), outcome; these four fields constitute the minimum required schema for a trial record
- [ ] AC-05: Given the program has been assigned to the child, then Dr. Sunita can assign the same program (or a modified version) to a different child by selecting "Assign to another child" — this creates a separate program record for the second child with its own program_version_id sequence; programs are child-specific records, not shared templates
- [ ] AC-06: Given Dr. Sunita attempts to assign a program with no targets, the "Assign Program" button is disabled with an inline message: "Add at least one target before assigning this program"
- [ ] AC-07: Given the assignment API call fails, then program.status remains "Draft"; no partial assignment; "Couldn't assign program — tap to retry" appears; a locally queued retry is created; program is NOT pushed to Priya's screen until confirmed server-side

**Edge Cases & Error States:**
- [ ] EC-01: If consent_status ≠ "confirmed" at the moment of assignment (e.g., consent was revoked between program creation and assignment), the assignment is blocked server-side; a message reads: "Parental consent is required before assigning a program. Update consent status in the child's profile."
- [ ] EC-02: If a program is already Active for this child, "Assign Program" triggers a version update (PROG-006) rather than a new assignment; a dialog appears: "This child already has an active program. Do you want to update it? A new version will be created automatically." — this flow continues into PROG-006
- [ ] EC-03: If Priya is not yet assigned to the child's care team, the program is still assigned and Active; a center-level warning banner appears on Dr. Sunita's view: "No Primary Therapist assigned — program is active but no therapist can view it in session"

**Non-Functional Requirements:**
- Performance: Assignment confirmation dialog appears in ≤ 500ms; program status transition and push to Priya's session screen completes within 30 seconds of server-side confirmation
- Offline: Assignment action is queued locally if offline; program is NOT pushed to Priya's screen until the queue item is confirmed server-side; "Assignment queued — will complete when connected" shown to Dr. Sunita
- Accessibility: Confirmation dialog touch targets ≥ 44px; dialog operable with TalkBack screen reader
- Privacy: ⚠️ DPDPA — program assignment is a clinical data event; written to immutable audit trail with: actor, child_id, program_id, program_version_id, timestamp; RBAC gate: only Supervisor and Director roles can assign programs

**Dependencies:**
- Blocked by: PROG-001 (domain/goal structure), PROG-002 or PROG-004 (at least one target required), EMR-002 (DPDPA consent = "confirmed")
- Enables: PROG-006 (versioning depends on an Active program existing), PROG-007 (Priya's read-only view requires an Active assigned program), INSESSION-001 (Journey 5 in-session data collection requires program_version_id and target_ids from an Active program)

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android
- [ ] program_version_id = 1 confirmed written on first assignment; verified in DB before merge
- [ ] Trial record schema confirmed by engineering: target_id, program_version_id, prompt_level (PromptLevel enum), outcome are all required fields — sign-off before merge
- [ ] PROGRAM_ASSIGNED event confirmed in clinical timeline (EMR-004 integration test)
- [ ] EC-01 (consent revoked) and EC-02 (active program already exists) tested
- [ ] Offline queue: assignment offline → reconnect → confirm status transition and push to Priya
- [ ] Code reviewed and merged

---

## Story PROG-006: Program versioning on update

**As a** Dr. Sunita (Clinical Supervisor)
**I want to** update an active therapy program — adding or removing targets, changing prompt levels, or revising mastery criteria — and have the system automatically create a new program version when I save, so that all trial data collected before my update remains linked to the version it was collected under and is never retroactively re-attributed to a program structure that didn't exist at the time
**So that** the program version history is a reliable audit trail and the supervisor review journey (Journey 7) and progress reports (Journey 8) can correctly attribute session data to the program version that was active when it was collected

**Inspired by:** CentralReach program versioning (date-effective versions, prior data linked to prior version); Motivity program update history; Catalyst version snapshots for compliance reporting

**Context:** Dr. Sunita is viewing or editing the Active program for a child (PROG-005 complete; program_version_id = 1 exists; Priya is actively collecting session data against this program). Dr. Sunita may need to update the program mid-month: add a new target as the child masters a current one, increase the mastery criterion, or fade the prompt level. Without versioning, a mid-month update would make it impossible to distinguish pre-update session data from post-update session data in the supervisor review or progress report. Program_version_id is non-negotiable on the trial record — this story defines the version increment mechanism.

**Acceptance Criteria:**
- [ ] AC-01: Given an Active program exists (program_version_id = N), when Dr. Sunita taps "Edit Program" on the Program/Data tab, then the Program Builder opens in Edit mode showing all current targets; an amber banner reads: "You are editing an active program. Saving changes will create a new version. Trial data collected so far will remain linked to Version [N]."
- [ ] AC-02: Given Dr. Sunita makes any of the following changes and taps "Save Program": adds a new target, removes a target, changes a target's prompt level, changes a target's mastery criterion, changes a target's trials_per_session, changes the program name — then a new version is automatically created: program_version_id increments to N+1, version_created_at = now(), version_created_by = Dr. Sunita user_id, change_note (free text, max 200 characters, optional but prompted with placeholder: "What changed and why?"), previous_version_id = N
- [ ] AC-03: Given the new version is saved, then: all existing trial records that were written against version N retain program_version_id = N — they are never updated to N+1; all new trials written by Priya after the update are written against program_version_id = N+1; this linkage is enforced at the database level, not just application logic
- [ ] AC-04: Given a new version is created, then the Program Version History view shows: a chronological list of all versions (Version 1, Version 2, etc.) each with: version number, created_by, created_at, change_note (if provided), target count; Dr. Sunita can tap any past version to view it in a read-only snapshot; no past version is editable
- [ ] AC-05: Given Priya is in an active session when Dr. Sunita saves a program update, then Priya receives an in-app banner on her session screen: "Program updated by Dr. Sunita — tap to review changes before continuing." Priya can dismiss the banner and continue with the cached version until she chooses to refresh; she is never force-refreshed mid-trial
- [ ] AC-06: Given Dr. Sunita navigates away from the Edit mode without saving, then no version increment occurs; the program remains at version N; unsaved changes are discarded after a "Discard changes?" confirmation dialog
- [ ] AC-07: Given a version update is saved offline (Dr. Sunita is on poor connectivity), then the version increment is queued locally; the draft is labeled "Pending version N+1 — will be saved when connected"; Priya does NOT receive the program update banner until the server-side write confirms; the version is not considered Active until server confirmation

**Edge Cases & Error States:**
- [ ] EC-01: If the version increment POST fails, the program reverts to version N in the UI; a retry banner appears; no partial version is written; no trial records are ever written against a draft version — only against confirmed server-side versions
- [ ] EC-02: If Dr. Sunita edits and saves a program update that removes a target that already has trial data, the system does not delete the trial data; the removed target's status is set to "Inactive" in version N+1; historical trial data for that target remains queryable against version N; Priya no longer sees the inactive target in her session screen for new trials
- [ ] EC-03: If two Supervisors attempt to save a program update simultaneously (concurrent edit), the server applies optimistic locking; the second writer receives: "Someone else saved changes to this program while you were editing. Review the latest version and re-apply your changes." — a conflict resolution screen shows both change sets

**Non-Functional Requirements:**
- Performance: Version increment on save completes and confirms in ≤ 3 seconds on 4G; version history list loads in ≤ 2 seconds for programs with up to 24 versions
- Offline: Pending version is held in local queue; Priya is not notified until server confirmation; read-only version history available from last sync
- Data integrity: program_version_id linkage on trial records is enforced at the database constraint level — not enforced by application logic alone; the DB must reject any trial record insert with a program_version_id that does not exist as a confirmed (non-draft) version
- Privacy: ⚠️ DPDPA — all program versions are child health data; version history is part of the immutable audit trail; version records retained for minimum 3 years; each version accessible only to assigned care team + supervisor + director

**Dependencies:**
- Blocked by: PROG-005 (Active assigned program with program_version_id must exist before a version update is possible)
- Enables: INSESSION-001 (Journey 5 trial records after this update write program_version_id = N+1; trial records before this update are immutably linked to version N), Journey 7 (Supervisor Review — version history and per-version trial data aggregation), Journey 8 (Progress Reporting — data attribution across version boundaries)

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android
- [ ] DB-level constraint confirmed by engineering: trial record INSERT rejected if program_version_id references a non-confirmed version — sign-off required before merge
- [ ] Version increment tested: edit program → save → confirm new version in DB; confirm prior trial records unchanged (program_version_id = N still on old records)
- [ ] EC-02 tested: remove target with existing trial data; confirm target status = "Inactive" in new version; confirm trial data not deleted
- [ ] EC-03 (concurrent edit conflict) tested with two simultaneous writes
- [ ] Priya's update banner tested: save update while Priya has session screen open; confirm banner appears; confirm Priya is not force-refreshed
- [ ] Code reviewed and merged

---

## Story PROG-007: Therapist program view — read-only

**As a** Priya (Special Educator)
**I want to** view the active therapy program for any child assigned to me — seeing all current targets, their teaching methods, current prompt levels, mastery status, and which targets are active for today — in a read-only view that loads from local cache even when I have no connectivity in the session room
**So that** I can reference the correct prompt levels and mastery criteria during a live session without asking Dr. Sunita, and so that the ≤ 2 tap access requirement is met for in-session use on a low-end Android phone

**Inspired by:** Catalyst session target list (therapist-facing, read-only, offline-cached); Motivity session data screen (program targets visible alongside data entry); Hi Rasmus therapist session view (simplified, mobile-first)

**Context:** Priya is on her Android phone, typically 1–2 minutes before a session begins, or while the session is in progress. The session room may have no Wi-Fi and intermittent mobile data. She has been assigned to this child's care team (PROG-005 complete; care team assignment in place). She cannot edit any field — the program is view-only for her role. She needs to see: which targets are active, what the current prompt level is for each, and what the mastery criterion is so she knows when to flag mastery to Dr. Sunita. The ≤ 2 taps from home screen is a hard product requirement for this story.

**Acceptance Criteria:**
- [ ] AC-01: Given Priya is logged in and opens the app to her Home Screen (My Children list), when she taps a child card, then the Session Tab for that child opens; on the Session Tab, a "Today's Program" card is visible above the fold without scrolling on a standard 360dp Android screen; tapping "View full program" on that card constitutes tap 2 — the program is accessible in ≤ 2 taps from the Home Screen
- [ ] AC-02: Given Priya opens the Program View Screen, then the screen displays the active program (current version) with: Program name and version number header, a scrollable target list showing for each target: target name, teaching method chip (DTT / NET / Other), current active prompt level chip (using the PromptLevel enum from PROG-003 — e.g., "GESTURAL"; displayed as human-readable "Gestural"), mastery criterion, mastery status chip ("In progress" / "Mastered" / "Not started")
- [ ] AC-03: Given the Program View Screen is rendered, then all target fields are read-only for Priya — no edit affordances are shown; no "Edit" button; no field tap activates an input; Priya's role is enforced by RBAC (Therapist role = read-only on program records)
- [ ] AC-04: Given Priya opens the Program View Screen with no connectivity, then the full program loads from local cache (last synced version); a persistent footer banner reads "Showing cached program — last synced [date/time]"; all target content is readable without any network request; this is a hard offline requirement — the screen must not show a loading spinner or error state if cached content exists
- [ ] AC-05: Given the active program has been updated by Dr. Sunita since Priya last synced (program_version_id on server > program_version_id in local cache), then an amber banner appears at the top: "Program updated [X hours ago] — tap to refresh." Priya can choose when to refresh; the app does NOT force-refresh or replace the cached version while Priya has the screen open or during an active session
- [ ] AC-06: Given the program has been synced to Priya's device, then the entire program content (all targets, all prompt levels, all mastery criteria, all teaching notes) is stored in local device storage in an encrypted format accessible without connectivity; the sync occurs automatically in the background when the device is online and at least one target has changed since the last sync
- [ ] AC-07: Given Priya views the program and the child has no active program assigned, then the screen shows: "No program set yet. Contact your supervisor." with Dr. Sunita's name displayed if she is assigned as Supervisor on the care team
- [ ] AC-08: Given Priya is not assigned to the child's care team, then accessing that child's program shows: "You are not assigned to this child. Contact your center admin." — no program content is shown; this is enforced server-side by RBAC

**Edge Cases & Error States:**
- [ ] EC-01: If the local cache is empty (first time the app is opened for this child before any sync has occurred) and Priya has no connectivity, then the screen shows: "Program not yet downloaded. Connect to the internet to load this child's program." — this is the only acceptable case where program content is not available offline
- [ ] EC-02: If the program has 20 targets, the scrollable list must render all 20 without performance degradation on minimum-spec Android (Redmi 2GB RAM); lazy rendering or virtual scroll must be used if needed
- [ ] EC-03: If the prompt level for a target is "Not set" (PROG-003 was not completed for that target), then the prompt level chip shows: "Prompt: Not set" in a neutral color — no blank or null state shown to Priya without an explicit label

**Non-Functional Requirements:**
- Performance: Program View Screen loads from local cache in ≤ 500ms; loads from network on 4G in ≤ 2 seconds; 20-target list renders completely in ≤ 1 second on minimum-spec Android
- Offline: Hard requirement — cached program content must be available without any network request when cache is populated; cache is encrypted at rest using device-level encryption; sync is background/automatic
- Accessibility: All target cards rendered at system default font size without horizontal scrolling on a 5.5-inch Android screen; back button and refresh CTA touch targets ≥ 44px; prompt level chips carry text labels alongside any color indicator (not color-only)
- In-session constraint: This screen must be reachable in ≤ 2 taps from the Home Screen — this is a non-negotiable product constraint; any navigation change that adds a third tap requires product sign-off before merge
- Privacy: ⚠️ DPDPA — program content is child health data; access strictly scoped to assigned care team members; Priya sees only programs for children assigned to her; cached content encrypted at rest; no program content transmitted to or accessible from unauthorized devices

**Dependencies:**
- Blocked by: PROG-005 (Active assigned program must exist; program_version_id must be set), PROG-003 (prompt level chip content comes from active_prompt_level on each target)
- Enables: INSESSION-001 (Journey 5 — Priya opens this screen before beginning trial data collection; the targets shown here are the targets available for selection in the in-session UI)

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android (Redmi/Realme, 2GB RAM, Android 10+)
- [ ] 2-tap access confirmed by QA: from Home Screen → tap child card → tap "View full program" — exactly 2 taps; regression test added for this path
- [ ] Offline load tested: sync program, enable airplane mode, open program view — confirm full content renders from cache; no loading spinner or network error
- [ ] EC-01 tested: first open with no prior sync and no connectivity; confirm correct error state
- [ ] RBAC tested: Priya cannot access program for a child she is not assigned to; confirmed server-side (not only client-side)
- [ ] 20-target render performance tested on Redmi device; acceptable load time confirmed
- [ ] Prompt level chip carries text label confirmed by design review before merge
- [ ] Code reviewed and merged

---

## Backlog Summary

| Story ID | Title | Persona | Complexity | Priority | Blocked by |
|---|---|---|---|---|---|
| PROG-001 | Therapy domain and goal setup | Dr. Sunita | M | P0 | EMR-001, EMR-002, AUTH-001 |
| PROG-002 | Skill target creation | Dr. Sunita | M | P0 | PROG-001 |
| PROG-003 | Prompt level configuration per target | Dr. Sunita | S | P0 | PROG-002 |
| PROG-004 | Maladaptive behavior target setup | Dr. Sunita | M | P0 | PROG-001 |
| PROG-005 | Assign therapy program to child | Dr. Sunita | M | P0 | PROG-001, PROG-002 or PROG-004, EMR-002 |
| PROG-006 | Program versioning on update | Dr. Sunita | L | P0 | PROG-005 |
| PROG-007 | Therapist program view — read-only | Priya | M | P0 | PROG-005, PROG-003 |

**Sprint recommendation:** PROG-001 through PROG-003 form the foundational skill target path and should be built as a single sprint. PROG-004 (maladaptive behavior targets) can run in parallel with PROG-003 since both are children of PROG-001/PROG-002 infrastructure. PROG-005 depends on at least PROG-001 and PROG-002 completing. PROG-006 and PROG-007 are the last to build — PROG-006 requires an Active program to exist, and PROG-007 requires both PROG-005 and PROG-003 to be complete.

**Note:** These stories are POST-MVP. Do not include in any sprint planning until the MVP scope (enrollment, scheduling, billing) has been validated with Indian therapy centers and a decision has been made to proceed to the clinical program design feature. Engineering should review the Pre-Build Decisions section immediately — the data model decisions affect in-scope MVP stories.

---

## Pre-Build Decisions Required

These decisions affect the data model for in-scope MVP journeys (Journey 5, Journey 7, Journey 6 session notes). Engineering must align on these schema decisions before building any story that touches trial records, session notes, or program targets — even if the PROG- stories themselves are deferred.

| # | Decision | Owner | Needed by | Downstream impact |
|---|---|---|---|---|
| PBD-01 | Confirm PromptLevel enum definition: `FULL_PHYSICAL, PARTIAL_PHYSICAL, GESTURAL, VERBAL, INDEPENDENT` — this exact enum must be used on both the program target record (PROG-003 active_prompt_level) and the in-session trial record (Journey 5 INSESSION-001 prompt_level field); any deviation after trial data exists is a schema migration | Engineering Lead | Before any Journey 5 (INSESSION-001) story is started | Trial record schema; Journey 7 supervisor review aggregations; Journey 8 progress report prompt fading charts |
| PBD-02 | Confirm trial record minimum required fields: target_id (UUID FK → program target), program_version_id (integer FK → program version), prompt_level (PromptLevel enum), outcome (OutcomeType enum: CORRECT / INCORRECT / PROMPTED) — these four fields are non-negotiable; adding or removing a field after trial data is written is a breaking migration | Engineering Lead | Before INSESSION-001 is started | Every Journey 5 story; Journey 7; Journey 8 |
| PBD-03 | Confirm program_version_id is enforced as a DB-level NOT NULL constraint and FK on the trial record — not an optional application-layer field; the DB must reject any trial insert without a valid confirmed program_version_id | Engineering Lead | Before PROG-006 and INSESSION-001 are started | Data integrity for cross-version queries in Journey 7 and Journey 8 |
| PBD-04 | Define BehaviorType enum values (PROG-004 AC-01): `SELF_INJURIOUS, AGGRESSION, PROPERTY_DESTRUCTION, ELOPEMENT, STEREOTYPY, TANTRUM, NON_COMPLIANCE, OTHER` — confirm these cover the behaviors present in Indian autism therapy center caseloads; gaps require adding enum values before first trial data is written | Clinical + Engineering | Before PROG-004 sprint | In-session behavior incident record schema; Journey 7 behavior frequency aggregations |
| PBD-05 | Define MeasurementType enum values (PROG-004 AC-02): `FREQUENCY, DURATION, INTENSITY` — confirm these are the correct measurement types for the target Indian center context | Clinical + Engineering | Before PROG-004 sprint | Behavior incident record display and aggregation logic |
| PBD-06 | Confirm offline encryption standard for cached program content on Priya's device (PROG-007 AC-06): device-level Android Keystore encryption vs. application-level AES-256 — must meet DPDPA 2023 requirements for health data of minors stored on consumer devices | Engineering Lead + Legal | Before PROG-007 sprint | DPDPA compliance; Priya's offline cached data security posture |
| PBD-07 | Confirm whether a "mastery status" field on the target record (PROG-007 AC-02: "In progress / Mastered / Not started") is manually set by Dr. Sunita or auto-calculated from trial data — if auto-calculated, the mastery calculation logic and the trial data pipeline (Journey 5) must be built before this field can display meaningful data | Product + Engineering | Before PROG-007 sprint | PROG-007 mastery status chip; Journey 7 supervisor review; Journey 8 progress reports |

---

## ⚠️ Feature Factory Disclaimer

These stories were defined by competitive observation, journey document synthesis, and category assumptions — not by validated primary research with Indian autism therapy clinical supervisors or therapists.

**What we assumed but haven't validated:**
- [ASSUMPTION] Dr. Sunita will adopt a platform-provided program structure (domains → goals → targets) rather than her existing Word document or paper binder format. Template adoption depends entirely on whether the field structure matches her clinical mental model, which is shaped by Indian RCI training programs — not US ABA certification frameworks. CentralReach's structures are US-ABA-specific and may not transfer to the Indian context without significant field-level adaptation.
- [ASSUMPTION] The five-level prompt hierarchy (Full Physical / Partial Physical / Gestural / Verbal / Independent) is the standard hierarchy used by RCI-trained Indian special educators. The BACB / BCBA-aligned prompt hierarchy may differ from what Indian clinical training programs teach. Validate with 5–10 working special educators before finalizing the PromptLevel enum.
- [ASSUMPTION] Indian clinical supervisors will find program versioning meaningful and will use the version history view. This assumes supervisors update programs more than once per child per month and experience the lack of version tracking as a genuine problem — neither of which has been confirmed.
- [ASSUMPTION] Priya will reference the program on her phone before or during sessions rather than using a printed program sheet or her existing memory of the program. Phone-based reference assumes the phone is charged, accessible, and that the app loads fast enough in the 1–2 minutes before a session begins to be useful.
- [ASSUMPTION] The maladaptive behavior taxonomy (BehaviorType enum in PROG-004) covers the behaviors actually present in Indian autism therapy center caseloads. The enum is derived from US ABA literature and may miss behaviors commonly documented in Indian clinical practice.
- [ASSUMPTION] Dr. Sunita is willing to build therapy programs on a minimum-spec Android phone. Supervisors may strongly prefer desktop or tablet for documentation tasks of this complexity. If the primary research reveals a strong desktop preference, the Program Creation Form must be designed mobile-first but also usable on a wider-screen form factor.

**What a researcher would ask before building this:**
- What does a real Indian autism therapy supervisor's program document look like today? Request 3–5 example programs from willing centers before finalizing the domain/goal/target field structure in PROG-001 and PROG-002. Does the platform's hierarchy match, or is it over-engineered from US ABA frameworks?
- Which prompt levels does the typical Indian RCI-trained special educator actually use? Show five special educators the five-level enum and ask which levels they recognize and use regularly. If the answer is "mostly Full Physical and Verbal — we don't differentiate Partial Physical from Full Physical in our documentation," the enum may need to be simplified.
- How does Dr. Sunita actually hand off a new or updated program to Priya today? Observe this in 3–5 centers. If the handover is a two-minute verbal briefing that "works well enough," the platform's program creation workflow must be substantially faster and less effortful to displace it.
- Does Priya currently reference a program document during sessions, or is the program memorized? If memorized, PROG-007 (offline program view) is solving a problem Priya does not perceive — which would mean adoption requires changing an established habit, not filling a recognized gap.

**What the Product Consultant would challenge:**
- Seven stories for program design before a single line of in-session data collection is built is a significant clinical investment on an unvalidated assumption. Consider whether a minimum viable program structure — just targets with prompt levels, no domain/goal hierarchy — is enough to unblock Journey 5 trial data collection and reduce pre-build risk. The full domain/goal hierarchy (PROG-001) may be more structure than Indian centers need at v1.
- PROG-006 (program versioning) is a correct and important architectural decision, but it adds meaningful complexity to the MVP clinical path. If the primary research reveals that Indian supervisors update programs infrequently (e.g., once per quarter at a program review meeting), the version-linking complexity may be premature for v1. The data model constraint (PBD-03) should still be defined now; the versioning UI can be deferred until the update frequency assumption is validated.
- The 20-target limit per program (PROG-002 AC-03) is an arbitrary ceiling. Complex cases may require more. Validate the typical target count for Indian autism therapy center caseloads before hardcoding this limit into the schema.

**Risk level:**
- PROG-001 (domain/goal structure): Medium-High — template adoption assumption is the highest-risk bet in the product; validate field structure against real programs before building
- PROG-002 (skill targets): Medium — field-level design is directionally sound; mastery criterion format needs validation against Indian clinical documentation practice
- PROG-003 (prompt levels): Medium — PromptLevel enum values need validation with Indian RCI-trained educators before the enum is written into the schema
- PROG-004 (maladaptive behavior targets): Medium — BehaviorType and ABC structure adapted from US ABA frameworks; Indian context validation required
- PROG-005 (program assignment): Low-Medium — assignment mechanics and DPDPA gate are well-defined; main risk is that the program content being assigned was built on unvalidated assumptions
- PROG-006 (versioning): Low-Medium — architectural decision is correct; UI complexity may be premature if update frequency is low
- PROG-007 (therapist read-only view): Low — table stakes for any clinical platform; offline cache requirement is well-defined; adoption assumption is the risk, not build complexity

Use the `/research` agent to validate prompt hierarchy terminology and template field structure alignment with Indian RCI clinical training before sprint planning.
Use the `/product-consultant` agent to challenge whether the full domain/goal/target hierarchy is required for v1 or whether a flatter structure (targets only) unblocks Journey 5 sooner.
Use the `/design-critique` agent to review the Program Creation Form (multi-target scrolling on minimum-spec Android) and the Program View Screen (≤ 2 tap access path) before prototyping.
