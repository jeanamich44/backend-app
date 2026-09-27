import json
import re
import urllib.parse
from typing import Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
import httpx

try:
    from curl_cffi.requests import AsyncSession
except Exception:
    AsyncSession = None

from app.auth import get_current_user
from app.db import get_db_pool

# =====================================================================

router = APIRouter(prefix="/api", tags=["client_services"])

# =====================================================================

class CarrefourBuyPayload(BaseModel):
    value: Optional[float] = None
    stock_id: Optional[int] = None

class IptvBuyPayload(BaseModel):
    subscription_type: str = Field(default="m3u", pattern="^(m3u)$")
    sub: int = Field(..., ge=1, le=12)

# =====================================================================

def _extract_url_from_json(element: Any) -> str:
    if isinstance(element, dict):
        for k in ("url", "link", "m3u_url", "playlist_url", "playlist", "download_link"):
            val = element.get(k)
            if isinstance(val, str) and (val.startswith("http://") or val.startswith("https://")):
                return val
        for v in element.values():
            found = _extract_url_from_json(v)
            if found:
                return found
    elif isinstance(element, list):
        for item in element:
            found = _extract_url_from_json(item)
            if found:
                return found
    elif isinstance(element, str):
        if element.startswith("http://") or element.startswith("https://"):
            return element
    return ""

def _extract_url_from_response(text: str) -> str:
    trimmed = (text or "").strip()
    if trimmed.startswith("http://") or trimmed.startswith("https://"):
        return trimmed
    try:
        data = json.loads(trimmed)
        found = _extract_url_from_json(data)
        if found:
            return found
    except Exception:
        pass
    m = re.search(r"https?://[^\s\"'<>\\]+", trimmed)
    return m.group(0) if m else ""

# =====================================================================

@router.get("/carrefour/stock")
async def get_carrefour_stock(user: Dict[str, Any] = Depends(get_current_user)):
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT value, price, COUNT(*) as count, MIN(id) as sample_id
            FROM stock
            WHERE brand = 'carr' AND is_sold = FALSE
            GROUP BY value, price
            ORDER BY value ASC
        """)
        return {
            "stock": [
                {
                    "value": float(r["value"] or 0),
                    "price": float(r["price"] or 0),
                    "count": int(r["count"] or 0),
                    "id": int(r["sample_id"])
                }
                for r in rows
            ]
        }

# =====================================================================

@router.post("/carrefour/buy")
async def buy_carrefour_card(
    payload: CarrefourBuyPayload,
    user: Dict[str, Any] = Depends(get_current_user)
):
    user_id = user["id"]
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        async with conn.transaction():
            if payload.stock_id:
                row = await conn.fetchrow("""
                    SELECT id, code, pin, value, price
                    FROM stock
                    WHERE id = $1 AND brand = 'carr' AND is_sold = FALSE
                    FOR UPDATE SKIP LOCKED
                """, payload.stock_id)
            elif payload.value is not None:
                row = await conn.fetchrow("""
                    SELECT id, code, pin, value, price
                    FROM stock
                    WHERE brand = 'carr' AND is_sold = FALSE AND value = $1
                    ORDER BY id ASC
                    LIMIT 1
                    FOR UPDATE SKIP LOCKED
                """, payload.value)
            else:
                row = await conn.fetchrow("""
                    SELECT id, code, pin, value, price
                    FROM stock
                    WHERE brand = 'carr' AND is_sold = FALSE
                    ORDER BY id ASC
                    LIMIT 1
                    FOR UPDATE SKIP LOCKED
                """)

            if not row:
                raise HTTPException(status_code=400, detail="Stock indisponible ou déjà vendu")

            price = float(row["price"] or 0)
            user_row = await conn.fetchrow("""
                SELECT balance FROM tma_users WHERE id = $1 FOR UPDATE
            """, user_id)

            if not user_row:
                raise HTTPException(status_code=404, detail="Utilisateur introuvable")

            current_balance = float(user_row["balance"] or 0)
            if current_balance < price:
                raise HTTPException(status_code=400, detail=f"Solde insuffisant ({current_balance:.2f} € requis: {price:.2f} €)")

            new_balance = current_balance - price
            await conn.execute("""
                UPDATE tma_users SET balance = $1, updated_at = NOW() WHERE id = $2
            """, new_balance, user_id)

            await conn.execute("""
                UPDATE stock SET is_sold = TRUE WHERE id = $1
            """, row["id"])

            await conn.execute("""
                INSERT INTO transactions (user_id, brand, code, pin, value, price, created_at)
                VALUES ($1, 'carr', $2, $3, $4, $5, NOW())
            """, user_id, row["code"], row["pin"], row["value"], price)

            return {
                "success": True,
                "item": {
                    "id": row["id"],
                    "code": row["code"],
                    "pin": row["pin"] or "0000",
                    "value": float(row["value"] or 0),
                    "price": price
                },
                "new_balance": new_balance
            }

# =====================================================================

@router.get("/carrefour/my-cards")
async def get_my_carrefour_cards(user: Dict[str, Any] = Depends(get_current_user)):
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT id, code, pin, value, price, created_at
            FROM transactions
            WHERE user_id = $1 AND brand = 'carr'
            ORDER BY created_at DESC
            LIMIT 50
        """, user["id"])
        return {
            "cards": [
                {
                    "id": r["id"],
                    "code": r["code"],
                    "pin": r["pin"] or "0000",
                    "value": float(r["value"] or 0),
                    "price": float(r["price"] or 0),
                    "created_at": r["created_at"].isoformat() if r["created_at"] else None
                }
                for r in rows
            ]
        }

