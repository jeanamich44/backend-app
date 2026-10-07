"""Applique un dict éditeur → Doc."""

from dataclasses import dataclass, field

from . import copy as texts
from . import layout, rules


@dataclass
class Item:
    sku: str = texts.SKU
    desc: str = texts.DESC
    qte: str = texts.QTE
    pu: str = texts.PU
    tva: str = texts.TVA


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
        qte=pick("qte", texts.QTE),
        pu=pick("pu", texts.PU),
        tva=pick("tva", texts.TVA),
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
    adresse: str = texts.ADRESSE_BILL
    cp_ville: str = texts.CP_BILL
    pays: str = texts.PAYS
    livraison_nom: str = texts.CLIENT_NOM
    livraison_societe: str = texts.SOCIETE
    livraison_adresse: str = texts.ADRESSE_SHIP
    livraison_cp_ville: str = texts.CP_SHIP
    livraison_pays: str = texts.PAYS
    num_facture: str = texts.NUM_FACTURE
    date_facture: str = field(default_factory=texts.slash_date)
    num_commande: str = texts.NUM_COMMANDE
    date_commande: str = field(default_factory=texts.slash_date)
    payment: str = texts.PAYMENT
    transporteur: str = texts.TRANSPORTEUR
    frais: str = texts.FRAIS
    total: str = "95,88"
    items: list = field(default_factory=_default_items)


@dataclass
class Visible:
    header: bool = True
    header_logo: bool = True
    header_title: bool = True
    header_addresses: bool = True
    middle: bool = True
    middle_refs: bool = True
    middle_columns: bool = True
    middle_rows: bool = True
    middle_tax: bool = True
    middle_totals: bool = True
    middle_pay: bool = True
    footer: bool = True
    footer_returns: bool = True
    footer_issuer: bool = True
    footer_tcpdf: bool = True


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
    vis.header_title = rules.flag(data, "header_title")
    vis.header_addresses = rules.flag(data, "header_addresses")
    vis.middle = rules.flag(data, "middle")
    vis.middle_refs = rules.flag(data, "middle_refs")
    vis.middle_columns = rules.flag(data, "middle_columns")
    vis.middle_rows = rules.flag(data, "middle_rows")
    vis.middle_tax = rules.flag(data, "middle_tax")
    vis.middle_totals = rules.flag(data, "middle_totals")
    vis.middle_pay = rules.flag(data, "middle_pay")
    vis.footer = rules.flag(data, "footer")
    vis.footer_returns = rules.flag(data, "footer_returns")
    vis.footer_issuer = rules.flag(data, "footer_issuer")
    vis.footer_tcpdf = rules.flag(data, "footer_tcpdf")
    for key in FIELDS_KEYS:
        if key in data:
            setattr(doc.card, key, data[key])
    doc.card.items = _items_from_payload(data)
    return rules.apply_doc(doc)


FIELDS_KEYS = (
    "nom", "adresse", "cp_ville", "pays",
    "livraison_nom", "livraison_societe", "livraison_adresse",
    "livraison_cp_ville", "livraison_pays",
    "num_facture", "date_facture",
    "num_commande", "date_commande",
    "payment", "transporteur", "frais", "total",
)
