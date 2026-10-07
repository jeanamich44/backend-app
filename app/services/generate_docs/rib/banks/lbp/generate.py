"""Assemble header, middle, footer."""

from app.services.generate_docs.common.canvas import new_pdf
from app.services.generate_docs.common.fonts import register, set_pdf_metrics

from . import footer, header, layout, middle, rules
from .data import Doc


def _fonts():
    register("ArialMT", "ArialMT.ttf")
    register("Arial-BoldMT", "Arial-BoldMT.ttf")
    register("StoneSansITCTTMedium", "StoneSansITCTTMedium.ttf")
    set_pdf_metrics("StoneSansITCTTMedium", 962, -251, [-60, -251, 1217, 962], 700)
    set_pdf_metrics("ArialMT", 1040, -325, [-665, -325, 2000, 1040], 716)
    set_pdf_metrics("Arial-BoldMT", 1056, -376, [-628, -376, 2000, 1056], 716)


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
