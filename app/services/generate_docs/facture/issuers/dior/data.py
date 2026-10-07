import re
from dataclasses import dataclass, field
from . import copy

# ----------------------------------------------------------------------

@dataclass
class Visible:
    header: bool = True
    header_bg: bool = True
    header_logo: bool = True
    header_duplicata: bool = True
    header_line: bool = True
    header_contact: bool = True
    header_client: bool = True
    header_meta: bool = True
    middle: bool = True
    middle_page: bool = True
    middle_vendeur: bool = True
    middle_articles: bool = True
    middle_line: bool = True
    middle_totals: bool = True
    middle_pay: bool = True
    middle_code: bool = True
    footer: bool = True
    footer_legal: bool = True

# ----------------------------------------------------------------------

@dataclass
class Header:
    duplicata: str = copy.DUPLICATA
    contact_line_0: str = copy.CONTACT_LINES[0]
    contact_line_1: str = copy.CONTACT_LINES[1]
    contact_line_2: str = copy.CONTACT_LINES[2]
    contact_line_3: str = copy.CONTACT_LINES[3]
    contact_line_4: str = copy.CONTACT_LINES[4]
    client_nom: str = copy.CLIENT_NOM
    client_email: str = copy.CLIENT_EMAIL
    client_tel: str = copy.CLIENT_TEL
    vente_title: str = copy.VENTE_TITLE
    oper: str = copy.OPER
    trans: str = copy.TRANS
    store: str = copy.STORE
    store_num: str = copy.STORE_NUM
    date_str: str = copy.DATE_STR

# ----------------------------------------------------------------------

@dataclass
class Item:
    ref: str = copy.ARTICLE_REF
    desc: str = copy.ARTICLE_DESC
    qty: str = copy.ARTICLE_QTY
    unit_price: str = copy.ARTICLE_UNIT_PRICE
    total: str = copy.ARTICLE_TOTAL

# ----------------------------------------------------------------------

@dataclass
class Middle:
    page_info: str = copy.PAGE_INFO
    vendeur: str = copy.VENDEUR
    items: list[Item] = field(default_factory=lambda: [Item()])
    count_label: str = copy.ARTICLE_COUNT
    total_facture: str = copy.TOTAL_FACTURE
    payment_method: str = copy.PAYMENT_METHOD
    payment_amount: str = copy.PAYMENT_AMOUNT
    rendu_amount: str = copy.RENDU_AMOUNT
    total_ht: str = copy.TOTAL_HT
    tva_product: str = copy.TVA_PRODUCT
    tva_rate: str = copy.TVA_RATE
    tva_amount: str = copy.TVA_AMOUNT
    total_ttc: str = copy.TOTAL_TTC
    code: str = copy.CODE

    @property
    def article_ref(self) -> str:
        return self.items[0].ref if self.items else copy.ARTICLE_REF

    @property
    def article_desc(self) -> str:
        return self.items[0].desc if self.items else copy.ARTICLE_DESC

    @property
    def article_qty(self) -> str:
        return self.items[0].qty if self.items else copy.ARTICLE_QTY

    @property
    def article_unit_price(self) -> str:
        return self.items[0].unit_price if self.items else copy.ARTICLE_UNIT_PRICE

    @property
    def article_total(self) -> str:
        return self.items[0].total if self.items else copy.ARTICLE_TOTAL

# ----------------------------------------------------------------------

@dataclass
class Footer:
    line_0: str = copy.LEGAL_LINE_0
    line_1: str = copy.LEGAL_LINE_1
    line_2: str = copy.LEGAL_LINE_2
    line_3: str = copy.LEGAL_LINE_3
    line_4: str = copy.LEGAL_LINE_4

# ----------------------------------------------------------------------

@dataclass
class FactureDior:
    visible: Visible = field(default_factory=Visible)
    header: Header = field(default_factory=Header)
    middle: Middle = field(default_factory=Middle)
    footer: Footer = field(default_factory=Footer)

# ----------------------------------------------------------------------

Doc = FactureDior

# ----------------------------------------------------------------------

