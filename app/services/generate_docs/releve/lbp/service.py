import io
import zipfile
from app.services.generate_docs.releve import releves_orchestrator as ro
from app.services.generate_docs.releve.lbp import generate_pdf as gp

def format_french_month(month_num: int) -> str:
    months_fr = [
        "Janvier", "Fevrier", "Mars", "Avril", "Mai", "Juin",
        "Juillet", "Aout", "Septembre", "Octobre", "Novembre", "Decembre"
    ]
    return months_fr[(month_num - 1) % 12]

import re

def clean_and_format_nom_complet(civilite: str, nom_input: str) -> str:
    raw = (nom_input or "").strip()
    if not raw:
        civ = (civilite or "M.").strip().upper()
        if civ in ["M.", "MR", "MONSIEUR"]:
            return "M. MARTIN LUCAS"
        elif civ in ["MME", "MADAME"]:
            return "Mme MARTIN LUCAS"
        return "M. MARTIN LUCAS"
        
    civ_pattern = r"^(?:M\.|MR\.|MR|MME\.|MME|MLLE\.|MLLE|MONSIEUR|MADAME|MADEMOISELLE)\s+"
    cleaned = raw
    detected = None
    while True:
        m = re.match(civ_pattern, cleaned, flags=re.IGNORECASE)
        if m:
            detected = m.group(0).strip()
            cleaned = cleaned[m.end():].strip()
        else:
            break
            
    chosen_civ = (civilite or detected or "M.").strip()
    civ_u = chosen_civ.upper().replace(".", "")
    if civ_u in ["MR", "MONSIEUR", "M"]:
        norm_civ = "M."
    elif civ_u in ["MME", "MADAME"]:
        norm_civ = "Mme"
    elif civ_u in ["MLLE", "MADEMOISELLE"]:
        norm_civ = "Mlle"
    else:
        norm_civ = chosen_civ
        
    if not cleaned:
        cleaned = "MARTIN LUCAS"
        
    return f"{norm_civ} {cleaned}".strip()

def map_request_to_config(req_data: dict) -> dict:
    mode = req_data.get("mode", "facile")
    
    civ = (req_data.get("civilite") or "M.").strip()
    nom = (req_data.get("nom") or "").strip()
    prenom = (req_data.get("prenom") or "").strip()

    if nom or prenom:
        np_val = f"{nom} {prenom}".strip()
    else:
        np_val = (req_data.get("nom_prenom") or req_data.get("titulaire_nom_complet") or req_data.get("titulaire_nom") or "").strip()
        if np_val:
            parts = np_val.split(None, 1)
            nom = parts[0]
            prenom = parts[1] if len(parts) > 1 else ""
        else:
            nom = "MARTIN"
            prenom = "LUCAS"
            np_val = "MARTIN LUCAS"

    nom_complet = clean_and_format_nom_complet(civ, np_val)
    
    iban_raw = str(req_data.get("iban") or "").replace(" ", "").upper()
    acc_raw = str(req_data.get("numero_compte") or "").replace(" ", "").upper()
    cle_raw = str(req_data.get("cle_compte") or "").replace(" ", "")

    if iban_raw.startswith("FR") and len(iban_raw) == 27:
        account_num = acc_raw or iban_raw[14:25]
        cle_compte = cle_raw or iban_raw[25:27]
        iban_final = iban_raw
    else:
        account_num = acc_raw or "1452934L025"
        cle_compte = cle_raw or "57"
        iban_final = iban_raw or "FR9020041010011452934L02557"
    
    cfg = {
        "bank_type": "lbp",
        "mode": mode,
        "profil": req_data.get("profil", "normal"),
        "wealth_profile": req_data.get("wealth_profile", "moyen"),
        "nom": nom,
        "prenom": prenom,
        "nom_prenom": np_val,
        "titulaire_nom": nom_complet,
        "titulaire_nom_complet": nom_complet,
        "civilite": civ,
        "adresse": req_data.get("adresse") or "15 RUE DE LA PAIX",
        "complement_adresse": req_data.get("complement_adresse") or "",
        "cp": req_data.get("cp") or "75001",
        "ville": req_data.get("ville") or "PARIS",
        "centre_financier": req_data.get("centre_financier") or "PARIS CENTRE FINANCIER",
        
        "identifiant": req_data.get("identifiant") or "1455835203",
        "account_num": account_num,
        "numero_compte": account_num,
        "cle_compte": cle_compte,
        "iban": iban_final,
        "bic": req_data.get("bic") or "PSSTFRPPPAR",
        "card_number": req_data.get("card_number") or "456",
        "decouvert_autorise": req_data.get("decouvert_autorise") or "300,00",
        "solde_initial": req_data.get("solde_initial") or "3450,00",
        "nb_transactions": req_data.get("nb_transactions_moyen", 14),
        "start_num_releve": req_data.get("numero_releve_debut") or req_data.get("start_num_releve"),
        "afficher_ccp": req_data.get("afficher_ccp", True),
        
        "has_epargne": req_data.get("include_epargne", False),
        "afficher_livret_a": req_data.get("include_epargne", False),
        "show_situation_livret_a": req_data.get("include_epargne", False),
        "show_tx_livret_a": req_data.get("include_epargne", False),
        "livret_a_nom": req_data.get("epargne_nom") or "Livret A",
        "livret_a_numero": req_data.get("epargne_numero") or "210 5436798 J",
        "livret_a_iban": req_data.get("epargne_iban") or "FR76 1001 1000 2021 0543 6798 J51",
        "livret_a_bic": req_data.get("epargne_bic") or "PSSTFRPPCNE",
        "livret_a_solde_initial": req_data.get("epargne_solde_initial") or "5000,00",
        "solde_livret_a_initial": req_data.get("epargne_solde_initial") or "5000,00",
        "livret_a_taux": req_data.get("epargne_taux") or "3,00",
        "livret_a_nb_transactions": req_data.get("epargne_nb_tx", 2),
        "epargne_comptes": req_data.get("epargne_comptes"),
        
        "custom_employeur_nom": req_data.get("employeur_nom"),
        "custom_salaire_montant": req_data.get("salaire_net"),
        "custom_salaire_jour": req_data.get("jour_salaire"),
        "custom_loyer_montant": req_data.get("loyer_montant"),
        "custom_loyer_bailleur": req_data.get("loyer_bailleur"),
        "prelevements_selectionnes": req_data.get("prelevements_selectionnes") or ["EDF", "ORANGE", "MUTUELLE"],
        "target_solde_final": req_data.get("target_solde_final"),
        "contacts_virements": req_data.get("contacts_virements"),
        "strict_zero_incident": req_data.get("strict_zero_incident", True),
        "taux_decouvert": req_data.get("taux_decouvert", "16,00"),
        "show_annexe_carbone": req_data.get("show_annexe_carbone", True),
        "annexe_info_type": req_data.get("annexe_info_type", "auto"),
        "annexe_info_custom_text": req_data.get("annexe_info_custom_text", ""),
        "date_edition_custom": req_data.get("date_edition_custom"),
        "custom_transactions": req_data.get("custom_transactions", [])
    }
    return cfg

