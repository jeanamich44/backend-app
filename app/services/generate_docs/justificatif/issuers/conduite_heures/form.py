from . import copy

# ----------------------------------------------------------------------


def get_form_schema() -> dict:
    return {
        "metadata": {
            "title": "GÉNÉRATEUR HEURES DE CONDUITE",
            "subtitle": "Liste des rendez-vous au format PDF",
            "logo": "/logos/cfrvitry.png",
            "headerBg": "bg-white border-sky-500/30",
            "priceKey": "conduite_heures",
            "apiBase": "/api/generate-docs/justificatif/conduite_heures",
            "filenameTemplate": "Justificatif_Heures_Conduite.pdf",
            "generateLabel": "Générer le justificatif",
            "backHref": "/services/generate-docs/justificatif",
            "backLabel": "Retour aux justificatifs"
        },
        "defaults": {
            "nom": copy.NOM,
            "prenom": copy.PRENOM,
            "num_eleve": copy.NUM_ELEVE,
            "edition_date": copy.EDITION_DATE,
            "edition_time": copy.EDITION_TIME,
            "rdvs": copy.DEFAULT_RDVS
        },
        "sections": [
            {
                "id": "eleve",
                "order": 1,
                "title": "1. Élève",
                "fields": [
                    {
                        "key": "nom",
                        "label": "Nom",
                        "kind": "text",
                        "span": 1,
                        "rules": {"min": 2, "max": 40, "required": True, "transform": "uppercase"},
                        "required": True,
                        "min": 2,
                        "max": 40,
                        "placeholder": "ex: Martin"
                    },
                    {
                        "key": "prenom",
                        "label": "Prénom",
                        "kind": "text",
                        "span": 1,
                        "rules": {"min": 2, "max": 40, "required": True, "transform": "uppercase"},
                        "required": True,
                        "min": 2,
                        "max": 40,
                        "placeholder": "ex: Lucas"
                    },
                    {
                        "key": "num_eleve",
                        "label": "N° élève",
                        "kind": "text",
                        "span": 2,
                        "rules": {"min": 2, "max": 20, "required": True},
                        "required": True,
                        "min": 2,
                        "max": 20,
                        "placeholder": "ex: 1001"
                    },
                    {
                        "key": "edition_date",
                        "label": "Date d'édition",
                        "kind": "date",
                        "span": 1,
                        "dateFormat": "slash",
                        "rules": {"required": True},
                        "required": True
                    },
                    {
                        "key": "edition_time",
                        "label": "Heure d'édition",
                        "kind": "time",
                        "span": 1,
                        "rules": {"required": True, "transform": "time"},
                        "required": True,
                        "placeholder": "ex: 22:13"
                    }
                ]
            }
        ],
        "itemsConfig": {
            "key": "rdvs",
            "label": "2. Rendez-vous",
            "enabled": True,
            "maxItems": 20,
            "blankItem": {
                "jour": "Lundi",
                "date": "",
                "debut": "13:00",
                "fin": "16:00",
                "activite": "LECON PLATEAU",
                "commentaire": ""
            },
            "columns": [
                {
                    "key": "jour",
                    "label": "Jour",
                    "kind": "select",
                    "required": True,
                    "options": [
                        {"label": "Lundi", "value": "Lundi"},
                        {"label": "Mardi", "value": "Mardi"},
                        {"label": "Mercredi", "value": "Mercredi"},
                        {"label": "Jeudi", "value": "Jeudi"},
                        {"label": "Vendredi", "value": "Vendredi"},
                        {"label": "Samedi", "value": "Samedi"},
                        {"label": "Dimanche", "value": "Dimanche"}
                    ]
                },
                {
                    "key": "date",
                    "label": "Date",
                    "kind": "date",
                    "required": True
                },
                {
                    "key": "debut",
                    "label": "Début",
                    "kind": "time",
                    "required": True,
                    "placeholder": "13:00"
                },
                {
                    "key": "fin",
                    "label": "Fin",
                    "kind": "time",
                    "required": True,
                    "placeholder": "16:00"
                },
                {
                    "key": "activite",
                    "label": "Activité",
                    "kind": "text",
                    "required": True
                },
                {
                    "key": "commentaire",
                    "label": "Commentaire",
                    "kind": "text",
                    "required": False,
                    "placeholder": "Optionnel"
                }
            ]
        },
        "customLayout": {
            "blocks": [
                {"id": "header", "label": "En-tête complet", "master": True, "section": "header"},
                {"id": "header_logo", "label": "Logo CFR Vitry", "master": False, "section": "header"},
                {"id": "header_identity", "label": "Nom et N° élève", "master": False, "section": "header"},
                {"id": "header_banner", "label": "Date et heure d'édition", "master": False, "section": "header"},
                {"id": "middle", "label": "Tableau complet des leçons (lignes & grille)", "master": True, "section": "middle"},
                {"id": "footer", "label": "Pied de page (coordonnées CFR Vitry & mentions légales)", "master": True, "section": "footer"}
            ],
            "visible": {
                "header": True,
                "header_logo": True,
                "header_identity": True,
                "header_banner": True,
                "middle": True,
                "footer": True
            },
            "sections": [
                {"id": "header", "label": "En-tête"},
                {"id": "middle", "label": "Tableau des rendez-vous"},
                {"id": "footer", "label": "Pied de page"}
            ]
        }
    }
