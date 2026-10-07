"""Empilement dynamique header / lignes / pagination (amazon2 + amazon3)."""

from dataclasses import dataclass, field

from . import copy as texts
from . import layout, rules
from .paint import wrap_lines


def is_amazon(doc) -> bool:
    return rules.sold_by_amazon(doc.card)


def footer_kind_for(doc) -> str:
    return rules.footer_kind(doc.card)


def footer_spec(kind: str):
    if kind == rules.FOOTER_EU:
        return (
            layout.FOOTER_EU_RULE_Y,
            layout.FOOTER_EU_Y,
            layout.FOOTER_EU_PAGE_Y,
            texts.LEGAL_EU,
        )
    return (
        layout.FOOTER_OSS_RULE_Y,
        layout.FOOTER_OSS_Y,
        layout.FOOTER_OSS_PAGE_Y,
        texts.LEGAL_OSS,
    )


def legal_lines(doc):
    return footer_spec(footer_kind_for(doc))[3]


def footer_ys(doc):
    rule_y, legal_ys, page_y, _lines = footer_spec(footer_kind_for(doc))
    return rule_y, legal_ys, page_y


def content_max(doc) -> float:
    if not doc.visible.footer:
        return layout.PAGE_H - 18.0
    rule_y, _legal, _page_y = footer_ys(doc)
    return rule_y - 6.0


def address_columns(card):
    bill = [card.nom, card.adresse, card.cp_ville, card.pays]
    ship = [
        card.livraison_nom, card.livraison_adresse,
        card.livraison_cp_ville, card.livraison_pays,
    ]
    seller = [card.seller_nom, card.seller_adresse]
    extra = (card.seller_adresse2 or "").strip()
    if extra:
        seller.append(extra)
    seller.append(card.seller_cp_ville)
    seller.append(card.seller_pays)
    tva = (card.seller_tva or "").strip()
    if tva:
        seller.append(texts.PAY_TVA_PREFIX + tva)
    return (
        [line for line in bill if (line or "").strip()],
        [line for line in ship if (line or "").strip()],
        [line for line in seller if (line or "").strip()],
    )


def desc_lines(item):
    return wrap_lines(
        item.nom, layout.FONT_UNI, layout.SIZE_SMALL,
        layout.DESC_MAX_W, layout.MAX_DESC_LINES,
    )


def item_content(item):
    lines = [(line, "desc") for line in desc_lines(item)]
    note = (item.note or "").strip()
    if note:
        lines.append((note, "note"))
    asin = (item.asin or "").strip()
    if asin:
        lines.append((texts.ASIN_PREFIX + asin, "asin"))
    if not lines:
        lines = [("", "desc")]
    return lines


def item_height(item) -> float:
    n = max(1, len(item_content(item)))
    return layout.ITEM_PAD_TOP + (n - 1) * layout.DESC_PITCH + layout.ITEM_PAD_BOT


def extra_keys(card):
    keys = ["expedition"]
    if rules.has_remise(card):
        keys.append("remise")
    return keys


def extras_grand_height(card, visible_totals: bool) -> float:
    if not visible_totals:
        return 0.0
    n = len(extra_keys(card))
    return layout.EXTRA_GAP + max(0, n - 1) * layout.EXTRA_PITCH + layout.GRAND_DY


def vat_block_height() -> float:
    return layout.VAT_AFTER_GRAND + layout.VAT_RATE_DY + layout.VAT_TOTAL_DY


def header_stack(doc) -> dict:
    card = doc.card
    vis = doc.visible
    bill, ship, seller = address_columns(card)
    if vis.header_addresses:
        n = max(len(bill), len(ship), len(seller), 1)
        last = layout.COL_DATA_Y0 + (n - 1) * layout.COL_PITCH
        addr_rule = last + layout.AFTER_ADDR
    else:
        addr_rule = layout.CONTACT_RULE_Y
    if vis.header_order:
        order_title = addr_rule + layout.AFTER_ADDR_RULE
        order_date = order_title + layout.ORDER_DATE_DY
        order_num = order_date + layout.ORDER_NUM_DY
        order_rule = order_num + layout.AFTER_ORDER
    else:
        order_title = addr_rule
        order_date = addr_rule
        order_num = addr_rule
        order_rule = addr_rule
    details = order_rule + layout.DETAILS_DY
    head_rule = order_rule + layout.HEAD_RULE_DY
    col_head = details + layout.COL_HEAD_DY
    col_sub = col_head + layout.COL_SUB_DY
    band0 = col_head + layout.BAND_DY
    return {
        "addr_rule": addr_rule,
        "order_title": order_title,
        "order_date": order_date,
        "order_num": order_num,
        "order_rule": order_rule,
        "details": details,
        "head_rule": head_rule,
        "col_head": col_head,
        "col_sub": col_sub,
        "band0": band0,
        "bill": bill,
        "ship": ship,
        "seller": seller,
    }


