"""Paragraphe d'attestation (ArialMT 9, wrap calé)."""

from .. import layout, rules
from ..paint import draw_string, fill, wrap_lines


def draw(c, doc):
    if not doc.visible.middle_body:
        return
    lines = wrap_lines(
        rules.body_text(doc.card),
        layout.FONT, layout.BODY_SIZE, layout.BODY_MAX_W,
    )
    fill(c, layout.COLOR)
    for i, line in enumerate(lines):
        draw_string(
            c, layout.BODY_X, layout.BODY_Y0 + i * layout.BODY_PITCH,
            line, layout.FONT, layout.BODY_SIZE,
        )
