#!/usr/bin/env python3
"""
Generate branded executive summary PDF for Autism Therapy Platform — Discovery Research.
Brand: Cognitivebotics color palette.
Strategy: SimpleDocTemplate with onFirstPage/onLaterPages callbacks.
Cover content drawn on canvas in onFirstPage; body starts on page 2.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
import os

# ── Brand Colors ──────────────────────────────────────────────────────────────
TEAL        = colors.HexColor('#175F63')
CYAN        = colors.HexColor('#20A6AD')
DARK_TEAL   = colors.HexColor('#10494C')
HEADING_TXT = colors.HexColor('#101319')
BODY_TXT    = colors.HexColor('#646871')
BG_WHITE    = colors.HexColor('#FFFFFF')
BG_LIGHT    = colors.HexColor('#EEF9F9')
ALERT_RED   = colors.HexColor('#cd423a')
BORDER      = colors.HexColor('#CBCBCB')
ORANGE      = colors.HexColor('#E07B39')
GREEN       = colors.HexColor('#5A8A5A')

PAGE_W, PAGE_H = A4   # 595.27 x 841.89 pts
OUTPUT_PATH = (
    '/Users/prahladrebala/Documents/pm-os/products/autism-therapy-platform/'
    'exec-summary-center-director.pdf'
)
L_MARGIN = 54
R_MARGIN = 54
T_MARGIN = 56
B_MARGIN = 50


# ── Page drawing callbacks ────────────────────────────────────────────────────

def first_page_cb(canvas, doc):
    """Cover page: drawn entirely on canvas. No Platypus content on this page."""
    c = canvas
    c.saveState()

    band_h = PAGE_H * 0.32

    # Top teal band
    c.setFillColor(TEAL)
    c.rect(0, PAGE_H - band_h, PAGE_W, band_h, fill=1, stroke=0)

    # Title
    c.setFont('Helvetica-Bold', 28)
    c.setFillColor(colors.white)
    c.drawCentredString(PAGE_W / 2, PAGE_H - band_h / 2 + 22, 'Executive Summary')

    # Subtitle
    c.setFont('Helvetica', 16)
    c.drawCentredString(
        PAGE_W / 2, PAGE_H - band_h / 2 - 14,
        'Autism Therapy Platform \u2014 Discovery Research'
    )

    # Meta block below band
    meta_y = PAGE_H - band_h - 55
    c.setFont('Helvetica', 12)
    c.setFillColor(BODY_TXT)
    c.drawCentredString(PAGE_W / 2, meta_y, 'Prepared for: Center Director')
    c.drawCentredString(PAGE_W / 2, meta_y - 22, 'Date: 2026-04-14')

    # Accent rule
    c.setStrokeColor(CYAN)
    c.setLineWidth(2)
    c.line(PAGE_W / 2 - 90, meta_y - 38, PAGE_W / 2 + 90, meta_y - 38)

    # Description text block
    desc_y = meta_y - 80
    c.setFont('Helvetica', 11)
    c.setFillColor(BODY_TXT)
    desc_lines = [
        'This document summarizes secondary desk research conducted across three workstreams:',
        'in-session data collection, patient enrollment & intake, and treatment plans,',
        'billing & follow-up. Findings are secondary evidence only.',
        'Primary fieldwork is required before any product decisions are made.',
    ]
    for i, line in enumerate(desc_lines):
        c.drawCentredString(PAGE_W / 2, desc_y - i * 17, line)

    # Divider + scope block
    scope_y = desc_y - 100
    c.setStrokeColor(BG_LIGHT)
    c.setLineWidth(0.5)
    c.line(L_MARGIN, scope_y + 20, PAGE_W - R_MARGIN, scope_y + 20)

    c.setFont('Helvetica-Bold', 10)
    c.setFillColor(TEAL)
    c.drawCentredString(PAGE_W / 2, scope_y + 2, 'Contents')

    c.setFont('Helvetica', 10)
    c.setFillColor(BODY_TXT)
    toc_items = [
        '1. What We Know',
        '2. What This Means \u2014 Decisions Required',
        '3. Open Risks and Assumptions',
        '4. Recommended Next Steps',
    ]
    for i, item in enumerate(toc_items):
        c.drawCentredString(PAGE_W / 2, scope_y - 16 - i * 18, item)

    # Bottom strip
    c.setFillColor(DARK_TEAL)
    c.rect(0, 0, PAGE_W, 18, fill=1, stroke=0)

    c.restoreState()


def inner_page_cb(canvas, doc):
    """Header + footer for inner pages."""
    c = canvas
    c.saveState()

    # Header
    hy = PAGE_H - 36
    c.setFont('Helvetica-Bold', 9)
    c.setFillColor(TEAL)
    c.drawString(L_MARGIN, hy, 'Autism Therapy Platform')

    c.setFont('Helvetica', 9)
    c.setFillColor(BODY_TXT)
    c.drawRightString(PAGE_W - R_MARGIN, hy, 'Confidential \u2014 Internal Use')

    c.setStrokeColor(TEAL)
    c.setLineWidth(1)
    c.line(L_MARGIN, hy - 8, PAGE_W - R_MARGIN, hy - 8)

    # Footer
    fy = 30
    c.setStrokeColor(BORDER)
    c.setLineWidth(0.5)
    c.line(L_MARGIN, fy + 12, PAGE_W - R_MARGIN, fy + 12)

    c.setFont('Helvetica', 8)
    c.setFillColor(BODY_TXT)
    # page 1 is cover, body pages start at 2 → show as page N-1
    c.drawCentredString(PAGE_W / 2, fy, str(doc.page - 1))

    c.restoreState()


# ── Styles ────────────────────────────────────────────────────────────────────

def build_styles():
    s = {}

    s['section_header'] = ParagraphStyle(
        'SectionHeader',
        fontName='Helvetica-Bold',
        fontSize=14,
        textColor=TEAL,
        leading=20,
        spaceAfter=6,
        spaceBefore=16,
        backColor=BG_LIGHT,
        borderPadding=(7, 10, 7, 10),
    )
    s['topic_label'] = ParagraphStyle(
        'TopicLabel',
        fontName='Helvetica-Bold',
        fontSize=11,
        textColor=DARK_TEAL,
        leading=15,
        spaceBefore=10,
        spaceAfter=4,
    )
    s['bullet'] = ParagraphStyle(
        'Bullet',
        fontName='Helvetica',
        fontSize=10.5,
        textColor=HEADING_TXT,
        leading=15,
        spaceAfter=5,
        spaceBefore=1,
        leftIndent=18,
    )
    s['intro'] = ParagraphStyle(
        'Intro',
        fontName='Helvetica',
        fontSize=10.5,
        textColor=BODY_TXT,
        leading=15,
        spaceAfter=8,
        spaceBefore=4,
    )
    s['closing'] = ParagraphStyle(
        'Closing',
        fontName='Helvetica',
        fontSize=10,
        textColor=BODY_TXT,
        leading=14,
        spaceBefore=10,
        backColor=BG_LIGHT,
        borderPadding=(8, 10, 8, 10),
    )
    return s


# ── Helpers ───────────────────────────────────────────────────────────────────

def sh(text, st):
    return Paragraph(text, st['section_header'])


def blt(text, st):
    return Paragraph(f'<font color="#20A6AD">\u2013</font>\u00a0\u00a0{text}', st['bullet'])


def cp(text, bold=False, color=None, align=TA_LEFT, size=10):
    """Cell paragraph."""
    st = ParagraphStyle(
        'cp',
        fontName='Helvetica-Bold' if bold else 'Helvetica',
        fontSize=size,
        textColor=color or HEADING_TXT,
        leading=14,
        alignment=align,
        wordWrap='CJK',
    )
    return Paragraph(text, st)


def lp(text):
    """Level cell with color."""
    if 'High' in text:
        color = ALERT_RED
    elif 'Medium' in text or 'Med' in text:
        color = ORANGE
    else:
        color = GREEN
    st = ParagraphStyle(
        'lp', fontName='Helvetica-Bold', fontSize=10,
        textColor=color, leading=14, alignment=TA_CENTER,
    )
    return Paragraph(text, st)


def table_style(num_rows):
    ts = TableStyle([
        ('BACKGROUND',    (0, 0), (-1, 0), TEAL),
        ('TEXTCOLOR',     (0, 0), (-1, 0), colors.white),
        ('FONTNAME',      (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE',      (0, 0), (-1, 0), 10),
        ('ALIGN',         (0, 0), (-1, 0), 'CENTER'),
        ('VALIGN',        (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING',    (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('LEFTPADDING',   (0, 0), (-1, -1), 8),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 8),
        ('GRID',          (0, 0), (-1, -1), 0.5, BORDER),
        ('LINEBELOW',     (0, 0), (-1, 0), 1.5, TEAL),
    ])
    for i in range(1, num_rows):
        bg = BG_LIGHT if i % 2 == 0 else BG_WHITE
        ts.add('BACKGROUND', (0, i), (-1, i), bg)
    return ts


# ── Content ───────────────────────────────────────────────────────────────────

def body(styles, usable_w):
    story = []

    story.append(Spacer(1, 8))
    story.append(Paragraph(
        'This executive summary synthesizes secondary desk research across three workstreams '
        'for the Autism Therapy Platform (India) Discovery phase: '
        '<b>in-session data collection</b>, <b>patient enrollment and intake</b>, and '
        '<b>treatment plans, billing, and follow-up</b>. '
        'Research was conducted in April 2026 via web search and published sources. '
        'All findings are secondary evidence only. Primary fieldwork with center directors '
        'and therapists is required before any product decisions are made.',
        styles['intro']
    ))
    story.append(Spacer(1, 4))

    # ── SECTION 1 ─────────────────────────────────────────────────────────────
    story.append(sh('1. What We Know', styles))

    topics = [
        ('In-session data collection', [
            'Real-time, in-session data recording is a clinical requirement in ABA \u2014 not optional. '
            'Retrospective recording degrades accuracy and is explicitly flagged as clinically '
            'inferior in peer-reviewed literature.',
            'Paper-based data collection has documented failure modes: miscounts, illegible notes, '
            'transcription errors, and delayed supervisor feedback. A peer-reviewed DTT study found '
            'measurable accuracy differences between paper and digital recording.',
            'Digital data collection is used in over half of ABA practices globally. All major '
            'platforms (Noteable, Raven Health, Ensora ABA) are built for one-handed, offline-first '
            'use \u2014 the established design baseline.',
            'No therapist-side clinical data collection tool has penetrated the Indian market. '
            'TherapEZ offers general practice management. Cognitivebotics tracks child performance '
            'within its own platform. Neither addresses therapist recording against individualized '
            'therapy program targets during live sessions \u2014 structurally different tasks.',
        ]),
        ('Patient enrollment and intake', [
            'There is no standardized intake protocol for autism therapy in India. '
            'The process is fragmented, medically-mediated, and entirely paper-based.',
            'Families arrive at intake after a long diagnostic journey \u2014 often years of waiting. '
            'Intake is a high-stakes trust moment; disorganized intake is a documented driver '
            'of early dropout (described in research as "invisible exits").',
            "India's DPDPA 2023 creates real compliance risk: digital health data of minors "
            'requires verifiable parental consent. Most centers are currently non-compliant '
            'because data lives in informal tools and paper with no formal consent process.',
            'UDID documentation support is an underserved recurring need \u2014 centers regularly '
            'assist families with government disability ID applications, managed ad hoc today.',
            'No purpose-built intake tool for Indian autism therapy centers exists. US tools '
            '(SimplePractice, Jane App) assume HIPAA, insurance, and BCBA structures '
            'that do not apply in India.',
        ]),
        ('Treatment plans, billing, and follow-up', [
            'Documentation burden is real and quantified globally: providers spend 2\u20133 hours '
            'per day on documentation in unautomated practices, reducible to 30\u201360 minutes '
            'with software. Whether this scale exists in Indian centers is unvalidated.',
            'Indian billing is informal and relationship-driven: fees collected via WhatsApp, '
            'handwritten receipts, and Excel. No insurance billing equivalent exists. '
            'Billing is a social act with emotionally stressed families \u2014 '
            'not a neutral administrative process.',
            'Appointment no-show rates vary dramatically by reminder method: 39% with no '
            'reminder, 24% with automated voicemail, 3% with live contact. Structured reminders '
            'are a high-ROI, evidence-based intervention with direct revenue impact.',
            'Dropout in Indian centers is driven by financial pressure, caregiver exhaustion, '
            'and communication breakdown. Most centers do not track dropout because no '
            'attendance system surfaces patterns early.',
            'WhatsApp is infrastructure, not a gap. Any follow-up or communication feature '
            'must work with WhatsApp behavior, not compete against it.',
        ]),
    ]

    for topic, points in topics:
        story.append(Paragraph(topic, styles['topic_label']))
        for pt in points:
            story.append(blt(pt, styles))
        story.append(Spacer(1, 4))

    # ── SECTION 2 ─────────────────────────────────────────────────────────────
    story.append(Spacer(1, 6))
    story.append(sh('2. What This Means \u2014 Decisions Required', styles))

    decisions = [
        '<b>Which workstream is the primary entry point?</b> In-session data collection has the '
        'strongest clinical forcing function. Intake has the highest compliance urgency. '
        'Billing/follow-up has the most direct revenue impact. This decision must be made before '
        'primary research begins \u2014 it determines who we recruit and what we observe.',
        '<b>Is offline-first a hard requirement or a Phase 2 feature?</b> Secondary research '
        'confirms it is the global baseline. India-specific connectivity data in therapy settings '
        'is unvalidated. The answer determines architecture choices before engineering begins.',
        '<b>What is the minimum viable data collection interaction?</b> One-handed, '
        '\u22642-tap entry is established globally. We need to know which specific data types '
        'Indian centers actually record before designing the interaction model.',
        '<b>How do we position against WhatsApp for parent communication?</b> Any feature '
        'competing directly with WhatsApp will fail. The product must complement or integrate '
        '\u2014 this strategy must be set before design begins.',
        '<b>What is the right pricing structure for Indian centers (5\u201320 staff)?</b> '
        'Willingness-to-pay at Indian price points is entirely unvalidated. This is the most '
        'critical commercial assumption in the business case.',
        '<b>How do we handle DPDPA 2023 compliance?</b> It cannot be retrofitted. '
        'Consent architecture must be designed in from day one \u2014 especially for intake '
        'and health data of minors.',
    ]

    for d in decisions:
        story.append(blt(d, styles))
    story.append(Spacer(1, 8))

    # ── SECTION 3 ─────────────────────────────────────────────────────────────
    story.append(sh('3. Open Risks and Assumptions', styles))
    story.append(Paragraph(
        'The following assumptions are driving current thinking. None have been validated '
        'through primary research. Each represents a decision point that fieldwork must answer.',
        styles['intro']
    ))
    story.append(Spacer(1, 6))

    risk_data = [
        [cp('Assumption / Risk', bold=True, color=colors.white),
         cp('Level', bold=True, color=colors.white, align=TA_CENTER),
         cp('Status', bold=True, color=colors.white)],
        [cp('Special educators find paper/WhatsApp data collection disruptive enough '
            'to adopt software \u2014 even with behavior change required.'),
         lp('High'), cp('Open \u2014 requires primary fieldwork')],
        [cp('Clinical supervisors spend significant uncompensated time on manual '
            'progress report and treatment plan writing.'),
         lp('High'), cp('Open \u2014 requires primary fieldwork')],
        [cp('Center directors would pay for a unified tool at Indian price points '
            'if it materially reduced their admin burden.'),
         lp('High'), cp('Open \u2014 requires director interviews and pricing research')],
        [cp('Offline-first is a hard requirement for the majority of Indian centers.'),
         lp('High'), cp('Open \u2014 no India connectivity data in therapy settings found')],
        [cp('Centers using Cognitivebotics still rely on paper or WhatsApp for '
            'in-session clinical data collection.'),
         lp('Medium'), cp('Open \u2014 requires center-level observation')],
        [cp('Most Indian autism therapy centers are not DPDPA 2023 compliant '
            'for digital health data of minors.'),
         lp('High'), cp('Open \u2014 compliance risk; needs legal review')],
        [cp('Intake dropout (families who make contact but do not enroll) '
            'is significant and unmeasured at most centers.'),
         lp('Medium'), cp('Open \u2014 requires director interviews')],
        [cp('Documentation in Indian centers takes 2+ hours/day '
            '(as documented globally in ABA practices).'),
         lp('Medium'), cp('Open \u2014 may be lower in less-structured Indian context')],
        [cp('WhatsApp cannot realistically be replaced for parent communication '
            '\u2014 the product must integrate or complement it.'),
         lp('High'), cp('Open \u2014 requires parent and director fieldwork')],
        [cp('English-only UI is acceptable for therapist-facing features '
            'in metro markets at launch.'),
         lp('Medium'), cp('Open \u2014 requires onboarding observation')],
    ]

    cw_r = [usable_w * 0.54, usable_w * 0.14, usable_w * 0.32]
    rt = Table(risk_data, colWidths=cw_r, repeatRows=1)
    rt.setStyle(table_style(len(risk_data)))
    story.append(rt)
    story.append(Spacer(1, 14))

    # ── SECTION 4 ─────────────────────────────────────────────────────────────
    story.append(sh('4. Recommended Next Steps', styles))
    story.append(Paragraph(
        'These actions are required before any product or design decisions can be made. '
        'Secondary research has established the landscape \u2014 primary fieldwork must '
        'validate whether the problems exist at actionable scale in Indian centers.',
        styles['intro']
    ))
    story.append(Spacer(1, 6))

    ns_data = [
        [cp('Action', bold=True, color=colors.white),
         cp('Owner', bold=True, color=colors.white),
         cp('Timeframe', bold=True, color=colors.white)],
        [cp('Decide primary workstream entry point (in-session data, intake, or '
            'billing/follow-up) before primary research begins.'),
         cp('Center Director + PM'), cp('Before research begins')],
        [cp('Recruit 5\u20138 center directors and senior therapists for 45-minute '
            'contextual inquiry sessions \u2014 observe actual workflows, not self-reports.'),
         cp('Researcher'), cp('Week 1\u20132')],
        [cp('Observe at least 3 live therapy sessions to understand in-session '
            'data recording behavior directly.'),
         cp('Researcher'), cp('Week 2\u20133')],
        [cp('Conduct intake observation at 2\u20133 centers to map actual steps, '
            'timing, and documentation at each stage.'),
         cp('Researcher'), cp('Week 2\u20133')],
        [cp('Interview center directors on billing workflow: how fees are communicated, '
            'collected, tracked, and what happens when families fall behind.'),
         cp('Researcher'), cp('Week 1\u20132')],
        [cp('Assess DPDPA 2023 compliance posture: engage legal counsel on consent '
            'architecture requirements for health data of minors.'),
         cp('PM + Legal'), cp('Parallel to fieldwork')],
        [cp('Test willingness-to-pay signal: present value proposition to 3\u20135 '
            'center directors and gauge pricing reaction directly.'),
         cp('PM'), cp('Week 3\u20134')],
        [cp('Synthesize fieldwork findings into a validated problem statement '
            'before moving to Define stage.'),
         cp('PM + Researcher'), cp('End of Week 4')],
    ]

    cw_n = [usable_w * 0.56, usable_w * 0.22, usable_w * 0.22]
    nt = Table(ns_data, colWidths=cw_n, repeatRows=1)
    nt.setStyle(table_style(len(ns_data)))
    story.append(nt)
    story.append(Spacer(1, 16))

    # Closing note
    story.append(Paragraph(
        '<b>Stage gate reminder:</b> This document is the output of secondary Discovery '
        'research only. No solutions, features, or product decisions should be proposed '
        'until primary fieldwork is complete and a validated problem statement is approved. '
        'Moving to Define or Design without completing primary research is a stage skip.',
        styles['closing']
    ))

    return story


# ── Build PDF ─────────────────────────────────────────────────────────────────

def build_pdf():
    doc = SimpleDocTemplate(
        OUTPUT_PATH,
        pagesize=A4,
        leftMargin=L_MARGIN,
        rightMargin=R_MARGIN,
        topMargin=T_MARGIN,
        bottomMargin=B_MARGIN,
        title='Executive Summary \u2014 Autism Therapy Platform Discovery Research',
        author='Cognitivebotics PM OS',
        subject='Discovery Research Executive Summary for Center Director',
    )

    styles = build_styles()
    usable_w = PAGE_W - L_MARGIN - R_MARGIN

    # The trick: on page 1, onFirstPage draws the full cover.
    # We use a PageBreak to move to page 2 for body content.
    # The first page template draws over whatever Platypus puts in frame,
    # so we just put a single empty paragraph as placeholder for page 1.

    story = []

    # Page 1 placeholder — canvas draws cover via onFirstPage callback
    # Use a spacer that won't overflow but fills the page
    story.append(Paragraph('', ParagraphStyle('blank', fontSize=1)))
    story.append(PageBreak())

    # Body content starts on page 2
    story += body(styles, usable_w)

    doc.build(
        story,
        onFirstPage=first_page_cb,
        onLaterPages=inner_page_cb,
    )

    size = os.path.getsize(OUTPUT_PATH)
    print(f'PDF written: {OUTPUT_PATH}')
    print(f'File size: {size:,} bytes ({size / 1024:.1f} KB)')
    return size


if __name__ == '__main__':
    build_pdf()
