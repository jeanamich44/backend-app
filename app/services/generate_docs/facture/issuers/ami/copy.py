from app.services.generate_docs.common import example_dates as _dates

BRAND = "AMI PARIS - ALEXANDRE MATTIUSSI"
TITLE = "FACTURE"

ISSUER_NOM = "Alexandre MATTIUSSI "
PHONE = "09.77.40.87.63"
ISSUER_ADDR = "Paris - 14 Rue d'Alger"

PO_LINE = "Numéro de boîte postale : 01480"
SHIP_LINE = "Envoi Express : 2/3 jours"
DATE_PREFIX = "Date : "
INVOICE_PREFIX = "Numéro de facture : "

NOM = "Martin"
PRENOM = "Lucas"
CLIENT_NOM = "Martin Lucas"
CLIENT_RUE = "12 Rue des Fleurs"
ADRESSE = "Martin Lucas - 12 Rue des Fleurs"
CP = "75011"
NUM_FACTURE = "67 459"

THANKS = (
    "Thank you for your trust. It is a pleasure to collaborate on your projet. Your next",
    "order will be shipped in 30 days.",
)
SINCERELY = "Sincerely,"
SIGN_NAME = "Urna Semper"

COL_DESC = "Description"
COL_QTY = "Quantité"
COL_PRICE = "Prix à "
COL_COST = "Coût"
SUBTOTAL = "Sous-total"
TAX = "Taxe"
TOTAL = "Total"

DESC = "Sweat capuche noir"
QTE = "1"
PU = "80,00"
TVA = "20"


def slash_date(d=None) -> str:
    return _dates.ami_invoice(d)
