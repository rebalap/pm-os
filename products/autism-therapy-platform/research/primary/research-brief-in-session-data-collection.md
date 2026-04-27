# Research Brief: In-Session Data Collection Workflows for Special Educators and Behavior Therapists in Indian Autism Therapy Centers

**Product:** Autism Therapy Platform (India)
**Date:** 2026-04-13
**Stage:** Discovery
**Decision to inform:** Do we have a clear enough understanding of in-session data collection workflows and pain points to define what problem we're solving — and where a software tool would genuinely fit alongside an existing digital intervention tool, Cognitivebotics?
**Recommended methods:** Contextual inquiry (observed sessions), semi-structured interviews, artifact collection (review of current paper forms, WhatsApp logs, and spreadsheet templates in use)

---

## Why This Research, Why Now

Indian autism therapy centers have no dominant software solution — clinical staff operate on paper, WhatsApp, and personal spreadsheets. Before any product decisions are made, we need to understand what actually happens during a session: what data is captured, when, how, and at what cost to the therapist and the child. We also need to understand where Cognitivebotics already sits in this workflow so we design for genuine complementarity rather than duplication or conflict.

The cost of skipping this research is high. We would be building around [ASSUMPTION]-level beliefs about what is painful, what is disruptive, and what therapists would actually use during a live session with an active child. An incorrect starting point at Discovery will cascade into a mis-scoped PRD, a misfit design, and a product that staff ignore in practice.

---

## Research Questions

| # | Question | Method | Rationale |
|---|---------|--------|-----------|
| 1 | What data does a special educator or behavior therapist actually record during a live session, and at what moments in the session does recording happen? | Contextual inquiry (observed session) | Self-report is unreliable for in-the-moment behaviors; we need direct observation to see what is captured, skipped, or deferred |
| 2 | What friction, errors, or workarounds arise from current paper/WhatsApp/spreadsheet-based data collection — and which of these do therapists experience as genuinely disruptive versus acceptable? | Semi-structured interview + artifact review | We need to distinguish real pain from tolerated inconvenience; artifacts (forms, spreadsheet templates, WhatsApp threads) reveal actual practice, not idealized descriptions |
| 3 | How does Cognitivebotics currently fit into the session workflow — what does it do, when is it used, and what does it not cover? | Semi-structured interview + contextual inquiry | We cannot design a complementary tool without understanding the exact scope and touchpoints of the existing tool; overlap risks create adoption failure |
| 4 | What happens to session data after a session ends — who uses it, for what purpose, and how quickly does it need to be available? | Semi-structured interview | Data collection is only meaningful if the downstream use is understood; this shapes whether real-time capture or end-of-session capture is the right model |
| 5 | What are the physical and environmental constraints of data collection during a live session — device handling, noise, interruptions, child behavior, space? | Contextual inquiry (observed session) | Constraints on one-handed use, screen visibility, and cognitive load cannot be inferred from interviews alone; direct observation is required |
| 6 | How do clinical supervisors currently use session data — what format do they need it in, how often do they review it, and where does the current process break down for them? | Semi-structured interview | Supervisor workflows are a distinct use case from in-session capture; understanding their needs will reveal whether a single tool can serve both or whether they are separate problems |

---

## Key Assumptions Being Tested

- [ASSUMPTION] Special educators and behavior therapists find paper- and WhatsApp-based data collection disruptive enough during live sessions that they would adopt a mobile software alternative — because our product context asserts this is a primary pain, but we have no direct user evidence confirming the disruption threshold or willingness to change behavior
- [ASSUMPTION] Cognitivebotics does not cover in-session behavioral data collection — because our complementarity hypothesis depends on this gap being real and clearly bounded; if Cognitivebotics already captures this data, the problem definition changes significantly
- [ASSUMPTION] Offline-first capability is a hard requirement, not a nice-to-have — because session environments may have poor connectivity, but we do not yet know how often this actually affects workflows or whether therapists have found workarounds
- [ASSUMPTION] English-only UI is acceptable for therapist-facing features in metro markets at launch — because metro-based centers may have English-comfortable staff, but we have not confirmed whether clinical staff in these centers actually prefer or tolerate English in a time-pressured session context
- [ASSUMPTION] Core data entry actions must be completable in two taps or fewer — because the session context demands minimal interruption, but we do not yet know what the actual minimum viable data capture looks like in practice

