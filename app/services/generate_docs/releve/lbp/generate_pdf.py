import pymupdf as fitz
import os
import io
import re
import random
from app.services.generate_docs.releve import generate_transactions
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF

from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
BASE_DIR = CURRENT_DIR.parents[1] / "assets" / "releve"

LOGO_PATH = str(BASE_DIR / "logos" / "logo.svg")
FONT_DIR = str(BASE_DIR / "fonts")

def is_block_enabled(data, block_key, default=True):
    val = data.get(block_key)
    if val is None:
        return default
    if isinstance(val, bool):
        return val
    if isinstance(val, str):
        return val.lower() in ('true', '1', 'on', 'yes')
    return bool(val)

def format_currency_pdf(val):
    val_str = str(val).strip()
    if not val_str.startswith('+') and not val_str.startswith('-'):
        val_str = f"+ {val_str}"
    if "€" not in val_str and "¤" not in val_str:
        val_str = f"{val_str} €"
    return val_str

pdfmetrics.registerFont(TTFont("Unit-MediumTF", os.path.join(FONT_DIR, "Unit-MediumTF.ttf")))
pdfmetrics.registerFont(TTFont("Unit-LightTF", os.path.join(FONT_DIR, "Unit-LightTF.ttf")))
pdfmetrics.registerFont(TTFont("Unit-RegularTF", os.path.join(FONT_DIR, "Unit-RegularTF.ttf")))
pdfmetrics.registerFont(TTFont("Unit-BoldTF", os.path.join(FONT_DIR, "Unit-BoldTF.ttf")))
pdfmetrics.registerFont(TTFont("Unit-MediumTFBold", os.path.join(FONT_DIR, "Unit-MediumTFBold.ttf")))
pdfmetrics.registerFont(TTFont("Unit-RegularTFBold", os.path.join(FONT_DIR, "Unit-RegularTFBold.ttf")))
pdfmetrics.registerFont(TTFont("Unit-BoldTFBold", os.path.join(FONT_DIR, "Unit-BoldTFBold.ttf")))
pdfmetrics.registerFont(TTFont("Unit-RegularTFIta", os.path.join(FONT_DIR, "Unit-RegularTFIta.ttf")))
pdfmetrics.registerFont(TTFont("HE_TERMINAL", os.path.join(FONT_DIR, "HE_TERMINAL.ttf")))
pdfmetrics.registerFont(TTFont("LBP", os.path.join(FONT_DIR, "LBP.ttf")))
pdfmetrics.registerFont(TTFont("LBP_Extra_BoldBold", os.path.join(FONT_DIR, "LBP_Extra_BoldBold.ttf")))
pdfmetrics.registerFontFamily('Unit-LightTF', normal='Unit-LightTF', bold='Unit-BoldTF')
pdfmetrics.registerFontFamily('Unit-RegularTF', normal='Unit-RegularTF', bold='Unit-BoldTF')

CACHED_LOGO = None

def get_cached_logo():
    global CACHED_LOGO
    if CACHED_LOGO is None and os.path.exists(LOGO_PATH):
        CACHED_LOGO = svg2rlg(LOGO_PATH)
    return CACHED_LOGO

def draw_logo(c, page_number=1):
    drawing = get_cached_logo()
    if drawing:
        desired_width = 82.27
        scale_factor = desired_width / drawing.width
        x_pos = 32.78 + 0.2443
        final_height = drawing.height * scale_factor
        y_pos = 840.0 - 13.89 - final_height - 0.0038
        c.saveState()
        c.translate(x_pos, y_pos)
        c.scale(scale_factor, scale_factor)
        renderPDF.draw(drawing, c, 0, 0)
        c.restoreState()

def draw_releve_info_block(c, data, page_number=1):
    if page_number != 1: return
    
    afficher_ccp = data.get("afficher_ccp", True)
    afficher_livret_a = data.get("afficher_livret_a", False)
    afficher_epargne = data.get("afficher_epargne", False)
    
    nb_comptes = sum([afficher_ccp, afficher_livret_a, afficher_epargne])
    if nb_comptes == 1:
        if afficher_ccp:
            titre_prefix = "Relevé de votre Compte Courant Postal"
        elif afficher_livret_a:
            nom = data.get("livret_a_nom")
            titre_prefix = f"Relevé de votre {nom.strip() if nom else 'Livret A'}"
        elif afficher_epargne:
            nom = data.get("epargne_nom")
            titre_prefix = f"Relevé de votre {nom.strip() if nom else 'Compte Épargne Logement'}"
    else:
        titre_prefix = "Relevé de vos comptes"
    
    num_releve = data.get("num_releve", "1")
    date_edition = data.get("date_edition", "03 février 2025")
    
    c.setFont("Unit-MediumTF", 16.01)
    c.setFillColorRGB(25/255.0, 55/255.0, 105/255.0)
    c.drawString(42.51, 840.0 - 99.01, f"{titre_prefix} - n° {num_releve} ")
    
    c.setFont("Unit-RegularTF", 11.01)
    c.setFillColorRGB(0, 0, 0)
    c.drawString(42.51, 840.0 - 111.98, ">  Périodicité mensuelle ")
    
    c.setFont("Unit-MediumTF", 9.01)
    text_statique = "Relevé édité le "
    width_statique = pdfmetrics.stringWidth(text_statique, "Unit-MediumTF", 9.01)
    c.drawString(419.86, 840.0 - 93.0, text_statique)
    
    c.setFont("Unit-RegularTF", 9.01)
    c.drawString(419.86 + width_statique, 840.0 - 93.0, date_edition)

def draw_contacts_block(c, data, page_number=1):
    if page_number != 1: return
    identifiant = data.get("identifiant", "1455835203")
    
    c.setLineWidth(0.24)
    c.setStrokeColorRGB(0, 0, 0)
    c.line(87.91, 840.0 - 127.11, 87.91, 840.0 - 172.51)
    c.line(87.91, 840.0 - 178.27, 87.91, 840.0 - 221.51)
    c.line(87.91, 840.0 - 227.27, 87.91, 840.0 - 251.77)
    
    c.setFont("Unit-MediumTFBold", 9.01)
    c.setFillColorRGB(25/255.0, 55/255.0, 105/255.0)
    c.drawString(45.4, 840.0 - 141.76, "Vos")
    c.drawString(45.4, 840.0 - 153.05, "Comptes")
    c.drawString(45.4, 840.0 - 164.1, "24h/24")
    
    c.setFont("Unit-MediumTF", 9.01)
    c.setFillColorRGB(0, 0, 0)
    c.drawString(90.79, 840.0 - 136.72, f"Votre identifiant : {identifiant}")
    c.drawString(90.79, 840.0 - 147.53, "> www.labanquepostale.fr")
    c.drawString(90.79, 840.0 - 158.34, "> Application La Banque Postale")
    
    def draw_superscript(x, y, text):
        c.setFont("Unit-MediumTF", 9.01)
        c.drawString(x, y, text)
        w = pdfmetrics.stringWidth(text, "Unit-MediumTF", 9.01)
        c.setFont("Unit-MediumTF", 7.01)
        c.drawString(x + w, y + (9.01 - 7.01), "(1)")

    draw_superscript(90.79, 840.0 - 169.14, "> Serveur vocal : 09 69 39 36 39")
    
    c.setFont("Unit-MediumTFBold", 9.01)
    c.setFillColorRGB(25/255.0, 55/255.0, 105/255.0)
    c.drawString(45.4, 840.0 - 192.2, "Votre")
    c.drawString(45.4, 840.0 - 203.01, "Service")
    c.drawString(45.4, 840.0 - 213.82, "Clients")
    
    c.setFillColorRGB(0, 0, 0)
    draw_superscript(90.79, 840.0 - 186.92, "> Téléphone : 3639")
    
    c.setFont("Unit-MediumTF", 9.01)
    c.drawString(90.79, 840.0 - 197.73, "> Messagerie depuis votre Espace Client")
    c.drawString(90.79, 840.0 - 208.54, "> Courrier : ")
    
    centre_fin = data.get("centre_financier") or "PARIS CENTRE FINANCIER"
    c.drawString(140.27, 840.0 - 208.54, "LA BANQUE POSTALE")
    c.drawString(140.27, 840.0 - 219.34, centre_fin)
    
    c.setFont("Unit-MediumTFBold", 9.01)
    c.setFillColorRGB(25/255.0, 55/255.0, 105/255.0)
    c.drawString(45.4, 840.0 - 236.88, "Votre")
    c.drawString(45.4, 840.0 - 247.93, "conseiller")
    
    c.setFont("Unit-MediumTF", 9.01)
    c.setFillColorRGB(0, 0, 0)
    c.drawString(90.79, 840.0 - 236.88, "Prendre un rendez-vous")
    
    draw_superscript(90.79, 840.0 - 247.93, "> Téléphone : 3639")
    
    c.setFont("Unit-MediumTF", 7.01)
    c.drawString(45.4, 840.0 - 264.26, "(1) Service gratuit + prix appel.")

def draw_titulaire_block(c, data, page_number=1):
    if page_number != 1: return
    
    nom = data.get("titulaire_nom_complet", "MR MARTIN LUCAS")
    
    lignes = [nom]
    
    # Ordre: 2. Complement (Chez, Batiment), 3. Voie (Rue), 4. CP Ville
    adr_comp = (data.get("titulaire_adresse1") or "").strip()
    if adr_comp: lignes.append(adr_comp)
    
    adr_voie = (data.get("titulaire_adresse2") or "31 RUE JEAN JAURES").strip()
    if adr_voie: lignes.append(adr_voie)
        
    cp_ville = data.get("titulaire_cp_ville", "31000 TOULOUSE").strip()
    if cp_ville: lignes.append(cp_ville)
    
    c.setFont("HE_TERMINAL", 9.01)
    c.setFillColorRGB(0, 0, 0)
    
    y_current = 205.65
    max_width = 223.0 # Limite sécurisée avant le bord droit de la page
    
    # Calcul mathématique de la limite de caractères (police à chasse fixe)
    char_width = pdfmetrics.stringWidth("A", "HE_TERMINAL", 9.01)
    max_chars = int(max_width / char_width) if char_width > 0 else 38
    
    for ligne in lignes[:4]:
        # Normalisation stricte : majuscules et espaces propres
        ligne_propre = " ".join(ligne.upper().split())
        
        # Troncature instantanée sans boucle
        if len(ligne_propre) > max_chars:
            ligne_propre = ligne_propre[:max_chars].strip()
            
        c.drawString(312.01, 840.0 - y_current, ligne_propre)
        y_current += 8.41


# ------------------
# ENCAPSULATION DES ZONES
# ------------------
def draw_small_header_block(c, data, page_number):
    if page_number <= 1: return
    
    numero = data.get("num_releve", "1")
    date_raw = str(data.get("date_edition_raw", "2025-02-03"))
    
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", date_raw)
    if m:
        date_chiffres = f"{m.group(3)}/{m.group(2)}/{m.group(1)}"
    else:
        date_chiffres = date_raw
    
    ligne1 = f"Relevé n° {numero} | {date_chiffres}"
    ligne2 = data.get("titulaire_nom_complet", "MR MARTIN LUCAS")
    
    c.setFont("Unit-RegularTF", 8.01)
    c.setFillColorRGB(0, 0, 0)
    
    x_right = 535.45
    c.drawRightString(x_right, 740.51, ligne1)
    c.drawRightString(x_right, 731.14, ligne2)

def draw_header(c, data, page_number):
    if is_block_enabled(data, "show_logo"):
        draw_logo(c, page_number)
    if is_block_enabled(data, "show_releve_info"):
        draw_releve_info_block(c, data, page_number)
    if is_block_enabled(data, "show_contacts"):
        draw_contacts_block(c, data, page_number)
    if is_block_enabled(data, "show_titulaire"):
        draw_titulaire_block(c, data, page_number)
    if is_block_enabled(data, "show_small_header"):
        draw_small_header_block(c, data, page_number)


