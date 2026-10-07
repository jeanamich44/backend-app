"""Middle = sections 1–8 (titres, valeurs, aide, validité)."""

from . import fields, help as help_block


def draw(c, doc):
    if not doc.visible.middle:
        return
    fields.draw(c, doc)
    help_block.draw(c, doc)
