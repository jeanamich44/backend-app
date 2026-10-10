import time
import json
import logging
from typing import Optional, Dict, Any, List
from app.db import get_db_pool

# =====================================================================

logger = logging.getLogger(__name__)

_memory_cache: Dict[str, Dict[str, Any]] = {}

# =====================================================================

def get(key: str) -> Optional[Any]:
    entry = _memory_cache.get(key)
    if not entry:
        return None
    if time.time() > entry["expires_at"]:
        _memory_cache.pop(key, None)
        return None
    return entry["value"]

# =====================================================================

def set(key: str, value: Any, ttl: int = 300) -> None:
    _memory_cache[key] = {
        "value": value,
        "expires_at": time.time() + ttl
    }

# =====================================================================

def delete(key: str) -> None:
    _memory_cache.pop(key, None)

# =====================================================================

def delete_prefix(prefix: str) -> None:
    to_remove = [k for k in _memory_cache if k.startswith(prefix)]
    for k in to_remove:
        _memory_cache.pop(k, None)

# =====================================================================

def clear() -> None:
    _memory_cache.clear()

# =====================================================================

async def get_cached_settings() -> Optional[Dict[str, Any]]:
    cached = get("settings:global")
    if cached is not None:
        return cached

    pool = await get_db_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow("SELECT id, general, security, payments FROM settings WHERE id = 'global'")
        if not row:
            return None

        data: Dict[str, Any] = {"id": row["id"]}
        for col in ("general", "security", "payments"):
            val = row[col]
            if val is not None:
                while isinstance(val, str):
                    try:
                        val = json.loads(val)
                    except Exception:
                        break
            data[col] = val if isinstance(val, dict) else {}

        set("settings:global", data, ttl=300)
        return data

# =====================================================================

def invalidate_settings() -> None:
    delete("settings:global")

# =====================================================================

async def get_cached_service(slug: str) -> Optional[Dict[str, Any]]:
    cache_key = f"service:{slug}"
    cached = get(cache_key)
    if cached is not None:
        return cached

    pool = await get_db_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow("SELECT id, slug, name, is_active, prices, config FROM services WHERE slug = $1", slug)
        if not row:
            return None

        prices = row["prices"]
        if prices is not None:
            while isinstance(prices, str):
                try:
                    prices = json.loads(prices)
                except Exception:
                    break
        prices_dict = prices if isinstance(prices, dict) else {}

        config = row["config"]
        if config is not None:
            while isinstance(config, str):
                try:
                    config = json.loads(config)
                except Exception:
                    break
        config_dict = config if isinstance(config, dict) else {}

        data = {
            "id": row["id"],
            "slug": row["slug"],
            "name": row["name"],
            "is_active": bool(row["is_active"]),
            "prices": prices_dict,
            "config": config_dict
        }

        set(cache_key, data, ttl=300)
        return data

# =====================================================================

def invalidate_service(slug: str) -> None:
    delete(f"service:{slug}")

# =====================================================================

async def get_cached_active_admins() -> List[Dict[str, Any]]:
    cache_key = "admin:active_ids"
    cached = get(cache_key)
    if cached is not None:
        return cached

    pool = await get_db_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT id, username, first_name FROM users WHERE admin = TRUE AND is_banned = FALSE")
        data = [{"id": r["id"], "username": r["username"], "first_name": r["first_name"]} for r in rows]
        set(cache_key, data, ttl=30)
        return data

# =====================================================================

def invalidate_active_admins() -> None:
    delete("admin:active_ids")