def draw_situation_title(c, data, y_pos):
    c.setFillColorRGB(25/255, 55/255, 105/255)
    c.setStrokeColorRGB(25/255, 55/255, 105/255)
    c.setLineWidth(0.24)
    c.rect(42.51, y_pos, 4.33, 12.73, fill=1, stroke=1)
    c.setFont("Unit-MediumTF", 15.01)
    c.drawString(55.96, y_pos, "Situation de vos comptes")
    
    w_titre = pdfmetrics.stringWidth("Situation de vos comptes ", "Unit-MediumTF", 15.01)
    c.setFont("Unit-RegularTF", 11.01)
    c.setFillColorRGB(0, 0, 0)
    date_sit = data.get("date_situation", "1 juillet 2026")
    c.drawString(55.96 + w_titre, y_pos, f"au {date_sit}")
    
    c.setFont("Unit-MediumTF", 8.01)
    c.drawRightString(535.45, y_pos - 0.96, "Solde")
    
    y_pos -= 5.77
    c.setLineWidth(0.48)
    c.setStrokeColorRGB(0.0, 0.0, 0.0)
    c.line(55.96, y_pos, 535.45, y_pos)
    return y_pos

def draw_account_row(c, nom_compte, numero, solde_val, y_pos, is_last=False):
    y_pos -= 10.57
    
    c.setFont("Unit-MediumTF", 11.01)
    c.setFillColorRGB(25/255, 55/255, 105/255)
    nom_format = nom_compte + " "
    c.drawString(55.96, y_pos, nom_format)
    
    w_nom = pdfmetrics.stringWidth(nom_format, "Unit-MediumTF", 11.01)
    c.setFont("Unit-MediumTF", 11.01)
    c.setFillColorRGB(0, 0, 0)
    c.drawString(55.96 + w_nom, y_pos, "n° ")
    
    w_no = pdfmetrics.stringWidth("n° ", "Unit-MediumTF", 11.01)
    c.setFont("Unit-RegularTF", 10.01)
    c.drawString(55.96 + w_nom + w_no, y_pos, f"{numero}")
    
    c.setFont("Unit-BoldTF", 10.51)
    c.setFillColorRGB(25/255, 55/255, 105/255)
    solde_val = format_currency_pdf(solde_val)
    c.drawRightString(535.45, y_pos, solde_val)
    
    y_pos -= 6.48
    c.setLineWidth(0.24)
    c.setStrokeColorRGB(0.0, 0.0, 0.0)
    c.line(55.96, y_pos, 535.45, y_pos)
        
    return y_pos

def draw_ccp(c, data, y_pos, is_last=False):
    return draw_account_row(c, data.get('ccp_nom', 'Compte Courant Postal'), data.get('ccp_numero', '14 529 34 L 025'), data.get('ccp_solde', '+  22 988,48'), y_pos, is_last)

def draw_livret_a(c, data, y_pos, is_last=False):
    return draw_account_row(c, data.get('livret_a_nom', 'Livret A'), data.get('livret_a_numero', '210 5436798 J'), data.get('livret_a_solde', '+  10 574,15'), y_pos, is_last)

def draw_epargne(c, data, y_pos, is_last=False):
    return draw_account_row(c, data.get('epargne_nom', 'Compte Épargne Logement'), data.get('epargne_numero', '340 9123847 K'), data.get('epargne_solde', '+  15 242,92'), y_pos, is_last)

def draw_single_account_situation(c, data, y_pos_in, cpt_type):
    if cpt_type == "CCP":
        nom = data.get("ccp_nom", "Compte Courant Postal")
        numero = data.get("ccp_numero", "14 529 34 L 025")
        default_iban = data.get("ccp_iban", "FR76 2004 1000 0114 5293 4L02 522")
        default_bic = data.get("ccp_bic", "PSSTFRPPPAR")
        solde = data.get("ccp_solde", "+ 22 988,48 ¤")
    elif cpt_type == "LIVRET_A":
        nom = data.get("livret_a_nom", "Livret A")
        numero = data.get("livret_a_numero", "210 5436798 J")
        default_iban = data.get("livret_a_iban", "FR76 1001 1000 2021 0543 6798 J51")
        default_bic = data.get("livret_a_bic", "PSSTFRPPCNE")
        solde = data.get("livret_a_solde", "+ 10 574,15 ¤")
    elif cpt_type == "EPARGNE":
        nom = data.get("epargne_nom", "Compte Épargne Logement")
        numero = data.get("epargne_numero", "340 9123847 K")
        default_iban = data.get("epargne_iban", "FR76 1001 1000 2034 0912 3847 K38")
        default_bic = data.get("epargne_bic", "PSSTFRPPCNE")
        solde = data.get("epargne_solde", "+ 15 242,92 ¤")
    else:
        nom = "Compte"
        numero = "14 529 34 L 025"
        default_iban = "FR76 2004 1000 0114 5293 4L02 522"
        default_bic = "PSSTFRPPPAR"
        solde = "+ 0,82 ¤"

    solde = format_currency_pdf(solde)
    titre_text = f" Situation de votre {nom} "
    
    y_title = y_pos_in - 8.42
    
    c.setFillColorRGB(25/255, 55/255, 105/255)
    c.setStrokeColorRGB(25/255, 55/255, 105/255)
    c.setLineWidth(0.24)
    c.rect(42.51, y_title, 4.33, 12.74, fill=1, stroke=1)
    
    c.setFont("Unit-MediumTF", 15.01)
    c.drawString(46.84, y_title, titre_text)
    
    w_titre = pdfmetrics.stringWidth(titre_text, "Unit-MediumTF", 15.01)
    c.setFont("Unit-RegularTF", 11.01)
    c.setFillColorRGB(0, 0, 0)
    c.drawString(46.84 + w_titre, y_title, f"n° {numero}")
    
    c.setFont("Unit-LightTF", 8.01)
    c.setFillColorRGB(0, 0, 0)
    raw_iban = str(default_iban).replace(" ", "")
    iban_str = " ".join(raw_iban[i:i+4] for i in range(0, len(raw_iban), 4))
    bic_str = str(default_bic).strip().upper()
    c.drawString(53.08, y_title - 12.97, f"IBAN : {iban_str}  |  BIC : {bic_str}")
    
    c.setLineWidth(0.24)
    c.setStrokeColorRGB(0.0, 0.0, 0.0)
    c.line(47.32, y_title - 18.73, 538.99, y_title - 18.73)
    
    c.setFont("Unit-MediumTF", 11.01)
    c.setFillColorRGB(25/255, 55/255, 105/255)
    c.drawString(53.08, y_title - 34.10, "Votre solde au ")
    w_vs = pdfmetrics.stringWidth("Votre solde au ", "Unit-MediumTF", 11.01)
    
    c.setFont("Unit-MediumTF", 10.01)
    date_sit = data.get("date_releve", "13/05/2025")
    c.drawString(53.08 + w_vs, y_title - 34.10, date_sit)
    
    c.setFont("Unit-MediumTF", 11.01)
    c.drawRightString(535.45, y_title - 34.10, solde)
    
    c.line(47.32, y_title - 41.79, 538.99, y_title - 41.79)
    
    return y_title - 41.79

def draw_middle(c, data, page_number):
    if page_number != 1:
        return 800
        
    has_carbo = data.get("has_carbo_resolved", False)
    if has_carbo:
        draw_annexe_carbo(c, 279.47)
        y_pos = 487.99
    else:
        y_pos = 552.45
        
    if not is_block_enabled(data, "show_middle", True):
        return y_pos
        
    if data.get("mode") == "blocks":
        rows_to_draw = []
        if is_block_enabled(data, "show_situation_ccp", False):
            rows_to_draw.append("CCP")
        if is_block_enabled(data, "show_situation_livret_a", False):
            rows_to_draw.append("LIVRET_A")
        if is_block_enabled(data, "show_situation_epargne", False):
            rows_to_draw.append("EPARGNE")
            
        show_title = is_block_enabled(data, "show_situation_title", False)
        
        if len(rows_to_draw) == 1:
            y_pos = draw_single_account_situation(c, data, y_pos, rows_to_draw[0])
            return y_pos - 56.68
        elif len(rows_to_draw) > 1:
            y_pos = draw_situation_title(c, data, y_pos)
            for i, cpt_type in enumerate(rows_to_draw):
                is_last = (i == len(rows_to_draw) - 1)
                if cpt_type == "CCP":
                    y_pos = draw_ccp(c, data, y_pos, is_last)
                elif cpt_type == "LIVRET_A":
                    y_pos = draw_livret_a(c, data, y_pos, is_last)
                elif cpt_type == "EPARGNE":
                    y_pos = draw_epargne(c, data, y_pos, is_last)
            return y_pos - 46.36
        elif show_title:
            y_pos = draw_situation_title(c, data, y_pos)
            return y_pos - 46.36
        else:
            return y_pos
    else:
        afficher_ccp = data.get("afficher_ccp", True)
        comptes_ep_list = data.get("comptes_epargne_list") or []
        
        account_rows = []
        if afficher_ccp:
            account_rows.append({
                "type": "CCP",
                "nom": data.get('ccp_nom', 'Compte Courant Postal'),
                "num": data.get('ccp_numero', data.get('ccp_account_num', '14 529 34 L 025')),
                "solde": data.get('ccp_solde', '+  0,00 ¤')
            })
            
        if comptes_ep_list:
            for ep in comptes_ep_list:
                account_rows.append({
                    "type": "EPARGNE",
                    "nom": ep.get("name", "Livret d'Épargne"),
                    "num": ep.get("num", "210 5436798 J"),
                    "solde": ep.get("solde_nouv", ep.get("solde", "+ 0,00 ¤"))
                })
        else:
            if data.get("afficher_livret_a"):
                account_rows.append({
                    "type": "LIVRET_A",
                    "nom": data.get('livret_a_nom', 'Livret A'),
                    "num": data.get('livret_a_numero', '210 5436798 J'),
                    "solde": data.get('livret_a_solde', '+  10 574,15 ¤')
                })
            if data.get("afficher_epargne"):
                account_rows.append({
                    "type": "EPARGNE",
                    "nom": data.get('epargne_nom', 'Compte Épargne Logement'),
                    "num": data.get('epargne_numero', '340 9123847 K'),
                    "solde": data.get('epargne_solde', '+  15 242,92 ¤')
                })
        
        if not account_rows:
            return y_pos
            
        if len(account_rows) == 1:
            y_pos = draw_single_account_situation(c, data, y_pos, account_rows[0]["type"])
            return y_pos - 56.68
        else:
            y_pos = draw_situation_title(c, data, y_pos)
            for i, row in enumerate(account_rows):
                is_last = (i == len(account_rows) - 1)
                y_pos = draw_account_row(c, row["nom"], row["num"], row["solde"], y_pos, is_last)
            return y_pos - 46.36

def draw_mentions_legales(c, data, page_number, total_pages):
    if page_number != 1: return
    
    c.setFont("LBP", 8.01)
    c.setFillColorRGB(0, 0, 0)
    
    t1 = c.beginText(42.51, 840.0 - 786.92)
    t1.setCharSpace(-0.0505)
    t1.textLine("LA BANQUE POSTALE - S.A. à Directoire et Conseil de Surveillance. Capital social 6 585 350 218 ¤. 115 rue de Sèvres 75275 Paris CEDEX 06. RCS Paris ")
    c.drawText(t1)
    
    t2 = c.beginText(42.51, 840.0 - 797.25)
    t2.setCharSpace(-0.0505)  # On applique la même micro-compression pour cohérence
    t2.textLine("n°421 100 645. IDU EMP FR231771_01UJPN. ORIAS n° 07 023 424.")
    c.drawText(t2)

def draw_conseil_conservation(c, data, page_number, total_pages):
    if page_number != total_pages or total_pages < 2: return
    c.setFont("Unit-RegularTF", 8.01)
    c.setFillColorRGB(0, 0, 0)
    c.drawString(42.51, 840.0 - 789.56, "Il vous est conseillé de conserver ce relevé.")

def draw_pagination(c, data, page_number, total_pages=1):
    c.setFillColorRGB(0, 0, 0)
    
    # Position Y dynamique
    y_pos = 789.56 if (page_number == total_pages and total_pages > 1) else 810.22
    
    # Limite droite stricte
    x_right = 535.45
    
    # Texte de la pagination
    text_num = f"{page_number}/{total_pages}"
    text_page = "Page "
    
    # On écrit de DROITE A GAUCHE pour garantir que la limite est toujours respectée
    c.setFont("Unit-BoldTF", 10.01)
    c.drawRightString(x_right, 840.0 - y_pos, text_num)
    
    w_num = pdfmetrics.stringWidth(text_num, "Unit-BoldTF", 10.01)
    
    c.setFont("Unit-RegularTF", 10.01)
    c.drawRightString(x_right - w_num, 840.0 - y_pos, text_page)

