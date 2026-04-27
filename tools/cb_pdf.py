"""
cb_pdf.py — Cognitivebotics branded PDF library (reportlab).

QUICK START
-----------
    from cb_pdf import CB_PDF

    # From a markdown file (most common)
    CB_PDF.build_from_markdown(
        md_path  = "research-brief.md",
        out_path = "research-brief.pdf",
        title    = "Research Brief: Center Lifecycle",
        doc_type = "Research Brief",
        date     = "April 2026",
    )

    # Programmatic
    pdf = CB_PDF("Interview Script", doc_type="Primary Research", date="April 2026")
    pdf.cover_page("Interview Script: Center Owner / Admin",
                   subtitle="Discovery Stage — Center Director")
    pdf.h2("Section 1 — Warm-Up")
    pdf.body("Tell me about your center.")
    pdf.save("output.pdf")

CLI
---
    python3 cb_pdf.py input.md output.pdf
    python3 cb_pdf.py input.md output.pdf --title "My Doc" --type "Research Brief"
"""

from __future__ import annotations
import re, os, sys
from datetime import datetime

# Import brand constants
_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _dir)
import cb_brand as B

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch, cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether, PageBreak
)
from reportlab.platypus.flowables import Flowable
from reportlab.lib import colors


# ── Color helpers ─────────────────────────────────────────────────────────────

def _c(h: str) -> colors.Color:
    """Convert hex string to reportlab Color."""
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return colors.Color(r / 255, g / 255, b / 255)

C_TEAL      = _c(B.TEAL)
C_CYAN      = _c(B.CYAN)
C_DARK_TEAL = _c(B.DARK_TEAL)
C_BLACK     = _c(B.BLACK)
C_GRAY      = _c(B.GRAY)
C_MINT      = _c(B.MINT)
C_WHITE     = colors.white
C_BORDER    = _c(B.BORDER)
C_RED       = _c(B.RED)

# Font: Helvetica is always available in reportlab.
# Nunito / Open Sans are referenced by name and will fall back to Helvetica
# if not registered.  To register custom TTF fonts:
#   from reportlab.pdfbase import pdfmetrics
#   from reportlab.pdfbase.ttfonts import TTFont
#   pdfmetrics.registerFont(TTFont('Nunito-Bold', '/path/to/Nunito-Bold.ttf'))
#
_HF  = 'Helvetica'          # heading fallback
_HFB = 'Helvetica-Bold'
_BF  = 'Helvetica'          # body fallback


# ── Paragraph styles ──────────────────────────────────────────────────────────

