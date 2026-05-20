#!/usr/bin/env python3
"""
cb_stakeholder_email.py — Convert a Cognitivebotics stakeholder communication .md
file into a branded HTML email ready to paste into Gmail or Outlook.

SVG files referenced with ![alt](path/to/file.svg) are read from disk and
inlined directly so they render in any email client.

CLI:
    python3 tools/cb_stakeholder_email.py path/to/2026-05-20-onboarding-explainer.md
    python3 tools/cb_stakeholder_email.py path/to/file.md --out path/to/output.html
"""

from __future__ import annotations
import sys, os, re, argparse
from pathlib import Path

_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _dir)
import cb_brand as B


# ── Color helpers ──────────────────────────────────────────────────────────────

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


# ── Style builder ──────────────────────────────────────────────────────────────

def _s(**kw) -> str:
    return "; ".join(f"{k.replace('_', '-')}: {v}" for k, v in kw.items())


# ── Inline markdown → HTML ────────────────────────────────────────────────────

def _inline(text: str) -> str:
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'_(.+?)_', r'<em>\1</em>', text)
    return text


# ── SVG inliner ───────────────────────────────────────────────────────────────

def _inline_svg(svg_path: Path) -> str:
    if not svg_path.exists():
        return (
            f'<div style="{_s(background_color=MINT, border=f"1px dashed {CYAN}", padding="12px 16px", color=GRAY, font_family=FONT_B, font_size="12px", margin="0 0 20px 0")}">'
            f'[SVG not found: {svg_path.name}]</div>'
        )
    svg_content = svg_path.read_text(encoding="utf-8")
    # Remove XML declaration if present
    svg_content = re.sub(r'<\?xml[^>]+\?>', '', svg_content).strip()
    # Add display block and max-width so it scales in email
    svg_content = re.sub(
        r'^<svg',
        '<svg style="display:block; max-width:100%; height:auto;"',
        svg_content,
        count=1,
    )
    return f'<div style="margin: 0 0 24px 0; line-height: 0;">{svg_content}</div>'


# ── Block renderers ───────────────────────────────────────────────────────────

def render_section_header(title: str) -> str:
    style = _s(
        background_color=DARK_TEAL,
        color=WHITE,
        font_family=FONT_H,
        font_size="14px",
        font_weight="700",
        padding="12px 16px",
        margin="28px -32px 16px -32px",
        letter_spacing="0.3px",
    )
    return f'<div style="{style}">{_inline(title)}</div>'


def render_subsection_header(title: str) -> str:
    style = _s(
        color=DARK_TEAL,
        font_family=FONT_H,
        font_size="13px",
        font_weight="700",
        padding="10px 0 5px 0",
        border_bottom=f"2px solid {CYAN}",
        margin="0 0 12px 0",
    )
    return f'<div style="{style}">{_inline(title)}</div>'


def render_para(text: str) -> str:
    style = _s(
        color=BLACK,
        font_family=FONT_B,
        font_size="13px",
        line_height="1.7",
        margin="0 0 12px 0",
    )
    return f'<p style="{style}">{_inline(text)}</p>'


def render_bullet(text: str, indent: int = 0) -> str:
    pad = 20 + indent * 16
    style = _s(
        color=BLACK,
        font_family=FONT_B,
        font_size="13px",
        line_height="1.6",
        margin="0 0 6px 0",
        padding_left=f"{pad}px",
        position="relative",
    )
    bullet = "&#8226;" if indent == 0 else "&#8722;"
    bullet_style = _s(
        position="absolute",
        left=f"{pad - 14}px",
        color=CYAN,
        font_weight="700",
    )
    return (
        f'<div style="{style}">'
        f'<span style="{bullet_style}">{bullet}</span>'
        f'{_inline(text)}</div>'
    )


def render_numbered(text: str, n: int) -> str:
    style = _s(
        color=BLACK,
        font_family=FONT_B,
        font_size="13px",
        line_height="1.6",
        margin="0 0 6px 0",
        padding_left="24px",
        position="relative",
    )
    num_style = _s(
        position="absolute",
        left="0",
        color=TEAL,
        font_weight="700",
        font_family=FONT_H,
    )
    return (
        f'<div style="{style}">'
        f'<span style="{num_style}">{n}.</span>'
        f'{_inline(text)}</div>'
    )


def render_action_item(text: str) -> str:
    text = re.sub(r'^-\s*\[\s*\]\s*', '', text).strip()
    parts = text.split(' — ', 1)
    action = parts[0].strip()
    meta = parts[1].strip() if len(parts) > 1 else ''
    style = _s(
        background_color=MINT,
        border_left=f"4px solid {CYAN}",
        padding="10px 14px",
        margin="0 0 8px 0",
        font_family=FONT_B,
        font_size="13px",
        color=BLACK,
        line_height="1.5",
    )
    meta_html = f' <span style="color:{GRAY}; font-size:12px;">— {_inline(meta)}</span>' if meta else ''
    return f'<div style="{style}">&#10003;&nbsp; <strong>{_inline(action)}</strong>{meta_html}</div>'


