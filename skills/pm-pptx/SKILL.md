---
name: pm-pptx
description: >
  Creates branded PowerPoint presentations for the PM OS / Autism Therapy Platform.
  Applies the Cognitivebotics brand identity automatically — correct colors, fonts,
  and layout structure — so every deck looks consistent without manual formatting.

  Use this skill whenever the user wants to turn PM OS documents into a slide deck:
  "make a deck", "create slides", "turn this into a presentation", "build a PowerPoint",
  "I need slides for the board", "create a leadership deck", "make a pitch deck",
  "discovery readout slides", "research summary slides".
---

# PM-OS PowerPoint Skill

Produce branded `.pptx` decks using the pre-built Cognitivebotics library (python-pptx).
**Never re-implement brand colors or slide helpers from scratch** — import the library.

## Brand library

```
/Users/prahladrebala/Documents/pm-os/tools/cb_pptx.py   ← PowerPoint helper library
/Users/prahladrebala/Documents/pm-os/tools/cb_brand.py  ← shared brand constants
```

---

## One-liner (markdown → pptx)

```python
import sys; sys.path.insert(0, '/Users/prahladrebala/Documents/pm-os/tools')
from cb_pptx import CB_Pptx

CB_Pptx.build_from_markdown(
    md_path   = '/path/to/source.md',
    out_path  = '/path/to/output.pptx',
    title     = 'Discovery Readout: Center Lifecycle',  # optional
    deck_type = 'Discovery Stage',
)
```

Markdown mapping: `#` → cover, `##` → section divider, `###` → content slide,
bullets → added to current slide, `>` → quote slide, `|table|` → table slide.

---

## CLI (run directly)

```bash
cd /Users/prahladrebala/Documents/pm-os/tools
python3 cb_pptx.py source.md output.pptx --title "Discovery Readout" --type "April 2026"
```

---

## Programmatic API (build slide by slide)

Use when building a curated deck from conversation content.

```python
import sys; sys.path.insert(0, '/Users/prahladrebala/Documents/pm-os/tools')
from cb_pptx import CB_Pptx

prs = CB_Pptx()

prs.cover(
    "Discovery Readout: Center Lifecycle",
    subtitle = "Autism Therapy Platform — April 2026",
    label    = "Discovery Stage",
)

prs.section_divider("What We Set Out to Learn")

prs.content("Research Goals", bullets=[
    "Understand the actual operational workflow of a therapy center",
    "Validate whether in-session paper data collection is a felt pain",
    "Map the billing and dropout workflows from the director's perspective",
])

prs.section_divider("Key Findings")

prs.content("Finding 1: Data collection is paper-first — always", bullets=[
    "All centers observed use paper data sheets during live sessions",
    "No digital tool meets the one-handed, in-session constraint",
    "Supervisors see session data 1–2 weeks after it is recorded",
    "  → Program updates are delayed; children run outdated targets",
])

prs.two_column(
    "Implication: The product must be ≤ 2 taps in-session",
    left_label  = "What we observed",
    right_label = "What it means for the product",
    left  = ["Paper causes transcription errors", "ABC data is retrospective",
             "Supervisor feedback is batched weekly"],
    right = ["Digital tool must need ≤ 2 taps per trial",
             "Behavioral logging must be in-the-moment",
             "Real-time data visibility is the core supervisor value prop"],
)

prs.quote_slide(
    quote       = "I finish the session and then I try to remember what happened "
                  "for the ABC. Sometimes I'm writing it from what I think happened.",
    attribution = "Special Educator, Bengaluru center",
    context     = "On retrospective ABC data recording",
)

prs.table_slide(
    "Open Hypotheses — Priority 1",
    headers = ["#", "Hypothesis", "Validation Method", "Status"],
    rows    = [
        ["H-01", "Paper data sheets used in live sessions",
         "Contextual observation", "Open"],
        ["H-03", "Offline-first is a hard requirement",
         "Session room connectivity test", "Open"],
        ["H-07", "Supervisor documentation >1hr/week outside clinical hours",
         "Time-diary interview", "Open"],
    ],
)

prs.content("Recommended Next Steps", bullets=[
    "Run 5–8 center director interviews (script ready)",
    "Run 8–10 therapist interviews (script ready)",
    "Schedule contextual observation in 3 centers",
    "  → Target: findings synthesis by end of May 2026",
])

prs.closing("Questions?", bullets=[
    "Scripts: /research/primary/",
    "Journey map: /research/journey-map.md",
    "Hypothesis register: Part 4 of journey map",
])

prs.save("/path/to/output.pptx")
```

---

## Available slide types

| Method | Slide layout |
|---|---|
| `prs.cover(title, subtitle, label)` | Full teal cover with product name |
| `prs.section_divider(title, description)` | Dark divider between major sections |
| `prs.content(title, bullets, body_text, note)` | Standard bullet slide |
| `prs.two_column(title, left, right, left_label, right_label)` | Finding / implication split |
| `prs.table_slide(title, headers, rows, col_widths)` | Branded data table |
| `prs.quote_slide(quote, attribution, context)` | Full-bleed user quote |
| `prs.closing(title, bullets)` | Dark closing / CTA slide |

---

## Deck templates by use case

### Discovery Readout
```
cover → section_divider("What We Set Out to Learn") → content (goals)
→ section_divider("Key Findings") → content × N → two_column × N → quote_slide × N
→ section_divider("What This Means") → content (implications)
→ table_slide (open hypotheses / risks)
→ content (next steps) → closing
```

### Executive / Board Update
```
cover → content (where we are) → content (what we know, 3–5 findings)
→ table_slide (key decisions needed) → table_slide (risks)
→ content (next steps) → closing
```

### Research Brief Presentation
```
cover → content (why this research) → table_slide (research questions)
→ content (assumptions being tested) → content (method + participants)
→ content (timeline) → content (what good looks like) → closing
```

---

## Instructions

1. Ask the user what type of deck they need if not clear from context.
2. Read all source documents they point to before building any slides.
3. Use the programmatic API to curate slides with the right content density — do not dump raw markdown onto slides.
4. A content slide should have 3–6 bullets max. Split into multiple slides if needed.
5. Use `quote_slide` for any direct participant quotes from research.
6. Use `two_column` for finding → implication pairs.
7. Write a short Python script using the library. Do **not** rewrite colors or shape helpers.
8. Run the script with Bash and confirm the output path and slide count.
