from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from app.auth import get_current_user
from app.services.sumup import create_checkout, verify_checkout
from app.db import get_db_pool

# =====================================================================

router = APIRouter(prefix="/api/payments", tags=["payments"])

# =====================================================================

class CreatePaymentRequest(BaseModel):
    amount: float = Field(..., ge=1.0, le=60.0)
    bank: Optional[str] = "bank2"

# =====================================================================

@router.post("/create")
async def create_payment(
    payload: CreatePaymentRequest,
    user: Dict[str, Any] = Depends(get_current_user)
):
    if payload.bank and payload.bank not in ("bank1", "bank2"):
        raise HTTPException(status_code=400, detail="Banque invalide (choix: bank1, bank2)")
    selected_bank = payload.bank or "bank2"
    result = await create_checkout(
        user_id=user["id"],
        amount=payload.amount,
        bank_name=selected_bank
    )
    return result

# =====================================================================

@router.get("/verify/{checkout_id}")
async def check_payment(
    checkout_id: str,
    user: Dict[str, Any] = Depends(get_current_user)
):
    result = await verify_checkout(checkout_id=checkout_id, user_id=user["id"])
    return result

# =====================================================================

@router.get("/history")
async def payment_history(
    limit: int = Query(20, ge=1, le=50),
    user: Dict[str, Any] = Depends(get_current_user)
) -> List[Dict[str, Any]]:
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT checkout_id, amount, currency, status, created_at
            FROM tma_payments
            WHERE user_id = $1
            ORDER BY created_at DESC
            LIMIT $2
            """,
            user["id"],
            limit
        )

    return [
        {
            "checkout_id": row["checkout_id"],
            "amount": float(row["amount"]),
            "currency": row["currency"],
            "status": row["status"],
            "created_at": row["created_at"].isoformat() if row["created_at"] else None
        }
        for row in rows
    ]

# =====================================================================

@router.post("/webhook")
async def sumup_webhook(payload: Dict[str, Any]):
    event_type = payload.get("event_type")
    checkout_id = payload.get("id") or payload.get("checkout_id")
    if checkout_id:
        try:
            await verify_checkout(checkout_id)
        except Exception:
            pass
    return {"status": "received"}
