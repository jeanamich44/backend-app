def get_form_schema() -> dict:
    return {
        "defaults": {
            "cp": "75011",
            "nom": "Martin",
            "pays": "FRANCE",
            "port": "0,00",
            "items": [
                {
                    "pu": "199,99",
                    "qte": "1",
                    "sku": "DF-1001",
                    "tva": "20.00",
                    "desc": "Casque Intégral Moto Noir Mat",
                    "taille": "L",
                    "couleur": "Noir"
                }
            ],
            "ville": "Paris",
            "prenom": "Lucas",
            "remise": "0,00",
            "adresse": "12 Rue des Fleurs",
            "payment": "Carte Bancaire",
            "num_client": "378062",
            "magasin_nom": "DAFY MOTO PARIS",
            "num_facture": "71266024",
            "date_facture": "09/09/2026",
            "livraison_cp": "75011",
            "num_commande": "2350151",
            "date_commande": "09/09/2026",
            "livraison_nom": "Martin",
            "livraison_mode": "chronopost",
            "livraison_pays": "FRANCE",
            "livraison_extra": "",
            "livraison_ville": "Paris",
            "livraison_prenom": "Lucas",
            "livraison_adresse": "12 Rue des Fleurs",
            "total": "239,99"
        },
        "metadata": {
            "logo": "/logos/dafy.png",
            "title": "GÉNÉRATEUR FACTURE DAFY MOTO",
            "apiBase": "/api/generate-docs/facture/dafy",
            "itemKey": "items",
            "backHref": "/services/generate-docs/facture",
            "category": "facture",
            "headerBg": "bg-white border-red-500/30",
            "maxItems": 2,
            "priceKey": "dafy",
            "subtitle": "Document PDF Dafy Moto officiel",
            "backLabel": "Retour aux factures",
            "itemBlank": {
                "pu": "0,00",
                "qte": "1",
                "sku": "",
                "tva": "20.00",
                "desc": "",
                "taille": "",
                "couleur": ""
            },
            "itemLabel": "4. Articles",
            "logoClass": "scale-120 md:scale-130",
            "generateLabel": "Générer la facture",
            "filenameTemplate": "Facture_Dafy_Moto.pdf"
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
                    },
                    {
                        "key": "livraison_mode",
                        "kind": "select",
                        "label": "Mode de livraison",
                        "options": [
                            {
                                "label": "Point de retrait Chronopost",
                                "value": "chronopost"
                            },
                            {
                                "label": "Chronopost à domicile",
                                "value": "domicile"
                            },
                            {
                                "label": "Retrait en Magasin",
                                "value": "magasin"
                            }
                        ]
                    },
                    {
                        "key": "livraison_extra",
                        "label": "Complément adresse",
                        "advanced": True
                    }
                ]
            },
            {
                "title": "3. Références & Magasin",
                "fields": [
                    {
                        "key": "magasin_nom",
                        "label": "Magasin",
                        "advanced": True
                    },
                    {
                        "key": "num_client",
                        "label": "N° client"
                    },
                    {
                        "key": "num_commande",
                        "label": "N° commande"
                    },
                    {
                        "key": "num_facture",
                        "label": "N° facture"
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
                        "label": "Moyen de paiement"
                    }
                ]
            },
            {
                "title": "4. Totaux",
                "position": "after_items",
                "fields": [
                    {
                        "key": "remise",
                        "label": "Remise",
                        "advanced": True
                    },
                    {
                        "key": "port",
                        "label": "Frais de port",
                        "advanced": True
                    },
                    {
                        "key": "total",
                        "label": "Total TTC",
                        "placeholder": "239,99"
                    }
                ]
            }
        ],
        "itemBlank": {
            "pu": "0,00",
            "qte": "1",
            "sku": "",
            "tva": "20.00",
            "desc": "",
            "taille": "",
            "couleur": ""
        },
        "itemColumns": [
            {
                "key": "sku",
                "label": "Réf",
                "advanced": True
            },
            {
                "key": "desc",
                "label": "Désignation"
            },
            {
                "key": "couleur",
                "label": "Couleur"
            },
            {
                "key": "taille",
                "label": "Taille"
            },
            {
                "key": "qte",
                "label": "Qté"
            },
            {
                "key": "pu",
                "label": "Prix unitaire HT"
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
                    "id": "header_banner",
                    "label": "Bandeau contact supérieur",
                    "section": "header"
                },
                {
                    "id": "header_logo",
                    "label": "Logo Dafy Moto",
                    "section": "header"
                },
                {
                    "id": "header_title",
                    "label": "Titre FACTURE",
                    "section": "header"
                },
                {
                    "id": "header_issuer",
                    "label": "Coordonnées Dafy Moto",
                    "section": "header"
                },
                {
                    "id": "header_refs",
                    "label": "Références & Dates commande",
                    "section": "header"
                },
                {
                    "id": "header_addresses",
                    "label": "Adresses Facturation & Livraison",
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
                    "label": "Totaux, Port & TVA",
                    "section": "middle"
                },
                {
                    "id": "footer",
                    "label": "Pied de page complet",
                    "master": True,
                    "section": "footer"
                },
                {
                    "id": "footer_thanks",
                    "label": "Message de remerciement",
                    "section": "footer"
                },
                {
                    "id": "footer_line",
                    "label": "Filet inférieur",
                    "section": "footer"
                },
                {
                    "id": "footer_legal",
                    "label": "Mentions légales Dafy",
                    "section": "footer"
                }
            ],
            "visible": {
                "footer": True,
                "header": True,
                "middle": True,
                "footer_line": True,
                "header_logo": True,
                "header_refs": True,
                "middle_rows": True,
                "footer_legal": True,
                "header_title": True,
                "footer_thanks": True,
                "header_banner": True,
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
        }
    }
