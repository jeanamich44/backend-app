import re

_META_KEYS = {"mode", "custom", "visible"}


def _first(data: dict, *keys, default: str = "") -> str:
    for key in keys:
        value = data.get(key)
        if value is None:
            continue
        text = str(value).strip()
        if text:
            return text
    return default


def _titulaire(data: dict) -> str:
    civilite = _first(data, "civilite")
    nom_prenom = _first(data, "nom_prenom")
    p = _first(data, "prenom")
    n = _first(data, "nom")
    if nom_prenom:
        return f"{civilite} {nom_prenom}".strip() if civilite else nom_prenom
    if p or n:
        nom = f"{n} {p}".strip() if p and n else (n or p)
        return f"{civilite} {nom}".strip() if civilite else nom
    name = _first(data, "titulaire")
    if name:
        return name
    return ""


def _ville(data: dict) -> str:
    combined = _first(data, "cp_ville")
    if combined:
        return combined
    return f"{_first(data, 'cp')} {_first(data, 'ville')}".strip()


def _split_cp_ville(value: str) -> tuple[str, str]:
    text = (value or "").strip()
    if not text:
        return "", ""
    parts = text.split(None, 1)
    if parts[0][:1].isdigit():
        return parts[0], parts[1] if len(parts) > 1 else ""
    return "", text


def _base(data: dict) -> dict:
    payload: dict = {}
    nom = _titulaire(data)
    rue = _first(data, "adresse")
    ville = _ville(data)
    if rue and not ville:
        m = re.search(r"\b(\d{5})\b", rue)
        if m:
            start = m.start()
            candidate_rue = rue[:start].strip().rstrip(",")
            candidate_ville = rue[start:].strip()
            if candidate_rue and candidate_ville:
                rue = candidate_rue
                ville = candidate_ville
    banque = _first(data, "code_banque", "banque")
    guichet = _first(data, "code_guichet", "guichet")
    compte = _first(data, "num_compte", "compte", "num_compte_mypos")
    cle = _first(data, "cle_rib", "cle")
    iban = _first(data, "iban")
    bic = _first(data, "bic")
    if nom:
        payload["middle_titulaire_nom"] = nom
    if rue:
        payload["middle_titulaire_rue"] = rue
        payload["middle_titulaire_adresse"] = rue
    if ville:
        payload["middle_titulaire_ville"] = ville
    if banque:
        payload["middle_banque"] = banque
        payload["middle_etablissement"] = banque
    if guichet:
        payload["middle_guichet"] = guichet
    if compte:
        payload["middle_compte"] = compte
    if cle:
        payload["middle_cle"] = cle
    if iban:
        payload["middle_iban"] = iban
        payload["middle_iban_text"] = iban
    if bic:
        payload["middle_bic"] = bic
        payload["middle_bic_text"] = bic
    return payload


def _lbp(data: dict) -> dict:
    out = _base(data)
    domiciliation = _first(data, "domiciliation")
    if domiciliation:
        out["middle_domiciliation"] = domiciliation
    return out


def _ca(data: dict) -> dict:
    out = _base(data)
    if _first(data, "caisse_nom"):
        out["middle_caisse"] = _first(data, "caisse_nom")
    if _first(data, "caisse_agence"):
        out["middle_agence_ville"] = _first(data, "caisse_agence")
    if _first(data, "caisse_tel"):
        out["middle_tel"] = _first(data, "caisse_tel")
    if _first(data, "caisse_fax"):
        out["middle_fax"] = _first(data, "caisse_fax")
    if _first(data, "date_edition"):
        out["middle_date"] = _first(data, "date_edition")
    if _first(data, "code_agence"):
        out["middle_code"] = _first(data, "code_agence")
    return out


def _sg(data: dict) -> dict:
    out = _base(data)
    if _first(data, "agence_nom"):
        out["middle_agence_text"] = _first(data, "agence_nom")
    if _first(data, "agence_adresse"):
        out["middle_agence_rue"] = _first(data, "agence_adresse")
    cp = _first(data, "agence_cp")
    ville = _first(data, "agence_ville")
    if cp or ville:
        out["middle_agence_ville"] = f"{cp} {ville}".strip()
    elif _first(data, "agence_cp_ville"):
        out["middle_agence_ville"] = _first(data, "agence_cp_ville")
    return out


def _cm(data: dict) -> dict:
    out = _base(data)
    agence = _first(data, "agence_nom", "caisse_nom")
    if agence:
        out["middle_agence_text"] = agence
    if _first(data, "agence_adresse"):
        out["middle_domiciliation_rue"] = _first(data, "agence_adresse")
    cp = _first(data, "agence_cp")
    ville = _first(data, "agence_ville")
    if cp or ville:
        out["middle_domiciliation_ville"] = f"{cp} {ville}".strip()
    elif _first(data, "agence_cp_ville"):
        out["middle_domiciliation_ville"] = _first(data, "agence_cp_ville")
    if _first(data, "agence_tel"):
        out["middle_phone"] = _first(data, "agence_tel")
    if _first(data, "devise"):
        out["middle_devise"] = _first(data, "devise")
    return out


