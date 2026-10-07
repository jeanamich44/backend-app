"""Applique un dict éditeur → Doc."""

from dataclasses import dataclass, field

from . import copy as texts
from . import layout, rules


@dataclass
class Item:
    sku: str = texts.SKU
    barcode: str = texts.BARCODE
    desc: str = texts.DESC
    desc2: str = texts.DESC2
    taille: str = texts.TAILLE
    couleur: str = texts.COULEUR
    qte: str = texts.QTE
    prix: str = texts.PRIX


def _default_items() -> list:
    return [Item()]


def _item_from_dict(item: dict) -> Item:
    return Item(
        sku=item.get("sku") or "",
        barcode=item.get("barcode") or "",
        desc=item.get("desc") or "",
        desc2=item.get("desc2") or "",
        taille=item.get("taille") or "",
        couleur=item.get("couleur") or "",
        qte=item.get("qte") or "",
        prix=item.get("prix") or "",
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
    ville: str = texts.VILLE
    cp: str = texts.CP
    pays: str = texts.PAYS
    retrait_magasin: bool = True
    num_commande: str = texts.NUM_COMMANDE
    date_commande: str = field(default_factory=texts.slash_date)
    date_expedition: str = field(default_factory=texts.slash_date)
    payment_mode: str = texts.PAYMENT
    total: str = "80,00"
    items: list = field(default_factory=_default_items)


@dataclass
class Visible:
    header: bool = True
    header_logo: bool = True
    header_title: bool = True
    header_service: bool = True
    header_order: bool = True
    header_addresses: bool = True
    middle: bool = True
    middle_columns: bool = True
    middle_rows: bool = True
    middle_totals: bool = True
    footer: bool = True
    footer_line: bool = True
    footer_payment: bool = True
    footer_notice: bool = True
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
    vis.header_title = rules.flag(data, "header_title")
    vis.header_service = rules.flag(data, "header_service")
    vis.header_order = rules.flag(data, "header_order")
    vis.header_addresses = rules.flag(data, "header_addresses")
    vis.middle = rules.flag(data, "middle")
    vis.middle_columns = rules.flag(data, "middle_columns")
    vis.middle_rows = rules.flag(data, "middle_rows")
    vis.middle_totals = rules.flag(data, "middle_totals")
    vis.footer = rules.flag(data, "footer")
    vis.footer_line = rules.flag(data, "footer_line")
    vis.footer_payment = rules.flag(data, "footer_payment")
    vis.footer_notice = rules.flag(data, "footer_notice")
    vis.footer_legal = rules.flag(data, "footer_legal")
    doc.card.retrait_magasin = rules.flag(data, "retrait_magasin")
    for key in (
        "nom", "adresse", "ville", "cp", "pays",
        "num_commande", "date_commande", "date_expedition", "payment_mode", "total",
    ):
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
    if "items" in data:
        doc.card.items = _items_from_payload(data)
    return rules.apply_doc(doc)
