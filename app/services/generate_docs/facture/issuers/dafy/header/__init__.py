from . import addresses, banner, issuer, logo, refs, title


def draw(c, doc):
    if not doc.visible.header:
        return
    banner.draw(c, doc)
    logo.draw(c, doc)
    title.draw(c, doc)
    issuer.draw(c, doc)
    refs.draw(c, doc)
    addresses.draw(c, doc)
