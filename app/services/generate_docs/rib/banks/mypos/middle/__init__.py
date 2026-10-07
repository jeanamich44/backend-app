"""Middle : lettre de confirmation + tableau IBAN."""

from . import letter, table


def draw(c, doc):
    if not doc.visible.middle:
        return
    letter.draw(c, doc)
    table.draw(c, doc)
