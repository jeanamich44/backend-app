"""Middle : titulaire, domiciliation, tableau, IBAN/BIC, filets, coupe."""

from .. import layout
from . import domiciliation, iban, lines, separator, table, titulaire


def draw(c, doc):
    if not doc.visible.middle:
        return
    for i in range(layout.CARD_COUNT):
        dy = i * layout.CARD_DY
        titulaire.draw(c, doc, dy)
        domiciliation.draw(c, doc, dy)
        table.draw(c, doc, dy)
        iban.draw(c, doc, dy)
        lines.draw(c, doc, dy)
        if i < layout.CARD_COUNT - 1:
            separator.draw(c, doc, dy)