def _items_from_payload(d: dict) -> list[Item]:
    raw = d.get("items")
    if isinstance(raw, list) and len(raw) > 0:
        res = []
        for it in raw[:3]:
            if isinstance(it, dict):
                ref = str(it.get("ref", it.get("article_ref", copy.ARTICLE_REF)))
                desc = str(it.get("desc", it.get("article_desc", copy.ARTICLE_DESC)))
                qty = str(it.get("qty", it.get("article_qty", copy.ARTICLE_QTY)))
                unit = str(it.get("unit_price", it.get("prix", it.get("article_unit_price", copy.ARTICLE_UNIT_PRICE))))
                tot = str(it.get("total", it.get("article_total", copy.ARTICLE_TOTAL)))
                res.append(Item(ref=ref, desc=desc, qty=qty, unit_price=unit, total=tot))
        if res:
            return res
    return [
        Item(
            ref=str(d.get("article_ref", copy.ARTICLE_REF)),
            desc=str(d.get("article_desc", copy.ARTICLE_DESC)),
            qty=str(d.get("article_qty", copy.ARTICLE_QTY)),
            unit_price=str(d.get("article_unit_price", copy.ARTICLE_UNIT_PRICE)),
            total=str(d.get("article_total", copy.ARTICLE_TOTAL)),
        )
    ]

# ----------------------------------------------------------------------

def _as_bool(val, default: bool = True) -> bool:
    if val is None:
        return default
    if isinstance(val, bool):
        return val
    if isinstance(val, str):
        return val.strip().lower() not in ("false", "0", "off", "no", "")
    return bool(val)

# ----------------------------------------------------------------------

def _to_float(val, default: float = 0.0) -> float:
    if val is None:
        return default
    if isinstance(val, (int, float)):
        return float(val)
    s = str(val).strip().replace(" ", "").replace("\u00a0", "").replace("€", "").replace(",", ".")
    try:
        return float(s)
    except (ValueError, TypeError):
        return default

# ----------------------------------------------------------------------

def _format_money(val: float) -> str:
    return f"{val:,.2f}".replace(",", " ").replace(".", ",").replace(" ", " ")

# ----------------------------------------------------------------------

