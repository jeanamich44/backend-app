"""Applique un dict éditeur → Doc."""

from dataclasses import dataclass, field

from . import copy as texts
from . import layout, rules


@dataclass
class Item:
    desc: str = texts.DESC
    qte: str = texts.QTE
    pu: str = texts.PU


def _default_items() -> list[Item]:
    return [Item()]


def _item_from_dict(item: dict) -> Item:
    return Item(
        desc=item.get("desc") or "",
        qte=item.get("qte") or "",
        pu=item.get("pu") or "",
    )


def _items_from_payload(data: dict) -> list[Item]:
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
    adresse: str = texts.ADRESSE
    cp: str = texts.CP
    num_facture: str = texts.NUM_FACTURE
    date_facture: str = field(default_factory=texts.slash_date)
    tva: str = texts.TVA
    total: str = "96,00"
    items: list = field(default_factory=_default_items)


@dataclass
class Visible:
    header: bool = True
    header_logo: bool = True
    header_brand: bool = True
    header_title: bool = True
    header_issuer: bool = True
    header_refs: bool = True
    middle: bool = True
    middle_columns: bool = True
    middle_rows: bool = True
    middle_totals: bool = True
    footer: bool = True
    footer_thanks: bool = True
    footer_sign: bool = True
    footer_line: bool = True


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
    vis.header_title = rules.flag(data, "header_title")
    vis.header_issuer = rules.flag(data, "header_issuer")
    vis.header_refs = rules.flag(data, "header_refs")
    vis.middle = rules.flag(data, "middle")
    vis.middle_columns = rules.flag(data, "middle_columns")
    vis.middle_rows = rules.flag(data, "middle_rows")
    vis.middle_totals = rules.flag(data, "middle_totals")
    vis.footer = rules.flag(data, "footer")
    vis.footer_thanks = rules.flag(data, "footer_thanks")
    vis.footer_sign = rules.flag(data, "footer_sign")
    vis.footer_line = rules.flag(data, "footer_line")
    for key in ("adresse", "cp", "num_facture", "date_facture", "tva", "total"):
        if key in data:
            setattr(doc.card, key, data[key])
    if "items" in data:
        doc.card.items = _items_from_payload(data)
    return rules.apply_doc(doc)
