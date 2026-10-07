"""Carte RIB : fond + titulaire, IBAN, BIC, tableau, domiciliation."""

from . import bic, card, domiciliation, iban, table, titulaire


def draw(c, doc):
    if not doc.visible.middle:
        return
    card.draw(c, doc)
    titulaire.draw(c, doc)
    iban.draw(c, doc)
    bic.draw(c, doc)
    table.draw(c, doc)
    domiciliation.draw(c, doc)
