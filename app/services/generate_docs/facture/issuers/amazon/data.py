"""Applique un dict éditeur → Doc."""

from dataclasses import dataclass, field

from . import copy as texts
from . import layout, rules


@dataclass
class Item:
    nom: str = texts.PRODUIT
    note: str = texts.NOTE_PIECES
    qte: str = texts.QTE
    pu_ht: str = texts.PU_HT
    pu_ttc: str = texts.PU_TTC
    asin: str = texts.ASIN


def _default_items() -> list:
    return [Item()]


def _item_from_dict(item: dict) -> Item:
    return Item(
        nom=item.get("nom") or "",
        note=item.get("note") or "",
        qte=item.get("qte") or "",
        pu_ht=item.get("pu_ht") or "",
        pu_ttc=item.get("pu_ttc") or "",
        asin=item.get("asin") or "",
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
    cp_ville: str = texts.VILLE_DEPT
    pays: str = texts.PAYS
    livraison_nom: str = texts.CLIENT_NOM
    livraison_adresse: str = texts.ADRESSE
    livraison_cp_ville: str = texts.VILLE
    livraison_pays: str = texts.PAYS
    seller_nom: str = texts.SELLER_AMZ
    seller_adresse: str = texts.SELLER_AMZ_ADDR
    seller_adresse2: str = ""
    seller_cp_ville: str = texts.SELLER_AMZ_CITY
    seller_pays: str = texts.SELLER_AMZ_PAYS
    seller_tva: str = texts.SELLER_AMZ_TVA
    payment_ref: str = texts.PAYMENT_REF
    num_facture: str = texts.NUM_FACTURE_AMZ
    date_facture: str = field(default_factory=lambda: texts.DATE_FACTURE)
    total: str = texts.TOTAL
    num_commande: str = texts.NUM_COMMANDE
    date_commande: str = field(default_factory=lambda: texts.DATE_COMMANDE)
    expedition_ht: str = texts.EXPEDITION_HT
    expedition_ttc: str = texts.EXPEDITION_TTC
    remise_ht: str = texts.REMISE_HT
    remise_ttc: str = texts.REMISE_TTC
    tva_rate: str = texts.TVA_TEXT
    sold_by_amazon: bool = True
    items: list = field(default_factory=_default_items)


@dataclass
class Visible:
    header: bool = True
    header_logo: bool = True
    header_title: bool = True
    header_identity: bool = True
    header_pay: bool = True
    header_contact: bool = True
    header_addresses: bool = True
    header_order: bool = True
    middle: bool = True
    middle_columns: bool = True
    middle_rows: bool = True
    middle_totals: bool = True
    middle_vat: bool = True
    footer: bool = True
    footer_line: bool = True
    footer_legal: bool = True
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
    vis.header_title = rules.flag(data, "header_title")
    vis.header_identity = rules.flag(data, "header_identity")
    vis.header_pay = rules.flag(data, "header_pay")
    vis.header_contact = rules.flag(data, "header_contact")
    vis.header_addresses = rules.flag(data, "header_addresses")
    vis.header_order = rules.flag(data, "header_order")
    vis.middle = rules.flag(data, "middle")
    vis.middle_columns = rules.flag(data, "middle_columns")
    vis.middle_rows = rules.flag(data, "middle_rows")
    vis.middle_totals = rules.flag(data, "middle_totals")
    vis.middle_vat = rules.flag(data, "middle_vat")
    vis.footer = rules.flag(data, "footer")
    vis.footer_line = rules.flag(data, "footer_line")
    vis.footer_legal = rules.flag(data, "footer_legal")
    vis.footer_page = rules.flag(data, "footer_page")
    for key in rules.FIELDS:
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
    if "sold_by_amazon" in data:
        doc.card.sold_by_amazon = rules.as_bool(data["sold_by_amazon"], True)
    if "items" in data:
        doc.card.items = _items_from_payload(data)
    return rules.apply_doc(doc)
