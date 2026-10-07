"""Header = titre de page, notice FR, notice EN."""

from . import notice_en, notice_fr, title


def draw(c, doc):
    if not doc.visible.header:
        return
    title.draw(c, doc)
    notice_fr.draw(c, doc)
    notice_en.draw(c, doc)
