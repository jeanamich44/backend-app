def get_form_schema() -> dict:
    return {
        "defaults": {
            "cp": "75011",
            "nom": "Martin",
            "pays": "France",
            "items": [
                {
                    "ht": "399,00",
                    "qte": "1",
                    "sku": "DAR-1001",
                    "tva": "20,00",
                    "desc": "Téléviseur LED 4K Ultra HD",
                    "desc2": "Garantie 2 ans incluse",
                    "date_delivrance": "09/09/2026"
                }
            ],
            "ville": "Paris",
            "prenom": "Lucas",
            "adresse": "12 Rue des Fleurs",
            "payment": "Carte Bancaire",
            "date_facture": "09/09/2026",
            "livraison_cp": "75011",
            "num_commande": "DAR-100110",
            "date_commande": "09/09/2026",
            "livraison_nom": "Martin",
            "livraison_pays": "France",
            "livraison_ville": "Paris",
            "livraison_prenom": "Lucas",
            "livraison_adresse": "12 Rue des Fleurs",
            "total": "478,80"
        },
        "metadata": {
            "logo": "/logos/darty.svg",
            "title": "GÉNÉRATEUR FACTURE DARTY",
            "apiBase": "/api/generate-docs/facture/darty",
            "itemKey": "items",
            "backHref": "/services/generate-docs/facture",
            "category": "facture",
            "headerBg": "bg-white border-red-500/30",
            "maxItems": 3,
            "priceKey": "darty",
            "subtitle": "Document PDF Darty officiel",
            "backLabel": "Retour aux factures",
            "itemBlank": {
                "ht": "0,00",
                "qte": "1",
                "sku": "DAR-1001",
                "tva": "20,00",
                "desc": "",
                "desc2": "",
                "date_delivrance": ""
            },
            "itemLabel": "4. Articles",
            "logoClass": "scale-110 md:scale-120",
            "generateLabel": "Générer la facture",
            "filenameTemplate": "Facture_Darty.pdf"
        },
        "sections": [
            {
                "title": "1. Facturation",
                "fields": [
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
                    },
                    {
                        "key": "pays",
                        "label": "Pays",
                        "advanced": True
                    }
                ]
            },
            {
                "title": "2. Livraison",
                "fields": [
                    {
                        "key": "livraison_nom",
                        "label": "Nom"
                    },
                    {
                        "key": "livraison_prenom",
                        "label": "Prénom"
                    },
                    {
                        "key": "livraison_adresse",
                        "label": "Adresse"
                    },
                    {
                        "key": "livraison_cp",
                        "label": "Code postal"
                    },
                    {
                        "key": "livraison_ville",
                        "label": "Ville"
                    },
                    {
                        "key": "livraison_pays",
                        "label": "Pays",
                        "advanced": True
                    }
                ]
            },
            {
                "title": "3. Commande & Règlement",
                "fields": [
                    {
                        "key": "num_commande",
                        "label": "N° commande"
                    },
                    {
                        "key": "date_commande",
                        "kind": "date",
                        "label": "Date commande",
                        "dateFormat": "slash"
                    },
                    {
                        "key": "date_facture",
                        "kind": "date",
                        "label": "Date facture",
                        "dateFormat": "slash"
                    },
                    {
                        "key": "payment",
                        "label": "Mode de règlement"
                    }
                ]
            },
            {
                "title": "4. Totaux",
                "position": "after_items",
                "fields": [
                    {
                        "key": "total",
                        "label": "Total TTC",
                        "placeholder": "478,80"
                    }
                ]
            }
        ],
        "itemColumns": [
            {
                "key": "desc",
                "label": "Désignation"
            },
            {
                "key": "desc2",
                "label": "Complément"
            },
            {
                "key": "qte",
                "label": "Qté"
            },
            {
                "key": "ht",
                "label": "Montant HT"
            },
            {
                "key": "sku",
                "label": "Réf",
                "advanced": True
            },
            {
                "key": "tva",
                "label": "TVA %",
                "advanced": True
            },
            {
                "key": "date_delivrance",
                "kind": "date",
                "label": "Date délivrance",
                "advanced": True,
                "dateFormat": "slash"
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
                    "label": "Logo Darty",
                    "section": "header"
                },
                {
                    "id": "header_issuer",
                    "label": "Coordonnées Darty & Siège",
                    "section": "header"
                },
                {
                    "id": "header_addresses",
                    "label": "Adresses Facturation & Livraison",
                    "section": "header"
                },
                {
                    "id": "header_title",
                    "label": "Titre FACTURE",
                    "section": "header"
                },
                {
                    "id": "middle",
                    "label": "Corps de facture complet",
                    "master": True,
                    "section": "middle"
                },
                {
                    "id": "middle_order",
                    "label": "Bloc N° commande & Dates",
                    "section": "middle"
                },
                {
                    "id": "middle_columns",
                    "label": "Colonnes des articles",
                    "section": "middle"
                },
                {
                    "id": "middle_rows",
                    "label": "Lignes des articles",
                    "section": "middle"
                },
                {
                    "id": "middle_totals",
                    "label": "Totaux HT, TVA & TTC",
                    "section": "middle"
                },
                {
                    "id": "footer",
                    "label": "Pied de page complet",
                    "master": True,
                    "section": "footer"
                },
                {
                    "id": "footer_page",
                    "label": "Numérotation de page",
                    "section": "footer"
                },
                {
                    "id": "footer_legal",
                    "label": "Mentions légales Darty",
                    "section": "footer"
                }
            ],
            "visible": {
                "footer": True,
                "header": True,
                "middle": True,
                "footer_page": True,
                "header_logo": True,
                "middle_rows": True,
                "footer_legal": True,
                "header_title": True,
                "middle_order": True,
                "header_issuer": True,
                "middle_totals": True,
                "middle_columns": True,
                "header_addresses": True
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
        },
        "itemBlank": {
            "ht": "0,00",
            "qte": "1",
            "sku": "DAR-1001",
            "tva": "20,00",
            "desc": "",
            "desc2": "",
            "date_delivrance": ""
        }
    }
