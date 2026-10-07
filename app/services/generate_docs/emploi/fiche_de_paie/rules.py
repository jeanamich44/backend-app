import re
import unicodedata

from .services.calculs import calculate_payroll

# ----------------------------------------------------------------------

LIMITS = {
    "raison_sociale": 45,
    "adresse": 45,
    "code_postal": 10,
    "ville": 35,
    "etablissement": 35,
    "siret": 14,
    "code_naf": 5,
    "convention_collective_court": 60,
    "date_debut": 10,
    "date_fin": 10,
    "date_paiement": 15,
    "mode_paiement": 20,
    "nom_complet": 40,
    "salarie_adresse": 45,
    "salarie_cp": 10,
    "salarie_ville": 35,
    "matricule": 15,
    "nir": 15,
    "emploi": 35,
    "qualification": 25,
    "echelon": 10,
    "coefficient": 10,
    "date_anciennete": 25,
}

# ----------------------------------------------------------------------

NUMERIC_RULES = {
    "net_a_payer_cible": {"min": 500.0, "max": 50000.0, "default": 2460.00},
    "heures_mensuelles": {"min": 10.0, "max": 250.0, "default": 151.67},
    "prime_habillage": {"min": 0.0, "max": 5000.0, "default": 210.42},
    "frais_professionnels": {"min": 0.0, "max": 2000.0, "default": 94.00},
    "mutuelle_salarie": {"min": 0.0, "max": 500.0, "default": 33.59},
    "mutuelle_patronale": {"min": 0.0, "max": 1000.0, "default": 64.45},
    "taux_pas": {"min": 0.0, "max": 100.0, "default": 5.00},
    "evolution_remuneration": {"min": 0.0, "max": 500.0, "default": 50.82},
    "allegement_cotisations": {"min": 0.0, "max": 2000.0, "default": 63.15},
    "plafond_mensuel_ss": {"min": 1000.0, "max": 10000.0, "default": 3864.00},
    "cp_n1_du": {"min": 0.0, "max": 100.0, "default": 30.00},
    "cp_n1_pris": {"min": 0.0, "max": 100.0, "default": 5.00},
    "cp_n1_reste": {"min": 0.0, "max": 100.0, "default": 25.00},
    "cp_n_du": {"min": 0.0, "max": 100.0, "default": 10.00},
    "cp_n_pris": {"min": 0.0, "max": 100.0, "default": 0.00},
    "cp_n_reste": {"min": 0.0, "max": 100.0, "default": 10.00},
    "repos_compensateur_du": {"min": 0.0, "max": 200.0, "default": 0.00},
    "repos_compensateur_pris": {"min": 0.0, "max": 200.0, "default": 0.00},
    "repos_compensateur_reste": {"min": 0.0, "max": 200.0, "default": 0.00},
}

# ----------------------------------------------------------------------


def clean_text(val, max_len: int | None = None, uppercase: bool = False) -> str:
    if val is None:
        return ""
    s = unicodedata.normalize("NFC", str(val))
    s = s.replace("\u00a0", " ").replace("\u202f", " ").strip()
    if uppercase:
        s = s.upper()
    if max_len is not None and len(s) > max_len:
        s = s[:max_len]
    return s


def clean_digits(val, max_len: int | None = None) -> str:
    if val is None:
        return ""
    s = re.sub(r"[^\d]", "", str(val))
    if max_len is not None and len(s) > max_len:
        s = s[:max_len]
    return s


def clean_nir(val) -> str:
    if val is None:
        return ""
    digits = re.sub(r"[^\d]", "", str(val))
    return digits[:LIMITS["nir"]]


def clean_siret(val) -> str:
    if val is None:
        return ""
    digits = re.sub(r"[^\d]", "", str(val))
    return digits[:LIMITS["siret"]]


def clean_code_naf(val) -> str:
    if val is None:
        return ""
    s = re.sub(r"[^A-Za-z0-9]", "", str(val)).upper()
    return s[:LIMITS["code_naf"]]


def clean_mode_paiement(val) -> str:
    if val is None:
        return ""
    s = clean_text(val, max_len=LIMITS["mode_paiement"])
    if s.lower().startswith("par "):
        s = s[4:].strip()
    return s


def clean_float(val, default: float = 0.0, min_val: float | None = None, max_val: float | None = None) -> float:
    if val is None or val == "":
        num = default
    else:
        try:
            s = str(val).replace("€", "").replace("%", "").replace(" ", "").replace(",", ".").strip()
            num = float(s)
        except (ValueError, TypeError):
            num = default
    if min_val is not None and num < min_val:
        num = min_val
    if max_val is not None and num > max_val:
        num = max_val
    return round(num, 2)

# ----------------------------------------------------------------------


def public_limits() -> dict:
    return dict(LIMITS)


def public_rules() -> dict:
    return {
        "text_fields": dict(LIMITS),
        "numeric_fields": dict(NUMERIC_RULES),
    }

# ----------------------------------------------------------------------