def render_blockquote(lines: list[str]) -> str:
    parts = [line.strip().lstrip('> ').strip() for line in lines if line.strip().lstrip('> ').strip()]
    content = ' '.join(parts)
    style = _s(
        background_color=MINT,
        border_left=f"4px solid {CYAN}",
        padding="10px 14px",
        margin="0 0 16px 0",
        color=GRAY,
        font_family=FONT_B,
        font_size="12px",
        line_height="1.6",
    )
    return f'<div style="{style}">{_inline(content)}</div>'


def render_table(lines: list[str]) -> str:
    rows = []
    for line in lines:
        if re.match(r'^\|[-:\s|]+\|$', line.strip()):
            continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        rows.append(cells)
    if not rows:
        return ''
    html = (
        f'<table style="{_s(width="100%", border_collapse="collapse", font_family=FONT_B, font_size="13px", margin="8px 0 20px 0")}"'
        f' cellpadding="0" cellspacing="0">'
    )
    for i, row in enumerate(rows):
        if i == 0:
            html += f'<tr style="{_s(background_color=TEAL)}">'
            for cell in row:
                html += (
                    f'<td style="{_s(padding="10px 14px", color=WHITE, font_family=FONT_H, font_weight="700", font_size="12px", text_transform="uppercase", letter_spacing="0.5px", border=f"1px solid {DARK_TEAL}")}">'
                    f'{_inline(cell)}</td>'
                )
        else:
            bg = MINT if i % 2 == 0 else WHITE
            html += f'<tr style="{_s(background_color=bg)}">'
            for cell in row:
                html += (
                    f'<td style="{_s(padding="9px 14px", color=BLACK, font_family=FONT_B, font_size="13px", border=f"1px solid {BORDER}", vertical_align="top")}">'
                    f'{_inline(cell)}</td>'
                )
        html += '</tr>'
    html += '</table>'
    return html


# ── Main converter ────────────────────────────────────────────────────────────

def md_to_stakeholder_email(md_text: str, source_dir: Path) -> str:
    lines = md_text.splitlines()

    title = "Cognitivebotics"
    to_field = ""
    subject_field = ""
    purpose_field = ""
    prepared_field = ""
    i = 0

    # Parse preamble (H1 + bold meta fields before first ---)
    while i < len(lines):
        stripped = lines[i].strip()
        if stripped.startswith('# '):
            title = stripped[2:].strip()
        elif re.match(r'^\*\*To:\*\*', stripped):
            to_field = re.sub(r'^\*\*To:\*\*\s*', '', stripped).strip()
        elif re.match(r'^\*\*Subject:\*\*', stripped):
            subject_field = re.sub(r'^\*\*Subject:\*\*\s*', '', stripped).strip()
        elif re.match(r'^\*\*Purpose:\*\*', stripped):
            purpose_field = re.sub(r'^\*\*Purpose:\*\*\s*', '', stripped).strip()
        elif re.match(r'^\*\*Prepared:\*\*', stripped):
            prepared_field = re.sub(r'^\*\*Prepared:\*\*\s*', '', stripped).strip()
        elif stripped == '---':
            i += 1
            break
        i += 1

    # Build meta block for header
    meta_parts = []
    if to_field:
        meta_parts.append(f"To: {to_field}")
    if subject_field:
        meta_parts.append(f"Subject: {subject_field}")
    if prepared_field:
        meta_parts.append(f"Prepared: {prepared_field}")
    meta_line = "&nbsp;&nbsp;·&nbsp;&nbsp;".join(meta_parts)

    # Parse body
    body_html = ""
    if purpose_field:
        purpose_style = _s(
            background_color="#F0FAFA",
            border_left=f"4px solid {TEAL}",
            padding="12px 16px",
            margin="16px 0 4px 0",
            color=DARK_TEAL,
            font_family=FONT_B,
            font_size="13px",
            line_height="1.6",
            font_style="italic",
        )
        body_html += f'<div style="{purpose_style}">{_inline(purpose_field)}</div>'

    list_buffer: list[tuple[str, int]] = []   # (text, indent)
    numbered_buffer: list[str] = []
    in_next_steps = False

    def flush_lists() -> str:
        nonlocal list_buffer, numbered_buffer
        out = ""
        if list_buffer:
            for txt, indent in list_buffer:
                out += render_bullet(txt, indent)
            out += '<div style="margin-bottom:12px;"></div>'
            list_buffer = []
        if numbered_buffer:
            for n, txt in enumerate(numbered_buffer, 1):
                out += render_numbered(txt, n)
            out += '<div style="margin-bottom:12px;"></div>'
            numbered_buffer = []
        return out

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped == '---':
            body_html += flush_lists()
            i += 1
            continue

        # ## Section header
        if re.match(r'^## ', stripped):
            body_html += flush_lists()
            section_title = re.sub(r'^##\s+', '', stripped).strip()
            in_next_steps = section_title.lower().startswith('next step')
            body_html += render_section_header(section_title)
            i += 1
            continue

        # ### Subsection header
        if re.match(r'^### ', stripped):
            body_html += flush_lists()
            sub_title = re.sub(r'^###\s+', '', stripped).strip()
            body_html += render_subsection_header(sub_title)
            i += 1
            continue

        # Table
        if stripped.startswith('|'):
            body_html += flush_lists()
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                table_lines.append(lines[i].strip())
                i += 1
            body_html += render_table(table_lines)
            continue

        # Blockquote
        if stripped.startswith('>'):
            body_html += flush_lists()
            bq_lines = []
            while i < len(lines) and lines[i].strip().startswith('>'):
                bq_lines.append(lines[i])
                i += 1
            body_html += render_blockquote(bq_lines)
            continue

        # SVG image reference  ![alt](path.svg)
        svg_match = re.match(r'^!\[([^\]]*)\]\(([^)]+\.svg)\)', stripped)
        if svg_match:
            body_html += flush_lists()
            alt = svg_match.group(1)
            svg_rel = svg_match.group(2)
            svg_path = (source_dir / svg_rel).resolve()
            if alt:
                caption_style = _s(
                    font_family=FONT_B,
                    font_size="11px",
                    color=GRAY,
                    text_align="center",
                    margin="4px 0 16px 0",
                )
                body_html += _inline_svg(svg_path)
                body_html += f'<div style="{caption_style}">{_inline(alt)}</div>'
            else:
                body_html += _inline_svg(svg_path)
            i += 1
            continue

        # Action items (- [ ] ...) — styled as checkboxes in Next Steps or anywhere
        if re.match(r'^-\s*\[\s*\]', stripped):
            body_html += flush_lists()
            body_html += render_action_item(stripped)
            i += 1
            continue

        # Indented bullet (  - or    -)
        indent_match = re.match(r'^(\s{2,})-\s+(.+)', line)
        if indent_match:
            body_html += flush_lists() if numbered_buffer else ""
            indent = len(indent_match.group(1)) // 2
            list_buffer.append((indent_match.group(2).strip(), indent))
            i += 1
            continue

        # Top-level bullet (- ...)
        if re.match(r'^-\s+', stripped):
            if numbered_buffer:
                body_html += flush_lists()
            text = re.sub(r'^-\s+', '', stripped)
            list_buffer.append((text, 0))
            i += 1
            continue

        # Numbered list (1. ...)
        num_match = re.match(r'^\d+\.\s+(.+)', stripped)
        if num_match:
            if list_buffer:
                body_html += flush_lists()
            numbered_buffer.append(num_match.group(1))
            i += 1
            continue

        # Flush any buffered lists before non-list content
        if stripped:
            body_html += flush_lists()
            body_html += render_para(stripped)
        else:
            body_html += flush_lists()

        i += 1

    body_html += flush_lists()

    # ── Assemble full email ────────────────────────────────────────────────────

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

