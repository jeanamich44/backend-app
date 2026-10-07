"""Footer = page + mentions Times-Roman."""

from . import legal, page


def draw(c, doc):
    if not doc.visible.footer:
        return
    page.draw(c, doc)
    legal.draw(c, doc)
