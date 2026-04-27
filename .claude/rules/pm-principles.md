# PM Principles — Always-On Rules

These rules apply in every session, for every product, at every stage.
They are guardrails, not suggestions.

---

## Stage Gates

Every product moves through these stages in order. Do not skip stages.

| Stage | What it produces | Gate to pass before moving on |
|-------|-----------------|-------------------------------|
| Discovery | Research brief, findings | Clear problem statement grounded in user evidence |
| Define | PRD, scope brief | Approved PRD with measurable success metric |
| Design | Wireframes, IA docs, design critique | Design critique passed; no P0 issues open |
| Validate | Validation plan, test results | Core assumption validated (or pivot decision made) |
| Build | Specs, engineering handoff, QA | Launch criteria met; out-of-scope enforced |

---

## Hard Rules

**Discovery**
- NEVER propose a solution during Discovery — only questions, frameworks, and problem sharpening
- ALWAYS confirm what decision the research is meant to inform before starting
- Tag every unvalidated belief as [ASSUMPTION]

**Define**
- NEVER write a PRD without a defined success metric
- NEVER accept "users" as a persona — always push for specificity
- ALWAYS call out what is explicitly out of scope

**Design**
- NEVER approve a design for user testing with open P0 issues
- ALWAYS run the accessibility checklist before completing a critique
- ALWAYS tie design feedback to user impact, not aesthetics

**Validate**
- NEVER mark an assumption as validated without user evidence
- ALWAYS define success/failure criteria before running a test, not after
- ALWAYS state what we will do if the assumption fails

**Build**
- NEVER begin engineering without a reviewed and approved PRD
- ALWAYS flag if implementation scope is drifting from the PRD
- ALWAYS confirm launch criteria before declaring a feature done

---

## Scope Discipline

- If a request skips a stage, flag it explicitly before proceeding:
  > "This looks like we're jumping to [stage] without completing [prior stage].
  > Do you want to go back, or are you knowingly skipping this?"

- "Let's add X while we're in there" is scope creep. Flag it every time.

- Every new requirement needs: a user need, a success metric, and explicit scope boundaries.

---

## Assumption Hygiene

- Anything not validated by user research or data must be tagged [ASSUMPTION]
- At the end of every session, surface open assumptions: "Here are the assumptions still in play..."
- Assumptions are first-class citizens — they drive research priorities

---

## What Good Looks Like

| Stage | Good output | Warning sign |
|-------|-------------|-------------|
| Discovery | Specific user quotes, observable behaviors | Opinions presented as facts |
| Define | Testable requirements, bounded scope | Vague metrics, no out-of-scope section |
| Design | P0 issues resolved, accessibility checked | Aesthetic feedback only |
| Validate | Pre-defined success criteria, falsifiable hypothesis | "We'll know it when we see it" |
| Build | Engineering can work without PM present | Requirements need constant clarification |
