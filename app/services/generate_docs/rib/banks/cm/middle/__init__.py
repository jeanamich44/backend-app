"""Middle : tableau RIB, IBAN/BIC, domiciliation, titulaire, notice, cadre."""

from . import (
    agence,
    bic,
    domiciliation,
    iban,
    lines,
    notice,
    reserved,
    table,
    titulaire,
)


def draw(c, doc):
    if not doc.visible.middle:
        return
    lines.draw(c, doc)
    table.draw(c, doc)
    agence.draw(c, doc)
    iban.draw(c, doc)
    bic.draw(c, doc)
    domiciliation.draw(c, doc)
    titulaire.draw(c, doc)
    notice.draw(c, doc)
    reserved.draw(c, doc)
