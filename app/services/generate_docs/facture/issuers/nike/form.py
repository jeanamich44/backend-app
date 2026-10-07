def get_form_schema() -> dict:
    return {
        "version": 4,
        "defaults": {
            "cp": "75011",
            "nom": "Martin",
            "vat": "VAT Reg. No:FR81405395518",
            "pays": "FR",
            "items": [
                {
                    "qte": "1.00",
                    "sku": "FB7921",
                    "tva": "20",
                    "brut": "119,99",
                    "desc": "Sweat à capuche et zip Nike\nSportswear Tech Fleece Windrunner\npour homme",
                    "remise": "0,00"
                },
                {
                    "qte": "1.00",
                    "sku": "FB8002",
                    "tva": "20",
                    "brut": "99,99",
                    "desc": "Pantalon de jogging Nike Sportswear\nTech Fleece pour homme",
                    "remise": "0,00"
                }
            ],
            "ville": "Paris",
            "prenom": "Lucas",
            "seller": "NIKE Retail B.V.,65-67 avenue des Champs-Elysees, Paris, 75008, France",
            "adresse": "12 Rue des Fleurs",
            "payment": "Carte de Crédit",
            "cp_ville": "75011 Paris",
            "num_facture": "FR1024736093",
            "livraison_cp": "75011",
            "num_commande": "C01402544289",
            "livraison_pays": "FR",
            "livraison_ville": "PARIS",
            "livraison_adresse": "12 RUE DES FLEURS",
            "livraison_cp_ville": "75011 PARIS",
            "total": "219,98"
        },
        "metadata": {
            "logo": "/logos/nike.svg",
            "title": "GÉNÉRATEUR FACTURE NIKE",
            "apiBase": "/api/generate-docs/facture/nike",
            "itemKey": "items",
            "backHref": "/services/generate-docs/facture",
            "category": "facture",
            "headerBg": "bg-white border-orange-500/30",
            "maxItems": 5,
            "priceKey": "nike",
            "subtitle": "Document PDF Nike officiel",
            "backLabel": "Retour aux factures",
            "itemLabel": "4. Articles",
            "generateLabel": "Générer la facture",
            "filenameTemplate": "Facture_Nike.pdf"
        },
        "sections": [
            {
                "title": "1. Adresse de facturation",
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
                        "kind": "country",
                        "label": "Pays",
                        "advanced": True
                    }
                ]
            },
            {
                "title": "2. Adresse de livraison",
                "fields": [
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
                        "kind": "country",
                        "label": "Pays",
                        "advanced": True
                    }
                ]
            },
            {
                "title": "3. Références",
                "fields": [
                    {
                        "key": "num_commande",
                        "label": "N° de commande"
                    },
                    {
                        "key": "num_facture",
                        "label": "N° de facture"
                    },
                    {
                        "key": "date_facture",
                        "kind": "date",
                        "label": "Date de la facture",
                        "dateFormat": "slash"
                    },
                    {
                        "key": "payment",
                        "kind": "select",
                        "label": "Mode de paiement",
                        "options": [
                            {
                                "label": "Carte de Crédit",
                                "value": "Carte de Crédit"
                            },
                            {
                                "label": "Carte Bancaire",
                                "value": "Carte Bancaire"
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
                                "label": "Carte Cadeau",
                                "value": "Carte Cadeau"
                            }
                        ]
                    },
                    {
                        "key": "date_envoi",
                        "kind": "date",
                        "label": "Date d'envoi",
                        "advanced": True,
                        "dateFormat": "slash"
                    },
                    {
                        "key": "date_echeance",
                        "kind": "date",
                        "label": "Date d'échéance",
                        "advanced": True,
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
                        "placeholder": "219,98"
                    }
                ]
            }
        ],
        "itemBlank": {
            "qte": "1.00",
            "sku": "",
            "tva": "20",
            "brut": "0,00",
            "desc": "",
            "remise": "0,00"
        },
        "itemColumns": [
            {
                "key": "desc",
                "label": "Description"
            },
            {
                "key": "sku",
                "label": "N° de produit (SKU)"
            },
            {
                "key": "qte",
                "label": "Quantité"
            },
            {
                "key": "brut",
                "label": "Prix TTC"
            },
            {
                "key": "remise",
                "label": "Remise",
                "advanced": True
            },
            {
                "key": "tva",
                "label": "TVA %",
                "advanced": True
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
                    "label": "Logo Nike",
                    "section": "header"
                },
                {
                    "id": "header_brand",
                    "label": "Marque & Coordonnées",
                    "section": "header"
                },
                {
                    "id": "header_refs",
                    "label": "Références commande & facture",
                    "section": "header"
                },
                {
                    "id": "header_addresses",
                    "label": "Blocs adresses",
                    "section": "header"
                },
                {
                    "id": "header_title",
                    "label": "Titre Facture",
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
                    "label": "Boîte des totaux & TVA",
                    "section": "middle"
                },
                {
                    "id": "footer",
                    "label": "Pied de page complet",
                    "master": True,
                    "section": "footer"
                },
                {
                    "id": "footer_seller",
                    "label": "Coordonnées vendeur",
                    "section": "footer"
                },
                {
                    "id": "footer_notice",
                    "label": "Mentions légales & retour",
                    "section": "footer"
                },
                {
                    "id": "footer_page",
                    "label": "Numérotation de page",
                    "section": "footer"
                }
            ],
            "visible": {
                "footer": True,
                "header": True,
                "middle": True,
                "footer_page": True,
                "header_logo": True,
                "header_refs": True,
                "middle_rows": True,
                "header_brand": True,
                "header_title": True,
                "footer_notice": True,
                "footer_seller": True,
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
        }
    }
