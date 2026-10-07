import importlib
import io
import re

from app.services.generate_docs.common import example_dates
from app.services.generate_docs.common.date_validation import validate_calendar_date, validate_time_format
from app.services.generate_docs.common.preview import pdf_bytes_to_watermarked_jpg
from app.services.generate_docs.facture.issuers.loro_piana import copy as loro_piana_texts
from app.services.generate_docs.facture.schemas import parse_facture_payload

ISSUERS = (
    "adidas", "amazon", "boulanger", "fnac", "nike", "ami", "burberry",
    "cdiscount", "dafy", "darty", "gaz", "engie", "loro_piana", "pack_moto", "dior", "jacquemus",
    "chanel", "channel", "fred", "nocibe", "sfr",
)

FILENAMES = {
    "adidas": ("Facture_Adidas.pdf", "preview_Facture_Adidas.jpg", "Adidas"),
    "amazon": ("Facture_Amazon.pdf", "preview_Facture_Amazon.jpg", "Amazon"),
    "boulanger": ("Facture_Boulanger.pdf", "preview_Facture_Boulanger.jpg", "Boulanger"),
    "fnac": ("Facture_Fnac.pdf", "preview_Facture_Fnac.jpg", "Fnac"),
    "nike": ("Facture_Nike.pdf", "preview_Facture_Nike.jpg", "Nike"),
    "ami": ("Facture_AMI.pdf", "preview_Facture_AMI.jpg", "AMI"),
    "burberry": ("Facture_Burberry.pdf", "preview_Facture_Burberry.jpg", "Burberry"),
    "cdiscount": ("Facture_Cdiscount.pdf", "preview_Facture_Cdiscount.jpg", "Cdiscount"),
    "dafy": ("Facture_Dafy_Moto.pdf", "preview_Facture_Dafy_Moto.jpg", "Dafy Moto"),
    "darty": ("Facture_Darty.pdf", "preview_Facture_Darty.jpg", "Darty"),
    "gaz": ("Facture_Gaz.pdf", "preview_Facture_Gaz.jpg", "Facture Gaz"),
    "engie": ("Facture_Gaz.pdf", "preview_Facture_Gaz.jpg", "Facture Gaz (Engie)"),
    "loro_piana": ("Facture_Loro_Piana.pdf", "preview_Facture_Loro_Piana.jpg", "Loro Piana"),
    "pack_moto": ("Facture_Pack_Moto.pdf", "preview_Facture_Pack_Moto.jpg", "Pack Moto"),
    "dior": ("Facture_Dior.pdf", "preview_Facture_Dior.jpg", "Dior"),
    "jacquemus": ("Facture_Jacquemus.pdf", "preview_Facture_Jacquemus.jpg", "Jacquemus"),
    "chanel": ("Facture_Chanel.pdf", "preview_Facture_Chanel.jpg", "Chanel"),
    "channel": ("Facture_Chanel.pdf", "preview_Facture_Chanel.jpg", "Chanel"),
    "fred": ("Facture_Fred.pdf", "preview_Facture_Fred.jpg", "Fred"),
    "nocibe": ("Facture_Nocibe.pdf", "preview_Facture_Nocibe.jpg", "Nocibé"),
    "sfr": ("Facture_SFR.pdf", "preview_Facture_SFR.jpg", "SFR"),
}


def _format_dior_datetime(date_val: str, time_val: str) -> str:
    months_fr = [
        "Janvier", "Fevrier", "Mars", "Avril", "Mai", "Juin",
        "Juillet", "Aout", "Septembre", "Octobre", "Novembre", "Decembre"
    ]
    formatted_date = date_val
    if "/" in date_val:
        parts = date_val.split("/")
        if len(parts) == 3:
            try:
                day = int(parts[0])
                month = int(parts[1])
                year = int(parts[2])
                if 1 <= month <= 12:
                    formatted_date = f"{day}-{months_fr[month - 1]}-{year}"
            except Exception:
                pass
    formatted_time = time_val or "13:12:14"
    if len(formatted_time) == 5:
        formatted_time = f"{formatted_time}:00"
    if formatted_date and formatted_time:
        return f"{formatted_date} {formatted_time}"
    return formatted_date or formatted_time or ""


