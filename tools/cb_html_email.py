#!/usr/bin/env python3
"""
cb_html_email.py — Convert a Cognitivebotics weekly announcement .md file
into a branded HTML email ready to paste into Gmail or Outlook.

CLI:
    python3 tools/cb_html_email.py path/to/2026-05-14-weekly-announcement.md
    python3 tools/cb_html_email.py path/to/file.md --out path/to/output.html
"""

from __future__ import annotations
import sys, os, re, argparse
from pathlib import Path

_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _dir)
import cb_brand as B


# ── Color helpers ─────────────────────────────────────────────────────────────

def _hex(h: str) -> str:
    return f"#{h}"

TEAL      = _hex(B.TEAL)
CYAN      = _hex(B.CYAN)
DARK_TEAL = _hex(B.DARK_TEAL)
BLACK     = _hex(B.BLACK)
GRAY      = _hex(B.GRAY)
MINT      = _hex(B.MINT)
WHITE     = _hex(B.WHITE)
BORDER    = _hex(B.BORDER)
RED       = _hex(B.RED)

FONT_H = "'Nunito', Arial, sans-serif"
FONT_B = "'Open Sans', Arial, sans-serif"


# ── Style builder ─────────────────────────────────────────────────────────────

def _s(**kw) -> str:
    return "; ".join(f"{k.replace('_', '-')}: {v}" for k, v in kw.items())


# ── Inline markdown → HTML ────────────────────────────────────────────────────

def _inline(text: str) -> str:
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    return text


# ── Block renderers ───────────────────────────────────────────────────────────

def parse_table(lines: list[str]) -> list[list[str]]:
    rows = []
    for line in lines:
        if re.match(r'^\|[-:\s|]+\|$', line.strip()):
            continue  # skip separator row
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        rows.append(cells)
    return rows


def render_table(rows: list[list[str]]) -> str:
    if not rows:
        return ''
    html = f'<table style="{_s(width="100%", border_collapse="collapse", font_family=FONT_B, font_size="13px", margin="8px 0 20px 0")}" cellpadding="0" cellspacing="0">'
    for i, row in enumerate(rows):
        if i == 0:
            html += f'<tr style="{_s(background_color=TEAL)}">'
            for cell in row:
                html += (
                    f'<td style="{_s(padding="10px 14px", color=WHITE, font_family=FONT_H, font_weight="700", font_size="12px", text_transform="uppercase", letter_spacing="0.5px", border="1px solid " + DARK_TEAL)}">'
                    f'{_inline(cell)}</td>'
                )
        else:
            bg = MINT if i % 2 == 0 else WHITE
            html += f'<tr style="{_s(background_color=bg)}">'
            for cell in row:
                html += (
                    f'<td style="{_s(padding="9px 14px", color=BLACK, font_family=FONT_B, font_size="13px", border="1px solid " + BORDER, vertical_align="top")}">'
                    f'{_inline(cell)}</td>'
                )
        html += '</tr>'
    html += '</table>'
    return html


def render_blockquote(lines: list[str]) -> str:
    parts = []
    for line in lines:
        stripped = line.strip().lstrip('> ').strip()
        if stripped:
            parts.append(stripped)
    content = ' '.join(parts)
    style = _s(
        background_color=MINT,
        border_left=f"4px solid {CYAN}",
        padding="10px 14px",
        margin="0 0 16px 0",
        color=GRAY,
        font_family=FONT_B,
        font_size="12px",
        line_height="1.6"
    )
    return f'<div style="{style}">{_inline(content)}</div>'


def render_flag(text: str) -> str:
    text = re.sub(r'^-\s*\[\s*\]\s*', '', text).strip()
    style = _s(
        background_color="#FFF5F5",
        border_left=f"4px solid {RED}",
        padding="10px 14px",
        margin="0 0 10px 0",
        color=BLACK,
        font_family=FONT_B,
        font_size="13px",
        line_height="1.5"
    )
    return f'<div style="{style}">&#9873; {_inline(text)}</div>'


def render_body(text: str) -> str:
    style = _s(
        color=BLACK,
        font_family=FONT_B,
        font_size="13px",
        line_height="1.6",
        margin="0 0 10px 0"
    )
    return f'<p style="{style}">{_inline(text)}</p>'


# ── Main converter ────────────────────────────────────────────────────────────

