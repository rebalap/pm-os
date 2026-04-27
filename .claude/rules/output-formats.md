# Output Formats — Document Standards

Standards for every document produced in this PM OS.
Apply these consistently regardless of which agent is active.

---

## Universal Document Rules

- Use headers and sections for all structured documents
- Always include a **Risks & Unknowns** section in every major document
- Tag unvalidated content as `[ASSUMPTION]`
- Use tables for comparisons, tradeoffs, and risk matrices
- Use checklists (`- [ ]`) for action items and review criteria
- Prefer bullet points over prose for lists of requirements, risks, or findings

---

## Document Types & Required Sections

### Research Brief
```
## Research Brief: [Topic]
**Decision to inform:**
**Stage:** Discovery / Evaluative
**Recommended methods:**

### Research Questions
### Key Assumptions Being Tested
### What Good Looks Like
### Suggested Recruitment Criteria
### Timeline Estimate
```

### Research Synthesis
```
## Research Findings: [Topic]
**Date:**
**Participants:**
**Methods used:**

### Key Themes
### Findings (what we observed)
### Implications (what it means)
### Open Questions
### Recommended Next Steps
```

### Scope Brief
```
## Scope Brief: [Feature/Initiative]
**Target user:**
**Job to be done:**
**Success metric (90 days):**

### In Scope
### Out of Scope (this phase)
### MVP Recommendation
### Top Risks
### Open Questions Before Building
### What Would Need to Be True to Succeed
```

### PRD (Product Requirements Document)
```
## PRD: [Feature Name]
**Product:**
**Author:**
**Date:**
**Status:** Draft / In Review / Approved
**Target users:**
**Success metric:**

### Problem Statement
### Background & Context
### User Stories
### Requirements (In Scope)
### Out of Scope
### Design & UX
### Edge Cases & Error States
### Launch Criteria
### Risks & Unknowns
### Open Questions
```

### Design Critique
```
## Design Critique: [Screen/Flow Name]
**Reviewer:** Design Consultant
**Date:**
**Overall assessment:**

### What Works Well
### Issues Found (P0 → P3)
### Accessibility Check
### Questions for the Designer
### Recommended Next Step
```

### Validation Plan
```
## Validation Plan: [Assumption Being Tested]
**Product:**
**Date:**
**Hypothesis:** [Falsifiable statement]
**Method:**
**Success criteria:** [What we'll see if validated]
**Failure criteria:** [What we'll see if invalidated]

### Participant Recruitment
### Test Protocol
### What We'll Do If Invalidated
### Timeline
```

---

## Tone & Voice

- Be direct — avoid hedging language ("it might be worth considering...")
- Use active voice ("Engineering will need X" not "X will be needed")
- Attribute claims — "3 of 5 users said..." not "users prefer..."
- Flag opinions clearly — "My recommendation:" vs. "Research shows:"

---

## Length Guidelines

| Document | Target length |
|----------|--------------|
| Research Brief | 1–2 pages |
| Research Synthesis | 2–4 pages |
| Scope Brief | 1 page |
| PRD | 3–6 pages |
| Design Critique | 1–2 pages |
| Validation Plan | 1–2 pages |

Longer is not better. If a PRD exceeds 6 pages, challenge whether scope is too broad.