<table width="100%" cellpadding="0" cellspacing="0" style="max-width: 680px; margin: 0 auto; background-color: {WHITE}; border-radius: 6px; overflow: hidden; border: 1px solid {BORDER}; box-shadow: 0 2px 8px rgba(0,0,0,0.07);">

  <!-- HEADER -->
  <tr>
    <td style="background: linear-gradient(135deg, {TEAL} 0%, {DARK_TEAL} 100%); padding: 28px 32px;">
      <div style="font-family: {FONT_H}; font-size: 21px; font-weight: 700; color: {WHITE}; letter-spacing: 0.3px; line-height: 1.35;">{title}</div>
      <div style="font-family: {FONT_B}; font-size: 11px; color: rgba(255,255,255,0.72); margin-top: 8px; line-height: 1.5;">{meta_line}</div>
    </td>
  </tr>

  <!-- BODY -->
  <tr>
    <td style="padding: 8px 32px 32px 32px; position: relative; overflow: hidden;">
      {body_html}
    </td>
  </tr>

  <!-- FOOTER -->
  <tr>
    <td style="background-color: {MINT}; padding: 14px 32px; border-top: 1px solid {BORDER};">
      <div style="font-family: {FONT_B}; font-size: 11px; color: {GRAY}; line-height: 1.5;">
        Cognitivebotics &nbsp;·&nbsp; Prepared {prepared_field or "by Prahlad Rebala"}
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
        description="Convert a Cognitivebotics stakeholder communication .md to a branded HTML email"
    )
    parser.add_argument("input", help="Path to the markdown communication file")
    parser.add_argument("--out", help="Output HTML path (default: same folder, .html extension)")
    args = parser.parse_args()

    in_path = Path(args.input).resolve()
    if not in_path.exists():
        print(f"Error: file not found: {in_path}", file=sys.stderr)
        sys.exit(1)

    out_path = Path(args.out).resolve() if args.out else in_path.with_suffix('.html')

    md_text = in_path.read_text(encoding="utf-8")
    html = md_to_stakeholder_email(md_text, source_dir=in_path.parent)
    out_path.write_text(html, encoding="utf-8")
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
