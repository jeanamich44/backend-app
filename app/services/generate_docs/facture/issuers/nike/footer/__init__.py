"""Footer = vendeur, notice retours, pagination."""

from . import notice, page, seller


def draw(c, doc):
    if not doc.visible.footer:
        return
    seller.draw(c, doc)
    notice.draw(c, doc)
    page.draw(c, doc)
