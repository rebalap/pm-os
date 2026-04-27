# User Journey: Supervisor Review & Program Updates

> ❌ **OUT OF SCOPE — MVP**
> **Decision date:** 22 April 2026 | **Decision by:** Engineering + Product
> **Rationale:** Deferred as part of Journey 4 (Clinical Program Design). Structured program update workflows require a digital program management system to exist first. The supervisor review of individual session notes (Journey 6) is in scope — what is deferred is the structured clinical workflow of modifying targets, prompt levels, and reinforcement schedules in a digital program record.
> **Deferred to:** Post-MVP release
> **Reference:** `meetings/engineering/2026-04-22-engineering-alignment-meeting-summary.md`

**Previously:** J2 (extension) | ❌ **OUT OF SCOPE — MVP (Deferred with Journey 4)**
**Trigger:** Dr. Sunita sits down to review accumulated session data and update the therapy program — typically weekly or fortnightly
**Primary actor:** Dr. Sunita (Clinical Supervisor / Senior Therapist)
**Supporting actors:** Priya (receives updated program); Rahul (may be notified of significant program changes)
**Entry condition:** Session notes exist for the child (Journey 6); therapy program exists in the system (Journey 4 — also deferred); supervisor has Supervisor role access
**End state:** Progress reviewed per target; mastered targets advanced; plateau targets modified; updated program pushed to therapist's view; program version history maintained
**Journey source documents:**
- *(Depends on Journey 4 feature cluster — not yet written)*

---

## Discovery Context

**MVP Scope:** ❌ OUT OF SCOPE — Deferred with Journey 4 (Clinical Program Design)

**Why this journey is deferred:**

This journey cannot be built meaningfully without Journey 4 (Clinical Program Design). The program update workflow requires a digital program record to modify — targets, prompt levels, reinforcement schedules, mastery criteria, and program version history must all exist in a structured digital form before a supervisor can interact with them. The MVP does not include Journey 4, which means there is no digital program record for Dr. Sunita to update. What is in scope for the MVP is the lighter version of supervisor oversight: reviewing individual session notes (Journey 6) and monitoring the caseload dashboard for attendance and overdue flags (Journey 3). The full clinical supervision loop — data-driven program modification, mastery tracking, version-controlled updates pushed to therapists — belongs to post-MVP.

There is an adoption risk associated with this deferral: clinical program management is the core value proposition for supervisors. If primary research confirms that Dr. Sunita will not adopt the platform without this feature, the deferral decision must be revisited before scope is locked.

**Pain points & friction (current state):**
- Manual calculation of progress metrics is time-consuming and error-prone 🔵 Inferred from ABA Matrix documentation burden finding
- 2–3 hours/day on documentation in non-automated practices (US figure) — Indian equivalent unvalidated but likely directionally true 🔶 [HYPOTHESIS] ✅ Source: ABA Matrix
- Review happens in batch — a child may be running an outdated program target for 1–2 weeks before supervisor notices ✅ BHCOE: "supervisor can analyze data only every one or two weeks" with paper
- Program update communication to Priya is verbal — high risk of being misapplied or misremembered 🔶 [HYPOTHESIS]
- No version history for the therapy program — what was the target prompt level 4 weeks ago? 🔵 Inferred as a structural gap
- Collecting paper data sheets from Priya's physical file or reading WhatsApp photos introduces risk of data loss and DPDPA exposure 🔶 [HYPOTHESIS] ⚠️ DPDPA — WhatsApp photo of child's clinical data is unencrypted transmission of minor's health data

**Emotional states:**
- Dr. Sunita: Cognitively taxed — this is complex analytical work done in fragmented time, often outside clinical hours 🔶 [HYPOTHESIS]
- Priya: Uncertain about program changes until explicitly told — may continue running outdated targets if communication breaks down 🔶 [HYPOTHESIS]

**Current workarounds:**
- Some supervisors maintain handwritten "master notebooks" per child with program versions — a single point of failure 🔶 [HYPOTHESIS]
- Verbal "stand-up" at start of day to communicate program changes — relies on memory and attendance 🔶 [HYPOTHESIS]
- Dr. Sunita manually calculates percentage correct per target using mental arithmetic or a calculator; occasionally plots trends in Excel if transcription has happened 🔶 [HYPOTHESIS]

---

## Conceptual Step-by-Step Flow

> ⚠️ This flow is conceptual — for post-MVP planning only. Requires Journey 4 (Clinical Program Design) to be built first.

