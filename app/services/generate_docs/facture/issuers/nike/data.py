"""Applique un dict éditeur → Doc."""

from dataclasses import dataclass, field

from . import copy as texts
from . import layout, rules


@dataclass
class Item:
    sku: str = texts.SKU
    desc: str = texts.DESC
    qte: str = texts.QTE
    brut: str = texts.BRUT
    remise: str = texts.REMISE
    tva: str = texts.TVA


def _default_items() -> list:
    return [
        Item(),
        Item(
            sku=texts.SKU_2,
            desc=texts.DESC_2,
            qte=texts.QTE_2,
            brut=texts.BRUT_2,
            remise=texts.REMISE_2,
            tva=texts.TVA_2,
        ),
    ]


def _item_from_dict(item: dict) -> Item:
    return Item(
        sku=item.get("sku") or "",
        desc=item.get("desc") or "",
        qte=item.get("qte") or "",
        brut=item.get("brut") or "",
        remise=item.get("remise") or "",
        tva=item.get("tva") or "",
    )


def _items_from_payload(data: dict) -> list:
    raw = data.get("items")
    if not isinstance(raw, list):
        return _default_items()
    rows = []
    for item in raw[: layout.MAX_ROWS]:
        if isinstance(item, dict):
            rows.append(_item_from_dict(item))
    return rows


@dataclass
class Card:
    nom: str = texts.CLIENT_NOM
    adresse: str = texts.ADRESSE
    cp_ville: str = texts.CP_VILLE
    pays: str = texts.PAYS
    livraison_adresse: str = texts.LIVRAISON_ADRESSE
    livraison_cp_ville: str = texts.LIVRAISON_CP_VILLE
    livraison_pays: str = texts.LIVRAISON_PAYS
    num_commande: str = texts.NUM_COMMANDE
    num_facture: str = texts.NUM_FACTURE
    date_facture: str = field(default_factory=texts.slash_date)
    date_envoi: str = field(default_factory=texts.slash_date)
    date_echeance: str = field(default_factory=texts.slash_date)
    seller: str = texts.SELLER
    vat: str = texts.VAT
    payment: str = texts.PAY_MODE
    total: str = "219,98"
    items: list = field(default_factory=_default_items)


@dataclass
class Visible:
    header: bool = True
    header_logo: bool = True
    header_brand: bool = True
    header_refs: bool = True
    header_addresses: bool = True
    header_title: bool = True
    middle: bool = True
    middle_columns: bool = True
    middle_rows: bool = True
    middle_totals: bool = True
    footer: bool = True
    footer_seller: bool = True
    footer_notice: bool = True
    footer_page: bool = True


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
    vis.header_brand = rules.flag(data, "header_brand")
    vis.header_refs = rules.flag(data, "header_refs")
    vis.header_addresses = rules.flag(data, "header_addresses")
    vis.header_title = rules.flag(data, "header_title")
    vis.middle = rules.flag(data, "middle")
    vis.middle_columns = rules.flag(data, "middle_columns")
    vis.middle_rows = rules.flag(data, "middle_rows")
    vis.middle_totals = rules.flag(data, "middle_totals")
    vis.footer = rules.flag(data, "footer")
    vis.footer_seller = rules.flag(data, "footer_seller")
    vis.footer_notice = rules.flag(data, "footer_notice")
    vis.footer_page = rules.flag(data, "footer_page")
    for key in (
        "nom", "adresse", "cp_ville", "pays",
        "livraison_adresse", "livraison_cp_ville", "livraison_pays",
        "num_commande", "num_facture",
        "date_facture", "date_envoi", "date_echeance",
        "seller", "vat", "payment", "total",
    ):
        if key in data:
            setattr(doc.card, key, data[key])
    if "items" in data:
        doc.card.items = _items_from_payload(data)
    return rules.apply_doc(doc)
