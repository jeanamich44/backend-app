from . import account, company, logo, recipient, service

# ----------------------------------------------------------------------

def draw(c, doc):
    if not doc.visible.header:
        return
    logo.draw(c, doc)
    service.draw(c, doc)
    company.draw(c, doc)
    account.draw(c, doc)
    recipient.draw(c, doc)
