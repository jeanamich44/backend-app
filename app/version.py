import os
import subprocess
from datetime import datetime, timezone
from typing import Dict, Any

# =====================================================================

STARTUP_TIME = datetime.now(timezone.utc).isoformat()

# =====================================================================

def get_git_info() -> Dict[str, Any]:
    commit = os.getenv("RENDER_GIT_COMMIT", "").strip()
    commit_date = ""
    try:
        out = subprocess.check_output(
            ["git", "log", "-1", "--format=%h|%cI"],
            stderr=subprocess.DEVNULL,
            timeout=2
        ).decode("utf-8").strip()
        if "|" in out:
            h, d = out.split("|", 1)
            if not commit:
                commit = h
            commit_date = d
    except Exception:
        pass

    if commit and len(commit) > 7:
        commit = commit[:7]

    return {
        "commit": commit or "unknown",
        "commit_date": commit_date,
        "boot_time": STARTUP_TIME
    }