def continuation_table() -> dict:
    details = layout.VAT_P2_Y
    col_head = details + layout.COL_HEAD_DY
    return {
        "details": details,
        "head_rule": details + (layout.HEAD_RULE_DY - layout.DETAILS_DY),
        "col_head": col_head,
        "col_sub": col_head + layout.COL_SUB_DY,
        "band0": col_head + layout.BAND_DY,
    }


def _take(items, y0, limit, reserved):
    taken = []
    y = y0
    for i, item in enumerate(items):
        h = item_height(item)
        if taken and (y + h + reserved) > limit:
            return taken, items[i:], y
        taken.append(item)
        y += h
    return taken, [], y


def _fits(end, extra, limit) -> bool:
    return extra <= 0 or (end + extra) <= limit


@dataclass
class PagePlan:
    kind: str
    footer_kind: str
    full: bool
    items: list = field(default_factory=list)
    extras: bool = False
    grand: bool = False
    vat: bool = False
    columns: bool = False
    band_y0: float = 0.0
    header: dict = field(default_factory=dict)
    index: int = 0
    count: int = 1


def _plan(kind, footer_kind, **kwargs):
    return PagePlan(
        kind=kind,
        footer_kind=footer_kind,
        full=(kind == "full"),
        **kwargs,
    )


def _split_page1(items, band0, limit, tail, vat_h, amazon, show_tot, show_vat):
    vat_try = amazon and show_vat
    page1, rest, end1 = _take(items, band0, limit, tail + (vat_h if vat_try else 0.0))
    if not rest:
        extras = show_tot and _fits(end1, tail, limit)
        vat = vat_try and extras and _fits(end1, tail + vat_h, limit)
        return page1, rest, extras, vat
    page1, rest, end1 = _take(items, band0, limit, tail)
    if not rest:
        extras = show_tot and _fits(end1, tail, limit)
        return page1, rest, extras, False
    page1, rest, end1 = _take(items, band0, limit, 0.0)
    return page1, rest, False, False


def paginate(doc) -> list:
    card = doc.card
    vis = doc.visible
    header = header_stack(doc)
    limit = content_max(doc)
    amazon = is_amazon(doc)
    foot = footer_kind_for(doc)
    show_tot = vis.middle_totals
    show_vat = vis.middle_vat
    tail = extras_grand_height(card, show_tot)
    vat_h = vat_block_height() if show_vat else 0.0
    items = list(card.items or ())
    band0 = header["band0"]
    page1, rest, extras_on_1, vat_on_1 = _split_page1(
        items, band0, limit, tail, vat_h, amazon, show_tot, show_vat,
    )
    plans = [
        _plan(
            "full", foot,
            items=page1,
            extras=extras_on_1,
            grand=extras_on_1,
            vat=vat_on_1,
            columns=True,
            band_y0=band0,
            header=header,
        ),
    ]
    while rest:
        cont = continuation_table()
        taken, rest, band_end = _take(rest, cont["band0"], limit, tail)
        if not taken and rest:
            taken, rest = [rest[0]], rest[1:]
            band_end = cont["band0"] + item_height(taken[0])
        last = not rest
        extras_here = last and show_tot and _fits(band_end, tail, limit)
        vat_here = (
            last and show_vat and extras_here
            and _fits(band_end, tail + vat_h, limit)
        )
        plans.append(
            _plan(
                "continue", foot,
                items=taken,
                extras=extras_here,
                grand=extras_here,
                vat=vat_here,
                columns=True,
                band_y0=cont["band0"],
                header=cont,
            ),
        )
    if show_tot and not any(plan.extras for plan in plans):
        extras_y = layout.VAT_P2_Y
        vat_here = show_vat and _fits(extras_y, tail + vat_h, limit)
        plans.append(
            _plan(
                "totals", foot,
                items=[],
                extras=True,
                grand=True,
                vat=vat_here,
                columns=False,
                band_y0=extras_y,
                header={},
            ),
        )
    if show_vat and not any(plan.vat for plan in plans):
        plans.append(
            _plan(
                "vat", foot,
                items=[],
                extras=False,
                grand=False,
                vat=True,
                columns=False,
                band_y0=layout.VAT_P2_Y,
                header={},
            ),
        )
    for i, plan in enumerate(plans):
        plan.index = i
        plan.count = len(plans)
    return plans
