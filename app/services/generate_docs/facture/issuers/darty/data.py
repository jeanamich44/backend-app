"""Applique un dict éditeur → Doc."""

from dataclasses import dataclass, field

from . import copy as texts
from . import layout, rules


@dataclass
class Item:
    sku: str = texts.SKU
    desc: str = texts.DESC
    desc2: str = texts.DESC2
    qte: str = texts.QTE
    ht: str = texts.HT
    tva: str = texts.TVA
    date_delivrance: str = field(default_factory=texts.slash_date)


def _default_items() -> list:
    return [Item()]


def _item_from_dict(item: dict, fallback: dict | None = None) -> Item:
    src = fallback or {}
    def pick(key, default=""):
        if key in item and item[key] is not None:
            return item[key]
        return src.get(key, default)
    return Item(
        sku=pick("sku", texts.SKU),
        desc=pick("desc", texts.DESC),
        desc2=pick("desc2", texts.DESC2),
        qte=pick("qte", texts.QTE),
        ht=pick("ht", texts.HT),
        tva=pick("tva", texts.TVA),
        date_delivrance=pick("date_delivrance", texts.slash_date()),
    )


def _items_from_payload(data: dict) -> list:
    raw = data.get("items")
    if isinstance(raw, list) and raw:
        rows = []
        for item in raw[: layout.MAX_ROWS]:
            if isinstance(item, dict):
                rows.append(_item_from_dict(item, data))
        if rows:
            return rows
    return [_item_from_dict(data if isinstance(data, dict) else {}, None)]


@dataclass
class Card:
    nom: str = texts.CLIENT_NOM
    adresse: str = texts.ADRESSE
    cp_ville: str = texts.CP_VILLE
    pays: str = texts.PAYS
    livraison_nom: str = texts.CLIENT_NOM
    livraison_adresse: str = texts.ADRESSE
    livraison_cp_ville: str = texts.CP_VILLE
    livraison_pays: str = texts.PAYS
    num_commande: str = texts.NUM_COMMANDE
    date_commande: str = field(default_factory=texts.slash_date)
    date_facture: str = field(default_factory=texts.slash_date)
    payment: str = texts.PAYMENT
    total: str = "478,80"
    items: list = field(default_factory=_default_items)


@dataclass
class Visible:
    header: bool = True
    header_logo: bool = True
    header_issuer: bool = True
    header_addresses: bool = True
    header_title: bool = True
    middle: bool = True
    middle_order: bool = True
    middle_columns: bool = True
    middle_rows: bool = True
    middle_totals: bool = True
    footer: bool = True
    footer_page: bool = True
    footer_legal: bool = True


@dataclass
class Doc:
    card: Card = field(default_factory=Card)
    visible: Visible = field(default_factory=Visible)


def from_payload(data: dict | None) -> Doc:
    data = rules.apply_payload(data)
    doc = Doc()
    vis = doc.visible
    vis.header = rules.flag(data, "header")
    vis.header_logo = rules.flag(data, "header_logo")
    vis.header_issuer = rules.flag(data, "header_issuer")
    vis.header_addresses = rules.flag(data, "header_addresses")
    vis.header_title = rules.flag(data, "header_title")
    vis.middle = rules.flag(data, "middle")
    vis.middle_order = rules.flag(data, "middle_order")
    vis.middle_columns = rules.flag(data, "middle_columns")
    vis.middle_rows = rules.flag(data, "middle_rows")
    vis.middle_totals = rules.flag(data, "middle_totals")
    vis.footer = rules.flag(data, "footer")
    vis.footer_page = rules.flag(data, "footer_page")
    vis.footer_legal = rules.flag(data, "footer_legal")
    for key in FIELDS_KEYS:
        if key in data:
            setattr(doc.card, key, data[key])
    nom_val = str(data.get("nom") or "").strip()
    prenom_val = str(data.get("prenom") or "").strip()
    if nom_val and prenom_val and prenom_val not in nom_val:
        doc.card.nom = f"{nom_val} {prenom_val}"
    elif nom_val:
        doc.card.nom = nom_val
    elif prenom_val:
        doc.card.nom = prenom_val
    l_nom = str(data.get("livraison_nom") or "").strip()
    l_prenom = str(data.get("livraison_prenom") or "").strip()
    if l_nom and l_prenom and l_prenom not in l_nom:
        doc.card.livraison_nom = f"{l_nom} {l_prenom}"
    elif l_nom:
        doc.card.livraison_nom = l_nom
    elif l_prenom:
        doc.card.livraison_nom = l_prenom
    doc.card.items = _items_from_payload(data)
    return rules.apply_doc(doc)


FIELDS_KEYS = (
    "nom", "adresse", "cp_ville", "pays",
    "livraison_nom", "livraison_adresse", "livraison_cp_ville", "livraison_pays",
    "num_commande", "date_commande", "date_facture", "payment", "total",
)
