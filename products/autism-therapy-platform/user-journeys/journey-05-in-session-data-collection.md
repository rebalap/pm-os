# User Journey: In-Session Data Collection (Behavioral Data)

> ❌ **OUT OF SCOPE — India MVP**
> **Decision date:** 22 April 2026 | **Decision by:** Product
> **Rationale:** Indian therapy is paid out-of-pocket. No insurance reimbursement system creates an external driver for trial-by-trial data logging. This is a strong differentiator for US and international markets where insurance authorization requires granular clinical documentation.
> **Future scope:** US / international market expansion
> **Reference:** `meetings/engineering/2026-04-22-engineering-alignment-meeting-summary.md`

**Previously:** *(No prior J-number)* | ❌ **OUT OF SCOPE — India MVP**
**Trigger:** A therapy session begins and the therapist needs to record trial-by-trial behavioral data in real time
**Primary actor:** Priya (Special Educator / Behavior Therapist)
**Supporting actors:** Dr. Sunita (Clinical Supervisor — reviews data); Arjun (child — shapes the physical constraints of the workflow)
**Entry condition:** Child is enrolled with active DPDPA consent (Journey 0); therapy program is designed with defined targets (Journey 4); session is scheduled and attendance marked as Present (Journey 3)
**End state:** All trials for the session are recorded (correct/incorrect/prompted); maladaptive behavior frequency logged; ABC data captured; session data immediately visible to supervisor without a paper handover step
**Journey source documents:**
- *(No existing feature cluster — net-new build; feature stories to be written post-MVP)*

---

## Discovery Context

**MVP Scope:** ❌ OUT OF SCOPE — India MVP (US/international future opportunity)

**Why this journey matters (long-term):**

This is the foundational break point identified in the original journey analysis — every downstream feature (supervisor review, progress reports, billing accuracy) depends on the quality of data captured here. The MVP accepts this limitation by design. In-session data collection is where clinical value creation begins: without accurate trial-by-trial data, supervisor review is based on recalled impressions rather than evidence, program updates are guesses rather than data-driven decisions, and progress reports are narratives rather than trend analyses. The entire clinical intelligence stack — supervision, reporting, home programs — depends on what gets recorded in the session room. When this journey is eventually built, it will be the make-or-break adoption moment: if therapists do not record data during live sessions, no downstream feature has the input it needs to function.

The reason this is deferred for India specifically is structural: in Indian therapy centers, families pay out-of-pocket. There is no insurance authorization cycle, no payor audit, and no external mandate requiring granular trial-by-trial documentation. In the US, insurance companies require detailed session logs as a condition of reimbursement — which creates an unavoidable forcing function for in-session digital data collection. India does not have this driver at the current stage of the market. Monitor primary research for signal on whether Indian centers would adopt in-session digital data collection even without a reimbursement driver.

**Pain points & friction (current paper-based state):**
- One-handed constraint: marking paper while managing a child's activity with the other hand is physically awkward and causes data entry errors 🔵 Inferred from ABA clinical context and global design standard
- Retrospective ABC data: the antecedent is often forgotten by session end — ABC notes are incomplete or inaccurate 🔵 Inferred from clinical documentation literature
- Paper illegibility: "unclear handwriting that often occur with paper systems" — transcription errors compound ✅ ResearchGate peer-reviewed comparison study on electronic vs. paper DTT data collection
- Delayed supervisor feedback: with paper, supervisor "may be able to analyze data only every one or two weeks" ✅ BHCOE research
- Connectivity unknown: if a mobile tool were introduced, session room connectivity may be unreliable — making offline-first a likely hard requirement 🔶 [HYPOTHESIS]
- No automatic graph or trend generation from paper data — supervisor must manually plot or calculate progress 🔵 Inferred

**Emotional states:**
- Priya during session: Fully focused on the child — data collection is secondary to session management. Feels the tension between giving full attention to the child and accurately recording outcomes. 🔵 Inferred from "one-handed constraint" documented in US ABA literature; applies structurally to any therapist doing live data collection
- Priya post-session: Relief. Possibly rushed — next child may be waiting. 🔶 [HYPOTHESIS]
- Dr. Sunita reviewing data: Frustrated by illegibility, inconsistent formats, missing entries. 🔵 Inferred from documented paper failure modes

**Current workarounds:**
- Some therapists write abbreviated tally codes they alone understand — reducing transcription time but creating handover risk 🔶 [HYPOTHESIS]
- WhatsApp photo of paper data sheet sent to supervisor as a shortcut to physical handover 🔶 [HYPOTHESIS] ⚠️ DPDPA — photo of child's clinical data sent via WhatsApp is unencrypted transmission of minor's health data
- Retrospective session note written from memory at day end, not in-session 🔶 [HYPOTHESIS]