---

## What Good Looks Like

We will be ready to move from Discovery to Define when:

- We have directly observed at least 3 live therapy sessions across at least 2 different centers, covering both individual and group session formats if both exist
- We have interviewed at least 8 participants: a mix of special educators/behavior therapists (front-line data collectors) and clinical supervisors (data consumers), with at least one participant per role from at least 2 distinct centers
- We can describe the in-session data collection workflow step by step — including what is captured, when, in what format, and what is routinely skipped or deferred
- We can describe, with specificity, where Cognitivebotics starts and stops in the session workflow, and what is currently outside its scope
- We can answer: "Is the current data collection process painful enough that therapists would change their behavior to use a new tool?" — with direct evidence from observation and participant quotes, not inference
- We have collected and reviewed at least 5 artifacts (paper forms, WhatsApp screenshots, spreadsheet templates) representing current documentation practice
- We have identified the top 2–3 downstream uses of session data by clinical supervisors and can describe what format they need it in

---

## Participant Recruitment Criteria

**Who:**
- Special educators holding an RCI license (B.Ed. Special Education or equivalent) actively delivering therapy sessions in an autism therapy center
- Behavior therapists delivering ABA-based or behavioral intervention sessions in an autism therapy center
- Clinical supervisors or senior therapists responsible for designing therapy programs and reviewing session data from junior staff

**Where:** Metro Indian cities — Bangalore, Mumbai, Delhi/NCR, Hyderabad, or Chennai, where center density and digital tool exposure are highest and most relevant to an early launch

**Center profile:** Small independent autism therapy centers (5–20 staff), founder-led or small-organization-run; NOT large hospital-based units (different workflow, different constraints)

**Cognitivebotics filter:** Recruit a mix — centers that currently use Cognitivebotics and centers that do not — to understand both the tool's presence in workflow and its absence

**How many:**
- 4–5 special educators or behavior therapists (front-line)
- 3–4 clinical supervisors or senior therapists (data consumers)
- Total: 7–9 participants across at least 3 distinct centers
- If possible, recruit at least one participant pair (therapist + supervisor) from the same center to understand the data handoff between roles

**Exclusion criteria:**
- Participants working in hospital-based or government rehabilitation centers (workflow and constraints differ significantly from private therapy centers)
- Participants who are BCBAs only and not also functioning as active session therapists (too rare in India to be representative; different credential base)
- Centers with more than 30 staff (outside the target segment)

**Recruitment method:** Outreach through RCI-affiliated training institutions, autism advocacy networks (Action for Autism, Autism Society of India), direct founder/center-director referrals, and LinkedIn outreach to special educators in metro cities

---

## Research Protocol

### Contextual Inquiry — Observed Session

**Format:** In-person, at the center during a live therapy session
**Duration:** 45–60 minutes per observed session (including brief pre/post debrief)
**Consent:** Written informed consent from the therapist and center director; verbal consent acknowledgment from parents per center protocol; no child is directly a research subject

**What to observe:**
- Moments when the therapist picks up or references a recording tool (paper, phone, clipboard)
- How many hands are free during recording; what the child is doing during that moment
- Whether data entry is deferred to after the session, and how much is reconstructed from memory
- Physical location of the recording tool relative to the session activity
- Any visible signs of friction: pausing, fumbling, skipping, abbreviating
- Device model and handling if a phone is in use
- Presence or use of Cognitivebotics during the session

**Debrief questions (5–10 minutes post-session):**
1. Was that a typical session for you in terms of data recording?
2. Was there anything you meant to record but didn't get to?
3. What does your data from this session get used for?

---

### Semi-Structured Interview — Therapist / Special Educator

**Format:** In-person preferred; remote acceptable if in-person is not feasible
**Duration:** 45 minutes
**Recording:** Audio with participant consent

**Guide outline:**

1. Warm-up (5 min)
   - Tell me about your role — how long have you been doing this work, and what does a typical week look like for you?

2. Session workflow context (10 min)
   - Walk me through what a typical therapy session looks like from when the child walks in to when they leave.
   - Where does data recording fit into that — before, during, or after?

