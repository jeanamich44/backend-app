from . import rib

TITLE = "IBAN"

LABEL_IBAN = "IBAN Identifiant International de Compte Bancaire"
LABEL_IBAN_RUNS = (
    ("IBAN Identifiant Int", 5.0),
    ("ernational de Compt", 5.0),
    ("e Bancair", 22.0),
    ("e", 0),
)
LABEL_IBAN_EN = "International Bank Account Number"
LABEL_IBAN_EN_RUNS = (
    ("Int", 5.0),
    ("ernational Bank Account Number", 0),
)
LABEL_BIC = "BIC Identifiant Internationnal de l’Etablissement "
LABEL_BIC_RUNS = (
    ("BIC Identifiant Int", 5.2),
    ("ernationnal de l’Etablissement ", 0),
)
LABEL_BIC_EN = "(Bank Identifier Code)"
LABEL_TITULAIRE = "Titulaire"
LABEL_TITULAIRE_RUNS = (
    ("Titulair", 22.0),
    ("e", 0),
)
LABEL_OWNER = "Account Owner"
LABEL_DOM = "Domiciliation"
LABEL_DOM_RUNS = (
    ("D", -8.0),
    ("omiciliation", 0),
)
LABEL_INSTITUTE = "Institute"
COMING_SOON = "(coming soon)"

NOTICE_1 = (
    "Remettez ce relevé à tout organisme ayant besoin de connaître vos "
    "références bancaires pour la domiciliation "
)
NOTICE_1_TW = 0.038
NOTICE_1_RUNS = (
    ("R", 5.0),
    ("emett", 5.0),
    ("ez ce r", 22.0),
    ("el", 10.0),
    ("e", 5.0),
    ("v", 5.0),
    ("é à t", 5.0),
    ("out or", 15.0),
    ("g", 5.0),
    ("anisme a", 12.0),
    ("y", -40.0),
    ("ant besoin de connaîtr", 22.0),
    ("e v", 5.0),
    ("os r", 22.0),
    ("éfér", 22.0),
    ("ences bancair", 22.0),
    ("es pour la domiciliation ", 0),
)
NOTICE_2 = (
    "de vos virements ou de prélèvements à votre compte. Vous éviterez "
    "ainsi des erreurs ou des retards d’exécution."
)
NOTICE_2_TW = -0.013
NOTICE_2_RUNS = (
    ("de v", 5.0),
    ("os vir", 22.0),
    ("ement", -20.0),
    ("s ou de pr", 22.0),
    ("él", 10.0),
    ("è", 5.0),
    ("v", 5.0),
    ("ement", -20.0),
    ("s à v", 5.0),
    ("otr", 22.0),
    ("e compt", 5.0),
    ("e. V", 23.0),
    ("ous é", 5.0),
    ("vit", 5.0),
    ("er", 22.0),
    ("ez ainsi des err", 22.0),
    ("eurs ou des r", 22.0),
    ("etar", 22.0),
    ("ds d’e", 7.0),
    ("x", 11.0),
    ("écution.", 0),
)

CIVILITE = "M."
NOM = "MARTIN"
PRENOM = "LUCAS"
TITULAIRE_NOM = "Martin Lucas"
ADRESSE = "12 Rue des Fleurs"
TITULAIRE_RUE = "12 Rue des Fleurs"
CP = "75011"
VILLE = "Paris"
TITULAIRE_VILLE = "75011 Paris"
PAYS = "France"
TITULAIRE_PAYS = "France"

DOM_RUE = "11, Place François Mitterrand"
DOM_VILLE = "49 100 ANGERS "

BANQUE = "16330"
GUICHET = "00001"
COMPTE = "00012345678"
CLE = rib.cle_rib(BANQUE, GUICHET, COMPTE)
IBAN = rib.iban_fr(BANQUE, GUICHET, COMPTE, CLE)
BIC = "AFOPFR21XXX"

_SMALL = {
    "de", "du", "des", "la", "le", "les", "et", "en", "au", "aux",
    "d'", "l'", "da", "di", "do",
}


def title_case(text: str) -> str:
    text = (text or "").strip()
    if not text:
        return text
    out = []
    for i, raw in enumerate(text.split(" ")):
        if not raw:
            continue
        if raw.isdigit():
            out.append(raw)
            continue
        bits = []
        for j, chunk in enumerate(raw.split("-")):
            if len(chunk) > 2 and chunk[1] in "'’":
                bits.append(
                    chunk[0].lower() + chunk[1] + chunk[2:].capitalize()
                )
                continue
            low = chunk.lower()
            if (i > 0 or j > 0) and low in _SMALL:
                bits.append(low)
            elif chunk:
                bits.append(chunk[0].upper() + chunk[1:].lower())
            else:
                bits.append(chunk)
        out.append("-".join(bits))
    return " ".join(out)
