from datetime import datetime
from app.services.generate_docs.common import example_dates as _dates

# ----------------------------------------------------------------------

CIVILITY = "M. "
CIVILITE = "M."
NOM = "Martin"
PRENOM = "Lucas"
NOM_COMPLET = "MARTIN LUCAS"
ADRESSE = "12 Rue des Fleurs"
CP = "75011"
VILLE = "Paris"
CP_VILLE = "75011 Paris"

TITLE = "Attestation d'abonnement"
SITE = "www.direct-energie.com"
REF = "Ref courrier : CS197"
NUM_CLIENT = "103866054"
DEPUIS = "1 Janvier 2020"

CLIENT_LABEL = "Référence client "
GREETING = "Madame, Monsieur,"
CONFIRM_TAIL = "l'adresse suivante :"
RIGHT = "La présente attestation est faite pour servir et valoir ce que de droit."
ADVICE = (
    "Nous vous conseillons de joindre, même si elle a plus de trois mois, votre dernière facture Direct Energie à ce ",
    "document. Vous la trouverez sur espaceclient.direct-energie.com",
)
CLOSING = "Je vous prie d'agréer, Madame, Monsieur, l'expression de mes salutations distinguées."
SIGN_NAME = "Cédric Belloir"
SIGN_ROLE = " Directeur de la Relation Client"
NOTE = (
    "*Ce contrat a été établi à votre nom, sur la base de vos déclarations lors de la "
    "souscription. Le présent document peut valoir justificatif de domicile."
)

LEGAL = (
    "DIRECT ENERGIE au capital de 4 514 788 € - 442 395 448 RCS Paris - 2 bis, rue Louis Armand - 75015 PARIS",
    "L'énergie est notre avenir, économisons-la !",
)

MONTHS = (
    "",
    "janvier", "février", "mars", "avril", "mai", "juin",
    "juillet", "août", "septembre", "octobre", "novembre", "décembre",
)


def paris_date(d=None) -> str:
    d = d or datetime.now()
    return f"Paris, le {d.day} {MONTHS[d.month]} {d.year}"


def confirm_line(depuis: str) -> str:
    date = (depuis or "").strip()
    return (
        "Suite à votre demande, je vous confirme qu'à ce jour et depuis le "
        f"{date}, vous faites partie de nos clients pour "
    )


def __getattr__(name: str):
    if name == "DATE":
        return _dates.edf_attestation()
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
