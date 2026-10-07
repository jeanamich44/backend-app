"""Footer = un sous-bloc mentions."""

from . import mentions


def draw(c, doc):
    if not doc.visible.footer:
        return
    mentions.draw(c, doc)
