"""Middle : trois coupons (titulaire, IBAN, BIC, tableau, légende, séparateur)."""

from .. import layout
from . import bic, iban, legend, separator, table, titulaire


def draw(c, doc):
    if not doc.visible.middle:
        return
    for i in range(layout.CARD_COUNT):
        dy = i * layout.CARD_DY
        titulaire.draw(c, doc, dy)
        iban.draw(c, doc, dy)
        bic.draw(c, doc, dy)
        table.draw(c, doc, dy)
        legend.draw(c, doc, dy)
        if i < layout.CARD_COUNT - 1:
            separator.draw(c, doc, dy)
