"""Assemble header, middle. Deux coupons."""

from app.services.generate_docs.common.canvas import new_pdf
from app.services.generate_docs.common.fonts import register, set_pdf_metrics

from . import header, layout, middle, rules
from .data import Doc


def _fonts():
    register(layout.FONT, layout.FONT_FILE)
    set_pdf_metrics(
        layout.FONT, layout.FONT_ASCENT, layout.FONT_DESCENT,
        layout.FONT_BBOX, layout.FONT_CAP,
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
