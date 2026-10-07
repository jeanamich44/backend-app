"""Footer = retours, émetteur, ligne TCPDF."""

from . import issuer, returns, tcpdf


def draw(c, doc):
    if not doc.visible.footer:
        return
    returns.draw(c, doc)
    issuer.draw(c, doc)
    tcpdf.draw(c, doc)
