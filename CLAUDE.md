# PM OS — Workspace Root

## What This Workspace Is
Product Management operating system for running a full product process from Discovery through Build.

## Active Products
- **Autism Therapy Platform** — Enterprise tools for autism therapy centers in India
  @products/autism-therapy-platform/CLAUDE.md
- **Cognitivebotics** — AI-powered digital learning platform extending therapy into the home for neurodiverse children (ages 2–18)
  @products/cognitivebotics/CLAUDE.md

## Process Stages
Every product moves through these stages in order. Confirm which stage we are in before starting.

1. **Discovery** — Understand users, problems, and market context
2. **Define** — Scope the problem, align on success metrics, write the PRD
3. **Design** — Wireframes, flows, information architecture
4. **Validate** — Test assumptions with users before building
5. **Build** — Spec refinement, engineering handoff, QA

---

## Agent Routing — Auto-Invoke

Route automatically based on the task. No need to invoke manually unless overriding.

| When the request involves... | Invoke |
|---|---|
| Research questions, interview planning, competitive analysis, synthesis | `researcher` |
| Feature scoping, MVP definition, strategy challenge, scope briefs | `product-consultant` |
| Wireframe critique, UX review, IA design, flow feedback | `design-consultant` |
| PRD review, requirements check, engineering readiness | `prd-reviewer` |
| Competitor features → tickets, user journey synthesis from documents | `mindless-product-owner` |
| User stories, sprint backlog, acceptance criteria | `product-owner` |
| Story review, sprint readiness, backlog QA | `story-reviewer` |
| Button labels, modal copy, empty states, error messages, tooltips, onboarding, notifications | `copywriter` |

**Slash commands for explicit control:**
`/research` · `/scope` · `/prd-create` · `/prd-review` · `/design-critique` · `/validate` · `/engineering-handoff` · `/competitor-scan`

---

## Memory — Load at Session Start

Current project state: @.claude/memory/atp_status.md
Open assumptions: @.claude/memory/open_assumptions.md
User preferences: @.claude/memory/user_context.md
Corrections log: @.claude/memory/corrections.md

---

## Templates
- PRD: @docs/templates/prd-template.md
- Research Plan: @docs/templates/research-plan-template.md
- Scope Brief: @docs/templates/scope-brief-template.md
- Design Critique: @docs/templates/design-critique-template.md
- Validation Plan: @docs/templates/validation-plan-template.md

---

## Hard Rules
- ALWAYS confirm which product and which stage before starting work
- NEVER propose solutions in the Discovery stage — only questions and frameworks
- Flag stage-skipping explicitly: *"This looks like we're jumping to [stage] without completing [prior stage]. Intentional?"*
- Tag every unvalidated belief `[ASSUMPTION]`
- Surface open assumptions at the end of every session for both products
