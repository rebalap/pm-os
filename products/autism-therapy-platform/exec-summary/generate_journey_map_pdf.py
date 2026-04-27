#!/usr/bin/env python3
"""
Generates branded PDF for the Autism Therapy Platform Journey Map Executive Summary.
Uses reportlab Platypus with Cognitivebotics brand identity.
"""

import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
pt = 1  # reportlab uses points natively; 1pt = 1 unit
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer,
    HRFlowable, KeepTogether, PageBreak, Flowable
)
from reportlab.pdfgen import canvas
from reportlab.platypus.flowables import Flowable

# ── Brand Colors ──────────────────────────────────────────────────────────────
TEAL        = colors.HexColor('#175F63')
CYAN        = colors.HexColor('#20A6AD')
DARK_TEAL   = colors.HexColor('#10494C')
HEADING_BK  = colors.HexColor('#101319')
BODY_GRAY   = colors.HexColor('#646871')
WHITE       = colors.white
LIGHT_MINT  = colors.HexColor('#EEF9F9')
BORDER_GRAY = colors.HexColor('#CBCBCB')
ALERT_RED   = colors.HexColor('#cd423a')
BLACK       = colors.black

# ── Page Geometry ─────────────────────────────────────────────────────────────
PAGE_W, PAGE_H = A4          # 595.27 x 841.89 pt
MARGIN        = 2.5 * cm
INNER_W       = PAGE_W - 2 * MARGIN

# Output path
OUTPUT_PATH = (
    "/Users/prahladrebala/Documents/pm-os/products/autism-therapy-platform/"
    "exec-summary/journey-map-exec-summary.pdf"
)

# ── Paragraph Styles ──────────────────────────────────────────────────────────
def make_styles():
    s = {}

    s['body'] = ParagraphStyle(
        'body',
        fontName='Helvetica',
        fontSize=10.5,
        leading=10.5 * 1.35,
        textColor=HEADING_BK,
        spaceAfter=6,
    )
    s['body_gray'] = ParagraphStyle(
        'body_gray',
        parent=s['body'],
        textColor=BODY_GRAY,
    )
    s['body_italic'] = ParagraphStyle(
        'body_italic',
        fontName='Helvetica-Oblique',
        fontSize=10,
        leading=10 * 1.35,
        textColor=BODY_GRAY,
        leftIndent=15,
        spaceAfter=6,
    )
    s['bullet'] = ParagraphStyle(
        'bullet',
        fontName='Helvetica',
        fontSize=10.5,
        leading=10.5 * 1.35,
        textColor=HEADING_BK,
        leftIndent=15,
        spaceAfter=4,
        bulletIndent=0,
    )
    s['stage_heading'] = ParagraphStyle(
        'stage_heading',
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=TEAL,
        spaceAfter=6,
        spaceBefore=12,
    )
    s['section_heading'] = ParagraphStyle(
        'section_heading',
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=TEAL,
        spaceAfter=8,
        spaceBefore=14,
    )
    s['table_header'] = ParagraphStyle(
        'table_header',
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=WHITE,
    )
    s['table_cell'] = ParagraphStyle(
        'table_cell',
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=HEADING_BK,
    )
    s['table_cell_red'] = ParagraphStyle(
        'table_cell_red',
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=ALERT_RED,
    )
    s['numbered_item'] = ParagraphStyle(
        'numbered_item',
        fontName='Helvetica',
        fontSize=10.5,
        leading=10.5 * 1.35,
        textColor=HEADING_BK,
        leftIndent=20,
        spaceAfter=8,
    )
    s['cover_title'] = ParagraphStyle(
        'cover_title',
        fontName='Helvetica-Bold',
        fontSize=26,
        leading=32,
        textColor=WHITE,
        alignment=TA_CENTER,
    )
    s['cover_subtitle'] = ParagraphStyle(
        'cover_subtitle',
        fontName='Helvetica',
        fontSize=16,
        leading=22,
        textColor=WHITE,
        alignment=TA_CENTER,
    )
    s['cover_meta'] = ParagraphStyle(
        'cover_meta',
        fontName='Helvetica',
        fontSize=11,
        leading=16,
        textColor=BODY_GRAY,
        alignment=TA_CENTER,
        spaceAfter=4,
    )
    s['cover_meta_small'] = ParagraphStyle(
        'cover_meta_small',
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=BODY_GRAY,
        alignment=TA_CENTER,
        spaceAfter=10,
    )
    s['legend'] = ParagraphStyle(
        'legend',
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=BODY_GRAY,
    )
    return s


