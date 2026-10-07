from .. import layout
from ..paint import draw_string, fill

# ----------------------------------------------------------------------

def draw(c, doc):
    if not doc.visible.header_contact:
        return
    text = doc.header.contact_email
    if not text:
        return
    fill(c, layout.COLOR_GREY)
    draw_string(
        c,
        layout.CONTACT_X,
        layout.CONTACT_Y,
        text,
        layout.FONT_REGULAR,
        layout.FONT_SIZE_BODY,
    )
