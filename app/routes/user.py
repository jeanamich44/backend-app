import json
from typing import Dict, Any, Optional
from fastapi import APIRouter, Depends
from app.auth import get_current_user
from app.db import get_db_pool
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

    services_status: Dict[str, bool] = {}
    generate_docs_config: Dict[str, Any] = {}
    try:
        pool = await get_db_pool()
        async with pool.acquire() as conn:
            s_rows = await conn.fetch("SELECT slug, is_active, config FROM services")
            for r in s_rows:
                slug = r["slug"]
                is_active = bool(r["is_active"])
                services_status[slug] = is_active
                if slug == "generate-docs":
                    cfg = r["config"]
                    while isinstance(cfg, str):
                        cfg = json.loads(cfg)
                    cfg_dict = cfg if isinstance(cfg, dict) else {}
                    generate_docs_config = {
                        "isActive": is_active,
                        "flattenPdf": bool(cfg_dict.get("flattenPdf", True)),
                        "previewOff": bool(cfg_dict.get("previewOff", False)),
                        "previewCooldownEnabled": bool(cfg_dict.get("previewCooldownEnabled", True)),
                        "previewCooldownSeconds": int(cfg_dict.get("previewCooldownSeconds", 30)),
                        "subcategories": cfg_dict.get("subcategories", {})
                    }
    except Exception:
        pass

    return {
        "id": user["id"],
        "username": user["username"],
        "first_name": user["first_name"],
        "balance": user["balance"],
        "admin": bool(user.get("admin", False)),
        "admin_slug": admin_slug,
        "support_telegram": support_telegram,
        "channel_telegram": channel_telegram,
        "services": services_status,
        "generateDocs": generate_docs_config
    }

# =====================================================================

@router.get("/user/balance")
async def get_balance(user: Dict[str, Any] = Depends(get_current_user)):
    return {
        "balance": user["balance"]
    }
