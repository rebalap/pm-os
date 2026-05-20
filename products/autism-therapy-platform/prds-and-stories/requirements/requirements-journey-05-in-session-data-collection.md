# Requirements: Journey 5 — In-Session Data Collection (Behavioral Data)

> **❌ OUT OF SCOPE — INDIA MVP**
>
> No insurance reimbursement driver in Indian out-of-pocket market. Requirements documented for future release and data model planning only. Do not include in MVP or post-MVP sprint planning without explicit product decision.
>
> **Decision date:** 22 April 2026 | **Decision by:** Product
> **Rationale:** Indian therapy is paid out-of-pocket. No insurance authorization cycle, no payor audit, no external mandate requiring granular trial-by-trial documentation. This journey is the foundational data layer for all downstream clinical intelligence (supervisor review, progress reports, home programs). When eventually built, it will be the make-or-break adoption moment for the platform.
> **Future scope:** US / international market expansion, or India market if primary research surfaces demand signal without a reimbursement driver.
> **Reference:** `meetings/engineering/2026-04-22-engineering-alignment-meeting-summary.md`

---

**Journey:** In-Session Data Collection (Behavioral Data)
**Primary persona:** Priya (Special Educator / Behavior Therapist — runs live sessions 1:1 with child)
**Supporting personas:** Dr. Sunita (Clinical Supervisor — reviews session data post-sync)
**Story prefix:** INSESSION-
**Source documents:**
- `/Users/prahladrebala/Documents/pm-os/products/autism-therapy-platform/user-journeys/journey-05-in-session-data-collection.md`
- `/Users/prahladrebala/Documents/pm-os/products/autism-therapy-platform/user-journeys/journey-map.md`

---

## Design Non-Negotiables (apply to every story in this journey)

These constraints override any competing requirement. They are not acceptance criteria — they are physical and regulatory realities of the session room context.

1. **One-handed operation is absolute.** Priya manages the child with one hand during live sessions. Any interaction requiring two hands to navigate, open, or confirm fails the design standard.
2. **≤ 2 taps to record a trial outcome from the active session screen.** Tap 1: the outcome button (Correct / Incorrect / Prompted). That is the complete interaction. If navigation to the screen counts as Tap 1, the recording tap must be Tap 2. No confirmation dialogs on trial marks.
3. **Haptic feedback on every confirmed mark.** Session rooms are noisy. Priya cannot look at the screen after every tap to confirm the record saved. Haptic is the confirmation signal.
4. **Offline-first is the primary behavior, not a fallback.** The local write is the authoritative record. The server sync is eventual consistency. The app must function identically whether the device has connectivity or not.
5. **DPDPA 2023 applies.** Trial-by-trial behavioral data of a minor is sensitive health data. Every story that writes or reads this data requires parental consent to be confirmed on record (Journey 0 gate) before the session can begin.

---

## User Stories

---

## Story INSESSION-001: DTT Trial Outcome Recording

**As a** Special Educator (Priya)
**I want to** mark the outcome of each discrete trial — Correct, Incorrect, or Prompted — with a single tap during a live session
**So that** I can record trial-by-trial data accurately without breaking contact with the child or pausing the session

**Inspired by:** Motivity and Catalyst (US ABA platforms) — both document one-tap trial recording as the core in-session interaction; Notate — large touch targets on active session screen

**Context:** Priya is in a session room with an active child (Arjun). She is holding or prompting the child with one hand. Her Android phone (Redmi/Realme class, 2GB RAM, Android 10+) is on a surface or in her free hand. The session was started from the Session Start screen (INSESSION-002 dependency). The active target is displayed on screen. She has just completed a discrete trial — she gave an instruction, the child responded, and she needs to record the outcome immediately while the next trial is set up.

**Acceptance Criteria:**

- [ ] AC-01: Given a session is In Progress and a target is displayed on the Active Session Screen, when Priya taps one of the three outcome buttons (Correct / Incorrect / Prompted), then a trial record is written to local storage immediately (< 200ms) with: target ID, outcome value, timestamp (ISO 8601 UTC), session ID, therapist ID, child ID, prompt level active at time of recording.
- [ ] AC-02: Given a trial record is written to local storage, when the tap registers, then haptic feedback fires immediately (short pulse, ≤ 50ms latency from tap) and the trial counter increments on screen — no confirmation dialog, no undo prompt.
- [ ] AC-03: Given the Active Session Screen is displayed, when Priya examines it with one hand, then all three outcome buttons (Correct / Incorrect / Prompted) are visible on screen without scrolling, each with a minimum touch target of 48x48dp, and the currently active target name and current prompt level are readable at a glance above the buttons.
- [ ] AC-04: Given a trial is recorded, when Priya completes the programmed trial block (default: 10 trials per target), then the screen displays a brief block summary ("8/10 Correct — 80%") with a single tap affordance to advance to the next target; the summary is dismissable within 1 tap.
- [ ] AC-05: Given the device is offline when a trial is recorded, when the write occurs, then the record is stored in the local queue identically to the online path — no error state is shown, no data is lost, and a non-intrusive offline indicator ("Offline — data saved") is visible in a persistent status bar.

**Edge Cases & Error States:**

- [ ] EC-01: If Priya accidentally double-taps an outcome button within 300ms, only one trial record is written (debounce on outcome buttons — 300ms minimum interval between trial registrations per target).
- [ ] EC-02: If the app is force-closed mid-session (device restart, low-memory kill on Redmi/Realme 2GB RAM class), when the app is reopened, the session resumes from its In Progress state with all previously recorded trials intact from local storage. No trial data is lost.
- [ ] EC-03: If the child's therapy program has no active targets loaded for this session (program not yet defined — PROG- story dependency not met), the session cannot be started and Priya sees a blocking screen: "No active program targets found. Contact [Supervisor Name] to set up this child's program before recording." Session start is gated.
- [ ] EC-04: If Priya taps the wrong outcome button (e.g., Correct instead of Incorrect), there is no in-session undo within the active trial flow. A post-session review screen (INSESSION-006) allows supervisors to annotate data quality — this is by design to prevent edit-during-session cognitive load.

**Non-Functional Requirements:**