def _fill_example_dates(issuer: str, payload: dict) -> dict:
    if issuer == "adidas":
        payload.setdefault("date_facture", example_dates.adidas_invoice())
        payload.setdefault("date_livraison", example_dates.adidas_delivery())
        return payload
    if issuer == "amazon":
        payload.setdefault("date_commande", example_dates.amazon_order())
        payload.setdefault("date_facture", example_dates.amazon_invoice())
        return payload
    if issuer == "nike":
        stamp = example_dates.nike_invoice()
        payload.setdefault("date_facture", stamp)
        df = str(payload.get("date_facture") or "").strip()
        if df:
            curr_envoi = str(payload.get("date_envoi") or "").strip()
            if not curr_envoi or curr_envoi == stamp:
                payload["date_envoi"] = df
            else:
                payload.setdefault("date_envoi", df)
            curr_ech = str(payload.get("date_echeance") or "").strip()
            if not curr_ech or curr_ech == stamp:
                payload["date_echeance"] = df
            else:
                payload.setdefault("date_echeance", df)
        else:
            payload.setdefault("date_envoi", stamp)
            payload.setdefault("date_echeance", stamp)
        return payload
    if issuer == "ami":
        payload.setdefault("date_facture", example_dates.ami_invoice())
        return payload
    if issuer == "burberry":
        stamp = example_dates.burberry_order()
        payload.setdefault("date_commande", stamp)
        payload.setdefault("date_expedition", stamp)
        return payload
    if issuer == "fnac":
        payload.setdefault("num_facture", "2027880107")
        payload.setdefault("num_commande", "BXU7ZFTY2SUE2")
        en_ligne = payload.get("en_ligne", True)
        if en_ligne in (False, 0, "0", "false", "False", "off", "no"):
            stamp = example_dates.fnac_magasin()
        else:
            stamp = example_dates.fnac_web()
        payload.setdefault("date_commande", stamp)
        payload.setdefault("date_facture", stamp)
        payload.setdefault("echeance", stamp)
        payload.setdefault("matricule", "7000575")
        lp = str(payload.get("livraison_prenom") or "").strip()
        ln = str(payload.get("livraison_nom") or "").strip()
        if lp and ln and lp not in ln:
            payload["livraison_nom"] = f"{ln} {lp}"
        fp = str(payload.get("facturation_prenom") or "").strip()
        fn = str(payload.get("facturation_nom") or "").strip()
        if fp and fn and fp not in fn:
            payload["facturation_nom"] = f"{fn} {fp}"
        lcp = str(payload.get("livraison_cp") or "").strip()
        lville = str(payload.get("livraison_ville") or "").strip()
        if lcp or lville:
            payload["livraison_cp_ville"] = f"{lcp} {lville}".strip()
        fcp = str(payload.get("facturation_cp") or "").strip()
        fville = str(payload.get("facturation_ville") or "").strip()
        if fcp or fville:
            payload["facturation_cp_ville"] = f"{fcp} {fville}".strip()
        num_fac = str(payload.get("num_facture") or "2027880107").strip()
        nom_ref = fn or ln or "Martin"
        prenom_ref = fp or lp or "Lucas"
        init_nom = nom_ref[0].upper() if nom_ref else "M"
        p_clean = re.sub(r"[^A-Za-z]", "", prenom_ref).upper() or "LUCAS"
        comp_nref = f"{num_fac} - {init_nom}{p_clean} -FND"
        curr_nref = str(payload.get("nref") or "").strip()
        if not curr_nref or curr_nref.startswith("100110078") or curr_nref == "2027880107 - MLUCAS -FND":
            if nom_ref != "Martin" or prenom_ref != "Lucas" or num_fac != "2027880107":
                payload["nref"] = comp_nref
            elif not curr_nref or curr_nref.startswith("100110078"):
                payload["nref"] = comp_nref
        elif not curr_nref.startswith(num_fac):
            payload["nref"] = comp_nref
        return payload
    if issuer in ("gaz", "engie"):
        payload.setdefault("date_facture", example_dates.burberry_order())
        return payload
    if issuer == "loro_piana":
        payload.setdefault("date_ticket", loro_piana_texts.ticket_datetime())
        return payload
    if issuer == "pack_moto":
        stamp = example_dates.ami_invoice()
        payload.setdefault("date_facture", stamp)
        payload.setdefault("date_commande", stamp)
        return payload
    if issuer == "dior":
        if not payload.get("client_nom"):
            prenom = str(payload.get("prenom", "")).strip()
            nom = str(payload.get("nom", "")).strip()
            civ = str(payload.get("civilite", "Mr")).strip()
            if prenom and nom:
                payload["client_nom"] = f"{civ} {nom.upper()} {prenom}".strip() if civ else f"{nom.upper()} {prenom}".strip()
            elif nom:
                payload["client_nom"] = f"{civ} {nom.upper()}".strip() if civ else nom.upper()
            elif prenom:
                payload["client_nom"] = f"{civ} {prenom}".strip() if civ else prenom
        payload.setdefault("client_tel", "06.58.69.25.45")
        if "items" in payload and isinstance(payload["items"], list):
            tot_qty = 0
            for it in payload["items"]:
                if isinstance(it, dict):
                    try:
                        tot_qty += max(1, int(str(it.get("qty", 1)).strip()))
                    except (ValueError, TypeError):
                        tot_qty += 1
            if tot_qty > 0:
                payload["count_label"] = f"{tot_qty} produit(s)"
        dv = str(payload.get("date_vente", "")).strip()
        hv = str(payload.get("heure_vente", "")).strip()
        if dv or hv:
            payload["date_str"] = _format_dior_datetime(dv, hv)
        elif not payload.get("date_str"):
            payload["date_str"] = example_dates.dior_invoice()
        return payload
    if issuer == "jacquemus":
        payload.setdefault("date_commande", example_dates.jacquemus_date())
        payload.setdefault("heure_commande", example_dates.jacquemus_time())
        payload.setdefault("val_date", example_dates.jacquemus_invoice())
        return payload
    if issuer in ("chanel", "channel"):
        payload.setdefault("date_vente", example_dates.chanel_date())
        payload.setdefault("heure_vente", example_dates.chanel_time())
        return payload
    if issuer == "fred":
        payload.setdefault("date_facture", example_dates.fred_date())
        payload.setdefault("ville_emission", "Neuilly Sur Marne")
        return payload
    if issuer == "nocibe":
        today = example_dates.nocibe_date()
        fnum = str(payload.get("facture_num") or "27414163").strip()
        if fnum and not fnum.upper().startswith("FACTURE"):
            payload["facture_num"] = f"FACTURE n°{fnum}"
        dem = str(payload.get("date_emission") or today).strip()
        if dem and not dem.lower().startswith("du "):
            payload["date_emission"] = f"Du {dem} "
        cdate = str(payload.get("commande_date") or today).strip()
        if cdate and not cdate.lower().startswith("date de commande"):
            payload["commande_date"] = f"Date de commande : {cdate} "
        cmode = str(payload.get("commande_mode") or "Click & Collect").strip()
        if cmode and not cmode.lower().startswith("vous avez opté"):
            payload["commande_mode"] = f"Vous avez opté pour une livraison : {cmode}"
        cexp = str(payload.get("commande_expedition") or today).strip()
        if cexp and not cexp.lower().startswith("date d’") and not cexp.lower().startswith("date d'"):
            payload["commande_expedition"] = f"Date d’épédition/retrait : {cexp} "
        fn = str(payload.get("nom") or "").strip()
        fp = str(payload.get("prenom") or "").strip()
        if (fn or fp) and not payload.get("client_nom"):
            payload["client_nom"] = f"{fn} {fp}".strip() + " "
        if payload.get("adresse") and not payload.get("client_rue"):
            payload["client_rue"] = payload["adresse"]
        fcp = str(payload.get("cp") or "").strip()
        fville = str(payload.get("ville") or "").strip()
        if (fcp or fville) and not payload.get("client_ville"):
            payload["client_ville"] = f"{fcp} {fville}".strip()
        ln = str(payload.get("livraison_nom") or "").strip()
        lp = str(payload.get("livraison_prenom") or "").strip()
        if lp and lp not in ln:
            payload["livraison_nom"] = f"{ln} {lp}".strip() + " "
        if payload.get("livraison_adresse") and not payload.get("livraison_rue"):
            payload["livraison_rue"] = payload["livraison_adresse"]
        lcp = str(payload.get("livraison_cp") or "").strip()
        lville = str(payload.get("livraison_ville") or "").strip()
        if (lcp or lville) and not payload.get("livraison_ville"):
            payload["livraison_ville"] = f"{lcp} {lville}".strip()
        return payload
    if issuer == "boulanger":
        today = example_dates.nocibe_date()
        payload.setdefault("facture_date", today)
        payload.setdefault("facture_time", "19:23")
        return payload
    if issuer == "sfr":
        payload.setdefault("date_facture", "2026-09-01")
        return payload
    return payload


