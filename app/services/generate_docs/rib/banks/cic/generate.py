"""Assemble header, middle, footer."""

from . import footer, header, layout, middle, rules
from .data import Doc
from app.services.generate_docs.common.canvas import new_pdf


def generate(doc=None, dest=None):
    doc = rules.apply_doc(doc or Doc())
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
