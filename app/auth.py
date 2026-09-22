import hmac
import hashlib
import json
import urllib.parse
from typing import Optional, Dict, Any
from fastapi import Header, HTTPException, status
from app.config import settings
from app.db import get_db_pool

# =====================================================================

def validate_telegram_init_data(init_data_raw: str) -> Optional[Dict[str, Any]]:
    if not init_data_raw:
        return None
    try:
        parsed = urllib.parse.parse_qs(init_data_raw)
        hash_val = parsed.get("hash", [None])[0]
        user_str = parsed.get("user", [None])[0]
        if not user_str:
            return None

        user_data = json.loads(user_str)

        if not settings.telegram_bot_token:
            raise HTTPException(status_code=500, detail="TELEGRAM_BOT_TOKEN absent de la configuration")

        if not hash_val:
            return None

        data_check_list = []
        for key in sorted(parsed.keys()):
            if key != "hash":
                data_check_list.append(f"{key}={parsed[key][0]}")
        data_check_string = "\n".join(data_check_list)

        secret_key = hmac.new(b"WebAppData", settings.telegram_bot_token.encode(), hashlib.sha256).digest()
        calc_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

        if not hmac.compare_digest(calc_hash, hash_val):
            return None

        return user_data
    except HTTPException:
        raise
    except Exception:
        return None

# =====================================================================

async def upsert_telegram_user(user_data: Dict[str, Any]) -> Dict[str, Any]:
    pool = await get_db_pool()
    user_id = int(user_data["id"])
    username = user_data.get("username")
    first_name = user_data.get("first_name")
    last_name = user_data.get("last_name")

    query = """
    INSERT INTO tma_users (id, username, first_name, last_name, updated_at)
    VALUES ($1, $2, $3, $4, NOW())
    ON CONFLICT (id) DO UPDATE SET
        username = EXCLUDED.username,
        first_name = EXCLUDED.first_name,
        last_name = EXCLUDED.last_name,
        updated_at = NOW()
    RETURNING id, username, first_name, last_name, balance, is_banned, created_at, updated_at;
    """

    async with pool.acquire() as conn:
        row = await conn.fetchrow(query, user_id, username, first_name, last_name)
        if not row:
            raise HTTPException(status_code=500, detail="Database operation failed")

        if row["is_banned"]:
            raise HTTPException(status_code=403, detail="Account suspended")

        return {
            "id": row["id"],
            "username": row["username"],
            "first_name": row["first_name"],
            "last_name": row["last_name"],
            "balance": float(row["balance"]),
            "is_banned": row["is_banned"],
            "created_at": row["created_at"].isoformat() if row["created_at"] else None,
            "updated_at": row["updated_at"].isoformat() if row["updated_at"] else None
        }

# =====================================================================

async def get_current_user(
    x_telegram_init_data: Optional[str] = Header(None, alias="X-Telegram-Init-Data")
) -> Dict[str, Any]:
    if not x_telegram_init_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    user_data = validate_telegram_init_data(x_telegram_init_data)
    if not user_data or "id" not in user_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    return await upsert_telegram_user(user_data)