**Key design constraints (for when this journey is built):**
- One-handed operation — therapist cannot pause the session
- ≤ 2 taps to record a trial outcome
- Haptic feedback preferred over audio (noisy environment)
- Offline-first — session room connectivity may be unreliable
- Low-end Android device compatibility (Redmi, Realme class)
- No complex navigation during session — target selection must happen before session starts, not during trials
- Arjun's behavioral profile shapes the physical workflow: some children require constant physical proximity and contact, making even a one-handed phone interaction a moment of potential behavioral disruption

---

## Conceptual Step-by-Step Flow

> ⚠️ This flow is conceptual — for post-MVP planning only. No implementation has been specced or approved.

| Step | Actor | Action | Screen / State | Technical Note |
|---|---|---|---|---|
| 1 | Priya | Opens the app before the session starts. Navigates to the child's session from "My Sessions" view. Taps "Start Session" on the session card. | My Sessions Screen → Session Start Screen | Reads: today's session for this child, active therapy program targets (pulled from Journey 4 program record). Session start creates a session instance record with status = In Progress. Future / not specced. |
| 2 | Priya | Reviews the session program — a pre-loaded list of today's target behaviors and their current prompt levels. Confirms the program is current before beginning trials. Taps "Begin Recording". | Session Program Preview Screen | Reads: child's active therapy program, target list for this session, prompt level per target, reinforcement schedule. Priya cannot edit targets from this screen — program modifications are Dr. Sunita's role. Future / not specced. |
| 3 | Priya | Selects the first target from the target list. The target name and current prompt level are displayed prominently. Session begins with the child. | Active Session Screen — Target View | Displays: target name, prompt level (e.g., "Full physical prompt"), trial counter, three large response buttons (Correct / Incorrect / Prompted). Target list remains accessible via a bottom sheet but is not displayed during trial recording to minimize screen complexity. Future / not specced. |
| 4 | Priya | Runs a discrete trial (DTT) with the child. At the end of the trial, taps the outcome: Correct (green), Incorrect (red), or Prompted (yellow). Haptic confirmation fires immediately on tap. | Active Session Screen — Trial Recording | Writes: trial record (target ID, outcome, timestamp). ≤ 1 tap to record a trial outcome. Trial counter increments. No confirmation dialog — tap registers immediately. Offline-first: writes to local store; syncs in background. Future / not specced. |
| 5 | Priya | Completes the programmed number of trials for the first target (typically 10 discrete trials per session per target). Swipes to the next target or taps "Next Target" in the bottom sheet. | Active Session Screen — Target Transition | Writes: target block complete marker with timestamp. Displays brief summary of block just completed (e.g., "8/10 correct — 80%"). Transition to next target is a single tap or swipe. Future / not specced. |
| 6 | Priya | During the session, a maladaptive behavior episode occurs (e.g., child hits the table, self-harms, has a tantrum). Priya taps the behavior counter button (a persistent floating button on the session screen). | Active Session Screen — Maladaptive Behavior Counter | Writes: behavior frequency tally (behavior type, timestamp, session phase). Behavior counter is a persistent element — always visible regardless of which target is displayed. Minimum tap target size. Haptic on every tap. Future / not specced. |
| 7 | Priya | After the episode, she has a 30-second window to add ABC data (Antecedent, Behavior, Consequence). A compact ABC capture panel slides up from the bottom. She selects antecedent and consequence from short dropdown menus (pre-configured per child). | ABC Data Capture Panel (bottom sheet overlay) | Writes: ABC record linked to behavior frequency entry (antecedent category, consequence category, free-text note — optional). Panel is non-blocking — session can continue if Priya dismisses it. Future / not specced. |
| 8 | Priya | Completes all programmed targets for the session. Taps "End Session". Reviews a session summary screen — trials per target, accuracy per target, maladaptive behavior count. | Session End Summary Screen | Reads: all trial records for the session, computed accuracy per target (correct / (correct + incorrect + prompted)), behavior frequency summary. Priya cannot edit trial records from this screen. Future / not specced. |
| 9 | Priya | Optionally adds a post-session narrative note — a brief free-text comment on child's mood, engagement, or any clinical observations not captured in structured data. Taps "Save and Close". | Session Note field (within Session End Summary) | Writes: session note text linked to session record. Pre-fills structured data into the note where possible (e.g., "Arjun completed 30 trials across 3 targets. Accuracy: 80% on Matching, 60% on Imitation, 40% on Requesting."). Future / not specced. |
| 10 | System | Session data syncs to the server when connectivity is available. Session status transitions from In Progress → Completed. Dr. Sunita's supervisor caseload dashboard is updated. | Background sync | Writes: full session record including all trial data, behavior frequency data, ABC records, session note — to server. Triggers: supervisor notification (if configured), progress data refresh. DPDPA note: all session data for a minor must be encrypted at rest and access-scoped to assigned staff + supervisor + admin. Future / not specced. |
| 11 | Dr. Sunita | Opens the child's clinical record from her Supervisor Caseload Dashboard. Navigates to the Session Data tab. Sees the latest session's trial data in a table and graph view — accuracy per target, trend over last N sessions. | Child Clinical Record — Session Data Tab (Supervisor View) | Reads: all session records for this child, accuracy per target per session, computed trend lines (moving average over configurable window). Supervisor can filter by target, by date range, by therapist. Future / not specced. |

