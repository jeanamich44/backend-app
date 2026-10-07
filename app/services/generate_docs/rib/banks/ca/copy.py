from app.services.generate_docs.common import example_dates as _dates
from . import rib

TITLE = "RELEVÉ D'IDENTITÉ BANCAIRE"

CRUMB = "Accueil (/ca-toulouse31/association/operations/synthese.html)"
CRUMB_SEP = " >  "
CRUMB_LINK = "Editez un RIB"

NOTICE = (
    "Ce relevé est destiné à tout organisme souhaitant connaître vos références "
    "bancaires pour domicilier des virements ou des prélèvements sur votre compte"
)

CAISSE = "CR TOULOUSE 31"
AGENCE = "TOULOUSE CAPITOLE"
LABEL_TEL = "Tel. "
LABEL_FAX = "Fax. "
TEL = "0562107433"
FAX = "0810031204"
CODE = "00350"


def __getattr__(name: str):
    if name == "DATE":
        return _dates.ca_edition()
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


CIVILITE = "M."
NOM = "MARTIN"
PRENOM = "LUCAS"
TITULAIRE_NOM = "M. MARTIN LUCAS"
TITULAIRE_OPT = ""
ADRESSE = "12 RUE DES FLEURS"
TITULAIRE_RUE = "12 RUE DES FLEURS"
CP = "75011"
VILLE = "PARIS"
TITULAIRE_VILLE = "75011 PARIS"

LABEL_TITULAIRE = "Intitulé du compte"
LABEL_DOM = "Domiciliation"
DOMICILIATION = ""

COL_BANQUE = "Code banque"
COL_GUICHET = "Code guichet"
COL_COMPTE = "Numéro de compte"
COL_CLE = "Clé RIB"

BANQUE = "13106"
GUICHET = "00500"
COMPTE = "30021598310"
CLE = rib.cle_rib(BANQUE, GUICHET, COMPTE)
IBAN = rib.iban_fr(BANQUE, GUICHET, COMPTE, CLE)
BIC = "AGRIFRPP831"

LABEL_IBAN = "IBAN"
LABEL_BIC = "Code BIC (Bank identification code) - code SWIFT"