def draw_footer(c, data, page_number, total_pages=1):
    if is_block_enabled(data, "show_mentions_legales"):
        draw_mentions_legales(c, data, page_number, total_pages)
    if is_block_enabled(data, "show_conseil_conservation"):
        draw_conseil_conservation(c, data, page_number, total_pages)
    if is_block_enabled(data, "show_pagination"):
        draw_pagination(c, data, page_number, total_pages)

def format_tx_amount(amt):
    if not amt: return ""
    val_clean = str(amt).replace('€', '').replace('¤', '').replace('+', '').replace('-', '').replace(' ', '').replace(',', '.')
    try:
        f = abs(float(val_clean))
        return f"{f:,.2f}".replace(',', ' ').replace('.', ',')
    except:
        return str(amt)

def draw_table_headers(c, y_topdown, is_epargne=False):
    c.setFont("Unit-MediumTF", 8.01)
    c.setFillColorRGB(0, 0, 0)
    c.setLineWidth(0.24)
    c.setStrokeColorRGB(0.0, 0.0, 0.0)
    
    if is_epargne:
        c.drawString(52.60, 840.0 - y_topdown, "Date")
        c.drawString(84.79, 840.0 - y_topdown, "Opérations")
        c.drawString(433.55, 840.0 - y_topdown, "Débit (€)")
        c.drawString(506.56, 840.0 - y_topdown, "Crédit (€)")
        
        y_line = (840.0 - y_topdown) - 4.81
        c.line(52.60, y_line, 81.18, y_line)
        c.line(84.79, y_line, 396.80, y_line)
        c.line(402.56, y_line, 467.89, y_line)
        c.line(473.66, y_line, 538.99, y_line)
    else:
        c.drawString(53.56, 840.0 - y_topdown, "Date")
        c.drawString(85.99, 840.0 - y_topdown, "Opérations")
        c.drawString(433.55, 840.0 - y_topdown, "Débit (€)")
        c.drawString(506.56, 840.0 - y_topdown, "Crédit (€)")
        
        y_line = (840.0 - y_topdown) - 4.80
        c.line(53.56, y_line, 80.22, y_line)
        c.line(85.99, y_line, 392.95, y_line)
        c.line(398.72, y_line, 463.57, y_line)
        c.line(469.34, y_line, 539.23, y_line)

def format_solde_number(amount_str):
    clean = str(amount_str).replace('€', '').replace('¤', '').replace('+', '').strip()
    return clean

def draw_solde_line(c, label, amount_str, y_topdown, is_nouveau=False, has_total_before=False, is_epargne=False):
    c.setFont("Unit-BoldTF", 10.01)
    c.setFillColorRGB(25/255.0, 55/255.0, 105/255.0)
    c.drawRightString(392.23 if is_epargne else 392.71, 840.0 - y_topdown, label)
    
    c.setFont("Unit-BoldTF", 11.01 if not is_nouveau else 10.01)
    c.setFillColorRGB(25/255.0, 55/255.0, 105/255.0)
    amt_text = format_solde_number(amount_str)
    c.drawRightString(538.99 if is_epargne else 539.23, 840.0 - y_topdown, amt_text)
    
    c.setStrokeColorRGB(0.0, 0.0, 0.0)
    if is_nouveau:
        if not has_total_before:
            c.setLineWidth(0.24)
            y_line = (840.0 - y_topdown) + 13.21
            c.line(174.14, y_line, 538.99 if is_epargne else 539.23, y_line)
    else:
        y_line = (840.0 - y_topdown) - 8.16
        if is_epargne:
            c.setLineWidth(0.48)
            c.line(84.79, y_line, 396.80, y_line)
            c.line(402.56, y_line, 467.89, y_line)
            c.line(473.66, y_line, 538.99, y_line)
        else:
            c.setLineWidth(0.24)
            c.line(85.99, y_line, 392.95, y_line)
            c.line(398.72, y_line, 463.57, y_line)
            c.line(469.34, y_line, 539.23, y_line)

def draw_total_operations_line(c, total_debit_str, total_credit_str, y_topdown, is_epargne=False):
    c.setFont("Unit-MediumTF", 10.01)
    c.setFillColorRGB(0, 0, 0)
    c.drawRightString(392.23 if is_epargne else 392.71, 840.0 - y_topdown, "Total des opérations")
    
    if total_debit_str:
        amt_d = format_solde_number(total_debit_str)
        c.drawRightString(467.89 if is_epargne else 463.57, 840.0 - y_topdown, amt_d)
    if total_credit_str:
        amt_c = format_solde_number(total_credit_str)
        c.drawRightString(538.99 if is_epargne else 539.23, 840.0 - y_topdown, amt_c)
        
    y_line = (840.0 - y_topdown) - 9.85
    c.setLineWidth(0.24)
    c.setStrokeColorRGB(0.0, 0.0, 0.0)
    c.line(174.14 if is_epargne else 176.78, y_line, 538.99 if is_epargne else 539.23, y_line)

def get_tx_lines(tx):
    if "lignes" in tx and tx["lignes"]:
        title = str(tx["lignes"][0])
        sublines = [str(l) for l in tx["lignes"][1:]]
    else:
        title = str(tx.get("title", tx.get("label", "")))
        sublines = [str(s) for s in tx.get("sublines", [])]
    return title, sublines

def get_tx_height(tx):
    title, sublines = get_tx_lines(tx)
    if not sublines:
        return 13.88
    if len(sublines) == 1:
        return 20.66
    return 20.66 + 9.37 * (len(sublines) - 1)

def draw_transaction_lines(c, tx, y_topdown, is_before_total=False, is_before_nouveau=False, is_epargne=False):
    title, sublines = get_tx_lines(tx)
    c.setFont("Unit-RegularTF", 9.01)
    c.setFillColorRGB(0, 0, 0)
    
    date_str = tx.get("date", "")
    if date_str:
        if "-" in date_str:
            parts = date_str.split("-")
            if len(parts) >= 3:
                date_str = f"{int(parts[2]):02d}/{int(parts[1]):02d}"
        elif "/" in date_str:
            parts = date_str.split("/")
            if len(parts) >= 2:
                try:
                    date_str = f"{int(parts[0]):02d}/{int(parts[1]):02d}"
                except ValueError:
                    pass
        c.drawString(52.60 if is_epargne else 53.56, 840.0 - y_topdown, date_str)
        
    y_rl = 840.0 - y_topdown
    
    is_frais = tx.get("is_frais", False) or tx.get("has_arrow", False)
    if not is_frais and not is_epargne:
        title_upper = title.upper()
        fee_patterns = ["COTISATION TRIMESTRIELLE", "COTISATION MENSUELLE", "MINIMUM FORFAITAIRE", "FRAIS OPERATIONS PARTICULIERES", "FRAIS IRREGULARITES", "FRAIS DE REJET", "COMMISSION D INTERVENTION"]
        if any(pat in title_upper for pat in fee_patterns):
            is_frais = True
            
    if is_frais and not is_epargne:
        c.saveState()
        c.setFillColorRGB(0.0, 0.0, 0.0)
        c.setStrokeColorRGB(0.0, 0.0, 0.0)
        c.setLineWidth(0.2402)
        c.setLineJoin(0)
        c.setLineCap(0)
        arrow_path = c.beginPath()
        arrow_path.moveTo(80.22, y_rl + 0.24)
        arrow_path.lineTo(80.22, y_rl + 4.80)
        arrow_path.lineTo(83.83, y_rl + 2.16)
        arrow_path.close()
        c.drawPath(arrow_path, fill=1, stroke=1)
        c.restoreState()
        
    c.drawString(84.79 if is_epargne else 85.99, y_rl, title)
    
    debit = ""
    credit = ""
    
    if tx.get("debit"):
        debit = format_tx_amount(tx["debit"])
    elif tx.get("credit"):
        credit = format_tx_amount(tx["credit"])
    else:
        signe = tx.get("signe", "+")
        raw_val = tx.get("montant") if tx.get("montant") is not None else tx.get("amount")
        if raw_val is not None:
            val_clean = str(raw_val).replace('EUR', '').replace('€', '').replace('¤', '').replace(' ', '').replace(',', '.')
            try:
                numeric_val = float(val_clean)
                if numeric_val < 0 or signe == "-":
                    debit = format_tx_amount(abs(numeric_val))
                else:
                    credit = format_tx_amount(abs(numeric_val))
            except ValueError:
                pass
            
    if debit:
        c.drawRightString(467.89 if is_epargne else 463.57, 840.0 - y_topdown, debit)
    elif credit:
        c.drawRightString(538.99 if is_epargne else 539.23, 840.0 - y_topdown, credit)
        
    curr_y = y_topdown
    for i, sub in enumerate(sublines):
        if i == 0:
            curr_y += 9.61
        else:
            curr_y += 9.37
        c.setFont("Unit-LightTF", 8.01)
        c.setFillColorRGB(0, 0, 0)
        c.drawString(84.79 if is_epargne else 85.99, 840.0 - curr_y, sub)
        
    if sublines:
        y_line = (840.0 - curr_y) - 2.16
    else:
        y_line = (840.0 - y_topdown) - 4.80
        
    c.setLineWidth(0.24)
    c.setStrokeColorRGB(0.0, 0.0, 0.0)
    if is_before_nouveau:
        pass
    elif is_before_total:
        c.line(402.56 if is_epargne else 398.72, y_line, 467.89 if is_epargne else 463.57, y_line)
        c.line(473.66 if is_epargne else 469.34, y_line, 538.99 if is_epargne else 539.23, y_line)
    else:
        c.line(84.79 if is_epargne else 85.99, y_line, 396.80 if is_epargne else 392.95, y_line)
        c.line(402.56 if is_epargne else 398.72, y_line, 467.89 if is_epargne else 463.57, y_line)
        c.line(473.66 if is_epargne else 469.34, y_line, 538.99 if is_epargne else 539.23, y_line)
    
    if not sublines:
        return y_topdown + 13.88
    elif len(sublines) == 1:
        return y_topdown + 20.66
    else:
        return y_topdown + 20.66 + 9.37 * (len(sublines) - 1)

def get_ancien_solde_date(data):
    mois = data.get("releve_mois_int", 1)
    annee = data.get("releve_annee_int", 2025)
    return f"01/{mois:02d}/{annee}"

def draw_suite_header(c, account_name, account_num):
    c.setFont("Unit-RegularTF", 11.01)
    c.setFillColorRGB(25/255.0, 55/255.0, 105/255.0)
    title = f"Vos opérations {account_name} "
    c.drawString(53.56, 840.0 - 143.04, title)
    w = pdfmetrics.stringWidth(title, "Unit-RegularTF", 11.01)
    c.setFillColorRGB(0, 0, 0)
    if account_num:
        c.drawString(53.56 + w, 840.0 - 143.04, f"n° {account_num} (suite)")
    else:
        c.drawString(53.56 + w, 840.0 - 143.04, "(suite)")

