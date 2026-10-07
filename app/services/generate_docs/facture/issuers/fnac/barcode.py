"""Code 39 du n° de facture (9 chiffres), comme les gabarits Fnac.pdf / fnac1.pdf."""

from . import layout
from .paint import fill_rect

_PATTERNS = {
    "0": "nnnwwnwnn",
    "1": "wnnwnnnnw",
    "2": "nnwwnnnnw",
    "3": "wnwwnnnnn",
    "4": "nnnwwnnnw",
    "5": "wnnwwnnnn",
    "6": "nnwwwnnnn",
    "7": "nnnwnnwnw",
    "8": "wnnwnnwnn",
    "9": "nnwwnnwnn",
    "*": "nwnnwnwnn",
}


def digits(value: str) -> str:
    return "".join(ch for ch in (value or "") if ch.isdigit())


def payload(value: str) -> str:
    body = digits(value)
    if not body:
        return "0" * layout.BARCODE_DIGITS
    if len(body) < layout.BARCODE_DIGITS:
        return body.zfill(layout.BARCODE_DIGITS)
    return body


def _runs(value: str):
    body = "*" + payload(value) + "*"
    for index, char in enumerate(body):
        pattern = _PATTERNS.get(char, _PATTERNS["0"])
        for pos, mark in enumerate(pattern):
            yield (3 if mark == "w" else 1), (pos % 2 == 0)
        if index < len(body) - 1:
            yield 1, False


def draw(c, value: str, box):
    x0, y0, x1, y1 = box
    fill_rect(c, x0, y0, x1, y1, layout.COLOR_WHITE)
    pad = layout.BARCODE_PAD
    p = payload(value)
    modules = max(layout.BARCODE_MODULES, (len(p) + 2) * 16 - 1)
    unit = ((x1 - x0) - 2 * pad) / modules
    x = x0 + pad
    top = y0 + pad
    bot = y1 - pad
    for width, bar in _runs(value):
        w = width * unit
        if bar:
            fill_rect(c, x, top, x + w, bot, layout.COLOR)
        x += w
