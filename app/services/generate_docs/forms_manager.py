import importlib
from typing import Optional

CATALOG = [
    ("rib", "lbp"),
    ("rib", "ca"),
    ("rib", "sg"),
    ("rib", "cm"),
    ("rib", "cic"),
    ("rib", "bnp"),
    ("rib", "ce"),
    ("rib", "bp"),
    ("rib", "lcl"),
    ("rib", "helios"),
    ("rib", "noelse"),
    ("rib", "revolut"),
    ("rib", "qonto"),
    ("rib", "bfb"),
    ("rib", "boursobank"),
    ("rib", "sumup"),
    ("rib", "mypos"),
    ("assurance", "maxance"),
    ("assurance", "axa"),
    ("justificatif", "attestation_direct_energie"),
    ("justificatif", "attestation_edf"),
    ("justificatif", "conduite_heures"),
    ("facture", "adidas"),
    ("facture", "amazon"),
    ("facture", "ami"),
    ("facture", "boulanger"),
    ("facture", "burberry"),
    ("facture", "cdiscount"),
    ("facture", "chanel"),
    ("facture", "dafy"),
    ("facture", "darty"),
    ("facture", "dior"),
    ("facture", "fnac"),
    ("facture", "fred"),
    ("facture", "gaz"),
    ("facture", "jacquemus"),
    ("facture", "loro_piana"),
    ("facture", "nike"),
    ("facture", "nocibe"),
    ("facture", "pack_moto"),
    ("facture", "sfr"),
]


def get_engine_form(category: str, slug: str) -> Optional[dict]:
    try:
        target_slug = slug
        if category == "facture":
            if slug in ("engie", "gaz"):
                target_slug = "gaz"
            elif slug in ("chanel", "channel"):
                target_slug = "chanel"
        if category == "rib":
            mod_path = f"app.services.generate_docs.rib.banks.{target_slug}.form"
        elif category in ("facture", "justificatif", "assurance"):
            mod_path = f"app.services.generate_docs.{category}.issuers.{target_slug}.form"
        elif category == "emploi":
            mod_path = f"app.services.generate_docs.emploi.{target_slug}.form"
        else:
            mod_path = f"app.services.generate_docs.{category}.{target_slug}.form"
        mod = importlib.import_module(mod_path)
        try:
            mod = importlib.reload(mod)
        except Exception:
            pass
        if hasattr(mod, "get_form_schema"):
            schema = mod.get_form_schema()
            title = schema.get("metadata", {}).get("title") or f"{category.upper()} {slug.upper()}"
            version = int(schema.get("version", 2))
            return {
                "id": f"{category}_{slug}",
                "category": category,
                "slug": slug,
                "title": title,
                "schema": schema,
                "isActive": True,
                "allowedRoles": "USER,ADMIN,RESELLER",
                "version": version,
                "updatedAt": "2026-10-06T18:00:00Z",
                "createdAt": "2026-10-01T00:00:00Z"
            }
    except Exception:
        pass
    return None


async def get_form_by_cat_slug(*args, **kwargs) -> Optional[dict]:
    if len(args) >= 3:
        return get_engine_form(str(args[1]), str(args[2]))
    elif len(args) == 2:
        return get_engine_form(str(args[0]), str(args[1]))
    elif len(args) == 1 and isinstance(args[0], str):
        parts = args[0].split("_", 1)
        if len(parts) == 2:
            return get_engine_form(parts[0], parts[1])
    cat = str(kwargs.get("category", ""))
    slug = str(kwargs.get("slug", ""))
    return get_engine_form(cat, slug)


def get_cached_form(doc_id: str) -> Optional[dict]:
    parts = str(doc_id or "").split("_", 1)
    if len(parts) == 2:
        return get_engine_form(parts[0], parts[1])
    return None


async def get_form(*args, **kwargs) -> Optional[dict]:
    doc_id = kwargs.get("doc_id")
    if not doc_id and args:
        doc_id = args[-1]
    return get_cached_form(str(doc_id or ""))


async def list_forms(*args, **kwargs) -> list[dict]:
    forms = []
    for cat, slug in CATALOG:
        f = get_engine_form(cat, slug)
        if f:
            forms.append(f)
    return forms


async def load_forms_cache(*args, **kwargs) -> dict[str, dict]:
    return {f["id"]: f for f in await list_forms()}


async def save_form(*args, **kwargs) -> dict:
    category = kwargs.get("category", "")
    slug = kwargs.get("slug", "")
    if not category and len(args) >= 3:
        category = args[2]
        slug = args[3] if len(args) >= 4 else ""
    return get_engine_form(str(category), str(slug)) or {}


async def delete_form(*args, **kwargs) -> bool:
    return True
