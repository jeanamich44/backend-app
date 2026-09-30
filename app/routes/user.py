import json
from typing import Dict, Any, Optional
from fastapi import APIRouter, Depends
from app.auth import get_current_user
from app.db import get_db_pool

# =====================================================================

router = APIRouter(prefix="/api", tags=["user"])

# =====================================================================

def _parse_json(val: Any) -> Dict[str, Any]:
    if not val:
        return {}
    res = val
    while isinstance(res, str):
        try:
            res = json.loads(res)
        except Exception:
            return {}
    return res if isinstance(res, dict) else {}

# =====================================================================

@router.get("/me")
async def get_me(user: Dict[str, Any] = Depends(get_current_user)):
    pool = await get_db_pool()
    admin_slug: Optional[str] = None
    support_telegram: Optional[str] = None
    channel_telegram: Optional[str] = None

    async with pool.acquire() as conn:
        s_row = await conn.fetchrow("SELECT general, security FROM settings WHERE id = 'global'")
        if s_row:
            gen_data = _parse_json(s_row["general"])
            sec_data = _parse_json(s_row["security"])
            support_telegram = gen_data.get("supportTelegram") or None
            channel_telegram = gen_data.get("channelTelegram") or None
            if user.get("admin") is True:
                admin_slug = sec_data.get("adminSlug") or None

    return {
        "id": user["id"],
        "username": user["username"],
        "first_name": user["first_name"],
        "balance": user["balance"],
        "admin": bool(user.get("admin", False)),
        "admin_slug": admin_slug,
        "support_telegram": support_telegram,
        "channel_telegram": channel_telegram
    }

# =====================================================================

@router.get("/user/balance")
async def get_balance(user: Dict[str, Any] = Depends(get_current_user)):
    return {
        "balance": user["balance"]
    }
