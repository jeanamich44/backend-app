"""Cellules variables du tableau."""

from .. import layout
from ..paint import draw_string, fill, width


def _date(c, x, y, jour, day):
    if not jour and not day:
        return
    fill(c, layout.COLOR_MUTED)
    if not jour:
        draw_string(c, x, y, day, layout.FONT_DEJAVU, layout.SIZE_CELL)
        return
    draw_string(c, x, y, jour, layout.FONT_DEJAVU, layout.SIZE_CELL)
    if not day:
        return
    space_x = int(x + width(jour, layout.FONT_DEJAVU, layout.SIZE_CELL))
    draw_string(c, space_x, y, " ", layout.FONT_HELV, layout.SIZE_CELL)
    draw_string(
        c, space_x + layout.DATE_GAP, y,
        day, layout.FONT_DEJAVU, layout.SIZE_CELL,
    )


def draw(c, doc):
    fill(c, layout.COLOR_MUTED)
    for i, rdv in enumerate(doc.card.rdvs[: layout.MAX_ROWS]):
        date_y, start_y, end_y, act_y = layout.row_text_ys(i)
        _date(c, layout.DATE_X, date_y, rdv.jour, rdv.date)
        fill(c, layout.COLOR_MUTED)
        draw_string(
            c, layout.START_X, start_y,
            rdv.debut, layout.FONT, layout.SIZE_CELL,
        )
        draw_string(
            c, layout.END_X, end_y,
            rdv.fin, layout.FONT, layout.SIZE_CELL,
        )
        draw_string(
            c, layout.ACT_X, act_y,
            rdv.activite, layout.FONT, layout.SIZE_CELL,
            max_width=layout.FILL_XS[4] - layout.ACT_X - 4,
        )
        if rdv.commentaire:
            draw_string(
                c, layout.COM_X, act_y,
                rdv.commentaire, layout.FONT, layout.SIZE_CELL,
                max_width=layout.FILL_XS[-1] - layout.COM_X - 4,
            )
