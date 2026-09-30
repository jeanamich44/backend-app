import json
import logging
import os
import sys
from pathlib import Path
from typing import Any
from dotenv import load_dotenv

# =====================================================================

logger = logging.getLogger(__name__)

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# =====================================================================

def _require_env(key: str) -> str:
    val = os.getenv(key)
    if not val or not val.strip():
        logger.critical(f"[FATAL CONFIG] Variable d'environnement '{key}' requise et absente")
        print(f"[FATAL CONFIG] Variable d'environnement '{key}' requise et absente", flush=True)
        sys.exit(1)
    return val.strip()

# =====================================================================

class Settings:
    def __init__(self):
        self.database_url: str = _require_env("DATABASE_URL")
        self.port: int = int(os.getenv("PORT", "8000"))
        self.frontend_url: str = ""
        self.telegram_bot_token: str = ""
        self.internal_api_secret: str = ""
        self.bot_name: str = "ChezRheyy"
        self.support_telegram: str = ""
        self.channel_telegram: str = ""
        self.backend_url: str = ""

    async def load_from_db(self, pool_or_conn: Any) -> None:
        try:
            row = await pool_or_conn.fetchrow("SELECT general, security FROM settings WHERE id = 'global'")
            if not row:
                msg = "[FATAL CONFIG] Ligne 'global' introuvable dans la table settings en BDD"
                logger.critical(msg)
                print(msg, flush=True)
                sys.exit(1)

            general = row["general"]
            while isinstance(general, str):
                general = json.loads(general)
            if not isinstance(general, dict):
                general = {}

            security = row["security"]
            while isinstance(security, str):
                security = json.loads(security)
            if not isinstance(security, dict):
                security = {}

            f_url = general.get("frontendUrl")
            tg_token = general.get("telegramBotToken")
            api_sec = security.get("apiSecretKey") or security.get("internalApiSecret")

            required = {
                "FRONTEND_URL": f_url,
                "TELEGRAM_BOT_TOKEN": tg_token,
                "INTERNAL_API_SECRET": api_sec
            }

            for name, val in required.items():
                if not val or not str(val).strip():
                    msg = f"[FATAL CONFIG ERROR] Variable dynamique obligatoire '{name}' absente ou vide en BDD (table settings)"
                    logger.critical(msg)
                    print(msg, flush=True)
                    sys.exit(1)

            self.frontend_url = str(f_url).strip()
            self.telegram_bot_token = str(tg_token).strip()
            self.internal_api_secret = str(api_sec).strip()
            self.bot_name = str(general.get("botName") or "ChezRheyy").strip()
            self.support_telegram = str(general.get("supportTelegram") or "").strip()
            self.channel_telegram = str(general.get("channelTelegram") or "").strip()
            self.backend_url = str(general.get("backendUrl") or "").strip()
            logger.info("Configuration dynamique chargée avec succès depuis la BDD.")
        except SystemExit:
            raise
        except Exception as e:
            msg = f"[FATAL CONFIG ERROR] Échec de récupération de la configuration en BDD : {e}"
            logger.critical(msg)
            print(msg, flush=True)
            sys.exit(1)

# =====================================================================

settings = Settings()
