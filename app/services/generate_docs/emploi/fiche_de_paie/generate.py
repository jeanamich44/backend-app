try:
    from app.services.generate_docs.common.canvas import new_pdf
    from app.services.generate_docs.common.fonts import register
except ImportError:
    from core.canvas import new_pdf
    from core.fonts import register

from . import rules
from .data import Doc
from .services import ecriture

# ----------------------------------------------------------------------


def _fonts():
    register(ecriture.layout.FONT_ARIAL, ecriture.layout.FONT_ARIAL_FILE)
    register(ecriture.layout.FONT_ARIAL_BOLD, ecriture.layout.FONT_ARIAL_BOLD_FILE)
    register(ecriture.layout.FONT_ARIAL_ITALIC, ecriture.layout.FONT_ARIAL_ITALIC_FILE)


def generate(doc=None, dest=None):
    doc = rules.apply_doc(doc or Doc())
    _fonts()
    pagesize = (ecriture.layout.PAGE_W, ecriture.layout.PAGE_H)
    c, out = new_pdf(pagesize=pagesize, dest=dest)
    ecriture.draw(c, doc)
    c.showPage()
    c.save()
    return out


def generate_pack(docs=None, dest=None):
    if not docs:
        docs = [Doc()]
    docs = [rules.apply_doc(d) for d in docs]
    _fonts()
    pagesize = (ecriture.layout.PAGE_W, ecriture.layout.PAGE_H)
    c, out = new_pdf(pagesize=pagesize, dest=dest)
    for d in docs:
        ecriture.draw(c, d)
        c.showPage()
    c.save()
    return out


if __name__ == "__main__":
    print(generate())
