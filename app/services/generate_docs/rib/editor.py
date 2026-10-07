"""Schéma éditeur par banque : textes, blocs, défauts, règles."""

from __future__ import annotations

import dataclasses
import importlib

from app.services.generate_docs.rib.service import BANKS

_COMMON_IDENTITY = {
    "middle_titulaire_nom",
    "middle_titulaire_rue",
    "middle_titulaire_ville",
    "middle_titulaire_adresse",
    "middle_titulaire_cp",
    "middle_titulaire_pays",
    "middle_banque",
    "middle_etablissement",
    "middle_guichet",
    "middle_compte",
    "middle_cle",
    "middle_iban",
    "middle_iban_text",
    "middle_bic",
    "middle_bic_text",
}

IDENTITY_KEYS: dict[str, set[str]] = {
    "lbp": _COMMON_IDENTITY | {"middle_domiciliation"},
    "ca": _COMMON_IDENTITY
    | {
        "middle_caisse",
        "middle_agence_ville",
        "middle_tel",
        "middle_fax",
        "middle_date",
        "middle_code",
    },
    "sg": _COMMON_IDENTITY | {"middle_agence_text", "middle_agence_rue", "middle_agence_ville"},
    "cm": _COMMON_IDENTITY
    | {
        "middle_agence_text",
        "middle_domiciliation_rue",
        "middle_domiciliation_ville",
        "middle_phone",
        "middle_devise",
    },
    "cic": _COMMON_IDENTITY
    | {
        "middle_agence_text",
        "middle_domiciliation_rue",
        "middle_domiciliation_ville",
        "middle_phone",
        "middle_devise",
    },
    "qonto": _COMMON_IDENTITY | {"middle_account_name"},
    "helios": _COMMON_IDENTITY | {"middle_titulaire_adresse"},
    "lcl": _COMMON_IDENTITY | {"middle_domiciliation_text"},
    "bp": _COMMON_IDENTITY | {"middle_domiciliation_text"},
    "bnp": _COMMON_IDENTITY | {"middle_domiciliation_text"},
    "bfb": _COMMON_IDENTITY | {"header_rue", "header_ville", "header_pays"},
    "ce": _COMMON_IDENTITY | {"middle_domiciliation_rue", "middle_domiciliation_ville"},
    "boursobank": set(_COMMON_IDENTITY),
    "revolut": _COMMON_IDENTITY | {"middle_titulaire_cp", "middle_titulaire_dept"},
    "noelse": _COMMON_IDENTITY | {"middle_titulaire_pays"},
    "sumup": _COMMON_IDENTITY
    | {
        "header_date_text",
        "middle_date_ouverture",
        "middle_institution",
        "middle_titulaire_pays",
        "middle_titulaire_adresse",
    },
    "mypos": _COMMON_IDENTITY
    | {
        "header_date_text",
        "middle_nom_societe",
        "middle_num_enregistrement",
        "middle_adresse",
        "middle_cp_ville",
        "middle_pays",
    },
}

