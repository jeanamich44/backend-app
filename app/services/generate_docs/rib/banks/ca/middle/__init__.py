"""Middle : notice, filets, agence, titulaire, codes, IBAN/BIC (× 2 coupons)."""

from .. import layout
from . import agence, bic, domiciliation, iban, lines, notice, table, titulaire


def draw(c, doc):
    if not doc.visible.middle:
        return
    for i in range(layout.CARD_COUNT):
        dy = i * layout.CARD_DY
        lines.draw(c, doc, dy)
        notice.draw(c, doc, dy)
        agence.draw(c, doc, dy)
        titulaire.draw(c, doc, dy)
        domiciliation.draw(c, doc, dy)
        table.draw(c, doc, dy)
        iban.draw(c, doc, dy)
        bic.draw(c, doc, dy)
