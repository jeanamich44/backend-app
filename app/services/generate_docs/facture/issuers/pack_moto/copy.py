from datetime import datetime

TITLE = "FACTURE"
SHIP_TITLE = "Adresse de livraison"
BILL_TITLE = "Adresse de facturation"

NOM = "Martin"
PRENOM = "Lucas"
CLIENT_NOM = "martin lucas"
SOCIETE = ""
ADRESSE_SHIP = "12 RUE DES FLEURS"
CP_SHIP = "75011 PARIS"
ADRESSE_BILL = "12 rue des fleurs"
CP_BILL = "75011 paris"
PAYS = "France Métropolitaine"

NUM_FACTURE = "#FA044682"

RETURNS = (
    "Pour toute demande de RETOUR PRODUIT, à effectuer dans les 30 JOURS.",
    "=> Veuillez nous contacter par mail à l'adresse suivante :",
    "contact@packmoto.fr et indiquer le numéro de facture et le motif de retour.",
    "Attention, les produits retournés doivent être neufs, dans leur emballage",
    "d\u2019origine, avec l\u2019étiquette et sans trace d\u2019usure.",
    "Sans respect de ces conditions, le retour pourra être refusé.",
)

LEGAL = (
    "PACKMOTO - 116 Rue de la fraternité - 93170 Bagnolet - France (Métropolitaine)",
    "Pour toute assistance, merci de nous contacter :",
    "Tél. : 0175348190",
)

TCPDF = "Powered by TCPDF (www.tcpdf.org)"

REF_LABELS = (
    "Numéro de facture",
    "Date de facturation",
    "Réf. de commande",
    "Date de commande",
    "Numéro de TVA",
)

TAX_KIND = "Produits"
TAX_RATE = "20"
SHIP_FREE = "Livraison gratuite"
TOTAL_PRODUCTS = "Total produits"
TOTAL_SHIP = "Frais de livraison"
TOTAL_HT = "Total (HT)"
TOTAL_TAX = "Taxe totale"
TOTAL = "Total"

PAY_LABEL = "Moyen de paiement"
CARRIER_LABEL = "Transporteur"
PAYMENT = "Carte bancaire"
TRANSPORTEUR = "Colissimo"
NUM_COMMANDE = "TSKNTPLVH"

SKU = "8009578142"
DESC = "Casque bluetooth"
QTE = "1"
PU = "80,00"
TVA = "20"
FRAIS = "0,00"


def slash_date(d=None) -> str:
    d = d or datetime.now()
    return f"{d:%d/%m/%Y}"
