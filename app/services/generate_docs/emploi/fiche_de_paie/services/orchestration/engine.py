from ...data import Doc, from_payload
from ...rules import apply_doc, apply_payload
from ..calculs import calculate_payroll
from ..informations import DEFAULTS_TABLE, extract_date_iso
from .timeline import get_month_sequence, get_payment_date_str, get_period_strings, get_retroactive_sequence

# ----------------------------------------------------------------------


def generate_payroll_sequence(
    base_params: dict | None = None,
    count: int = 3,
    start_month: int | None = None,
    start_year: int | None = None,
) -> list[Doc]:
    p = apply_payload(base_params or {})

    dur = count
    if "duree_mois" in p:
        try:
            dur = int(p["duree_mois"])
        except (ValueError, TypeError):
            pass
    elif "duree" in p:
        try:
            dur = int(p["duree"])
        except (ValueError, TypeError):
            pass
    dur = max(1, min(24, dur))

    s_m = start_month or p.get("start_month") or p.get("mois_debut")
    s_y = start_year or p.get("start_year") or p.get("annee_debut")

    if s_m is None or s_y is None:
        if any(k in p for k in ("date_debut", "date_fin", "date_paiement", "annee")):
            d_iso = extract_date_iso(p)
            try:
                parts = d_iso.split("-")
                s_y = int(parts[0])
                s_m = int(parts[1])
            except (ValueError, TypeError, IndexError):
                pass

    if s_m is not None and s_y is not None:
        try:
            months_seq = get_month_sequence(int(s_m), int(s_y), dur)
        except (ValueError, TypeError):
            months_seq = get_retroactive_sequence(dur)
    elif "end_month" in p and "end_year" in p:
        try:
            months_seq = get_retroactive_sequence(dur, end_month=int(p["end_month"]), end_year=int(p["end_year"]))
        except (ValueError, TypeError):
            months_seq = get_retroactive_sequence(dur)
    else:
        months_seq = get_retroactive_sequence(dur)

    prelim_calc = calculate_payroll(p)
    brut = prelim_calc["salaire_brut"]
    tot_sal = prelim_calc["total_retenues_salariales"]
    net_imp = prelim_calc["net_imposable"]
    heures = prelim_calc["heures"]
    tot_pat = prelim_calc["total_retenues_patronales"]

    cng_defaults = DEFAULTS_TABLE["conges"]
    cp_n1_du = float(p.get("cp_n1_du", cng_defaults["cp_n1_du"]))
    cp_n1_pris = float(p.get("cp_n1_pris", cng_defaults["cp_n1_pris"]))
    cp_n1_reste = float(p.get("cp_n1_reste", cng_defaults["cp_n1_reste"]))
    cp_n_du = float(p.get("cp_n_du", cng_defaults["cp_n_du"]))
    cp_n_pris = float(p.get("cp_n_pris", cng_defaults["cp_n_pris"]))
    cp_n_reste = float(p.get("cp_n_reste", cng_defaults["cp_n_reste"]))
    rc_du = float(p.get("repos_compensateur_du", cng_defaults["repos_compensateur_du"]))
    rc_pris = float(p.get("repos_compensateur_pris", cng_defaults["repos_compensateur_pris"]))
    rc_reste = float(p.get("repos_compensateur_reste", cng_defaults["repos_compensateur_reste"]))

    docs_list = []
    prev_m = None

    for idx, (m, y) in enumerate(months_seq):
        d_deb, d_fin = get_period_strings(m, y)
        d_pay = get_payment_date_str(m, y)

        if idx > 0:
            if prev_m == 5 and m == 6:
                cp_n1_du = cp_n_du
                cp_n1_pris = cp_n_pris
                cp_n1_reste = cp_n_reste
                cp_n_du = 2.50
                cp_n_pris = 0.00
                cp_n_reste = 2.50
            else:
                cp_n_du = round(cp_n_du + 2.50, 2)
                cp_n_reste = round(cp_n_reste + 2.50, 2)

        prev_m = m

        cumuls_m = {
            "brut": round(brut * m, 2),
            "cotisations": round(tot_sal * m, 2),
            "net_imposable": round(net_imp * m, 2),
            "heures": round(heures * m, 2),
            "part_patronale": round(tot_pat * m, 2),
        }

        p_m = dict(p)
        p_m["date_debut"] = d_deb
        p_m["date_fin"] = d_fin
        p_m["date_paiement"] = d_pay
        p_m["mois"] = m
        p_m["annee"] = y
        p_m["cumuls"] = cumuls_m

        p_m["cp_n1_du"] = cp_n1_du
        p_m["cp_n1_pris"] = cp_n1_pris
        p_m["cp_n1_reste"] = cp_n1_reste
        p_m["cp_n_du"] = cp_n_du
        p_m["cp_n_pris"] = cp_n_pris
        p_m["cp_n_reste"] = cp_n_reste
        p_m["repos_compensateur_du"] = rc_du
        p_m["repos_compensateur_pris"] = rc_pris
        p_m["repos_compensateur_reste"] = rc_reste

        doc_m = from_payload(p_m)
        docs_list.append(apply_doc(doc_m))

    return docs_list