def md_to_html_email(md_text: str) -> str:
    lines = md_text.splitlines()

    title = "Cognitivebotics — Weekly Product Announcement"
    period = ""
    prepared = ""
    i = 0

    # Parse preamble
    while i < len(lines):
        stripped = lines[i].strip()
        if stripped.startswith('# '):
            title = stripped[2:].strip()
        elif stripped.startswith('**Period:**'):
            period = re.sub(r'\*\*Period:\*\*\s*', '', stripped).strip()
        elif stripped.startswith('**Prepared:**'):
            prepared = re.sub(r'\*\*Prepared:\*\*\s*', '', stripped).strip()
        elif stripped == '---':
            i += 1
            break
        i += 1

    # Parse body blocks
    body_html = ""

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Skip bare dividers
        if stripped == '---':
            i += 1
            continue

        # ## Flags section
        if re.match(r'^## Flags', stripped):
            style = _s(
                background_color="#FEF0EF",
                color=RED,
                font_family=FONT_H,
                font_size="14px",
                font_weight="700",
                padding="12px 16px",
                margin="28px -32px 16px -32px"
            )
            body_html += f'<div style="{style}">&#9873; Flags for Follow-Up</div>'
            i += 1
            continue

        # ## N. Section header
        if re.match(r'^## ', stripped):
            section_title = re.sub(r'^##\s+\d+\.\s*', '', stripped).strip()
            style = _s(
                background_color=DARK_TEAL,
                color=WHITE,
                font_family=FONT_H,
                font_size="14px",
                font_weight="700",
                padding="12px 16px",
                margin="28px -32px 16px -32px",
                letter_spacing="0.3px"
            )
            body_html += f'<div style="{style}">{section_title}</div>'
            i += 1
            continue

        # ### Subsection header
        if re.match(r'^### ', stripped):
            sub_title = re.sub(r'^###\s+', '', stripped).strip()
            style = _s(
                color=DARK_TEAL,
                font_family=FONT_H,
                font_size="13px",
                font_weight="700",
                padding="12px 0 6px 0",
                border_bottom=f"2px solid {CYAN}",
                margin="0 0 12px 0"
            )
            body_html += f'<div style="{style}">{sub_title}</div>'
            i += 1
            continue

        # Table
        if stripped.startswith('|'):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                table_lines.append(lines[i].strip())
                i += 1
            body_html += render_table(parse_table(table_lines))
            continue

        # Blockquote — collect contiguous > lines
        if stripped.startswith('>'):
            bq_lines = []
            while i < len(lines) and lines[i].strip().startswith('>'):
                bq_lines.append(lines[i])
                i += 1
            body_html += render_blockquote(bq_lines)
            continue

        # Flag item
        if re.match(r'^-\s*\[\s*\]', stripped):
            body_html += render_flag(stripped)
            i += 1
            continue

        # Non-empty body text
        if stripped:
            body_html += render_body(stripped)

        i += 1

    # ── Assemble full email ───────────────────────────────────────────────────

    meta_line = ""
    if period:
        meta_line += f"Period: {period}"
    if period and prepared:
        meta_line += "&nbsp;&nbsp;·&nbsp;&nbsp;"
    if prepared:
        meta_line += f"Prepared: {prepared}"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700&family=Open+Sans:wght@400;600&display=swap');
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
</style>
</head>
<body style="background-color: #ECF4F4; padding: 32px 16px; font-family: Arial, sans-serif;">

<table width="100%" cellpadding="0" cellspacing="0" style="max-width: 640px; margin: 0 auto; background-color: {WHITE}; border-radius: 6px; overflow: hidden; border: 1px solid {BORDER}; box-shadow: 0 2px 8px rgba(0,0,0,0.07);">

  <!-- HEADER -->
  <tr>
    <td style="background-color: {TEAL}; padding: 28px 32px;">
      <div style="font-family: {FONT_H}; font-size: 20px; font-weight: 700; color: {WHITE}; letter-spacing: 0.3px; line-height: 1.3;">{title}</div>
      <div style="font-family: {FONT_B}; font-size: 12px; color: rgba(255,255,255,0.78); margin-top: 8px;">{meta_line}</div>
    </td>
  </tr>

  <!-- BODY -->
  <tr>
    <td style="padding: 8px 32px 32px 32px;">
      {body_html}
    </td>
  </tr>

  <!-- FOOTER -->
  <tr>
    <td style="background-color: {MINT}; padding: 14px 32px; border-top: 1px solid {BORDER};">
      <div style="font-family: {FONT_B}; font-size: 11px; color: {GRAY}; line-height: 1.5;">
        Cognitivebotics &nbsp;·&nbsp; Confidential — Internal Use &nbsp;·&nbsp; Generated {prepared}
      </div>
    </td>
  </tr>

</table>
</body>
</html>"""

    return html


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Convert a Cognitivebotics announcement .md to a branded HTML email"
    )
    parser.add_argument("input", help="Path to the markdown announcement file")
    parser.add_argument("--out", help="Output HTML path (default: same folder, .html extension)")
    args = parser.parse_args()

    in_path = Path(args.input).resolve()
    if not in_path.exists():
        print(f"Error: file not found: {in_path}", file=sys.stderr)
        sys.exit(1)

    out_path = Path(args.out).resolve() if args.out else in_path.with_suffix('.html')

    md_text = in_path.read_text(encoding="utf-8")
    html = md_to_html_email(md_text)
    out_path.write_text(html, encoding="utf-8")
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