def _styles() -> dict:
    return {
        'h1': ParagraphStyle('h1',
            fontName=_HFB, fontSize=B.SZ_H1, textColor=C_TEAL,
            spaceBefore=B.SP_H1_BEFORE, spaceAfter=B.SP_H1_AFTER,
            leading=B.SZ_H1 * 1.3,
            borderPadding=(0, 0, 4, 0),
        ),
        'h2': ParagraphStyle('h2',
            fontName=_HFB, fontSize=B.SZ_H2, textColor=C_DARK_TEAL,
            spaceBefore=B.SP_H2_BEFORE, spaceAfter=B.SP_H2_AFTER,
            leading=B.SZ_H2 * 1.3,
        ),
        'h3': ParagraphStyle('h3',
            fontName=_HFB, fontSize=B.SZ_H3, textColor=C_CYAN,
            spaceBefore=B.SP_H3_BEFORE, spaceAfter=B.SP_H3_AFTER,
            leading=B.SZ_H3 * 1.3,
        ),
        'body': ParagraphStyle('body',
            fontName=_BF, fontSize=B.SZ_BODY, textColor=C_BLACK,
            spaceBefore=0, spaceAfter=B.SP_BODY_AFTER,
            leading=B.SZ_BODY * 1.4,
        ),
        'italic': ParagraphStyle('italic',
            fontName=_BF, fontSize=B.SZ_SMALL, textColor=C_GRAY,
            spaceBefore=2, spaceAfter=2,
            leading=B.SZ_SMALL * 1.4,
            leftIndent=24, fontStyle='italic',
        ),
        'small': ParagraphStyle('small',
            fontName=_BF, fontSize=B.SZ_SMALL, textColor=C_GRAY,
            spaceBefore=0, spaceAfter=2,
            leading=B.SZ_SMALL * 1.3,
        ),
        'kv_key': ParagraphStyle('kv_key',
            fontName=_HFB, fontSize=B.SZ_BODY, textColor=C_TEAL,
            spaceBefore=2, spaceAfter=2,
        ),
        'bullet': ParagraphStyle('bullet',
            fontName=_BF, fontSize=B.SZ_BODY, textColor=C_BLACK,
            spaceBefore=1, spaceAfter=2,
            leftIndent=18, bulletIndent=0,
            leading=B.SZ_BODY * 1.4,
        ),
        'bullet2': ParagraphStyle('bullet2',
            fontName=_BF, fontSize=B.SZ_BODY, textColor=C_BLACK,
            spaceBefore=1, spaceAfter=2,
            leftIndent=36, bulletIndent=18,
            leading=B.SZ_BODY * 1.4,
        ),
        'checkbox': ParagraphStyle('checkbox',
            fontName=_BF, fontSize=B.SZ_BODY, textColor=C_BLACK,
            spaceBefore=1, spaceAfter=2,
            leftIndent=18, bulletIndent=0,
        ),
        'question': ParagraphStyle('question',
            fontName=_BF, fontSize=B.SZ_BODY, textColor=C_BLACK,
            spaceBefore=8, spaceAfter=2,
            leftIndent=24, firstLineIndent=-24,
            leading=B.SZ_BODY * 1.4,
        ),
        'callout': ParagraphStyle('callout',
            fontName=_BF, fontSize=B.SZ_BODY, textColor=C_BLACK,
            spaceBefore=2, spaceAfter=2,
            leftIndent=8, rightIndent=8,
            leading=B.SZ_BODY * 1.4,
        ),
        'quote': ParagraphStyle('quote',
            fontName=_BF, fontSize=B.SZ_BODY, textColor=C_BLACK,
            spaceBefore=4, spaceAfter=4,
            leftIndent=8, rightIndent=8,
            leading=B.SZ_BODY * 1.5,
            fontStyle='italic',
        ),
        'cover_title': ParagraphStyle('cover_title',
            fontName=_HFB, fontSize=B.SZ_COVER, textColor=C_WHITE,
            spaceBefore=0, spaceAfter=8,
            leading=B.SZ_COVER * 1.2,
        ),
        'cover_sub': ParagraphStyle('cover_sub',
            fontName=_BF, fontSize=B.SZ_SUB, textColor=C_WHITE,
            spaceBefore=0, spaceAfter=4,
        ),
        'cover_meta': ParagraphStyle('cover_meta',
            fontName=_BF, fontSize=B.SZ_BODY, textColor=C_GRAY,
            spaceBefore=4, spaceAfter=2,
        ),
    }


# ── Callout box flowable ──────────────────────────────────────────────────────

class CalloutBox(Flowable):
    """Mint background box with thick cyan left border."""

    def __init__(self, content: list, width: float = None,
                 bg=C_MINT, border=C_CYAN, border_width: float = 3):
        super().__init__()
        self._content     = content    # list of (text, style_name) tuples
        self._width       = width or (letter[0] - 2 * inch)
        self._bg          = bg
        self._border      = border
        self._border_width = border_width
        self._styles      = _styles()

    def wrap(self, availW, availH):
        self.width  = min(availW, self._width)
        # Estimate height
        self.height = len(self._content) * 18 + 12
        return self.width, self.height

    def draw(self):
        c = self.canv
        c.saveState()
        # Background
        c.setFillColor(self._bg)
        c.rect(0, 0, self.width, self.height, fill=1, stroke=0)
        # Left border
        c.setFillColor(self._border)
        c.rect(0, 0, self._border_width, self.height, fill=1, stroke=0)
        c.restoreState()


