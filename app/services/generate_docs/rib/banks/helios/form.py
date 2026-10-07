from . import copy

def get_form_schema() -> dict:
    return {
        "metadata": {
            "title": "GÉNÉRATEUR RIB HELIOS",
            "logo": "helios",
            "apiBase": "/api/generate-docs/rib/helios",
            "headerBg": "bg-gradient-to-br from-cyan-900/40 to-slate-950/80 border-cyan-500/30",
            "priceKey": "helios",
            "subtitle": "Document PDF Helios officiel",
            "filenameTemplate": f"RIB_Helios_{copy.NOM}.pdf"
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
            "middle": "true",
            "middle_notice": "true",
            "middle_titulaire": "true",
            "middle_iban": "true",
            "middle_bic": "true",
            "middle_domiciliation": "true",
            "middle_table": "true",
            "middle_notes": "true",
            "middle_lines": "true",
            "footer": "true",
            "footer_legal": "true",
            "header_title_text": copy.TITLE,
            "middle_notice_text": copy.NOTICE,
            "middle_domiciliation_text": copy.DOMICILIATION,
            "footer_legal_text": copy.LEGAL
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
                            {"label": "Mr", "value": "Mr"},
                            {"label": "Mme", "value": "Mme"},
                            {"label": "Mlle", "value": "Mlle"}
                        ],
                        "rules": {"required": True}
                    },
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
                "title": "Coordonnées Bancaires",
                "order": 2,
                "fields": [
                    {
                        "key": "code_banque",
                        "label": "Code Banque",
                        "kind": "digits",
                        "span": 1,
                        "autoIban": "banque",
                        "placeholder": "17448",
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
                        "placeholder": "00012345678",
                        "rules": {"required": True, "min": 11, "max": 11, "transform": "uppercase"}
                    },
                    {
                        "key": "cle",
                        "label": "Clé RIB",
                        "kind": "digits",
                        "span": 1,
                        "autoIban": "cle",
                        "placeholder": "74",
                        "rules": {"required": True, "min": 2, "max": 2, "transform": "digits_only"}
                    },
                    {
                        "key": "iban",
                        "label": "IBAN",
                        "kind": "iban",
                        "span": 2,
                        "placeholder": "FR76 1744 8000 0100 0123 4567 874",
                        "rules": {"required": True, "min": 27, "max": 34, "transform": "uppercase"}
                    },
                    {
                        "key": "bic",
                        "label": "BIC / SWIFT",
                        "kind": "bic",
                        "span": 2,
                        "placeholder": "SFPEFRP2XXX",
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
                        "placeholder": "RELEVÉ D’IDENTITÉ BANCAIRE",
                        "rules": {"max": 40}
                    }
                ]
            },
            {
                "id": "middle_section",
                "title": "Corps",
                "order": 4,
                "hasAdvancedMode": True,
                "fields": [
                    {
                        "key": "middle_notice_text",
                        "label": "Notice explicative",
                        "kind": "textarea",
                        "span": 2,
                        "placeholder": "Ce relevé est destiné à tout organisme...",
                        "rules": {"max": 400}
                    },
                    {
                        "key": "middle_domiciliation_text",
                        "label": "Domiciliation",
                        "kind": "text",
                        "span": 2,
                        "placeholder": "Okali, 50 rue La Boétie, 75008 Paris",
                        "rules": {"max": 80}
                    }
                ]
            },
            {
                "id": "footer_section",
                "title": "Pied de page",
                "order": 5,
                "hasAdvancedMode": True,
                "fields": [
                    {
                        "key": "footer_legal_text",
                        "label": "Mentions légales",
                        "kind": "textarea",
                        "span": 2,
                        "placeholder": "HELIOS SAS...",
                        "rules": {"max": 800}
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
                {"id": "middle", "label": "Corps du document", "master": True, "section": "middle"},
                {"id": "middle_notice", "label": "Notice", "master": False, "section": "middle"},
                {"id": "middle_titulaire", "label": "Bloc titulaire", "master": False, "section": "middle"},
                {"id": "middle_iban", "label": "IBAN", "master": False, "section": "middle"},
                {"id": "middle_bic", "label": "BIC", "master": False, "section": "middle"},
                {"id": "middle_domiciliation", "label": "Bloc domiciliation", "master": False, "section": "middle"},
                {"id": "middle_table", "label": "Tableau RIB", "master": False, "section": "middle"},
                {"id": "middle_notes", "label": "Notes", "master": False, "section": "middle"},
                {"id": "middle_lines", "label": "Filets / lignes", "master": False, "section": "middle"},
                {"id": "footer", "label": "Pied de page", "master": True, "section": "footer"},
                {"id": "footer_legal", "label": "Mentions légales", "master": False, "section": "footer"}
            ],
            "visible": {
                "header": True,
                "header_logo": True,
                "header_title": True,
                "middle": True,
                "middle_notice": True,
                "middle_titulaire": True,
                "middle_iban": True,
                "middle_bic": True,
                "middle_domiciliation": True,
                "middle_table": True,
                "middle_notes": True,
                "middle_lines": True,
                "footer": True,
                "footer_legal": True
            }
        }
    }