def draw_account_header(c, account_name, account_num, iban, bic, y_topdown, data=None):
    c.setFillColorRGB(25/255.0, 55/255.0, 105/255.0)
    c.rect(42.51, (840.0 - y_topdown) - 0.24, 4.33, 12.73, fill=1, stroke=0)
    
    c.setFont("Unit-MediumTF", 15.01)
    c.drawString(53.56, 840.0 - y_topdown, account_name + " ")
    
    w_nom = pdfmetrics.stringWidth(account_name + " ", "Unit-MediumTF", 15.01)
    c.setFont("Unit-RegularTF", 11.01)
    c.setFillColorRGB(0, 0, 0)
    c.drawString(53.56 + w_nom, 840.0 - y_topdown, f"n° {account_num}")
    
    y_topdown += 12.01
    c.setFont("Unit-LightTF", 8.01)
    c.setFillColorRGB(0, 0, 0)
    raw_iban = str(iban).replace(" ", "")
    iban_str = " ".join(raw_iban[i:i+4] for i in range(0, len(raw_iban), 4))
    c.drawString(53.56, 840.0 - y_topdown, f"IBAN : {iban_str}  |  BIC : {bic}")
    
    is_etudiant = ((data.get("profil_transactions") == "etudiant") or (data.get("age_profile") == "jeune")) if data else False
    has_decouvert = is_block_enabled(data, "show_tx_decouvert_ccp", default=(not is_etudiant)) if data else True
    
    if has_decouvert and data:
        date_releve = data.get("date_releve", "31/01/2025")
        decouvert_amt = data.get("ccp_decouvert_autorise", "200,00")
        
        y_topdown += 10.08
        c.setFont("Unit-RegularTF", 9.01)
        c.setFillColorRGB(0, 0, 0)
        t_dec1 = f"> Découvert autorisé au {date_releve} : {decouvert_amt} € "
        c.drawString(53.56, 840.0 - y_topdown, t_dec1)
        w_dec1 = pdfmetrics.stringWidth(t_dec1, "Unit-RegularTF", 9.01)
        
        c.setFont("Unit-RegularTF", 8.01)
        c.drawString(53.56 + w_dec1, 840.0 - y_topdown, "(à régulariser sous 30 jours). Pour information, l'utilisation d'un découvert de 1 500,00 € ")
        
        y_topdown += 9.85
        c.drawString(53.56, 840.0 - y_topdown, "pendant une durée de 30 jours avec un taux nominal annuel de 16,00 % correspond à un TAEG de 18,79 % (1). L'utilisation d'un découvert de")
        
        y_topdown += 9.61
        c.drawString(53.56, 840.0 - y_topdown, "1 500,00 € pendant une durée de 30 jours avec un taux nominal annuel de 15,00 % correspond à un TAEG de 17,60 % (1).")
        
        y_topdown += 9.61
        c.drawString(53.56, 840.0 - y_topdown, "(1) Le TAEG réellement appliqué dépend de l’utilisation effective du découvert.")
        
        y_topdown += 10.08
        c.setFont("Unit-RegularTF", 9.01)
        c.drawString(53.56, 840.0 - y_topdown, "> Avantage FORMULE DE COMPTE : jusqu'à 3,00 € par trimestre, vos intérêts débiteurs ne vous sont pas facturés.")
        
        y_topdown += 9.84
        c.setFont("Unit-RegularTF", 8.01)
        c.drawString(57.17, 840.0 - y_topdown, "(Seuil en vigueur au 01/07/2010)")
        
        return y_topdown + 23.93
        
    return y_topdown + 22.0

def draw_epargne_main_header(c, y_topdown):
    c.setFillColorRGB(25/255.0, 55/255.0, 105/255.0)
    c.rect(42.51, (840.0 - y_topdown) - 0.24, 4.33, 12.73, fill=1, stroke=0)
    c.setFont("Unit-MediumTF", 15.01)
    c.drawString(52.60, 840.0 - y_topdown, "Comptes d'Épargne")
    return y_topdown + 15.13

def draw_epargne_subheader(c, account_name, account_num, iban, bic, y_topdown):
    c.setFillColorRGB(25/255.0, 55/255.0, 105/255.0)
    c.setStrokeColorRGB(25/255.0, 55/255.0, 105/255.0)
    c.setLineWidth(0.24)
    c.rect(52.60, (840.0 - y_topdown) + 2.17, 4.33, 4.32, fill=1, stroke=1)
    
    c.setFont("Unit-MediumTF", 12.01)
    c.setFillColorRGB(25/255.0, 55/255.0, 105/255.0)
    c.drawString(66.05, 840.0 - y_topdown, account_name + " ")
    w_nom = pdfmetrics.stringWidth(account_name + " ", "Unit-MediumTF", 12.01)
    
    c.setFont("Unit-RegularTF", 11.01)
    c.setFillColorRGB(0, 0, 0)
    c.drawString(66.05 + w_nom, 840.0 - y_topdown, "n° ")
    w_no = pdfmetrics.stringWidth("n° ", "Unit-RegularTF", 11.01)
    
    c.drawString(66.05 + w_nom + w_no, 840.0 - y_topdown, account_num)
    
    y_topdown += 12.25
    c.setFont("Unit-LightTF", 8.01)
    c.setFillColorRGB(0, 0, 0)
    raw_iban = str(iban).replace(" ", "")
    iban_str = " ".join(raw_iban[i:i+4] for i in range(0, len(raw_iban), 4))
    c.drawString(66.05, 840.0 - y_topdown, f"IBAN : {iban_str}  |  BIC : {bic}")
    return y_topdown + 26.66

def draw_annexe_fgdr_legal(c, y_topdown):
    c.setFillColorRGB(25/255.0, 55/255.0, 105/255.0)
    
    lines = [
        [
            ("LBP_Extra_BoldBold", "Pour faire opposition en cas de perte ou vol de vos Moyens de paiement : Sur vos cartes"),
            ("Unit-LightTF", " (24h/24, 7J/7) via l'Espace Client Internet, l'application mobile ou au")
        ],
        [
            ("Unit-LightTF", "3639 (Service gratuit + prix appel)."),
            ("LBP_Extra_BoldBold", " Sur vos chèques"),
            ("Unit-LightTF", " au 3639 (Service gratuit + prix appel)."),
            ("LBP_Extra_BoldBold", " Pour bloquer les virements digitaux en cas de virements frauduleux")
        ],
        [
            ("LBP_Extra_BoldBold", "constatés sur votre compte :"),
            ("Unit-LightTF", " Rendez-vous sur l'Espace Client Internet (24h/24, 7j/7) pour modifier votre mot de passe ou sur le site labanquepostale.fr pour lancer la")
        ],
        [
            ("Unit-LightTF", "procédure de réinitialisation du mot de passe. Vous pouvez également contacter notre Service Clients au 3639 (Service gratuit + prix appel)."),
            ("LBP_Extra_BoldBold", " Besoin d'une information")
        ],
        [
            ("LBP_Extra_BoldBold", "sur la bonne exécution de votre Contrat ou de déposer une réclamation ?"),
            ("Unit-LightTF", " Contactez-nous via votre messagerie sécurisée (BEL/APP), votre bureau de poste ou le")
        ],
        [
            ("Unit-LightTF", "Service Clients soit par courrier à l'adresse : La Banque Postale, TSA 10400, 69945 Lyon CEDEX 20, soit par téléphone au 3639 (Service gratuit + prix appel)."),
            ("LBP_Extra_BoldBold", " En cas de")
        ],
        [
            ("LBP_Extra_BoldBold", "désaccord avec la réponse apportée à votre réclamation écrite (datée de moins d'un an et signée) ou en l'absence de réponse dans un délai de 2 mois,"),
            ("Unit-LightTF", " vous")
        ],
        [
            ("Unit-LightTF", "pouvez saisir gratuitement Le Médiateur de la consommation de La Banque Postale sur le site https://mediateur.groupelaposte.com (à privilégier) ou par courrier au")
        ],
        [
            ("Unit-LightTF", "115 rue de Sèvres, Case postale G 009, 75275 Paris CEDEX 06. La demande de médiation devra être accompagnée d'une copie de la réclamation initiale écrite. En cas")
        ],
        [
            ("Unit-LightTF", "de souscription en ligne d'un produit ou service, vous pouvez également recourir à la plateforme européenne de Règlement en Ligne des Litiges (RLL) sur le site")
        ],
        [
            ("Unit-LightTF", "https://ec.europa.eu/consumers/odr/."),
            ("LBP_Extra_BoldBold", " La Garantie de vos dépôts (www.garantiedesdepots.fr) :"),
            ("Unit-LightTF", " Vos CCP, CAT, CSL, CEL, PEL, Livret jeune, livret B, PEP, Compte")
        ],
        [
            ("Unit-LightTF", "d'attente et Compte relais sont couverts par la Garantie des Dépôts du FGDR (Fonds de Garantie des Dépôts et de Résolution). Vos livrets A, LDDS et LEP bénéficient de la")
        ],
        [
            ("Unit-LightTF", "garantie de l'Etat.")
        ]
    ]
    
    target_width = 496.88
    line_height = 9.85
    cur_y = y_topdown
    
    for l_idx, line_spans in enumerate(lines):
        is_last_line = (l_idx == len(lines) - 1)
        natural_w = sum(pdfmetrics.stringWidth(txt, font_name, 8.01) for font_name, txt in line_spans)
        scale_x = (target_width / natural_w) if (not is_last_line and natural_w > 0) else 0.925
        
        c.saveState()
        c.translate(42.51, 840.0 - cur_y)
        c.scale(scale_x, 1.0)
        
        x_pos = 0.0
        for font_name, txt in line_spans:
            c.setFont(font_name, 8.01)
            c.drawString(x_pos, 0.0, txt)
            x_pos += pdfmetrics.stringWidth(txt, font_name, 8.01)
            
        c.restoreState()
        cur_y += line_height
        
INFO_MODELS_POOL = ["releve_en_ligne", "prelevement", "cheque", "alerte_sms", "fraude"]

def get_info_block_height(info_type, show_header=True):
    h = 19.5 if show_header else 0.0
    if info_type == "prelevement":
        h += 43.06
    elif info_type == "releve_en_ligne":
        h += 54.59
    elif info_type == "cheque":
        h += 31.53
    elif info_type == "alerte_sms":
        h += 53.11
    elif info_type == "fraude":
        h += 100.75
    else:
        h += 45.0
    return h

def pick_info_model_for_space(available_space, requested_type="auto", custom_text="", show_header=True):
    if custom_text or requested_type == "personnalise":
        needed = (19.5 if show_header else 0.0) + 40.0
        return "personnalise" if available_space >= needed else None
        
    if requested_type and requested_type != "auto" and requested_type in INFO_MODELS_POOL:
        needed = get_info_block_height(requested_type, show_header)
        if available_space >= needed:
            return requested_type
        return None
        
    candidates = [m for m in INFO_MODELS_POOL if get_info_block_height(m, show_header) <= available_space]
    if not candidates:
        return None
    return random.choice(candidates)

