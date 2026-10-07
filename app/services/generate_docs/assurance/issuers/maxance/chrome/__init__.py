"""Carrés numérotés, filets gris, boutons téléphone."""

from .. import layout
from ..paint import badge, round_rect, stroke_line


def draw(c, doc):
    if not doc.visible.middle and not doc.visible.footer:
        return
    for x0, y0, number in layout.BADGES:
        if number == "9" and not doc.visible.footer:
            continue
        if number != "9" and not doc.visible.middle:
            continue
        badge(c, x0, y0, number)
    if doc.visible.middle:
        for x0, y, x1 in layout.LINES[:3]:
            stroke_line(c, x0, y, x1, 1.0, layout.COLOR_LINE)
        for box in (layout.PHONE1, layout.PHONE2):
            round_rect(
                c, *box, layout.PHONE_RADIUS,
                layout.COLOR_BADGE, layout.COLOR_PHONE_STROKE, 1.0,
            )
    if doc.visible.footer:
        for x0, y, x1 in layout.LINES[3:]:
            stroke_line(c, x0, y, x1, 1.0, layout.COLOR_LINE)