# =====================================================================

@router.get("/iptv/prices")
async def get_iptv_public_prices(user: Dict[str, Any] = Depends(get_current_user)):
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow("SELECT prices, config FROM services WHERE slug = 'iptv'")
        prices = {}
        config = {}
        if row:
            if row["prices"]:
                raw_p = row["prices"]
                while isinstance(raw_p, str):
                    raw_p = json.loads(raw_p)
                prices = raw_p if isinstance(raw_p, dict) else {}
            if row["config"]:
                raw_c = row["config"]
                while isinstance(raw_c, str):
                    raw_c = json.loads(raw_c)
                config = raw_c if isinstance(raw_c, dict) else {}

        demo_on_raw = str(config.get("demo_enabled", "true")).lower()
        demo_enabled = demo_on_raw in ("true", "1", "on")
        try:
            demo_price = float(str(prices.get("price_demo") or prices.get("demo") or config.get("price_demo") or "1").replace(",", "."))
        except Exception:
            demo_price = 1.0

        p1 = float(str(prices.get("price_1m") or prices.get("m3u_1_mois") or 5).replace(",", "."))
        p3 = float(str(prices.get("price_3m") or prices.get("m3u_3_mois") or 10).replace(",", "."))
        p6 = float(str(prices.get("price_6m") or prices.get("m3u_6_mois") or 20).replace(",", "."))
        p12 = float(str(prices.get("price_12m") or prices.get("m3u_12_mois") or 35).replace(",", "."))

        return {
            "prices": {
                "1": p1,
                "3": p3,
                "6": p6,
                "12": p12,
                "demo": demo_price
            },
            "demo_enabled": demo_enabled,
            "host": config.get("host") or "http://cf.business-cloud-neo.com",
            "message_footer": config.get("message_footer", "")
        }

# =====================================================================

