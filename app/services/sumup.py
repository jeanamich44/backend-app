import os
import time
import uuid
import json
import httpx
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional, Tuple
from fastapi import HTTPException
from app.db import get_db_pool
from app.services.cache import get_cached_settings
from app.services.telegram import dispatch_admin_notification

# =====================================================================

SUMUP_API_BASE = "https://api.sumup.com"
SUMUP_CHECKOUT_PREFIX = "https://checkout.sumup.com/pay/c-"

_token_cache: Dict[str, Tuple[str, float]] = {}

# =====================================================================

async def get_payment_settings(requested_bank: Optional[str] = None) -> Tuple[Dict[str, str], int, str, Dict[str, Any]]:
    settings_data = await get_cached_settings()
    if not settings_data or not settings_data.get("payments"):
        raise HTTPException(status_code=500, detail="Table settings colonne payments absente")

    pay_data = settings_data["payments"]
    if not isinstance(pay_data, dict):
        raise HTTPException(status_code=500, detail="Format JSON payments non conforme")

    active_bank = str(pay_data.get("activeBank") or "bank2").strip()
    bank_name = requested_bank if requested_bank in ("bank1", "bank2") else active_bank

    raw_exp = pay_data.get("expirationMinutes")
    try:
        exp_minutes = int(raw_exp)
        if exp_minutes <= 0:
            exp_minutes = 15
    except (TypeError, ValueError):
        exp_minutes = 15

    limits = {
        "payment_enabled": bool(pay_data.get("paymentEnabled", True)),
        "min_amount": float(pay_data.get("minPaymentAmount") or 1.0),
        "max_amount": float(pay_data.get("maxPaymentAmount") or 500.0),
        "max_pending": int(pay_data.get("maxPendingPaymentsPerClient") or 1)
    }

    bank_obj = pay_data.get(bank_name)
    if not isinstance(bank_obj, dict):
        b_list = pay_data.get("banks_list", [])
        if isinstance(b_list, list):
            bank_obj = next((b for b in b_list if isinstance(b, dict) and b.get("id") == bank_name), None)

    if not isinstance(bank_obj, dict):
        bank_obj = pay_data.get("bank2") or pay_data.get("bank1")

    if not isinstance(bank_obj, dict):
        raise HTTPException(status_code=500, detail=f"Configuration de {bank_name} absente en base")

    pay_to_email = bank_obj.get("payToEmail")
    client_id = bank_obj.get("clientId")
    client_secret = bank_obj.get("clientSecret")
    api_key = bank_obj.get("apiKey")

    if not pay_to_email or not client_id or not client_secret:
        raise HTTPException(status_code=500, detail=f"Identifiants {bank_name} incomplets en base")

    config = {
        "pay_to_email": str(pay_to_email).strip(),
        "client_id": str(client_id).strip(),
        "client_secret": str(client_secret).strip(),
        "api_key": str(api_key).strip() if api_key else "",
    }
    return config, exp_minutes, bank_name, limits

# =====================================================================

