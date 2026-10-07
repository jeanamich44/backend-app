from ..informations.defaults import (
    DEFAULTS_TABLE,
    get_pmss_for_date,
    get_previous_month_dates,
    get_taux_agirc_t1_patronale_for_date,
    get_taux_agirc_t1_salariale_for_date,
    get_taux_vieillesse_deplafonnée_patronale_for_date,
)

# ----------------------------------------------------------------------


def solve_brut_for_net(
    net_cible: float | None = None,
    taux_pas: float | None = None,
    frais_pro: float | None = None,
    mutuelle_sal: float | None = None,
    mutuelle_pat: float | None = None,
    pmss: float | None = None,
    taux_agirc_sal: float | None = None,
    date_context: dict | str | None = None,
) -> float:
    rem = DEFAULTS_TABLE["remuneration"]
    rates = rem.get("taux_cotisations", {})

    target = rem["net_a_payer_cible"] if net_cible is None else float(net_cible)
    pas_pct = rem["taux_pas"] if taux_pas is None else float(taux_pas)
    frais = rem["frais_professionnels"] if frais_pro is None else float(frais_pro)
    m_sal = rem["mutuelle_salarie"] if mutuelle_sal is None else float(mutuelle_sal)
    m_pat = rem["mutuelle_patronale"] if mutuelle_pat is None else float(mutuelle_pat)
    p_plaf = get_pmss_for_date(date_context) if pmss is None else float(pmss)

    t_csg_assiette = rates.get("assiette_csg_taux", 0.9825)
    t_ret_plaf = rates.get("retraite_plafonnee_salariale", 0.0690)
    t_ret_deplaf = rates.get("retraite_deplafonnee_salariale", 0.0040)
    t_agirc = get_taux_agirc_t1_salariale_for_date(date_context) if taux_agirc_sal is None else float(taux_agirc_sal)
    t_csg_ded = rates.get("csg_deductible_salariale", 0.0680)
    t_csg_nonded = rates.get("csg_crds_nondeductible_salariale", 0.0290)

    def eval_net(b: float) -> float:
        base_ss = min(b, p_plaf)
        base_csg = round(b * t_csg_assiette + m_pat, 2)
        s_ret_p = round(base_ss * t_ret_plaf, 2)
        s_ret_d = round(b * t_ret_deplaf, 2)
        s_ag = round(base_ss * t_agirc, 2)
        s_cd = round(base_csg * t_csg_ded, 2)
        s_cnd = round(base_csg * t_csg_nonded, 2)
        tot_sal = round(m_sal + s_ret_p + s_ret_d + s_ag + s_cd + s_cnd, 2)
        net_av_impot = round(b - tot_sal, 2)
        tot_ded = round(m_sal + s_ret_p + s_ret_d + s_ag + s_cd, 2)
        net_impo = round(b - tot_ded + m_pat, 2)
        pas_amt = round(net_impo * (pas_pct / 100.0), 2)
        return round(net_av_impot - pas_amt + frais, 2)

    low = max(0.0, target * 0.7)
    high = max(50000.0, target * 3.0)
    mid = (low + high) / 2.0

    for _ in range(30):
        mid = (low + high) / 2.0
        val = eval_net(mid)
        if val < target:
            low = mid
        else:
            high = mid

    center_cents = int(round(mid * 100.0))
    search_start = max(0, center_cents - 300)
    search_end = center_cents + 300

    best_b = mid
    min_diff = float("inf")

    for c in range(search_start, search_end + 1):
        b = c / 100.0
        diff = abs(eval_net(b) - target)
        if diff < 0.001:
            return b
        if diff < min_diff:
            min_diff = diff
            best_b = b

    return round(best_b, 2)