@router.post("/iptv/buy")
async def buy_iptv_subscription(
    payload: IptvBuyPayload,
    user: Dict[str, Any] = Depends(get_current_user)
):
    user_id = user["id"]
    if payload.sub not in (1, 3, 6, 12):
        raise HTTPException(status_code=400, detail="Durée d'abonnement non supportée (1, 3, 6, 12 mois)")

    pool = await get_db_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow("SELECT prices, config FROM services WHERE slug = 'iptv'")
        if not row:
            raise HTTPException(status_code=500, detail="Configuration IPTV non disponible")

        prices = {}
        config = {}
        if row["prices"]:
            raw_p = row["prices"]
            while isinstance(raw_p, str):
                raw_p = json.loads(raw_p)
            prices = raw_p if isinstance(raw_p, dict) else {}
        if row["config"]:
            raw_c = row["config"]
            while isinstance(raw_c, str):
                raw_c = json.loads(raw_c)
            config = raw_c if isinstance(raw_c, dict) else {}

        accounts = config.get("accounts", [])
        active_acc = next((a for a in accounts if a.get("active")), None)
        if not active_acc and accounts:
            active_acc = accounts[0]
        if not active_acc:
            raise HTTPException(status_code=500, detail="Aucun compte API IPTV configuré")

        api_url = (active_acc.get("api_url") or "").strip()
        api_key = (active_acc.get("api_key") or "").strip()
        pack = str(active_acc.get("pack") or "47013").strip()
        host = config.get("host") or "http://cf.business-cloud-neo.com"

        price_map = {
            1: float(str(prices.get("price_1m") or prices.get("m3u_1_mois") or 5).replace(",", ".")),
            3: float(str(prices.get("price_3m") or prices.get("m3u_3_mois") or 10).replace(",", ".")),
            6: float(str(prices.get("price_6m") or prices.get("m3u_6_mois") or 20).replace(",", ".")),
            12: float(str(prices.get("price_12m") or prices.get("m3u_12_mois") or 35).replace(",", "."))
        }
        price = price_map[payload.sub]

        user_row = await conn.fetchrow("SELECT balance FROM tma_users WHERE id = $1 FOR UPDATE", user_id)
        if not user_row:
            raise HTTPException(status_code=404, detail="Utilisateur introuvable")

        current_balance = float(user_row["balance"] or 0)
        if current_balance < price:
            raise HTTPException(status_code=400, detail=f"Solde insuffisant ({current_balance:.2f} € requis: {price:.2f} €)")

    sep = "&" if "?" in api_url else "?"
    note_txt = f"TMA_{user_id}_{payload.sub}m"
    target_api = f"{api_url}{sep}action=new&type=m3u&sub={payload.sub}&pack={pack}&country=FR&notes={urllib.parse.quote(note_txt)}&api_key={api_key}"

    try:
        if AsyncSession is not None:
            async with AsyncSession(impersonate="chrome146") as session:
                resp = await session.get(target_api, timeout=30)
                if resp.status_code != 200:
                    raise Exception(f"Erreur HTTP {resp.status_code} de l'API IPTV")
                text = resp.text
        else:
            async with httpx.AsyncClient(timeout=30) as session:
                resp = await session.get(target_api)
                if resp.status_code != 200:
                    raise Exception(f"Erreur HTTP {resp.status_code} de l'API IPTV")
                text = resp.text
        if "Invalid API Key" in text or "error" in text.lower():
            try:
                err_json = json.loads(text)
                if err_json.get("status") == "error":
                    raise Exception(err_json.get("message") or err_json.get("result") or "Erreur API IPTV")
            except json.JSONDecodeError:
                pass
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Échec de commande IPTV : {str(e)}")

    extracted_url = _extract_url_from_response(text)
    username = ""
    password = ""

    if extracted_url:
        try:
            parsed = urllib.parse.urlparse(extracted_url)
            qs = urllib.parse.parse_qs(parsed.query)
            username = qs.get("username", [None])[0] or qs.get("user", [None])[0] or qs.get("u", [None])[0] or ""
            password = qs.get("password", [None])[0] or qs.get("pass", [None])[0] or qs.get("p", [None])[0] or ""
            if not username or not password:
                parts = parsed.path.strip("/").split("/")
                if len(parts) >= 3:
                    if not username:
                        username = parts[-2]
                    if not password:
                        password = parts[-1].split(".")[0]
        except Exception:
            pass

    if not username:
        raise HTTPException(status_code=502, detail="Identifiants IPTV non retournés par l'API")

    async with pool.acquire() as conn:
        async with conn.transaction():
            user_row = await conn.fetchrow("SELECT balance FROM tma_users WHERE id = $1 FOR UPDATE", user_id)
            current_balance = float(user_row["balance"] or 0)
            if current_balance < price:
                raise HTTPException(status_code=400, detail="Solde insuffisant au moment du débit")

            new_balance = current_balance - price
            await conn.execute("UPDATE tma_users SET balance = $1, updated_at = NOW() WHERE id = $2", new_balance, user_id)
            await conn.execute("""
                INSERT INTO transactions (user_id, brand, code, pin, value, price, notes, created_at)
                VALUES ($1, 'iptv', $2, $3, $4, $5, $6, NOW())
            """, user_id, username or "Abonnement", password or "Actif", payload.sub, price, extracted_url or "")

    return {
        "success": True,
        "username": username,
        "password": password,
        "host": host,
        "url": extracted_url or f"{host}/get.php?username={username}&password={password}&type=m3u_plus&output=ts",
        "sub": payload.sub,
        "subscription_type": "m3u",
        "price": price,
        "new_balance": new_balance
    }

# =====================================================================

