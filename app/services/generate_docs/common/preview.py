import io
import zipfile
import pymupdf as fitz

PREVIEW_WATERMARK = "APERCU"


def add_preview_watermark(pdf_bytes: bytes, text: str = PREVIEW_WATERMARK) -> bytes:
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    try:
        for page in doc:
            rect = page.rect
            for y in range(0, int(rect.height), 160):
                for x in range(0, int(rect.width), 220):
                    pos = fitz.Point(x, y)
                    page.insert_text(
                        pos,
                        text,
                        fontname="helv",
                        fontsize=38,
                        color=(0.82, 0.82, 0.82),
                        morph=(pos, fitz.Matrix(-40)),
                        overlay=True,
                    )
        return doc.tobytes(deflate=True)
    finally:
        doc.close()


def pdf_bytes_to_jpg(pdf_bytes: bytes, dpi: int = 150, jpg_quality: int = 85) -> bytes:
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    try:
        page = doc[0]
        pix = page.get_pixmap(dpi=dpi, alpha=False)
        return pix.tobytes(output="jpeg", jpg_quality=jpg_quality)
    finally:
        doc.close()


def pdf_bytes_to_watermarked_jpg(
    pdf_bytes: bytes,
    dpi: int = 120,
    jpg_quality: int = 70,
    text: str = PREVIEW_WATERMARK,
) -> bytes:
    return pdf_bytes_to_jpg(
        add_preview_watermark(pdf_bytes, text),
        dpi=dpi,
        jpg_quality=jpg_quality,
    )


def flatten_pdf_bytes(pdf_bytes: bytes, dpi: int = 300, jpg_quality: int = 92) -> bytes:
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    try:
        new_doc = fitz.open()
        for page in doc:
            pix = page.get_pixmap(dpi=dpi, colorspace=fitz.csRGB)
            img_bytes = pix.tobytes(output="jpeg", jpg_quality=jpg_quality)
            new_page = new_doc.new_page(width=page.rect.width, height=page.rect.height)
            new_page.insert_image(page.rect, stream=img_bytes)
        return new_doc.tobytes(deflate=True, garbage=3)
    finally:
        doc.close()


def flatten_zip_bytes(zip_bytes: bytes, dpi: int = 300, jpg_quality: int = 92) -> bytes:
    buf_in = io.BytesIO(zip_bytes)
    buf_out = io.BytesIO()
    with zipfile.ZipFile(buf_in, "r") as zf_in, zipfile.ZipFile(buf_out, "w", zipfile.ZIP_DEFLATED) as zf_out:
        for item in zf_in.infolist():
            content = zf_in.read(item.filename)
            if item.filename.lower().endswith(".pdf"):
                content = flatten_pdf_bytes(content, dpi=dpi, jpg_quality=jpg_quality)
            zf_out.writestr(item, content)
    return buf_out.getvalue()

