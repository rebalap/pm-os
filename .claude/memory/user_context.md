# User Context

**Name:** Prahlad Rebala
**Email:** prahlad.rebala@gmail.com
**Role:** Product Manager / Founder

---

## Working Style

- Evidence-first PM: every claim must be grounded in user research or tagged [ASSUMPTION]
- Stage-gate discipline: always confirm which product and which stage before starting work
- Assumption hygiene: surface open assumptions at end of every session
- Scope discipline: flag "let's add X while we're here" as scope creep every time
- Structured output preferred: tables, checklists, headers — not dense prose

## Output Preferences

- Documents: branded .docx via `python3 tools/cb_docx.py`, PDF via `cb_pdf.py`, slides via `cb_pptx.py`
- Research: always use Tavily (`python3 tools/tavily-search.py`) — not WebSearch
- Voice: direct, active, evidence-attributed. No hedging language ("might be worth considering")
- Length discipline: PRDs max 6 pages; scope briefs 1 page; research briefs 1-2 pages

## Correction Protocol

When Prahlad corrects a direction or mistakes are made, add an entry to `.claude/memory/corrections.md`.
Ask to confirm before logging. Corrections become CLAUDE.md rules over time.
