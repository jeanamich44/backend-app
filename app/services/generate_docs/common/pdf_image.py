"""XObjects image au format PDF d’origine (Indexed / DCT), sans passage par ImageReader."""

from io import BytesIO
from pathlib import Path
import zlib

from PIL import Image
from reportlab.lib.utils import _digester
from reportlab.pdfbase.pdfdoc import (
    PDFArray,
    PDFDictionary,
    PDFName,
    PDFObject,
    PDFStream,
)
from reportlab.pdfbase.pdfutils import readJPEGInfo

from app.services.generate_docs.common.paths import LOGOS_DIR


class _IndexedXObject(PDFObject):
    def __init__(self, width, height, indices: bytes, palette: bytes,
                 index_flate: bytes | None = None, palette_flate: bytes | None = None,
                 color_mask=None):
        self.width = width
        self.height = height
        pal = palette.ljust(768, b"\x00")[:768]
        self._index_flate = index_flate if index_flate is not None else zlib.compress(indices)
        self._palette_flate = palette_flate if palette_flate is not None else zlib.compress(pal)
        self.color_mask = color_mask

    def format(self, document):
        pal = PDFStream(
            dictionary=PDFDictionary({"Filter": PDFName("FlateDecode")}),
            content=self._palette_flate,
            filters=[],
        )
        pal_ref = document.Reference(pal)
        dictionary = {
            "Type": PDFName("XObject"),
            "Subtype": PDFName("Image"),
            "Width": self.width,
            "Height": self.height,
            "BitsPerComponent": 8,
            "Filter": PDFName("FlateDecode"),
            "ColorSpace": PDFArray([
                PDFName("Indexed"),
                PDFName("DeviceRGB"),
                255,
                pal_ref,
            ]),
        }
        if self.color_mask is not None:
            lo, hi = self.color_mask
            dictionary["Mask"] = PDFArray([lo, hi])
        img = PDFStream(
            dictionary=PDFDictionary(dictionary),
            content=self._index_flate,
            filters=[],
        )
        return img.format(document)


def _register(c, img, key: bytes):
    name = _digester(key)
    reg = c._doc.getXObjectName(name)
    existing = c._doc.idToObject.get(reg)
    if existing is None:
        img.name = name
        c._setXObjects(img)
        c._doc.Reference(img, reg)
        c._doc.addForm(name, img)
    c._formsinuse.append(name)
    c._currentPageHasImages = 1
    return reg


def _pdf_num(value):
    if abs(value - round(value)) < 1e-9:
        return str(int(round(value)))
    return ("%.10f" % value).rstrip("0")


def draw_indexed_html(c, width, height, index_flate, palette_flate, page_h, x, y_down, w, h,
                      color_mask=None):
    """Pose Indexed comme PDF4NET : page Y vers le bas + hauteur image négative."""
    pal = zlib.decompress(palette_flate)
    indices = zlib.decompress(index_flate)
    img = _IndexedXObject(
        width, height, indices, pal,
        index_flate=index_flate, palette_flate=palette_flate,
        color_mask=color_mask,
    )
    key = index_flate if color_mask is None else index_flate + b"|mask" + bytes(color_mask)
    reg = _register(c, img, key)
    c.saveState()
    c._code.append("1 0 0 1 0 %s cm" % _pdf_num(page_h))
    c._code.append("1 0 0 -1 0 0 cm")
    c._code.append("q")
    c._code.append("1 0 0 1 %s %s cm" % (_pdf_num(x), _pdf_num(y_down)))
    c._code.append("%s 0 0 %s 0 0 cm" % (_pdf_num(w), _pdf_num(-h)))
    c._code.append("/%s Do" % reg)
    c._code.append("Q")
    c.restoreState()


class _GrayFlateXObject(PDFObject):
    def __init__(self, data: bytes, width: int, height: int):
        self.width = width
        self.height = height
        self._data = data

    def format(self, document):
        img = PDFStream(
            dictionary=PDFDictionary({
                "Type": PDFName("XObject"),
                "Subtype": PDFName("Image"),
                "Width": self.width,
                "Height": self.height,
                "BitsPerComponent": 8,
                "Filter": PDFName("FlateDecode"),
                "ColorSpace": PDFName("DeviceGray"),
            }),
            content=self._data,
            filters=[],
        )
        return img.format(document)


class _JpegXObject(PDFObject):
    def __init__(self, data: bytes, width: int, height: int, cmyk=False, smask=None):
        self.width = width
        self.height = height
        self._data = data
        self.cmyk = cmyk
        self.smask = smask

    def format(self, document):
        dictionary = {
            "Type": PDFName("XObject"),
            "Subtype": PDFName("Image"),
            "Width": self.width,
            "Height": self.height,
            "BitsPerComponent": 8,
            "Filter": PDFName("DCTDecode"),
            "ColorSpace": PDFName("DeviceCMYK" if self.cmyk else "DeviceRGB"),
        }
        if self.cmyk:
            dictionary["Decode"] = PDFArray([1, 0, 1, 0, 1, 0, 1, 0])
        if self.smask is not None:
            dictionary["SMask"] = document.Reference(self.smask)
        img = PDFStream(
            dictionary=PDFDictionary(dictionary),
            content=self._data,
            filters=[],
        )
        return img.format(document)


def _indexed_from_png(path: Path):
    im = Image.open(path)
    if im.mode != "P":
        raise ValueError(f"{path.name} must be palette PNG (Indexed), got {im.mode}")
    pal = bytes(im.getpalette() or [])
    return im.size[0], im.size[1], im.tobytes(), pal


def _jpeg_info(data: bytes):
    info = readJPEGInfo(BytesIO(data))
    width, height = info[0], info[1]
    components = info[2] if len(info) > 2 else 3
    return width, height, components


def draw_logo(c, filename: str, x: float, y: float, w: float, h: float, smask: str | None = None, base_dir: Path | None = None):
    base = base_dir or LOGOS_DIR
    path = base / filename
    data = path.read_bytes()
    smask_data = (base / smask).read_bytes() if smask else b""
    name = _digester(data + smask_data)
    reg = c._doc.getXObjectName(name)
    img = c._doc.idToObject.get(reg)
    if img is None:
        suffix = path.suffix.lower()
        if suffix in {".jpg", ".jpeg"}:
            width, height, components = _jpeg_info(data)
            mask = None
            if smask:
                mask = _GrayFlateXObject(smask_data, width, height)
            img = _JpegXObject(data, width, height, cmyk=components == 4, smask=mask)
        else:
            width, height, indices, palette = _indexed_from_png(path)
            img = _IndexedXObject(width, height, indices, palette)
        img.name = name
        c._setXObjects(img)
        c._doc.Reference(img, reg)
        c._doc.addForm(name, img)
    c._formsinuse.append(name)
    c._currentPageHasImages = 1
    c.saveState()
    c.translate(x, y)
    c.scale(w, h)
    c._code.append("/%s Do" % reg)
    c.restoreState()
