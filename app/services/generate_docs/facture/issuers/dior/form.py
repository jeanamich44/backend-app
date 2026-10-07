def get_form_schema() -> dict:
    return {
        "version": 5,
        "defaults": {
            "nom": "Martin",
            "code": "1066000",
            "oper": "Maria",
            "items": [
                {
                    "qty": "1",
                    "ref": "KC1322VNI",
                    "desc": "S799 / T40 SNEAKERS TOILE ET VEAU",
                    "total": "790,00",
                    "unit_price": "790,00"
                }
            ],
            "store": "FRpar01",
            "trans": "10738",
            "prenom": "Lucas",
            "vendeur": "Maria",
            "total_ht": "658,33",
            "tva_rate": "TVA 20%",
            "duplicata": "DUPLICATA",
            "store_num": "3",
            "total_ttc": "790,00",
            "client_tel": "0658692545",
            "date_vente": "24/04/2024",
            "tva_amount": "131,67",
            "heure_vente": "16:32",
            "tva_product": "TVA FR Product",
            "vente_title": "VENTE",
            "client_email": "martin.lucas@gmail.com",
            "rendu_amount": "10,00",
            "total_facture": "790,00",
            "payment_amount": "800,00",
            "payment_method": "Cash"
        },
        "metadata": {
            "logo": "/logos/dior.svg",
            "title": "Dior",
            "apiBase": "/api/generate-docs/facture/dior",
            "itemKey": "items",
            "backHref": "/services/generate-docs/facture",
            "headerBg": "bg-white border-neutral-800/30",
            "maxItems": 3,
            "priceKey": "dior",
            "subtitle": "Facture boutique Christian Dior",
            "backLabel": "Retour aux factures",
            "itemLabel": "Articles",
            "logoClass": "scale-[0.70] md:scale-[0.75]",
            "generateLabel": "Générer la facture Dior",
            "filenameTemplate": "Facture_Dior.pdf"
        },
        "sections": [
            {
                "title": "1. Coordonnées client",
                "fields": [
                    {
                        "key": "nom",
                        "kind": "text",
                        "span": 1,
                        "label": "Nom",
                        "rules": {
                            "max": 35,
                            "min": 2,
                            "required": True
                        },
                        "placeholder": "Martin"
                    },
                    {
                        "key": "prenom",
                        "kind": "text",
                        "span": 1,
                        "label": "Prénom",
                        "rules": {
                            "max": 35,
                            "min": 2,
                            "required": True
                        },
                        "placeholder": "Lucas"
                    },
                    {
                        "key": "client_email",
                        "kind": "text",
                        "span": 1,
                        "label": "Email",
                        "rules": {
                            "max": 50,
                            "min": 5,
                            "required": True
                        },
                        "placeholder": "martin.lucas@gmail.com"
                    },
                    {
                        "key": "client_tel",
                        "kind": "text",
                        "span": 1,
                        "label": "Téléphone",
                        "rules": {
                            "max": 20,
                            "min": 10,
                            "required": True,
                            "transform": "digits_only"
                        },
                        "placeholder": "0658692545"
                    }
                ]
            },
            {
                "title": "2. Vente en boutique",
                "fields": [
                    {
                        "key": "date_vente",
                        "kind": "date",
                        "span": 1,
                        "label": "Date de la vente",
                        "rules": {
                            "required": True
                        },
                        "dateFormat": "slash",
                        "placeholder": "JJ/MM/AAAA"
                    },
                    {
                        "key": "heure_vente",
                        "kind": "time",
                        "span": 1,
                        "label": "Heure de la vente",
                        "rules": {
                            "required": True
                        },
                        "placeholder": "HH:MM"
                    },
                    {
                        "key": "payment_method",
                        "kind": "select",
                        "span": 1,
                        "label": "Mode de paiement",
                        "rules": {
                            "max": 20,
                            "required": True
                        },
                        "options": [
                            {
                                "label": "Cash",
                                "value": "Cash"
                            },
                            {
                                "label": "Carte Bancaire",
                                "value": "Carte Bancaire"
                            },
                            {
                                "label": "American Express",
                                "value": "American Express"
                            },
                            {
                                "label": "Visa",
                                "value": "Visa"
                            },
                            {
                                "label": "MasterCard",
                                "value": "MasterCard"
                            }
                        ]
                    },
                    {
                        "key": "vendeur",
                        "kind": "text",
                        "span": 1,
                        "label": "Conseiller / Vendeur",
                        "rules": {
                            "max": 25,
                            "min": 2,
                            "required": True
                        },
                        "placeholder": "Maria"
                    }
                ]
            },
            {
                "title": "3. Paramètres boutique & Caisse",
                "fields": [
                    {
                        "key": "store",
                        "kind": "text",
                        "span": 1,
                        "label": "Boutique / Store",
                        "rules": {
                            "max": 20,
                            "required": True
                        },
                        "advanced": True
                    },
                    {
                        "key": "store_num",
                        "kind": "text",
                        "span": 1,
                        "label": "N° Caisse",
                        "rules": {
                            "max": 10,
                            "required": True
                        },
                        "advanced": True
                    },
                    {
                        "key": "oper",
                        "kind": "text",
                        "span": 1,
                        "label": "Opérateur",
                        "rules": {
                            "max": 25,
                            "required": True
                        },
                        "advanced": True
                    },
                    {
                        "key": "trans",
                        "kind": "text",
                        "span": 1,
                        "label": "N° Transaction",
                        "rules": {
                            "max": 25,
                            "required": True
                        },
                        "advanced": True
                    },
                    {
                        "key": "vente_title",
                        "kind": "text",
                        "span": 1,
                        "label": "Titre vente",
                        "rules": {
                            "max": 20,
                            "required": True
                        },
                        "advanced": True
                    },
                    {
                        "key": "duplicata",
                        "kind": "text",
                        "span": 1,
                        "label": "Mention Duplicata",
                        "rules": {
                            "max": 30,
                            "required": True
                        },
                        "advanced": True
                    },
                    {
                        "key": "code",
                        "kind": "text",
                        "span": 2,
                        "label": "Code transaction / Barcode",
                        "rules": {
                            "max": 25,
                            "required": True
                        },
                        "advanced": True
                    }
                ],
                "advanced": True
            },
            {
                "title": "4. Totaux & Taxes",
                "position": "after_items",
                "fields": [
                    {
                        "key": "total_ttc",
                        "kind": "text",
                        "span": 2,
                        "label": "Total TTC",
                        "rules": {
                            "max": 15,
                            "required": True
                        }
                    },
                    {
                        "key": "total_facture",
                        "kind": "text",
                        "span": 1,
                        "label": "Total facture",
                        "rules": {
                            "max": 15,
                            "required": True
                        },
                        "advanced": True
                    },
                    {
                        "key": "total_ht",
                        "kind": "text",
                        "span": 1,
                        "label": "Total HT",
                        "rules": {
                            "max": 15,
                            "required": True
                        },
                        "advanced": True
                    },
                    {
                        "key": "tva_amount",
                        "kind": "text",
                        "span": 1,
                        "label": "Montant TVA",
                        "rules": {
                            "max": 15,
                            "required": True
                        },
                        "advanced": True
                    },
                    {
                        "key": "payment_amount",
                        "kind": "text",
                        "span": 1,
                        "label": "Montant versé",
                        "rules": {
                            "max": 15,
                            "required": True
                        },
                        "advanced": True
                    },
                    {
                        "key": "rendu_amount",
                        "kind": "text",
                        "span": 1,
                        "label": "Rendu",
                        "rules": {
                            "max": 15,
                            "required": True
                        },
                        "advanced": True
                    }
                ]
            }
        ],
        "itemBlank": {
            "qty": "1",
            "ref": "",
            "desc": "",
            "total": "0,00",
            "unit_price": "0,00"
        },
        "itemColumns": [
            {
                "key": "ref",
                "label": "Référence",
                "rules": {
                    "max": 20
                }
            },
            {
                "key": "desc",
                "label": "Désignation",
                "rules": {
                    "max": 50
                }
            },
            {
                "key": "qty",
                "label": "Qté",
                "rules": {
                    "max": 10
                }
            },
            {
                "key": "unit_price",
                "label": "Prix unitaire (€)",
                "rules": {
                    "max": 15
                }
            },
            {
                "key": "total",
                "label": "Total (€)",
                "rules": {
                    "max": 15
                }
            }
        ],
        "itemsConfig": {
            "key": "items",
            "label": "Articles (3 maximum)",
            "columns": [
                {
                    "key": "ref",
                    "kind": "text",
                    "label": "Référence",
                    "required": True
                },
                {
                    "key": "desc",
                    "kind": "text",
                    "label": "Désignation",
                    "required": True
                },
                {
                    "key": "qty",
                    "kind": "text",
                    "label": "Qté",
                    "required": True
                },
                {
                    "key": "unit_price",
                    "kind": "text",
                    "label": "Prix unitaire (€)",
                    "required": True
                },
                {
                    "key": "total",
                    "kind": "text",
                    "label": "Total (€)",
                    "required": True
                }
            ],
            "enabled": True,
            "maxItems": 3,
            "blankItem": {
                "qty": "1",
                "ref": "",
                "desc": "",
                "total": "0,00",
                "unit_price": "0,00"
            }
        },
        "customLayout": {
            "blocks": [
                {
                    "id": "header",
                    "label": "En-tête complet",
                    "master": True,
                    "section": "header"
                },
                {
                    "id": "header_bg",
                    "label": "Fond architectural Dior",
                    "section": "header"
                },
                {
                    "id": "header_logo",
                    "label": "Logo boutique Dior",
                    "section": "header"
                },
                {
                    "id": "header_duplicata",
                    "label": "Mention Duplicata",
                    "section": "header"
                },
                {
                    "id": "header_line",
                    "label": "Ligne de séparation en-tête",
                    "section": "header"
                },
                {
                    "id": "header_contact",
                    "label": "Coordonnées boutique Dior",
                    "section": "header"
                },
                {
                    "id": "header_client",
                    "label": "Coordonnées client",
                    "section": "header"
                },
                {
                    "id": "header_meta",
                    "label": "Métadonnées vente & caisse",
                    "section": "header"
                },
                {
                    "id": "middle",
                    "label": "Corps de facture complet",
                    "master": True,
                    "section": "middle"
                },
                {
                    "id": "middle_page",
                    "label": "Numérotation de page",
                    "section": "middle"
                },
                {
                    "id": "middle_vendeur",
                    "label": "Nom du vendeur",
                    "section": "middle"
                },
                {
                    "id": "middle_articles",
                    "label": "Lignes d'articles",
                    "section": "middle"
                },
                {
                    "id": "middle_line",
                    "label": "Filet de séparation totaux",
                    "section": "middle"
                },
                {
                    "id": "middle_totals",
                    "label": "Bloc totaux & TVA",
                    "section": "middle"
                },
                {
                    "id": "middle_pay",
                    "label": "Détails paiement & rendu",
                    "section": "middle"
                },
                {
                    "id": "middle_code",
                    "label": "Code-barres / Code transaction",
                    "section": "middle"
                },
                {
                    "id": "footer",
                    "label": "Pied de page complet",
                    "master": True,
                    "section": "footer"
                },
                {
                    "id": "footer_legal",
                    "label": "Mentions légales & retours",
                    "section": "footer"
                }
            ],
            "visible": {
                "footer": True,
                "header": True,
                "middle": True,
                "header_bg": True,
                "middle_pay": True,
                "header_line": True,
                "header_logo": True,
                "header_meta": True,
                "middle_code": True,
                "middle_line": True,
                "middle_page": True,
                "footer_legal": True,
                "header_client": True,
                "middle_totals": True,
                "header_contact": True,
                "middle_vendeur": True,
                "middle_articles": True,
                "header_duplicata": True
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
