from dataclasses import dataclass, field
from . import copy as texts
from . import layout, rules

# ----------------------------------------------------------------------

@dataclass
class Item:
    numero_ligne: str = texts.ITEM_NUM_LIGNE
    description: str = texts.ITEM_DESCRIPTION
    date: str = texts.ITEM_DATE
    montant_ttc: str = texts.ITEM_MONTANT_TTC

# ----------------------------------------------------------------------

def _default_items() -> list[Item]:
    return [Item()]

# ----------------------------------------------------------------------

def _item_from_dict(d: dict) -> Item:
    return Item(
        numero_ligne=str(d.get("numero_ligne", "") or ""),
        description=str(d.get("description", "") or ""),
        date=str(d.get("date", "") or ""),
        montant_ttc=str(d.get("montant_ttc", "") or ""),
    )

# ----------------------------------------------------------------------

def _items_from_payload(data: dict) -> list[Item]:
    raw = data.get("items")
    if not isinstance(raw, list):
        return _default_items()
    out = []
    for it in raw[: layout.MAX_ITEMS]:
        if isinstance(it, dict):
            out.append(_item_from_dict(it))
    return out or _default_items()

# ----------------------------------------------------------------------

@dataclass
class Card:
    nom: str = texts.NOM
    prenom: str = texts.PRENOM
    adresse: str = texts.RECIPIENT_ADRESSE
    cp: str = "75011"
    ville: str = "Paris"
    service_faq_url: str = texts.SERVICE_URL
    service_phone: str = texts.SERVICE_PHONE
    service_siege: str = texts.SERVICE_SIEGE
    company_name: str = texts.COMPANY_SERVICE
    company_address: str = texts.COMPANY_ADDRESS
    company_capital_rcs: str = texts.COMPANY_CAPITAL
    company_tva_ape: str = texts.COMPANY_TVA
    titulaire_ligne: str = texts.ACCOUNT_TITULAIRE_NAME
    num_compte_client: str = texts.ACCOUNT_COMPTE_NUM
    date_facture: str = "2026-09-01"
    num_facture: str = "169793"
    destinataire_nom: str = texts.RECIPIENT_NOM
    destinataire_adresse: str = texts.RECIPIENT_ADRESSE
    destinataire_cp_ville: str = texts.RECIPIENT_CP_VILLE
    montant_ht: str = "6.25"
    montant_tva: str = "1.25"
    taux_tva: str = "20.0 %"
    total_ttc: str = "7.50"
    solde_ht: str = "0.00"
    solde_ttc: str = "0.00"
    net_a_payer_ht: str = "6.25"
    net_a_payer_ttc: str = "7.50"
    items: list[Item] = field(default_factory=_default_items)
    total_facture_ht: str = texts.TOTAL_HT_VAL
    total_facture_ttc: str = texts.TOTAL_TTC_VAL
    mention_encaissement: str = texts.TVA_ENCAISSEMENT
    footer_note: str = texts.FOOTER_NOTE
    sepa_ligne1: str = texts.FOOTER_SEPA_L1
    sepa_ligne2: str = texts.FOOTER_SEPA_L2

# ----------------------------------------------------------------------

@dataclass
class Visible:
    header: bool = True
    header_logo: bool = True
    header_service: bool = True
    header_company: bool = True
    header_account: bool = True
    header_recipient: bool = True
    middle: bool = True
    middle_recap: bool = True
    middle_banner: bool = True
    middle_table: bool = True
    footer: bool = True
    footer_notes: bool = True
    footer_sepa: bool = True

# ----------------------------------------------------------------------

@dataclass
class Doc:
    card: Card = field(default_factory=Card)
    visible: Visible = field(default_factory=Visible)

# ----------------------------------------------------------------------

def from_payload(data: dict | None) -> Doc:
    data = rules.apply_payload(data)
    doc = Doc()
    vis = doc.visible
    vis.header = rules.flag(data, "header")
    vis.header_logo = rules.flag(data, "header_logo")
    vis.header_service = rules.flag(data, "header_service")
    vis.header_company = rules.flag(data, "header_company")
    vis.header_account = rules.flag(data, "header_account")
    vis.header_recipient = rules.flag(data, "header_recipient")
    vis.middle = rules.flag(data, "middle")
    vis.middle_recap = rules.flag(data, "middle_recap")
    vis.middle_banner = rules.flag(data, "middle_banner")
    vis.middle_table = rules.flag(data, "middle_table")
    vis.footer = rules.flag(data, "footer")
    vis.footer_notes = rules.flag(data, "footer_notes")
    vis.footer_sepa = rules.flag(data, "footer_sepa")

    keys = (
        "nom", "prenom", "adresse", "cp", "ville",
        "service_faq_url", "service_phone", "service_siege",
        "company_name", "company_address", "company_capital_rcs", "company_tva_ape",
        "titulaire_ligne", "num_compte_client", "date_facture", "num_facture",
        "destinataire_nom", "destinataire_adresse", "destinataire_cp_ville",
        "montant_ht", "montant_tva", "taux_tva", "total_ttc",
        "solde_ht", "solde_ttc", "net_a_payer_ht", "net_a_payer_ttc",
        "total_facture_ht", "total_facture_ttc", "mention_encaissement",
        "footer_note", "sepa_ligne1", "sepa_ligne2",
    )
    for k in keys:
        if k in data:
            setattr(doc.card, k, str(data[k]))

    if "items" in data and isinstance(data["items"], list):
        doc.card.items = _items_from_payload(data)
    elif any(k in data for k in ("item_description", "item_date", "item_montant_ttc", "item_numero_ligne")):
        it = doc.card.items[0]
        if "item_description" in data:
            it.description = str(data["item_description"])
        if "item_date" in data:
            it.date = str(data["item_date"])
        if "item_montant_ttc" in data:
            it.montant_ttc = str(data["item_montant_ttc"])
        if "item_numero_ligne" in data:
            it.numero_ligne = str(data["item_numero_ligne"])

    return rules.apply_doc(doc)
