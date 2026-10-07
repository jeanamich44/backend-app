"""Assemble chrome, header, middle, footer."""

from app.services.generate_docs.common.canvas import new_pdf
from app.services.generate_docs.common.fonts import register, set_pdf_metrics

from . import chrome, footer, header, layout, middle, rules, static
from .data import Doc


def _fonts():
    register(layout.FONT, layout.FONT_FILE)
    register(layout.FONT_BOLD, layout.FONT_BOLD_FILE)
    register(layout.FONT_H, layout.FONT_H_FILE)
    register(layout.FONT_HB, layout.FONT_HB_FILE)
    register(layout.FONT_FL, layout.FONT_FL_FILE)
    register(layout.FONT_FB, layout.FONT_FB_FILE)
    register(layout.FONT_P, layout.FONT_P_FILE)
    set_pdf_metrics(
        layout.FONT, layout.FONT_ASCENT, layout.FONT_DESCENT,
        layout.FONT_BBOX, layout.FONT_CAP,
    )
    set_pdf_metrics(
        layout.FONT_BOLD, layout.FONT_BOLD_ASCENT, layout.FONT_BOLD_DESCENT,
        layout.FONT_BOLD_BBOX, layout.FONT_CAP,
    )
    set_pdf_metrics(
        layout.FONT_H, layout.H_ASCENT, layout.H_DESCENT,
        layout.H_BBOX, layout.H_CAP,
    )
    set_pdf_metrics(
        layout.FONT_HB, layout.HB_ASCENT, layout.HB_DESCENT,
        layout.HB_BBOX, layout.HB_CAP,
    )
    set_pdf_metrics(
        layout.FONT_FL, layout.FL_ASCENT, layout.FL_DESCENT,
        layout.FL_BBOX, layout.FL_CAP,
    )
    set_pdf_metrics(
        layout.FONT_FB, layout.FB_ASCENT, layout.FB_DESCENT,
        layout.FB_BBOX, layout.FB_CAP,
    )
    set_pdf_metrics(
        layout.FONT_P, layout.P_ASCENT, layout.P_DESCENT,
        layout.P_BBOX, layout.P_CAP,
    )
    set_pdf_metrics(
        layout.FONT_C, layout.C_ASCENT, layout.C_DESCENT,
        layout.C_BBOX, layout.C_CAP,
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