# ── Custom Flowables ──────────────────────────────────────────────────────────

class StageHeadingBand(Flowable):
    """Full-width light-mint band with stage heading text."""
    def __init__(self, text, width, styles):
        super().__init__()
        self.text = text
        self.band_width = width
        self.styles = styles
        self.height = 26

    def wrap(self, avail_w, avail_h):
        return self.band_width, self.height

    def draw(self):
        c = self.canv
        # Draw background band (offset to fill from left margin edge)
        c.setFillColor(LIGHT_MINT)
        c.rect(-MARGIN, 0, PAGE_W, self.height, fill=1, stroke=0)
        # Draw text
        c.setFont('Helvetica-Bold', 13)
        c.setFillColor(TEAL)
        c.drawString(4, 7, self.text)


class CoverPage(Flowable):
    """Draws the entire cover page as a single flowable."""
    def __init__(self, page_w, page_h, styles):
        super().__init__()
        self.page_w = page_w
        self.page_h = page_h
        self.styles = styles

    def wrap(self, avail_w, avail_h):
        # This flowable fills the whole page
        return avail_w, avail_h

    def draw(self):
        c = self.canv
        pw, ph = self.page_w, self.page_h

        # ── Top teal band (~28% height) ──────────────────────────────────────
        band_h = ph * 0.28
        c.setFillColor(TEAL)
        c.rect(0, ph - band_h, pw, band_h, fill=1, stroke=0)

        # Title text — vertically centered in band
        title_text = "End-to-End User Journey"
        subtitle_text = "Autism Therapy Platform — Indian Therapy Center Lifecycle"

        # Title
        c.setFont('Helvetica-Bold', 26)
        c.setFillColor(WHITE)
        title_y = ph - band_h / 2 + 10
        c.drawCentredString(pw / 2, title_y, title_text)

        # Subtitle
        c.setFont('Helvetica', 16)
        c.setFillColor(WHITE)
        subtitle_y = title_y - 30
        c.drawCentredString(pw / 2, subtitle_y, subtitle_text)

        # ── Bottom dark strip ────────────────────────────────────────────────
        strip_h = 12
        c.setFillColor(DARK_TEAL)
        c.rect(0, 0, pw, strip_h, fill=1, stroke=0)

        # ── Body area metadata ───────────────────────────────────────────────
        body_top = ph - band_h - 40
        c.setFont('Helvetica', 11)
        c.setFillColor(BODY_GRAY)
        c.drawCentredString(pw / 2, body_top, "Prepared for: Product & Design Leadership")

        c.setFont('Helvetica', 10)
        body_top2 = body_top - 20
        c.drawCentredString(
            pw / 2, body_top2,
            "Date: 2026-04-14  |  Stage: Discovery  |  Evidence: Secondary Research"
        )

        # ── Legend box ───────────────────────────────────────────────────────
        legend_text = (
            "Evidence labels:  \u2705 Observed (peer-reviewed / regulatory)  |  "
            "\U0001f535 Inferred  |  \U0001f536 Hypothesis (unvalidated)  |  "
            "\u26a0\ufe0f DPDPA risk"
        )
        box_margin = MARGIN
        box_top = body_top2 - 40
        box_w = pw - 2 * box_margin
        box_h = 36

        # Box background
        c.setFillColor(LIGHT_MINT)
        c.rect(box_margin, box_top - box_h, box_w, box_h, fill=1, stroke=0)

        # Left cyan border
        c.setFillColor(CYAN)
        c.rect(box_margin, box_top - box_h, 3, box_h, fill=1, stroke=0)

        # Legend text
        c.setFont('Helvetica', 9)
        c.setFillColor(BODY_GRAY)
        c.drawString(box_margin + 10, box_top - 16, legend_text)


class LegendBox(Flowable):
    """Inline legend box for cover page body area (used in Platypus flow)."""
    def __init__(self, width, text, styles):
        super().__init__()
        self.box_width = width
        self.text = text
        self.styles = styles
        self.box_h = 38

    def wrap(self, avail_w, avail_h):
        return self.box_width, self.box_h

    def draw(self):
        c = self.canv
        # Box background
        c.setFillColor(LIGHT_MINT)
        c.rect(0, 0, self.box_width, self.box_h, fill=1, stroke=0)
        # Cyan left border
        c.setFillColor(CYAN)
        c.rect(0, 0, 3, self.box_h, fill=1, stroke=0)
        # Text
        c.setFont('Helvetica', 9)
        c.setFillColor(BODY_GRAY)
        c.drawString(10, self.box_h - 14, "Evidence labels:  \u2705 Observed (peer-reviewed / regulatory)  |  \U0001f535 Inferred")
        c.drawString(10, self.box_h - 26, "\U0001f536 Hypothesis (unvalidated)  |  \u26a0\ufe0f DPDPA risk")


