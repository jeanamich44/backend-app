"""Une carte RIB : logo, titre, tableau, IBAN/BIC, titulaire."""

from . import iban_bic, logo, table, title, titulaire


def draw(c, doc, dy=0):
    logo.draw(c, doc, dy)
    title.draw(c, doc, dy)
    table.draw(c, doc, dy)
    iban_bic.draw(c, doc, dy)
    titulaire.draw(c, doc, dy)
