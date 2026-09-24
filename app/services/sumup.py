import os
import time
import uuid
import json
import httpx
from typing import Dict, Any, Optional, Tuple
from fastapi import HTTPException
from app.db import get_db_pool

# =====================================================================

SUMUP_API_BASE = "https://api.sumup.com"
SUMUP_CHECKOUT_PREFIX = "https://checkout.sumup.com/pay/c-"

_token_cache: Dict[str, Tuple[str, float]] = {}

# =====================================================================

async def get_bank_config(bank_name: str) -> Dict[str, str]:
    if bank_name not in ("bank1", "bank2"):
        raise HTTPException(status_code=400, detail=f"Banque '{bank_name}' non reconnue")

    pool = await get_db_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow("SELECT payments FROM settings WHERE id = 'global'")
        if not row or not row["payments"]:
            raise HTTPException(status_code=500, detail="Table settings colonne payments absente")

        pay_data = row["payments"]
        while isinstance(pay_data, str):
            pay_data = json.loads(pay_data)

        if not isinstance(pay_data, dict):
            raise HTTPException(status_code=500, detail="Format JSON payments non conforme")

        bank_obj = pay_data.get(bank_name)
        if not isinstance(bank_obj, dict):
            raise HTTPException(status_code=500, detail=f"Configuration de {bank_name} absente en base")

        pay_to_email = bank_obj.get("payToEmail")
        client_id = bank_obj.get("clientId")
        client_secret = bank_obj.get("clientSecret")
        api_key = bank_obj.get("apiKey")

        if not pay_to_email or not client_id or not client_secret:
            raise HTTPException(status_code=500, detail=f"Identifiants {bank_name} incomplets en base")

        return {
            "pay_to_email": str(pay_to_email).strip(),
            "client_id": str(client_id).strip(),
            "client_secret": str(client_secret).strip(),
            "api_key": str(api_key).strip() if api_key else "",
        }

# =====================================================================