# ── Header / Footer Canvas ────────────────────────────────────────────────────

class HeaderFooterCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        self._total_pages = 0
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        self._total_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self._draw_header_footer()
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def _draw_header_footer(self):
        page_num = self._saved_page_states.index(dict(
            (k, v) for k, v in self.__dict__.items()
            if k in self._saved_page_states[0]
        )) if hasattr(self, '_pageNumber') else self._pageNumber

        # Skip cover page (page 1)
        if self._pageNumber == 1:
            return

        pw, ph = A4

        # ── Header ────────────────────────────────────────────────────────────
        hdr_y = ph - MARGIN + 4
        self.setFont('Helvetica-Bold', 9)
        self.setFillColor(TEAL)
        self.drawString(MARGIN, hdr_y, "Autism Therapy Platform — Journey Map")

        self.setFont('Helvetica', 9)
        self.setFillColor(BODY_GRAY)
        self.drawRightString(pw - MARGIN, hdr_y, "Confidential — Internal Use")

        # Divider line
        self.setStrokeColor(TEAL)
        self.setLineWidth(1)
        self.line(MARGIN, hdr_y - 4, pw - MARGIN, hdr_y - 4)

        # ── Footer ────────────────────────────────────────────────────────────
        ftr_y = MARGIN - 14
        # Top border
        self.setStrokeColor(BORDER_GRAY)
        self.setLineWidth(0.5)
        self.line(MARGIN, ftr_y + 10, pw - MARGIN, ftr_y + 10)

        # Page number
        self.setFont('Helvetica', 8)
        self.setFillColor(BODY_GRAY)
        page_text = f"{self._pageNumber} of {self._total_pages}"
        self.drawCentredString(pw / 2, ftr_y, page_text)


def build_header_footer(canvas_obj, doc):
    """Called on each page for header/footer (fallback for SimpleDocTemplate)."""
    page_num = doc.page
    total = getattr(doc, '_total_pages', '?')

    if page_num == 1:
        return

    pw, ph = A4

    # Header
    hdr_y = ph - MARGIN + 4
    canvas_obj.saveState()
    canvas_obj.setFont('Helvetica-Bold', 9)
    canvas_obj.setFillColor(TEAL)
    canvas_obj.drawString(MARGIN, hdr_y, "Autism Therapy Platform — Journey Map")

    canvas_obj.setFont('Helvetica', 9)
    canvas_obj.setFillColor(BODY_GRAY)
    canvas_obj.drawRightString(pw - MARGIN, hdr_y, "Confidential — Internal Use")

    canvas_obj.setStrokeColor(TEAL)
    canvas_obj.setLineWidth(1)
    canvas_obj.line(MARGIN, hdr_y - 4, pw - MARGIN, hdr_y - 4)

    # Footer
    ftr_y = MARGIN - 14
    canvas_obj.setStrokeColor(BORDER_GRAY)
    canvas_obj.setLineWidth(0.5)
    canvas_obj.line(MARGIN, ftr_y + 10, pw - MARGIN, ftr_y + 10)

    canvas_obj.setFont('Helvetica', 8)
    canvas_obj.setFillColor(BODY_GRAY)
    canvas_obj.drawCentredString(pw / 2, ftr_y, f"{page_num}")
    canvas_obj.restoreState()


# ── Table Builders ────────────────────────────────────────────────────────────

