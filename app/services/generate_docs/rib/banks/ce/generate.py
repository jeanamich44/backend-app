from app.services.generate_docs.common.canvas import new_pdf
from app.services.generate_docs.common.fonts import register, set_pdf_metrics

from . import footer, header, layout, middle, rules
from .data import Doc


def _fonts():
    register(layout.FONT, layout.FONT_FILE)
    register(layout.FONT_MEDIUM, layout.FONT_MEDIUM_FILE)
    register(layout.FONT_IBAN, layout.FONT_IBAN_FILE)
    set_pdf_metrics(layout.FONT, 932, -189, [-23, -188, 792, 783], 693)
    set_pdf_metrics(layout.FONT_MEDIUM, 932, -189, [-27, -185, 794, 808], 693)
    set_pdf_metrics(layout.FONT_IBAN, 750, -250, [0, -193, 561, 641], 637)


def generate(doc=None, dest=None):
    doc = rules.apply_doc(doc or Doc())
    _fonts()
    pagesize = (layout.PAGE_W, layout.PAGE_H)
    c, out = new_pdf(pagesize=pagesize, dest=dest)
    for i in range(layout.CARD_COUNT):
        dy = i * layout.CARD_DY
        header.draw_card(c, doc, dy)
        middle.draw_card(c, doc, dy)
    footer.draw(c, doc)
    c.showPage()
    c.save()
    return out


if __name__ == "__main__":
    generate()


