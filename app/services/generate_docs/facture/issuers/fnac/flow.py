"""Lignes article, hauteur, pagination (tableau à cadre fixe)."""

from dataclasses import dataclass, field

from . import copy as texts
from . import layout, rules
from .paint import wrap_lines


def is_web(doc) -> bool:
    return rules.en_ligne(doc.card)


def footer_kind_for(doc) -> str:
    return rules.footer_kind(doc.card)


def store_lines(card):
    lines = [card.store_nom, card.store_l1, card.store_l2, card.store_l3]
    return [line for line in lines if (line or "").strip()]


def _plain(*parts):
    return [part.strip() for part in parts if (part or "").strip()]


def _mag_lines(email, nom, adresse, cp_ville, x, y0):
    rows = []
    if (email or "").strip():
        rows.append(((email or "").strip(), True, layout.SIZE_9))
    if (nom or "").strip():
        rows.append(((nom or "").strip(), True, layout.SIZE_9))
    if (adresse or "").strip():
        rows.append(((adresse or "").strip(), False, layout.SIZE_9))
    if (cp_ville or "").strip():
        rows.append(((cp_ville or "").strip(), False, layout.SIZE_9))
    lines = [
        (y0 + i * layout.ADDR_PITCH_MAG, text, bold, size)
        for i, (text, bold, size) in enumerate(rows)
    ]
    return x, lines


def _web_livraison(card):
    nom = (card.livraison_nom or "").strip()
    rue = (card.livraison_adresse or "").strip()
    city = " ".join(_plain(card.livraison_cp_ville, card.livraison_pays))
    lines = []
    if nom:
        lines.append((layout.ADDR_LIV_WEB_Y_NOM, nom, True, layout.SIZE_11))
    if rue:
        lines.append((layout.ADDR_LIV_WEB_Y_RUE, rue, False, layout.SIZE_9))
    if city:
        lines.append((layout.ADDR_LIV_WEB_Y_CITY, city, False, layout.SIZE_9))
    return layout.ADDR_TEXT_X, lines


def _web_facturation(card):
    nom = (card.facturation_nom or "").strip()
    rue = (card.facturation_adresse or "").strip()
    ville = (card.facturation_cp_ville or "").strip()
    pays = (card.facturation_pays or "").strip()
    lines = []
    if nom:
        lines.append((layout.ADDR_FAC_WEB_Y_NOM, nom, True, layout.SIZE_11))
    if rue:
        lines.append((layout.ADDR_FAC_WEB_Y_RUE, rue, False, layout.SIZE_9))
    if ville:
        lines.append((layout.ADDR_FAC_WEB_Y_CITY, ville, False, layout.SIZE_9))
    if pays:
        lines.append((layout.ADDR_FAC_WEB_Y_PAYS, pays, False, layout.SIZE_9))
    return layout.ADDR_TEXT_X, lines


def address_columns(card):
    if rules.en_ligne(card):
        return _web_livraison(card), _web_facturation(card)
    liv = _mag_lines(
        card.livraison_email, card.livraison_nom, card.livraison_adresse,
        card.livraison_cp_ville, layout.ADDR_TEXT_X_MAG, layout.ADDR_LIV_TEXT_Y0_MAG,
    )
    fac = _mag_lines(
        card.facturation_email, card.facturation_nom, card.facturation_adresse,
        card.facturation_cp_ville, layout.ADDR_TEXT_X_FAC_MAG, layout.ADDR_FAC_TEXT_Y0_MAG,
    )
    return liv, fac


def desc_font():
    return layout.FONT


def title_lines(item):
    return wrap_lines(
        item.nom, layout.FONT, layout.SIZE_8,
        layout.DESC_RIGHT - layout.DESC_X, layout.MAX_DESC_LINES,
    )


def extra_lines(item, web: bool):
    lines = []
    sub = (item.subtitle or "").strip()
    if sub:
        lines.append((sub, layout.SIZE_8_5, False, "sub"))
    serial = (item.serial or "").strip()
    if serial:
        lines.append((texts.SERIAL_PREFIX + serial, layout.SIZE_8, False, "serial"))
    dist = (item.distribution or "").strip()
    if dist:
        lines.append((dist, layout.SIZE_8, False, "dist"))
    pieces = (item.pieces or "").strip()
    if pieces:
        lines.append((pieces, layout.SIZE_8, False, "pieces"))
    garantie = (item.garantie or "").strip()
    if garantie:
        lines.append((garantie, layout.SIZE_8, False, "garantie"))
    if rules.has_eco(item):
        qte = rules.parse_qty(item.qte)
        ht = qte * rules.parse_money(item.eco_ht)
        ttc = qte * rules.parse_money(item.eco_ttc)
        lines.append((texts.ECO_LABEL, layout.SIZE_8, False, "eco", ht, ttc))
    if web and rules.has_remise(item):
        brut = rules.format_amount(rules.parse_money(item.pu_brut_ht), True)
        rem = rules.format_amount(rules.parse_money(item.remise_ht), True)
        text = f"{texts.REMISE_PREFIX}{brut}{texts.REMISE_MID}{rem}"
        lines.append((text, layout.SIZE_6, False, "remise"))
    return lines


def item_height(item, web: bool) -> float:
    n_title = max(1, len(title_lines(item)))
    extras = extra_lines(item, web)
    h = layout.DESC_DY
    h += (n_title - 1) * layout.TITLE_PITCH
    for extra in extras:
        if extra[3] == "remise":
            h += layout.REMISE_PITCH
        else:
            h += layout.EXTRA_PITCH
    h += layout.VOLUME_GAP_WEB if web else layout.VOLUME_GAP_MAG
    h += layout.ITEM_AFTER_VOLUME
    return h


def table_limit() -> float:
    return layout.TABLE[3] - 12.0


def _take(items, y0, limit, web):
    taken = []
    y = y0
    for i, item in enumerate(items):
        h = item_height(item, web)
        if taken and (y + h) > limit:
            return taken, items[i:], y
        taken.append(item)
        y += h
    return taken, [], y


@dataclass
class PagePlan:
    kind: str
    footer_kind: str
    items: list = field(default_factory=list)
    index: int = 0
    count: int = 1


def paginate(doc) -> list:
    web = is_web(doc)
    foot = footer_kind_for(doc)
    items = list(doc.card.items or ())
    limit = table_limit()
    rest = items
    plans = []
    while True:
        taken, rest, _end = _take(rest, layout.ITEM_Y0, limit, web)
        if not taken and rest:
            taken, rest = [rest[0]], rest[1:]
        plans.append(PagePlan(kind="full", footer_kind=foot, items=taken))
        if not rest:
            break
    if not plans:
        plans.append(PagePlan(kind="full", footer_kind=foot, items=[]))
    for i, plan in enumerate(plans):
        plan.index = i
        plan.count = len(plans)
    return plans