@router.post("/iptv/buy-demo")
async def buy_iptv_demo(user: Dict[str, Any] = Depends(get_current_user)):
    user_id = user["id"]
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow("SELECT prices, config FROM services WHERE slug = 'iptv'")
        if not row:
            raise HTTPException(status_code=500, detail="Configuration IPTV non disponible")

        prices = {}
        if row["prices"]:
            raw_p = row["prices"]
            while isinstance(raw_p, str):
                raw_p = json.loads(raw_p)
            prices = raw_p if isinstance(raw_p, dict) else {}

        config = {}
        if row["config"]:
            raw_c = row["config"]
            while isinstance(raw_c, str):
                raw_c = json.loads(raw_c)
            config = raw_c if isinstance(raw_c, dict) else {}

        demo_on_raw = str(config.get("demo_enabled", "true")).lower()
        if demo_on_raw not in ("true", "1", "on"):
            raise HTTPException(status_code=400, detail="Les tests démo IPTV sont actuellement désactivés")

        try:
            demo_price = float(str(prices.get("price_demo") or prices.get("demo") or config.get("price_demo") or "1").replace(",", "."))
        except Exception:
            demo_price = 1.0

        if demo_price > 0:
            user_row = await conn.fetchrow("SELECT balance FROM tma_users WHERE id = $1 FOR UPDATE", user_id)
            current_balance = float(user_row["balance"] or 0)
            if current_balance < demo_price:
                raise HTTPException(status_code=400, detail=f"Solde insuffisant ({current_balance:.2f} € requis: {demo_price:.2f} €)")

        accounts = config.get("accounts", [])
        active_acc = next((a for a in accounts if a.get("active")), None)
        if not active_acc and accounts:
            active_acc = accounts[0]
        if not active_acc:
            raise HTTPException(status_code=500, detail="Aucun compte API IPTV configuré")

        api_url = (active_acc.get("api_url") or "").strip()
        api_key = (active_acc.get("api_key") or "").strip()
        pack = str(active_acc.get("pack") or "47013").strip()
        host = config.get("host") or "http://cf.business-cloud-neo.com"

    sep = "&" if "?" in api_url else "?"
    note_txt = f"DEMO_{user_id}"
    target_api = f"{api_url}{sep}action=new&type=m3u&sub=0&pack={pack}&country=FR&notes={urllib.parse.quote(note_txt)}&api_key={api_key}"

    try:
        if AsyncSession is not None:
            async with AsyncSession(impersonate="chrome146") as session:
                resp = await session.get(target_api, timeout=30)
                text = resp.text
        else:
            async with httpx.AsyncClient(timeout=30) as session:
                resp = await session.get(target_api)
                text = resp.text
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Échec de génération de la démo : {str(e)}")

    extracted_url = _extract_url_from_response(text)
    username = ""
    password = ""
    if extracted_url:
        try:
            parsed = urllib.parse.urlparse(extracted_url)
            qs = urllib.parse.parse_qs(parsed.query)
            username = qs.get("username", [None])[0] or qs.get("user", [None])[0] or ""
            password = qs.get("password", [None])[0] or qs.get("pass", [None])[0] or ""
            if not username or not password:
                parts = parsed.path.strip("/").split("/")
                if len(parts) >= 3:
                    if not username:
                        username = parts[-2]
                    if not password:
                        password = parts[-1].split(".")[0]
        except Exception:
            pass

    async with pool.acquire() as conn:
        async with conn.transaction():
            if demo_price > 0:
                await conn.execute("UPDATE tma_users SET balance = balance - $1, updated_at = NOW() WHERE id = $2", demo_price, user_id)
            await conn.execute("""
                INSERT INTO transactions (user_id, brand, code, pin, value, price, notes, created_at)
                VALUES ($1, 'iptv', $2, $3, 0, $4, $5, NOW())
            """, user_id, username or "Demo", password or "24h", demo_price, extracted_url or "")
            new_bal_row = await conn.fetchval("SELECT balance FROM tma_users WHERE id = $1", user_id)

    return {
        "success": True,
        "username": username or "demo",
        "password": password or "demo",
        "host": host,
        "url": extracted_url or f"{host}/get.php?username={username}&password={password}&type=m3u_plus&output=ts",
        "duration": "24h",
        "price": demo_price,
        "new_balance": float(new_bal_row or 0)
    }

# =====================================================================

@router.get("/iptv/my-subscriptions")
async def get_my_iptv_subscriptions(user: Dict[str, Any] = Depends(get_current_user)):
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT id, code as username, pin as password, value as months, price, notes as url, created_at
            FROM transactions
            WHERE user_id = $1 AND brand = 'iptv'
            ORDER BY created_at DESC
            LIMIT 50
        """, user["id"])
        return {
            "subscriptions": [
                {
                    "id": r["id"],
                    "username": r["username"],
                    "password": r["password"],
                    "months": int(r["months"] or 0),
                    "price": float(r["price"] or 0),
                    "url": r["url"],
                    "created_at": r["created_at"].isoformat() if r["created_at"] else None
                }
                for r in rows
            ]
        }
