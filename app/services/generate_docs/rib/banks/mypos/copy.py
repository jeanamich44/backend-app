from app.services.generate_docs.common import example_dates as _dates

TITLE = "Certificat IBAN"


def __getattr__(name: str):
    if name == "DATE":
        return _dates.mypos_edition()
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


BRAND = "myPOS Ltd"
ADDR_1 = "12 St. Stephen’s Green,"
ADDR_2 = "Dublin D02 WK11,"
ADDR_3 = "Ireland"

GREETING = "A qui cela peut s'adresser,"

NOM_SOCIETE = "LUCAS ENTREPRISE SASU"
NUM_ENREGISTREMENT = "123456789"
ADRESSE = "12 RUE DES FLEURS"
CP = "75011"
VILLE = "PARIS"
CP_VILLE = "75011 PARIS"
PAYS = "France Métropolitaine"
TITULAIRE = "MARTIN LUCAS"
COMPTE = "00012345"

TRANSFER = (
    "Les transferts bancaires en faveur de notre client doit être "
    "effectuée à l'IBAN:"
)

LABEL_BENEF = "Nom du Bénéficiaire:"
LABEL_IBAN = "IBAN:"
LABEL_DEVISE = "Devise du compte:"
LABEL_INSTITUTION = "IBAN avec l'Institution:"
LABEL_BIC = "BIC:"

INSTITUTION = "myPOS Ltd"
DEVISE = "EUR"
IBAN = "IE12MPOS99039000012345"
BIC = "MPOSIE2D"

FOOTER_1 = (
    "myPOS Ltd, immatriculée sous le numéro 700880, est un établissement "
    "de monnaie électronique agréé sous le contrôle de la Banque"
)
FOOTER_2 = (
    "centrale d’Irlande, avec le numéro de référence C475122. "
    "Siège social : 12 St. Stephen’s Green, Dublin D02 WK11, Ireland"
)
PAGE_NO = "1"


def split_cp_ville(cp_ville: str) -> tuple[str, str]:
    text = (cp_ville or "").strip()
    if not text:
        return "", ""
    parts = text.split(None, 1)
    if parts[0].isdigit():
        return parts[0], parts[1] if len(parts) > 1 else ""
    return "", text


def confirm_blocks(card) -> tuple[str, ...]:
    nom = card.nom_societe or ""
    siren = card.num_enregistrement or ""
    rue = card.adresse or ""
    cp, ville = split_cp_ville(card.cp_ville)
    pays = card.pays or ""
    titulaire = card.titulaire or ""
    compte = card.compte or ""
    adresse = rue
    if cp:
        adresse = f"{rue}, {cp}" if rue else cp
    lieu = ", ".join(part for part in (ville, pays) if part)
    return (
        f"Nous confirmons par la présente que  {nom} de numéro",
        f"d'enregistrement: {siren} et adresse d'enregistrement: {adresse}",
        (
            f"{lieu} representé par {titulaire} "
            f"a un compte de monnaie électronique myPOS Numéro {compte}"
        ),
    )


def confirm_paragraph(card) -> str:
    return " ".join(confirm_blocks(card))
