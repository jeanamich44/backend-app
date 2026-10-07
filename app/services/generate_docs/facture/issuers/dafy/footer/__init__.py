from . import legal, line, thanks


def draw(c, doc):
    if not doc.visible.footer:
        return
    thanks.draw(c, doc)
    line.draw(c, doc)
    legal.draw(c, doc)
