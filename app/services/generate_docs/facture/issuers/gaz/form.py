def get_form_schema() -> dict:
    return {
        "version": 2,
        "defaults": {
            "civilite": "M.",
            "nom": "Martin",
            "prenom": "Lucas",
            "adresse": "12 Rue des Fleurs",
            "cp": "75011",
            "ville": "Paris",
            "num_facture": "535006482817",
            "date_facture": "09/09/26",
            "num_client": "319375842",
            "num_contrat": "525866248",
            "lieu_pce": "1GHE*FD 48",
            "lieu_bat": "BAT A 1ET",
            "compte": "20041000014763925L0XXXX.",
            "montant_gaz": "46,20",
            "montant_prestations": "21,50",
            "total": "67,70",
            "montant_ht": "61,55",
            "montant_tva": "6,15"
        },
        "metadata": {
            "logo": "/logos/gaz.svg",
            "title": "GÉNÉRATEUR FACTURE GAZ (ENGIE)",
            "apiBase": "/api/generate-docs/facture/gaz",
            "backHref": "/services/generate-docs/facture",
            "category": "facture",
            "headerBg": "bg-white border-blue-500/30",
            "priceKey": "gaz",
            "subtitle": "Facture de souscription gaz Engie officielle",
            "backLabel": "Retour aux factures",
            "logoClass": "scale-115 md:scale-125",
            "generateLabel": "Générer la facture",
            "filenameTemplate": "Facture_Gaz.pdf"
        },
        "sections": [
            {
                "title": "1. Titulaire & Adresse",
                "fields": [
                    {
                        "key": "civilite",
                        "label": "Civilité",
                        "kind": "select",
                        "options": [
                            {"value": "MME", "label": "MME"},
                            {"value": "M.", "label": "M."},
                            {"value": "__CUSTOM__", "label": "Personnalisé"}
                        ]
                    },
                    {
                        "key": "nom",
                        "label": "Nom"
                    },
                    {
                        "key": "prenom",
                        "label": "Prénom"
                    },
                    {
                        "key": "adresse",
                        "label": "Adresse"
                    },
                    {
                        "key": "cp",
                        "label": "Code postal"
                    },
                    {
                        "key": "ville",
                        "label": "Ville"
                    }
                ]
            },
            {
                "title": "2. Références Contrat & Compteur",
                "fields": [
                    {
                        "key": "num_facture",
                        "label": "N° de facture"
                    },
                    {
                        "key": "date_facture",
                        "kind": "date",
                        "label": "Date de facture",
                        "dateFormat": "slash"
                    },
                    {
                        "key": "num_client",
                        "label": "Référence client"
                    },
                    {
                        "key": "num_contrat",
                        "label": "N° compte de contrat"
                    },
                    {
                        "key": "lieu_pce",
                        "label": "Lieu de consommation (PCE)"
                    },
                    {
                        "key": "lieu_bat",
                        "label": "Complément lieu / Bâtiment",
                        "advanced": True
                    },
                    {
                        "key": "compte",
                        "label": "N° de compte bancaire",
                        "advanced": True
                    }
                ]
            },
            {
                "title": "3. Montants & Taxes",
                "fields": [
                    {
                        "key": "montant_gaz",
                        "label": "Montant gaz (€)"
                    },
                    {
                        "key": "montant_prestations",
                        "label": "Montant prestations (€)"
                    },
                    {
                        "key": "total",
                        "label": "Total TTC (€)"
                    },
                    {
                        "key": "montant_ht",
                        "label": "Montant total HT (€)",
                        "advanced": True
                    },
                    {
                        "key": "montant_tva",
                        "label": "Montant TVA (€)",
                        "advanced": True
                    }
                ]
            }
        ],
        "customLayout": {
            "blocks": [
                {
                    "id": "header",
                    "label": "En-tête complet",
                    "master": True,
                    "section": "header"
                },
                {
                    "id": "header_logo",
                    "label": "Logo Engie",
                    "section": "header"
                },
                {
                    "id": "header_title",
                    "label": "Bandeau titre & Références",
                    "section": "header"
                },
                {
                    "id": "header_refs",
                    "label": "Références client & Contrat",
                    "section": "header"
                },
                {
                    "id": "header_lieu",
                    "label": "Lieu de consommation (PCE)",
                    "section": "header"
                },
                {
                    "id": "header_window",
                    "label": "Fenêtre titulaire & Adresse",
                    "section": "header"
                },
                {
                    "id": "header_barcode",
                    "label": "Code-barres",
                    "section": "header"
                },
                {
                    "id": "header_correspond",
                    "label": "Coordonnées de correspondance",
                    "section": "header"
                },
                {
                    "id": "middle",
                    "label": "Corps de facture complet",
                    "master": True,
                    "section": "middle"
                },
                {
                    "id": "middle_legal",
                    "label": "Mentions légales",
                    "section": "middle"
                },
                {
                    "id": "middle_amounts",
                    "label": "Détail montants, taxes & Total",
                    "section": "middle"
                },
                {
                    "id": "middle_next",
                    "label": "Encadré prochaine facture",
                    "section": "middle"
                },
                {
                    "id": "middle_paiement",
                    "label": "Moyen de paiement & Compte",
                    "section": "middle"
                },
                {
                    "id": "footer",
                    "label": "Pied de page complet",
                    "master": True,
                    "section": "footer"
                },
                {
                    "id": "footer_contacts",
                    "label": "Contacts & Urgences",
                    "section": "footer"
                },
                {
                    "id": "footer_economies",
                    "label": "Conseils économies d'énergie",
                    "section": "footer"
                },
                {
                    "id": "footer_cheque",
                    "label": "Chèque énergie",
                    "section": "footer"
                },
                {
                    "id": "footer_triman",
                    "label": "Logo Triman / Tri",
                    "section": "footer"
                }
            ],
            "visible": {
                "footer": True,
                "header": True,
                "middle": True,
                "header_lieu": True,
                "header_logo": True,
                "header_refs": True,
                "middle_next": True,
                "header_title": True,
                "middle_legal": True,
                "footer_cheque": True,
                "footer_triman": True,
                "header_window": True,
                "header_barcode": True,
                "middle_amounts": True,
                "footer_contacts": True,
                "middle_paiement": True,
                "footer_economies": True,
                "header_correspond": True
            },
            "sections": [
                {
                    "id": "header",
                    "label": "En-tête"
                },
                {
                    "id": "middle",
                    "label": "Corps de facture"
                },
                {
                    "id": "footer",
                    "label": "Pied de page"
                }
            ]
        }
    }
