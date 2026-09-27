import ssl
import asyncpg
from typing import Optional
from app.config import settings

# =====================================================================

db_pool: Optional[asyncpg.Pool] = None

# =====================================================================

def _get_ssl_context() -> Optional[ssl.SSLContext]:
    if "railway" in settings.database_url or "proxy.rlwy.net" in settings.database_url or "aivencloud" in settings.database_url or "sslmode=require" in settings.database_url:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        return ctx
    return None

# =====================================================================

async def init_db() -> asyncpg.Pool:
    global db_pool
    if db_pool is None:
        ssl_ctx = _get_ssl_context()
        db_pool = await asyncpg.create_pool(
            settings.database_url,
            min_size=1,
            max_size=5,
            ssl=ssl_ctx,
            command_timeout=60
        )
        async with db_pool.acquire() as conn:
            await conn.execute("""
                CREATE EXTENSION IF NOT EXISTS "pgcrypto";

                CREATE TABLE IF NOT EXISTS stock (
                    id SERIAL PRIMARY KEY,
                    brand TEXT NOT NULL DEFAULT 'carr',
                    code TEXT NOT NULL,
                    pin TEXT DEFAULT '0000',
                    value NUMERIC DEFAULT 0,
                    price NUMERIC DEFAULT 0,
                    is_sold BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                );

                CREATE TABLE IF NOT EXISTS transactions (
                    id SERIAL PRIMARY KEY,
                    user_id BIGINT NOT NULL,
                    brand TEXT NOT NULL,
                    code TEXT,
                    pin TEXT,
                    value NUMERIC DEFAULT 0,
                    price NUMERIC NOT NULL,
                    notes TEXT,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                );

                CREATE TABLE IF NOT EXISTS tma_users (
                    id BIGINT PRIMARY KEY,
                    username VARCHAR(255),
                    first_name VARCHAR(255),
                    last_name VARCHAR(255),
                    balance NUMERIC DEFAULT 0.0,
                    is_banned BOOLEAN DEFAULT FALSE,
                    admin BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMPTZ DEFAULT NOW(),
                    updated_at TIMESTAMPTZ DEFAULT NOW()
                );

                ALTER TABLE tma_users ADD COLUMN IF NOT EXISTS balance NUMERIC DEFAULT 0.0;
                ALTER TABLE tma_users ADD COLUMN IF NOT EXISTS is_banned BOOLEAN DEFAULT FALSE;
                ALTER TABLE tma_users ADD COLUMN IF NOT EXISTS admin BOOLEAN DEFAULT FALSE;

                CREATE TABLE IF NOT EXISTS tma_payments (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    user_id BIGINT,
                    checkout_id VARCHAR(255),
                    checkout_reference VARCHAR(255),
                    amount NUMERIC DEFAULT 0.0,
                    currency VARCHAR(10) DEFAULT 'EUR',
                    status VARCHAR(50) DEFAULT 'PENDING',
                    sumup_payload JSONB,
                    created_at TIMESTAMPTZ DEFAULT NOW(),
                    updated_at TIMESTAMPTZ DEFAULT NOW()
                );

                CREATE TABLE IF NOT EXISTS tma_generations (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    user_id BIGINT,
                    category VARCHAR(100),
                    slug VARCHAR(100),
                    cost NUMERIC DEFAULT 0.0,
                    status VARCHAR(50) DEFAULT 'COMPLETED',
                    metadata JSONB,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                );

                CREATE TABLE IF NOT EXISTS settings (
                    id TEXT PRIMARY KEY,
                    general JSONB,
                    payments JSONB,
                    security JSONB
                );

                CREATE TABLE IF NOT EXISTS services (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    slug TEXT UNIQUE,
                    name TEXT,
                    description TEXT,
                    prices JSONB,
                    config JSONB,
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                );

                INSERT INTO settings (id, general, payments, security)
                VALUES (
                    'global',
                    '{"botName": "ChezRheyy", "maintenanceMode": false, "supportTelegram": "@RheyySupport"}',
                    '{"activeBank": "bank1", "oxapayApiKey": "", "paymentEnabled": true, "maxPaymentAmount": 60, "minPaymentAmount": 1, "expirationMinutes": 15, "maxPendingPaymentsPerClient": 1}',
                    '{"adminSlug": "espace-sec-x9k2m7", "apiSecretKey": "c8b9f1d0a83e47229b12480ad2e08e6f"}'
                )
                ON CONFLICT (id) DO NOTHING;
            """)
    return db_pool

# =====================================================================

async def get_db_pool() -> asyncpg.Pool:
    global db_pool
    if db_pool is None:
        return await init_db()
    return db_pool

# =====================================================================

async def close_db() -> None:
    global db_pool
    if db_pool is not None:
        await db_pool.close()
        db_pool = None

# =====================================================================

async def check_db_health() -> bool:
    try:
        pool = await get_db_pool()
        async with pool.acquire() as conn:
            val = await conn.fetchval("SELECT 1")
            return val == 1
    except Exception:
        return False
