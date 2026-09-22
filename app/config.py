import os
import sys
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

# =====================================================================

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# =====================================================================

def _require_env(key: str) -> str:
    val = os.getenv(key)
    if not val or not val.strip():
        print(f"[CONFIG_ERROR] Variable d'environnement '{key}' requise et absente", flush=True)
        sys.exit(1)
    return val.strip()

# =====================================================================

@dataclass(frozen=True)
class Settings:
    database_url: str = _require_env("DATABASE_URL")
    telegram_bot_token: str = _require_env("TELEGRAM_BOT_TOKEN")
    frontend_url: str = os.getenv("FRONTEND_URL", "")
    internal_api_secret: str = os.getenv("INTERNAL_API_SECRET", "")
    port: int = int(os.getenv("PORT", "8000"))

# =====================================================================

settings = Settings()
