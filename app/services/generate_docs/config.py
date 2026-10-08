import json
import time

from app.core.billing import safe_parse_json

_CACHED_DOCS_CONFIG = None
_CACHED_DOCS_CONFIG_TIME = 0.0
DOCS_CONFIG_CACHE_TTL = 30.0

# --------------------------------------------------------------------------
def invalidate_generate_docs_config_cache() -> None:
    global _CACHED_DOCS_CONFIG, _CACHED_DOCS_CONFIG_TIME
    _CACHED_DOCS_CONFIG = None
    _CACHED_DOCS_CONFIG_TIME = 0.0

DEFAULT_PREVIEW_COOLDOWN_SECONDS = 600
SUBCATEGORY_DEFAULTS = {
    "rib": True,
    "releve": True,
    "assurance": True,
    "facture": True,
    "justificatif": True,
    "emploi": True,
}

NEW_PRICE_DEFAULTS = {
    "adidas": 5.0,
    "amazon": 5.0,
    "fnac": 5.0,
    "nike": 5.0,
    "ami": 5.0,
    "burberry": 5.0,
    "cdiscount": 5.0,
    "dafy": 5.0,
    "darty": 5.0,
    "boulanger": 5.0,
    "gaz": 5.0,
    "loro_piana": 5.0,
    "pack_moto": 5.0,
    "dior": 5.0,
    "jacquemus": 5.0,
    "chanel": 5.0,
    "channel": 5.0,
    "fred": 5.0,
    "nocibe": 5.0,
    "sfr": 5.0,
    "conduite_heures": 5.0,
    "attestation_edf": 5.0,
    "attestation_direct_energie": 5.0,
    "axa": 5.0,
    "fiche_de_paie_1m": 8.0,
    "fiche_de_paie_3m": 20.0,
    "fiche_de_paie_6m": 40.0,
    "fiche_de_paie_12m": 60.0,
}


def _as_bool(value, default: bool = True) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        return value.strip().lower() not in {"0", "false", "off", "no", ""}
    if isinstance(value, dict):
        return _as_bool(value.get("enabled", value.get("active", default)), default)
    return default


def _as_int(value, default: int, minimum: int = 0, maximum: int = 86400) -> int:
    try:
        parsed = int(float(value))
    except (TypeError, ValueError):
        parsed = default
    return max(minimum, min(maximum, parsed))


def normalize_generate_docs_config(raw) -> dict:
    data = raw if isinstance(raw, dict) else safe_parse_json(raw)
    subs_raw = data.get("subcategories") if isinstance(data.get("subcategories"), dict) else {}
    subcategories = {}
    for key, default in SUBCATEGORY_DEFAULTS.items():
        info = subs_raw.get(key)
        enabled = default
        documents = {}
        if isinstance(info, dict):
            enabled = _as_bool(info.get("active", info.get("enabled")), default)
            docs = info.get("documents")
            if isinstance(docs, dict):
                documents = {k: {"enabled": _as_bool(v, True)} for k, v in docs.items()}
        elif info is not None:
            enabled = _as_bool(info, default)
        subcategories[key] = {"active": enabled, "enabled": enabled, "documents": documents}

    seconds = _as_int(
        data.get("previewCooldownSeconds", DEFAULT_PREVIEW_COOLDOWN_SECONDS),
        DEFAULT_PREVIEW_COOLDOWN_SECONDS,
    )
    enabled = _as_bool(data.get("previewCooldownEnabled"), True)
    if seconds <= 0:
        enabled = False
    preview_off = _as_bool(data.get("previewOff"), False)
    flatten_pdf = _as_bool(data.get("flattenPdf"), False)

    return {
        **data,
        "previewCooldownEnabled": enabled,
        "previewCooldownSeconds": seconds,
        "previewOff": preview_off,
        "flattenPdf": flatten_pdf,
        "subcategories": subcategories,
    }


def merge_generate_docs_prices(prices) -> tuple[dict, bool]:
    data = prices if isinstance(prices, dict) else safe_parse_json(prices)
    if not isinstance(data, dict):
        data = {}
    changed = False
    merged = dict(data)
    for key, value in NEW_PRICE_DEFAULTS.items():
        if key not in merged:
            merged[key] = value
            changed = True
    return merged, changed


def seed_generate_docs_config(raw) -> tuple[dict, bool]:
    data = raw if isinstance(raw, dict) else safe_parse_json(raw)
    if not isinstance(data, dict):
        data = {}
    subs_raw = data.get("subcategories") if isinstance(data.get("subcategories"), dict) else {}
    first_justificatif = "justificatif" not in subs_raw
    first_emploi = "emploi" not in subs_raw
    normalized = normalize_generate_docs_config(data)
    changed = first_justificatif or first_emploi
    if first_justificatif:
        normalized["subcategories"]["facture"]["enabled"] = True
        normalized["subcategories"]["justificatif"]["enabled"] = True
    if first_emploi:
        normalized["subcategories"]["emploi"]["enabled"] = True
    next_config = {
        **data,
        "previewCooldownEnabled": normalized["previewCooldownEnabled"],
        "previewCooldownSeconds": normalized["previewCooldownSeconds"],
        "previewOff": normalized["previewOff"],
        "flattenPdf": normalized["flattenPdf"],
        "subcategories": normalized["subcategories"],
    }
    return next_config, changed


async def persist_generate_docs_params(conn, prices: dict, config: dict) -> None:
    await conn.execute(
        "UPDATE services SET prices = $1::jsonb, config = $2::jsonb WHERE slug = $3",
        json.dumps(prices),
        json.dumps(config),
        "generate-docs",
    )


async def load_generate_docs_config(db_pool, force_refresh: bool = False) -> dict:
    global _CACHED_DOCS_CONFIG, _CACHED_DOCS_CONFIG_TIME
    now = time.time()
    if not force_refresh and _CACHED_DOCS_CONFIG is not None and (now - _CACHED_DOCS_CONFIG_TIME) < DOCS_CONFIG_CACHE_TTL:
        return _CACHED_DOCS_CONFIG
    if not db_pool:
        return {
            "isActive": False,
            "prices": dict(NEW_PRICE_DEFAULTS),
            **normalize_generate_docs_config({}),
        }
    async with db_pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT prices, config, is_active FROM services WHERE slug = $1",
            "generate-docs",
        )
        if not row:
            res = {
                "isActive": False,
                "prices": dict(NEW_PRICE_DEFAULTS),
                **normalize_generate_docs_config({}),
            }
            _CACHED_DOCS_CONFIG = res
            _CACHED_DOCS_CONFIG_TIME = now
            return res
        prices, prices_changed = merge_generate_docs_prices(row["prices"])
        config, config_changed = seed_generate_docs_config(row["config"])
        if prices_changed or config_changed:
            await persist_generate_docs_params(conn, prices, config)
    normalized = normalize_generate_docs_config(config)
    res = {
        "isActive": row["is_active"] is not False,
        "prices": prices or {},
        "previewCooldownEnabled": normalized["previewCooldownEnabled"],
        "previewCooldownSeconds": normalized["previewCooldownSeconds"],
        "previewOff": normalized["previewOff"],
        "flattenPdf": normalized["flattenPdf"],
        "subcategories": normalized["subcategories"],
    }
    _CACHED_DOCS_CONFIG = res
    _CACHED_DOCS_CONFIG_TIME = now
    return res
