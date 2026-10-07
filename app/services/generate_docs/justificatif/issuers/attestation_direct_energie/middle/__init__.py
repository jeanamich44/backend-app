"""Middle = réf. client, corps, signature, note."""

from . import body, note, refs, sign


def draw(c, doc):
    if not doc.visible.middle:
        return
    refs.draw(c, doc)
    body.draw(c, doc)
    sign.draw(c, doc)
    note.draw(c, doc)
