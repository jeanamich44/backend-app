"""Middle = corps, lieu de conso, date."""

from . import body, date, lieu


def draw(c, doc):
    if not doc.visible.middle:
        return
    body.draw(c, doc)
    lieu.draw(c, doc)
    date.draw(c, doc)