def draw_annexe_info_block(c, info_type, custom_text, y_topdown, show_header=True):
    if show_header:
        c.setFillColorRGB(25/255.0, 55/255.0, 105/255.0)
        c.rect(42.51, (840.0 - y_topdown) - 0.24, 4.33, 12.73, fill=1, stroke=0)
        c.setFont("Unit-MediumTF", 15.01)
        c.drawString(50.44, 840.0 - y_topdown, "Pour votre information")
        y_topdown += 19.5
        
    c.setFillColorRGB(0, 0, 0)
    if info_type == "prelevement":
        c.setFont("Unit-RegularTFBold", 10.01)
        c.drawString(52.36, 840.0 - y_topdown, "Planifiez vos dépenses et optez pour le prélèvement. Grâce à lui, vous payez à date fixe et de façon")
        y_topdown += 11.53
        c.drawString(52.36, 840.0 - y_topdown, "automatique les factures régulières comme le loyer, l'électricité, l'eau ou les assurances.")
        y_topdown += 11.53
        c.drawString(52.36, 840.0 - y_topdown, "Renseignez-vous auprès de votre Conseiller !")
        y_topdown += 20.0
    elif info_type == "releve_en_ligne":
        c.setFont("Unit-BoldTFBold", 10.01)
        c.drawString(52.36, 840.0 - y_topdown, "Simple, gratuit, sécurisé... et si vous passiez au relevé en ligne ?")
        y_topdown += 11.53
        c.setFont("Unit-RegularTFBold", 10.01)
        c.drawString(52.36, 840.0 - y_topdown, "Ce nouveau service vous permet de consulter et télécharger vos relevés CCP directement depuis votre")
        y_topdown += 11.53
        c.drawString(52.36, 840.0 - y_topdown, "espace sécurisé, en remplacement de l'envoi par courrier. Vos relevés resteront disponibles pendant 10 ans.")
        y_topdown += 11.53
        c.drawString(52.36, 840.0 - y_topdown, "Rendez-vous vite sur labanquepostale.fr pour en bénéficier !")
        y_topdown += 20.0
    elif info_type == "cheque":
        c.setFont("Unit-RegularTFBold", 10.01)
        c.drawString(52.36, 840.0 - y_topdown, "Avant de remettre votre chèque à l'encaissement, n'oubliez pas de le signer et d'indiquer votre numéro de")
        y_topdown += 11.53
        c.drawString(52.36, 840.0 - y_topdown, "compte au verso.")
        y_topdown += 20.0
    elif info_type == "alerte_sms":
        c.setFont("Unit-RegularTFBold", 10.01)
        c.drawString(52.36, 840.0 - y_topdown, "Une maîtrise sur toute la ligne ! Des SMS*, des emails, vous permettent de suivre au plus près votre compte")
        y_topdown += 11.53
        c.drawString(52.36, 840.0 - y_topdown, "et vous évitent de mauvaises surprises. Renseignez-vous depuis votre espace Client labanquepostale.fr ou")
        y_topdown += 11.53
        c.drawString(52.36, 840.0 - y_topdown, "auprès de votre Conseiller pour en profiter.")
        y_topdown += 10.05
        c.setFont("Unit-RegularTFIta", 8.01)
        c.drawString(52.36, 840.0 - y_topdown, "* Service accessible avec un abonnement Orange, SFR, Bouygues Télécom, Free.")
        y_topdown += 20.0
    elif info_type == "fraude":
        c.setFont("Unit-MediumTF", 10.01)
        header_txt = "Information fraude : "
        c.drawString(52.36, 840.0 - y_topdown, header_txt)
        hw = pdfmetrics.stringWidth(header_txt, "Unit-MediumTF", 10.01)
        c.setFont("Unit-RegularTF", 10.01)
        c.drawString(52.36 + hw, 840.0 - y_topdown, "Les fraudeurs profitent de la période estivale pour multiplier leurs tentatives de fraude. Leur")
        y_topdown += 11.53
        c.drawString(52.36, 840.0 - y_topdown, "technique préférée est l'usurpation d'identité ! Ils se font passer pour un collaborateur bancaire, un service")
        y_topdown += 11.53
        c.drawString(52.36, 840.0 - y_topdown, "administratif voire l'un de vos proches ou créent de faux sites de comparateurs de Crédits.")
        y_topdown += 11.53
        c.drawString(52.36, 840.0 - y_topdown, "Par téléphone, e-mail ou sms, ils cherchent ensuite à récupérer vos informations personnelles et bancaires. En cas")
        y_topdown += 11.53
        c.drawString(52.36, 840.0 - y_topdown, "de doute, ajournez la demande et contactez rapidement votre conseiller bancaire ou rendez-vous en bureau de")
        y_topdown += 11.53
        c.drawString(52.36, 840.0 - y_topdown, "poste.")
        y_topdown += 23.10
        c.drawString(52.36, 840.0 - y_topdown, "Retrouvez nos conseils pour vous protéger contre la fraude bancaire sur le site labanquepostale.fr")
        y_topdown += 20.0
    elif info_type == "personnalise" or custom_text:
        txt = custom_text or "Information client personnalisée."
        p = Paragraph(txt.replace("\n", "<br/>"), ParagraphStyle(name='CustomInfo', fontName='Unit-RegularTFBold', fontSize=10.01, leading=12.0, textColor=colors.HexColor('#000000')))
        w, h = p.wrap(490.0, 300)
        p.drawOn(c, 52.36, 840.0 - y_topdown - h)
        y_topdown += h + 20.0
    return y_topdown

def draw_annexe_carbo(c, y_topdown=279.47):
    c.setStrokeColorRGB(0, 0, 0)
    c.setLineWidth(0.24)
    
    y_top = 840.0 - y_topdown
    y_bottom = 840.0 - (y_topdown + 30.26)
    
    c.line(42.51, y_top, 534.91, y_top)
    c.line(42.51, y_bottom, 534.91, y_bottom)
    c.line(42.51, y_bottom, 42.51, y_top)
    c.line(534.91, y_bottom, 534.91, y_top)
    
    c.setFont("Unit-RegularTF", 10.01)
    c.setFillColorRGB(0, 0, 0)
    c.drawString(55.96, 840.0 - (y_topdown + 12.49), "Avec Carbo, estimez de manière simple et gratuite l'empreinte carbone de vos dépenses bancaires. Activez le")
    c.drawString(55.96, 840.0 - (y_topdown + 24.02), "service depuis votre Espace Client Internet ou votre Application mobile (rubrique « Empreinte carbone »).")
    
    return y_topdown + 30.26