def _callout_table(lines: list[str], title: str = None,
                   available_width: float = None) -> Table:
    """Build a callout box as a single-cell Table (reliable in Platypus)."""
    st = _styles()
    w  = available_width or (letter[0] - 2 * inch)
    paras = []
    if title:
        paras.append(Paragraph(f'<b><font color="#{B.TEAL}">{title}</font></b>', st['callout']))
    for line in lines:
        paras.append(Paragraph(_md_to_rl(line), st['callout']))

    tbl = Table([[paras]], colWidths=[w])
    tbl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_MINT),
        ('LINEBEFORE',  (0, 0), (-1, -1), 3.5, C_CYAN),
        ('LINETOP',     (0, 0), (-1, -1), 0,   C_MINT),
        ('LINERIGHT',   (0, 0), (-1, -1), 0,   C_MINT),
        ('LINEBOTTOM',  (0, 0), (-1, -1), 0,   C_MINT),
        ('TOPPADDING',  (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('VALIGN',      (0, 0), (-1, -1), 'TOP'),
    ]))
    return tbl


def _md_to_rl(text: str) -> str:
    """Convert simple **bold** and *italic* markdown to ReportLab XML tags."""
    # Bold
    text = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', text)
    # Italic (only single *)
    text = re.sub(r'\*([^*]+)\*', r'<i>\1</i>', text)
    return text


# ── Header / footer canvas callback ──────────────────────────────────────────

class _HeaderFooterCanvas:
    """Mixin that draws header/footer on every page via a canvas callback."""

    def __init__(self, title: str, doc_type: str, date: str,
                 page_count_holder: dict):
        self.title             = title
        self.doc_type          = doc_type
        self.date              = date
        self.page_count_holder = page_count_holder

    def __call__(self, canvas, doc):
        canvas.saveState()
        w, h = letter

        # ── Header (skip cover page) ──
        if doc.page > 1:
            canvas.setFillColor(C_TEAL)
            canvas.setFont(_HFB, B.SZ_SMALL)
            canvas.drawString(inch, h - 0.55 * inch, self.title)
            canvas.setFillColor(C_GRAY)
            canvas.setFont(_BF, B.SZ_SMALL)
            canvas.drawRightString(w - inch, h - 0.55 * inch, B.PRODUCT_NAME)
            canvas.setStrokeColor(C_TEAL)
            canvas.setLineWidth(1)
            canvas.line(inch, h - 0.62 * inch, w - inch, h - 0.62 * inch)

        # ── Footer ──
        y_foot = 0.45 * inch
        canvas.setStrokeColor(C_BORDER)
        canvas.setLineWidth(0.5)
        canvas.line(inch, y_foot + 0.12 * inch, w - inch, y_foot + 0.12 * inch)

        canvas.setFillColor(C_GRAY)
        canvas.setFont(_BF, 8)
        canvas.drawString(inch, y_foot, B.CONFIDENTIALITY)
        canvas.drawCentredString(w / 2, y_foot, f'Page {doc.page}')
        canvas.drawRightString(w - inch, y_foot, self.date)

        canvas.restoreState()


# ── CB_PDF class ──────────────────────────────────────────────────────────────

