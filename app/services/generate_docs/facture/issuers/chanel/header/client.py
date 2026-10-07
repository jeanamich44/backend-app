from .. import layout, paint

# ----------------------------------------------------------------------

def draw(c, doc):
    paint.draw_text(c, layout.CLIENT_CODE_X, layout.CLIENT_CODE_Y, doc.header.client_code)
    y = layout.CLIENT_Y
    lines = [
        doc.header.client_name,
        doc.header.client_address_1,
        doc.header.client_address_2,
        doc.header.client_address_3,
    ]
    for line in lines:
        if line:
            paint.draw_text(c, layout.CLIENT_X, y, line)
        y -= layout.CLIENT_LEADING
