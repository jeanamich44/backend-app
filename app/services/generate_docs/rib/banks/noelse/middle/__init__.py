"""Middle : IBAN, BIC, titulaire, domiciliation, notice."""

from . import bic, domiciliation, iban, notice, table, titulaire


def draw(c, doc):
    if not doc.visible.middle:
        return
    for i in range(3):
        table.draw(c, doc, i)
        iban.draw(c, doc, i)
        bic.draw(c, doc, i)
        titulaire.draw(c, doc, i)
        domiciliation.draw(c, doc, i)
        notice.draw(c, doc, i)