---

## Decision Points (Conceptual)

### Decision 1: DTT vs NET session type

**At step:** 2–4 (program preview and trial recording)

**Context:** Discrete Trial Training (DTT) is a structured, repetitive format where each trial has a clear beginning, instruction, response, and consequence — making trial-by-trial recording straightforward. Natural Environment Teaching (NET) is play-based and less structured — "trials" are embedded in natural interactions and may not have clean boundaries.

- **Path A — DTT session:** Trial recording maps directly onto the step-by-step flow above. Each discrete trial is recorded with an outcome. Trial count per target is the primary data structure.
- **Path B — NET session:** Trial recording is less granular. The screen would switch to an interval recording or event recording mode — Priya records behavioral occurrences within time intervals (e.g., "Did the child spontaneously request an item in the last 5 minutes?") rather than trial outcomes. The data structure is observation-based, not trial-based. The target list and recording interface must adapt to the session type selected at step 1.
- **Design implication:** Session type must be selectable at session start (step 1). The recording UI shown in steps 3–5 applies to DTT. NET requires a parallel UI that presents interval-based prompts rather than trial outcome buttons. Both must meet the ≤ 2 tap, one-handed, offline-first constraints.

---

### Decision 2: Connectivity loss during session

**At step:** 4–7 (trial recording in progress)

**Context:** Session rooms in Indian therapy centers may have intermittent or absent mobile data. Offline-first is listed as a likely hard requirement (H-03 — [HYPOTHESIS], not yet validated).

- **Path A — Online throughout session:** Trial records write to local store and sync to server continuously. No visible difference to Priya — sync happens silently in background. Supervisor data refreshes in near-real-time.
- **Path B — Connectivity lost mid-session:** App continues to function without interruption. All trial records, behavior frequency tallies, and ABC data are written to local storage. A non-intrusive banner ("Offline — data saved locally") confirms to Priya that recording is continuing safely. No data loss.
- **Path C — Connectivity not restored before session end:** Full session record is stored in local queue. Syncs to server when any data connection is available — could be minutes or hours after session end. Supervisor sees session data after sync completes, not in real time. In the meantime, supervisor's caseload dashboard shows "Data pending sync" for this session.
- **Design implication:** Offline-first is not a fallback mode — it is the primary behavior. The local write is the authoritative record; the server sync is eventual consistency. Data must survive app close, device restart, and delayed connectivity restoration.

---

### Decision 3: Maladaptive behavior episode occurs

**At step:** 6–7 (behavior counter and ABC capture)

**Context:** Maladaptive behavior episodes are high-stakes clinical events that must be recorded without interrupting the session. The therapist's first obligation during a behavioral episode is to manage the child — not to enter data.

- **Path A — Priya taps the floating behavior counter button during the episode:** Single-tap frequency count recorded with timestamp. Session continues uninterrupted. The 30-second ABC capture window opens after the tap but is dismissable — Priya can fill it in immediately or immediately after the episode subsides.
- **Path B — Priya cannot tap during the episode (both hands occupied managing the child):** After the episode resolves, Priya taps the behavior counter. The system records the behavior with the current timestamp. She can manually adjust the timestamp in the ABC panel if the actual onset time was earlier. Timestamp editing must be limited to ±5 minutes from session time to maintain data integrity.
- **Path C — Episode severity requires session stop:** Priya taps "Pause Session" (a secondary control, less prominent than trial recording). Session status = Paused. Timer stops. Data is preserved. Priya manages the child and resumes when appropriate, or taps "End Session Early" if the episode concludes the session. A reason code is recorded (behavioral incident, child dysregulation, safety concern).
- **Design implication:** The behavior counter must be a persistent floating element on every screen state during an active session — not buried in a menu. Haptic feedback on the behavior counter tap is essential in noisy environments. ABC capture must be non-blocking — a therapist who is managing a behavioral episode cannot be locked into a data entry flow.