def _cic(data: dict) -> dict:
    return _cm(data)


def _qonto(data: dict) -> dict:
    out = _base(data)
    if _first(data, "nom_compte"):
        out["middle_account_name"] = _first(data, "nom_compte")
    if out.get("middle_titulaire_nom"):
        out["middle_titulaire_nom"] = out["middle_titulaire_nom"].upper()
    if out.get("middle_titulaire_rue"):
        out["middle_titulaire_rue"] = out["middle_titulaire_rue"].upper()
    if out.get("middle_titulaire_ville"):
        out["middle_titulaire_ville"] = out["middle_titulaire_ville"].upper()
    return out


def _helios(data: dict) -> dict:
    data = dict(data)
    civ = _first(data, "civilite")
    if civ and civ.upper() in {"M.", "M", "MR", "MR.", "MONSIEUR"}:
        data["civilite"] = "Mr"
    out = _base(data)
    rue = _first(data, "adresse")
    ville = _ville(data)
    if rue and ville:
        out["middle_titulaire_adresse"] = f"{rue}, {ville}"
    elif ville:
        out["middle_titulaire_adresse"] = ville
    return out


def _lcl(data: dict) -> dict:
    out = _base(data)
    if _first(data, "domiciliation"):
        out["middle_domiciliation_text"] = _first(data, "domiciliation")
    return out


def _bp(data: dict) -> dict:
    return _lcl(data)


def _bnp(data: dict) -> dict:
    out = _base(data)
    dom = _first(data, "agence_domiciliation", "agence_nom", "domiciliation")
    if dom:
        out["middle_domiciliation_text"] = dom
    return out


def _bfb(data: dict) -> dict:
    out = _base(data)
    if _first(data, "domiciliation"):
        out["middle_domiciliation_text"] = _first(data, "domiciliation")
    if out.get("middle_titulaire_nom"):
        out["middle_titulaire_nom"] = out["middle_titulaire_nom"].upper()
    rue = _first(data, "header_rue") or out.get("middle_titulaire_rue") or _first(data, "adresse")
    if rue:
        out["header_rue"] = rue.upper()
    ville = _first(data, "header_ville") or out.get("middle_titulaire_ville") or _ville(data)
    if ville:
        out["header_ville"] = ville.upper()
    pays = _first(data, "header_pays", "pays")
    if pays:
        out["header_pays"] = pays
    elif not out.get("header_pays"):
        out["header_pays"] = "France"
    return out


def _ce(data: dict) -> dict:
    out = _base(data)
    out["middle_titulaire_prefix"] = ""
    rue = _first(data, "domiciliation_rue", "domiciliation_adresse")
    cp = _first(data, "domiciliation_cp")
    ville = _first(data, "domiciliation_ville")
    if rue:
        out["middle_domiciliation_rue"] = rue
    if cp or ville:
        out["middle_domiciliation_ville"] = f"{cp} {ville}".strip()

    if not out.get("middle_domiciliation_rue") or not out.get("middle_domiciliation_ville"):
        raw = data.get("domiciliation") or ""
        lines = [line.strip() for line in str(raw).splitlines() if line.strip()]
        if len(lines) >= 2:
            if not out.get("middle_domiciliation_rue"):
                out["middle_domiciliation_rue"] = lines[0]
            if not out.get("middle_domiciliation_ville"):
                out["middle_domiciliation_ville"] = " ".join(lines[1:])
        elif len(lines) == 1:
            m = re.search(r"\b(\d{5})\b", lines[0])
            if m:
                start = m.start()
                parsed_rue = lines[0][:start].strip().rstrip(",")
                parsed_ville = lines[0][start:].strip()
                if not out.get("middle_domiciliation_rue"):
                    out["middle_domiciliation_rue"] = parsed_rue or lines[0]
                if not out.get("middle_domiciliation_ville"):
                    out["middle_domiciliation_ville"] = parsed_ville
            elif not out.get("middle_domiciliation_rue"):
                out["middle_domiciliation_rue"] = lines[0]

    if out.get("middle_domiciliation_rue") and not out.get("middle_domiciliation_ville"):
        m = re.search(r"\b(\d{5})\b", out["middle_domiciliation_rue"])
        if m:
            start = m.start()
            candidate_rue = out["middle_domiciliation_rue"][:start].strip().rstrip(",")
            candidate_ville = out["middle_domiciliation_rue"][start:].strip()
            if candidate_rue and candidate_ville:
                out["middle_domiciliation_rue"] = candidate_rue
                out["middle_domiciliation_ville"] = candidate_ville

    return out


