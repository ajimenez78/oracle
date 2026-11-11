"""Oracle slide style: colors, fonts and drawing helpers for python-pptx."""

from pathlib import Path

from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

HERE = Path(__file__).parent
LOGO_FULL = HERE / "logo_panel.jpg"
LOGO_ICON = HERE / "logo_icon.png"

NAVY = RGBColor(0x1B, 0x16, 0x33)
NAVY_SOFT = RGBColor(0x2A, 0x24, 0x4A)
CYAN = RGBColor(0x2E, 0xC9, 0xE8)
PURPLE = RGBColor(0x8B, 0x5C, 0xF6)
INK = RGBColor(0x1E, 0x1B, 0x33)
MUTED = RGBColor(0x5B, 0x5A, 0x70)
CARD = RGBColor(0xF3, 0xF2, 0xFA)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

TITLE_FONT = "Ubuntu"
BODY_FONT = "Noto Sans"

SLIDE_W = 13.333
SLIDE_H = 7.5
MARGIN = 0.6


def fill_background(slide, color):
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = color


def box(slide, x, y, w, h, color, shape=MSO_SHAPE.RECTANGLE):
    shp = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    shp.fill.solid()
    shp.fill.fore_color.rgb = color
    shp.line.fill.background()
    shp.shadow.inherit = False
    if shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        shp.adjustments[0] = 0.08
    return shp


def accent_bar(slide, x, y, w, h):
    shp = box(slide, x, y, w, h, CYAN)
    shp.fill.gradient()
    shp.fill.gradient_angle = 0
    stops = shp.fill.gradient_stops
    stops[0].color.rgb = CYAN
    stops[1].color.rgb = PURPLE
    return shp


def text(slide, x, y, w, h, content, size=16, color=INK, bold=False,
         font=BODY_FONT, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    """Add a text box. `content` is a string or a list of paragraphs.

    Each paragraph is a string or a list of (text, bold) runs.
    """
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = Inches(0.05)
    tf.margin_top = tf.margin_bottom = Inches(0.03)
    paragraphs = content if isinstance(content, list) else [content]
    for i, para in enumerate(paragraphs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.space_after = Pt(size * 0.45)
        runs = para if isinstance(para, list) else [(para, bold)]
        for run_text, run_bold in runs:
            run = p.add_run()
            run.text = run_text
            run.font.size = Pt(size)
            run.font.bold = run_bold
            run.font.color.rgb = color
            run.font.name = font
    return tb


def content_slide(prs, title, number):
    """Light slide with a dark title band, logo, accent line and footer."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    fill_background(slide, WHITE)
    box(slide, 0, 0, SLIDE_W, 1.15, NAVY)
    accent_bar(slide, 0, 1.15, SLIDE_W, 0.06)
    text(slide, MARGIN, 0.18, 10.8, 0.8, title, size=28, color=WHITE,
         bold=True, font=TITLE_FONT, anchor=MSO_ANCHOR.MIDDLE)
    slide.shapes.add_picture(str(LOGO_ICON), Inches(SLIDE_W - 1.3), Inches(0.17),
                             Inches(0.82), Inches(0.82))
    footer = "Oracle  ·  Aprendizajes de Product Feedback"
    text(slide, MARGIN, SLIDE_H - 0.45, 8, 0.3, footer, size=10, color=MUTED)
    text(slide, SLIDE_W - MARGIN - 1, SLIDE_H - 0.45, 1, 0.3, str(number),
         size=10, color=MUTED, align=PP_ALIGN.RIGHT)
    return slide


def card(slide, x, y, w, h, heading, body, accent=CYAN, heading_size=17,
         body_size=14):
    """Rounded card with a colored left edge, a heading and body paragraphs."""
    box(slide, x, y, w, h, CARD, MSO_SHAPE.ROUNDED_RECTANGLE)
    box(slide, x, y + 0.2, 0.07, h - 0.4, accent)
    text(slide, x + 0.25, y + 0.18, w - 0.45, 0.6, heading, size=heading_size,
         bold=True, font=TITLE_FONT)
    text(slide, x + 0.25, y + 0.18 + heading_size / 40, w - 0.45,
         h - 0.4 - heading_size / 40, body, size=body_size, color=MUTED)


def callout(slide, x, y, w, h, content, size=18):
    """Dark banner used for a key message."""
    box(slide, x, y, w, h, NAVY, MSO_SHAPE.ROUNDED_RECTANGLE)
    accent_bar(slide, x + 0.3, y + h - 0.12, 1.2, 0.05)
    text(slide, x + 0.3, y, w - 0.6, h, content, size=size, color=WHITE,
         anchor=MSO_ANCHOR.MIDDLE)


def number_badge(slide, x, y, label, color=CYAN, size=0.55):
    badge = box(slide, x, y, size, size, color, MSO_SHAPE.OVAL)
    tf = badge.text_frame
    tf.margin_left = tf.margin_right = 0
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    run.text = label
    run.font.size = Pt(15)
    run.font.bold = True
    run.font.name = TITLE_FONT
    run.font.color.rgb = WHITE
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    return badge
