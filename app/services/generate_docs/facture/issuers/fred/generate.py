from pathlib import Path
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from app.services.generate_docs.common.canvas import new_pdf
from .data import Doc

PAGE_W, PAGE_H = A4
LOGO_PATH = Path(__file__).resolve().parent.parent.parent.parent / "assets" / "logos" / "fred.png"


def generate(doc: Doc = None, dest=None):
    doc = doc or Doc()
    c, out = new_pdf(pagesize=(PAGE_W, PAGE_H), dest=dest)

    vis = doc.visible or {}

    c.setFillColor(HexColor("#FFFFFF"))
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    if vis.get("header", True):
        if vis.get("header_logo", True) and LOGO_PATH.exists():
            c.drawImage(str(LOGO_PATH), 60, PAGE_H - 105, width=85, height=30, preserveAspectRatio=True, mask="auto")

        if vis.get("header_boutique", True):
            c.setFillColor(HexColor("#000000"))
            c.setFont("Helvetica-Bold", 10.5)
            c.drawCentredString(PAGE_W / 2, PAGE_H - 58, str(doc.store_name))
            if doc.store_code:
                c.setFont("Helvetica", 9.5)
                c.drawCentredString(PAGE_W / 2, PAGE_H - 125, str(doc.store_code))

        if vis.get("header_meta", True):
            invoice_title = f"Facture n°{doc.num_facture}"
            c.setFillColor(HexColor("#000000"))
            c.setFont("Helvetica-Bold", 10)
            c.drawString(60, PAGE_H - 225, invoice_title)

            tw = c.stringWidth(invoice_title, "Helvetica-Bold", 10)
            c.setStrokeColor(HexColor("#000000"))
            c.setLineWidth(0.8)
            c.line(60, PAGE_H - 227, 60 + tw, PAGE_H - 227)

            if doc.date_lieu:
                c.setFont("Helvetica", 9.5)
                c.drawString(60, PAGE_H - 255, str(doc.date_lieu))

    if vis.get("middle", True):
        table_x = 60
        table_w = 475
        table_top = PAGE_H - 280
        table_bottom = 175
        table_h = table_top - table_bottom
        header_h = 20
        split_x = table_x + table_w - 95

        if vis.get("middle_table", True):
            c.setFillColor(HexColor("#F6F6F6"))
            c.rect(table_x, table_top - header_h, table_w, header_h, fill=1, stroke=0)

            c.setStrokeColor(HexColor("#000000"))
            c.setLineWidth(1.0)
            c.rect(table_x, table_bottom, table_w, table_h, fill=0, stroke=1)
            c.line(table_x, table_top - header_h, table_x + table_w, table_top - header_h)
            c.line(split_x, table_bottom, split_x, table_top)

            c.setFillColor(HexColor("#000000"))
            c.setFont("Helvetica-Bold", 9.5)
            c.drawString(table_x + 10, table_top - 14, "Qté")
            c.drawString(table_x + 50, table_top - 14, "Article")
            c.drawString(split_x + 6, table_top - 14, "Prix TTC EURO")

            cur_y = table_top - header_h - 18
            for it in doc.items:
                c.setFillColor(HexColor("#000000"))
                c.setFont("Helvetica", 9.5)
                c.drawString(table_x + 15, cur_y, str(it.quantite))
                c.drawString(table_x + 50, cur_y, str(it.code))
                c.drawRightString(table_x + table_w - 15, cur_y, str(it.prix_ttc))

                cur_y -= 15
                c.setFont("Helvetica-Oblique", 8.5)
                lines = it.designation.split("\n")
                for l in lines:
                    trimmed = l.strip()
                    if trimmed:
                        c.drawString(table_x + 50, cur_y, trimmed)
                        cur_y -= 12
                cur_y -= 10

        if vis.get("middle_totals", True):
            box_h = 85
            box_top = 145
            box_bottom = 60

            b1_x = table_x
            b1_w = 175
            b1_split = b1_x + 100
            b1_hdr_h = 18

            c.setFillColor(HexColor("#F6F6F6"))
            c.rect(b1_x, box_top - b1_hdr_h, b1_w, b1_hdr_h, fill=1, stroke=0)

            c.setStrokeColor(HexColor("#000000"))
            c.setLineWidth(1.0)
            c.rect(b1_x, box_bottom, b1_w, box_h, fill=0, stroke=1)
            c.line(b1_x, box_top - b1_hdr_h, b1_x + b1_w, box_top - b1_hdr_h)
            c.line(b1_split, box_bottom, b1_split, box_top)

            c.setFillColor(HexColor("#000000"))
            c.setFont("Helvetica-Bold", 8.5)
            c.drawString(b1_x + 4, box_top - 13, "Modes de règlement")
            c.drawCentredString(b1_split + (b1_w - 100) / 2, box_top - 13, "EURO")

            c.setFont("Helvetica", 8.5)
            c.drawString(b1_x + 4, 112, str(doc.mode_paiement))
            c.drawRightString(b1_x + b1_w - 10, 112, str(doc.net_a_payer))

            b2_w = 175
            b2_x = table_x + table_w - b2_w
            b2_split = b2_x + 95
            row_h = box_h / 4

            c.setFillColor(HexColor("#F6F6F6"))
            c.rect(b2_x, box_bottom, b2_w, row_h, fill=1, stroke=0)

            c.setStrokeColor(HexColor("#000000"))
            c.setLineWidth(1.0)
            c.rect(b2_x, box_bottom, b2_w, box_h, fill=0, stroke=1)
            c.line(b2_split, box_bottom, b2_split, box_top)

            c.setFillColor(HexColor("#000000"))
            c.setFont("Helvetica", 8.5)

            y1 = box_top - 15
            c.drawString(b2_x + 5, y1, "Hors Taxes")
            c.drawRightString(b2_x + b2_w - 8, y1, str(doc.hors_taxes))

            y2 = box_top - row_h - 15
            c.drawString(b2_x + 5, y2, "Base H.T.")
            c.drawRightString(b2_x + b2_w - 8, y2, str(doc.base_ht))

            y3 = box_top - (row_h * 2) - 15
            c.drawString(b2_x + 5, y3, "TVA 20%")
            c.drawRightString(b2_x + b2_w - 8, y3, str(doc.tva_20))

            y4 = box_bottom + 6
            c.drawString(b2_x + 5, y4, "Net à payer TTC (€)")
            c.drawRightString(b2_x + b2_w - 8, y4, str(doc.net_a_payer))

    c.showPage()
    c.save()
    return out