def generate_lbp_preview_pdf_bytes(req_data: dict) -> bytes:
    import pymupdf as fitz

    cfg = map_request_to_config(req_data)
    duree = int(req_data.get("duree_mois", 1))
    mois_debut = int(req_data.get("mois_debut", 1))
    annee_debut = int(req_data.get("annee_debut", 2026))

    generated_series = ro.generate_multi_releves(cfg, mois_debut, annee_debut, duration_months=duree)
    if not generated_series:
        raise ValueError("Échec de génération de l'aperçu")

    merged_doc = fitz.open()

    for doc_data in generated_series:
        pdf_bytes = gp.generate_releve_lbp_pdf_bytes(doc_data)
        month_doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        merged_doc.insert_pdf(month_doc)
        month_doc.close()

    merged_bytes = merged_doc.tobytes(deflate=True)
    merged_doc.close()

    return gp.add_watermark_to_pdf_bytes(merged_bytes)

def generate_lbp_releves_bytes(req_data: dict) -> tuple[bytes, str, str]:
    cfg = map_request_to_config(req_data)
    duree = int(req_data.get("duree_mois", 1))
    mois_debut = int(req_data.get("mois_debut", 1))
    annee_debut = int(req_data.get("annee_debut", 2026))
    
    generated_series = ro.generate_multi_releves(cfg, mois_debut, annee_debut, duration_months=duree)
    if not generated_series:
        raise ValueError("Échec de génération de la série de relevés")
        
    if duree == 1:
        single_doc = generated_series[0]
        pdf_bytes = gp.generate_releve_lbp_pdf_bytes(single_doc)
        month_name = format_french_month(mois_debut)
        filename = f"Releve_LBP_{month_name}_{annee_debut}.pdf"
        return pdf_bytes, "application/pdf", filename
    else:
        # Multi-mois : Archivage ZIP ordonné
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            for idx, doc_data in enumerate(generated_series):
                m_num = doc_data.get("releve_mois", mois_debut + idx)
                y_num = doc_data.get("releve_annee", annee_debut)
                m_name = format_french_month(m_num)
                num_rel = int(str(doc_data.get("num_releve", idx + 1)).strip())
                
                doc_pdf_bytes = gp.generate_releve_lbp_pdf_bytes(doc_data)
                doc_filename = f"Releve_LBP_N{num_rel:02d}_{m_name}_{y_num}.pdf"
                zf.writestr(doc_filename, doc_pdf_bytes)
                
        zip_buffer.seek(0)
        zip_bytes = zip_buffer.getvalue()
        zip_filename = f"Releves_La_Banque_Postale_{duree}_mois.zip"
        return zip_bytes, "application/zip", zip_filename
