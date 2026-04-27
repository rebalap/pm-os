"""
cb_brand.py — Cognitivebotics brand constants.

Imported by cb_docx, cb_pdf, and cb_pptx so brand values are defined in
exactly one place.  Never edit colors or typography in the individual tool
files — change them here and every output format picks up the update.
"""

# ── Colors (hex strings, no #) ────────────────────────────────────────────────
TEAL      = "175F63"   # primary brand color
CYAN      = "20A6AD"   # accent / bullets / callout borders
DARK_TEAL = "10494C"   # H2, dark accents
BLACK     = "101319"   # body text
GRAY      = "646871"   # captions, probes, footer text
MINT      = "EEF9F9"   # table alt rows, callout backgrounds
WHITE     = "FFFFFF"
BORDER    = "CBCBCB"   # thin borders
RED       = "CD423A"   # error / risk / alert

# ── Colors as (R, G, B) tuples for reportlab ─────────────────────────────────
def _t(h):
    return (int(h[0:2], 16) / 255, int(h[2:4], 16) / 255, int(h[4:6], 16) / 255)

TEAL_F      = _t(TEAL)
CYAN_F      = _t(CYAN)
DARK_TEAL_F = _t(DARK_TEAL)
BLACK_F     = _t(BLACK)
GRAY_F      = _t(GRAY)
MINT_F      = _t(MINT)
WHITE_F     = _t(WHITE)
BORDER_F    = _t(BORDER)
RED_F       = _t(RED)

# ── Typography ────────────────────────────────────────────────────────────────
FONT_HEADING  = "Nunito"
FONT_BODY     = "Open Sans"
FONT_FALLBACK = "Helvetica"   # always available in reportlab / PDF

# ── Font sizes (pt) ───────────────────────────────────────────────────────────
SZ_H1    = 22
SZ_H2    = 16
SZ_H3    = 13
SZ_BODY  = 11
SZ_SMALL =  9
SZ_COVER = 28   # cover page title
SZ_SUB   = 16   # cover subtitle

# ── Spacing (pt, used in docx twips = pt * 20) ───────────────────────────────
SP_H1_BEFORE = 0;  SP_H1_AFTER = 10
SP_H2_BEFORE = 16; SP_H2_AFTER = 4
SP_H3_BEFORE = 10; SP_H3_AFTER = 3
SP_BODY_AFTER = 4

# ── Slide dimensions (pptx, in EMU) ──────────────────────────────────────────
SLIDE_W = 9144000   # 10 inches
SLIDE_H = 5143500   # 7.5 inches (widescreen 16:9 ≈ 6858000; 4:3 ≈ 6858000)
# Use standard widescreen
SLIDE_W_WIDE = 9144000
SLIDE_H_WIDE = 5143500

# ── Gradient stops (for cover slides) ────────────────────────────────────────
GRADIENT_STOPS = [TEAL, CYAN]      # left → right
GRADIENT_DARK  = [DARK_TEAL, TEAL] # dark variant

# ── Document metadata defaults ────────────────────────────────────────────────
PRODUCT_NAME   = "Autism Therapy Platform"
COMPANY_NAME   = "Cognitivebotics"
CONFIDENTIALITY = "Confidential — Internal Use"
