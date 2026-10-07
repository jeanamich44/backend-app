from . import copy

def get_form_schema() -> dict:
    return {
        "metadata": {
            "title": "GÉNÉRATEUR RIB BFORBANK",
            "logo": "bfb",
            "apiBase": "/api/generate-docs/rib/bfb",
            "headerBg": "bg-gradient-to-br from-blue-800/30 to-slate-950/80 border-blue-400/30",
            "priceKey": "bfb",
            "subtitle": "Document PDF BforBank officiel",
            "filenameTemplate": f"RIB_BFB_{copy.NOM}.pdf"
        },
        "defaults": {
            "nom": copy.NOM,
            "prenom": copy.PRENOM,
            "adresse": copy.RUE,
            "cp": "75011",
            "ville": "PARIS",
            "code_banque": copy.BANQUE,
            "guichet": copy.GUICHET,
            "compte": copy.COMPTE,
            "cle": copy.CLE,
            "iban": copy.IBAN,
            "bic": copy.BIC,
            "header": "true",
            "header_logo": "true",
            "header_adresse": "true",
            "header_title": "true",
            "middle": "true",
            "middle_card": "true",
            "middle_titulaire": "true",
            "middle_iban": "true",
            "middle_bic": "true",
            "middle_table": "true",
            "middle_domiciliation": "true",
            "footer": "true"
        },
        "sections": [
            {
                "id": "titulaire_section",
                "title": "Titulaire",
                "order": 1,
                "fields": [
                    {
                        "key": "nom",
                        "label": "Nom",
                        "kind": "text",
                        "span": 1,
                        "placeholder": "EX: MARTIN",
                        "rules": {"required": True, "min": 2, "max": 35, "transform": "uppercase"}
                    },
                    {
                        "key": "prenom",
                        "label": "Prénom",
                        "kind": "text",
                        "span": 1,
                        "placeholder": "EX: LUCAS",
                        "rules": {"required": True, "min": 2, "max": 35, "transform": "uppercase"}
                    },
                    {
                        "key": "adresse",
                        "label": "Adresse",
                        "kind": "address",
                        "span": 2,
                        "placeholder": "EX: 12 RUE DES FLEURS",
                        "rules": {"required": True, "min": 5, "max": 60, "transform": "uppercase"}
                    },
                    {
                        "key": "cp",
                        "label": "Code postal",
                        "kind": "cp",
                        "span": 1,
                        "placeholder": "EX: 75011",
                        "rules": {"required": True, "min": 5, "max": 5, "transform": "digits_only"}
                    },
                    {
                        "key": "ville",
                        "label": "Ville",
                        "kind": "ville",
                        "span": 1,
                        "placeholder": "EX: PARIS",
                        "rules": {"required": True, "min": 2, "max": 45, "transform": "uppercase"}
                    }
                ]
            },
            {
                "id": "coordonnees_bancaires",
                "title": "Coordonnées bancaires",
                "order": 2,
                "fields": [
                    {
                        "key": "code_banque",
                        "label": "Code Banque",
                        "kind": "digits",
                        "span": 1,
                        "autoIban": "banque",
                        "placeholder": "16218",
                        "rules": {"required": True, "min": 5, "max": 5, "transform": "digits_only"}
                    },
                    {
                        "key": "guichet",
                        "label": "Code Guichet",
                        "kind": "digits",
                        "span": 1,
                        "autoIban": "guichet",
                        "placeholder": "00001",
                        "rules": {"required": True, "min": 5, "max": 5, "transform": "digits_only"}
                    },
                    {
                        "key": "compte",
                        "label": "N° de Compte",
                        "kind": "alnum",
                        "span": 1,
                        "autoIban": "compte",
                        "placeholder": "31284765011",
                        "rules": {"required": True, "min": 11, "max": 11, "transform": "uppercase"}
                    },
                    {
                        "key": "cle",
                        "label": "Clé RIB",
                        "kind": "digits",
                        "span": 1,
                        "autoIban": "cle",
                        "placeholder": "51",
                        "rules": {"required": True, "min": 2, "max": 2, "transform": "digits_only"}
                    },
                    {
                        "key": "iban",
                        "label": "IBAN",
                        "kind": "iban",
                        "span": 2,
                        "placeholder": "FR76 1621 8000 0131 2847 6501 151",
                        "rules": {"required": True, "min": 27, "max": 34, "transform": "uppercase"}
                    },
                    {
                        "key": "bic",
                        "label": "BIC / SWIFT",
                        "kind": "bic",
                        "span": 2,
                        "placeholder": "BFBKFRP1",
                        "rules": {"required": True, "min": 8, "max": 11, "transform": "uppercase"}
                    }
                ]
            }
        ],
        "customLayout": {
            "sections": [
                {"id": "header", "label": "En-tête"},
                {"id": "middle", "label": "Corps du document"},
                {"id": "footer", "label": "Pied de page"}
            ],
            "blocks": [
                {"id": "header", "label": "En-tête", "master": True, "section": "header"},
                {"id": "header_logo", "label": "Logo", "master": False, "section": "header"},
                {"id": "header_adresse", "label": "Adresse émetteur", "master": False, "section": "header"},
                {"id": "header_title", "label": "Titre", "master": False, "section": "header"},
                {"id": "middle", "label": "Corps du document", "master": True, "section": "middle"},
                {"id": "middle_card", "label": "Cadre principal", "master": False, "section": "middle"},
                {"id": "middle_titulaire", "label": "Bloc titulaire", "master": False, "section": "middle"},
                {"id": "middle_iban", "label": "IBAN", "master": False, "section": "middle"},
                {"id": "middle_bic", "label": "BIC", "master": False, "section": "middle"},
                {"id": "middle_table", "label": "Tableau RIB", "master": False, "section": "middle"},
                {"id": "middle_domiciliation", "label": "Bloc domiciliation", "master": False, "section": "middle"},
                {"id": "footer", "label": "Pied de page", "master": True, "section": "footer"}
            ],
            "visible": {
                "header": True,
                "header_logo": True,
                "header_adresse": True,
                "header_title": True,
                "middle": True,
                "middle_card": True,
                "middle_titulaire": True,
                "middle_iban": True,
                "middle_bic": True,
                "middle_table": True,
                "middle_domiciliation": True,
                "footer": True
            }
        }
    }
