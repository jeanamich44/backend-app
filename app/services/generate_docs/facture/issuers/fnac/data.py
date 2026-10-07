"""Applique un dict éditeur → Doc."""

from dataclasses import dataclass, field

from . import copy as texts
from . import layout, rules


@dataclass
class Item:
    nom: str = texts.PRODUIT
    subtitle: str = texts.SUBTITLE
    ean: str = texts.EAN
    reference: str = texts.REFERENCE
    qte: str = texts.QTE
    pu_ht: str = texts.PU_HT
    pu_ttc: str = texts.PU_TTC
    pu_brut_ht: str = texts.PU_BRUT
    remise_ht: str = texts.REMISE_HT
    serial: str = texts.SERIAL
    distribution: str = texts.DISTRIBUTION
    pieces: str = texts.PIECES
    garantie: str = texts.GARANTIE
    eco_ht: str = texts.ECO_HT
    eco_ttc: str = texts.ECO_TTC


def _default_items() -> list:
    return [Item()]


def _item_from_dict(item: dict) -> Item:
    return Item(
        nom=item.get("nom") or "",
        subtitle=item.get("subtitle") or "",
        ean=item.get("ean") or "",
        reference=item.get("reference") or "",
        qte=item.get("qte") or "",
        pu_ht=item.get("pu_ht") or "",
        pu_ttc=item.get("pu_ttc") or "",
        pu_brut_ht=item.get("pu_brut_ht") or "",
        remise_ht=item.get("remise_ht") or "",
        serial=item.get("serial") or "",
        distribution=item.get("distribution") or "",
        pieces=item.get("pieces") or "",
        garantie=item.get("garantie") or "",
        eco_ht=item.get("eco_ht") or "",
        eco_ttc=item.get("eco_ttc") or "",
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
    livraison_email: str = texts.EMAIL
    livraison_nom: str = texts.CLIENT_NOM
    livraison_adresse: str = texts.ADRESSE
    livraison_cp_ville: str = texts.VILLE
    livraison_pays: str = texts.PAYS_WEB
    facturation_email: str = texts.EMAIL
    facturation_nom: str = texts.CLIENT_NOM
    facturation_adresse: str = texts.ADRESSE
    facturation_cp_ville: str = texts.VILLE
    facturation_pays: str = texts.PAYS_WEB
    store_nom: str = texts.STORE_WEB_NOM
    store_l1: str = texts.STORE_WEB_L1
    store_l2: str = texts.STORE_WEB_L2
    store_l3: str = texts.STORE_WEB_L3
    num_commande: str = texts.NUM_COMMANDE
    date_commande: str = field(default_factory=lambda: texts.DATE_WEB)
    num_facture: str = texts.NUM_FACTURE
    date_facture: str = field(default_factory=lambda: texts.DATE_WEB)
    nref: str = texts.NREF
    matricule: str = texts.MATRICULE
    payment_mode: str = texts.PAYMENT_WEB
    echeance: str = field(default_factory=lambda: texts.DATE_WEB)
    tva_code: str = texts.TVA_CODE_WEB
    tva_rate: str = texts.TVA_RATE
    frais_ht: str = texts.FRAIS_HT
    tva_frais: str = texts.TVA_FRAIS
    pays_expedition: str = texts.SHIP
    total: str = "120.00"
    en_ligne: bool = True
    items: list = field(default_factory=_default_items)


@dataclass
class Visible:
    header: bool = True
    header_logo: bool = True
    header_store: bool = True
    header_order: bool = True
    header_addresses: bool = True
    header_page: bool = True
    middle: bool = True
    middle_columns: bool = True
    middle_rows: bool = True
    middle_ship: bool = True
    middle_vat: bool = True
    middle_totals: bool = True
    footer: bool = True
    footer_legal: bool = True
    footer_help: bool = True


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
    vis.header_store = rules.flag(data, "header_store")
    vis.header_order = rules.flag(data, "header_order")
    vis.header_addresses = rules.flag(data, "header_addresses")
    vis.header_page = rules.flag(data, "header_page")
    vis.middle = rules.flag(data, "middle")
    vis.middle_columns = rules.flag(data, "middle_columns")
    vis.middle_rows = rules.flag(data, "middle_rows")
    vis.middle_ship = rules.flag(data, "middle_ship")
    vis.middle_vat = rules.flag(data, "middle_vat")
    vis.middle_totals = rules.flag(data, "middle_totals")
    vis.footer = rules.flag(data, "footer")
    vis.footer_legal = rules.flag(data, "footer_legal")
    vis.footer_help = rules.flag(data, "footer_help")
    for key in rules.FIELDS:
        if key in data:
            setattr(doc.card, key, data[key])
    if "en_ligne" in data:
        doc.card.en_ligne = rules.as_bool(data["en_ligne"], True)
    if "items" in data:
        doc.card.items = _items_from_payload(data)
    return rules.apply_doc(doc)