def validate_facture_payload(issuer: str, payload: dict | None) -> None:
    if not payload:
        return
    for k, v in payload.items():
        if not v or not isinstance(v, str):
            continue
        k_lower = k.lower()
        if k_lower == "date_ticket":
            parts = v.strip().split(" ")
            if len(parts) == 2:
                validate_calendar_date(parts[0], "Date ticket")
                validate_time_format(parts[1], "Heure ticket")
            else:
                validate_calendar_date(v, "Date ticket")
            continue
        if ("date" in k_lower or k_lower in ("edition", "val_date", "echeance")) and not k_lower.startswith(("has_", "show_")):
            if v.lower() not in ("true", "false", "none"):
                label = k.replace("_", " ").capitalize()
                validate_calendar_date(v, label)
        elif ("time" in k_lower or "heure" in k_lower) and not k_lower.startswith(("has_", "show_")):
            if v.lower() not in ("true", "false", "none"):
                label = k.replace("_", " ").capitalize()
                validate_time_format(v, label)
    items = payload.get("items")
    if isinstance(items, list):
        for idx, row in enumerate(items):
            if not isinstance(row, dict):
                continue
            for rk, rv in row.items():
                if not rv or not isinstance(rv, str):
                    continue
                rk_lower = rk.lower()
                if "date" in rk_lower or rk_lower == "echeance":
                    validate_calendar_date(rv, f"Ligne {idx + 1} {rk}")
                elif "time" in rk_lower or "heure" in rk_lower:
                    validate_time_format(rv, f"Ligne {idx + 1} {rk}")


def generate_pdf_bytes(issuer: str, data: dict | None = None) -> bytes:
    if issuer not in ISSUERS:
        raise ValueError(f"Émetteur facture inconnu: {issuer}")
    if data:
        validate_facture_payload(issuer, data)
    actual_issuer = "gaz" if issuer == "engie" else ("chanel" if issuer == "channel" else issuer)
    payload = _fill_example_dates(issuer, parse_facture_payload(issuer, data))
    data_mod = importlib.import_module(
        f"app.services.generate_docs.facture.issuers.{actual_issuer}.data"
    )
    gen_mod = importlib.import_module(
        f"app.services.generate_docs.facture.issuers.{actual_issuer}.generate"
    )
    doc = data_mod.from_payload(payload)
    buf = io.BytesIO()
    gen_mod.generate(doc, dest=buf)
    return buf.getvalue()


def generate_preview_jpg_bytes(issuer: str, data: dict | None = None) -> bytes:
    return pdf_bytes_to_watermarked_jpg(generate_pdf_bytes(issuer, data))
