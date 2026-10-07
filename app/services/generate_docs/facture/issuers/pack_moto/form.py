def get_form_schema() -> dict:
    return {
        "defaults": {
            "cp": "75011",
            "nom": "Martin",
            "pays": "France",
            "frais": "0.00",
            "items": [
                {
                    "pu": "79,90",
                    "qte": "1",
                    "sku": "8009578142",
                    "tva": "20.00",
                    "desc": "Gants Moto Cuir Renforcé Homme"
                }
            ],
            "ville": "Paris",
            "prenom": "Lucas",
            "adresse": "12 Rue des Fleurs",
            "payment": "Carte Bancaire",
            "num_facture": "#FA044682",
            "date_facture": "09/09/2026",
            "livraison_cp": "75011",
            "num_commande": "TSKNTPLVH",
            "transporteur": "Colissimo Domicile",
            "date_commande": "09/09/2026",
            "livraison_nom": "Martin",
            "livraison_pays": "France",
            "livraison_ville": "Paris",
            "livraison_prenom": "Lucas",
            "livraison_adresse": "12 Rue des Fleurs",
            "livraison_societe": "",
            "total": "95,88"
        },
        "metadata": {
            "logo": "/logos/pack_moto.png",
            "title": "GÉNÉRATEUR FACTURE PACK MOTO",
            "apiBase": "/api/generate-docs/facture/pack_moto",
            "itemKey": "items",
            "backHref": "/services/generate-docs/facture",
            "headerBg": "bg-white border-orange-500/30",
            "maxItems": 6,
            "priceKey": "pack_moto",
            "subtitle": "Document PDF Pack Moto officiel",
            "backLabel": "Retour aux factures",
            "itemLabel": "4. Articles",
            "logoClass": "scale-120 md:scale-130",
            "generateLabel": "Générer la facture",
            "filenameTemplate": "Facture_Pack_Moto.pdf"
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
                        "key": "livraison_societe",
                        "label": "Société",
                        "advanced": True
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
                "title": "3. Commande et Expédition",
                "fields": [
                    {
                        "key": "num_facture",
                        "label": "N° facture"
                    },
                    {
                        "key": "date_facture",
                        "kind": "date",
                        "label": "Date facture",
                        "dateFormat": "slash"
                    },
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
                        "key": "payment",
                        "label": "Mode de paiement"
                    },
                    {
                        "key": "transporteur",
                        "label": "Transporteur"
                    }
                ]
            },
            {
                "title": "4. Totaux",
                "position": "after_items",
                "fields": [
                    {
                        "key": "frais",
                        "label": "Frais de livraison (€)",
                        "advanced": True
                    },
                    {
                        "key": "total",
                        "label": "Total TTC",
                        "placeholder": "95,88"
                    }
                ]
            }
        ],
        "itemBlank": {
            "pu": "0,00",
            "qte": "1",
            "sku": "",
            "tva": "20.00",
            "desc": ""
        },
        "itemColumns": [
            {
                "key": "desc",
                "label": "Désignation"
            },
            {
                "key": "qte",
                "label": "Qté"
            },
            {
                "key": "pu",
                "label": "P.U TTC (€)"
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
                    "label": "Logo Pack Moto",
                    "section": "header"
                },
                {
                    "id": "header_title",
                    "label": "Titre Facture & Numéro",
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
                    "id": "middle_refs",
                    "label": "Références Commande & Transporteur",
                    "section": "middle"
                },
                {
                    "id": "middle_columns",
                    "label": "En-têtes colonnes articles",
                    "section": "middle"
                },
                {
                    "id": "middle_rows",
                    "label": "Lignes des articles",
                    "section": "middle"
                },
                {
                    "id": "middle_tax",
                    "label": "Tableau récapitulatif TVA",
                    "section": "middle"
                },
                {
                    "id": "middle_totals",
                    "label": "Totaux HT, Frais & TTC",
                    "section": "middle"
                },
                {
                    "id": "middle_pay",
                    "label": "Mode de règlement",
                    "section": "middle"
                },
                {
                    "id": "footer",
                    "label": "Pied de page complet",
                    "master": True,
                    "section": "footer"
                },
                {
                    "id": "footer_returns",
                    "label": "Conditions de retour",
                    "section": "footer"
                },
                {
                    "id": "footer_issuer",
                    "label": "Mentions légales émetteur",
                    "section": "footer"
                },
                {
                    "id": "footer_tcpdf",
                    "label": "Mention génération document",
                    "section": "footer"
                }
            ],
            "visible": {
                "footer": True,
                "header": True,
                "middle": True,
                "middle_pay": True,
                "middle_tax": True,
                "header_logo": True,
                "middle_refs": True,
                "middle_rows": True,
                "footer_tcpdf": True,
                "header_title": True,
                "footer_issuer": True,
                "middle_totals": True,
                "footer_returns": True,
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
