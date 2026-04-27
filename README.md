# PM OS — Setup & Usage Guide

A Claude Code-powered Product Management operating system for running
structured product work from discovery through to build.

---

## Setup Instructions

### Step 1 — Copy global identity file
```bash
cp global/CLAUDE.md ~/.claude/CLAUDE.md
```
This loads your PM identity into every Claude Code session across all projects.

### Step 2 — Open this workspace in Claude Code
```bash
cd ~/pm-os
claude
```
Claude will automatically load `CLAUDE.md`, the `.claude/rules/` files,
and all agent definitions at session start.

### Step 3 — Verify agents are available
In Claude Code, type:
```
/project:research
```
If the researcher agent activates and asks clarifying questions, you're set up correctly.

---

## Folder Structure

```
pm-os/
├── CLAUDE.md                          # Workspace root — loaded every session
├── README.md                          # This file
│
├── .claude/
│   ├── agents/                        # Specialist consultant personas
│   │   ├── researcher.md              # Research analyst
│   │   ├── product-consultant.md      # Scope & strategy
│   │   ├── design-consultant.md       # Design critic
│   │   └── prd-reviewer.md            # PRD quality gate
│   │
│   ├── commands/                      # Slash commands
│   │   ├── research.md                # /project:research
│   │   ├── prd-create.md              # /project:prd-create
│   │   ├── prd-review.md              # /project:prd-review
│   │   ├── scope.md                   # /project:scope
│   │   ├── design-critique.md         # /project:design-critique
│   │   └── validate.md                # /project:validate
│   │
│   └── rules/                         # Always-on guardrails
│       ├── pm-principles.md           # Stage gates, hard rules
│       └── output-formats.md          # Document standards
│
├── docs/
│   └── templates/                     # Reusable document templates
│       ├── prd-template.md
│       ├── research-plan-template.md
│       ├── scope-brief-template.md
│       ├── design-critique-template.md
│       └── validation-plan-template.md
│
├── global/
│   └── CLAUDE.md                      # Copy to ~/.claude/CLAUDE.md
│
└── products/
    └── autism-therapy-platform/
        ├── CLAUDE.md                  # Product context — loaded every session
        ├── stage-tracker.md           # Where we are in the process
        ├── research/                  # All research artifacts
        │   ├── autism-center-discovery-research-plan.md
        │   ├── competitive-landscape-draft.md
        │   ├── questions/             # Research question docs
        │   └── findings/              # Synthesized findings
        │       └── raw/               # Raw interview notes
        ├── prds/                      # Product Requirements Documents
        ├── briefs/                    # Scope briefs
        └── designs/                   # Design critique notes
```

---

## How to Use — By Stage

### 🔍 Discovery
```
/project:research autism therapy center operations
```
→ Produces a research plan with questions, methods, and recruitment criteria.

For competitive analysis:
```
/project:research competitive landscape for ABA therapy software
```

### 📋 Define
First, scope the work:
```
/project:scope [feature name]
```

Then write the PRD:
```
/project:prd-create [feature name]
```

Then review it:
```
/project:prd-review [path to PRD or paste content]
```

### 🎨 Design
After design artifacts exist:
```
/project:design-critique [screen or flow name]
```

### ✅ Validate
```
/project:validate [assumption or feature to test]
```

---

## Adding a New Product
1. Create `products/[product-slug]/CLAUDE.md` with product context
2. Add a reference to it in the root `CLAUDE.md` under "Active Products"
3. Create subdirectories: `research/`, `prds/`, `briefs/`, `designs/`
4. Copy and fill in `stage-tracker.md`

---

## Tips

**Use `#` to save to memory during a session**
Start any message with `#` and Claude Code will ask which CLAUDE.md to save it to.
Great for capturing learnings mid-session.

**Keep CLAUDE.md files under 200 lines**
Use `@imports` to reference templates and detailed content.
Longer files reduce how reliably Claude follows instructions.

**Update stage-tracker.md after every milestone**
It's your source of truth on where each workstream stands.

**Assumptions are first-class citizens**
Tag everything unvalidated as `[ASSUMPTION]`. Discovery exists to burn these down.
