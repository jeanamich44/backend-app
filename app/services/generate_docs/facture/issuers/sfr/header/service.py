from .. import copy as texts
from .. import layout, paint

# ----------------------------------------------------------------------

def draw(c, doc):
    if not doc.visible.header_service:
        return
    card = doc.card
    font = layout.FONT
    sz = layout.SIZE_TEXT_SM
    col = layout.COLOR_TEXT

    paint.draw_string(c, layout.SERVICE_X, layout.SERVICE_Y0, texts.SERVICE_LABEL, font, sz, col)
    paint.draw_string(c, layout.SERVICE_VAL_X, layout.SERVICE_Y0, texts.SERVICE_ASSISTANCE, font, sz, col)

    url_x = layout.LINK_X0
    url_text = card.service_faq_url
    paint.draw_string(c, url_x, layout.SERVICE_Y0, url_text, font, sz, layout.COLOR_BLUE_LINK)
    url_w = paint.width(url_text, font, sz)
    paint.stroke_line(c, url_x, layout.LINK_Y, url_x + url_w, layout.LINK_Y, 0.6, layout.COLOR_BLUE_LINK)
    paint.draw_string(c, url_x + url_w + 0.34, layout.SERVICE_Y0, texts.SERVICE_DOT, font, sz, col)

    y1 = layout.SERVICE_Y0 + layout.SERVICE_LINE_H
    paint.draw_string(c, layout.SERVICE_VAL_X, y1, card.service_phone, font, sz, col)

    y2 = y1 + layout.SERVICE_LINE_H
    paint.draw_string(c, layout.SERVICE_VAL_X, y2, texts.SERVICE_SFR, font, sz, col)

    y3 = y2 + layout.SERVICE_LINE_H
    paint.draw_string(c, layout.SERVICE_VAL_X, y3, card.service_siege, font, sz, col)
