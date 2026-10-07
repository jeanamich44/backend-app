"""Assemble chrome, header, middle, footer Engie Gaz."""

from app.services.generate_docs.common.canvas import new_pdf
from app.services.generate_docs.common.fonts import register, set_pdf_metrics

from . import chrome, footer, header, layout, middle, rules, static
from .data import Doc


def _fonts():
    register(layout.FONT, layout.FONT_FILE)
    register(layout.FONT_BOLD, layout.FONT_BOLD_FILE)
    register(layout.FONT_ITALIC, layout.FONT_ITALIC_FILE)
    register(layout.FONT_OCRB, layout.FONT_OCRB_FILE)
    register(layout.FONT_VERDANA_BOLD, layout.FONT_VERDANA_BOLD_FILE)
    set_pdf_metrics(
        layout.FONT, layout.FONT_ASCENT, layout.FONT_DESCENT,
        layout.FONT_BBOX, layout.FONT_CAP,
    )
    set_pdf_metrics(
        layout.FONT_BOLD, layout.FONT_BOLD_ASCENT, layout.FONT_BOLD_DESCENT,
        layout.FONT_BOLD_BBOX, layout.FONT_CAP,
    )
    set_pdf_metrics(
        layout.FONT_ITALIC, layout.FONT_ITALIC_ASCENT, layout.FONT_ITALIC_DESCENT,
        layout.FONT_ITALIC_BBOX, layout.FONT_CAP,
    )
    set_pdf_metrics(
        layout.FONT_OCRB, layout.OCRB_ASCENT, layout.OCRB_DESCENT,
        layout.OCRB_BBOX, layout.OCRB_CAP,
    )
    set_pdf_metrics(
        layout.FONT_VERDANA_BOLD, layout.VERDANA_ASCENT, layout.VERDANA_DESCENT,
        layout.VERDANA_BOLD_BBOX, layout.VERDANA_CAP,
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
