from datetime import datetime

BANNER_LEAD = "   Une question ? Nos experts Dafy sont à votre écoute au"
BANNER_PHONE = " 04 73 26 85 69"
BANNER_NOTE = " (appel non surtaxé)"

TITLE_PREFIX = "FACTURE N\u00b0"

ISSUER_NOM = "Service Client Dafy"
ISSUER_LIGNES = (
    "Z.A. de l\u2019Arti\u00e8re",
    "Rue Henri Becquerel",
    "63 110 Beaumont",
    "04 73 26 85 69",
)

REF_LABELS = (
    "Num\u00e9ro de client",
    "Date de commande",
    "Date de facturation",
    "N\u00b0 commande",
    "Moyen de paiement",
)

SHIP_TITLE = (
    " Adresse de livraison : Point de retrait par",
    "Chronopost",
)
SHIP_TITLE_DOMICILE = (" Adresse de livraison : En 24h par Chronopost",)
SHIP_TITLE_MAGASIN = (" Adresse de livraison : Magasin Dafy",)
BILL_TITLE = "Adresse de facturation :"
LIVRAISON_CHRONO = "chronopost"
LIVRAISON_DOMICILE = "domicile"
LIVRAISON_MAGASIN = "magasin"
LIVRAISON_MODES = (
    ("chronopost", "Point de retrait Chronopost"),
    ("domicile", "Chronopost à domicile"),
    ("magasin", "Magasin Dafy"),
)
MAGASIN_NOM = "Dafy Moto Paris"

NOM = "Martin"
PRENOM = "Lucas"
CLIENT_NOM = "MARTIN LUCAS"
ADRESSE = "12 Rue des Fleurs"
CP_VILLE = "75011 PARIS"
PAYS = "France"
LIVRAISON_EXTRA = ""

NUM_CLIENT = "378062"
NUM_COMMANDE = "2350151"
NUM_FACTURE = "71266024"

PAYMENT = "PayPal"
PAYMENT_MODES = (
    "PayPal",
    "Carte bancaire",
    "Apple Pay",
    "Virement",
)

COL_LABELS = (
    "R\u00e9f\u00e9rence",
    "Description",
    "Qt\u00e9",
    "PU HT",
    "TVA",
    "Montant HT",
)
ATTR_COULEUR = "Couleur"
ATTR_TAILLE = "Taille"
ATTR_SEP = " : "

TOTAL_HT = "Montant total HT"
TOTAL_TTC = "Total net TTC"
TOTAL_REMISE = "Remise"
TOTAL_PORT = "Frais de port"
TOTAL_DUE = "Total \u00e0 r\u00e9gler"
TOTAL_TVA = "Dont TVA"

SKU = "1001100"
DESC = "Sweat capuche"
COULEUR = "Noir"
TAILLE = "M"
QTE = "1"
PU = "80,00"
TVA = "20"

SKU2 = "1001101"
DESC2 = "Pantalon jogging"
PU2 = "60,00"

REMISE = "0,00"
PORT = "3,99"

THANKS = "Merci pour votre achat sur www.dafy-moto.com ! A bient\u00f4t"

LEGAL = (
    "Service Client Dafy - Rue Henri Becquerel - 63 110 Beaumont - France",
    "Siret : 824 484 026 00011 - TVA Intracom : FR 08 824484026",
    "DAFY@STORE SAS au capital de 20000\u20ac",
    "T\u00e9l : 04 73 26 85 69 - Email : serviceclient@dafy-moto.com",
    "Site internet : www.dafy-moto.com",
)


def slash_date(d=None) -> str:
    d = d or datetime.now()
    return f"{d:%d/%m/%Y}"
