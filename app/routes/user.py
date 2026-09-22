from typing import Dict, Any
from fastapi import APIRouter, Depends
from app.auth import get_current_user

# =====================================================================

router = APIRouter(prefix="/api", tags=["user"])

# =====================================================================

@router.get("/me")
async def get_me(user: Dict[str, Any] = Depends(get_current_user)):
    return {
        "id": user["id"],
        "username": user["username"],
        "first_name": user["first_name"],
        "balance": user["balance"]
    }

# =====================================================================

@router.get("/user/balance")
async def get_balance(user: Dict[str, Any] = Depends(get_current_user)):
    return {
        "balance": user["balance"]
    }