def _boursobank(data: dict) -> dict:
    out = _base(data)
    if _first(data, "header_title_text"):
        out["header_title_text"] = _first(data, "header_title_text")
    if _first(data, "header_subtitle_text"):
        out["header_subtitle_text"] = _first(data, "header_subtitle_text")
    for key in (
        "header", "header_logo", "header_title", "header_subtitle",
        "middle", "middle_titulaire", "middle_bic", "middle_iban",
        "middle_domiciliation", "middle_table", "middle_separator",
        "footer",
    ):
        if key in data:
            out[key] = data[key]
    return out


def _revolut(data: dict) -> dict:
    out = _base(data)
    nom = _first(data, "nom_prenom")
    if not nom:
        p = _first(data, "prenom")
        n = _first(data, "nom")
        if p or n:
            nom = f"{n} {p}".strip() if p and n else (n or p)
    if nom:
        out["middle_titulaire_nom"] = nom.upper()
    elif out.get("middle_titulaire_nom"):
        out["middle_titulaire_nom"] = out["middle_titulaire_nom"].upper()
    if out.get("middle_titulaire_rue"):
        out["middle_titulaire_rue"] = re.sub(r"[A-Za-zÀ-ÿ]+", lambda m: m.group(0).capitalize(), out["middle_titulaire_rue"])
        out["middle_titulaire_adresse"] = out["middle_titulaire_rue"]
    cp, ville = _split_cp_ville(_ville(data))
    if cp:
        out["middle_titulaire_cp"] = cp
    if ville:
        out["middle_titulaire_ville"] = re.sub(r"[A-Za-zÀ-ÿ]+", lambda m: m.group(0).capitalize(), ville)
    region = _first(data, "region", "departement", "dept", "middle_titulaire_dept")
    if region:
        out["middle_titulaire_dept"] = re.sub(r"[A-Za-zÀ-ÿ]+", lambda m: m.group(0).capitalize(), region)
    return out


def _noelse(data: dict) -> dict:
    out = _base(data)
    nom = _first(data, "nom_prenom")
    if not nom:
        p = _first(data, "prenom")
        n = _first(data, "nom")
        if p or n:
            nom = f"{n} {p}".strip() if p and n else (n or p)
    if nom:
        out["middle_titulaire_nom"] = nom
    if _first(data, "pays"):
        out["middle_titulaire_pays"] = _first(data, "pays")
    return out


def _sumup(data: dict) -> dict:
    data = dict(data)
    data.pop("civilite", None)
    out = _base(data)
    if out.get("middle_titulaire_nom"):
        out["middle_titulaire_nom"] = re.sub(
            r"^(?:M\.|MR\.|MR|MME\.|MRS\.|MS\.|MADAME|MONSIEUR)\s+",
            "",
            out["middle_titulaire_nom"],
            flags=re.IGNORECASE,
        ).strip()
    date_doc = _first(data, "date_document")
    heure_doc = _first(data, "heure_document", "heure")
    if heure_doc:
        clean_time = re.sub(r"\s*(?:gmt|utc)\b", "", heure_doc, flags=re.IGNORECASE).strip()
        time_formatted = f"{clean_time} GMT" if clean_time else ""
        date_part = date_doc.split(",")[0].strip() if date_doc else ""
        if date_part and time_formatted:
            out["header_date_text"] = f"{date_part}, {time_formatted}"
        elif date_part:
            out["header_date_text"] = date_part
        elif time_formatted:
            out["header_date_text"] = time_formatted
    elif date_doc:
        out["header_date_text"] = date_doc
    elif _first(data, "header_date_text"):
        out["header_date_text"] = _first(data, "header_date_text")
    if _first(data, "pays"):
        out["middle_titulaire_pays"] = _first(data, "pays")
    elif not out.get("middle_titulaire_pays"):
        out["middle_titulaire_pays"] = "France"
    if _first(data, "date_ouverture"):
        out["middle_date_ouverture"] = _first(data, "date_ouverture")
    if _first(data, "institution"):
        out["middle_institution"] = _first(data, "institution")
    elif not out.get("middle_institution"):
        out["middle_institution"] = "SumUp Limited"
    if _first(data, "header_title_text"):
        out["header_title_text"] = _first(data, "header_title_text")
    if _first(data, "middle_notice_text"):
        out["middle_notice_text"] = _first(data, "middle_notice_text")
    if _first(data, "footer_legal_text"):
        out["footer_legal_text"] = _first(data, "footer_legal_text")
    if _first(data, "footer_legal_right_text"):
        out["footer_legal_right_text"] = _first(data, "footer_legal_right_text")
    for key in (
        "header", "header_logo", "header_title", "header_date",
        "middle", "middle_holder", "middle_account", "middle_notice",
        "footer", "footer_legal", "footer_legal_right",
    ):
        if key in data:
            out[key] = data[key]
    return out


