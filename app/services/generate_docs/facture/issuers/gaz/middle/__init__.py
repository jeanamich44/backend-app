"""Middle : phrase latérale + montants + prochaine + paiement."""

from . import amounts, legal, next, paiement


def draw(c, doc):
    if not doc.visible.middle:
        return
    legal.draw(c, doc)
    amounts.draw(c, doc)
    next.draw(c, doc)
    paiement.draw(c, doc)