| Step | Actor | Action | Screen / State | Technical Note |
|---|---|---|---|---|
| 1 | Dr. Sunita | Opens the Supervisor Caseload Dashboard. Reviews the list of children under her supervision. Sorts by "Last program update" to identify children whose programs are overdue for review (threshold: 14 days since last update). | Supervisor Caseload Dashboard — Program Review View | Reads: all children in caseload, last program update date per child, session count since last program update, overdue program flag (configurable threshold). Overdue flag is text + color — never color alone. Future / not specced. |
| 2 | Dr. Sunita | Taps a child's row to open their clinical record. Lands on the Program & Data tab — not the profile tab. Sees: active program summary (list of current targets, prompt levels, mastery criteria), and a data summary for the review period. | Child Clinical Record — Program & Data Tab | Reads: active therapy program record (from Journey 4), session data records for the review window (from Journey 5 — in-session data collection, also deferred), session notes from Journey 6. If Journey 5 data is unavailable (India MVP context), this view would rely solely on session notes and manually entered progress observations. Future / not specced. |
| 3 | Dr. Sunita | Reviews the data for each active target. For each target, the system displays: number of sessions this target was run, accuracy per session (percentage correct), and a trend line over the review window. Dr. Sunita identifies which targets have reached mastery criteria, which are progressing, and which are plateauing or regressing. | Target Progress View — Per-Target Data Grid | Reads: trial records aggregated by target, computed accuracy per session, configurable mastery threshold (e.g., 80% correct over 3 consecutive sessions). Mastery badge displayed when threshold is met. Future / not specced. |
| 4 | Dr. Sunita | For a target that has met mastery criteria: taps "Advance Target". Selects next phase from a menu — options include: Fade prompt level (e.g., full physical → partial physical → gesture → independent), Generalize to new context, or Maintain and move on. Adds a brief clinical note on the change. | Target Modification Panel — Mastery Advance flow | Writes: program version event (target ID, change type = mastery advance, new prompt level or phase, clinical note, timestamp, author). Old program version is preserved in version history — not overwritten. Future / not specced. |
| 5 | Dr. Sunita | For a target that is plateauing or regressing: taps "Modify Target". Reviews options — change prompt level, modify reinforcement schedule, change teaching format (DTT → NET), or flag for supervision discussion. Selects modification and adds rationale note. | Target Modification Panel — Plateau/Regression flow | Writes: program version event (target ID, change type = modification, specific change made, rationale, timestamp, author). The modification reason is required — cannot save without selecting a reason category. Future / not specced. |
| 6 | Dr. Sunita | Reviews the full program after changes. Sees a summary of what has changed since the last version: targets advanced (N), targets modified (N), targets with no change (N). Confirms the update is ready to push to Priya. Taps "Publish Update". | Program Update Summary Screen | Reads: diff between current program version and last published version. Writes: new program version record (version number, timestamp, author, list of changes). Old version remains accessible in version history. Status changes from Draft → Published. Future / not specced. |
| 7 | System | Published program update is pushed to Priya's view. A notification appears on Priya's home screen: "[Child name]'s program has been updated. X targets changed. Review before your next session." | Background notification → Priya's Home Screen | Writes: program update notification event (child ID, version number, change summary, therapist IDs for this child). Priya's My Sessions view shows a "Program updated" badge on the affected child's session card. Future / not specced. |
| 8 | Priya | Taps the "Program updated" badge on the session card. Reviews the change summary — which targets changed and how. The changes are displayed as a diff: "Requesting was: Full physical prompt → Now: Partial physical prompt." Priya marks the update as reviewed. | Program Update Review Screen — Therapist View | Reads: program change diff (new vs. previous version, per-target). Writes: therapist acknowledgement record (therapist ID, timestamp of review, program version confirmed). Acknowledgement is visible to Dr. Sunita in the version history. Future / not specced. |
| 9 | Dr. Sunita | At the end of the review session, optionally records a supervision note — a brief summary of clinical observations across the caseload review. May flag specific children for a direct supervision conversation with Priya. | Supervision Note Screen | Writes: supervision note record (free text, linked to child IDs flagged, timestamp). Supervision notes are separate from session notes — they represent the supervisor's clinical judgment rather than session observation. Future / not specced. |
| 10 | Dr. Sunita | Returns to the Caseload Dashboard. The "Last program update" timestamp for reviewed children now shows today's date. Overdue program flags have cleared. | Supervisor Caseload Dashboard — updated | Reads: refreshed caseload list with updated timestamps. Program review workflow is complete for this cycle. Future / not specced. |

---

## Decision Points (Conceptual)

### Decision 1: Target has reached mastery criteria

**At step:** 4 (target advance flow)

