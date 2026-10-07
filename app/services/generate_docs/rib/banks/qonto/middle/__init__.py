"""Middle : nom de compte, IBAN/BIC, codes RIB, titulaire, pastille SWIFT, filets."""

from . import account, bic, iban, lines, swift, table, titulaire


def draw(c, doc):
    if not doc.visible.middle:
        return
    account.draw(c, doc)
    lines.draw(c, doc)
    iban.draw(c, doc)
    bic.draw(c, doc)
    table.draw(c, doc)
    titulaire.draw(c, doc)
    swift.draw(c, doc)
