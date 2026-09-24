import json
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Response
from pydantic import BaseModel, Field
from app.auth import get_current_user
from app.services.sumup import create_checkout, verify_checkout, get_pending_checkout, cancel_checkout
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

@router.get("/pending")
async def get_current_pending_payment(
    user: Dict[str, Any] = Depends(get_current_user)
):
    return await get_pending_checkout(user_id=user["id"])

# =====================================================================

@router.post("/cancel")
async def cancel_current_pending_payment(
    user: Dict[str, Any] = Depends(get_current_user)
):
    return await cancel_checkout(user_id=user["id"])

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
    print(f"[RENDER WEBHOOK] Ping SumUp reçu: {json.dumps(payload)}", flush=True)
    checkout_id = payload.get("id") or payload.get("checkout_id") or payload.get("resource_id")
    if not checkout_id and "event" in payload and isinstance(payload.get("event"), dict):
        checkout_id = payload["event"].get("id") or payload["event"].get("checkout_id")

    if not checkout_id:
        print("[RENDER WEBHOOK WARNING] Aucun checkout_id détecté dans le ping", flush=True)
        return {"status": "ignored", "reason": "no_checkout_id"}

    print(f"[RENDER WEBHOOK] Déclenchement vérification S2S pour checkout_id={checkout_id}", flush=True)
    try:
        result = await verify_checkout(checkout_id)
        print(f"[RENDER WEBHOOK SUCCÈS] Statut vérifié: {result.get('status')}", flush=True)
        return {"status": "processed", "result": result.get("status")}
    except Exception as e:
        print(f"[RENDER WEBHOOK ERREUR] Échec traitement pour {checkout_id}: {str(e)}", flush=True)
        return {"status": "error", "detail": str(e)}

# =====================================================================

@router.api_route("/webhook", methods=["GET", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"])
async def reject_webhook_non_post():
    return Response(status_code=404)
