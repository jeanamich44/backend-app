"""Middle : trois coupons (domiciliation, tableau, IBAN/BIC, titulaire, notice, séparateur)."""

from .. import layout
from . import adresse, bic, domiciliation, iban, notice, separator, table, titulaire


def draw(c, doc):
    if not doc.visible.middle:
        return
    for i in range(layout.CARD_COUNT):
        dy = i * layout.CARD_DY
        domiciliation.draw(c, doc, dy)
        table.draw(c, doc, dy)
        iban.draw(c, doc, dy)
        bic.draw(c, doc, dy)
        titulaire.draw(c, doc, dy)
        adresse.draw(c, doc, dy)
        notice.draw(c, doc, dy)
        if i < layout.CARD_COUNT - 1:
            separator.draw(c, doc, dy)
    separator.draw_dashes(c, doc)