**Context:** A target is considered mastered when it meets the center's configured mastery threshold — typically 80% or higher accuracy across 3 or more consecutive sessions. Mastery does not mean the skill is fully generalized; it means the child has demonstrated consistent performance under the current teaching conditions and is ready for the next phase.

- **Path A — Advance to next prompt level:** Prompt fading is the standard ABA progression. If the child is at full physical prompt and has mastered the target, Dr. Sunita advances to partial physical prompt. The target remains active but with a modified prompt level. The next review cycle will assess whether the child maintains mastery at the new prompt level.
- **Path B — Generalize to new context:** The child has mastered the target in the therapy room with Priya. Dr. Sunita marks the target as "Generalization phase" — the target now needs to be practiced in a different context (with a different therapist, in a different room, or as a home program activity assigned to Meena). A generalization note is added specifying the new context.
- **Path C — Retire the target and introduce next target:** If the target has been mastered and generalized, Dr. Sunita marks it as Complete, archives it in the program history, and introduces a new target at the appropriate level from the child's therapy domain. The new target is drafted here and immediately becomes part of the published program.
- **Design implication:** Mastery criteria thresholds must be configurable per center and per child — the 80%/3 session default is common in ABA literature but not universal. Dr. Sunita must be able to override the automated mastery flag with her clinical judgment; the system can surface the data, but the advancement decision belongs to the clinician.

---

### Decision 2: Target is plateauing or regressing

**At step:** 5 (target modification flow)

**Context:** A target is plateauing when accuracy has been flat (no upward trend) for 2+ consecutive sessions. A target is regressing when accuracy has declined from a previously higher level. Both conditions require clinical attention and possible program modification.

- **Path A — Modify the prompt level:** If the target was advanced too quickly (prompt faded before the child was ready), Dr. Sunita increases the prompt level — returning to a more supportive level to rebuild consistent responding. This is a common intervention when accuracy drops after a prompt fade.
- **Path B — Modify the reinforcement schedule:** If the child has lost motivation for the current reinforcer, Dr. Sunita changes the reinforcement schedule or reinforcer type. This requires coordination with Priya, who knows the child's current preferred items. The modification note should capture the reasoning and the new reinforcer to use.
- **Path C — Change teaching format:** If DTT is not working for this target, Dr. Sunita may switch to NET (natural environment teaching) to build the skill in a less structured context. This is a significant procedure change — it affects how Priya runs the session and requires clear communication, not just a digital program update.
- **Path D — Flag for supervision discussion:** If the plateau is persistent or unexpected, Dr. Sunita flags the target for a face-to-face supervision conversation with Priya before making a program change. The flag is visible in the program but does not publish a version update until the conversation has happened and a direction is agreed.
- **Design implication:** The system should surface plateau and regression signals automatically — Dr. Sunita should not need to scan raw numbers to identify problem targets. Automated flags (configurable threshold: flat trend over N sessions) should draw her attention to targets needing review while she retains full clinical authority over the response.

---

### Decision 3: Program change communication to therapist

**At step:** 7–8 (program publish and therapist acknowledgement)

**Context:** Once Dr. Sunita publishes a program update, Priya needs to see and internalize the changes before her next session with the child. The risk in the current paper-based workflow is that Priya misses or misremembers program changes — running yesterday's targets at yesterday's prompt levels while the program has already been updated.

- **Path A — Digital push notification + in-app acknowledgement (in-scope design):** When the program is published, Priya receives a push notification on her Android phone. She reviews the change diff and taps "Acknowledged" before her next session. Dr. Sunita can see that Priya has confirmed review. This is the intended digital workflow.
- **Path B — Priya does not acknowledge before the next session:** The child's session card in Priya's My Sessions view continues to show the "Program updated — review required" badge. If the session begins (attendance marked as Present) without acknowledgement, the system records that the session ran under an unreviewed program update. This is a clinical risk flag visible to Dr. Sunita in the supervision view.
- **Path C — Program change requires a verbal discussion (not just a notification):** Some changes — particularly format changes (DTT → NET) or significant procedure modifications — cannot be communicated effectively through a text diff alone. Dr. Sunita flags these changes as "Requires verbal briefing" when publishing. The notification to Priya includes: "This update requires a discussion with Dr. Sunita before your next session." The session is not blocked, but the flag remains until Dr. Sunita manually marks the verbal briefing as complete.
- **Design implication:** Acknowledgement is important but must not create friction that discourages Dr. Sunita from publishing updates. The diff view for Priya must be genuinely easy to read — "Target X changed from [old] to [new]" in plain language, not a clinical data grid. The therapist acknowledgement is a safety mechanism, not a compliance gate.
