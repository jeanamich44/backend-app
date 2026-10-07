"""Assemble header + middle, un coupon."""

from pathlib import Path

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from app.services.generate_docs.common.canvas import new_pdf
from app.services.generate_docs.common.fonts import set_pdf_metrics

from . import embed, header, layout, middle, rules, widths
from .data import Doc

_CHROME = Path(__file__).resolve().parent / "chrome"


def _ensure_font(name: str, filename: str):
    if name in pdfmetrics.getRegisteredFontNames():
        return
    font = TTFont(name, str(_CHROME / filename))
    embed.bind_keep_ids(font.face)
    pdfmetrics.registerFont(font)


def _apply_cid_widths(name: str, table: dict[int, int]):
    face = pdfmetrics.getFont(name).face
    for code, width in table.items():
        face.charWidths[code] = width


def _fonts():
    _ensure_font(layout.FONT, layout.FONT_FILE)
    _ensure_font(layout.FONT_BOLD, layout.FONT_BOLD_FILE)
    _apply_cid_widths(layout.FONT, widths.REGULAR)
    _apply_cid_widths(layout.FONT_BOLD, widths.BOLD)
    set_pdf_metrics(
        layout.FONT, layout.FONT_ASCENT, layout.FONT_DESCENT,
        layout.FONT_BBOX, layout.FONT_CAP,
    )
    set_pdf_metrics(
        layout.FONT_BOLD, layout.FONT_ASCENT, layout.FONT_DESCENT,
        layout.FONT_BOLD_BBOX, layout.FONT_BOLD_CAP,
    )


def generate(doc=None, dest=None):
    doc = rules.apply_doc(doc or Doc())
    _fonts()
    pagesize = (layout.PAGE_W, layout.PAGE_H)
    c, out = new_pdf(pagesize=pagesize, dest=dest)
    header.draw(c, doc)
    middle.draw(c, doc)
    c.showPage()
    c.save()
    return out


if __name__ == "__main__":
    print(generate())
