"""Notice d'usage : wrap + justification iText (Tc/Tw, ratio 1/3)."""

from .. import layout
from ..paint import draw_string, fill, width, wrap_lines


def _itext_spacing(text: str, font: str, size: float, target: float):
    extra = target - width(text, font, size) - width(" ", font, size)
    n = len(text)
    spaces = text.count(" ")
    denom = n + 3 * spaces
    if extra <= 0 or denom <= 0:
        return 0, None
    tc = extra / denom
    return tc, 3 * tc


def draw(c, doc, dy=0):
    if not doc.visible.middle_notice:
        return
    text = doc.card.notice
    if not text:
        return
    fill(c, layout.COLOR)
    y = layout.NOTICE_Y + dy
    font, size, max_w = layout.LABEL_FONT, layout.SIZE_LABEL, layout.NOTICE_W
    for paragraph in text.split("\n"):
        paragraph = paragraph.strip()
        if not paragraph:
            y += layout.NOTICE_LEADING
            continue
        lines = wrap_lines(paragraph, font, size, max_w)
        last = len(lines) - 1
        for i, line in enumerate(lines):
            tc, tw = (0, None)
            if i < last:
                tc, tw = _itext_spacing(line, font, size, max_w)
            draw_string(
                c, layout.NOTICE_X, y, line + " " if i < last else line, font, size,
                max_width=max_w + 4, char_space=tc, word_space=tw,
            )
            y += layout.NOTICE_LEADING
