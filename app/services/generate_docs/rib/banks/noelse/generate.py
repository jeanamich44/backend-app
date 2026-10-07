"""Assemble header + middle, trois coupons."""

from app.services.generate_docs.common.canvas import new_pdf
from app.services.generate_docs.common.fonts import register, set_pdf_metrics

from . import header, layout, middle, rules
from .data import Doc


def _fonts():
    register(layout.FONT, layout.FONT_FILE)
    register(layout.FONT_NARROW, layout.FONT_NARROW_FILE)
    register(layout.FONT_BOLD, layout.FONT_BOLD_FILE)
    register(layout.FONT_ITALIC, layout.FONT_ITALIC_FILE)
    for name in (layout.FONT, layout.FONT_NARROW, layout.FONT_BOLD):
        set_pdf_metrics(
            name, layout.FONT_ASCENT, layout.FONT_DESCENT,
            layout.FONT_BBOX, layout.FONT_CAP,
        )
    set_pdf_metrics(
        layout.FONT_ITALIC, layout.FONT_ITALIC_ASCENT, layout.FONT_ITALIC_DESCENT,
        layout.FONT_ITALIC_BBOX, layout.FONT_ITALIC_CAP,
    )


def generate(doc=None, dest=None):
    doc = rules.apply_doc(doc or Doc())
    _fonts()
    pagesize = (layout.PAGE_W, layout.PAGE_H)
    c, out = new_pdf(pagesize=pagesize, dest=dest)
    header.draw(c, doc)
    middle.draw(c, doc)
    c.showPage()
    c.save()
    return out


if __name__ == "__main__":
    print(generate())