def make_table_style(n_rows, n_cols, high_risk_rows=None):
    """Standard alternating-row table style."""
    style = [
        # Header row
        ('BACKGROUND', (0, 0), (-1, 0), TEAL),
        ('TEXTCOLOR',  (0, 0), (-1, 0), WHITE),
        ('FONTNAME',   (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE',   (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING',    (0, 0), (-1, 0), 8),
        # Body rows
        ('FONTNAME',   (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE',   (0, 1), (-1, -1), 9.5),
        ('VALIGN',     (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
        ('RIGHTPADDING', (0, 0), (-1, -1), 7),
        # Borders
        ('GRID',       (0, 0), (-1, -1), 0.5, BORDER_GRAY),
        ('BOX',        (0, 0), (-1, -1), 0.5, BORDER_GRAY),
    ]
    # Alternating row backgrounds
    for i in range(1, n_rows):
        bg = WHITE if i % 2 == 1 else LIGHT_MINT
        style.append(('BACKGROUND', (0, i), (-1, i), bg))

    # High-risk row overrides
    if high_risk_rows:
        for row_idx in high_risk_rows:
            # Make risk cell red-bold
            style.append(('TEXTCOLOR', (1, row_idx), (1, row_idx), ALERT_RED))
            style.append(('FONTNAME',  (1, row_idx), (1, row_idx), 'Helvetica-Bold'))

    return TableStyle(style)


def build_glance_table(styles):
    headers = [
        Paragraph('Stage', styles['table_header']),
        Paragraph('Primary Persona', styles['table_header']),
        Paragraph('Core Tool Today', styles['table_header']),
        Paragraph('Biggest Break', styles['table_header']),
    ]
    rows_data = [
        ['1. Family inquiry',        'Rahul (Director)',            'WhatsApp / memory',  'No inquiry tracking; leads lost'],
        ['2. Intake & enrollment',   'Rahul, Dr. Sunita',          'Paper forms',         'No consent mechanism; DPDPA exposure \u26a0\ufe0f'],
        ['3. Assessment & program',  'Dr. Sunita (Supervisor)',     'Paper / Word',        'Verbal handover to therapist; program misapplied'],
        ['4. In-session data coll.', 'Priya (Special Educator)',   'Paper data sheet',    'One-handed constraint; 1\u20132 week feedback lag'],
        ['5. Supervisor review',     'Dr. Sunita',                 'Paper / Excel',       'Batch review; outdated targets run for weeks'],
        ['6. Progress reporting',    'Dr. Sunita',                 'Word / WhatsApp',     'Written from scratch; reports parents can\u2019t read \u26a0\ufe0f'],
        ['7. Billing & fee coll.',   'Rahul',                      'WhatsApp / paper',    'Manual, relationship-sensitive; fees delayed'],
        ['8. Dropout & follow-up',   'Rahul',                      'WhatsApp message',    'No tracking; dropout invisible until it\u2019s done'],
    ]

    col_w = [INNER_W * 0.20, INNER_W * 0.22, INNER_W * 0.20, INNER_W * 0.38]

    data = [headers]
    for row in rows_data:
        data.append([Paragraph(cell, styles['table_cell']) for cell in row])

    tbl = Table(data, colWidths=col_w, repeatRows=1)
    tbl.setStyle(make_table_style(len(data), 4))
    return tbl


def build_breakpoints_table(styles):
    headers = [
        Paragraph('#', styles['table_header']),
        Paragraph('Break Point', styles['table_header']),
        Paragraph('Stage', styles['table_header']),
        Paragraph('Personas Hit', styles['table_header']),
        Paragraph('Evidence', styles['table_header']),
    ]
    rows_data = [
        ['BP-01', 'Paper in-session data collection \u2014 delayed, inaccurate, one-handed', 'Stage 4', 'Priya, Dr. Sunita',    '\U0001f535 \u2705'],
        ['BP-02', 'Supervisor review happens in batch, 1\u20132 weeks behind',               'Stage 5', 'Dr. Sunita, Priya',    '\u2705'],
        ['BP-03', 'Progress reports written from scratch; parent can\u2019t understand them',  'Stage 6', 'Dr. Sunita, Meena',   '\U0001f535 \U0001f536'],
        ['BP-04', 'No attendance tracking; dropout invisible until complete',                 'Stage 8', 'Rahul, Meena',        '\U0001f535 \u2705'],
        ['BP-05', 'No intake protocol; DPDPA non-compliance from day one',                   'Stage 2', 'All',                  '\u2705 \u26a0\ufe0f'],
    ]

    col_w = [INNER_W * 0.08, INNER_W * 0.42, INNER_W * 0.12, INNER_W * 0.22, INNER_W * 0.16]

    data = [headers]
    for row in rows_data:
        data.append([Paragraph(cell, styles['table_cell']) for cell in row])

    tbl = Table(data, colWidths=col_w, repeatRows=1)
    tbl.setStyle(make_table_style(len(data), 5))
    return tbl


def build_assumptions_table(styles):
    headers = [
        Paragraph('Hypothesis', styles['table_header']),
        Paragraph('Risk', styles['table_header']),
        Paragraph('Validate via', styles['table_header']),
    ]
    rows_data = [
        ['Priya records trial data on paper during live sessions (vs. skipping entirely)',
         'High',
         'Contextual observation'],
        ['Offline-first is a hard requirement in session rooms',
         'High',
         'On-site connectivity test'],
        ['Supervisor-to-therapist handover is verbal; program is misapplied',
         'High',
         'Observation + debrief interview'],
        ['Supervisors spend significant out-of-hours time on report writing',
         'High',
         'Time-diary / interview'],
        ['Centers are not DPDPA-compliant at intake',
         'High',
         'Director interview + consent form review'],
    ]

    col_w = [INNER_W * 0.50, INNER_W * 0.12, INNER_W * 0.38]

    data = [headers]
    for row in rows_data:
        data.append([Paragraph(cell, styles['table_cell']) for cell in row])

    # All risk rows are High (rows 1-5)
    high_risk_rows = list(range(1, len(rows_data) + 1))

    tbl = Table(data, colWidths=col_w, repeatRows=1)
    tbl.setStyle(make_table_style(len(data), 3, high_risk_rows=high_risk_rows))
    return tbl


# ── Section Divider ───────────────────────────────────────────────────────────

def section_divider():
    return [
        Spacer(1, 8),
        HRFlowable(width=INNER_W, thickness=0.5, color=BORDER_GRAY, spaceAfter=6),
        Spacer(1, 4),
    ]


# ── Cover Page Flowables ──────────────────────────────────────────────────────

class CoverBand(Flowable):
    """Draws the teal cover band spanning full page width."""
    def __init__(self, page_w, page_h):
        super().__init__()
        self.page_w = page_w
        self.page_h = page_h
        self.band_h = page_h * 0.28

    def wrap(self, avail_w, avail_h):
        return avail_w, self.band_h

    def draw(self):
        c = self.canv
        # Shift left to cover full page (beyond margin)
        c.setFillColor(TEAL)
        c.rect(-MARGIN, 0, self.page_w, self.band_h, fill=1, stroke=0)

        # Title
        c.setFont('Helvetica-Bold', 26)
        c.setFillColor(WHITE)
        c.drawCentredString(self.page_w / 2 - MARGIN, self.band_h / 2 + 10,
                            "End-to-End User Journey")

        # Subtitle
        c.setFont('Helvetica', 16)
        c.drawCentredString(self.page_w / 2 - MARGIN, self.band_h / 2 - 16,
                            "Autism Therapy Platform \u2014 Indian Therapy Center Lifecycle")


class BottomStrip(Flowable):
    """Draws the dark teal bottom strip across full page width."""
    def __init__(self, page_w, page_h):
        super().__init__()
        self.page_w = page_w
        self.page_h = page_h

    def wrap(self, avail_w, avail_h):
        return avail_w, 0  # zero height — draws absolutely

    def draw(self):
        c = self.canv
        c.setFillColor(DARK_TEAL)
        c.rect(-MARGIN, -MARGIN, self.page_w, 12, fill=1, stroke=0)


# ── Main Build Function ───────────────────────────────────────────────────────

def build_pdf():
    styles = make_styles()

    doc = SimpleDocTemplate(
        OUTPUT_PATH,
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN,
        bottomMargin=MARGIN,
    )

    story = []

    # ── COVER PAGE ────────────────────────────────────────────────────────────
    story.append(CoverBand(PAGE_W, PAGE_H))
    story.append(Spacer(1, 28))
    story.append(Paragraph("Prepared for: Product &amp; Design Leadership", styles['cover_meta']))
    story.append(Paragraph(
        "Date: 2026-04-14  \u2502  Stage: Discovery  \u2502  Evidence: Secondary Research",
        styles['cover_meta_small']
    ))
    story.append(Spacer(1, 18))
    story.append(LegendBox(INNER_W, "", styles))
    story.append(BottomStrip(PAGE_W, PAGE_H))
    story.append(PageBreak())

    # ── SECTION: The Journey at a Glance ──────────────────────────────────────
    story.append(Paragraph("The Journey at a Glance", styles['section_heading']))
    story.append(Paragraph(
        "A child's therapy journey at an Indian autism center spans 8 stages across 4 personas \u2014 "
        "from a family\u2019s first WhatsApp message to ongoing therapy, billing, and (too often) silent dropout. "
        "The entire journey runs on paper, WhatsApp, and memory. No structured digital tool exists at any stage.",
        styles['body']
    ))
    story.append(Spacer(1, 8))
    story.append(build_glance_table(styles))
    story.extend(section_divider())

    # ── SECTION: Stage-by-Stage Breakdown ────────────────────────────────────
    story.append(Paragraph("Stage-by-Stage Breakdown", styles['section_heading']))

    # Stage 1
    stage1 = [
        StageHeadingBand("Stage 1 \u2014 Family Inquiry & First Contact", INNER_W, styles),
        Spacer(1, 6),
        Paragraph(
            "A parent hears about the center through word of mouth or a paediatrician referral and sends a WhatsApp "
            "message. The inquiry is noted in the WhatsApp thread itself \u2014 or in a paper notebook \u2014 with no "
            "structured record. There is no pipeline visibility, no automated follow-up, and no reminder if the family "
            "goes quiet.",
            styles['body']
        ),
        Paragraph(
            "<i>Emotional state: Meena (parent) arrives anxious and exhausted from a long diagnostic journey. "
            "This is a high-stakes trust moment. \u2705 Tandfonline 2025</i>",
            styles['body_italic']
        ),
        Paragraph(
            "\u2013 <b>Key break:</b> Warm leads are lost because they live in a WhatsApp scroll history. \U0001f536",
            styles['bullet']
        ),
        Spacer(1, 10),
    ]
    story.append(KeepTogether(stage1))

    # Stage 2
    stage2 = [
        StageHeadingBand("Stage 2 \u2014 Intake & Enrollment", INNER_W, styles),
        Spacer(1, 6),
        Paragraph(
            "The family arrives for an intake appointment. A developmental history is taken verbally or on paper. "
            "Prior documents \u2014 diagnosis reports, school records, UDID card \u2014 are collected as photocopies. "
            "A fee structure is explained verbally. A consent form may or may not be signed.",
            styles['body']
        ),
        Paragraph(
            "<i>Emotional state: Meena is overwhelmed and needs to feel heard. "
            "Dr. Sunita is clinically focused but time-pressured. \u2705 / \U0001f536</i>",
            styles['body_italic']
        ),
        Paragraph(
            "\u2013 No standardised intake protocol \u2014 process varies by staff and day \u2705 PMC",
            styles['bullet']
        ),
        Paragraph(
            "\u2013 Digital storage of child health records without verifiable parental consent = "
            "<b>DPDPA 2023 non-compliance</b> \u26a0\ufe0f \u2705",
            styles['bullet']
        ),
        Paragraph(
            "\u2013 Fee agreement is verbal \u2014 ambiguity accumulates over months \U0001f536",
            styles['bullet']
        ),
        Spacer(1, 10),
    ]
    story.append(KeepTogether(stage2[:3]))
    story.extend(stage2[3:])

    # Stage 3
    stage3 = [
        StageHeadingBand("Stage 3 \u2014 Assessment & Program Design", INNER_W, styles),
        Spacer(1, 6),
        Paragraph(
            "Dr. Sunita conducts 1\u20133 assessment sessions (ISAA, CARS, Vineland). Results are compiled on paper "
            "into a baseline profile. An individualised therapy program is written \u2014 targets, prompt levels, "
            "reinforcement schedules. This program is communicated to Priya via a verbal briefing, possibly with a "
            "paper handout.",
            styles['body']
        ),
        Paragraph(
            "\u2013 Verbal handover = Priya may run sessions with misremembered prompt levels or wrong targets \U0001f536",
            styles['bullet']
        ),
        Paragraph(
            "\u2013 Parents leave without a written summary of what is being worked on or why \U0001f536",
            styles['bullet']
        ),
        Paragraph(
            "\u2013 RPWD Act 2016 mandates documented individualised programs \u2014 compliance is informal \u2705 / \U0001f536",
            styles['bullet']
        ),
        Spacer(1, 10),
    ]
    story.append(KeepTogether(stage3[:2]))
    story.extend(stage3[2:])

    # Stage 4
    stage4 = [
        StageHeadingBand("Stage 4 \u2014 Ongoing Therapy Sessions (In-Session Data Collection)", INNER_W, styles),
        Spacer(1, 6),
        Paragraph(
            "This is the highest-frequency workflow in the product. Priya runs discrete trials (DTT) or naturalistic "
            "teaching (NET) with the child, marking outcomes on a paper data sheet \u2014 correct, incorrect, or "
            "prompted \u2014 while managing the child with her other hand.",
            styles['body']
        ),
        Paragraph(
            "\u2013 <b>One-handed constraint</b> makes paper recording physically awkward; entries are missed or "
            "illegible \U0001f535",
            styles['bullet']
        ),
        Paragraph(
            "\u2013 ABC data (antecedent-behaviour-consequence) is often written retrospectively from memory \u2014 "
            "inaccurate by design \U0001f535",
            styles['bullet']
        ),
        Paragraph(
            "\u2013 Paper data sheets sit in a physical file until Dr. Sunita reviews them \u2014 sometimes "
            "<b>1\u20132 weeks later</b> \u2705 BHCOE",
            styles['bullet']
        ),
        Paragraph(
            "\u2013 Some therapists photograph paper sheets and send via WhatsApp \u2014 unencrypted transmission "
            "of child health data \u26a0\ufe0f DPDPA \U0001f536",
            styles['bullet']
        ),
        Paragraph(
            "<b>This is the foundational break point.</b> Everything downstream \u2014 program updates, reports, "
            "billing \u2014 depends on session data that is currently inaccurate, delayed, and inaccessible.",
            styles['body']
        ),
        Spacer(1, 10),
    ]
    story.append(KeepTogether(stage4[:2]))
    story.extend(stage4[2:])

    # Stage 5
    stage5 = [
        StageHeadingBand("Stage 5 \u2014 Supervisor Review & Program Updates", INNER_W, styles),
        Spacer(1, 6),
        Paragraph(
            "Dr. Sunita collects paper data sheets and manually calculates percentage-correct per target. She "
            "identifies mastery or plateau patterns and updates the therapy program. Changes are communicated to "
            "Priya verbally.",
            styles['body']
        ),
        Paragraph(
            "\u2013 Manual calculation is time-consuming and error-prone \U0001f535",
            styles['bullet']
        ),
        Paragraph(
            "\u2013 Global benchmark: <b>2\u20133 hours/day</b> on documentation without software tools \u2705 "
            "ABA Matrix \u2014 Indian equivalent unvalidated \U0001f536",
            styles['bullet']
        ),
        Paragraph(
            "\u2013 Program update communicated verbally \u2192 Priya may continue running old targets \U0001f536",
            styles['bullet']
        ),
        Paragraph(
            "\u2013 No version history: \u201cWhat was the prompt level 4 weeks ago?\u201d is unanswerable \U0001f535",
            styles['bullet']
        ),
        Spacer(1, 10),
    ]
    story.append(KeepTogether(stage5[:2]))
    story.extend(stage5[2:])

    # Stage 6
    stage6 = [
        StageHeadingBand("Stage 6 \u2014 Progress Reporting to Parents", INNER_W, styles),
        Spacer(1, 6),
        Paragraph(
            "Monthly or quarterly, Dr. Sunita compiles session data and writes a progress narrative per domain. "
            "Reports are handed over in person or sent as a PDF via WhatsApp. A verbal meeting may accompany "
            "the report. Home program instructions are given verbally.",
            styles['body']
        ),
        Paragraph(
            "\u2013 <b>Reports are written from scratch every cycle</b> \u2014 no carry-forward from prior reports "
            "or auto-population from session data \U0001f535",
            styles['bullet']
        ),
        Paragraph(
            "\u2013 Report language is clinical; Meena frequently doesn\u2019t understand what she\u2019s reading "
            "\u2705 Product context",
            styles['bullet']
        ),
        Paragraph(
            "\u2013 WhatsApp delivery of progress reports = unencrypted sensitive health data \u26a0\ufe0f DPDPA \U0001f535",
            styles['bullet']
        ),
        Paragraph(
            "\u2013 Home program guidance is verbal \u2014 Meena is unlikely to remember what to practise \U0001f536",
            styles['bullet']
        ),
        Spacer(1, 10),
    ]
    story.append(KeepTogether(stage6[:2]))
    story.extend(stage6[2:])

    # Stage 7
    stage7 = [
        StageHeadingBand("Stage 7 \u2014 Billing & Fee Collection", INNER_W, styles),
        Spacer(1, 6),
        Paragraph(
            "Rahul tallies sessions from a paper attendance register, calculates fees, and sends a WhatsApp message "
            "to the family. Payment is made in cash or via UPI. Outstanding balances are tracked in Excel or not at all.",
            styles['body']
        ),
        Paragraph(
            "\u2013 Asking financially stressed families for money is emotionally uncomfortable \u2014 Rahul delays "
            "these conversations \U0001f536",
            styles['bullet']
        ),
        Paragraph(
            "\u2013 No automated reminder \u2014 Rahul must manually track who has paid \U0001f535",
            styles['bullet']
        ),
        Paragraph(
            "\u2013 No financial dashboard: monthly revenue, collection rate, outstanding fees are invisible at a "
            "glance \U0001f535",
            styles['bullet']
        ),
        Paragraph(
            "\u2013 Evidence: <b>no-show rates drop from 39% \u2192 3%</b> with structured reminders \u2705 "
            "Psychiatric Services \u2014 the same principle applies to payment follow-up \U0001f535",
            styles['bullet']
        ),
        Spacer(1, 10),
    ]
    story.append(KeepTogether(stage7[:2]))
    story.extend(stage7[2:])

    # Stage 8
    stage8 = [
        StageHeadingBand("Stage 8 \u2014 Appointment Follow-Up & Dropout Prevention", INNER_W, styles),
        Spacer(1, 6),
        Paragraph(
            "A family misses a session. Staff notice through memory or a gap in the paper schedule. A single "
            "WhatsApp message is sent. If the family goes quiet, dropout is effectively accepted \u2014 experienced "
            "as an outcome, not a process failure.",
            styles['body']
        ),
        Paragraph(
            "\u2013 No attendance tracking system \u2014 dropout is <b>invisible until it has already happened</b> \U0001f535",
            styles['bullet']
        ),
        Paragraph(
            "\u2013 \u201cInvisible exits\u201d: families withdraw silently under financial strain and caregiver "
            "exhaustion \u2705 Tandfonline 2025",
            styles['bullet']
        ),
        Paragraph(
            "\u2013 One WhatsApp message is the entire dropout intervention \u2014 evidence shows live contact is "
            "13\u00d7 more effective \u2705",
            styles['bullet']
        ),
        Paragraph(
            "\u2013 No re-engagement protocol: if a family returns after a gap, no structured way to update the "
            "program exists \U0001f536",
            styles['bullet']
        ),
        Spacer(1, 10),
    ]
    story.append(KeepTogether(stage8[:2]))
    story.extend(stage8[2:])

    story.extend(section_divider())

    # ── SECTION: 5 Highest-Impact Break Points ───────────────────────────────
    story.append(Paragraph("The 5 Highest-Impact Break Points", styles['section_heading']))
    story.append(build_breakpoints_table(styles))
    story.extend(section_divider())

    # ── SECTION: What This Means ──────────────────────────────────────────────
    story.append(Paragraph("What This Means \u2014 Decisions Required", styles['section_heading']))

    decisions = [
        ("<b>In-session data collection is the foundation.</b> Every other break point is downstream of inaccurate, "
         "delayed session data. Solve this first or there is nothing reliable to build reporting, billing, or dropout "
         "prevention on."),
        ("<b>DPDPA compliance is not a later feature.</b> It appears at Stages 2, 4, and 6. The first time the "
         "product stores a child\u2019s clinical data digitally, verifiable parental consent is a legal requirement "
         "\u2014 not a roadmap item."),
        ("<b>WhatsApp is in the journey whether we design for it or not.</b> It is the inquiry channel, the billing "
         "channel, the progress report delivery channel, and the dropout follow-up channel. The product must map to "
         "these touchpoints, not replace them."),
        ("<b>Dropout prevention has the strongest evidence ROI.</b> The 39% \u2192 3% no-show rate finding is the "
         "sharpest data point across all research. Structured attendance tracking with reminder triggers is a "
         "high-impact, low-complexity Phase 2 candidate."),
        ("<b>Validate before designing.</b> Approximately 45% of this journey map is hypothesis, not observed fact. "
         "Primary fieldwork at 3\u20135 centers is the gate before any design work begins."),
    ]
    for i, text in enumerate(decisions, 1):
        # Number in teal, then text
        full_text = f'<font color="#175F63"><b>{i}.</b></font>  {text}'
        story.append(Paragraph(full_text, styles['numbered_item']))

    story.extend(section_divider())

    # ── SECTION: Open Assumptions ─────────────────────────────────────────────
    story.append(Paragraph("Open Assumptions (Top 5 by Risk)", styles['section_heading']))
    story.append(build_assumptions_table(styles))
    story.append(Spacer(1, 20))

    # ── Build ─────────────────────────────────────────────────────────────────
    doc.build(story, onFirstPage=build_header_footer, onLaterPages=build_header_footer)
    print(f"PDF written to: {OUTPUT_PATH}")


if __name__ == '__main__':
    build_pdf()
