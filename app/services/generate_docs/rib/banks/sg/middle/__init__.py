"""Middle : titulaire, agence, cadre RIB, codes, IBAN/BIC, pointillés."""

from .. import layout
from . import agence, bic, iban, lines, separator, table, titulaire


def draw(c, doc):
    if not doc.visible.middle:
        return
    for i in range(layout.CARD_COUNT):
        dy = i * layout.CARD_DY
        titulaire.draw(c, doc, dy)
        agence.draw(c, doc, dy)
        lines.draw(c, doc, dy)
        table.draw(c, doc, dy)
        iban.draw(c, doc, dy)
        bic.draw(c, doc, dy)
        separator.draw(c, doc, dy)