def _mypos(data: dict) -> dict:
    out = _base(data)
    if _first(data, "date_edition"):
        out["header_date_text"] = _first(data, "date_edition")
    elif _first(data, "header_date_text"):
        out["header_date_text"] = _first(data, "header_date_text")
    if _first(data, "nom_societe"):
        out["middle_nom_societe"] = _first(data, "nom_societe")
    elif _first(data, "middle_nom_societe"):
        out["middle_nom_societe"] = _first(data, "middle_nom_societe")
    if _first(data, "num_enregistrement"):
        out["middle_num_enregistrement"] = _first(data, "num_enregistrement")
    elif _first(data, "middle_num_enregistrement"):
        out["middle_num_enregistrement"] = _first(data, "middle_num_enregistrement")
    if _first(data, "adresse"):
        out["middle_adresse"] = _first(data, "adresse")
    elif _first(data, "middle_adresse"):
        out["middle_adresse"] = _first(data, "middle_adresse")
    if _ville(data):
        out["middle_cp_ville"] = _ville(data)
    elif _first(data, "middle_cp_ville"):
        out["middle_cp_ville"] = _first(data, "middle_cp_ville")
    if _first(data, "pays"):
        out["middle_pays"] = _first(data, "pays")
    elif _first(data, "middle_pays"):
        out["middle_pays"] = _first(data, "middle_pays")
    if _first(data, "devise"):
        out["middle_devise"] = _first(data, "devise")
    elif _first(data, "middle_devise"):
        out["middle_devise"] = _first(data, "middle_devise")
    if _first(data, "header_title_text"):
        out["header_title_text"] = _first(data, "header_title_text")
    if _first(data, "footer_page_text"):
        out["footer_page_text"] = _first(data, "footer_page_text")
    for key in (
        "header", "header_logo", "header_title", "header_date", "header_address",
        "middle", "middle_letter", "middle_table",
        "footer", "footer_legal", "footer_page",
    ):
        if key in data:
            out[key] = data[key]
    return out


_BANK_MAP = {
    "lbp": _lbp,
    "ca": _ca,
    "sg": _sg,
    "cm": _cm,
    "cic": _cic,
    "qonto": _qonto,
    "helios": _helios,
    "lcl": _lcl,
    "bp": _bp,
    "bnp": _bnp,
    "bfb": _bfb,
    "ce": _ce,
    "boursobank": _boursobank,
    "revolut": _revolut,
    "noelse": _noelse,
    "sumup": _sumup,
    "mypos": _mypos,
}


def _is_lab_key(key: str) -> bool:
    if key in _META_KEYS:
        return False
    return key.startswith(("header", "middle_", "footer")) or key in {"header", "middle", "footer"}


def _apply_normal_defaults(bank: str, mapped: dict) -> dict:
    if bank == "lbp":
        mapped["middle_titulaire_opt1"] = ""
        mapped["middle_titulaire_opt2"] = ""
    elif bank == "ca":
        mapped.setdefault("middle_titulaire_opt", "")
    elif bank == "bp":
        mapped.setdefault("middle_titulaire_opt", "")
    elif bank == "ce":
        mapped.setdefault("middle_titulaire_prefix", "")
        mapped.setdefault("middle_titulaire_opt", "")
    return mapped


def _overlay_custom(mapped: dict, data: dict, bank: str) -> dict:
    from app.services.generate_docs.rib.editor import IDENTITY_KEYS, _COMMON_IDENTITY

    identity = IDENTITY_KEYS.get(bank, _COMMON_IDENTITY)
    for key, value in data.items():
        if not _is_lab_key(key) or key in identity:
            continue
        if isinstance(value, (dict, list)):
            continue
        mapped[key] = value
    custom = data.get("custom")
    if isinstance(custom, dict):
        for key, value in custom.items():
            if key in _META_KEYS or key in identity:
                continue
            if isinstance(value, bool) or value is not None:
                mapped[key] = value
    visible = data.get("visible")
    if isinstance(visible, dict):
        for key, value in visible.items():
            mapped[key] = value
    return mapped


def to_lab_payload(bank: str, data: dict | None) -> dict:
    data = data or {}
    mode = str(data.get("mode") or "normal").strip().lower()
    mapper = _BANK_MAP.get(bank, _base)
    mapped = mapper(data)
    if mode == "custom":
        return _overlay_custom(mapped, data, bank)
    return _apply_normal_defaults(bank, mapped)
