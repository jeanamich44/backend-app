"""Applique un dict éditeur → Doc."""

from dataclasses import dataclass, field

from . import copy as texts
from . import layout, rules


@dataclass
class Item:
    sku: str = texts.SKU
    desc: str = texts.DESC
    qte: str = texts.QTE
    prix: str = texts.PRIX


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
        prix=pick("prix", texts.PRIX),
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
    num_ticket: str = texts.NUM_TICKET
    ticket_caisse: str = texts.TICKET_CAISSE
    date_ticket: str = field(default_factory=texts.ticket_datetime)
    caissier: str = texts.CAISSIER
    payment: str = texts.PAYMENT
    monnaie: str = texts.MONNAIE_AMT
    tva_rate: str = texts.TVA_RATE
    total: str = "1 250,00"
    items: list = field(default_factory=_default_items)


@dataclass
class Visible:
    header: bool = True
    header_logo: bool = True
    header_store: bool = True
    header_title: bool = True
    header_refs: bool = True
    middle: bool = True
    middle_columns: bool = True
    middle_rows: bool = True
    middle_totals: bool = True
    middle_pay: bool = True
    middle_line: bool = True


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
    vis.header_title = rules.flag(data, "header_title")
    vis.header_refs = rules.flag(data, "header_refs")
    vis.middle = rules.flag(data, "middle")
    vis.middle_columns = rules.flag(data, "middle_columns")
    vis.middle_rows = rules.flag(data, "middle_rows")
    vis.middle_totals = rules.flag(data, "middle_totals")
    vis.middle_pay = rules.flag(data, "middle_pay")
    vis.middle_line = rules.flag(data, "middle_line")
    for key in FIELDS_KEYS:
        if key in data:
            setattr(doc.card, key, data[key])
    doc.card.items = _items_from_payload(data)
    return rules.apply_doc(doc)


FIELDS_KEYS = (
    "num_ticket", "ticket_caisse", "date_ticket", "caissier",
    "payment", "monnaie", "tva_rate", "total",
)