def from_payload(data: dict | None) -> FactureDior:
    d = dict(data) if data else {}
    if isinstance(d.get("visible"), dict):
        d.update(d["visible"])
    vis = Visible(
        header=_as_bool(d.get("header"), True),
        header_bg=_as_bool(d.get("header_bg", d.get("chrome_bg")), True),
        header_logo=_as_bool(d.get("header_logo"), True),
        header_duplicata=_as_bool(d.get("header_duplicata"), True),
        header_line=_as_bool(d.get("header_line"), True),
        header_contact=_as_bool(d.get("header_contact"), True),
        header_client=_as_bool(d.get("header_client"), True),
        header_meta=_as_bool(d.get("header_meta"), True),
        middle=_as_bool(d.get("middle"), True),
        middle_page=_as_bool(d.get("middle_page"), True),
        middle_vendeur=_as_bool(d.get("middle_vendeur"), True),
        middle_articles=_as_bool(d.get("middle_articles"), True),
        middle_line=_as_bool(d.get("middle_line"), True),
        middle_totals=_as_bool(d.get("middle_totals"), True),
        middle_pay=_as_bool(d.get("middle_pay"), True),
        middle_code=_as_bool(d.get("middle_code"), True),
        footer=_as_bool(d.get("footer"), True),
        footer_legal=_as_bool(d.get("footer_legal"), True),
    )
    nom_val = str(d.get("nom", "")).strip()
    prenom_val = str(d.get("prenom", "")).strip()
    civ_val = str(d.get("civilite", copy.CIVILITE)).strip()
    if nom_val and prenom_val:
        client_nom_val = f"{civ_val} {nom_val.upper()} {prenom_val}".strip() if civ_val else f"{nom_val.upper()} {prenom_val}".strip()
    elif nom_val:
        client_nom_val = f"{civ_val} {nom_val.upper()}".strip() if civ_val else nom_val.upper()
    elif prenom_val:
        client_nom_val = f"{civ_val} {prenom_val}".strip() if civ_val else prenom_val
    else:
        client_nom_val = str(d.get("client_nom", copy.CLIENT_NOM)).strip()

    tel_raw = str(d.get("client_tel", copy.CLIENT_TEL)).strip()
    tel_digits = re.sub(r"\D", "", tel_raw)
    if len(tel_digits) == 10:
        client_tel_val = ".".join(tel_digits[i:i+2] for i in range(0, 10, 2))
    else:
        client_tel_val = tel_raw

    hdr = Header(
        duplicata=str(d.get("duplicata", copy.DUPLICATA)),
        contact_line_0=str(d.get("contact_line_0", copy.CONTACT_LINES[0])),
        contact_line_1=str(d.get("contact_line_1", copy.CONTACT_LINES[1])),
        contact_line_2=str(d.get("contact_line_2", copy.CONTACT_LINES[2])),
        contact_line_3=str(d.get("contact_line_3", copy.CONTACT_LINES[3])),
        contact_line_4=str(d.get("contact_line_4", copy.CONTACT_LINES[4])),
        client_nom=client_nom_val,
        client_email=str(d.get("client_email", copy.CLIENT_EMAIL)),
        client_tel=client_tel_val,
        vente_title=str(d.get("vente_title", copy.VENTE_TITLE)),
        oper=str(d.get("oper", copy.OPER)),
        trans=str(d.get("trans", copy.TRANS)),
        store=str(d.get("store", copy.STORE)),
        store_num=str(d.get("store_num", copy.STORE_NUM)),
        date_str=str(d.get("date_str", copy.DATE_STR)),
    )
    items_list = _items_from_payload(d)
    total_qty = 0
    sum_items = 0.0
    for it in items_list:
        try:
            q = int(str(it.qty).strip())
            total_qty += max(1, q)
        except (ValueError, TypeError):
            total_qty += 1
            q = 1
        it_tot = _to_float(it.total)
        if it_tot <= 0.0:
            it_tot = q * _to_float(it.unit_price)
        sum_items += it_tot

    count_val = f"{total_qty} produit(s)"

    user_ttc = None
    if "total_ttc" in d and str(d["total_ttc"]).strip():
        user_ttc = _to_float(d["total_ttc"])
    elif "total_facture" in d and str(d["total_facture"]).strip():
        user_ttc = _to_float(d["total_facture"])
    elif "total" in d and str(d["total"]).strip():
        user_ttc = _to_float(d["total"])

    if user_ttc is not None and user_ttc > 0.0:
        final_ttc = user_ttc
    elif sum_items > 0.0:
        final_ttc = sum_items
    else:
        final_ttc = _to_float(copy.TOTAL_TTC, 790.0)

    calc_ht = round(final_ttc / 1.2, 2)
    calc_tva = round(final_ttc - calc_ht, 2)

    user_ht = _to_float(d.get("total_ht")) if d.get("total_ht") is not None and str(d.get("total_ht")).strip() else None
    user_tva = _to_float(d.get("tva_amount")) if d.get("tva_amount") is not None and str(d.get("tva_amount")).strip() else None

    if user_ht is not None and user_tva is not None and abs((user_ht + user_tva) - final_ttc) < 0.02:
        final_ht = user_ht
        final_tva = user_tva
    else:
        final_ht = calc_ht
        final_tva = calc_tva

    pay_method = str(d.get("payment_method", copy.PAYMENT_METHOD)).strip()
    is_cash = pay_method.lower() in ("cash", "espèces", "especes")
    if is_cash:
        user_pay = _to_float(d.get("payment_amount")) if d.get("payment_amount") is not None and str(d.get("payment_amount")).strip() else None
        if user_pay is not None and user_pay >= final_ttc:
            pay_amt_float = user_pay
        else:
            pay_amt_float = final_ttc
        pay_amt_str = _format_money(pay_amt_float)

        user_rendu = _to_float(d.get("rendu_amount")) if d.get("rendu_amount") is not None and str(d.get("rendu_amount")).strip() else None
        calc_rendu = round(pay_amt_float - final_ttc, 2)
        if user_rendu is not None and abs(user_rendu - calc_rendu) < 0.02:
            rendu_str = _format_money(user_rendu)
        elif calc_rendu > 0.0:
            rendu_str = _format_money(calc_rendu)
        else:
            rendu_str = "0,00"
    else:
        pay_amt_str = _format_money(final_ttc)
        rendu_str = ""

    mid = Middle(
        page_info=str(d.get("page_info", copy.PAGE_INFO)),
        vendeur=str(d.get("vendeur", copy.VENDEUR)),
        items=items_list,
        count_label=count_val,
        total_facture=_format_money(final_ttc),
        payment_method=pay_method,
        payment_amount=pay_amt_str,
        rendu_amount=rendu_str,
        total_ht=_format_money(final_ht),
        tva_product=str(d.get("tva_product", copy.TVA_PRODUCT)),
        tva_rate=str(d.get("tva_rate", copy.TVA_RATE)),
        tva_amount=_format_money(final_tva),
        total_ttc=_format_money(final_ttc),
        code=str(d.get("code", copy.CODE)),
    )
    ftr = Footer(
        line_0=str(d.get("line_0", copy.LEGAL_LINE_0)),
        line_1=str(d.get("line_1", copy.LEGAL_LINE_1)),
        line_2=str(d.get("line_2", copy.LEGAL_LINE_2)),
        line_3=str(d.get("line_3", copy.LEGAL_LINE_3)),
        line_4=str(d.get("line_4", copy.LEGAL_LINE_4)),
    )
    return FactureDior(visible=vis, header=hdr, middle=mid, footer=ftr)

# ----------------------------------------------------------------------

Doc = FactureDior
