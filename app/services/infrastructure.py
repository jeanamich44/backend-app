import os
import sys
import time
import shutil
import ctypes
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from app.db import get_db_pool

# =====================================================================

_START_TIME = time.time()
_REQ_COUNT = 0
_STATUS_2XX = 0
_STATUS_4XX = 0
_STATUS_5XX = 0
_LATENCY_SUM_MS = 0.0
_LAST_CPU_SAMPLE: Optional[Dict[str, float]] = None
_LAST_NET_SAMPLE: Optional[Dict[str, Any]] = None

# =====================================================================

def record_http_request(status_code: int, duration_ms: float) -> None:
    global _REQ_COUNT, _STATUS_2XX, _STATUS_4XX, _STATUS_5XX, _LATENCY_SUM_MS
    _REQ_COUNT += 1
    _LATENCY_SUM_MS += max(0.0, duration_ms)
    if 200 <= status_code < 300:
        _STATUS_2XX += 1
    elif 400 <= status_code < 500:
        _STATUS_4XX += 1
    elif status_code >= 500:
        _STATUS_5XX += 1

# =====================================================================

def get_error_counts() -> int:
    return _STATUS_4XX + _STATUS_5XX

# =====================================================================

def _format_duration(seconds: float) -> str:
    secs = int(seconds)
    days = secs // 86400
    secs %= 86400
    hours = secs // 3600
    secs %= 3600
    mins = secs // 60
    secs %= 60
    parts = []
    if days > 0:
        parts.append(f"{days}j")
    if hours > 0 or days > 0:
        parts.append(f"{hours}h")
    parts.append(f"{mins}m")
    parts.append(f"{secs}s")
    return " ".join(parts)

# =====================================================================

def _read_container_cpu_time() -> Optional[float]:
    cgroup_v2_cpu_stat = "/sys/fs/cgroup/cpu.stat"
    if os.path.exists(cgroup_v2_cpu_stat):
        try:
            with open(cgroup_v2_cpu_stat, "r") as f:
                for line in f:
                    if line.startswith("usage_usec"):
                        usec = float(line.split()[1])
                        return usec / 1000000.0
        except Exception:
            pass

    for p in (
        "/sys/fs/cgroup/cpuacct/cpuacct.usage",
        "/sys/fs/cgroup/cpu,cpuacct/cpuacct.usage",
        "/sys/fs/cgroup/cpu/cpuacct.usage"
    ):
        if os.path.exists(p):
            try:
                with open(p, "r") as f:
                    nsec = float(f.read().strip())
                    return nsec / 1000000000.0
            except Exception:
                pass

    if os.path.exists("/proc/self/stat"):
        try:
            with open("/proc/self/stat", "r") as f:
                fields = f.read().split()
                utime = float(fields[13])
                stime = float(fields[14])
                clk_tck = 100.0
                if hasattr(os, "sysconf") and "SC_CLK_TCK" in os.sysconf_names:
                    clk_tck = float(os.sysconf("SC_CLK_TCK"))
                return (utime + stime) / clk_tck
        except Exception:
            pass

    return None

# =====================================================================

def _get_container_allocated_cores() -> float:
    cgroup_v2_cpu_max = "/sys/fs/cgroup/cpu.max"
    if os.path.exists(cgroup_v2_cpu_max):
        try:
            with open(cgroup_v2_cpu_max, "r") as f:
                parts = f.read().strip().split()
                if len(parts) >= 2 and parts[0] != "max":
                    quota = float(parts[0])
                    period = float(parts[1])
                    if period > 0:
                        return round(quota / period, 2)
        except Exception:
            pass

    quota_p = "/sys/fs/cgroup/cpu/cpu.cfs_quota_us"
    period_p = "/sys/fs/cgroup/cpu/cpu.cfs_period_us"
    if os.path.exists(quota_p) and os.path.exists(period_p):
        try:
            with open(quota_p, "r") as f:
                quota = float(f.read().strip())
            with open(period_p, "r") as f:
                period = float(f.read().strip())
            if quota > 0 and period > 0:
                return round(quota / period, 2)
        except Exception:
            pass

    return 1.0

# =====================================================================

