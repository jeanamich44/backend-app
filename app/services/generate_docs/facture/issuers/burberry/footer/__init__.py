"""Footer = filet, paiement, notice retrait, mentions légales."""

from . import legal, line, notice, payment


def draw(c, doc):
    if not doc.visible.footer:
        return
    line.draw(c, doc)
    payment.draw(c, doc)
    notice.draw(c, doc)
    legal.draw(c, doc)
