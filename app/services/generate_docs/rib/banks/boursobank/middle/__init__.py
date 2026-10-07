"""Middle : deux colonnes live + séparateur raster (aucun vecteur sur ce gabarit)."""

from .. import layout
from . import bic, domiciliation, iban, separator, table, titulaire


def draw(c, doc):
    if not doc.visible.middle:
        return
    for i in range(layout.CARD_COUNT):
        dy = i * layout.CARD_DY
        titulaire.draw(c, doc, dy)
        bic.draw(c, doc, dy)
        iban.draw(c, doc, dy)
        domiciliation.draw(c, doc, dy)
        table.draw(c, doc, dy)
        if i < layout.CARD_COUNT - 1:
            separator.draw(c, doc, dy)