def _get_cpu_info() -> Dict[str, Any]:
    global _LAST_CPU_SAMPLE
    allocated_cores = _get_container_allocated_cores()
    host_cores = os.cpu_count() or 1
    cpu_percent = 0.0
    now = time.time()
    
    load_avg = None
    if hasattr(os, "getloadavg"):
        try:
            load_avg = [round(x, 2) for x in os.getloadavg()]
        except Exception:
            load_avg = None

    container_cpu_time = _read_container_cpu_time()

    if container_cpu_time is not None:
        if _LAST_CPU_SAMPLE and "cpu_time" in _LAST_CPU_SAMPLE:
            d_cpu = container_cpu_time - _LAST_CPU_SAMPLE["cpu_time"]
            d_time = now - _LAST_CPU_SAMPLE["time"]
            if d_time > 0 and d_cpu >= 0:
                cpu_percent = round((d_cpu / (d_time * allocated_cores)) * 100.0, 1)
        _LAST_CPU_SAMPLE = {"cpu_time": container_cpu_time, "time": now}
    else:
        proc_time = time.process_time()
        if _LAST_CPU_SAMPLE and "proc_time" in _LAST_CPU_SAMPLE:
            d_proc = proc_time - _LAST_CPU_SAMPLE["proc_time"]
            d_time = now - _LAST_CPU_SAMPLE["time"]
            if d_time > 0 and d_proc >= 0:
                cpu_percent = round((d_proc / (d_time * allocated_cores)) * 100.0, 1)
        _LAST_CPU_SAMPLE = {"proc_time": proc_time, "time": now}

    cpu_percent = max(0.0, min(100.0, cpu_percent))
    return {
        "cores": allocated_cores,
        "host_cores": host_cores,
        "percent": cpu_percent,
        "load_avg": load_avg
    }

# =====================================================================

def _get_memory_info() -> Dict[str, Any]:
    total_mb = 512.0
    used_mb = 0.0
    free_mb = 512.0
    percent = 0.0
    process_rss_mb = 0.0
    cgroup_limit_mb = None
    cgroup_used_mb = None

    if os.path.exists("/proc/self/status"):
        try:
            with open("/proc/self/status", "r") as f:
                for line in f:
                    if line.startswith("VmRSS:"):
                        val_kb = float(line.split()[1])
                        process_rss_mb = round(val_kb / 1024.0, 1)
                        break
        except Exception:
            pass

    cgroup_v2_usage = "/sys/fs/cgroup/memory.current"
    cgroup_v2_max = "/sys/fs/cgroup/memory.max"
    cgroup_v1_usage = "/sys/fs/cgroup/memory/memory.usage_in_bytes"
    cgroup_v1_max = "/sys/fs/cgroup/memory/memory.limit_in_bytes"

    if os.path.exists(cgroup_v2_usage):
        try:
            with open(cgroup_v2_usage, "r") as f:
                cgroup_used_mb = round(float(f.read().strip()) / (1024.0 * 1024.0), 1)
            if os.path.exists(cgroup_v2_max):
                with open(cgroup_v2_max, "r") as f:
                    content = f.read().strip()
                    if content != "max":
                        lim = round(float(content) / (1024.0 * 1024.0), 1)
                        if lim < 32768.0:
                            cgroup_limit_mb = lim
        except Exception:
            pass
    elif os.path.exists(cgroup_v1_usage):
        try:
            with open(cgroup_v1_usage, "r") as f:
                cgroup_used_mb = round(float(f.read().strip()) / (1024.0 * 1024.0), 1)
            if os.path.exists(cgroup_v1_max):
                with open(cgroup_v1_max, "r") as f:
                    limit_raw = float(f.read().strip())
                    if limit_raw < 1e14:
                        lim = round(limit_raw / (1024.0 * 1024.0), 1)
                        if lim < 32768.0:
                            cgroup_limit_mb = lim
        except Exception:
            pass

    if os.name == "nt":
        try:
            class MEMORYSTATUSEX(ctypes.Structure):
                _fields_ = [
                    ("dwLength", ctypes.c_ulong),
                    ("dwMemoryLoad", ctypes.c_ulong),
                    ("ullTotalPhys", ctypes.c_ulonglong),
                    ("ullAvailPhys", ctypes.c_ulonglong),
                    ("ullTotalPageFile", ctypes.c_ulonglong),
                    ("ullAvailPageFile", ctypes.c_ulonglong),
                    ("ullTotalVirtual", ctypes.c_ulonglong),
                    ("ullAvailVirtual", ctypes.c_ulonglong),
                    ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
                ]
            stat = MEMORYSTATUSEX()
            stat.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
            total_mb = round(stat.ullTotalPhys / (1024.0 * 1024.0), 1)
            free_mb = round(stat.ullAvailPhys / (1024.0 * 1024.0), 1)
            used_mb = round(max(0.0, total_mb - free_mb), 1)
            percent = round((used_mb / total_mb) * 100.0, 1) if total_mb > 0 else 0.0
        except Exception:
            pass

    final_total_mb = cgroup_limit_mb or 512.0
    final_used_mb = round(max(cgroup_used_mb or 0.0, process_rss_mb), 1)
    if os.name == "nt" and not cgroup_used_mb and not process_rss_mb:
        final_used_mb = used_mb
        final_total_mb = total_mb

    final_free_mb = round(max(0.0, final_total_mb - final_used_mb), 1)
    percent = round((final_used_mb / final_total_mb) * 100.0, 1) if final_total_mb > 0 else 0.0

    return {
        "total_mb": final_total_mb,
        "used_mb": final_used_mb,
        "free_mb": final_free_mb,
        "percent": percent,
        "process_rss_mb": process_rss_mb,
        "cgroup_limit_mb": cgroup_limit_mb or 512.0,
        "cgroup_used_mb": cgroup_used_mb or final_used_mb
    }

