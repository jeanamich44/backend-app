from app.services.generate_docs.common.canvas import new_pdf
from app.services.generate_docs.common.fonts import register, set_pdf_metrics
from . import chrome, footer, header, layout, middle, rules, static
from .data import Doc

# ----------------------------------------------------------------------

def _fonts():
    register(layout.FONT_REGULAR, layout.FONT_REGULAR_FILE)
    register(layout.FONT_BOLD, layout.FONT_BOLD_FILE)

    set_pdf_metrics(layout.FONT_REGULAR, 1069, -293, [-549, -272, 1201, 1048], 714)
    set_pdf_metrics(layout.FONT_BOLD, 1069, -293, [-619, -295, 1319, 1069], 714)

# ----------------------------------------------------------------------

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

# ----------------------------------------------------------------------

if __name__ == "__main__":
    print(generate())
