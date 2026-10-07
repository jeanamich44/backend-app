from .. import layout
from . import bic, domiciliation, iban, lines, table, titulaire


def draw_card(c, doc, dy=0):
    if not doc.visible.middle:
        return
    titulaire.draw(c, doc, dy)
    iban.draw(c, doc, dy)
    bic.draw(c, doc, dy)
    lines.draw_iban_line(c, doc, dy)
    table.draw(c, doc, dy)
    domiciliation.draw(c, doc, dy)
    lines.draw_table_line(c, doc, dy)
    lines.draw_separators(c, doc, dy)


def draw(c, doc):
    for i in range(layout.CARD_COUNT):
        draw_card(c, doc, i * layout.CARD_DY)