class CB_PDF:
    """
    Cognitivebotics branded PDF builder using reportlab Platypus.

    Build content with method calls, then call `.save(path)`.
    """

    def __init__(self, title: str = 'Document',
                 doc_type: str = 'Internal',
                 date: str = 'April 2026'):
        self._title    = title
        self._doc_type = doc_type
        self._date     = date
        self._story: list = []
        self._st       = _styles()
        self._page_count = {'total': '?'}

    # ── Cover ─────────────────────────────────────────────────────────────────

    def cover_page(self, title: str, subtitle: str = '',
                   meta: list[tuple[str, str]] = None) -> 'CB_PDF':
        """Full cover page with teal header band."""
        w, h = letter
        inner_w = w - 2 * inch

        # Cover band (implemented as a table row with teal background)
        cover_rows = [[Paragraph(_md_to_rl(title), self._st['cover_title'])]]
        if subtitle:
            cover_rows.append([Paragraph(subtitle, self._st['cover_sub'])])

        cover_tbl = Table(cover_rows, colWidths=[inner_w])
        cover_tbl.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), C_TEAL),
            ('TOPPADDING',    (0, 0), (-1, -1), 24),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 24),
            ('LEFTPADDING',   (0, 0), (-1, -1), 16),
            ('RIGHTPADDING',  (0, 0), (-1, -1), 16),
        ]))
        self._story.append(cover_tbl)
        self._story.append(Spacer(1, 0.3 * inch))

        # Metadata below band
        if meta:
            for k, v in meta:
                self._story.append(
                    Paragraph(f'<b><font color="#{B.TEAL}">{k}:</font></b>  {v}',
                              self._st['cover_meta']))
        self._story.append(Spacer(1, 0.2 * inch))

        # Dark bottom strip
        strip = Table([['']], colWidths=[inner_w], rowHeights=[8])
        strip.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), C_DARK_TEAL)]))
        self._story.append(strip)
        self._story.append(PageBreak())
        return self

    # ── Headings ──────────────────────────────────────────────────────────────

    def h1(self, text: str) -> 'CB_PDF':
        self._story.append(Paragraph(_md_to_rl(text), self._st['h1']))
        self._story.append(
            HRFlowable(width='100%', thickness=1.5, color=C_TEAL, spaceAfter=6))
        return self

    def h2(self, text: str) -> 'CB_PDF':
        self._story.append(Paragraph(_md_to_rl(text), self._st['h2']))
        return self

    def h3(self, text: str) -> 'CB_PDF':
        self._story.append(Paragraph(_md_to_rl(text), self._st['h3']))
        return self

    # ── Body ──────────────────────────────────────────────────────────────────

    def body(self, text: str) -> 'CB_PDF':
        self._story.append(Paragraph(_md_to_rl(text), self._st['body']))
        return self

    def italic(self, text: str) -> 'CB_PDF':
        clean = text.strip().strip('*')
        self._story.append(Paragraph(f'<i>{_md_to_rl(clean)}</i>', self._st['italic']))
        return self

    def kv(self, key: str, value: str) -> 'CB_PDF':
        self._story.append(
            Paragraph(f'<b><font color="#{B.TEAL}">{key}:</font></b>  {_md_to_rl(value)}',
                      self._st['body']))
        return self

    def spacer(self, height: float = 0.1) -> 'CB_PDF':
        self._story.append(Spacer(1, height * inch))
        return self

    def rule(self) -> 'CB_PDF':
        self._story.append(
            HRFlowable(width='100%', thickness=0.5, color=C_BORDER, spaceAfter=4))
        return self

    # ── Lists ─────────────────────────────────────────────────────────────────

    def bullet(self, text: str, level: int = 0) -> 'CB_PDF':
        sym   = '•' if level == 0 else '–'
        color = B.CYAN if level == 0 else B.TEAL
        style = self._st['bullet'] if level == 0 else self._st['bullet2']
        self._story.append(
            Paragraph(f'<font color="#{color}">{sym}</font>  {_md_to_rl(text)}',
                      style))
        return self

    def checkbox(self, text: str) -> 'CB_PDF':
        self._story.append(
            Paragraph(f'<font color="#{B.TEAL}">☐</font>  {_md_to_rl(text)}',
                      self._st['checkbox']))
        return self

    def question(self, number: int | str, text: str) -> 'CB_PDF':
        self._story.append(Spacer(1, 0.06 * inch))
        self._story.append(
            Paragraph(
                f'<b><font color="#{B.TEAL}">{number}.</font></b>  {_md_to_rl(text)}',
                self._st['question']))
        return self

    # ── Callout elements ──────────────────────────────────────────────────────

    def blockquote(self, text: str) -> 'CB_PDF':
        parts = [p.strip() for p in text.split('\n') if p.strip()]
        self._story.append(_callout_table(parts))
        self._story.append(Spacer(1, 0.1 * inch))
        return self

    def callout(self, lines: list[str], title: str = None) -> 'CB_PDF':
        self._story.append(_callout_table(lines, title=title))
        self._story.append(Spacer(1, 0.1 * inch))
        return self

    # ── Tables ────────────────────────────────────────────────────────────────

    def table(self, headers: list[str], rows: list[list[str]],
              col_widths: list[float] = None) -> 'CB_PDF':
        """Branded table: teal header, alternating mint/white rows."""
        inner_w = letter[0] - 2 * inch
        ncols   = len(headers)

        if col_widths:
            cw = [w * inch for w in col_widths]
        else:
            cw = [inner_w / ncols] * ncols

        st = self._st
        header_row = [Paragraph(f'<b><font color="white">{h}</font></b>',
                                 ParagraphStyle('th', fontName=_HFB,
                                                fontSize=B.SZ_SMALL + 1,
                                                textColor=C_WHITE))
                       for h in headers]
        data = [header_row]
        for r in rows:
            data.append([Paragraph(_md_to_rl(str(v)), st['body'])
                         for v in r[:ncols]])

        tbl = Table(data, colWidths=cw, repeatRows=1)

        row_styles = [
            ('BACKGROUND', (0, 0), (-1, 0), C_TEAL),
            ('GRID',       (0, 0), (-1, -1), 0.5, C_BORDER),
            ('TOPPADDING',    (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING',   (0, 0), (-1, -1), 6),
            ('RIGHTPADDING',  (0, 0), (-1, -1), 6),
            ('VALIGN',        (0, 0), (-1, -1), 'TOP'),
        ]
        for i in range(1, len(data)):
            if i % 2 == 0:
                row_styles.append(('BACKGROUND', (0, i), (-1, i), C_MINT))

        tbl.setStyle(TableStyle(row_styles))
        self._story.append(tbl)
        self._story.append(Spacer(1, 0.1 * inch))
        return self

    def cover_table(self, pairs: list[tuple[str, str]]) -> 'CB_PDF':
        """Two-column metadata cover block."""
        inner_w = letter[0] - 2 * inch
        data = []
        for k, v in pairs:
            data.append([
                Paragraph(f'<b><font color="#{B.TEAL}">{k}</font></b>',
                          self._st['small']),
                Paragraph(_md_to_rl(v), self._st['small']),
            ])
        tbl = Table(data, colWidths=[1.8 * inch, inner_w - 1.8 * inch])
        row_styles = [
            ('GRID',    (0, 0), (-1, -1), 0.5, C_BORDER),
            ('TOPPADDING',    (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('LEFTPADDING',   (0, 0), (-1, -1), 6),
            ('RIGHTPADDING',  (0, 0), (-1, -1), 6),
        ]
        for i in range(0, len(data), 2):
            row_styles.append(('BACKGROUND', (0, i), (-1, i), C_MINT))
        tbl.setStyle(TableStyle(row_styles))
        self._story.append(tbl)
        self._story.append(Spacer(1, 0.15 * inch))
        return self

    # ── Build & save ──────────────────────────────────────────────────────────

    def save(self, path: str):
        cb = _HeaderFooterCanvas(
            title=self._title, doc_type=self._doc_type,
            date=self._date, page_count_holder=self._page_count)

        doc = SimpleDocTemplate(
            path,
            pagesize=letter,
            leftMargin=inch, rightMargin=inch,
            topMargin=0.9 * inch, bottomMargin=0.75 * inch,
            title=self._title,
            author=B.COMPANY_NAME,
        )
        doc.build(self._story, onFirstPage=cb, onLaterPages=cb)
        print(f'Saved: {path}  ({doc.page} pages)')
        return path

    # ── Markdown builder ──────────────────────────────────────────────────────

    def from_markdown_content(self, content: str,
                               skip_top_metadata: bool = True) -> 'CB_PDF':
        lines     = content.split('\n')
        i         = 0
        meta_done = False

        while i < len(lines):
            line     = lines[i]
            stripped = line.strip()

            if not stripped:
                i += 1
                continue

            if stripped == '---':
                meta_done = True
                i += 1
                continue

            if stripped.startswith('# ') and not stripped.startswith('## '):
                if skip_top_metadata and not meta_done:
                    i += 1
                    continue
                self.h1(stripped[2:].strip())
                i += 1
                continue

            if not meta_done and re.match(r'^\*\*[^*]+\*\*', stripped):
                i += 1
                continue

            if stripped.startswith('## ') and not stripped.startswith('### '):
                meta_done = True
                self.h2(stripped[3:].strip())
                i += 1
                continue

            if stripped.startswith('### '):
                meta_done = True
                self.h3(stripped[4:].strip())
                i += 1
                continue

            if stripped.startswith('>'):
                meta_done = True
                parts = []
                while i < len(lines) and lines[i].strip().startswith('>'):
                    p = lines[i].strip()
                    parts.append('' if p == '>' else p[2:])
                    i += 1
                self.blockquote('\n'.join(x for x in parts))
                continue

            if stripped.startswith('|'):
                meta_done = True
                rows_raw = []
                while i < len(lines) and lines[i].strip().startswith('|'):
                    raw = lines[i].strip()
                    if not re.match(r'^\|[\s\-\|:]+\|$', raw):
                        cells = [c.strip() for c in raw.split('|') if c.strip()]
                        if cells:
                            rows_raw.append(cells)
                    i += 1
                if rows_raw:
                    max_c = max(len(r) for r in rows_raw)
                    rows_raw = [r + [''] * (max_c - len(r)) for r in rows_raw]
                    self.table(rows_raw[0], rows_raw[1:])
                continue

            if stripped.startswith('- [ ]'):
                meta_done = True
                self.checkbox(stripped[5:].strip())
                i += 1
                continue

            if re.match(r'^[ \t]{3,}- ', line):
                meta_done = True
                self.bullet(re.sub(r'^[ \t]+-\s+', '', line).strip(), level=1)
                i += 1
                continue

            if stripped.startswith('- '):
                meta_done = True
                self.bullet(stripped[2:])
                i += 1
                continue

            m = re.match(r'^(\d+)\.\s+(.+)$', stripped)
            if m:
                meta_done = True
                self.question(m.group(1), m.group(2))
                i += 1
                continue

            if re.match(r'^[ \t]{3,}\*', line):
                meta_done = True
                self.italic(stripped)
                i += 1
                continue

            if (stripped.startswith('*') and not stripped.startswith('**')
                    and stripped.endswith('*') and not stripped.endswith('**')):
                meta_done = True
                self.italic(stripped[1:-1] if len(stripped) > 2 else stripped)
                i += 1
                continue

            m_kv = re.match(r'^\*\*(.+?):\*\*\s*(.*)$', stripped)
            if m_kv:
                meta_done = True
                self.kv(m_kv.group(1), m_kv.group(2).strip())
                i += 1
                continue

            if stripped:
                meta_done = True
                self.body(stripped)
            i += 1

        return self

    @classmethod
    def build_from_markdown(cls, md_path: str, out_path: str,
                             title: str = None, doc_type: str = 'Internal',
                             date: str = 'April 2026',
                             with_cover: bool = True) -> str:
        """One-call: markdown file → branded PDF."""
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()

        h1_text = ''
        meta    = []
        for line in content.split('\n'):
            s = line.strip()
            if s.startswith('# ') and not s.startswith('## ') and not h1_text:
                h1_text = s[2:].strip()
            elif re.match(r'^\*\*(.+?):\*\*\s*(.+)$', s):
                m = re.match(r'^\*\*(.+?):\*\*\s*(.+)$', s)
                meta.append((m.group(1), m.group(2)))
            elif s == '---':
                break

        if not title:
            title = h1_text or os.path.splitext(os.path.basename(md_path))[0]

        pdf = cls(title=title, doc_type=doc_type, date=date)

        if with_cover:
            pdf.cover_page(h1_text or title, subtitle=doc_type, meta=meta)
        else:
            pdf.h1(h1_text or title)
            if meta:
                pdf.cover_table(meta)

        pdf.from_markdown_content(content, skip_top_metadata=True)
        pdf.save(out_path)
        return out_path


# ── CLI ───────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser(description='Convert markdown to branded PDF')
    ap.add_argument('input',             help='Input .md file')
    ap.add_argument('output',            help='Output .pdf file')
    ap.add_argument('--title', '-t',     default=None,       help='Document title')
    ap.add_argument('--type',  '-y',     default='Internal', help='Document type label')
    ap.add_argument('--date',  '-d',     default='April 2026', help='Date in footer')
    ap.add_argument('--no-cover',        action='store_true', help='Skip cover page')
    args = ap.parse_args()
    CB_PDF.build_from_markdown(
        args.input, args.output,
        title=args.title, doc_type=args.type, date=args.date,
        with_cover=not args.no_cover)
