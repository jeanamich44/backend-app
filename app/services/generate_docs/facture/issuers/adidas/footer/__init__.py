"""Footer = trait + mentions légales."""

from . import legal, line


def draw(c, doc):
    if not doc.visible.footer:
        return
    line.draw(c, doc)
    legal.draw(c, doc)
