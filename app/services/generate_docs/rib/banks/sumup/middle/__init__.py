"""Middle : titulaire, compte, notice."""

from . import account, holder, notice


def draw(c, doc):
    if not doc.visible.middle:
        return
    holder.draw(c, doc)
    account.draw(c, doc)
    notice.draw(c, doc)
