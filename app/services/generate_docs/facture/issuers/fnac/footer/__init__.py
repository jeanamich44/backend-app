"""Footer = mentions légales + aide (canal figé à la création de page)."""

from . import help as help_box
from . import legal


def draw(c, doc, plan):
    if not doc.visible.footer:
        return
    legal.draw(c, doc, plan)
    help_box.draw(c, doc, plan)