def populate_transactions(data):
    def to_int(val, default=0):
        try:
            return int(str(val).strip())
        except (ValueError, TypeError):
            return default

    nb_ccp = to_int(data.get("ccp_nb_transactions"), 0)
    nb_livret = to_int(data.get("livret_a_nb_transactions"), 0)
    nb_epargne = to_int(data.get("epargne_nb_transactions"), 0)
    
    if data.get("mode") == "blocks":
        if "epargne_nb_transactions" not in data and (is_block_enabled(data, "show_tx_epargne", False) or is_block_enabled(data, "show_tx_items_epargne", False)):
            nb_epargne = 2
        if "livret_a_nb_transactions" not in data and (is_block_enabled(data, "show_tx_livret_a", False) or is_block_enabled(data, "show_tx_items_livret_a", False)):
            nb_livret = 2
    
    def parse_amount(amt_str):
        if not amt_str: return 0.0
        s = str(amt_str).replace('EUR', '').replace('€', '').replace('¤', '').replace(' ', '').replace('+', '').replace(',', '.')
        try:
            return float(s)
        except ValueError:
            return 0.0
        
    def format_amount(amount):
        s = f"{amount:,.2f}".replace(',', ' ').replace('.', ',')
        return s

    city = (data.get("titulaire_ville") or "PARIS").strip().upper()
    month = data.get("releve_mois_int", data.get("releve_mois", 1))
    year = data.get("releve_annee_int", data.get("releve_annee", 2025))
    wealth_profile = data.get("wealth_profile", "moyen")
    profil_trans = data.get("profil_transactions", "normal")
    age_profile = data.get("age_profile", "adulte")
    titulaire_nom = data.get("titulaire_nom", "MARTIN LUCAS")
    card_number = data.get("ccp_carte_numero", "790")
    cp = data.get("titulaire_cp", "75000")
    titulaire_sexe = data.get("titulaire_sexe", "M")
    dest_iban = data.get("dest_iban")

    def get_tx_delta(tx):
        if tx.get("credit"):
            return abs(parse_amount(tx["credit"]))
        if tx.get("debit"):
            return -abs(parse_amount(tx["debit"]))
        signe = tx.get("signe", "+")
        raw_val = tx.get("montant") if tx.get("montant") is not None else tx.get("amount")
        if raw_val is not None:
            val = abs(parse_amount(raw_val))
            return -val if signe == "-" else val
        return 0.0

    def generate_realistic_delta(wealth, is_epargne=False):
        if is_epargne:
            return float(random.choice([50, 100, 150, 200, 250, 300, 400, 500]))
        if wealth == "pauvre":
            return round(random.uniform(-30.0, 90.0), 2)
        elif wealth == "riche":
            return round(random.uniform(1200.0, 3500.0), 2)
        else:
            return round(random.uniform(150.0, 550.0), 2)

    nb_ccp = int(data.get("ccp_nb_transactions", 0))
    nb_livret = int(data.get("livret_a_nb_transactions", 0))
    nb_epargne = int(data.get("epargne_nb_transactions", 0))
    
    city_val = str(data.get("titulaire_ville", "")).strip()
    if not city_val:
        cp_ville = str(data.get("titulaire_cp_ville", data.get("cp_ville", "PARIS"))).strip()
        city_val = cp_ville.split(" ")[-1].strip() if " " in cp_ville else cp_ville
    city = city_val.upper() if city_val else "PARIS"
    
    month = data.get("releve_mois_str", "01")
    year = data.get("releve_annee_str", "25")
    
    wealth_profile = data.get("wealth_profile", "moyen")
    age_profile = data.get("age_profile", "adulte")
    profil_trans = data.get("profil_transactions", "normal")
    titulaire_nom = data.get("titulaire_nom_complet", "MR MARTIN LUCAS")
    card_number = str(data.get("ccp_carte_numero", data.get("carte_numero", "790"))).strip() or "790"
    cp = str(data.get("titulaire_cp", "75000")).strip()
    titulaire_sexe = str(data.get("titulaire_sexe", "M")).strip()
    dest_iban = str(data.get("livret_a_iban", data.get("epargne_iban", ""))).strip()

    # 1. Résolution des soldes CCP
    ccp_anc_val = data.get("ccp_solde_ancien", data.get("solde_ancien"))
    ccp_nouv_val = data.get("ccp_solde", data.get("solde"))
    
    has_ccp_anc = (ccp_anc_val is not None and str(ccp_anc_val).strip() != "")
    has_ccp_nouv = (ccp_nouv_val is not None and str(ccp_nouv_val).strip() != "")
    default_anc = 2500.0 if wealth_profile == "moyen" else (600.0 if wealth_profile == "pauvre" else 15000.0)
    
    if nb_ccp == 0 and not data.get("transactions_ccp"):
        delta_ccp = 0.0
        if has_ccp_anc:
            val_anc = format_amount(parse_amount(ccp_anc_val))
            data["ccp_solde_ancien"] = data["solde_ancien"] = val_anc
            data["ccp_solde"] = data["solde"] = val_anc
        elif has_ccp_nouv:
            val_nouv = format_amount(parse_amount(ccp_nouv_val))
            data["ccp_solde_ancien"] = data["solde_ancien"] = val_nouv
            data["ccp_solde"] = data["solde"] = val_nouv
        else:
            val_def = format_amount(default_anc)
            data["ccp_solde_ancien"] = data["solde_ancien"] = val_def
            data["ccp_solde"] = data["solde"] = val_def
        data["transactions_ccp"] = []
    else:
        if has_ccp_anc and has_ccp_nouv:
            delta_ccp = parse_amount(ccp_nouv_val) - parse_amount(ccp_anc_val)
        elif has_ccp_anc and not has_ccp_nouv:
            delta_ccp = generate_realistic_delta(wealth_profile, False)
            data["ccp_solde"] = format_amount(parse_amount(ccp_anc_val) + delta_ccp)
            data["solde"] = data["ccp_solde"]
        elif has_ccp_nouv and not has_ccp_anc:
            delta_ccp = generate_realistic_delta(wealth_profile, False)
            data["ccp_solde_ancien"] = format_amount(parse_amount(ccp_nouv_val) - delta_ccp)
            data["solde_ancien"] = data["ccp_solde_ancien"]
        else:
            delta_ccp = generate_realistic_delta(wealth_profile, False)
            data["ccp_solde_ancien"] = format_amount(default_anc)
            data["solde_ancien"] = data["ccp_solde_ancien"]
            data["ccp_solde"] = format_amount(default_anc + delta_ccp)
            data["solde"] = data["ccp_solde"]

        if nb_ccp > 0 and not data.get("transactions_ccp"):
            data["transactions_ccp"] = generate_transactions.generate_random_txs(
                nb_ccp, city, month, year, False, profil_trans, wealth_profile, age_profile,
                titulaire_nom, card_number, cp, titulaire_sexe, dest_iban, target_delta=delta_ccp
            )
        elif data.get("transactions_ccp"):
            real_sum = sum(get_tx_delta(t) for t in data["transactions_ccp"])
            cur_anc = parse_amount(data.get("ccp_solde_ancien", data.get("solde_ancien", 0.0)))
            data["ccp_solde"] = format_amount(cur_anc + real_sum)
            data["solde"] = data["ccp_solde"]

        if data.get("transactions_ccp"):
            data["transactions_ccp"] = generate_transactions.ensure_positive_running_balance(
                data["transactions_ccp"], data.get("ccp_solde_ancien", data.get("solde_ancien")), month=month, year=year
            )

    totals_ccp = generate_transactions.compute_total_operations(data.get("transactions_ccp", []))
    data["ccp_total_debit"] = totals_ccp["total_debit"]
    data["ccp_total_credit"] = totals_ccp["total_credit"]

    # Extraction des flux miroirs depuis le CCP vers les comptes d'épargne
    mirror_txs_la = []
    mirror_txs_ep = []
    nom_propre = " ".join(titulaire_nom.upper().split())
    if nom_propre.startswith("MR "): nom_propre = nom_propre[3:]
    elif nom_propre.startswith("MME "): nom_propre = nom_propre[4:]
    elif nom_propre.startswith("M "): nom_propre = nom_propre[2:]

    for tx in data.get("transactions_ccp", []):
        tx_str = " ".join(str(l) for l in tx.get("lignes", []))
        date_tx = tx.get("date", f"15/{month}")
        day_part = date_tx.split("/")[0] if "/" in date_tx else "15"
        mo_part = date_tx.split("/")[1] if "/" in date_tx else str(month).zfill(2)
        amt_val = abs(get_tx_delta(tx))
        amt_str = f"{amt_val:,.2f}".replace(',', ' ').replace('.', ',')
        
        if "LIVRET A" in tx_str and tx.get("signe") == "-":
            mirror_txs_la.append({
                "date": date_tx,
                "lignes": [
                    f"VIREMENT DE {nom_propre}",
                    f"DATE DE VALEUR : {day_part} {mo_part} 20{year}"
                ],
                "montant": amt_str,
                "amount": amt_val,
                "signe": "+",
                "type": "VIREMENT",
                "is_mirror": True
            })
            
        if ("EPARGNE" in tx_str or "COMPTE EPARGNE" in tx_str) and tx.get("signe") == "-":
            mirror_txs_ep.append({
                "date": date_tx,
                "lignes": [
                    f"VIREMENT DE {nom_propre}",
                    f"DATE DE VALEUR : {day_part} {mo_part} 20{year}"
                ],
                "montant": amt_str,
                "amount": amt_val,
                "signe": "+",
                "type": "VIREMENT",
                "is_mirror": True
            })

    # 2. Résolution des soldes Livret A
    should_populate_la = data.get("afficher_livret_a", False) or (
        data.get("mode") == "blocks" and (
            is_block_enabled(data, "show_tx_livret_a", False) or
            is_block_enabled(data, "show_tx_items_livret_a", False) or
            nb_livret > 0
        )
    )
    is_decembre = (int(month) == 12)
    
    taux_la_val = data.get("livret_a_taux")
    if taux_la_val is not None and str(taux_la_val).strip() != "":
        try:
            taux_la = float(str(taux_la_val).replace(',', '.'))
            if taux_la > 0.5:
                taux_la /= 100.0
        except ValueError:
            taux_la = generate_transactions.get_annual_interest_rate("LIVRET_A", year)
    else:
        taux_la = generate_transactions.get_annual_interest_rate("LIVRET_A", year)

    taux_ep_val = data.get("epargne_taux")
    if taux_ep_val is not None and str(taux_ep_val).strip() != "":
        try:
            taux_ep = float(str(taux_ep_val).replace(',', '.'))
            if taux_ep > 0.5:
                taux_ep /= 100.0
        except ValueError:
            taux_ep = generate_transactions.get_annual_interest_rate("CEL", year)
    else:
        taux_ep = generate_transactions.get_annual_interest_rate("CEL", year)

    if should_populate_la:
        la_anc_val = data.get("livret_a_solde_ancien")
        la_nouv_val = data.get("livret_a_solde")
        has_la_anc = (la_anc_val is not None and str(la_anc_val).strip() != "")
        has_la_nouv = (la_nouv_val is not None and str(la_nouv_val).strip() != "")
        mirror_sum_la = sum(m.get("amount", 0.0) * (1 if m.get("signe") == "+" else -1) for m in mirror_txs_la)
        
        default_anc_la = 10000.0 if wealth_profile == "moyen" else (3000.0 if wealth_profile == "pauvre" else 22000.0)
        if nb_livret == 0 and not data.get("transactions_livret_a"):
            delta_la = 0.0
            if has_la_anc:
                val_anc_la = format_amount(parse_amount(la_anc_val))
                data["livret_a_solde_ancien"] = data["livret_a_solde"] = val_anc_la
            elif has_la_nouv:
                val_nouv_la = format_amount(parse_amount(la_nouv_val))
                data["livret_a_solde_ancien"] = data["livret_a_solde"] = val_nouv_la
            else:
                val_def_la = format_amount(default_anc_la)
                data["livret_a_solde_ancien"] = data["livret_a_solde"] = val_def_la
            data["transactions_livret_a"] = []
        else:
            if has_la_anc and has_la_nouv:
                delta_la = parse_amount(la_nouv_val) - parse_amount(la_anc_val)
            elif has_la_anc and not has_la_nouv:
                if is_decembre and not mirror_txs_la:
                    delta_la = round(parse_amount(la_anc_val) * taux_la, 2)
                else:
                    delta_la = mirror_sum_la if mirror_txs_la else generate_realistic_delta(wealth_profile, True)
                data["livret_a_solde"] = format_amount(parse_amount(la_anc_val) + delta_la)
            elif has_la_nouv and not has_la_anc:
                if is_decembre and not mirror_txs_la:
                    delta_la = round(parse_amount(la_nouv_val) / (1.0 + taux_la) * taux_la, 2)
                else:
                    delta_la = mirror_sum_la if mirror_txs_la else generate_realistic_delta(wealth_profile, True)
                data["livret_a_solde_ancien"] = format_amount(parse_amount(la_nouv_val) - delta_la)
            else:
                if is_decembre and not mirror_txs_la:
                    delta_la = round(default_anc_la * taux_la, 2)
                else:
                    delta_la = mirror_sum_la if mirror_txs_la else generate_realistic_delta(wealth_profile, True)
                data["livret_a_solde_ancien"] = format_amount(default_anc_la)
                data["livret_a_solde"] = format_amount(default_anc_la + delta_la)

            if nb_livret > 0 and not data.get("transactions_livret_a"):
                data["transactions_livret_a"] = generate_transactions.generate_random_txs(
                    nb_livret, city, month, year, True, profil_trans, wealth_profile, age_profile,
                    titulaire_nom, card_number, cp, titulaire_sexe, dest_iban, target_delta=delta_la,
                    account_type="LIVRET_A", mirror_txs=mirror_txs_la, solde_ancien=data.get("livret_a_solde_ancien"),
                    custom_taux=taux_la
                )
            elif data.get("transactions_livret_a"):
                real_sum = sum(get_tx_delta(t) for t in data["transactions_livret_a"])
                cur_anc = parse_amount(data.get("livret_a_solde_ancien", 0.0))
                data["livret_a_solde"] = format_amount(cur_anc + real_sum)

            if data.get("transactions_livret_a"):
                data["transactions_livret_a"] = generate_transactions.ensure_positive_running_balance(
                    data["transactions_livret_a"], data.get("livret_a_solde_ancien"), month=month, year=year
                )

        totals_la = generate_transactions.compute_total_operations(data.get("transactions_livret_a", []))
        data["livret_a_total_debit"] = totals_la["total_debit"]
        data["livret_a_total_credit"] = totals_la["total_credit"]

    # 3. Résolution des soldes Épargne Logement
    should_populate_ep = data.get("afficher_epargne", False) or (
        data.get("mode") == "blocks" and (
            is_block_enabled(data, "show_tx_epargne", False) or
            is_block_enabled(data, "show_tx_items_epargne", False) or
            nb_epargne > 0
        )
    )
    if should_populate_ep:
        ep_anc_val = data.get("epargne_solde_ancien")
        ep_nouv_val = data.get("epargne_solde")
        has_ep_anc = (ep_anc_val is not None and str(ep_anc_val).strip() != "")
        has_ep_nouv = (ep_nouv_val is not None and str(ep_nouv_val).strip() != "")
        mirror_sum_ep = sum(m.get("amount", 0.0) * (1 if m.get("signe") == "+" else -1) for m in mirror_txs_ep)
        default_anc_ep = 15000.0 if wealth_profile == "moyen" else (5000.0 if wealth_profile == "pauvre" else 30000.0)
        
        if nb_epargne == 0 and not data.get("transactions_epargne"):
            delta_ep = 0.0
            if has_ep_anc:
                val_anc_ep = format_amount(parse_amount(ep_anc_val))
                data["epargne_solde_ancien"] = data["epargne_solde"] = val_anc_ep
            elif has_ep_nouv:
                val_nouv_ep = format_amount(parse_amount(ep_nouv_val))
                data["epargne_solde_ancien"] = data["epargne_solde"] = val_nouv_ep
            else:
                val_def_ep = format_amount(default_anc_ep)
                data["epargne_solde_ancien"] = data["epargne_solde"] = val_def_ep
            data["transactions_epargne"] = []
        else:
            if has_ep_anc and has_ep_nouv:
                delta_ep = parse_amount(ep_nouv_val) - parse_amount(ep_anc_val)
            elif has_ep_anc and not has_ep_nouv:
                if is_decembre and not mirror_txs_ep:
                    delta_ep = round(parse_amount(ep_anc_val) * taux_ep, 2)
                else:
                    delta_ep = mirror_sum_ep if mirror_txs_ep else generate_realistic_delta(wealth_profile, True)
                data["epargne_solde"] = format_amount(parse_amount(ep_anc_val) + delta_ep)
            elif has_ep_nouv and not has_ep_anc:
                if is_decembre and not mirror_txs_ep:
                    delta_ep = round(parse_amount(ep_nouv_val) / (1.0 + taux_ep) * taux_ep, 2)
                else:
                    delta_ep = mirror_sum_ep if mirror_txs_ep else generate_realistic_delta(wealth_profile, True)
                data["epargne_solde_ancien"] = format_amount(parse_amount(ep_nouv_val) - delta_ep)
            else:
                if is_decembre and not mirror_txs_ep:
                    delta_ep = round(default_anc_ep * taux_ep, 2)
                else:
                    delta_ep = mirror_sum_ep if mirror_txs_ep else generate_realistic_delta(wealth_profile, True)
                data["epargne_solde_ancien"] = format_amount(default_anc_ep)
                data["epargne_solde"] = format_amount(default_anc_ep + delta_ep)

            if nb_epargne > 0 and not data.get("transactions_epargne"):
                data["transactions_epargne"] = generate_transactions.generate_random_txs(
                    nb_epargne, city, month, year, True, profil_trans, wealth_profile, age_profile,
                    titulaire_nom, card_number, cp, titulaire_sexe, dest_iban, target_delta=delta_ep,
                    account_type="EPARGNE", mirror_txs=mirror_txs_ep, solde_ancien=data.get("epargne_solde_ancien"),
                    custom_taux=taux_ep
                )
            elif data.get("transactions_epargne"):
                real_sum = sum(get_tx_delta(t) for t in data["transactions_epargne"])
                cur_anc = parse_amount(data.get("epargne_solde_ancien", 0.0))
                data["epargne_solde"] = format_amount(cur_anc + real_sum)

            if data.get("transactions_epargne"):
                data["transactions_epargne"] = generate_transactions.ensure_positive_running_balance(
                    data["transactions_epargne"], data.get("epargne_solde_ancien"), month=month, year=year
                )

        totals_ep = generate_transactions.compute_total_operations(data.get("transactions_epargne", []))
        data["epargne_total_debit"] = totals_ep["total_debit"]
        data["epargne_total_credit"] = totals_ep["total_credit"]

    return data

