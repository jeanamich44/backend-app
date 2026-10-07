"""Header = logo + titre + date."""

from . import logo, title


def draw(c, doc):
    if not doc.visible.header:
        return
    logo.draw(c, doc)
    title.draw(c, doc)
