import io

import fitz

from . import rules
from .data import from_payload
from .generate import generate, generate_pack
from .services.informations import get_default_table
from .services.orchestration import generate_payroll_sequence

# ----------------------------------------------------------------------


def defaults(mode: str = "en_ligne", **kwargs) -> dict:
    tbl = get_default_table()
    emp = tbl["employeur"]
    sal = tbl["salarie"]
    per = tbl["periode"]
    rem = tbl["remuneration"]
    cng = tbl["conges"]
    return {
        "_limits": rules.public_limits(),
        "_rules": rules.public_rules(),

        "duree_mois": 3,
        "start_month": "",
        "start_year": "",

        "header": True,
        "header_employeur": True,
        "header_titre": True,
        "header_periode": True,
        "header_salarie": True,
        "header_convention": True,

        "middle": True,
        "middle_tableau_cotisations": True,
        "middle_net_avant_impot": True,
        "middle_impot_source": True,

        "footer": True,
        "footer_conges": True,
        "footer_cumuls": True,
        "footer_recapitulatif": True,
        "footer_mentions": True,

        "raison_sociale": emp["raison_sociale"],
        "adresse": emp["adresse"],
        "code_postal": emp["code_postal"],
        "ville": emp["ville"],
        "etablissement": emp["etablissement"],
        "siret": emp["siret"],
        "code_naf": emp["code_naf"],
        "convention_collective_court": emp["convention_collective_court"],

        "date_debut": per["date_debut"],
        "date_fin": per["date_fin"],
        "date_paiement": per["date_paiement"],
        "mode_paiement": per["mode_paiement"],
        "plafond_mensuel_ss": f"{per['plafond_mensuel_ss']:.2f}",

        "nom_complet": sal["nom_complet"],
        "salarie_adresse": sal["adresse"],
        "salarie_cp": sal["code_postal"],
        "salarie_ville": sal["ville"],
        "matricule": sal["matricule"],
        "nir": sal["nir"],
        "emploi": sal["emploi"],
        "qualification": sal["qualification"],
        "echelon": sal["echelon"],
        "coefficient": sal["coefficient"],
        "date_anciennete": sal["date_anciennete"],

        "net_a_payer_cible": f"{rem['net_a_payer_cible']:.2f}",
        "heures_mensuelles": f"{rem['heures_mensuelles']:.2f}",
        "prime_habillage": f"{rem['prime_habillage']:.2f}",
        "frais_professionnels": f"{rem['frais_professionnels']:.2f}",
        "mutuelle_salarie": f"{rem['mutuelle_salarie']:.2f}",
        "mutuelle_patronale": f"{rem['mutuelle_patronale']:.2f}",
        "allegement_cotisations": f"{rem['allegement_cotisations']:.2f}",
        "taux_pas": f"{rem['taux_pas']:.2f}",

        "cp_n1_du": f"{cng['cp_n1_du']:.2f}",
        "cp_n1_pris": f"{cng['cp_n1_pris']:.2f}",
        "cp_n1_reste": f"{cng['cp_n1_reste']:.2f}",
        "cp_n_du": f"{cng['cp_n_du']:.2f}",
        "cp_n_pris": f"{cng['cp_n_pris']:.2f}",
        "cp_n_reste": f"{cng['cp_n_reste']:.2f}",
        "repos_compensateur_du": f"{cng['repos_compensateur_du']:.2f}",
        "repos_compensateur_pris": f"{cng['repos_compensateur_pris']:.2f}",
        "repos_compensateur_reste": f"{cng['repos_compensateur_reste']:.2f}",
    }


def pdf_bytes(payload: dict | None = None) -> bytes:
    doc = from_payload(payload)
    buf = io.BytesIO()
    generate(doc, dest=buf)
    return buf.getvalue()


def pack_pdf_bytes(payload: dict | None = None, count: int = 3) -> bytes:
    docs = generate_payroll_sequence(payload, count=count)
    buf = io.BytesIO()
    generate_pack(docs, dest=buf)
    return buf.getvalue()


def png_from_pdf(pdf: bytes, scale: float = 2.0, page_index: int = 0) -> bytes:
    doc = fitz.open(stream=pdf, filetype="pdf")
    idx = min(page_index, len(doc) - 1)
    pix = doc[idx].get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False)
    doc.close()
    return pix.tobytes("png")


def png_bytes(payload: dict | None = None, scale: float = 2.0) -> bytes:
    return png_from_pdf(pdf_bytes(payload), scale)
