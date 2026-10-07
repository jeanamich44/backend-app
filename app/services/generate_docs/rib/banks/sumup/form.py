from . import copy

def get_form_schema() -> dict:
    return {
        "metadata": {
            "title": "GÉNÉRATEUR ACCOUNT DETAILS SUMUP",
            "logo": "sumup",
            "apiBase": "/api/generate-docs/rib/sumup",
            "headerBg": "bg-gradient-to-br from-slate-900/60 to-cyan-950/40 border-cyan-500/30",
            "priceKey": "sumup",
            "subtitle": "Document PDF SumUp officiel",
            "filenameTemplate": f"Account_Details_SumUp_{copy.NOM}.pdf"
        },
        "defaults": {
            "date_document": copy.DATE,
            "heure_document": "00:29",
            "nom": copy.NOM,
            "prenom": copy.PRENOM,
            "adresse": copy.TITULAIRE_ADRESSE,
            "cp": "75011",
            "ville": "Paris",
            "pays": copy.TITULAIRE_PAYS,
            "date_ouverture": copy.DATE_OUVERTURE,
            "institution": copy.INSTITUTION,
            "iban": copy.IBAN,
            "bic": copy.BIC,
            "header": "true",
            "header_logo": "true",
            "header_title": "true",
            "header_date": "true",
            "middle": "true",
            "middle_holder": "true",
            "middle_account": "true",
            "middle_notice": "true",
            "footer": "true",
            "footer_legal": "true",
            "footer_legal_right": "true",
            "header_title_text": copy.TITLE,
            "middle_notice_text": copy.NOTICE,
            "footer_legal_text": copy.FOOTER_LEFT,
            "footer_legal_right_text": copy.FOOTER_RIGHT
        },
        "sections": [
            {
                "id": "titulaire_section",
                "title": "Titulaire du compte",
                "order": 1,
                "fields": [
                    {
                        "key": "date_document",
                        "label": "Date du document",
                        "kind": "date",
                        "span": 1,
                        "placeholder": "08 Aug 2026",
                        "rules": {"required": False, "max": 20}
                    },
                    {
                        "key": "heure_document",
                        "label": "Heure du document",
                        "kind": "time",
                        "span": 1,
                        "placeholder": "00:29",
                        "rules": {"required": False, "max": 10}
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
                        "rules": {"required": True, "min": 5, "max": 60}
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
                        "placeholder": "EX: Paris",
                        "rules": {"required": True, "min": 2, "max": 45}
                    },
                    {
                        "key": "pays",
                        "label": "Pays",
                        "kind": "text",
                        "span": 2,
                        "placeholder": "France",
                        "rules": {"required": False, "min": 2, "max": 45}
                    }
                ]
            },
            {
                "id": "compte_section",
                "title": "Détails du compte",
                "order": 2,
                "fields": [
                    {
                        "key": "date_ouverture",
                        "label": "Date d'ouverture",
                        "kind": "date",
                        "span": 1,
                        "placeholder": "06 Mar 2026",
                        "rules": {"required": False, "max": 20}
                    },
                    {
                        "key": "institution",
                        "label": "Institution",
                        "kind": "text",
                        "span": 1,
                        "placeholder": "SumUp Limited",
                        "rules": {"required": True, "min": 2, "max": 40}
                    },
                    {
                        "key": "iban",
                        "label": "IBAN",
                        "kind": "iban",
                        "span": 2,
                        "placeholder": "IE10SUMU00000112350000",
                        "rules": {"required": True, "min": 15, "max": 34, "transform": "uppercase"}
                    },
                    {
                        "key": "bic",
                        "label": "BIC / SWIFT",
                        "kind": "bic",
                        "span": 2,
                        "placeholder": "SUMUIE22XXX",
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
                        "placeholder": "Account details statement",
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
                        "placeholder": "Give this statement...",
                        "rules": {"max": 400}
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
                        "label": "Mentions légales gauche",
                        "kind": "textarea",
                        "span": 2,
                        "placeholder": "SumUp Limited...",
                        "rules": {"max": 300}
                    },
                    {
                        "key": "footer_legal_right_text",
                        "label": "Mentions légales droite",
                        "kind": "textarea",
                        "span": 2,
                        "placeholder": "is regulated by...",
                        "rules": {"max": 300}
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
                {"id": "header_date", "label": "Date document", "master": False, "section": "header"},
                {"id": "middle", "label": "Corps du document", "master": True, "section": "middle"},
                {"id": "middle_holder", "label": "Bloc titulaire", "master": False, "section": "middle"},
                {"id": "middle_account", "label": "Bloc compte", "master": False, "section": "middle"},
                {"id": "middle_notice", "label": "Notice", "master": False, "section": "middle"},
                {"id": "footer", "label": "Pied de page", "master": True, "section": "footer"},
                {"id": "footer_legal", "label": "Mentions légales gauche", "master": False, "section": "footer"},
                {"id": "footer_legal_right", "label": "Mentions légales droite", "master": False, "section": "footer"}
            ],
            "visible": {
                "header": True,
                "header_logo": True,
                "header_title": True,
                "header_date": True,
                "middle": True,
                "middle_holder": True,
                "middle_account": True,
                "middle_notice": True,
                "footer": True,
                "footer_legal": True,
                "footer_legal_right": True
            }
        }
    }
