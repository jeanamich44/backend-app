"""Assemble header, middle, footer."""

from app.services.generate_docs.common.canvas import new_pdf
from app.services.generate_docs.common.fonts import register, set_pdf_metrics

from . import chrome, footer, header, layout, middle, rules, static
from .data import Doc


def _fonts():
    register(layout.FONT, layout.FONT_FILE)
    register(layout.FONT_BOLD, layout.FONT_BOLD_FILE)
    register(layout.FONT_DEJAVU, layout.FONT_DEJAVU_FILE)
    register(layout.FONT_TREBUCHET, layout.FONT_TREBUCHET_FILE)
    set_pdf_metrics(
        layout.FONT, layout.FONT_ASCENT, layout.FONT_DESCENT, layout.FONT_BBOX,
    )
    set_pdf_metrics(
        layout.FONT_BOLD, layout.FONT_BOLD_ASCENT, layout.FONT_BOLD_DESCENT,
        layout.FONT_BOLD_BBOX,
    )
    set_pdf_metrics(
        layout.FONT_DEJAVU, layout.FONT_DEJAVU_ASCENT, layout.FONT_DEJAVU_DESCENT,
        layout.FONT_DEJAVU_BBOX, layout.FONT_DEJAVU_CAP,
    )
    set_pdf_metrics(
        layout.FONT_TREBUCHET, layout.FONT_TREB_ASCENT, layout.FONT_TREB_DESCENT,
        layout.FONT_TREB_BBOX,
    )


def generate(doc=None, dest=None):
    doc = rules.apply_doc(doc or Doc())
    _fonts()
    pagesize = (layout.PAGE_W, layout.PAGE_H)
    c, out = new_pdf(pagesize=pagesize, dest=dest)
    chrome.draw(c, doc)
    header.draw(c, doc)
    middle.draw(c, doc)
    footer.draw(c, doc)
    static.draw(c, doc)
    c.showPage()
    c.save()
    return out


if __name__ == "__main__":
    print(generate())
