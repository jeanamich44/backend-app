"""Assemble header, middle, footer."""

from app.services.generate_docs.common.canvas import new_pdf
from app.services.generate_docs.common.fonts import register, set_pdf_metrics

from . import footer, header, layout, middle, rules
from .data import Doc


def _fonts():
    register(layout.FONT, layout.FONT_FILE)
    register(layout.FONT_BOLD, layout.FONT_BOLD_FILE)
    set_pdf_metrics(layout.FONT, 775, -225, [-191, -309, 1153, 930], 667)
    set_pdf_metrics(layout.FONT_BOLD, 790, -210, [-172, -288, 1147, 903], 667)


def generate(doc=None, dest=None):
    doc = rules.apply_doc(doc or Doc())
    _fonts()
    pagesize = (layout.PAGE_W, layout.PAGE_H)
    c, out = new_pdf(pagesize=pagesize, dest=dest)
    header.draw(c, doc)
    middle.draw(c, doc)
    footer.draw(c, doc)
    c.showPage()
    c.save()
    return out


if __name__ == "__main__":
    print(generate())
