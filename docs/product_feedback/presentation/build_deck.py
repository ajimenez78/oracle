"""Build the Oracle Product Feedback deck as a .pptx file."""

from pptx import Presentation
from pptx.enum.text import MSO_ANCHOR
from pptx.util import Inches

import slides_content as sc
from deck_kit import HERE, SLIDE_H, SLIDE_W

OUTPUT = HERE / "oracle_product_feedback.pptx"

SLIDES = [
    sc.title_slide,
    sc.starting_point,
    sc.target_user,
    sc.research,
    sc.user_voices,
    sc.learnings,
    sc.competitors,
    sc.proposal,
    sc.hypotheses,
    sc.mvp,
    sc.why_ai,
    sc.next_steps,
    sc.closing,
]


def main():
    prs = Presentation()
    prs.slide_width = Inches(SLIDE_W)
    prs.slide_height = Inches(SLIDE_H)
    for number, build in enumerate(SLIDES, start=1):
        build(prs, number)
    prs.save(OUTPUT)
    print(f"Saved {OUTPUT} with {len(SLIDES)} slides")


if __name__ == "__main__":
    main()
