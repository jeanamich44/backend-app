from .. import layout
from ..paint import fill_rect


def draw(c, doc):
    if not doc.visible.footer_line:
        return
    fill_rect(c, *layout.FOOT_RULE, layout.COLOR_GRAY)