FIELD_LABELS = {
    "header_title_text": "Titre",
    "header_subtitle_text": "Sous-titre",
    "header_notice_fr_text": "Notice (FR)",
    "header_notice_en_text": "Notice (EN)",
    "header_crumb_text": "Fil d'Ariane",
    "header_crumb_link": "Lien du fil d'Ariane",
    "header_date_text": "Date du document",
    "header_rue": "Adresse de l'établissement",
    "header_ville": "Ville de l'établissement",
    "header_pays": "Pays de l'établissement",
    "header_text_content": "Texte d'accompagnement",
    "middle_title_text": "Titre du corps",
    "middle_notice_text": "Notice",
    "middle_titulaire_nom": "Titulaire",
    "middle_titulaire_opt": "Complément titulaire",
    "middle_titulaire_opt1": "Complément d'adresse 1",
    "middle_titulaire_opt2": "Complément d'adresse 2",
    "middle_titulaire_prefix": "Civilité / préfixe",
    "middle_titulaire_rue": "Adresse du titulaire",
    "middle_titulaire_ville": "CP & ville du titulaire",
    "middle_titulaire_cp": "Code postal",
    "middle_titulaire_dept": "Département / région",
    "middle_titulaire_adresse": "Adresse complète du titulaire",
    "middle_titulaire_pays": "Pays du titulaire",
    "middle_account_name": "Nom du compte",
    "middle_agence_text": "Agence",
    "middle_agence_rue": "Adresse de l'agence",
    "middle_agence_ville": "Ville de l'agence",
    "middle_caisse": "Caisse régionale",
    "middle_tel": "Téléphone",
    "middle_fax": "Fax",
    "middle_phone": "Téléphone agence",
    "middle_date": "Date d'édition",
    "middle_code": "Code agence",
    "middle_banque": "Code banque",
    "middle_etablissement": "Code établissement",
    "middle_guichet": "Code guichet",
    "middle_compte": "Numéro de compte",
    "middle_cle": "Clé RIB",
    "middle_iban": "IBAN",
    "middle_iban_text": "IBAN",
    "middle_bic": "BIC",
    "middle_bic_text": "BIC",
    "middle_domiciliation": "Domiciliation",
    "middle_domiciliation_text": "Domiciliation",
    "middle_domiciliation_nom": "Nom de domiciliation",
    "middle_domiciliation_rue": "Adresse de domiciliation",
    "middle_domiciliation_ville": "Ville de domiciliation",
    "middle_domiciliation_pays": "Pays de domiciliation",
    "middle_devise": "Devise",
    "middle_nom_societe": "Nom de la société",
    "middle_num_enregistrement": "N° d'enregistrement",
    "middle_adresse": "Adresse",
    "middle_cp_ville": "CP & ville",
    "middle_pays": "Pays",
    "middle_date_ouverture": "Date d'ouverture",
    "middle_institution": "Institution",
    "footer_line1_text": "Mentions légales (ligne 1)",
    "footer_line2_text": "Mentions légales (ligne 2)",
    "footer_code_text": "Code document",
    "footer_legal_text": "Mentions légales",
    "footer_legal_right_text": "Mentions légales (droite)",
    "footer_page_text": "Pagination",
    "footer_rib_text": "Référence pied de page",
}

BLOCK_LABELS = {
    "header": "En-tête",
    "header_logo": "Logo",
    "header_title": "Titre",
    "header_subtitle": "Sous-titre",
    "header_notice_fr": "Notice FR",
    "header_notice_en": "Notice EN",
    "header_crumb": "Fil d'Ariane",
    "header_date": "Date",
    "header_adresse": "Adresse établissement",
    "header_address": "Adresse établissement",
    "header_text": "Texte d'accompagnement",
    "middle": "Corps du document",
    "middle_logo": "Logo",
    "middle_title": "Titre",
    "middle_notice": "Notice",
    "middle_lines": "Filets / lignes",
    "middle_agence": "Bloc agence",
    "middle_titulaire": "Bloc titulaire",
    "middle_holder": "Bloc titulaire",
    "middle_domiciliation": "Bloc domiciliation",
    "middle_table": "Tableau RIB",
    "middle_iban": "IBAN",
    "middle_bic": "BIC",
    "middle_iban_bic": "IBAN & BIC",
    "middle_swift": "SWIFT",
    "middle_separator": "Séparateur",
    "middle_card": "Carte",
    "middle_account": "Nom du compte",
    "middle_adresse": "Adresse",
    "middle_legend": "Légende",
    "middle_letter": "Lettre / intro",
    "middle_libelle": "Libellés",
    "middle_notes": "Notes",
    "middle_reserved": "Zone réservée",
    "footer": "Pied de page",
    "footer_mentions": "Mentions légales",
    "footer_legal": "Mentions légales",
    "footer_legal_right": "Mentions légales (droite)",
    "footer_page": "Pagination",
    "footer_rib": "Référence RIB",
}