# =====================================================================

def _get_disk_info() -> Dict[str, Any]:
    path = "/" if os.name != "nt" else "."
    usage = shutil.disk_usage(path)
    total_gb = round(usage.total / (1024.0**3), 2)
    used_gb = round(usage.used / (1024.0**3), 2)
    free_gb = round(usage.free / (1024.0**3), 2)
    pct = round((usage.used / usage.total) * 100.0, 1) if usage.total > 0 else 0.0
    return {
        "total_gb": total_gb,
        "used_gb": used_gb,
        "free_gb": free_gb,
        "percent": pct
    }

# =====================================================================

def _get_network_info() -> Dict[str, Any]:
    global _LAST_NET_SAMPLE
    rx_bytes = 0
    tx_bytes = 0
    rx_packets = 0
    tx_packets = 0
    now = time.time()
    ingress_rate_kbps = 0.0
    egress_rate_kbps = 0.0

    if os.path.exists("/proc/net/dev"):
        try:
            with open("/proc/net/dev", "r") as f:
                lines = f.readlines()[2:]
            for line in lines:
                parts = line.split(":")
                if len(parts) == 2:
                    iface = parts[0].strip()
                    if iface == "lo":
                        continue
                    vals = [int(x) for x in parts[1].split()]
                    if len(vals) >= 9:
                        rx_bytes += vals[0]
                        rx_packets += vals[1]
                        tx_bytes += vals[8]
                        tx_packets += vals[9]
        except Exception:
            pass

    if _LAST_NET_SAMPLE:
        d_time = now - _LAST_NET_SAMPLE["time"]
        if d_time > 0:
            d_rx = rx_bytes - _LAST_NET_SAMPLE["rx_bytes"]
            d_tx = tx_bytes - _LAST_NET_SAMPLE["tx_bytes"]
            ingress_rate_kbps = round(max(0.0, d_rx) / 1024.0 / d_time, 2)
            egress_rate_kbps = round(max(0.0, d_tx) / 1024.0 / d_time, 2)

    _LAST_NET_SAMPLE = {
        "time": now,
        "rx_bytes": rx_bytes,
        "tx_bytes": tx_bytes
    }

    return {
        "egress_bytes": tx_bytes,
        "egress_mb": round(tx_bytes / (1024.0 * 1024.0), 2),
        "egress_rate_kbps": egress_rate_kbps,
        "ingress_bytes": rx_bytes,
        "ingress_mb": round(rx_bytes / (1024.0 * 1024.0), 2),
        "ingress_rate_kbps": ingress_rate_kbps,
        "packets_sent": tx_packets,
        "packets_recv": rx_packets
    }

# =====================================================================

def get_render_metrics() -> Dict[str, Any]:
    uptime_sec = round(time.time() - _START_TIME)
    avg_latency = round(_LATENCY_SUM_MS / _REQ_COUNT, 2) if _REQ_COUNT > 0 else 0.0
    rps = round(_REQ_COUNT / max(1.0, uptime_sec), 2)

    return {
        "status": "online",
        "cpu": _get_cpu_info(),
        "memory": _get_memory_info(),
        "disk": _get_disk_info(),
        "network": _get_network_info(),
        "app": {
            "uptime_seconds": uptime_sec,
            "uptime_formatted": _format_duration(uptime_sec),
            "total_requests": _REQ_COUNT,
            "rps": rps,
            "avg_latency_ms": avg_latency,
            "status_2xx": _STATUS_2XX,
            "status_4xx": _STATUS_4XX,
            "status_5xx": _STATUS_5XX,
            "service_id": os.getenv("RENDER_SERVICE_ID", "local-dev"),
            "instance_id": os.getenv("RENDER_INSTANCE_ID", "inst-1"),
            "service_name": os.getenv("RENDER_SERVICE_NAME", "backend-app"),
            "commit": os.getenv("RENDER_GIT_COMMIT", "local-head")
        }
    }

# =====================================================================