def apply_payload(payload: dict | None = None) -> dict:
    p = dict(payload or {})

    text_upper_fields = ("ville", "salarie_ville", "nom_complet", "emploi", "qualification", "convention_collective_court")
    for f in text_upper_fields:
        if f in p:
            p[f] = clean_text(p[f], max_len=LIMITS.get(f), uppercase=True)

    text_fields = ("raison_sociale", "adresse", "etablissement", "salarie_adresse", "matricule", "echelon", "coefficient", "date_anciennete", "date_debut", "date_fin", "date_paiement")
    for f in text_fields:
        if f in p:
            p[f] = clean_text(p[f], max_len=LIMITS.get(f))

    if "code_postal" in p:
        p["code_postal"] = clean_digits(p["code_postal"], max_len=LIMITS["code_postal"])
    if "salarie_cp" in p:
        p["salarie_cp"] = clean_digits(p["salarie_cp"], max_len=LIMITS["salarie_cp"])
    if "siret" in p:
        p["siret"] = clean_siret(p["siret"])
    if "code_naf" in p:
        p["code_naf"] = clean_code_naf(p["code_naf"])
    if "nir" in p:
        p["nir"] = clean_nir(p["nir"])
    if "mode_paiement" in p:
        p["mode_paiement"] = clean_mode_paiement(p["mode_paiement"])

    for k, spec in NUMERIC_RULES.items():
        if k in p:
            p[k] = clean_float(p[k], default=spec["default"], min_val=spec["min"], max_val=spec["max"])

    if "cp_n1_du" in p and "cp_n1_pris" in p:
        du = p["cp_n1_du"]
        pris = p["cp_n1_pris"]
        if "cp_n1_reste" not in p or p["cp_n1_reste"] is None:
            p["cp_n1_reste"] = max(0.0, round(du - pris, 2))

    if "cp_n_du" in p and "cp_n_pris" in p:
        du = p["cp_n_du"]
        pris = p["cp_n_pris"]
        if "cp_n_reste" not in p or p["cp_n_reste"] is None:
            p["cp_n_reste"] = max(0.0, round(du - pris, 2))

    if "repos_compensateur_du" in p and "repos_compensateur_pris" in p:
        du = p["repos_compensateur_du"]
        pris = p["repos_compensateur_pris"]
        if "repos_compensateur_reste" not in p or p["repos_compensateur_reste"] is None:
            p["repos_compensateur_reste"] = max(0.0, round(du - pris, 2))

    return p

# ----------------------------------------------------------------------


def apply_doc(doc):
    if not doc:
        return doc

    emp = getattr(doc, "employeur", None)
    if emp:
        emp.raison_sociale = clean_text(emp.raison_sociale, max_len=LIMITS["raison_sociale"])
        emp.adresse = clean_text(emp.adresse, max_len=LIMITS["adresse"])
        emp.code_postal = clean_digits(emp.code_postal, max_len=LIMITS["code_postal"])
        emp.ville = clean_text(emp.ville, max_len=LIMITS["ville"], uppercase=True)
        emp.etablissement = clean_text(emp.etablissement, max_len=LIMITS["etablissement"])
        emp.siret = clean_siret(emp.siret)
        emp.code_naf = clean_code_naf(emp.code_naf)
        emp.convention_collective_court = clean_text(emp.convention_collective_court, max_len=LIMITS["convention_collective_court"], uppercase=True)

    sal = getattr(doc, "salarie", None)
    if sal:
        sal.nom_complet = clean_text(sal.nom_complet, max_len=LIMITS["nom_complet"], uppercase=True)
        sal.adresse = clean_text(sal.adresse, max_len=LIMITS["salarie_adresse"])
        sal.code_postal = clean_digits(sal.code_postal, max_len=LIMITS["salarie_cp"])
        sal.ville = clean_text(sal.ville, max_len=LIMITS["salarie_ville"], uppercase=True)
        sal.matricule = clean_text(sal.matricule, max_len=LIMITS["matricule"])
        sal.nir = clean_nir(sal.nir)
        sal.emploi = clean_text(sal.emploi, max_len=LIMITS["emploi"], uppercase=True)
        sal.qualification = clean_text(sal.qualification, max_len=LIMITS["qualification"], uppercase=True)
        sal.echelon = clean_text(sal.echelon, max_len=LIMITS["echelon"])
        sal.coefficient = clean_text(sal.coefficient, max_len=LIMITS["coefficient"])
        sal.date_anciennete = clean_text(sal.date_anciennete, max_len=LIMITS["date_anciennete"])

    per = getattr(doc, "periode", None)
    if per:
        per.date_debut = clean_text(per.date_debut, max_len=LIMITS["date_debut"])
        per.date_fin = clean_text(per.date_fin, max_len=LIMITS["date_fin"])
        per.date_paiement = clean_text(per.date_paiement, max_len=LIMITS["date_paiement"])
        per.mode_paiement = clean_mode_paiement(per.mode_paiement)
        per.plafond_mensuel_ss = clean_float(per.plafond_mensuel_ss, default=3864.00, min_val=1000.0, max_val=10000.0)

    cng = getattr(doc, "conges", None)
    if cng:
        for f in ("cp_n1_du", "cp_n1_pris", "cp_n1_reste", "cp_n_du", "cp_n_pris", "cp_n_reste", "repos_compensateur_du", "repos_compensateur_pris", "repos_compensateur_reste"):
            spec = NUMERIC_RULES.get(f, {"default": 0.0, "min": 0.0, "max": 200.0})
            val = getattr(cng, f, 0.0)
            setattr(cng, f, clean_float(val, default=spec["default"], min_val=spec["min"], max_val=spec["max"]))

    if not getattr(doc, "calculs", None) or not isinstance(doc.calculs, dict):
        doc.calculs = calculate_payroll({})

    return doc
