"""Pays d'expédition, bande entre tableau et TVA (clip PDF4NET)."""

from .. import copy as texts
from .. import layout
from ..paint import clip_rect, draw_string, fill, width

_SEP = " – "


def _parts(ship: str):
    if _SEP not in ship:
        return ship, None
    left, right = ship.split(_SEP, 1)
    default_left = texts.SHIP.split(_SEP, 1)[0]
    en_x = layout.SHIP_EN_X + width(left, layout.FONT, layout.SIZE_9) - width(
        default_left, layout.FONT, layout.SIZE_9,
    )
    return left + _SEP, (en_x, right)


def draw(c, doc, plan):
    if not doc.visible.middle_ship:
        return
    ship = (doc.card.pays_expedition or "").strip()
    if not ship:
        return
    fill(c, layout.COLOR)
    c.saveState()
    clip_rect(c, *layout.SHIP_CLIP)
    head, tail = _parts(ship)
    draw_string(c, layout.SHIP_X, layout.SHIP_Y, head, layout.FONT, layout.SIZE_9)
    if tail:
        draw_string(c, tail[0], layout.SHIP_Y, tail[1], layout.FONT, layout.SIZE_9)
    c.restoreState()
