from . import copy

def get_form_schema() -> dict:
    return {
        "metadata": {
            "title": "GÉNÉRATEUR RIB BOURSOBANK",
            "logo": "boursobank",
            "apiBase": "/api/generate-docs/rib/boursobank",
            "headerBg": "bg-gradient-to-br from-pink-950/40 to-slate-950/80 border-pink-500/30",
            "priceKey": "boursobank",
            "subtitle": "Document PDF BoursoBank officiel",
            "filenameTemplate": f"RIB_BoursoBank_{copy.NOM}.pdf"
        },
        "defaults": {
            "civilite": copy.CIVILITE,
            "nom": copy.NOM,
            "prenom": copy.PRENOM,
            "adresse": copy.ADRESSE,
            "cp": copy.CP,
            "ville": copy.VILLE,
            "code_banque": copy.BANQUE,
            "guichet": copy.GUICHET,
            "compte": copy.COMPTE,
            "cle": copy.CLE,
            "iban": copy.IBAN,
            "bic": copy.BIC,
            "header": "true",
            "header_logo": "true",
            "header_title": "true",
            "header_subtitle": "true",
            "middle": "true",
            "middle_titulaire": "true",
            "middle_bic": "true",
            "middle_iban": "true",
            "middle_domiciliation": "true",
            "middle_table": "true",
            "middle_separator": "true",
            "footer": "true",
            "header_title_text": copy.TITLE,
            "header_subtitle_text": copy.SUBTITLE
        },
        "sections": [
            {
                "id": "titulaire",
                "title": "Titulaire du compte",
                "order": 1,
                "fields": [
                    {
                        "key": "civilite",
                        "label": "Civilité",
                        "kind": "select",
                        "span": 1,
                        "options": [
                            {"label": "M.", "value": "MR"},
                            {"label": "Mme", "value": "MME"},
                            {"label": "Mlle", "value": "MLLE"}
                        ],
                        "rules": {"required": True}
                    },
                    {
                        "key": "nom",
                        "label": "Nom",
                        "kind": "text",
                        "span": 1,
                        "placeholder": "MARTIN",
                        "rules": {"required": True, "min": 2, "max": 40, "transform": "uppercase"}
                    },
                    {
                        "key": "prenom",
                        "label": "Prénom",
                        "kind": "text",
                        "span": 1,
                        "placeholder": "LUCAS",
                        "rules": {"required": True, "min": 2, "max": 40, "transform": "uppercase"}
                    },
                    {
                        "key": "adresse",
                        "label": "Adresse",
                        "kind": "address",
                        "span": 2,
                        "placeholder": "12 RUE DES FLEURS",
                        "rules": {"required": True, "min": 5, "max": 42, "transform": "uppercase"}
                    },
                    {
                        "key": "cp",
                        "label": "Code postal",
                        "kind": "cp",
                        "span": 1,
                        "placeholder": "75011",
                        "rules": {"required": True, "min": 5, "max": 5, "transform": "digits_only"}
                    },
                    {
                        "key": "ville",
                        "label": "Ville",
                        "kind": "ville",
                        "span": 1,
                        "placeholder": "PARIS",
                        "rules": {"required": True, "min": 2, "max": 40, "transform": "uppercase"}
                    }
                ]
            },
            {
                "id": "coordonnees_bancaires",
                "title": "Coordonnées Bancaires",
                "order": 2,
                "fields": [
                    {
                        "key": "code_banque",
                        "label": "Code Banque",
                        "kind": "digits",
                        "span": 1,
                        "autoIban": "banque",
                        "placeholder": "40618",
                        "rules": {"required": True, "min": 5, "max": 5, "transform": "digits_only"}
                    },
                    {
                        "key": "guichet",
                        "label": "Code Guichet",
                        "kind": "digits",
                        "span": 1,
                        "autoIban": "guichet",
                        "placeholder": "80428",
                        "rules": {"required": True, "min": 5, "max": 5, "transform": "digits_only"}
                    },
                    {
                        "key": "compte",
                        "label": "N° de Compte",
                        "kind": "alnum",
                        "span": 1,
                        "autoIban": "compte",
                        "placeholder": "00012345678",
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
                        "placeholder": "FR76 4061 8804 2800 0123 4567 851",
                        "rules": {"required": True, "min": 27, "max": 34, "transform": "uppercase"}
                    },
                    {
                        "key": "bic",
                        "label": "BIC / SWIFT",
                        "kind": "bic",
                        "span": 2,
                        "placeholder": "BOUSFRPPXXX",
                        "rules": {"required": True, "min": 8, "max": 11, "transform": "uppercase"}
                    }
                ]
            },
            {
                "id": "header_section",
                "title": "En-tête",
                "order": 3,
                "hasAdvancedMode": True,
                "fields": [
                    {
                        "key": "header_title_text",
                        "label": "Titre de l'en-tête",
                        "kind": "text",
                        "span": 2,
                        "placeholder": "Relevé d'Identité Bancaire",
                        "rules": {"max": 40}
                    },
                    {
                        "key": "header_subtitle_text",
                        "label": "Sous-titre de l'en-tête",
                        "kind": "text",
                        "span": 2,
                        "placeholder": "Compte bancaire",
                        "rules": {"max": 30}
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
                {"id": "header_title", "label": "Titre", "master": False, "section": "header"},
                {"id": "header_subtitle", "label": "Sous-titre", "master": False, "section": "header"},
                {"id": "middle", "label": "Corps du document", "master": True, "section": "middle"},
                {"id": "middle_titulaire", "label": "Bloc titulaire", "master": False, "section": "middle"},
                {"id": "middle_bic", "label": "BIC", "master": False, "section": "middle"},
                {"id": "middle_iban", "label": "IBAN", "master": False, "section": "middle"},
                {"id": "middle_domiciliation", "label": "Bloc domiciliation", "master": False, "section": "middle"},
                {"id": "middle_table", "label": "Tableau RIB", "master": False, "section": "middle"},
                {"id": "middle_separator", "label": "Séparateur", "master": False, "section": "middle"},
                {"id": "footer", "label": "Pied de page", "master": True, "section": "footer"}
            ],
            "visible": {
                "header": True,
                "header_logo": True,
                "header_title": True,
                "header_subtitle": True,
                "middle": True,
                "middle_titulaire": True,
                "middle_bic": True,
                "middle_iban": True,
                "middle_domiciliation": True,
                "middle_table": True,
                "middle_separator": True,
                "footer": True
            }
        }
    }
