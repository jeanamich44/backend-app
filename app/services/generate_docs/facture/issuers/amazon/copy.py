from app.services.generate_docs.common import example_dates as _dates

TITLE = "Facture"
PAYE = "Payé "
PAY_REF_PREFIX = "Référence de paiement "
PAY_SOLD_PREFIX = "Vendu par "
PAY_TVA_PREFIX = "TVA "
PAY_DATE = "Date de la facture/Date de la livraison"
PAY_INV = "Numéro de la facture"
PAY_INV_CONT = "Numéro de la facture "
PAY_TOTAL = "Total à payer"

CONTACT = "Veuillez contacter le Service Client en visitant le lien suivant: "
CONTACT_URL = "www.amazon.fr/contact-us"

BILL_TITLE = "Adresse de facturation"
SHIP_TITLE = "Adresse de livraison"
SELLER_TITLE = "Vendu par"

ORDER_TITLE = "Informations de la commande"
ORDER_DATE_LABEL = "Date de la commande"
ORDER_NUM_LABEL = "Numéro de la commande"

NOM = "Martin"
PRENOM = "Lucas"
CLIENT_NOM = "Martin Lucas"
ADRESSE = "12 Rue des Fleurs"
VILLE = "Paris, 75011"
VILLE_DEPT = "PARIS, 75011"
PAYS = "FR"

SELLER_AMZ = "Amazon EU S.à r.l., Succursale Française"
SELLER_AMZ_ADDR = "67 Boulevard du General Leclerc"
SELLER_AMZ_CITY = "Clichy 92110"
SELLER_AMZ_PAYS = "France"
SELLER_AMZ_TVA = "LU19647148"

SELLER_MKP = "EUROSTORE"
SELLER_MKP_ADDR = "18 Rue du Commerce"
SELLER_MKP_CITY = "Paris, 75015"
SELLER_MKP_PAYS = "FR"
SELLER_MKP_TVA = "FR10011001100"

PAYMENT_REF = "2MVI3VL9HC4A0NEC"
NUM_FACTURE_AMZ = "DS-ASE-INV-FR-2022-172445727"
NUM_FACTURE_MKP = "FR26MKP10011"
NUM_COMMANDE = "403-2699905-9515527"
TOTAL = "120,00 €"


def __getattr__(name: str):
    if name == "DATE_FACTURE":
        return _dates.amazon_invoice()
    if name == "DATE_COMMANDE":
        return _dates.amazon_order()
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

DETAILS = "Détails de la facture"
COL_DESC = "Description"
COL_QTE = "Qté"
COL_PU = "Prix Unitaire"
COL_TVA = "Taux TVA"
COL_TOTAL = "Total"
COL_HT = "HT"
COL_TTC = "TTC"
TVA_TEXT = "20 %"
VAT_TAUX = "Taux TVA"
VAT_TOTAL_HT = "Total HT"
VAT_TVA = "TVA"
VAT_TOTAL = "Total"
LIVRAISON_LABEL = "Frais d'expédition"
REMISE_LABEL = "Remise"
GRAND_LABEL = "Facture Total"
ASIN_PREFIX = "ASIN: "
NOTE_PIECES = "Information indisponible sur les pièces détachées"

PRODUIT = "Casque audio sans fil Bluetooth, autonomie 30 h."
QTE = "1"
PU_HT = "100,00"
PU_TTC = "120,00"
ASIN = "B0C3D81M43"
EXPEDITION_HT = "0,00"
EXPEDITION_TTC = "0,00"
REMISE_HT = "0,00"
REMISE_TTC = "0,00"

LEGAL_EU = (
    "Nos prix des équipements électriques et électroniques incluent l'éco-participation, conformément à l’article L. 541-10-2 du code de l'environnement. ",
    "LU-BIO-04 ",
    "Amazon EU S.à r.l. - 38 avenue John F. Kennedy, L-1855 Luxembourg ",
    "R.C.S. Luxembourg : B 101818 • Capital Social: 37.500 EUR • N° de licence: 104408 • N° de TVA intracommunautaire: LU20260743 ",
    "Amazon EU S.à r.l., Succursale Française – 67 Boulevard du Général Leclerc, 92110 Clichy, France ",
    "SIREN : 487773327 • RCS Nanterre • APE : 4791B • TVA : FR 12487773327",
)
LEGAL_OSS = (
    "La TVA du pays de livraison a été facturée et sera reportée sous le numéro de TVA Guichet Unique (OSS) mentionné sur cette facture",
)
PAGE_LABEL = "Page "
PAGE_OF = " de "