async def get_sumup_access_token(bank_name: str) -> str:
    global _token_cache
    now = time.time()
    if bank_name in _token_cache:
        token, expires_at = _token_cache[bank_name]
        if now < expires_at:
            return token

    config = await get_bank_config(bank_name)
    async with httpx.AsyncClient(timeout=15.0) as client:
        res = await client.post(
            f"{SUMUP_API_BASE}/token",
            data={
                "grant_type": "client_credentials",
                "client_id": config["client_id"],
                "client_secret": config["client_secret"],
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        if res.status_code != 200:
            raise HTTPException(status_code=502, detail="Authentification passerelle SumUp échouée")
        data = res.json()
        token = data["access_token"]
        expires_in = int(data.get("expires_in", 3600))
        _token_cache[bank_name] = (token, now + expires_in - 120)
        return token

# =====================================================================

async def create_checkout(
    user_id: int,
    amount: float,
    bank_name: str = "bank2"
) -> Dict[str, Any]:
    if amount < 1.0 or amount > 60.0:
        raise HTTPException(status_code=400, detail="Montant invalide (limite 1€ à 60€)")

    config = await get_bank_config(bank_name)
    token = await get_sumup_access_token(bank_name)
    ref = str(uuid.uuid4())

    backend_base = os.getenv("RENDER_EXTERNAL_URL") or os.getenv("BACKEND_PUBLIC_URL") or "https://backend-app-eas7.onrender.com"
    webhook_url = f"{backend_base.rstrip('/')}/api/payments/webhook"

    print(f"[RENDER SUMUP CREATE] Initialisation checkout: user={user_id}, montant={amount}€, return_url={webhook_url}", flush=True)

    async with httpx.AsyncClient(timeout=15.0) as client:
        res = await client.post(
            f"{SUMUP_API_BASE}/v0.1/checkouts",
            json={
                "checkout_reference": ref,
                "amount": round(float(amount), 2),
                "currency": "EUR",
                "pay_to_email": config["pay_to_email"],
                "description": f"Recharge {amount:.2f} EUR",
                "return_url": webhook_url,
                "hosted_checkout": {"enabled": True},
            },
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
        )
        if res.status_code not in (200, 201):
            print(f"[RENDER SUMUP CREATE ERREUR] Statut={res.status_code}, Réponse={res.text}", flush=True)
            raise HTTPException(status_code=502, detail="Création checkout SumUp échouée")

        data = res.json()
        checkout_id = data.get("id")
        if not checkout_id:
            raise HTTPException(status_code=502, detail="Réponse SumUp invalide sans checkout id")

        print(f"[RENDER SUMUP CREATE SUCCÈS] Checkout ID: {checkout_id}, Ref: {ref}", flush=True)

        pool = await get_db_pool()
        async with pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO tma_payments (user_id, checkout_id, checkout_reference, amount, currency, status, sumup_payload)
                VALUES ($1, $2, $3, $4, 'EUR', 'PENDING', $5::jsonb)
                """,
                user_id,
                checkout_id,
                ref,
                round(float(amount), 2),
                json.dumps({"bank": bank_name, "created_at": time.time()}),
            )

        return {
            "checkout_id": checkout_id,
            "payment_url": f"{SUMUP_CHECKOUT_PREFIX}{checkout_id}",
            "amount": round(float(amount), 2),
            "bank": bank_name
        }

# =====================================================================

async def verify_checkout(
    checkout_id: str,
    user_id: Optional[int] = None
) -> Dict[str, Any]:
    print(f"[RENDER SUMUP VERIFY] Requête vérification pour {checkout_id} (user_id={user_id})", flush=True)

    pool = await get_db_pool()
    async with pool.acquire() as conn:
        payment = await conn.fetchrow(
            "SELECT * FROM tma_payments WHERE checkout_id = $1",
            checkout_id
        )

    if not payment:
        print(f"[RENDER SUMUP VERIFY ERREUR] Paiement {checkout_id} inexistant en BDD", flush=True)
        raise HTTPException(status_code=404, detail="Paiement introuvable")

    if user_id and payment["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Accès non autorisé à ce paiement")

    current_status = payment["status"]
    amount = float(payment["amount"])
    payer_id = payment["user_id"]

    if current_status == "PAID":
        print(f"[RENDER SUMUP VERIFY DÉJÀ PAYÉ] Checkout {checkout_id} déjà marqué PAID pour user {payer_id}", flush=True)
        async with pool.acquire() as conn:
            user_row = await conn.fetchrow("SELECT balance FROM tma_users WHERE id = $1", payer_id)
            balance = float(user_row["balance"]) if user_row else 0.0
        return {
            "checkout_id": checkout_id,
            "status": "PAID",
            "amount": amount,
            "balance": balance
        }

    payload = payment["sumup_payload"]
    if isinstance(payload, str):
        try:
            payload = json.loads(payload)
        except Exception:
            payload = {}

    if not isinstance(payload, dict) or not payload.get("bank"):
        raise HTTPException(status_code=500, detail="Métadonnées de banque manquantes dans la transaction")

    bank_name = payload["bank"]
    token = await get_sumup_access_token(bank_name)

    async with httpx.AsyncClient(timeout=15.0) as client:
        res = await client.get(
            f"{SUMUP_API_BASE}/v0.1/checkouts/{checkout_id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        if res.status_code != 200:
            print(f"[RENDER SUMUP API ERREUR] Code {res.status_code} pour {checkout_id}", flush=True)
            return {
                "checkout_id": checkout_id,
                "status": current_status,
                "amount": amount
            }

        sumup_data = res.json()
        remote_status = str(sumup_data.get("status", "")).upper()
        print(f"[RENDER SUMUP API RÉPONSE] Statut officiel reçu pour {checkout_id}: {remote_status}", flush=True)

    if remote_status == "PAID":
        async with pool.acquire() as conn:
            async with conn.transaction():
                upd = await conn.execute(
                    """
                    UPDATE tma_payments
                    SET status = 'PAID', updated_at = NOW(), sumup_payload = $1::jsonb
                    WHERE checkout_id = $2 AND status != 'PAID'
                    """,
                    json.dumps(sumup_data),
                    checkout_id
                )
                if upd == "UPDATE 1":
                    user_upd = await conn.fetchrow(
                        """
                        UPDATE tma_users
                        SET balance = balance + $1, updated_at = NOW()
                        WHERE id = $2
                        RETURNING balance
                        """,
                        amount,
                        payer_id
                    )
                    new_balance = float(user_upd["balance"]) if user_upd else 0.0
                    print(f"[RENDER SUMUP CRÉDIT EFFECTUÉ] User {payer_id} crédité de +{amount}€ (Solde={new_balance}€)", flush=True)
                else:
                    user_row = await conn.fetchrow("SELECT balance FROM tma_users WHERE id = $1", payer_id)
                    new_balance = float(user_row["balance"]) if user_row else 0.0

        return {
            "checkout_id": checkout_id,
            "status": "PAID",
            "amount": amount,
            "balance": new_balance
        }

    elif remote_status in ("FAILED", "CANCELLED", "EXPIRED"):
        async with pool.acquire() as conn:
            await conn.execute(
                """
                UPDATE tma_payments
                SET status = $1, updated_at = NOW(), sumup_payload = $2::jsonb
                WHERE checkout_id = $3
                """,
                remote_status,
                json.dumps(sumup_data),
                checkout_id
            )
        return {
            "checkout_id": checkout_id,
            "status": remote_status,
            "amount": amount
        }

    return {
        "checkout_id": checkout_id,
        "status": "PENDING",
        "amount": amount
    }