SECTION_TITLES = {
    "header": "En-tête",
    "middle": "Corps",
    "footer": "Pied de page",
}


def _section_of(key: str) -> str:
    if key.startswith("header"):
        return "header"
    if key.startswith("footer"):
        return "footer"
    return "middle"


def _humanize(key: str) -> str:
    text = key
    for prefix in ("header_", "middle_", "footer_"):
        if text.startswith(prefix):
            text = text[len(prefix) :]
            break
    if text.endswith("_text"):
        text = text[: -len("_text")]
    return text.replace("_", " ").strip().capitalize()


def _widget(field_id: str, spec: dict) -> str:
    if field_id in {"header_title_text", "header_subtitle_text"}:
        return "input"
    max_n = spec.get("max") or 0
    charset = spec.get("charset") or "text"
    if charset == "text" and max_n >= 80:
        return "textarea"
    if max_n >= 160:
        return "textarea"
    return "input"


def _bank_modules(bank: str):
    data_mod = importlib.import_module(f"app.services.generate_docs.rib.banks.{bank}.data")
    rules_mod = importlib.import_module(f"app.services.generate_docs.rib.banks.{bank}.rules")
    return data_mod, rules_mod


def editor_schema(bank: str) -> dict:
    data_mod, rules_mod = _bank_modules(bank)
    identity = IDENTITY_KEYS.get(bank, _COMMON_IDENTITY)
    doc = data_mod.Doc()
    fields = []
    defaults: dict[str, str] = {}
    for field_id, spec in rules_mod.FIELDS.items():
        group, attr = rules_mod._DOC_ATTR.get(field_id, (None, None))
        value = ""
        if group and attr:
            obj = getattr(doc, group, None)
            if obj is not None:
                value = getattr(obj, attr, "") or ""
        defaults[field_id] = str(value)
        flabel = FIELD_LABELS.get(field_id) or _humanize(field_id)
        if bank == "bfb":
            if field_id == "header_rue":
                flabel = "Adresse du titulaire"
            elif field_id == "header_ville":
                flabel = "CP & ville du titulaire"
            elif field_id == "header_pays":
                flabel = "Pays du titulaire"
        fields.append(
            {
                "id": field_id,
                "label": flabel,
                "section": _section_of(field_id),
                "min": spec["min"],
                "max": spec["max"],
                "charset": spec["charset"],
                "widget": _widget(field_id, spec),
                "identity": field_id in identity,
            }
        )

    if bank == "noelse" and "middle_titulaire_pays" not in rules_mod.FIELDS:
        fields.append(
            {
                "id": "middle_titulaire_pays",
                "label": FIELD_LABELS["middle_titulaire_pays"],
                "section": "middle",
                "min": 0,
                "max": 40,
                "charset": "text",
                "widget": "input",
                "identity": True,
            }
        )
        defaults["middle_titulaire_pays"] = str(getattr(doc.card, "titulaire_pays", "") or "")

    blocks = []
    visible = {}
    for item in dataclasses.fields(data_mod.Visible):
        visible[item.name] = bool(getattr(doc.visible, item.name))
        blabel = BLOCK_LABELS.get(item.name) or _humanize(item.name)
        if bank == "bfb" and item.name == "header_adresse":
            blabel = "Adresse titulaire"
        elif bank == "sumup" and item.name == "middle_account":
            blabel = "Bloc compte"
        blocks.append(
            {
                "id": item.name,
                "label": blabel,
                "section": _section_of(item.name),
                "master": item.name in {"header", "middle", "footer"},
            }
        )

    return {
        "bank": bank,
        "sections": [
            {"id": key, "label": label}
            for key, label in SECTION_TITLES.items()
            if any(block["section"] == key for block in blocks)
            or any(field["section"] == key for field in fields)
        ],
        "fields": fields,
        "blocks": blocks,
        "defaults": defaults,
        "visible": visible,
    }


def all_editor_schemas() -> dict:
    return {bank: editor_schema(bank) for bank in BANKS}
