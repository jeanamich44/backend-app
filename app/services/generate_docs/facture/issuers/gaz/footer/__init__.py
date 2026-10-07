"""Pied : triman, contacts, économies, chèque énergie."""

from . import cheque, contacts, economies, triman


def draw(c, doc):
    if not doc.visible.footer:
        return
    triman.draw(c, doc)
    contacts.draw(c, doc)
    economies.draw(c, doc)
    cheque.draw(c, doc)
