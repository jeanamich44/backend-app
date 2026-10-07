"""Assemble header, tableau, footer (1 ou 2 pages)."""

from app.services.generate_docs.common.canvas import new_pdf
from app.services.generate_docs.common.fonts import register, set_pdf_metrics

from . import chrome, flow, footer, header, layout, middle, rules, static
from .data import Doc


def _fonts():
    register(layout.FONT_UNI, layout.FONT_UNI_FILE)
    set_pdf_metrics(
        layout.FONT_UNI, layout.UNI_ASCENT, layout.UNI_DESCENT,
        layout.UNI_BBOX, layout.UNI_CAP,
    )


def generate(doc=None, dest=None):
    doc = rules.apply_doc(doc or Doc())
    _fonts()
    pagesize = (layout.PAGE_W, layout.PAGE_H)
    c, out = new_pdf(pagesize=pagesize, dest=dest)
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