- Performance: Trial record write to local storage must complete in < 200ms on minimum-spec device (Redmi 2GB RAM, Android 10+). Haptic feedback latency must be < 50ms from tap event. Active Session Screen must load in < 1.5s from session start.
- Offline: All trial records write to local SQLite store first. Background sync to server via queue worker when connectivity is available. App must survive process kill and device restart without data loss — local store is the source of truth.
- Accessibility: Touch targets minimum 48x48dp on all outcome buttons. Correct button green (#4CAF50 or equivalent with 4.5:1 contrast on background), Incorrect button red (#F44336), Prompted button yellow/amber (#FF9800) — color alone must not be the only differentiator; button labels must be present. Haptic feedback is the primary confirmation signal.
- Privacy: ⚠️ DPDPA 2023 — trial-by-trial behavioral data constitutes sensitive health data of a minor. Session start must be gated behind confirmed parental consent record (Journey 0). All trial records stored locally must be encrypted at rest (AES-256 or equivalent). Server-synced records must be access-scoped to assigned therapist, supervisor, and center admin only.

**Dependencies:**
- Blocked by: PROG-XXX (Active therapy program with defined targets must exist for child — Journey 4 data model); CONSENT-XXX (Parental DPDPA consent confirmed — Journey 0)
- Enables: INSESSION-003 (session timer and trial counter), INSESSION-005 (session summary auto-generation), INSESSION-006 (supervisor review sync), INSESSION-007 (data sync on restore)

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android (Redmi/Realme, 2GB RAM, Android 10+)
- [ ] Haptic feedback confirmed on physical device — not on emulator
- [ ] Trial record persists through app force-kill and device restart (verified by QA kill-and-reopen test)
- [ ] Offline mode verified: airplane mode active during trial recording, records confirmed in local store, sync confirmed on reconnect
- [ ] DPDPA gate verified: session start blocked when parental consent record is absent
- [ ] EC-01 debounce verified
- [ ] Code reviewed and merged

---

## Story INSESSION-002: Session Start and Program Load

**As a** Special Educator (Priya)
**I want to** start a session for a specific child and see their active program targets pre-loaded on screen before beginning trials
**So that** I know exactly which targets to run and at what prompt level, without having to navigate during the live session

**Inspired by:** Catalyst (US ABA) — pre-session program review screen before trial recording begins; Motivity — session setup confirmation before data collection starts

**Context:** Priya arrives at the session room before the child enters (or with the child already present). She opens the app, navigates to the scheduled session, and needs to confirm the program targets for today's session before beginning. This setup must complete before the first trial — it cannot happen during trial recording. The screen must be configured and ready before the child begins responding. This is the only navigation-heavy moment in the in-session flow — once recording starts, navigation is locked to the minimum required.

**Acceptance Criteria:**

- [ ] AC-01: Given a session is scheduled for today and Priya opens the app, when she taps the session card from "My Sessions" (today's view), then the Session Program Preview screen loads showing: child name, session date, session type (DTT or NET), list of active program targets for this session, current prompt level per target, and programmed trial count per target — all pre-populated from the child's active therapy program record (PROG- data dependency).
- [ ] AC-02: Given the Session Program Preview screen is displayed, when Priya taps "Begin Recording", then the Active Session Screen loads with the first target pre-selected and the three outcome buttons (Correct / Incorrect / Prompted) immediately tappable — ready for the first trial within 1.5s of the tap.
- [ ] AC-03: Given the Session Program Preview screen is displayed, when Priya reviews it, then she cannot modify any program target, prompt level, or trial count from this screen — program modifications are locked to Dr. Sunita's role (RBAC gate: Clinical Supervisor role only).
- [ ] AC-04: Given the device is offline when Priya navigates to the session, when the app loads the Session Program Preview, then it loads the cached version of the child's therapy program from local storage — no connectivity required. The cached program version date is displayed ("Program last updated: [date]") so Priya can flag if she suspects the program is stale.
- [ ] AC-05: Given a session is started, when the session status transitions from Scheduled to In Progress, then the session start timestamp is recorded (ISO 8601 UTC), the session instance record is written to local storage, and the system confirms parental DPDPA consent is on record before allowing Begin Recording — if consent is absent, a blocking screen is shown with the instruction to contact the admin.

**Edge Cases & Error States:**

- [ ] EC-01: If no sessions are scheduled for the child today (scheduling gap or system error), Priya sees a "No session scheduled today" state with a contact instruction — she cannot manually create an ad-hoc session from the therapist role. Ad-hoc session creation is a Center Director / Admin function.
- [ ] EC-02: If the child's therapy program was updated by Dr. Sunita after the local cache was last synced and Priya is offline, Priya sees the cached program with the stale version warning. She must acknowledge ("I understand this may not be the latest version") before proceeding. This is a data integrity trade-off explicitly accepted in the offline-first design.
- [ ] EC-03: If Priya navigates away from the Session Program Preview screen without tapping Begin Recording (e.g., a phone call interrupts), the session status remains Scheduled — not In Progress — until Begin Recording is explicitly tapped.

**Non-Functional Requirements:**

- Performance: Session Program Preview screen must load from local cache in < 1.5s on minimum-spec device. The transition from Begin Recording tap to Active Session Screen (trial-ready state) must complete in < 1.5s.
- Offline: Full session setup must be completable with no connectivity. Program targets, prompt levels, and trial counts are cached from the last successful sync. App must surface cache date so Priya can identify stale programs.
- Accessibility: "Begin Recording" is the primary action — must be visually dominant, minimum 48dp height, placed in the thumb-reachable zone for one-handed use.
- Privacy: ⚠️ DPDPA 2023 — session start is the entry point to creating a minor's health data record. DPDPA consent gate must be enforced here. Session instance record is sensitive health data; local encryption at rest required.

**Dependencies:**
- Blocked by: SCHED-XXX (session must be scheduled — Journey 3); PROG-XXX (active therapy program must exist — Journey 4); CONSENT-XXX (parental consent — Journey 0)
- Enables: INSESSION-001 (DTT trial recording), INSESSION-003 (session timer), INSESSION-004 (prompt level logging), INSESSION-005 (session summary)

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android (Redmi/Realme, 2GB RAM, Android 10+)
- [ ] Offline load from cache verified with airplane mode active
- [ ] DPDPA consent gate verified: session blocked when consent absent, session proceeds when consent present
- [ ] RBAC gate verified: program modification controls absent from therapist role view
- [ ] Stale cache warning verified: program version date displayed correctly
- [ ] Code reviewed and merged

---

## Story INSESSION-003: Session Timer and Trial Counter

**As a** Special Educator (Priya)
**I want to** see a running session timer and a live trial counter for the current target on the Active Session Screen at all times
**So that** I know how long the session has been running and how many trials remain in the current block without needing to count manually

**Inspired by:** Motivity (US ABA) — persistent session timer and trial block counter on data collection screen; Hi Rasmus — real-time trial counter in session view

**Context:** Priya is running trials during an active session. The timer and trial counter are ambient — they run in the background and are visible on screen, but they do not require Priya to interact with them. They are informational elements that support her clinical judgment (is this session running long? how many trials are left in this block?) without adding taps or cognitive load.

**Acceptance Criteria:**

- [ ] AC-01: Given a session is In Progress, when the Active Session Screen is displayed, then a session elapsed timer (HH:MM:SS format) is visible in a persistent position on screen, increments every second, and runs continuously without requiring any interaction from Priya.
- [ ] AC-02: Given a target is active and trials are being recorded, when Priya views the Active Session Screen, then a trial counter displays the current count and the programmed block total (e.g., "Trial 4 of 10") and updates immediately after each trial tap — the counter increment is part of the same 200ms write cycle as the trial record.
- [ ] AC-03: Given the session timer is running and the device loses connectivity, when Priya continues recording trials, then the session timer continues running without interruption — the timer is driven by the device clock, not a server call.
- [ ] AC-04: Given Priya taps "Pause Session" (a secondary control, less prominent than outcome buttons), when the session is paused, then the session timer stops and a "Session Paused" visual indicator is displayed. The timer resumes exactly from the paused value when Priya taps "Resume Session". The pause event is recorded with timestamp.
- [ ] AC-05: Given the session reaches 60 minutes elapsed (a configurable threshold — default 60 minutes), when the timer crosses this threshold, then a non-blocking visual nudge appears ("Session is 60 minutes — consider wrapping up") that auto-dismisses after 5 seconds without requiring a tap from Priya.

**Edge Cases & Error States:**

- [ ] EC-01: If the app is backgrounded (phone call, notification) while a session is In Progress, the session timer continues running using the device clock. When Priya returns to the app, the timer reflects the actual elapsed time including the backgrounded period. The session is not auto-paused by backgrounding.
- [ ] EC-02: If the device clock is significantly wrong (device clock skew > 5 minutes from server time detected on sync), a data quality flag is attached to all trial records written during that session — visible to Dr. Sunita in the supervisor review view with a note: "Timestamps may be inaccurate — device clock was out of sync at time of recording."

**Non-Functional Requirements:**

- Performance: Timer must update every second without jank on minimum-spec device. Trial counter increment must occur within the same 200ms write cycle as the trial record — they cannot be out of sync.
- Offline: Timer is device-clock-driven. No server dependency. Runs through connectivity loss without interruption.
- Accessibility: Timer and trial counter must be readable in ambient light. Minimum font size 14sp. Must not interfere with the primary outcome buttons — placed in a non-thumb-zone area (top of screen) to avoid accidental interaction.
- Privacy: Timer and counter are display-only — they do not independently write data. The pause event record (AC-04) follows the same DPDPA data handling as trial records.

**Dependencies:**
- Blocked by: INSESSION-001 (session must be in progress for timer to run), INSESSION-002 (session start creates the session instance that the timer attaches to)
- Enables: INSESSION-005 (session summary uses session duration from timer), INSESSION-008 (supervisor notification includes session duration)

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android (Redmi/Realme, 2GB RAM, Android 10+)
- [ ] Timer confirmed to run without server connection (airplane mode test)
- [ ] Timer confirmed to continue running when app is backgrounded
- [ ] Trial counter confirmed to increment within 200ms of trial tap (same write cycle)
- [ ] Pause/Resume behavior verified with timestamps
- [ ] Code reviewed and merged

---

## Story INSESSION-004: Prompt Level Logging

**As a** Special Educator (Priya)
**I want to** record the prompt level used during each trial as part of the trial outcome — or switch the active prompt level for an entire block with a single tap
**So that** Dr. Sunita can see not just whether the child succeeded but how much support was needed, which is the key data for fading prompts in the therapy program

**Inspired by:** CentralReach (US ABA) — prompt level as a dimension of every trial record; Catalyst — prompt level displayed on active session screen with single-tap adjustment

**Context:** In ABA therapy, the prompt level is not a fixed property of the session — it can vary trial by trial, or it can be held constant for a block. Priya needs to record which prompt level she used. In most sessions, she will run a block at a consistent prompt level (set before the block begins) and only needs to record the occasional deviation. In some sessions, a prompting hierarchy (most-to-least or least-to-most) requires prompt level to be tracked per trial. Both scenarios must be supported. The prompt level control must never block the trial outcome tap — it is secondary to the Correct / Incorrect / Prompted buttons.

**Acceptance Criteria:**

- [ ] AC-01: Given a session is In Progress and a target is displayed on the Active Session Screen, when Priya views the screen, then the currently active prompt level for the target (as configured in the therapy program — e.g., "Full Physical Prompt", "Partial Physical Prompt", "Gestural Prompt", "Independent") is displayed visibly above the outcome buttons.
- [ ] AC-02: Given the current active prompt level is displayed, when Priya taps the prompt level indicator, then a compact selection bottom sheet appears with the available prompt levels for this target (configured per target in the therapy program — not a global list), allowing Priya to change the active prompt level with a single tap. The bottom sheet dismisses automatically after selection. Total interaction: 2 taps (tap indicator, tap new level).
- [ ] AC-03: Given Priya changes the active prompt level mid-block, when she records the next trial, then that trial record stores the new prompt level. All prior trials in the block retain their original prompt level. The prompt level change event is recorded with timestamp and is visible in the supervisor review.
- [ ] AC-04: Given the therapy program specifies a fixed prompt level for a target (no adjustment expected), when the Active Session Screen is displayed for that target, then the prompt level indicator is displayed as read-only (no tap affordance) and labeled "Fixed — contact supervisor to adjust".
- [ ] AC-05: Given a trial record is written, when the record is stored (locally and eventually server-synced), then the prompt level is stored as a first-class field on the trial record schema — not as a free-text note — to enable supervisor filtering and trend analysis by prompt level.

**Edge Cases & Error States:**

- [ ] EC-01: If Dr. Sunita has not defined prompt levels for a target in the therapy program (PROG- setup gap), the prompt level field defaults to "Not specified" on the trial record and Priya sees a warning flag on the target: "Prompt levels not configured for this target. Contact supervisor." She can still record trial outcomes — the prompt level gap does not block recording.
- [ ] EC-02: If Priya opens the prompt level bottom sheet during a trial (child is responding and Priya is managing the interaction), she can dismiss the bottom sheet with a swipe-down or back button without changing the prompt level. The underlying session state is not affected.

**Non-Functional Requirements:**

- Performance: Prompt level bottom sheet must open in < 300ms of tap. Selection and dismiss must complete within the 200ms trial write cycle — prompt level field is written as part of the same atomic trial record write.
- Offline: Prompt level selection is a purely local operation during sessions. No server call required. Stored as part of the trial record in the local queue.
- Accessibility: Prompt level indicator must have minimum 44dp touch target if tappable. Bottom sheet options must have minimum 48dp row height for one-handed tap accuracy.
- Privacy: ⚠️ DPDPA 2023 — prompt level per trial is part of the clinical trial record and is sensitive health data for a minor. Same data handling rules as trial outcome records.

**Dependencies:**
- Blocked by: INSESSION-001 (trial recording must exist — prompt level is a field on the trial record), INSESSION-002 (session and target loaded), PROG-XXX (therapy program must define prompt levels per target)
- Enables: INSESSION-005 (session summary includes prompt level data), PROG-XXX (supervisor uses prompt level data to update fading criteria in therapy program)

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android (Redmi/Realme, 2GB RAM, Android 10+)
- [ ] Prompt level stored as a typed enum field (not free text) on trial record schema — confirmed in data model review
- [ ] Bottom sheet interaction confirmed at ≤ 2 taps from active session screen
- [ ] Offline storage verified — prompt level survives app kill and device restart
- [ ] EC-01 fallback behavior verified: recording not blocked when prompt levels are not configured
- [ ] Code reviewed and merged

---

## Story INSESSION-005: Maladaptive Behavior Frequency and Duration Recording

**As a** Special Educator (Priya)
**I want to** log a maladaptive behavior episode with a single tap while a session is in progress — and optionally add ABC data (Antecedent, Behaviour, Consequence) immediately after
**So that** the clinical record captures behavioral incidents accurately in real time rather than from memory at session end, giving Dr. Sunita the data to adjust the behavior intervention plan

**Inspired by:** Catalyst (US ABA) — floating behavior counter button during active sessions; CentralReach — ABC data capture linked to frequency event; Motivity — persistent behavior counter accessible from any session screen state

**Context:** A maladaptive behavior episode (e.g., table hit, self-harm, tantrum, aggression) can occur at any point during the session — during a trial, between trials, or during a break. When an episode occurs, Priya's first obligation is managing the child safely. Data recording is secondary. The behavior counter must be tappable with one hand at any moment without navigating away from the current session state. In some episodes, Priya will have both hands occupied managing the child — in this case, she taps the counter immediately after the episode subsides. ABC data capture must be non-blocking — she must be able to dismiss it and continue the session.

**Acceptance Criteria:**

- [ ] AC-01: Given a session is In Progress, when Priya views any state of the Active Session Screen (trial recording, between targets, paused), then a floating behavior counter button is persistently visible in a consistent screen position (recommended: bottom-right corner, outside the thumb zone of the outcome buttons), with a minimum touch target of 56x56dp and a visible frequency count badge showing the current session tally for the primary behavior type.
- [ ] AC-02: Given the floating behavior counter button is visible, when Priya taps it, then a behavior frequency record is written to local storage immediately (< 200ms) with: session ID, behavior type (primary — configurable per child in the therapy program), timestamp, session phase (mid-trial, between-trials, paused), and haptic feedback fires on tap. The session continues uninterrupted — no modal or blocking overlay appears.
- [ ] AC-03: Given a behavior frequency record has been written, when 5 seconds have elapsed since the tap, then a non-blocking ABC capture panel slides up from the bottom of the screen. Priya can fill in Antecedent (dropdown — pre-configured per child) and Consequence (dropdown — pre-configured per child) with one tap each. A free-text note field is available but optional. Submitting the panel writes an ABC record linked to the frequency event. Dismissing the panel (swipe down or tap outside) closes it without ABC data — the frequency record is retained regardless.
- [ ] AC-04: Given an ABC capture panel is displayed, when Priya cannot complete it immediately (both hands occupied, episode still active), then she can dismiss the panel and re-access it within a 5-minute window via a "Pending ABC" indicator on the behavior counter button. After 5 minutes, the window closes and the frequency record is marked "ABC not captured".
- [ ] AC-05: Given Priya needs to log behavior duration (e.g., for a prolonged tantrum), when she taps the behavior counter button a second time within the same episode, then a duration mode activates: the first tap records episode start, the second tap records episode end, and the duration is calculated and stored on the behavior record. A visual indicator ("Timing episode...") is displayed between the two taps so Priya can distinguish a duration recording from a frequency tap.

**Edge Cases & Error States:**

- [ ] EC-01: If Priya taps the behavior counter and cannot access the ABC panel for 5 minutes (managing a severe episode), the frequency record is retained with "ABC not captured" status. Dr. Sunita can add an observation note in the supervisor review but cannot retrospectively add ABC data — the data integrity boundary is the end of the 5-minute window.
- [ ] EC-02: If multiple behavior types are defined for the child (e.g., both "aggression" and "self-harm" tracked separately), a long-press on the behavior counter button opens a compact behavior type selector (maximum 4 types). Short-press always records the most recently used behavior type — minimizing taps for the most common scenario.
- [ ] EC-03: If the device is offline when a behavior event occurs, the frequency and ABC records write to the local queue identically to the online path. No data loss. Non-intrusive offline indicator ("Offline — data saved") visible in status bar.

**Non-Functional Requirements:**

- Performance: Behavior frequency record write must complete in < 200ms. Haptic feedback latency < 50ms. ABC panel slide-up animation must complete in < 300ms.
- Offline: Frequency records and ABC records write to local SQLite store first. Background sync when connectivity restored. App must survive process kill without losing behavior records.
- Accessibility: Floating button minimum 56x56dp (larger than standard 44dp — reflects high-stakes, one-handed use during behavioral incident). Button must be reachable in the thumb zone for one-handed grip. Haptic feedback is critical here — Priya may not look at the screen during an episode.
- Privacy: ⚠️ DPDPA 2023 — behavioral incident records are sensitive health data for a minor. Encrypted at rest on device. Access-scoped to assigned therapist, supervisor, and admin on server. ABC data (Antecedent, Behaviour, Consequence) may describe specific behavioral presentations — heightened sensitivity applies.

**Dependencies:**
- Blocked by: INSESSION-002 (session must be In Progress), PROG-XXX (behavior types and ABC dropdown options must be pre-configured in therapy program)
- Enables: INSESSION-005 (session summary includes behavior frequency count), INSESSION-007 (data sync includes behavior and ABC records), PROG-XXX (behavior data feeds supervisor behavior intervention plan review)

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android (Redmi/Realme, 2GB RAM, Android 10+)
- [ ] Floating button confirmed persistently visible across all Active Session Screen states (trial recording, between targets, paused)
- [ ] Haptic feedback confirmed on physical device for both behavior tap and ABC submission
- [ ] ABC panel 5-minute window and auto-dismiss verified in QA
- [ ] Duration mode (double-tap) verified: start timestamp, end timestamp, duration calculation
- [ ] Offline: frequency and ABC records survive app force-kill and device restart
- [ ] EC-02 long-press behavior type selector verified with 2 and 4 behavior types
- [ ] Code reviewed and merged

---

## Story INSESSION-006: Session Summary Auto-Generation from Trial Data

**As a** Special Educator (Priya)
**I want to** see an automatically computed session summary — trials per target, accuracy percentage per target, and behavior frequency count — when I end the session
**So that** I can verify the session data, add a brief narrative note if needed, and close the session without manually calculating anything

**Inspired by:** Motivity (US ABA) — auto-computed session summary at session end; CentralReach — structured session note with pre-populated data from trial records; SimplePractice — structured session note template

**Context:** Priya has completed all programmed targets for the session and taps "End Session". The post-session window is time-pressured — the next child may already be waiting or the parent is at the door. The session summary must be computed instantly from local trial data and require minimum effort from Priya to confirm and close. The narrative note field is optional — the structured data summary is the primary record. Priya cannot edit individual trial records from this screen — data editing is a supervisor function with an audit trail.

**Acceptance Criteria:**

- [ ] AC-01: Given Priya taps "End Session" from the Active Session Screen, when the Session End Summary screen loads, then it displays: (a) session date, child name, therapist name, session duration; (b) a per-target summary table with columns: Target Name, Trials Recorded, Correct Count, Incorrect Count, Prompted Count, Accuracy % (Correct / Total Trials x 100, rounded to nearest integer); (c) maladaptive behavior frequency count per behavior type; (d) a free-text narrative note field (optional, placeholder: "Add session observations..."). The summary loads within 1.5s of the End Session tap — computed entirely from local trial data without a server call.
- [ ] AC-02: Given the Session End Summary screen is displayed, when Priya taps "Save and Close", then the session status transitions from In Progress to Completed, the session record is finalized in local storage, and the sync queue is flagged as ready for server upload. Priya is returned to the My Sessions screen.
- [ ] AC-03: Given the Session End Summary screen is displayed, when Priya adds a narrative note and taps "Save and Close", then the note text is stored as a field on the session record (max 1000 characters) alongside the structured trial data — not as a replacement for it.
- [ ] AC-04: Given the session summary is displayed, when Priya reviews the per-target accuracy percentages, then she cannot edit any individual trial outcome from this screen. A non-intrusive label reads: "Trial records are final. Supervisors can annotate data quality in the clinical review." This is an explicit design decision to prevent therapist-side retrospective editing.
- [ ] AC-05: Given a session is ended with fewer trials recorded than the programmed trial count (e.g., session ended early due to behavioral incident), when the summary screen loads, then the summary accurately reflects the actual trials recorded. A visual indicator flags each target where the trial count was below the programmed count (e.g., "3/10 trials — session ended early").

**Edge Cases & Error States:**

- [ ] EC-01: If Priya taps "End Session" with zero trials recorded (session was started but no outcomes logged — child did not engage or session was immediately disrupted), the summary screen shows a zero-trial state with a mandatory reason selector: "Why are no trials recorded?" with options (Child not present, Behavioral incident, Session cancelled, Other). This reason is stored on the session record.
- [ ] EC-02: If the app is killed before Priya taps "Save and Close" on the Session End Summary screen, when the app is reopened, the session remains in "In Progress" state (not Completed) and all trial data is intact in local storage. Priya must explicitly save to finalize the session.
- [ ] EC-03: If the narrative note exceeds 1000 characters, the text input stops accepting characters and a character count indicator shows "1000/1000". No truncation occurs silently.

**Non-Functional Requirements:**

- Performance: Session End Summary must load within 1.5s on minimum-spec device, computed from local data with no server call. Accuracy calculations for up to 10 targets and 100 total trials must complete in < 500ms.
- Offline: Summary is computed entirely from local trial data. "Save and Close" writes the finalized session record to local storage and queues for server sync. Fully functional with no connectivity.
- Accessibility: Per-target summary table must be scrollable if more than 4 targets are present. Minimum row height 44dp. "Save and Close" is the primary action — visually dominant, placed in thumb-reachable zone.
- Privacy: ⚠️ DPDPA 2023 — the session summary consolidates all trial-by-trial behavioral data for a session. This is a complete clinical record of a minor's behavioral health data. Encrypted at rest. Access-scoped to assigned therapist, supervisor, and admin.

**Dependencies:**
- Blocked by: INSESSION-001 (trial records must exist to compute summary), INSESSION-003 (session duration from timer), INSESSION-005 (behavior frequency count in summary)
- Enables: INSESSION-007 (finalized session record is what gets synced to server), INSESSION-008 (supervisor notification triggered on sync of a Completed session record)

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android (Redmi/Realme, 2GB RAM, Android 10+)
- [ ] Accuracy calculation verified: multiple test scenarios with known trial counts
- [ ] EC-01 zero-trial state verified with mandatory reason selector
- [ ] EC-02 kill-before-save verified: session remains In Progress on reopen, data intact
- [ ] Narrative note saves as field on session record alongside structured data (not instead of)
- [ ] Summary loads in < 1.5s from local data in airplane mode
- [ ] Code reviewed and merged

---

## Story INSESSION-007: Data Sync When Connectivity Restores

**As a** Special Educator (Priya)
**I want** the session data I recorded offline to sync to the server automatically when connectivity is restored — without me having to initiate it or wait for it to complete
**So that** Dr. Sunita can see accurate session data without me needing to do anything after saving the session

**Inspired by:** Motivity (US ABA) — background sync with offline queue; CentralReach — transparent background data sync with supervisor dashboard update on completion

**Context:** Session rooms in Indian therapy centers may have no mobile data during sessions. Priya may have recorded an entire session offline. When she leaves the session room and enters an area with connectivity — even if she is not actively using the app — the queued session data should sync silently in the background. This is an infrastructure story. It has no meaningful UI beyond a sync status indicator. The correctness of this sync is critical: a lost or duplicated session record directly impacts Dr. Sunita's clinical decisions.

**Acceptance Criteria:**

- [ ] AC-01: Given a finalized session record (status = Completed) is present in the local sync queue, when the device acquires any data connectivity (WiFi or mobile data), then the background sync worker initiates upload within 60 seconds of connectivity detection — without requiring the app to be in the foreground and without requiring any user action.
- [ ] AC-02: Given the background sync worker is uploading session data, when the upload completes successfully, then: (a) the local record is marked as Synced with server timestamp; (b) the server record is verified against the local record (trial count, session ID, child ID match check) before the local record is marked Synced; (c) if the counts do not match, the sync is flagged as a data integrity error and the full local record is retained pending manual review.
- [ ] AC-03: Given a sync is in progress and connectivity is lost mid-upload, when the device reconnects, then the sync worker retries from the last confirmed checkpoint — it does not re-upload records already confirmed as synced. The retry mechanism uses exponential backoff (initial retry: 30s, max retry interval: 10 minutes).
- [ ] AC-04: Given multiple sessions are queued for sync (Priya had two sessions offline in sequence), when connectivity is restored, then sessions sync in chronological order (earliest session first). The sync queue is processed serially, not in parallel, to avoid server-side race conditions on the child's clinical record.
- [ ] AC-05: Given a session record has been in the sync queue for more than 24 hours without a successful sync, when Dr. Sunita opens the child's clinical record on the supervisor dashboard, then a "Data pending sync" indicator is shown for that session with the last attempted sync timestamp — so Dr. Sunita knows the data exists locally but has not yet reached the server.

**Edge Cases & Error States:**

- [ ] EC-01: If the server rejects a session record during sync (e.g., session ID already exists on server — duplicate upload from a previous partial sync), the sync worker checks whether the existing server record is complete (trial count matches local record). If complete, the local record is marked Synced and the duplicate upload is discarded. If incomplete, the server record is updated with the complete local record. Server-side idempotency key: session ID.
- [ ] EC-02: If the local device storage is critically low (< 100MB free — a real constraint on 16–32GB Redmi/Realme devices), the app displays a persistent warning: "Device storage is low — session data may not be saved. Free up space before your next session." This warning is shown on the My Sessions screen, not during an active session (to avoid cognitive disruption).
- [ ] EC-03: If a session record fails to sync after 5 retry attempts over 48 hours, a center admin alert is generated (not a Priya-facing alert — she cannot do anything about it). The admin sees: child name, session date, therapist name, sync status, and a manual re-sync button.

**Non-Functional Requirements:**

- Performance: Sync must not consume foreground thread resources — background worker only. For a typical session record (10 targets x 10 trials = 100 trial records, plus behavior records and session metadata), upload payload should be < 50KB. Sync should complete in < 10s on a standard 4G connection.
- Offline: The sync mechanism is specifically designed for the offline-first model. The local SQLite store is the source of truth at all times. Sync is eventual consistency — never blocking, never data-destructive.
- Accessibility: Sync is background — no UI beyond a status indicator. No user action required or expected.
- Privacy: ⚠️ DPDPA 2023 — all session data transmitted to server must be encrypted in transit (TLS 1.2 minimum, TLS 1.3 preferred). Server-side records access-scoped to assigned therapist, supervisor, and center admin (RBAC). Sync worker must not log child ID, behavioral data, or trial outcomes to any unencrypted device log file.

**Dependencies:**
- Blocked by: INSESSION-006 (session must be in Completed state to enter sync queue), AUTH-XXX (device authentication token required for server upload)
- Enables: INSESSION-008 (supervisor notification is triggered by sync completion event)

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android (Redmi/Realme, 2GB RAM, Android 10+)
- [ ] Background sync verified: session uploaded while app is backgrounded (not in foreground)
- [ ] Mid-upload connectivity loss and retry verified
- [ ] Duplicate upload / idempotency key behavior verified (EC-01)
- [ ] Sync ordering verified: two queued sessions sync in chronological order
- [ ] Server-side record count verification step confirmed in sync flow
- [ ] TLS encryption on transit confirmed in security review
- [ ] Code reviewed and merged

---

## Story INSESSION-008: Supervisor Notification on Session Data Sync

**As a** Clinical Supervisor (Dr. Sunita)
**I want to** receive a notification when a session I supervise has synced to the server
**So that** I know immediately when new clinical data is available for review without polling each child's record manually throughout the day

**Inspired by:** CentralReach (US ABA) — supervisor caseload dashboard updates on session sync; Theralytics — configurable notification rules for supervisor review queue

**Context:** Dr. Sunita manages a clinical caseload of multiple children across multiple therapists. Under the current paper workflow, she reviews data in batch — often 1–2 weeks delayed. The digital workflow's core clinical value proposition is near-real-time data visibility. When Priya's session data syncs, Dr. Sunita should know about it so she can review before the program runs stale. Notifications must be configurable — if Dr. Sunita is running her own sessions, a constant stream of notifications is disruptive.

**Acceptance Criteria:**

- [ ] AC-01: Given a session record for a child on Dr. Sunita's clinical caseload transitions to Synced status on the server, when the sync is confirmed, then Dr. Sunita receives an in-app notification within 60 seconds: "New session data available — [Child Name], [Session Date], [Therapist Name]. Tap to review."
- [ ] AC-02: Given Dr. Sunita taps the notification, when the notification is opened, then she is taken directly to that session's data view in the child's clinical record — showing the per-target accuracy summary, behavior frequency count, and session note (if added by Priya). She does not need to navigate through the caseload dashboard to find the session.
- [ ] AC-03: Given Dr. Sunita prefers not to receive per-session notifications during certain hours, when she configures a "Do Not Disturb" window in her notification settings (e.g., 9:00–13:00 — her peak clinical hours), then session sync notifications during this window are queued and delivered in a single batch notification at the end of the window: "3 new sessions available to review."
- [ ] AC-04: Given Dr. Sunita has reviewed a session in the clinical record, when she marks it as "Reviewed", then the session record is updated with her reviewer ID and review timestamp, and the in-app notification for that session is cleared from her notification center.
- [ ] AC-05: Given a child's session data has not been reviewed by Dr. Sunita within 48 hours of sync, when the 48-hour threshold passes, then the session is flagged as "Overdue Review" in Dr. Sunita's caseload dashboard — visually distinct from reviewed sessions. No additional notification is sent — the dashboard flag is sufficient.

**Edge Cases & Error States:**

- [ ] EC-01: If Dr. Sunita is offline when a notification is generated, the notification is stored and delivered when she next opens the app — it is not a push notification that is lost if the device is offline. In-app notification queue holds undelivered notifications for up to 7 days.
- [ ] EC-02: If Dr. Sunita is assigned as supervisor to a large caseload (> 20 active children) and multiple sessions sync simultaneously, notifications are batched if they arrive within a 5-minute window: "4 new sessions available to review — [Child 1], [Child 2], [Child 3], and 1 more." Individual sessions are listed in the notification center.
- [ ] EC-03: If a session syncs but the data is flagged as a potential data integrity issue (EC-02 from INSESSION-007 — trial count mismatch), the notification to Dr. Sunita includes a warning flag: "Session data synced — data integrity check failed. Review manually." She is not blocked from viewing the data.

**Non-Functional Requirements:**

- Performance: Notification must be generated and delivered in-app within 60 seconds of sync completion on the server. No real-time WebSocket required — polling interval of 60 seconds is acceptable for the MVP of this feature.
- Offline: In-app notifications are queued if Dr. Sunita's device is offline. Delivered on next app open. Notification state (delivered, read, dismissed) is server-managed, not local-only — so notifications are consistent across devices if Dr. Sunita uses multiple devices.
- Accessibility: Notification tap target in notification center minimum 44dp row height. Unread indicator must not rely on color alone (bold text or icon required alongside color differentiation).
- Privacy: ⚠️ DPDPA 2023 — notification content includes child name and session data reference. Notification must not include detailed clinical data (trial counts, behavior descriptions) in push notification payload that could be read from the lock screen. In-app notification may show full detail — push notification body must be limited to: "New session data available for review." Child name is acceptable in the notification, but behavioral details are not.

**Dependencies:**
- Blocked by: INSESSION-007 (sync must complete to trigger notification), AUTH-XXX (Dr. Sunita must be authenticated with the correct caseload scope), RBAC-XXX (notification is delivered only to the assigned supervisor, not all supervisors)
- Enables: Future PROG- stories (supervisor review triggers program update consideration)

**Definition of Done:**
- [ ] All AC pass in QA on minimum-spec Android (Redmi/Realme, 2GB RAM, Android 10+)
- [ ] Notification delivered within 60 seconds of sync confirmed in test
- [ ] Do Not Disturb window behavior verified
- [ ] Batch notification for simultaneous syncs verified (EC-02)
- [ ] Data integrity warning flag on notification verified (EC-03)
- [ ] Push notification payload verified: no clinical detail on lock screen
- [ ] Reviewed / mark as reviewed flow verified with reviewer timestamp
- [ ] Overdue Review flag (48h) verified in caseload dashboard
- [ ] Code reviewed and merged

---

## Backlog Table

| Story ID | Title | Persona | Complexity | Priority | Blocked by |
|---|---|---|---|---|---|
| INSESSION-001 | DTT Trial Outcome Recording | Priya | L | P0 | PROG-XXX, CONSENT-XXX, INSESSION-002 |
| INSESSION-002 | Session Start and Program Load | Priya | M | P0 | SCHED-XXX, PROG-XXX, CONSENT-XXX |
| INSESSION-003 | Session Timer and Trial Counter | Priya | S | P1 | INSESSION-001, INSESSION-002 |
| INSESSION-004 | Prompt Level Logging | Priya | M | P1 | INSESSION-001, INSESSION-002, PROG-XXX |
| INSESSION-005 | Maladaptive Behavior Frequency and Duration Recording | Priya | L | P1 | INSESSION-002, PROG-XXX |
| INSESSION-006 | Session Summary Auto-Generation | Priya | M | P0 | INSESSION-001, INSESSION-003, INSESSION-005 |
| INSESSION-007 | Data Sync When Connectivity Restores | Priya / System | L | P0 | INSESSION-006, AUTH-XXX |
| INSESSION-008 | Supervisor Notification on Session Data Sync | Dr. Sunita | M | P1 | INSESSION-007, AUTH-XXX, RBAC-XXX |

**Complexity key:** S = 1 day; M = 2–3 days; L = 3–5 days; XL = must be split
**Priority key:** P0 = product does not function without this; P1 = ships with v1 of this journey; P2 = next iteration

**Build sequence (hard ordering enforced by dependency chain):**
1. INSESSION-002 (session start, program load)
2. INSESSION-001 (trial recording — core data write)
3. INSESSION-003 (timer and counter — display layer on top of active session)
4. INSESSION-004 (prompt level — field extension on trial record)
5. INSESSION-005 (behavior recording — parallel data type to trial records)
6. INSESSION-006 (session summary — computed from all above)
7. INSESSION-007 (data sync — infrastructure after local record is finalized)
8. INSESSION-008 (supervisor notification — triggered by sync completion)

---

## Pre-Build Decisions

These decisions must be made and documented before any story in this journey enters engineering sprint planning. They are not acceptance criteria — they are architectural and design choices that will constrain implementation across all eight stories.

**Decision 1 — Trial record data model (cross-journey dependency with PROG- stories)**

The trial record schema must be defined jointly with the PROG- (Clinical Program Design) data model before any INSESSION- story is implemented. The trial record must reference: child ID, session ID, target ID, program version ID (to handle program updates mid-treatment), therapist ID, prompt level (as an enum, not free text), outcome (Correct / Incorrect / Prompted), timestamp (ISO 8601 UTC), and sync status. The program version ID is critical: if Dr. Sunita updates the therapy program mid-month, sessions before and after the update must be queryable against the correct program version. Without this field, progress trend data across a program revision becomes ambiguous. This schema decision cannot be deferred — it determines the shape of every table in the clinical data layer.

**Decision 2 — Offline storage engine choice**

The local data store must support: atomic writes per trial record, surviving app process kill and device restart, background sync queue management, and encryption at rest. Candidate options include SQLite with Room (Android Architecture Components — recommended for minimum-spec Android 10+ compatibility), Realm, or a custom queue. The choice must be confirmed before INSESSION-001 is specced for engineering. The selected engine is used by every INSESSION- story, the PROG- stories, and the SCHED- (scheduling / attendance) stories — it is a platform-level decision, not a journey-level decision.

**Decision 3 — One-handed interaction pattern and outcome button layout**

The Active Session Screen interaction design must be validated as a design prototype before INSESSION-001 enters development. The core question: can Priya reliably tap the correct outcome button (Correct / Incorrect / Prompted) with one hand on a 5.5–6.5 inch Android screen, at clinical speed, without looking at the screen for confirmation (relying on haptic instead)? The layout options (vertical stack, horizontal row, radial arrangement) each have different one-handed reach profiles on different device sizes. This must be tested on physical Redmi/Realme devices — not on emulators. A design prototype review with the Design Consultant agent is the recommended gate before sprint planning.

**Decision 4 — Session type (DTT vs. NET) and data model fork**

The eight stories above are scoped to DTT (Discrete Trial Training) — the structured format where each trial has a clean boundary and a binary/ternary outcome. Natural Environment Teaching (NET) uses an interval recording model rather than a trial-by-trial model. The decision of whether to build DTT-only first or to build the session type abstraction (DTT and NET as parallel recording modes) upfront must be made before INSESSION-002 is finalized. Building DTT-only first is faster but may require a data model migration when NET is added. Building the abstraction upfront adds complexity to the first release. This decision directly affects the session record schema, the Active Session Screen branching logic, and the session summary computation.

**Decision 5 — ABC dropdown pre-configuration ownership and cadence**

Stories INSESSION-005 (behavior recording) and INSESSION-004 (prompt levels) both rely on per-child dropdown configurations that are managed by Dr. Sunita as part of the therapy program (PROG- stories). If PROG- stories are not yet built when this journey is implemented, a fallback must be defined: either a center-level default dropdown list (less clinically precise but unblocking) or a hard gate (behavior recording cannot be used without per-child configuration). This is a product decision that determines how tightly INSESSION- stories are coupled to PROG- stories. A center-level default list is the recommended fallback to allow INSESSION- to be tested and validated before PROG- is built.

**Decision 6 — Haptic feedback specification for minimum-spec Android devices**

Haptic feedback is described as non-negotiable across INSESSION-001, INSESSION-003, INSESSION-004, and INSESSION-005. On minimum-spec Android 10+ devices (Redmi/Realme 2GB RAM class), the haptic actuator quality and API support varies significantly. The Android VibrationEffect API (available on API 26+) must be confirmed as the implementation standard, and the specific waveform pattern for each feedback type (trial recorded, behavior logged, session end) must be specified and verified on physical test devices before implementation. Haptic "confirmation" that is too weak or absent on a subset of target devices is a functional failure — not a cosmetic one.

---

## ⚠️ Feature Factory Disclaimer

These requirements were defined from journey document synthesis, ABA clinical domain knowledge, and competitive observation of US ABA platforms (Motivity, CentralReach, Catalyst, Hi Rasmus) — not from validated primary research with Indian therapy centers.

**What we assumed but have not validated:**

- [ASSUMPTION] Indian special educators (Priya) actually record trial-by-trial data during live sessions in the current paper-based workflow. If most Indian centers do not do trial-by-trial recording at all (i.e., the behavior has not yet been established), the entire interaction model of this journey may need to change before any build investment is made. (Hypothesis H-01 in journey map — highest priority to validate.)
- [ASSUMPTION] Session rooms in Indian therapy centers have sufficiently unreliable connectivity to require offline-first as a hard design constraint rather than a graceful degradation. (Hypothesis H-03 in journey map — must be validated by on-site connectivity testing before the offline architecture is committed.)
- [ASSUMPTION] The one-handed interaction model (outcome buttons designed for one-handed tap while managing the child) translates from US ABA clinical context to Indian therapy center context. The physical workflow of Indian special educators — who may work with children very differently from the US ABA DTT model — must be observed directly before the Active Session Screen layout is locked.
- [ASSUMPTION] Low-end Android (Redmi/Realme 2GB RAM) is the correct primary device target. If primary research reveals that Indian therapy centers provide dedicated tablets to therapists or that therapist personal devices are higher-spec than assumed, the device constraint changes meaningfully.
- [ASSUMPTION] The PROG- (Clinical Program Design) data model will be built and available when this journey is eventually implemented. All eight INSESSION- stories have hard dependencies on structured, digital therapy program records. If PROG- is not built first, these stories cannot be implemented as specified.

**What a researcher would ask before building this:**

- Do Indian special educators currently record discrete trial data at all during live sessions, or do they record summary-level data (e.g., "worked on matching today — went okay") at session end? The answer determines whether this journey is a digital replacement for an existing behavior or a behavior change effort.
- Is the one-handed interaction constraint as acute in Indian centers as in US ABA settings? Do some Indian therapy center session formats allow the therapist to set the child up in a structured task and step back briefly to record — reducing the one-handed urgency?
- What maladaptive behavior types are most commonly tracked in Indian autism therapy centers, and how do supervisors currently use ABC data to adjust behavior intervention plans? This shapes whether the ABC capture flow (INSESSION-005) is clinical infrastructure or overhead.

**What the Product Consultant would challenge:**

- This entire journey is scoped for a future market (US / international) or an India-specific use case that has not yet been confirmed to exist (trial-by-trial recording without a reimbursement driver). The data model decisions flagged in Pre-Build Decision 1 (trial record schema) may be the only output of this document that should be acted on before primary research validates the India demand signal. Everything else should remain in a parking lot until that research is complete.
- The dependency chain (PROG- must be built before INSESSION- can function) means this journey cannot be built incrementally without significant prior investment. The Pre-Build Decisions are likely to surface that the real cost of this journey is borne in PROG- and the offline sync infrastructure — not in the UI layer. Scope that dependency chain before any estimates are committed.

**Risk level:**

- INSESSION-001, INSESSION-002, INSESSION-006: High risk — core interaction model is unvalidated for Indian therapy context. Do not build without primary observation research.
- INSESSION-003, INSESSION-004: Medium risk — timer and prompt level logging are additive features on top of the core trial recording model. Lower independent risk but still dependent on the core model being validated.
- INSESSION-005: High risk — maladaptive behavior recording and ABC capture are specific to a clinical workflow (behavior intervention planning) that may be structured very differently in Indian centers than in US ABA contexts.
- INSESSION-007, INSESSION-008: Low-to-medium risk — offline sync and supervisor notification are infrastructure and coordination features. The patterns are well-established. Risk is primarily in the data model design (Pre-Build Decision 1) and the RBAC implementation, not in the user-facing behavior.

Use the /researcher agent to validate H-01, H-03, and H-05 from the hypothesis register before this journey is brought into sprint planning.
Use the /product-consultant agent to scope the PROG- dependency chain before Pre-Build Decisions 1 and 4 are resolved.
Use the /design-critique agent to review the Active Session Screen prototype (Pre-Build Decision 3) before INSESSION-001 enters development.