def calculate_payroll(params: dict | None = None) -> dict:
    p = params or {}
    rem = DEFAULTS_TABLE["remuneration"]
    rates = rem.get("taux_cotisations", {})

    net_cible = float(p.get("net_a_payer_cible", rem["net_a_payer_cible"]))
    heures = float(p.get("heures_mensuelles", rem["heures_mensuelles"]))
    taux_pas = float(p.get("taux_pas", rem["taux_pas"]))
    frais_pro = float(p.get("frais_professionnels", rem["frais_professionnels"]))
    mutuelle_sal = float(p.get("mutuelle_salarie", rem["mutuelle_salarie"]))
    mutuelle_pat = float(p.get("mutuelle_patronale", rem["mutuelle_patronale"]))
    allegement = float(p.get("allegement_cotisations", rem["allegement_cotisations"]))
    prime_habillage = float(p.get("prime_habillage", rem["prime_habillage"]))
    if "plafond_mensuel_ss" in p and p["plafond_mensuel_ss"] not in (None, ""):
        try:
            raw_pmss = float(str(p["plafond_mensuel_ss"]).replace(",", "."))
            exp_pmss = get_pmss_for_date(p)
            if raw_pmss not in (3428.00, 3666.00, 3864.00, 3925.00, 4005.00) or raw_pmss == exp_pmss:
                pmss = raw_pmss
            else:
                pmss = exp_pmss
        except (ValueError, TypeError):
            pmss = get_pmss_for_date(p)
    else:
        pmss = get_pmss_for_date(p)

    t_maladie_ss = float(p.get("taux_maladie_ss", rates.get("maladie_ss_patronale", 0.1300)))
    t_at_mp = float(p.get("taux_at_mp", rates.get("accident_travail_patronale", 0.0100)))
    t_ret_plaf_sal = float(p.get("taux_ret_plaf_sal", rates.get("retraite_plafonnee_salariale", 0.0690)))
    t_ret_plaf_pat = float(p.get("taux_ret_plaf_pat", rates.get("retraite_plafonnee_patronale", 0.0855)))
    t_ret_deplaf_sal = float(p.get("taux_ret_deplaf_sal", rates.get("retraite_deplafonnee_salariale", 0.0040)))
    if "taux_ret_deplaf_pat" in p and p["taux_ret_deplaf_pat"] not in (None, ""):
        try:
            raw_t = float(str(p["taux_ret_deplaf_pat"]).replace(",", "."))
            exp_t = get_taux_vieillesse_deplafonnée_patronale_for_date(p)
            if raw_t not in (0.0190, 0.0202, 0.0211) or raw_t == exp_t:
                t_ret_deplaf_pat = raw_t
            else:
                t_ret_deplaf_pat = exp_t
        except (ValueError, TypeError):
            t_ret_deplaf_pat = get_taux_vieillesse_deplafonnée_patronale_for_date(p)
    else:
        t_ret_deplaf_pat = get_taux_vieillesse_deplafonnée_patronale_for_date(p)

    if "taux_agirc_sal" in p and p["taux_agirc_sal"] not in (None, ""):
        try:
            raw_t = float(str(p["taux_agirc_sal"]).replace(",", "."))
            exp_t = get_taux_agirc_t1_salariale_for_date(p)
            if raw_t not in (0.0390, 0.0401) or raw_t == exp_t:
                t_agirc_sal = raw_t
            else:
                t_agirc_sal = exp_t
        except (ValueError, TypeError):
            t_agirc_sal = get_taux_agirc_t1_salariale_for_date(p)
    else:
        t_agirc_sal = get_taux_agirc_t1_salariale_for_date(p)

    if "taux_agirc_pat" in p and p["taux_agirc_pat"] not in (None, ""):
        try:
            raw_t = float(str(p["taux_agirc_pat"]).replace(",", "."))
            exp_t = get_taux_agirc_t1_patronale_for_date(p)
            if raw_t not in (0.0585, 0.0601) or raw_t == exp_t:
                t_agirc_pat = raw_t
            else:
                t_agirc_pat = exp_t
        except (ValueError, TypeError):
            t_agirc_pat = get_taux_agirc_t1_patronale_for_date(p)
    else:
        t_agirc_pat = get_taux_agirc_t1_patronale_for_date(p)
    t_famille = float(p.get("taux_famille", rates.get("famille_patronale", 0.0345)))
    t_chomage = float(p.get("taux_chomage", rates.get("chomage_patronale", 0.0420)))
    t_autres = float(p.get("taux_autres", rates.get("autres_contributions_patronale", 0.0550)))
    t_csg_ded = float(p.get("taux_csg_ded", rates.get("csg_deductible_salariale", 0.0680)))
    t_csg_nonded = float(p.get("taux_csg_nonded", rates.get("csg_crds_nondeductible_salariale", 0.0290)))
    t_csg_assiette = float(p.get("assiette_csg_taux", rates.get("assiette_csg_taux", 0.9825)))

    brut = p.get("salaire_brut")
    if brut is None:
        brut = solve_brut_for_net(
            net_cible,
            taux_pas,
            frais_pro,
            mutuelle_sal,
            mutuelle_pat,
            pmss,
            taux_agirc_sal=t_agirc_sal,
            date_context=p,
        )
    else:
        brut = float(brut)

    salaire_base = round(brut - prime_habillage, 2)
    taux_horaire_base = round(salaire_base / heures, 3)
    taux_horaire_brut = round(brut / heures, 3)

    base_ss = min(brut, pmss)
    base_csg = round(brut * t_csg_assiette + mutuelle_pat, 2)

    s_mutuelle = mutuelle_sal
    p_mutuelle = mutuelle_pat

    p_maladie_ss = round(brut * t_maladie_ss, 2)
    p_at_mp = round(brut * t_at_mp, 2)

    s_ret_plaf = round(base_ss * t_ret_plaf_sal, 2)
    p_ret_plaf = round(base_ss * t_ret_plaf_pat, 2)

    s_ret_deplaf = round(brut * t_ret_deplaf_sal, 2)
    p_ret_deplaf = round(brut * t_ret_deplaf_pat, 2)

    s_agirc_t1 = round(base_ss * t_agirc_sal, 2)
    p_agirc_t1 = round(base_ss * t_agirc_pat, 2)

    p_famille = round(brut * t_famille, 2)
    p_chomage = round(brut * t_chomage, 2)
    p_autres = round(brut * t_autres, 2)

    s_csg_ded = round(base_csg * t_csg_ded, 2)
    s_csg_nonded = round(base_csg * t_csg_nonded, 2)

    total_salarial = round(
        s_mutuelle + s_ret_plaf + s_ret_deplaf + s_agirc_t1 + s_csg_ded + s_csg_nonded, 2
    )
    total_patronal = round(
        p_maladie_ss + p_mutuelle + p_at_mp + p_ret_plaf + p_ret_deplaf + p_agirc_t1 + p_famille + p_chomage + p_autres, 2
    )

    cotis_deductibles = round(s_mutuelle + s_ret_plaf + s_ret_deplaf + s_agirc_t1 + s_csg_ded, 2)
    net_imposable = round(brut - cotis_deductibles + p_mutuelle, 2)
    montant_net_social = round(brut - cotis_deductibles + p_mutuelle, 2)

    net_avant_impot = round(brut - total_salarial, 2)
    pas_montant = round(net_imposable * (taux_pas / 100.0), 2)
    net_a_payer = round(net_avant_impot - pas_montant + frais_pro, 2)

    total_verse = round(brut + total_patronal - allegement, 2)

    if "cumuls" in p and isinstance(p["cumuls"], dict):
        cumuls = {
            "brut": round(float(p["cumuls"].get("brut", brut)), 2),
            "cotisations": round(float(p["cumuls"].get("cotisations", total_salarial)), 2),
            "net_imposable": round(float(p["cumuls"].get("net_imposable", net_imposable)), 2),
            "heures": round(float(p["cumuls"].get("heures", heures)), 2),
            "part_patronale": round(float(p["cumuls"].get("part_patronale", total_patronal)), 2),
        }
    else:
        period_info = get_previous_month_dates()
        mois_idx = int(p.get("mois_idx", p.get("mois", period_info["mois"])))
        cumuls = {
            "brut": round(brut * mois_idx, 2),
            "cotisations": round(total_salarial * mois_idx, 2),
            "net_imposable": round(net_imposable * mois_idx, 2),
            "heures": round(heures * mois_idx, 2),
            "part_patronale": round(total_patronal * mois_idx, 2),
        }

    return {
        "heures": heures,
        "taux_horaire_base": taux_horaire_base,
        "salaire_base": salaire_base,
        "prime_habillage": prime_habillage,
        "salaire_brut": brut,
        "taux_horaire_brut": taux_horaire_brut,
        "base_ss": base_ss,
        "base_csg": base_csg,
        "base_mutuelle": float(p.get("base_mutuelle", 3428.00)),
        "evolution_remuneration": float(p.get("evolution_remuneration", 50.82)),
        "cotisations": {
            "mutuelle_salariale": s_mutuelle,
            "mutuelle_patronale": p_mutuelle,
            "maladie_ss_patronale": p_maladie_ss,
            "accident_travail_patronale": p_at_mp,
            "retraite_plafonnee_salariale": s_ret_plaf,
            "retraite_plafonnee_patronale": p_ret_plaf,
            "retraite_deplafonnee_salariale": s_ret_deplaf,
            "retraite_deplafonnee_patronale": p_ret_deplaf,
            "agirc_t1_salariale": s_agirc_t1,
            "agirc_t1_patronale": p_agirc_t1,
            "famille_patronale": p_famille,
            "chomage_patronale": p_chomage,
            "autres_contributions_patronale": p_autres,
            "csg_deductible": s_csg_ded,
            "csg_crds_non_deductible": s_csg_nonded,
        },
        "total_retenues_salariales": total_salarial,
        "total_retenues_patronales": total_patronal,
        "reintegration_mutuelle": p_mutuelle,
        "net_imposable": net_imposable,
        "montant_net_social": montant_net_social,
        "taux_pas": taux_pas,
        "pas_montant": pas_montant,
        "frais_professionnels": frais_pro,
        "net_avant_impot": net_avant_impot,
        "net_a_payer": net_a_payer,
        "allegement_cotisations": allegement,
        "total_verse_employeur": total_verse,
        "cumuls": cumuls,
        "taux_agirc_sal": t_agirc_sal,
        "taux_agirc_pat": t_agirc_pat,
    }