3. Current data collection practice (15 min)
   - Show me what you currently use to record data during a session (prompt artifact collection here).
   - What information do you always capture? What do you sometimes skip?
   - What happens to that data after the session — who looks at it, and when?
   - Describe a time when the data recording got in the way of the session, or felt like a burden.
   - Describe a time when you wished you had captured something but didn't.

4. Cognitivebotics and existing tools (10 min)
   - Do you use Cognitivebotics? If so, when in a session does it come into play?
   - What does it capture or track? What does it not cover?
   - Are there other tools — digital or paper — that are part of your session routine?

5. Constraints and environment (5 min)
   - What makes it hard to use a phone or tablet during a session?
   - Have you ever tried to use an app or digital tool during a session? What happened?

---

### Semi-Structured Interview — Clinical Supervisor / Senior Therapist

**Format:** In-person preferred; remote acceptable
**Duration:** 45 minutes
**Recording:** Audio with participant consent

**Guide outline:**

1. Warm-up (5 min)
   - Describe your role — how many staff do you supervise, and what does a typical week look like?

2. Data review workflow (15 min)
   - How do you currently receive session data from your therapists?
   - What do you do with it — how do you review it, and what decisions does it inform?
   - How much time per week do you spend on data review or progress reporting?
   - What format is the data in when it reaches you, and what format do you actually need it in?

3. Pain and breakdown points (15 min)
   - Where does the current process most often fail or slow you down?
   - Describe the last time you had to write a progress report — what did that involve?
   - Are there therapy decisions you're making without the data you'd want to have? What data is missing?

4. Cognitivebotics and existing tools (10 min)
   - How does Cognitivebotics factor into your review process, if at all?
   - What does it provide, and what gap does it leave?

---

## Timeline

| Milestone | Target date |
|-----------|------------|
| Research brief approved | Week 1 |
| Participant recruitment outreach begins | Week 1 |
| Contextual inquiry sessions scheduled | Week 2 |
| Contextual inquiry complete (3 sessions, 2+ centers) | Week 3 |
| Therapist and supervisor interviews complete | Week 4 |
| Artifact collection and review complete | Week 4 |
| Synthesis and thematic analysis | Week 5 |
| Findings shared with product team | End of Week 5 |

Total estimated effort: 5 weeks from brief approval to synthesis complete

---

## Risks & Unknowns

- **Recruitment risk:** RCI-licensed special educators in metro centers are time-constrained during the workday; scheduling contextual inquiry during live sessions requires center director buy-in and may be declined for clinical or logistical reasons. Mitigation: approach center directors first; frame as low-burden observation, not evaluation of staff
- **Cognitivebotics access risk:** We do not yet have a relationship with Cognitivebotics or documented knowledge of its current feature scope. If participants describe its capabilities inconsistently, we will need a secondary review of its documentation or a direct conversation with its team to triangulate. Do not rely solely on participant descriptions of what the tool does
- **Demand bias risk:** Therapists who agree to participate may be more tech-comfortable or more frustrated with current tools than the average user. Self-selection will skew toward people already motivated to change. Counteract by probing for concrete past behavior, not future intent
- **Observation effect risk:** Being observed during a session may cause therapists to record more carefully or differently than usual. Post-session debrief should explicitly ask whether the session was typical
- **Language risk:** If participants are more comfortable in Kannada, Hindi, Tamil, or another regional language, English-only interviews will produce thinner data. Where possible, match researcher language to participant preference, or use a local research partner fluent in the relevant language

---

## Open Questions

- [ ] Does Cognitivebotics have publicly available documentation or a product overview we can review before fieldwork to avoid relying entirely on participant recall of its features?
- [ ] Are there existing center directors or founders in the product team's network who can make warm introductions to clinical staff for recruitment?
- [ ] What consent and data handling protocol applies to audio-recording clinical staff who work with minor children, under DPDPA 2023 — does any consent flow to the center or to RCI?
- [ ] Should we observe DTT sessions, NET sessions, or both? Are there meaningful workflow differences in data collection between these session types that would require deliberate sampling?
- [ ] Is there a target city where fieldwork should begin based on existing product team relationships or proximity?
