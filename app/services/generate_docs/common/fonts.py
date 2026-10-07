from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from .paths import FONTS_DIR

_registered = set()


def font_path(filename: str):
    path = FONTS_DIR / filename
    if not path.is_file():
        raise FileNotFoundError(f"Police introuvable : {path}")
    return path


def register(name: str, filename: str):
    if name in _registered and name in pdfmetrics._fonts:
        return name
    if name in pdfmetrics._fonts:
        _registered.add(name)
        return name
    pdfmetrics.registerFont(TTFont(name, str(font_path(filename))))
    _registered.add(name)
    return name


def set_pdf_metrics(name, ascent, descent, bbox, cap_height=None, **kwargs):
    face = pdfmetrics.getFont(name).face
    face.ascent = ascent
    face.descent = descent
    face.bbox = list(bbox)
    if cap_height is not None:
        face.capHeight = cap_height
    for k, v in kwargs.items():
        setattr(face, k, v)