async def get_bank_config(bank_name: str) -> Dict[str, str]:
    config, _, _, _ = await get_payment_settings(bank_name)
    return config

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
    bank_name: Optional[str] = None
) -> Dict[str, Any]:
    config, exp_minutes, selected_bank, limits = await get_payment_settings(bank_name)

    if not limits["payment_enabled"]:
        raise HTTPException(status_code=403, detail="Les recharges sont actuellement désactivées.")

    min_amt = limits["min_amount"]
    max_amt = limits["max_amount"]
    if amount < min_amt or amount > max_amt:
        raise HTTPException(
            status_code=400,
            detail=f"Montant invalide (limite autorisée: {min_amt:g}€ à {max_amt:g}€)"
        )

    pool = await get_db_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            """
            UPDATE payments
            SET status = 'EXPIRED', updated_at = NOW()
            WHERE user_id = $1 AND status = 'PENDING' AND created_at < NOW() - ($2 * INTERVAL '1 minute')
            """,
            user_id,
            exp_minutes
        )

        pending_rows = await conn.fetch(
            "SELECT checkout_id FROM payments WHERE user_id = $1 AND status = 'PENDING' ORDER BY created_at DESC",
            user_id
        )

    max_p = limits["max_pending"]
    active_pending_count = 0
    for p_row in pending_rows:
        check_res = await verify_checkout(p_row["checkout_id"], user_id=user_id)
        if check_res.get("status") == "PENDING":
            active_pending_count += 1
            if active_pending_count >= max_p:
                print(f"[RENDER SUMUP BLOCAGE] Refus création: user {user_id} a atteint la limite de factures PENDING ({active_pending_count}/{max_p})", flush=True)
                raise HTTPException(
                    status_code=409,
                    detail="Vous avez atteint la limite de paiements en attente. Veuillez finaliser votre règlement ou annuler la facture en cours."
                )

    async with pool.acquire() as conn:
        daily_count = await conn.fetchval(
            "SELECT COUNT(*) FROM payments WHERE user_id = $1 AND created_at >= NOW() - INTERVAL '24 hours'",
            user_id
        )
        if daily_count and daily_count >= 7:
            print(f"[RENDER SUMUP BLOCAGE] Quota atteint: user {user_id} a déjà généré {daily_count} factures sur 24h", flush=True)
            raise HTTPException(
                status_code=429,
                detail="Quota atteint"
            )

    token = await get_sumup_access_token(selected_bank)
    ref = str(uuid.uuid4())

    backend_base = os.getenv("RENDER_EXTERNAL_URL") or os.getenv("BACKEND_PUBLIC_URL") or getattr(settings, "backend_url", "")
    if not backend_base:
        raise HTTPException(status_code=500, detail="URL publique backend non configurée")
    webhook_url = f"{backend_base.rstrip('/')}/api/payments/webhook"

    valid_until = (datetime.now(timezone.utc) + timedelta(minutes=exp_minutes)).strftime("%Y-%m-%dT%H:%M:%SZ")

    print(f"[RENDER SUMUP CREATE] Initialisation checkout: user={user_id}, montant={amount}€, expiration={exp_minutes}min, return_url={webhook_url}", flush=True)

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
                "valid_until": valid_until,
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

        async with pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO payments (user_id, checkout_id, checkout_reference, amount, currency, status, sumup_payload)
                VALUES ($1, $2, $3, $4, 'EUR', 'PENDING', $5::jsonb)
                """,
                user_id,
                checkout_id,
                ref,
                round(float(amount), 2),
                json.dumps({"bank": selected_bank, "created_at": time.time(), "expiration_minutes": exp_minutes}),
            )

        dispatch_admin_notification(
            f"💳 <b>Nouvelle Recharge Créée</b>\n\n"
            f"👤 <b>Client ID</b> : <code>{user_id}</code>\n"
            f"💰 <b>Montant</b> : {round(float(amount), 2):.2f} €\n"
            f"🏦 <b>Banque</b> : {selected_bank.upper()}\n"
            f"🆔 <b>Checkout ID</b> : <code>{checkout_id}</code>\n"
            f"⏳ <b>Statut</b> : En attente de paiement"
        )

        return {
            "checkout_id": checkout_id,
            "payment_url": f"{SUMUP_CHECKOUT_PREFIX}{checkout_id}",
            "amount": round(float(amount), 2),
            "bank": selected_bank,
            "expiration_minutes": exp_minutes
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
            "SELECT * FROM payments WHERE checkout_id = $1",
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
            user_row = await conn.fetchrow("SELECT balance FROM users WHERE id = $1", payer_id)
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
        if res.status_code == 404:
            print(f"[RENDER SUMUP API 404] Checkout {checkout_id} non trouvé chez SumUp, bascule en EXPIRED", flush=True)
            async with pool.acquire() as conn:
                await conn.execute(
                    "UPDATE payments SET status = 'EXPIRED', updated_at = NOW() WHERE checkout_id = $1",
                    checkout_id
                )
            return {
                "checkout_id": checkout_id,
                "status": "EXPIRED",
                "amount": amount
            }

        if res.status_code != 200:
            print(f"[RENDER SUMUP API ERREUR] Code {res.status_code} pour {checkout_id}", flush=True)
            return {
                "checkout_id": checkout_id,
                "status": current_status,
                "amount": amount
            }

        sumup_data = res.json()
        raw_status = str(sumup_data.get("status", "")).upper()
        print(f"[RENDER SUMUP API RÉPONSE] Statut officiel reçu pour {checkout_id}: {raw_status}", flush=True)

    if raw_status in ("PAID", "SUCCESSFUL"):
        async with pool.acquire() as conn:
            async with conn.transaction():
                upd = await conn.execute(
                    """
                    UPDATE payments
                    SET status = 'PAID', updated_at = NOW(), sumup_payload = $1::jsonb
                    WHERE checkout_id = $2 AND status != 'PAID'
                    """,
                    json.dumps(sumup_data),
                    checkout_id
                )
                if upd == "UPDATE 1":
                    user_upd = await conn.fetchrow(
                        """
                        UPDATE users
                        SET balance = balance + $1, updated_at = NOW()
                        WHERE id = $2
                        RETURNING balance
                        """,
                        amount,
                        payer_id
                    )
                    new_balance = float(user_upd["balance"]) if user_upd else 0.0
                    print(f"[RENDER SUMUP CRÉDIT EFFECTUÉ] User {payer_id} crédité de +{amount}€ (Solde={new_balance}€)", flush=True)
                    dispatch_admin_notification(
                        f"✅ <b>Recharge Validée & Créditée !</b>\n\n"
                        f"👤 <b>Client ID</b> : <code>{payer_id}</code>\n"
                        f"💰 <b>Montant crédité</b> : +{amount:.2f} €\n"
                        f"💳 <b>Nouveau solde</b> : {new_balance:.2f} €\n"
                        f"🆔 <b>Checkout ID</b> : <code>{checkout_id}</code>"
                    )
                else:
                    user_row = await conn.fetchrow("SELECT balance FROM users WHERE id = $1", payer_id)
                    new_balance = float(user_row["balance"]) if user_row else 0.0

        return {
            "checkout_id": checkout_id,
            "status": "PAID",
            "amount": amount,
            "balance": new_balance
        }

    elif raw_status in ("FAILED", "DECLINED"):
        async with pool.acquire() as conn:
            await conn.execute(
                """
                UPDATE payments
                SET status = 'FAILED', updated_at = NOW(), sumup_payload = $1::jsonb
                WHERE checkout_id = $2
                """,
                json.dumps(sumup_data),
                checkout_id
            )
        dispatch_admin_notification(
            f"⚠️ <b>Recharge Échouée / Refusée</b>\n\n"
            f"👤 <b>Client ID</b> : <code>{payer_id}</code>\n"
            f"💰 <b>Montant</b> : {amount:.2f} €\n"
            f"🆔 <b>Checkout ID</b> : <code>{checkout_id}</code>"
        )
        return {
            "checkout_id": checkout_id,
            "status": "FAILED",
            "amount": amount
        }

    elif raw_status in ("CANCELLED", "CANCELED"):
        async with pool.acquire() as conn:
            await conn.execute(
                """
                UPDATE payments
                SET status = 'CANCELLED', updated_at = NOW(), sumup_payload = $1::jsonb
                WHERE checkout_id = $2
                """,
                json.dumps(sumup_data),
                checkout_id
            )
        dispatch_admin_notification(
            f"❌ <b>Recharge Annulée</b>\n\n"
            f"👤 <b>Client ID</b> : <code>{payer_id}</code>\n"
            f"💰 <b>Montant</b> : {amount:.2f} €\n"
            f"🆔 <b>Checkout ID</b> : <code>{checkout_id}</code>"
        )
        return {
            "checkout_id": checkout_id,
            "status": "CANCELLED",
            "amount": amount
        }

    elif raw_status == "EXPIRED":
        async with pool.acquire() as conn:
            await conn.execute(
                """
                UPDATE payments
                SET status = 'EXPIRED', updated_at = NOW(), sumup_payload = $1::jsonb
                WHERE checkout_id = $2
                """,
                json.dumps(sumup_data),
                checkout_id
            )
        dispatch_admin_notification(
            f"⌛ <b>Recharge Expirée</b>\n\n"
            f"👤 <b>Client ID</b> : <code>{payer_id}</code>\n"
            f"💰 <b>Montant</b> : {amount:.2f} €\n"
            f"🆔 <b>Checkout ID</b> : <code>{checkout_id}</code>"
        )
        return {
            "checkout_id": checkout_id,
            "status": "EXPIRED",
            "amount": amount
        }

    return {
        "checkout_id": checkout_id,
        "status": "PENDING",
        "amount": amount
    }

# =====================================================================

async def get_pending_checkout(user_id: int) -> Optional[Dict[str, Any]]:
    _, exp_minutes, _, _ = await get_payment_settings()
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            """
            UPDATE payments
            SET status = 'EXPIRED', updated_at = NOW()
            WHERE user_id = $1 AND status = 'PENDING' AND created_at < NOW() - ($2 * INTERVAL '1 minute')
            """,
            user_id,
            exp_minutes
        )

        row = await conn.fetchrow(
            """
            SELECT checkout_id, amount, created_at, sumup_payload
            FROM payments
            WHERE user_id = $1 AND status = 'PENDING'
            ORDER BY created_at DESC
            LIMIT 1
            """,
            user_id
        )

    if not row:
        return None

    check_res = await verify_checkout(row["checkout_id"], user_id=user_id)
    if check_res.get("status") != "PENDING":
        print(f"[RENDER SUMUP PENDING CHECK] La facture {row['checkout_id']} n'est plus PENDING mais {check_res.get('status')}", flush=True)
        return None

    return {
        "checkout_id": row["checkout_id"],
        "amount": float(row["amount"]),
        "payment_url": f"{SUMUP_CHECKOUT_PREFIX}{row['checkout_id']}",
        "created_at": row["created_at"].isoformat() if row["created_at"] else None,
        "expiration_minutes": exp_minutes
    }

# =====================================================================

async def cancel_checkout(user_id: int) -> Dict[str, Any]:
    print(f"[RENDER SUMUP CANCEL] Demande d'annulation de facture en attente pour user {user_id}", flush=True)

    pool = await get_db_pool()
    async with pool.acquire() as conn:
        payment = await conn.fetchrow(
            """
            SELECT checkout_id, sumup_payload
            FROM payments
            WHERE user_id = $1 AND status = 'PENDING'
            ORDER BY created_at DESC
            LIMIT 1
            """,
            user_id
        )

    if not payment:
        print(f"[RENDER SUMUP CANCEL] Aucune facture PENDING trouvée pour user {user_id}", flush=True)
        raise HTTPException(status_code=404, detail="Aucune facture en attente à annuler.")

    checkout_id = payment["checkout_id"]
    payload = payment["sumup_payload"]
    bank_name = "bank2"
    if isinstance(payload, str):
        try:
            payload = json.loads(payload)
        except Exception:
            payload = {}
    if isinstance(payload, dict) and payload.get("bank"):
        bank_name = payload["bank"]

    try:
        token = await get_sumup_access_token(bank_name)
        async with httpx.AsyncClient(timeout=10.0) as client:
            res = await client.delete(
                f"{SUMUP_API_BASE}/v0.1/checkouts/{checkout_id}",
                headers={"Authorization": f"Bearer {token}"}
            )
            print(f"[RENDER SUMUP CANCEL API] Statut API DELETE: {res.status_code}", flush=True)
    except Exception as ex:
        print(f"[RENDER SUMUP CANCEL API ERREUR] {str(ex)}", flush=True)

    async with pool.acquire() as conn:
        await conn.execute(
            """
            UPDATE payments
            SET status = 'CANCELLED', updated_at = NOW()
            WHERE checkout_id = $1
            """,
            checkout_id
        )
        print(f"[RENDER SUMUP CANCEL SUCCÈS] Facture {checkout_id} marquée CANCELLED pour user {user_id}", flush=True)

    dispatch_admin_notification(
        f"❌ <b>Recharge Annulée par le Client</b>\n\n"
        f"👤 <b>Client ID</b> : <code>{user_id}</code>\n"
        f"🆔 <b>Checkout ID</b> : <code>{checkout_id}</code>"
    )

    return {
        "success": True,
        "checkout_id": checkout_id,
        "status": "CANCELLED",
        "message": "Facture en attente annulée avec succès."
    }