def compute_dates(data):
    """
    Calcule dynamiquement et de manière cohérente toutes les dates du relevé :
    - Mois et année des opérations
    - Date de situation / solde au (dernier jour du mois de relevé)
    - Date d'édition du relevé (début du mois suivant avec jour dynamique)
    """
    mois_noms = ["", "janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
    
    if "releve_mois" in data and "releve_annee" in data:
        try:
            mois = int(data["releve_mois"])
            annee = int(data["releve_annee"])
        except (ValueError, TypeError):
            mois, annee = 1, 2025
    elif "date_edition" in data:
        date_str = str(data["date_edition"])
        m_iso = re.match(r"^(\d{4})-(\d{2})-(\d{2})$", date_str.strip())
        m_fr = re.match(r"^(\d{2})/(\d{2})/(\d{4})$", date_str.strip())
        if m_iso:
            annee, mois = int(m_iso.group(1)), int(m_iso.group(2))
        elif m_fr:
            annee, mois = int(m_fr.group(3)), int(m_fr.group(2))
        else:
            mois, annee = 1, 2025
    else:
        mois, annee = 1, 2025

    if mois in [1, 3, 5, 7, 8, 10, 12]:
        dernier_jour = 31
    elif mois in [4, 6, 9, 11]:
        dernier_jour = 30
    else:
        is_bissextile = (annee % 4 == 0 and annee % 100 != 0) or (annee % 400 == 0)
        dernier_jour = 29 if is_bissextile else 28

    nom_mois = mois_noms[mois]
    data["date_situation"] = f"{dernier_jour} {nom_mois} {annee}"
    data["date_releve"] = f"{str(dernier_jour).zfill(2)}/{str(mois).zfill(2)}/{annee}"
    data["releve_mois_int"] = mois
    data["releve_annee_int"] = annee
    data["releve_mois_str"] = str(mois).zfill(2)
    data["releve_annee_str"] = str(annee)[-2:]

    if mois == 12:
        edit_mois = 1
        edit_annee = annee + 1
    else:
        edit_mois = mois + 1
        edit_annee = annee
        
    edit_jour = random.randint(2, 5)
    edit_nom_mois = mois_noms[edit_mois]
    data["date_edition"] = f"{str(edit_jour).zfill(2)} {edit_nom_mois} {edit_annee}"
    data["date_edition_raw"] = f"{edit_annee}-{str(edit_mois).zfill(2)}-{str(edit_jour).zfill(2)}"

def validate_input_data(data):
    compute_dates(data)
    errors = []
    
    # 0. Normalisation des booléens d'activation
    def _parse_bool(val, default=True):
        if val is None: return default
        if isinstance(val, bool): return val
        if isinstance(val, str): return val.lower() == 'true'
        return bool(val)
        
    data["afficher_ccp"] = _parse_bool(data.get("afficher_ccp", True))
    data["afficher_livret_a"] = _parse_bool(data.get("afficher_livret_a", False))
    data["afficher_epargne"] = _parse_bool(data.get("afficher_epargne", False))
    
    if not (data["afficher_ccp"] or data["afficher_livret_a"] or data["afficher_epargne"]) and data.get("mode") != "blocks":
        errors.append("Au moins un compte (CCP, Livret A ou Épargne) doit être activé pour éditer le relevé.")
        
    # 1. Validation de l'identité du titulaire
    nom_raw = str(data.get("titulaire_nom", "")).strip()
    if not nom_raw and data.get("mode") != "blocks":
        errors.append("Le champ 'Nom du titulaire' (titulaire_nom) est obligatoire.")
    elif len(nom_raw) > 35:
        errors.append(f"Le nom du titulaire dépasse 35 caractères ('{nom_raw[:25]}...').")
    if not nom_raw:
        nom_raw = "MARTIN LUCAS"
        
    civ_pattern = r"^(?:M\.|MR\.|MR|MME\.|MME|MLLE\.|MLLE|MONSIEUR|MADAME|MADEMOISELLE)\s+"
    cleaned_nom = nom_raw
    detected_civ = None
    while True:
        m_civ = re.match(civ_pattern, cleaned_nom, flags=re.IGNORECASE)
        if m_civ:
            detected_civ = m_civ.group(0).strip()
            cleaned_nom = cleaned_nom[m_civ.end():].strip()
        else:
            break
            
    civ_field = str(data.get("civilite") or detected_civ or ("M." if str(data.get("titulaire_sexe", "M")).upper() in ["M", "MR"] else "Mme")).strip()
    civ_u = civ_field.upper().replace(".", "")
    if civ_u in ["M", "MR", "MONSIEUR"]:
        final_civ = "M."
    elif civ_u in ["MME", "MADAME"]:
        final_civ = "Mme"
    elif civ_u in ["MLLE", "MADEMOISELLE"]:
        final_civ = "Mlle"
    else:
        final_civ = civ_field
        
    if not cleaned_nom:
        cleaned_nom = "MARTIN LUCAS"
        
    data["titulaire_nom_complet"] = f"{final_civ} {cleaned_nom}".strip()

    # 2. Validation de l'adresse et géographie
    cp = str(data.get("titulaire_cp", "")).strip()
    if not cp and data.get("mode") != "blocks":
        errors.append("Le 'Code Postal' (titulaire_cp) est obligatoire.")
    elif cp and not re.match(r"^\d{5}$", cp):
        errors.append(f"Format de Code Postal invalide ('{cp}'). Attendu : 5 chiffres (ex: 75001, 31000).")
    if not cp:
        cp = "75001"
        
    ville = str(data.get("titulaire_ville", "")).strip()
    if not ville and data.get("mode") != "blocks":
        errors.append("La 'Ville' (titulaire_ville) est obligatoire.")
    if not ville:
        ville = "PARIS"
        
    data["titulaire_cp_ville"] = f"{cp} {ville}".strip()
    if len(data["titulaire_cp_ville"]) > 38:
        errors.append(f"La ligne Code Postal + Ville dépasse 38 caractères ('{data['titulaire_cp_ville']}').")
        
    # 3. Validation de l'identifiant client
    ident = str(data.get("identifiant", "")).strip()
    if ident and not re.match(r"^\d{6,12}$", ident):
        errors.append(f"Identifiant bancaire invalide ('{ident}'). Attendu : 6 à 12 chiffres.")
        
    # 4. Validation des paramètres du relevé (Mois / Année)
    mois_val = data.get("releve_mois_int")
    if mois_val is None or not (1 <= mois_val <= 12):
        errors.append(f"Mois du relevé invalide ('{data.get('releve_mois')}'). Attendu : entier entre 1 et 12.")
        
    annee_val = data.get("releve_annee_int")
    if annee_val is None or not (2000 <= annee_val <= 2099):
        errors.append(f"Année du relevé invalide ('{data.get('releve_annee')}'). Attendu : année valide (ex: 2025).")

    # 5. Validation des comptes bancaires activés
    comptes_a_valider = []
    if data["afficher_ccp"]: comptes_a_valider.append(("CCP", "ccp"))
    if data["afficher_livret_a"]: comptes_a_valider.append(("Livret A", "livret_a"))
    if data["afficher_epargne"]: comptes_a_valider.append(("Épargne", "epargne"))
    
    for label, prefix_cpt in comptes_a_valider:
        # IBAN
        iban = str(data.get(f"{prefix_cpt}_iban", "")).replace(" ", "").upper()
        if iban and not re.match(r"^FR\d{2}[A-Z0-9]{23}$", iban):
            errors.append(f"IBAN {label} invalide ('{data.get(f'{prefix_cpt}_iban')}'). Attendu : Format IBAN français (FR + 25 caractères).")
        # BIC
        bic = str(data.get(f"{prefix_cpt}_bic", "")).strip().upper()
        if bic and not re.match(r"^[A-Z0-9]{8,11}$", bic):
            errors.append(f"BIC {label} invalide ('{bic}'). Attendu : 8 ou 11 caractères alphanumériques.")

    # 6. Règles strictes sur les champs de valeurs monétaires
    champs_solde = ['ccp_solde', 'livret_a_solde', 'epargne_solde', 'ccp_solde_ancien', 'livret_a_solde_ancien', 'epargne_solde_ancien']
    for champ in champs_solde:
        val = data.get(champ)
        if val:
            val_clean = str(val).replace('€', '').replace('¤', '').replace('+', '').replace('-', '').replace(' ', '').replace(',', '.')
            try:
                float(val_clean)
            except ValueError:
                errors.append(f"Montant invalide pour '{champ}' ('{val}'). Attendu : valeur numérique décimale.")

    if errors:
        raise ValueError("Échec de la validation backend :\n- " + "\n- ".join(errors))

def format_date_french(date_str):
    if not date_str: return ""
    m_iso = re.match(r"^(\d{4})-(\d{2})-(\d{2})$", str(date_str).strip())
    m_fr = re.match(r"^(\d{2})/(\d{2})/(\d{4})$", str(date_str).strip())
    mois_noms = ["", "janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
    
    if m_iso:
        y, m, d = m_iso.groups()
        return f"{d} {mois_noms[int(m)]} {y}"
    elif m_fr:
        d, m, y = m_fr.groups()
        return f"{d} {mois_noms[int(m)]} {y}"
    return str(date_str)

def generate_pdf_doc(data):
    validate_input_data(data)
    data["date_edition_raw"] = data.get("date_edition", "")
    if "date_edition" in data:
        data["date_edition"] = format_date_french(data["date_edition"])
    data = populate_transactions(data)
    
    if "has_carbo_resolved" not in data:
        if data.get("mode") == "blocks":
            data["has_carbo_resolved"] = is_block_enabled(data, "show_annexe_carbone", is_block_enabled(data, "show_annexe_carbo", False))
        else:
            if "show_annexe_carbone" in data and data["show_annexe_carbone"] is not None:
                data["has_carbo_resolved"] = bool(data["show_annexe_carbone"])
            elif "show_annexe_carbo" in data and data["show_annexe_carbo"] is not None:
                data["has_carbo_resolved"] = bool(data["show_annexe_carbo"])
            else:
                data["has_carbo_resolved"] = (random.random() < 0.10)
    
    def render_all(c, is_simulation=False, total_pages_override=None):
        page_number = 1
        total_pages = total_pages_override if total_pages_override is not None else (1 if is_simulation else c.page_count)
        
        draw_header(c, data, page_number)
        y_reportlab = draw_middle(c, data, page_number)
        y_current = 840.0 - y_reportlab
        
        def check_page_break(c, y, needed, account_name, account_num, is_fresh_account=False):
            nonlocal page_number
            if y + needed > 765.0:
                draw_footer(c, data, page_number, total_pages)
                c.showPage()
                page_number += 1
                draw_header(c, data, page_number)
                if not is_fresh_account and account_name not in ("Mentions Légales & FGDR", "Comptes d'Épargne") and not str(account_name).startswith("Mentions"):
                    draw_suite_header(c, account_name, account_num)
                    y = 164.66
                    draw_table_headers(c, y)
                    y += 13.69
                else:
                    y = 145.0
            return y

        is_blocks_mode = (data.get("mode") == "blocks")
        txs_ccp = data.get("transactions_ccp", [])
        is_master_ccp = is_block_enabled(data, "show_tx_ccp", default=(not is_blocks_mode))
        
        has_ccp_content = (
            is_master_ccp or 
            is_block_enabled(data, "show_tx_header_ccp", False) or 
            is_block_enabled(data, "show_tx_table_headers_ccp", False) or 
            is_block_enabled(data, "show_tx_ancien_solde_ccp", False) or 
            is_block_enabled(data, "show_tx_items_ccp", False) or 
            is_block_enabled(data, "show_tx_nouveau_solde_ccp", False)
        ) if is_blocks_mode else (data.get("afficher_ccp", True) and is_master_ccp)

        if has_ccp_content:
            account_name = data.get("ccp_nom", "Compte Courant Postal")
            account_num = data.get("ccp_numero") or data.get("ccp_account_num") or data.get("account_num")
            iban = data.get("ccp_iban") or data.get("iban") or "FR7620041010010012345678984"
            if not account_num:
                clean_ib = str(iban).replace(" ", "").upper()
                if clean_ib.startswith("FR") and len(clean_ib) == 27:
                    account_num = clean_ib[14:25]
                else:
                    account_num = "00123456789"
            bic = data.get("ccp_bic") or data.get("bic") or "PSSTFRPPPAR"
            
            if is_block_enabled(data, "show_tx_header_ccp", default=is_master_ccp):
                is_etud = (data.get("profil_transactions") == "etudiant" or data.get("age_profile") == "jeune")
                has_dec = is_block_enabled(data, "show_tx_decouvert_ccp", default=(not is_etud))
                needed_hdr = 100.0 if has_dec else 60.0
                y_current = check_page_break(c, y_current, needed_hdr, account_name, account_num)
                y_current = draw_account_header(c, account_name, account_num, iban, bic, y_current, data=data)
            
            if is_block_enabled(data, "show_tx_table_headers_ccp", default=is_master_ccp):
                draw_table_headers(c, y_current)
                y_current += 19.46
            
            if is_block_enabled(data, "show_tx_ancien_solde_ccp", default=is_master_ccp):
                solde_anc = data.get("ccp_solde_ancien", data.get("solde_ancien", "22 494,72"))
                date_anc = get_ancien_solde_date(data)
                draw_solde_line(c, f"Ancien solde au {date_anc}", solde_anc, y_current)
                y_current += 17.05
                
            has_tx_items_ccp = is_block_enabled(data, "show_tx_items_ccp", default=is_master_ccp) and bool(txs_ccp)
            has_total_ccp = has_tx_items_ccp and is_block_enabled(data, "show_tx_total_ccp", default=is_master_ccp)

            if has_tx_items_ccp:
                for i, tx in enumerate(txs_ccp):
                    is_last_tx = (i == len(txs_ccp) - 1)
                    is_before_total = (is_last_tx and has_total_ccp)
                    is_before_nouveau = (is_last_tx and not has_total_ccp and is_block_enabled(data, "show_tx_nouveau_solde_ccp", default=is_master_ccp))
                    needed_height = get_tx_height(tx)
                    y_current = check_page_break(c, y_current, needed_height, account_name, account_num)
                    y_current = draw_transaction_lines(c, tx, y_current, is_before_total=is_before_total, is_before_nouveau=is_before_nouveau)
                
            if has_total_ccp:
                y_current = check_page_break(c, y_current, 15.0, account_name, account_num)
                draw_total_operations_line(c, data.get("ccp_total_debit", ""), data.get("ccp_total_credit", ""), y_current)
                y_current += 23.06
                
            if is_block_enabled(data, "show_tx_nouveau_solde_ccp", default=is_master_ccp):
                solde_nouv = data.get("ccp_solde", data.get("solde", "22 988,48"))
                y_current = check_page_break(c, y_current, 15.0, account_name, account_num)
                date_nouv = data.get("date_releve", "31/01/2025")
                draw_solde_line(c, f"Nouveau solde au {date_nouv}", solde_nouv, y_current, is_nouveau=True, has_total_before=has_total_ccp)
                y_current += 58.13


        # 2. Epargne (Livret A + Epargne Logement)
        txs_la = data.get("transactions_livret_a", [])
        txs_ep = data.get("transactions_epargne", [])

        if is_blocks_mode:
            has_grp_ep = is_block_enabled(data, "show_tx_epargne_group", False)
            has_head_ep = is_block_enabled(data, "show_tx_header_epargne", False)
            has_tab_ep = is_block_enabled(data, "show_tx_table_headers_epargne", False)
            has_la = (
                is_block_enabled(data, "show_tx_livret_a", False) or 
                is_block_enabled(data, "show_tx_subheader_livret_a", False) or 
                is_block_enabled(data, "show_tx_ancien_solde_livret_a", False) or 
                is_block_enabled(data, "show_tx_items_livret_a", False) or 
                is_block_enabled(data, "show_tx_nouveau_solde_livret_a", False)
            )
            has_ep = (
                is_block_enabled(data, "show_tx_epargne", False) or 
                is_block_enabled(data, "show_tx_subheader_epargne", False) or 
                is_block_enabled(data, "show_tx_ancien_solde_epargne", False) or 
                is_block_enabled(data, "show_tx_items_epargne", False) or 
                is_block_enabled(data, "show_tx_nouveau_solde_epargne", False)
            )
            has_any_epargne = has_grp_ep or has_head_ep or has_tab_ep or has_la or has_ep
        else:
            has_la = bool(txs_la) and data.get("afficher_livret_a", False) and is_block_enabled(data, "show_tx_livret_a", True)
            has_ep = bool(txs_ep) and data.get("afficher_epargne", False) and is_block_enabled(data, "show_tx_epargne", True)
            has_grp_ep = has_head_ep = has_tab_ep = False
            has_any_epargne = (has_la or has_ep)

        info_blocks_pages = set()

        want_info_block = is_block_enabled(data, "show_annexe_info_group", False) or \
                          is_block_enabled(data, "show_annexe_info_content", False) or \
                          is_block_enabled(data, "show_annexe_info_header", False)
        
        can_auto_fill = is_block_enabled(data, "auto_fill_info_block", default=True)
        req_type = data.get("annexe_info_type", "auto")
        custom_txt = data.get("annexe_info_custom_text", "")
        is_explicit_info = (req_type not in ["auto", "none"] or bool(custom_txt))

        if (want_info_block or can_auto_fill or is_explicit_info) and has_ccp_content:
            if page_number not in info_blocks_pages:
                available_space = 765.0 - y_current
                show_hdr = is_block_enabled(data, "show_annexe_info_header", default=True)
                chosen_type = pick_info_model_for_space(available_space, req_type, custom_text=custom_txt, show_header=show_hdr)
                if not chosen_type and is_explicit_info:
                    draw_footer(c, data, page_number, total_pages)
                    c.showPage()
                    page_number += 1
                    if not is_simulation:
                        draw_header(c, data, page_number)
                    y_current = 145.0
                    available_space = 765.0 - y_current
                    chosen_type = pick_info_model_for_space(available_space, req_type, custom_text=custom_txt, show_header=show_hdr) or (req_type if req_type != "auto" else "releve_en_ligne")
                
                if chosen_type:
                    y_current = draw_annexe_info_block(c, chosen_type, custom_txt, y_current, show_header=show_hdr)
                    info_blocks_pages.add(page_number)

        if has_any_epargne:
            if has_ccp_content:
                draw_footer(c, data, page_number, total_pages)
                c.showPage()
                page_number += 1
                if not is_simulation:
                    draw_header(c, data, page_number)
                y_current = 143.28

            has_group_header = is_block_enabled(data, "show_tx_header_epargne", default=(not is_blocks_mode or has_grp_ep))
            has_table_header = is_block_enabled(data, "show_tx_table_headers_epargne", default=(not is_blocks_mode or has_grp_ep))
            
            if has_group_header:
                y_current = check_page_break(c, y_current, 60.0, "Comptes d'Épargne", "", is_fresh_account=True)
                y_current = draw_epargne_main_header(c, y_current)
            if has_table_header:
                draw_table_headers(c, y_current, is_epargne=True)
                y_current += 16.34

            if data.get("comptes_epargne_list"):
                epargnes_to_draw = data.get("comptes_epargne_list")
            else:
                epargnes_to_draw = []
                if has_la:
                    epargnes_to_draw.append({
                        "type": "livret_a",
                        "name": data.get("livret_a_nom", "Livret A"),
                        "num": data.get("livret_a_numero", "210 5436798 J"),
                        "iban": data.get("livret_a_iban", "FR76 1001 1000 2021 0543 6798 J51"),
                        "bic": data.get("livret_a_bic", "PSSTFRPPCNE"),
                        "txs": txs_la,
                        "solde_anc": data.get("livret_a_solde_ancien", "10 500,00"),
                        "solde_nouv": data.get("livret_a_solde", "10 574,15")
                    })
                    
                if has_ep:
                    epargnes_to_draw.append({
                        "type": "epargne",
                        "name": data.get("epargne_nom", "Compte Épargne Logement"),
                        "num": data.get("epargne_numero", "340 9123847 K"),
                        "iban": data.get("epargne_iban", "FR76 1001 1000 2034 0912 3847 K38"),
                        "bic": data.get("epargne_bic", "PSSTFRPPCNE"),
                        "txs": txs_ep,
                        "solde_anc": data.get("epargne_solde_ancien", "15 200,00"),
                        "solde_nouv": data.get("epargne_solde", "15 242,92")
                    })
            
            for ep in epargnes_to_draw:
                    ep_type = ep["type"]
                    is_master = is_block_enabled(data, f"show_tx_{ep_type}", default=(not is_blocks_mode))
                    
                    if is_block_enabled(data, f"show_tx_subheader_{ep_type}", default=is_master):
                        y_current = check_page_break(c, y_current, 30.0, "Comptes d'Épargne", "")
                        y_current = draw_epargne_subheader(c, ep["name"], ep["num"], ep["iban"], ep["bic"], y_current)
                    
                    if is_block_enabled(data, f"show_tx_ancien_solde_{ep_type}", default=is_master):
                        date_anc = get_ancien_solde_date(data)
                        draw_solde_line(c, f"Ancien solde au {date_anc}", ep["solde_anc"], y_current, is_epargne=True)
                        y_current += 17.05
                        
                    has_ep_tx_items = is_block_enabled(data, f"show_tx_items_{ep_type}", default=is_master) and bool(ep["txs"])
                    has_total_ep = has_ep_tx_items and (len(ep["txs"]) >= 2) and is_block_enabled(data, f"show_tx_total_{ep_type}", default=is_master)

                    if has_ep_tx_items:
                        for i, tx in enumerate(ep["txs"]):
                            is_last_tx = (i == len(ep["txs"]) - 1)
                            is_before_total = (is_last_tx and has_total_ep)
                            is_before_nouveau = (is_last_tx and not has_total_ep and is_block_enabled(data, f"show_tx_nouveau_solde_{ep_type}", default=is_master))
                            needed_height = get_tx_height(tx)
                            y_current = check_page_break(c, y_current, needed_height, "Comptes d'Épargne", "")
                            y_current = draw_transaction_lines(c, tx, y_current, is_before_total=is_before_total, is_before_nouveau=is_before_nouveau, is_epargne=True)
                        if not has_total_ep:
                            y_current += 4.80
                        
                    if has_total_ep:
                        tot_d_ep = data.get(f"{ep_type}_total_debit", "")
                        tot_c_ep = data.get(f"{ep_type}_total_credit", "")
                        y_current = check_page_break(c, y_current, 15.0, "Comptes d'Épargne", "")
                        draw_total_operations_line(c, tot_d_ep, tot_c_ep, y_current, is_epargne=True)
                        y_current += 23.06

                    if is_block_enabled(data, f"show_tx_nouveau_solde_{ep_type}", default=is_master):
                        y_current = check_page_break(c, y_current, 15.0, "Comptes d'Épargne", "")
                        date_nouv = data.get("date_releve", "31/01/2025")
                        draw_solde_line(c, f"Nouveau solde au {date_nouv}", ep["solde_nouv"], y_current, is_nouveau=True, has_total_before=has_total_ep, is_epargne=True)
                        y_current += 58.13

        has_fgdr = is_block_enabled(data, "show_annexe_fgdr_legal", default=(data.get("mode") != "blocks"))
        if has_fgdr:
            if page_number in info_blocks_pages or (y_current + 85.0 > 765.0):
                draw_footer(c, data, page_number, total_pages)
                c.showPage()
                page_number += 1
                if not is_simulation:
                    draw_header(c, data, page_number)
                y_current = 145.0
            y_current = draw_annexe_fgdr_legal(c, y_current)

        draw_footer(c, data, page_number, total_pages)
        if not is_simulation:
            c.showPage()
            
        needs_page2_blocks = (data.get("mode") == "blocks" and page_number == 1 and 
                             (is_block_enabled(data, "show_small_header", False) or 
                              is_block_enabled(data, "show_conseil_conservation", False)))
        needs_page2_normal = (data.get("mode") != "blocks" and page_number == 1 and total_pages >= 2)
        
        if (needs_page2_blocks or needs_page2_normal) and page_number < total_pages:
            page_number += 1
            if is_simulation:
                c.showPage()
            else:
                draw_header(c, data, page_number)
                draw_footer(c, data, page_number, total_pages)
                c.showPage()

    dummy_buffer = io.BytesIO()
    dummy_c = canvas.Canvas(dummy_buffer, pagesize=(595.0, 840.0))
    dummy_c.page_count = 1
    original_showPage = dummy_c.showPage
    def new_showPage():
        dummy_c.page_count += 1
        original_showPage()
    dummy_c.showPage = new_showPage
    
    render_all(dummy_c, is_simulation=True, total_pages_override=2)
    
    final_total_pages = dummy_c.page_count
    if data.get("mode") != "blocks" and final_total_pages < 2:
        final_total_pages = 2
    elif data.get("mode") == "blocks" and final_total_pages < 2 and (is_block_enabled(data, "show_small_header", False) or is_block_enabled(data, "show_conseil_conservation", False)):
        final_total_pages = 2
        
    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=(595.0, 840.0))
    c.page_count = final_total_pages
    render_all(c, is_simulation=False, total_pages_override=final_total_pages)
    
    c.save()
    return pdf_buffer.getvalue()

def generate_releve_lbp_pdf_bytes(data, is_preview=False):
    return generate_pdf_doc(data)

def add_watermark_to_pdf_bytes(pdf_bytes):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    for page in doc:
        rect = page.rect
        for y in range(0, int(rect.height), 160):
            for x in range(0, int(rect.width), 220):
                pos = fitz.Point(x, y)
                morph_mat = fitz.Matrix(-40)
                page.insert_text(
                    pos,
                    "APERCU",
                    fontname="helv",
                    fontsize=38,
                    color=(0.82, 0.82, 0.82),
                    morph=(pos, morph_mat),
                    overlay=True
                )
    watermarked = doc.tobytes(deflate=True)
    doc.close()
    return watermarked


