import re

from .. import copy as texts
from .. import layout
from ..paint import draw_right, fill


def draw(c, doc):
    if not doc.visible.header_title:
        return
    fill(c, layout.COLOR)
    num = str(doc.card.num_facture or "").strip()
    num = re.sub(r"^(?:FAC(?:TURE)?\s*(?:N°?)?\s*[-:]?\s*)", "", num, flags=re.IGNORECASE)
    draw_right(
        c, layout.TITLE_RIGHT, layout.TITLE_Y,
        texts.TITLE_PREFIX + num,
        layout.FONT_BOLD, layout.SIZE_TITLE,
    )
