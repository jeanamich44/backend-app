"""Colonne gauche : Vos Contacts Utiles."""

from .. import copy as texts
from .. import layout
from ..chrome.contacts_paths import CONTACTS_BOX_OPS, CONTACTS_HEAD_OPS, STROKE_W
from ..paint import draw_image, draw_spans, fill_ops, stroke_ops

_S = layout.PICTO_S
_CR_W = layout.CRISTAL_W
_CR_H = layout.CRISTAL_H

IMAGES = (
    ("gaz_picto_user.jpg", 44.2204704284668, 599.84912109375, _S, _S, None),
    ("gaz_picto_app.jpg", 44.2204704284668, 616.2900390625, _S, _S, None),
    ("gaz_picto_phone.jpg", 44.2204704284668, 633.014404296875, _S, _S, None),
    ("gaz_cristal.jpg", 59.527557373046875, 642.1196899414062, _CR_W, _CR_H, layout.CRISTAL_SMASK),
    ("gaz_picto_mail.jpg", 44.2204704284668, 667.313720703125, _S, _S, None),
    ("gaz_picto_gas.jpg", 44.2204704284668, 698.6196899414062, _S, _S, None),
    ("gaz_grdf.jpg", 156.47244262695312, 697.7692260742188, layout.GRDF_W, layout.GRDF_H, None),
    ("gaz_picto_elec.jpg", 44.2204704284668, 716.7614135742188, _S, _S, None),
    ("gaz_cristal.jpg", 156.47244262695312, 713.9266967773438, _CR_W, _CR_H, layout.CRISTAL_SMASK),
)


def _spans():
    b, r, sm, xs = layout.FONT_BOLD, layout.FONT, layout.SIZE_SMALL, layout.SIZE_XS
    head, body, phone = layout.SIZE_HEAD, layout.SIZE_BODY, layout.SIZE_HEAD
    white, blue, black, grey = (
        layout.COLOR_WHITE, layout.COLOR_BLUE, layout.COLOR, layout.COLOR_PHONE,
    )
    t = texts
    return (
        (125.24951171875, 574.28076171875, t.CONTACTS_TITLE, b, head, white),
        (107.17474365234375, 595.46142578125, t.CONTACTS_SERVICE, b, head, blue),
        (59.527557373046875, 609.7116088867188, t.CONTACTS_WEB, r, body, black),
        (216.95159912109375, 609.7116088867188, t.CONTACTS_URL, b, body, black),
        (59.527557373046875, 626.152587890625, t.CONTACTS_APP, r, body, black),
        (59.527557373046875, 640.41162109375, t.CONTACTS_HOURS, r, sm, black),
        (127.55905151367188, 652.6761474609375, t.CONTACTS_PHONE, b, phone, grey),
        (127.558837890625, 660.256103515625, t.CONTACTS_FREE, r, xs, grey),
        (59.527557373046875, 676.751220703125, t.CONTACTS_MAIL_NAME, r, body, black),
        (86.6474609375, 676.751220703125, t.CONTACTS_MAIL_ADDR, r, sm, black),
        (106.9046630859375, 693.09814453125, t.CONTACTS_URGENCE, b, head, blue),
        (59.527557373046875, 707.7099609375, t.CONTACTS_GRDF, r, sm, black),
        (159.82049560546875, 707.3485107421875, t.CONTACTS_GRDF_PHONE, b, body, black),
        (59.527557373046875, 722.802978515625, t.CONTACTS_ENEDIS, r, sm, black),
        (224.50393676757812, 724.483154296875, t.CONTACTS_ENEDIS_PHONE, b, phone, grey),
        (224.50393676757812, 732.0631103515625, t.CONTACTS_FREE, r, xs, grey),
    )


def draw(c, doc):
    if not doc.visible.footer_contacts:
        return
    stroke_ops(c, CONTACTS_BOX_OPS, layout.BLUE, STROKE_W, cap=0)
    fill_ops(c, CONTACTS_HEAD_OPS, layout.BLUE, even_odd=True)
    for filename, x, y, w, h, smask in IMAGES:
        draw_image(c, filename, x, y, w, h, smask=smask)
    draw_spans(c, _spans())
