"""Middle : trois coupons (Y Skia : pas un simple ×221)."""

from .. import layout
from . import bic, iban, libelle, lines, notice, separator, table, titulaire


def draw(c, doc):
    if not doc.visible.middle:
        return
    for i in range(layout.CARD_COUNT):
        lines.draw(c, doc, i)
        notice.draw(c, doc, i)
        table.draw(c, doc, i)
        iban.draw(c, doc, i)
        bic.draw(c, doc, i)
        titulaire.draw(c, doc, i)
        libelle.draw(c, doc, i)
        if i < layout.CARD_COUNT - 1:
            separator.draw(c, doc, i)