async def get_aiven_metrics() -> Dict[str, Any]:
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        db_size_bytes = await conn.fetchval("SELECT pg_database_size(current_database())")
        db_size_pretty = await conn.fetchval("SELECT pg_size_pretty(pg_database_size(current_database()))")
        max_conn = await conn.fetchval("SELECT setting::int FROM pg_settings WHERE name = 'max_connections'")
        shared_buf = await conn.fetchval("SELECT setting FROM pg_settings WHERE name = 'shared_buffers'")
        work_mem = await conn.fetchval("SELECT setting FROM pg_settings WHERE name = 'work_mem'")
        maint_work_mem = await conn.fetchval("SELECT setting FROM pg_settings WHERE name = 'maintenance_work_mem'")
        pg_version = await conn.fetchval("SHOW server_version")

        stat_db = await conn.fetchrow("""
            SELECT numbackends, xact_commit, xact_rollback, blks_read, blks_hit,
                   tup_returned, tup_fetched, tup_inserted, tup_updated, tup_deleted,
                   conflicts, temp_files, temp_bytes, deadlocks, stats_reset
            FROM pg_stat_database
            WHERE datname = current_database()
        """)

        activity_rows = await conn.fetch("""
            SELECT state, count(*) as count
            FROM pg_stat_activity
            WHERE datname = current_database()
            GROUP BY state
        """)

        top_tables = await conn.fetch("""
            SELECT relname AS table_name,
                   pg_total_relation_size(relid) AS total_bytes,
                   pg_size_pretty(pg_total_relation_size(relid)) AS pretty_size,
                   n_live_tup AS live_rows
            FROM pg_stat_user_tables
            ORDER BY pg_total_relation_size(relid) DESC
            LIMIT 6
        """)

    activity_map: Dict[str, int] = {}
    for row in activity_rows:
        state_key = row["state"] or "idle"
        activity_map[state_key] = row["count"]

    curr_conn = stat_db["numbackends"] or 0
    max_c = max_conn or 20
    saturation_pct = round((curr_conn / max_c) * 100.0, 1)

    blks_hit = stat_db["blks_hit"] or 0
    blks_read = stat_db["blks_read"] or 0
    blks_total = blks_hit + blks_read
    cache_hit_ratio = round((blks_hit / blks_total) * 100.0, 2) if blks_total > 0 else 100.0

    xact_commit = stat_db["xact_commit"] or 0
    xact_rollback = stat_db["xact_rollback"] or 0
    xact_total = xact_commit + xact_rollback
    commit_ratio = round((xact_commit / xact_total) * 100.0, 2) if xact_total > 0 else 100.0

    tables_data = []
    for t in top_tables:
        tables_data.append({
            "name": t["table_name"],
            "bytes": t["total_bytes"],
            "pretty_size": t["pretty_size"],
            "rows": t["live_rows"]
        })

    stats_reset_val = stat_db["stats_reset"]
    stats_reset_str = stats_reset_val.isoformat() if hasattr(stats_reset_val, "isoformat") else str(stats_reset_val)

    return {
        "status": "online",
        "cpu_and_activity": {
            "max_connections": max_c,
            "current_connections": curr_conn,
            "connection_saturation_percent": saturation_pct,
            "active_queries": activity_map.get("active", 0),
            "idle_connections": activity_map.get("idle", 0),
            "idle_in_transaction": activity_map.get("idle in transaction", 0),
            "xact_commit": xact_commit,
            "xact_rollback": xact_rollback,
            "commit_ratio_percent": commit_ratio
        },
        "memory_cache": {
            "cache_hit_ratio_percent": cache_hit_ratio,
            "blks_hit": blks_hit,
            "blks_read": blks_read,
            "shared_buffers": shared_buf,
            "work_mem": work_mem,
            "maintenance_work_mem": maint_work_mem
        },
        "storage_volume": {
            "total_size_bytes": db_size_bytes,
            "total_size_pretty": db_size_pretty,
            "temp_bytes": stat_db["temp_bytes"] or 0,
            "temp_files": stat_db["temp_files"] or 0,
            "top_tables": tables_data
        },
        "networking_io": {
            "tup_returned": stat_db["tup_returned"] or 0,
            "tup_fetched": stat_db["tup_fetched"] or 0,
            "tup_inserted": stat_db["tup_inserted"] or 0,
            "tup_updated": stat_db["tup_updated"] or 0,
            "tup_deleted": stat_db["tup_deleted"] or 0,
            "conflicts": stat_db["conflicts"] or 0,
            "deadlocks": stat_db["deadlocks"] or 0,
            "server_version": pg_version,
            "stats_reset": stats_reset_str
        }
    }

# =====================================================================

async def get_all_infrastructure_metrics() -> Dict[str, Any]:
    render_data = get_render_metrics()
    aiven_data = await get_aiven_metrics()
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "render": render_data,
        "aiven": aiven_data
    }
