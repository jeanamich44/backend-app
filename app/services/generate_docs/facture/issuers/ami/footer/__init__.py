"""Footer = remerciements, signature, filet bas."""

from . import line, sign, thanks


def draw(c, doc):
    if not doc.visible.footer:
        return
    thanks.draw(c, doc)
    sign.draw(c, doc)
    line.draw(c, doc)
