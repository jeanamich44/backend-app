def get_form_schema() -> dict:
    return {
        "version": 3,
        "defaults": {
            "cp": "75011",
            "nom": "Martin",
            "pays": "France",
            "items": [
                {
                    "qte": "1",
                    "sku": "80089081003",
                    "desc": "Cotton Pique Polo",
                    "prix": "80.00",
                    "desc2": "Polo Shirt",
                    "taille": "M",
                    "barcode": "5045556761666",
                    "couleur": "Noir"
                }
            ],
            "ville": "Paris",
            "prenom": "Lucas",
            "adresse": "12 Rue des Fleurs",
            "num_commande": "4845001",
            "payment_mode": "MasterCard *************6357",
            "retrait_magasin": True,
            "total": "80,00"
        },
        "metadata": {
            "logo": "/logos/burberry.png",
            "title": "GÉNÉRATEUR FACTURE BURBERRY",
            "apiBase": "/api/generate-docs/facture/burberry",
            "itemKey": "items",
            "backHref": "/services/generate-docs/facture",
            "category": "facture",
            "headerBg": "bg-white border-neutral-800/30",
            "maxItems": 2,
            "priceKey": "burberry",
            "subtitle": "Déclaration d'expédition Burberry",
            "backLabel": "Retour aux factures",
            "itemLabel": "4. Articles",
            "logoClass": "scale-100 md:scale-105",
            "generateLabel": "Générer la facture",
            "filenameTemplate": "Facture_Burberry.pdf"
        },
        "sections": [
            {
                "title": "1. Mode de livraison",
                "fields": [
                    {
                        "key": "retrait_magasin",
                        "kind": "checkbox",
                        "label": "Collect-in-store (Retrait en boutique)"
                    }
                ]
            },
            {
                "title": "2. Adresse client",
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
                "title": "3. Commande",
                "fields": [
                    {
                        "key": "num_commande",
                        "label": "N° de commande"
                    },
                    {
                        "key": "payment_mode",
                        "kind": "select",
                        "label": "Mode de paiement",
                        "options": [
                            {
                                "label": "MasterCard",
                                "value": "MasterCard"
                            },
                            {
                                "label": "Visa",
                                "value": "Visa"
                            },
                            {
                                "label": "American Express",
                                "value": "American Express"
                            },
                            {
                                "label": "PayPal",
                                "value": "PayPal"
                            },
                            {
                                "label": "Apple Pay",
                                "value": "Apple Pay"
                            },
                            {
                                "label": "Carte cadeau",
                                "value": "Carte cadeau"
                            },
                            {
                                "label": "Virement",
                                "value": "Virement"
                            }
                        ]
                    },
                    {
                        "key": "date_commande",
                        "kind": "date",
                        "label": "Date de la commande",
                        "dateFormat": "slash"
                    },
                    {
                        "key": "date_expedition",
                        "kind": "date",
                        "label": "Date d'expédition",
                        "dateFormat": "slash"
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
                        "span": 2,
                        "placeholder": "80,00"
                    }
                ]
            }
        ],
        "itemBlank": {
            "qte": "1",
            "sku": "",
            "desc": "",
            "prix": "0.00",
            "desc2": "",
            "taille": "",
            "barcode": "",
            "couleur": ""
        },
        "itemColumns": [
            {
                "key": "desc",
                "label": "Description"
            },
            {
                "key": "desc2",
                "label": "Sous-titre"
            },
            {
                "key": "taille",
                "label": "Taille"
            },
            {
                "key": "couleur",
                "label": "Couleur"
            },
            {
                "key": "qte",
                "label": "Quantité"
            },
            {
                "key": "prix",
                "label": "Prix"
            },
            {
                "key": "sku",
                "label": "N° d'article (SKU)",
                "placeholder": "80089081003"
            },
            {
                "key": "barcode",
                "label": "Code-barres",
                "placeholder": "5045556761666"
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
                    "label": "Logo Burberry",
                    "section": "header"
                },
                {
                    "id": "header_title",
                    "label": "Titre Déclaration d'expédition",
                    "section": "header"
                },
                {
                    "id": "header_service",
                    "label": "Service Client",
                    "section": "header"
                },
                {
                    "id": "header_order",
                    "label": "Références & Dates commande",
                    "section": "header"
                },
                {
                    "id": "header_addresses",
                    "label": "Blocs adresses (expédition & facturation)",
                    "section": "header"
                },
                {
                    "id": "middle",
                    "label": "Corps de facture complet",
                    "master": True,
                    "section": "middle"
                },
                {
                    "id": "middle_columns",
                    "label": "En-tête des colonnes",
                    "section": "middle"
                },
                {
                    "id": "middle_rows",
                    "label": "Lignes d'articles",
                    "section": "middle"
                },
                {
                    "id": "middle_totals",
                    "label": "Total de la commande",
                    "section": "middle"
                },
                {
                    "id": "footer",
                    "label": "Pied de page complet",
                    "master": True,
                    "section": "footer"
                },
                {
                    "id": "footer_line",
                    "label": "Ligne de séparation supérieure",
                    "section": "footer"
                },
                {
                    "id": "footer_payment",
                    "label": "Méthode de paiement",
                    "section": "footer"
                },
                {
                    "id": "footer_notice",
                    "label": "Informations de livraison",
                    "section": "footer"
                },
                {
                    "id": "footer_legal",
                    "label": "Mentions légales",
                    "section": "footer"
                }
            ],
            "visible": {
                "footer": True,
                "header": True,
                "middle": True,
                "footer_line": True,
                "header_logo": True,
                "middle_rows": True,
                "footer_legal": True,
                "header_order": True,
                "header_title": True,
                "footer_notice": True,
                "middle_totals": True,
                "footer_payment": True,
                "header_service": True,
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
        }
    }
