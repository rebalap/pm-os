---
name: pm-docx
description: |
  Creates branded Word documents (.docx) for the PM OS / Autism Therapy Platform. Applies the Cognitivebotics visual identity automatically — correct heading colors, fonts, table styles, and layout — so every document looks consistent and professional.
  Use this skill whenever the user wants to turn PM OS content into a formatted Word doc: "create a Word doc", "write this up as a document", "make a report", "format this as a brief", "export to docx", "I need a formatted PRD", "write the research brief as a document", "turn this into a proper report", "create a therapy program document".
---
# PM-OS Word Document Skill

Produce branded `.docx` files using the pre-built Cognitivebotics library.
**Never re-implement brand colors or helper functions from scratch** — import the library.

## Brand library

```
/Users/prahladrebala/Documents/pm-os/tools/cb_docx.py   ← Word helper library
/Users/prahladrebala/Documents/pm-os/tools/cb_brand.py  ← shared brand constants
```

---

## One-liner (markdown → docx)

```python
import sys; sys.path.insert(0, '/Users/prahladrebala/Documents/pm-os/tools')
from cb_docx import CB_Doc

CB_Doc.build_from_markdown(
    md_path  = '/path/to/source.md',
    out_path = '/path/to/output.docx',
    title    = 'Short title shown in footer',   # optional; auto-extracted from H1
    date     = 'April 2026',
)
```

That is the complete script for converting any PM OS markdown file.

---

## CLI (run directly)

```bash
cd /Users/prahladrebala/Documents/pm-os/tools
python3 cb_docx.py source.md output.docx --title "Research Brief" --date "April 2026"
```

---

## Programmatic API (build manually)

Use when content comes from conversation rather than a file.

```python
import sys; sys.path.insert(0, '/Users/prahladrebala/Documents/pm-os/tools')
from cb_docx import CB_Doc

d = CB_Doc(short_title="PRD: Session Data Collection", date="April 2026")

d.h1("PRD: In-Session Data Collection")
d.cover_table([
    ("Product",        "Autism Therapy Platform"),
    ("Author",         "[Name]"),
    ("Date",           "April 2026"),
    ("Status",         "Draft"),
    ("Target users",   "Special Educators (Priya)"),
    ("Success metric", "80% of therapists log data in-session within 30 days"),
])
d.h2("Problem Statement")
d.body("Special educators currently record trial data on paper during live sessions...")
d.h2("User Stories")
d.table(
    headers=["As a...", "I want to...", "So that..."],
    rows=[["Special Educator", "tap to log trial outcomes",
           "I don't break eye contact with the child"]],
)
d.h2("Launch Criteria")
d.checkbox("All REQ-0X requirements pass QA")
d.checkbox("Tested on Redmi / Realme mid-range Android")
d.callout([
    "Depends on H-01 being validated by primary research.",
    "Do not begin engineering until field research is complete.",
], title="[ASSUMPTION]")
d.save("/path/to/output.docx")
```

---

## Available methods

| Method | What it does |
| --- | --- |
| `d.h1(text)` | H1 — teal 22pt Nunito Bold with underline rule |
| `d.h2(text)` | H2 — dark teal 16pt |
| `d.h3(text)` | H3 — cyan 13pt |
| `d.body(text)` | Body paragraph — `**bold**` and `*italic*` inline supported |
| `d.italic(text)` | Indented italic line — goals, probes, researcher notes |
| `d.kv(key, value)` | **Bold teal key:** value — metadata lines |
| `d.bullet(text, level=0)` | Bullet (level 0 = cyan ●, level 1 = teal –) |
| `d.checkbox(text)` | ☐ checkbox line |
| `d.question(num, text)` | Numbered interview question with teal number |
| `d.blockquote(text)` | Mint box with cyan left border — opening statements |
| `d.callout(lines, title)` | Callout box — [ASSUMPTION], notes, warnings |
| `d.table(headers, rows)` | Teal header, alternating mint/white rows |
| `d.cover_table(pairs)` | Two-column metadata cover block |
| `d.spacer()` | Vertical space |
| `d.save(path)` | Write the file |
| `CB_Doc.build_from_markdown(md, out)` | Markdown file → .docx (one call) |

All methods return `self` — chain freely: `d.h2("...").body("...").bullet("...")`

---

## Instructions

1. Read the source file(s) the user points to.
2. If a markdown file exists → use `CB_Doc.build_from_markdown()` (3 lines total).
3. If content comes from conversation → use the programmatic API.
4. Write a short Python script using the library. Do **not** rewrite brand helpers or colors.
5. Run the script with Bash and confirm the output path.
