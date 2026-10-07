"""Assemble header, tableau, footer (1 ou n pages)."""

from app.services.generate_docs.common.canvas import new_pdf
from app.services.generate_docs.common.fonts import register, set_pdf_metrics

from . import chrome, flow, footer, header, layout, middle, rules, static
from .data import Doc


def _fonts():
    register(layout.FONT, layout.FONT_FILE)
    register(layout.FONT_BOLD, layout.FONT_BOLD_FILE)
    set_pdf_metrics(
        layout.FONT, layout.FONT_ASCENT, layout.FONT_DESCENT,
        layout.FONT_BBOX, layout.FONT_CAP,
    )
    set_pdf_metrics(
        layout.FONT_BOLD, layout.FONT_ASCENT, layout.FONT_DESCENT,
        layout.FONT_BOLD_BBOX, layout.FONT_CAP,
    )


def generate(doc=None, dest=None):
    doc = rules.apply_doc(doc or Doc())
    _fonts()
    pagesize = (layout.PAGE_W, layout.PAGE_H)
    c, out = new_pdf(pagesize=pagesize, dest=dest)
    c._fnac_web = rules.en_ligne(doc.card)
    for plan in flow.paginate(doc):
        chrome.draw(c, doc, plan)
        header.draw(c, doc, plan)
        middle.draw(c, doc, plan)
        footer.draw(c, doc, plan)
        static.draw(c, doc)
        c.showPage()
    c.save()
    return out


if __name__ == "__main__":
    print(generate())
