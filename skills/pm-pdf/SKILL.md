---
name: pm-pdf
description: >
  Exports PM OS documents to branded PDF — applying the Cognitivebotics visual identity
  with consistent headers, footers, typography, and color. Works from markdown files,
  Word docs, or raw content provided in the conversation.

  Use this skill whenever the user wants a PDF output: "export to PDF", "create a PDF",
  "I need a PDF version", "make this a shareable PDF", "generate a PDF report",
  "send this as a PDF", "format as PDF for the client", "PDF for the center director".
---

# PM-OS PDF Export Skill

Produce branded PDFs using the pre-built Cognitivebotics library (reportlab).
**Never re-implement brand colors or layout helpers from scratch** — import the library.

## Brand library

```
/Users/prahladrebala/Documents/pm-os/tools/cb_pdf.py    ← PDF helper library
/Users/prahladrebala/Documents/pm-os/tools/cb_brand.py  ← shared brand constants
```

---

## One-liner (markdown → PDF)

```python
import sys; sys.path.insert(0, '/Users/prahladrebala/Documents/pm-os/tools')
from cb_pdf import CB_PDF

CB_PDF.build_from_markdown(
    md_path  = '/path/to/source.md',
    out_path = '/path/to/output.pdf',
    title    = 'Short title shown in header/footer',  # optional; auto-extracted from H1
    doc_type = 'Research Brief',   # label on cover page subtitle
    date     = 'April 2026',
    with_cover = True,             # False to skip cover page
)
```

---

## CLI (run directly)

```bash
cd /Users/prahladrebala/Documents/pm-os/tools
python3 cb_pdf.py source.md output.pdf --title "Research Brief" --type "Discovery" --date "April 2026"
python3 cb_pdf.py source.md output.pdf --no-cover   # skip cover page
```

---

## Programmatic API (build manually)

Use when content comes from conversation rather than a file.

```python
import sys; sys.path.insert(0, '/Users/prahladrebala/Documents/pm-os/tools')
from cb_pdf import CB_PDF

pdf = CB_PDF(title="Scope Brief: Billing", doc_type="Scope Brief", date="April 2026")

# Optional branded cover page
pdf.cover_page(
    title    = "Scope Brief: Billing & Fee Collection",
    subtitle = "Autism Therapy Platform — Define Stage",
    meta     = [("Product", "Autism Therapy Platform"), ("Date", "April 2026"),
                ("Author", "[Name]"), ("Stage", "Define")],
)

pdf.h2("Problem We're Solving")
pdf.body("Center directors manage billing through WhatsApp messages and paper registers...")

pdf.h2("In Scope")
pdf.bullet("Monthly fee statement auto-generated from session attendance")
pdf.bullet("UPI payment link sent to parent via WhatsApp")
pdf.bullet("Outstanding balance dashboard for center director")

pdf.h2("Out of Scope (this phase)")
pdf.bullet("Insurance claim submission — no insurance mandate in India")
pdf.bullet("Multi-currency — INR only at launch")

pdf.h2("Top Risks")
pdf.table(
    headers=["Risk", "Likelihood", "Impact", "Mitigation"],
    rows=[
        ["Directors avoid fee conversations regardless of tooling",
         "Medium", "High", "Validate via director interview (H-09)"],
    ],
)

pdf.callout(
    ["Center directors would pay for billing automation at Indian price points."],
    title="[ASSUMPTION]"
)

pdf.save("/path/to/output.pdf")
```

---

## Available methods

| Method | What it does |
|---|---|
| `pdf.cover_page(title, subtitle, meta)` | Full cover page with teal band + dark strip |
| `pdf.h1(text)` | H1 with underline rule — teal 22pt |
| `pdf.h2(text)` | H2 — dark teal 16pt |
| `pdf.h3(text)` | H3 — cyan 13pt |
| `pdf.body(text)` | Body paragraph — `**bold**` and `*italic*` inline supported |
| `pdf.italic(text)` | Indented italic — goals, probes, notes |
| `pdf.kv(key, value)` | **Bold teal key:** value — metadata |
| `pdf.bullet(text, level=0)` | Bullet (● cyan or – teal) |
| `pdf.checkbox(text)` | ☐ checkbox line |
| `pdf.question(num, text)` | Numbered interview question |
| `pdf.blockquote(text)` | Mint callout box with cyan left border |
| `pdf.callout(lines, title)` | Callout box — [ASSUMPTION], warnings, notes |
| `pdf.table(headers, rows)` | Teal header, alternating mint/white rows |
| `pdf.cover_table(pairs)` | Two-column metadata block (no cover page) |
| `pdf.rule()` | Thin horizontal divider |
| `pdf.spacer(height)` | Vertical space (in inches) |
| `pdf.save(path)` | Render and save — prints page count |
| `CB_PDF.build_from_markdown(md, out)` | Markdown file → branded PDF (one call) |

---

## PDF types and when to use `with_cover`

| Document type | `with_cover` | `doc_type` label |
|---|---|---|
| Research Brief / Synthesis | `True` | `"Research Brief"` |
| PRD | `True` | `"Product Requirements"` |
| Interview Script | `False` | — |
| Scope Brief | `True` | `"Scope Brief"` |
| Progress Report (parent-facing) | `True` | `"Progress Report"` |
| Executive Summary | `False` | — |

---

## Instructions

1. Read the source file(s) the user points to.
2. If a markdown file exists → use `CB_PDF.build_from_markdown()` (3 lines total).
3. If content comes from conversation → use the programmatic API.
4. Choose `with_cover=True` for formal documents shared externally; `False` for internal working docs.
5. Write a short Python script using the library. Do **not** rewrite colors or layout helpers.
6. Run the script with Bash and confirm the output path and page count.
