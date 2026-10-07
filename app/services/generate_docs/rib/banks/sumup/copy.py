from app.services.generate_docs.common import example_dates as _dates

TITLE = "Account details statement"


def __getattr__(name: str):
    if name == "DATE":
        return _dates.sumup_document()
    if name == "DATE_OUVERTURE":
        return _dates.sumup_opening()
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


HOLDER_TITLE = "Account holder details"
LABEL_NAME = "Name"
LABEL_ADDRESS = "Address"

CIVILITE = "M."
NOM = "MARTIN"
PRENOM = "LUCAS"
TITULAIRE_NOM = "MARTIN LUCAS"
TITULAIRE_ADRESSE = "12 RUE DES FLEURS"
TITULAIRE_VILLE = "75011 Paris"
TITULAIRE_PAYS = "France"

ACCOUNT_TITLE = "Account details"
LABEL_OPENING = "Opening date"
LABEL_INSTITUTION = "Institution"
LABEL_IBAN = "IBAN"
LABEL_BIC = "BIC"
INSTITUTION = "SumUp Limited"
IBAN = "IE10SUMU00000112350000"
BIC = "SUMUIE22XXX"

NOTICE = (
    "Give this statement to any organization that needs to know your account "
    "details for the setup and execution of payments into or out of your account.\n\n"
    "This document was created automatically and is valid without a signature."
)

FOOTER_LEFT = (
    "SumUp Limited\n"
    "Block 8, Harcourt Centre, Charlotte Way,\n"
    "Dublin D02 A9N9, Ireland\n"
    "VAT ID: IE9813461A"
)

FOOTER_RIGHT = (
    "SumUp Limited, trading as SumUp,\n"
    "is regulated by the Central Bank of Ireland."
)
