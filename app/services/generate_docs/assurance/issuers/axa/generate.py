from app.services.generate_docs.common.canvas import new_pdf
from app.services.generate_docs.common.fonts import register, set_pdf_metrics

from . import footer, header, layout, middle, rules
from .data import Doc

# ----------------------------------------------------------------------


def _fonts():
    register(layout.FONT_REGULAR, layout.FONT_REGULAR_FILE)
    register(layout.FONT_BOLD, layout.FONT_BOLD_FILE)
    register(layout.FONT_ITALIC, layout.FONT_ITALIC_FILE)
    register(layout.FONT_LIGHT, layout.FONT_LIGHT_FILE)
    register(layout.FONT_NARROW, layout.FONT_NARROW_FILE)
    register(layout.FONT_CARLITO, layout.FONT_CARLITO_FILE)

    set_pdf_metrics(
        layout.FONT_REGULAR, layout.FONT_REGULAR_ASCENT, layout.FONT_REGULAR_DESCENT,
        layout.FONT_REGULAR_BBOX, layout.FONT_REGULAR_CAP,
    )
    set_pdf_metrics(
        layout.FONT_BOLD, layout.FONT_BOLD_ASCENT, layout.FONT_BOLD_DESCENT,
        layout.FONT_BOLD_BBOX, layout.FONT_BOLD_CAP,
    )
    set_pdf_metrics(
        layout.FONT_ITALIC, layout.FONT_ITALIC_ASCENT, layout.FONT_ITALIC_DESCENT,
        layout.FONT_ITALIC_BBOX, layout.FONT_ITALIC_CAP,
    )
    set_pdf_metrics(
        layout.FONT_LIGHT, layout.FONT_LIGHT_ASCENT, layout.FONT_LIGHT_DESCENT,
        layout.FONT_LIGHT_BBOX, layout.FONT_LIGHT_CAP,
    )
    set_pdf_metrics(
        layout.FONT_NARROW, layout.FONT_NARROW_ASCENT, layout.FONT_NARROW_DESCENT,
        layout.FONT_NARROW_BBOX, layout.FONT_NARROW_CAP,
    )
    set_pdf_metrics(
        layout.FONT_CARLITO, layout.FONT_CARLITO_ASCENT, layout.FONT_CARLITO_DESCENT,
        layout.FONT_CARLITO_BBOX, layout.FONT_CARLITO_CAP,
    )


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
