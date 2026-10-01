from typing import Dict, Any, Optional
from fastapi import APIRouter, Depends
from app.auth import get_current_user
from app.services.cache import get_cached_settings

# =====================================================================

router = APIRouter(prefix="/api", tags=["user"])

# =====================================================================

@router.get("/me")
async def get_me(user: Dict[str, Any] = Depends(get_current_user)):
    admin_slug: Optional[str] = None
    support_telegram: Optional[str] = None
    channel_telegram: Optional[str] = None

    s_data = await get_cached_settings()
    if s_data:
        gen_data = s_data.get("general") or {}
        sec_data = s_data.get("security") or {}
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
