import asyncio
import json
import logging
import random
import re
import string
import time
import urllib.parse
from typing import Dict, Any, Optional, Tuple
from curl_cffi.requests import AsyncSession

# =====================================================================

logger = logging.getLogger(__name__)

STATIC_W = "083dfde075a4172d32dd8ea12465b5a03fe6dd2db225003a924d77f8f7e55405529c7e4aac9d870a3dfd4400150608afd506d52cb3d79f054a371f79259a693d0aeb2b0aab9a2361118257af86ce9b8682434ed049efc8982100c523081532dfb4ed88631f231be497c9a1af0dc4da708959c5fafd8a14b0bb63a7085619b32fbdd91fd6b79f66276f5e21825ec5d0713def7155fa7ef3c84c272a22d8f8ddf9247ed60518b1f3cd6ca3230bda3ada3da6767683f0dde8747b8ad5dd9af804a334af471ab1266efb417d2cbd0c56b659d2c2d235bb839f361eb57abaa3fb2a3a2eca07098fc899c174c10414b0cbe671215dc2aa4afe8f18001520c0ecd029efffc4911f220de26c1eb4e7a38e357ebe1f4d19676f900945ac16c039ed84290d07aa3f39d45152250cfdb8977d0ca855183fb7d3149b680316a1457c5eea74cbcd90afa13854de0e7ef9c9fbfb96e208c31681d87c8d485bde8734fd70cd7b835dcf50ed3db4d1554e3cf6aa9de35566c422b8639fdb81b22e48a95ee4d1f244445651033005d8c8e3496aae71e34f32036a3f047311cf32ad8c20b80b3b42d6d87a258780d753b9bd39c497f39eeed4369eeb684425c6eb4a800c5a549ffe5619b26b85248021813abd502fdca1c8f06f8b8e7808a01bca87efaa304e2a3605de66ccc3036772540404aacf18ade80e8fa0063aea3e403b0a99acd70efd8d7c0dfbc0b98fa0662de3bda234f78f6f93"

BOUQ_LIST = [
    "441","225","335","336","331","329","332","333","366","389","326","327","328","330","334","337","344","343","340","342","341","345","383","353",
    "351","359","346","347","348","349","356","371","357","352","369","354","355","358","360","361","362","363","364","372","365","368","370","376",
    "338","339","350","373","374","375","377","224","1","228","229","230","231","232","234","233","235","236","237","238","239","240","241","380",
    "242","245","413","384","246","247","248","421","390","392","393","394","395","422","424","412","399","400","401","414","415","257","443","261",
    "259","260","262","405","423","263","437","227","300","6","302","264","265","266","267","268","269","270","398","271","273","272","274","275",
    "276","277","382","278","279","280","281","282","283","284","285","286","287","288","381","289","290","291","292","293","294","295","298","297",
    "296","299","301","303","304","305","307","306","430","308","309","310","311","312","313","314","319","315","316","317","318","320","321","322",
    "323","324","325","5","178","183","185","186","221","425","200","191","192","198","187","189","190","193","194","220","196","219","197","199",
    "201","202","203","204","205","206","207","208","209","210","211","212","213","214","215","107","106","116","117","118","119","120","121","122",
    "108","109","110","112","111","184","222","113","114","115","123","124","442","125","126","127","176","128","129","131","132","133","407","179",
    "417","135","136","385","143","137","138","388","139","140","141","142","145","146","147","149","150","387","386","148","409","151","130","180",
    "144","153","152","378","379","154","155","181","156","223","157","158","159","160","161","428","162","163","182","164","165","166","167","168",
    "436","134","169","170","171","172","174","402","175","177","82","83","86","88","91","89","90","93","92","408","94","195","95","96","97",
    "216","98","99","100","101","102","103","104","105","3","9","79","8","10","406","11","429","63","42","12","13","14","15","21","17","18",
    "16","431","432","19","20","426","22","23","24","25","26","27","28","30","35","29","34","31","32","33","37","36","39","40","43","419",
    "74","73","72","71","70","69","68","67","44","438","433","46","47","434","435","48","49","41","420","78","77","76","75","45","54","81",
    "427","439","440","55","56","80","57","58","59","411","410","60","62","38","52","403","53","65","418","50","51","87","218","64","66","61",
    "217","416"
]

BASE_HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
    "cache-control": "max-age=0",
    "origin": "https://cms-4k.com",
    "referer": "https://cms-4k.com/login",
    "sec-ch-ua": '"Chromium";v="146", "Not)A;Brand";v="24", "Google Chrome";v="146"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"
}

_auth_headers: Optional[Dict[str, str]] = None
_auth_until: float = 0.0
_auth_lock = asyncio.Lock()
_stats_cache: Optional[Dict[str, str]] = None
_stats_until: float = 0.0

# =====================================================================

def reset_auth_cache() -> None:
    global _auth_headers, _auth_until, _stats_cache, _stats_until
    _auth_headers = None
    _auth_until = 0.0
    _stats_cache = None
    _stats_until = 0.0

def _html_session_active(html: str) -> bool:
    if not html:
        return False
    return "Dashboard | 4K" in html or "Remaining Demo" in html

def _extract_jsonp(text: str, cb: str) -> Dict[str, Any]:
    m = re.search(re.escape(cb) + r"\((.*)\)", text, re.DOTALL)
    if not m:
        raise Exception(f"Impossible d'extraire le JSON du callback {cb}")
    return json.loads(m.group(1))

# =====================================================================

async def authenticate_session(account: Dict[str, Any]) -> Dict[str, str]:
    global _auth_headers, _auth_until

    now = time.time()
    if _auth_headers and now < _auth_until:
        return dict(_auth_headers)

    async with _auth_lock:
        now = time.time()
        if _auth_headers and now < _auth_until:
            return dict(_auth_headers)

        if _auth_headers:
            try:
                async with AsyncSession(impersonate="chrome146", headers=_auth_headers, timeout=30) as s:
                    r = await s.get("https://cms-4k.com/addnew?t=lines")
                    if r.status_code == 200 and _html_session_active(r.text):
                        _auth_until = time.time() + 1200
                        return dict(_auth_headers)
            except Exception as e:
                logger.warning(f"Session panel expirée ou invalide: {e}")

        return await _login_panel_fresh(account)

# =====================================================================

async def _login_panel_fresh(account: Dict[str, Any]) -> Dict[str, str]:
    global _auth_headers, _auth_until

    username = str(account.get("username") or "").strip()
    password = str(account.get("password") or "").strip()
    if not username or not password:
        raise Exception("Identifiants panel IPTV manquants (username/password)")

    reset_auth_cache()

    async with AsyncSession(impersonate="chrome146", headers=BASE_HEADERS, timeout=45) as s:
        resp_login = await s.get("https://cms-4k.com/login")
        if resp_login.status_code != 200:
            raise Exception(f"Échec chargement login panel: {resp_login.status_code}")

        m_cap = re.search(r'(?:var\s+)?captchaId\s*=\s*["\']([^"\']+)["\']', resp_login.text)
        if not m_cap:
            raise Exception("CaptchaId introuvable sur la page de login panel")
        captcha_id = m_cap.group(1)

        stormersessid = s.cookies.get("STORMERSESSID")
        if not stormersessid:
            m_sc = re.search(r"STORMERSESSID=([^;]+)", resp_login.headers.get("set-cookie", ""))
            if m_sc:
                stormersessid = m_sc.group(1)
        if not stormersessid:
            raise Exception("Cookie STORMERSESSID introuvable")

        ts = int(time.time() * 1000)
        cb_load = f"geetest_{random.randint(0, 10000) + ts}"
        load_url = f"https://gcaptcha4.geetest.com/load?callback={urllib.parse.quote(cb_load)}&captcha_id={urllib.parse.quote(captcha_id)}&client_type=web&lang=eng"
        resp_load = await s.get(load_url)
        if resp_load.status_code != 200:
            raise Exception("Échec chargement Geetest load")

        load_json = _extract_jsonp(resp_load.text, cb_load)
        load_data = load_json.get("data", {})
        lot_number = str(load_data.get("lot_number") or "")
        payload = str(load_data.get("payload") or "")
        process_token = str(load_data.get("process_token") or "")

        cb_verify = f"geetest_{random.randint(0, 10000) + ts}"
        verify_url = (
            f"https://gcaptcha4.geetest.com/verify?callback={urllib.parse.quote(cb_verify)}"
            f"&captcha_id={urllib.parse.quote(captcha_id)}&client_type=web"
            f"&lot_number={urllib.parse.quote(lot_number)}&payload={urllib.parse.quote(payload)}"
            f"&process_token={urllib.parse.quote(process_token)}&payload_protocol=1&pt=1&w={urllib.parse.quote(STATIC_W)}"
        )
        resp_verify = await s.get(verify_url)
        if resp_verify.status_code != 200:
            raise Exception("Échec vérification Geetest")

        verify_json = _extract_jsonp(resp_verify.text, cb_verify)
        seccode = verify_json.get("data", {}).get("seccode", {})
        if not seccode:
            raise Exception("Seccode Geetest vide")

        form = {
            "uname": username,
            "upass": password,
            "lot_number": str(seccode.get("lot_number") or ""),
            "captcha_output": str(seccode.get("captcha_output") or ""),
            "pass_token": str(seccode.get("pass_token") or ""),
            "gen_time": str(seccode.get("gen_time") or ""),
            "btn-login": ""
        }

        post_headers = dict(BASE_HEADERS)
        post_headers["cookie"] = f"STORMERSESSID={stormersessid}"
        post_headers["content-type"] = "application/x-www-form-urlencoded"

        resp_post = await s.post("https://cms-4k.com/login.php", data=form, headers=post_headers)

        new_sess = s.cookies.get("STORMERSESSID") or stormersessid
        auth_headers = dict(BASE_HEADERS)
        auth_headers["cookie"] = f"STORMERSESSID={new_sess}"

        if resp_post.status_code in (301, 302, 303, 307):
            loc = resp_post.headers.get("location", "https://cms-4k.com/index")
            target_url = urllib.parse.urljoin("https://cms-4k.com/login.php", loc)
            resp_dash = await s.get(target_url, headers=auth_headers)
            if resp_dash.status_code != 200 or not _html_session_active(resp_dash.text):
                raise Exception("Échec de connexion au Dashboard après redirection")
        elif resp_post.status_code == 200:
            if not _html_session_active(resp_post.text):
                resp_dash = await s.get("https://cms-4k.com/addnew?t=lines", headers=auth_headers)
                if resp_dash.status_code != 200 or not _html_session_active(resp_dash.text):
                    raise Exception("Échec de validation de la session panel")
        else:
            raise Exception(f"Erreur HTTP login panel: {resp_post.status_code}")

        _auth_headers = auth_headers
        _auth_until = time.time() + 1200
        return dict(auth_headers)

# =====================================================================

async def get_reseller_panel_stats(account: Dict[str, Any], force_refresh: bool = False) -> Dict[str, str]:
    global _stats_cache, _stats_until

    now = time.time()
    if not force_refresh and _stats_cache and now < _stats_until:
        return dict(_stats_cache)

    auth = await authenticate_session(account)
    async with AsyncSession(impersonate="chrome146", headers=auth, timeout=30) as s:
        resp = await s.get("https://cms-4k.com/addnew?t=lines")
        if resp.status_code != 200:
            reset_auth_cache()
            auth = await authenticate_session(account)
            async with AsyncSession(impersonate="chrome146", headers=auth, timeout=30) as s2:
                resp = await s2.get("https://cms-4k.com/addnew?t=lines")
                if resp.status_code != 200:
                    raise Exception("Échec chargement page statistiques panel")

        html = resp.text
        m_demo = re.search(r"Remaining Demo</p>\s*<h5[^>]*>([^<]+)</h5>", html, re.IGNORECASE)
        m_bal = re.search(r"Balance:\s*<b[^>]*>(\d+)</b>", html, re.IGNORECASE)

        res = {
            "credits": m_bal.group(1) if m_bal else "Inconnu",
            "remaining_demos": m_demo.group(1).strip() if m_demo else "0"
        }
        _stats_cache = res
        _stats_until = time.time() + 120
        return res

# =====================================================================

async def _charger_table_lignes(auth_headers: Dict[str, str]) -> Tuple[Dict[str, Any], Dict[str, str]]:
    ts = int(time.time() * 1000)
    columns = [
        "id", "username", "password", "link_flag", "exp_date_flag", "package_flag",
        "reseller_notes", "owner", "status", "active", "speed_percent", "connections",
        "watching", "created_at", "country_code", ""
    ]

    params = [
        ("draw", "1"),
        ("order[0][column]", "0"),
        ("order[0][dir]", "desc"),
        ("start", "0"),
        ("length", "200"),
        ("search[value]", ""),
        ("search[regex]", "false"),
        ("id", "lines"),
        ("filter", "15"),
        ("state", "0"),
        ("reseller", ""),
        ("template", "0"),
        ("_", str(ts))
    ]

    for i, col in enumerate(columns):
        params.append((f"columns[{i}][data]", col))
        params.append((f"columns[{i}][searchable]", "true"))
        params.append((f"columns[{i}][orderable]", "true" if i == 4 else "false"))
        params.append((f"columns[{i}][search][value]", ""))
        params.append((f"columns[{i}][search][regex]", "false"))

    query_str = urllib.parse.urlencode(params)
    url = f"https://cms-4k.com/api_table.php?{query_str}"

    headers_table = dict(auth_headers)
    headers_table["accept"] = "application/json, text/javascript, */*; q=0.01"
    headers_table["x-requested-with"] = "XMLHttpRequest"
    headers_table["referer"] = "https://cms-4k.com/users?t=lines"

    async with AsyncSession(impersonate="chrome146", headers=headers_table, timeout=30) as s:
        r = await s.get(url)
        text = r.text.strip()
        if not text.startswith("{") and not text.startswith("["):
            raise Exception("Réponse non-JSON reçue depuis api_table.php")
        return json.loads(text), headers_table

# =====================================================================

async def generate_demo_iptv_line(account: Dict[str, Any], host: str, telegram_id: Any) -> Dict[str, str]:
    stats = await get_reseller_panel_stats(account, force_refresh=True)
    raw_rd = stats.get("remaining_demos", "")
    m_num = re.search(r"\d+", raw_rd)
    if m_num and int(m_num.group(0)) <= 0:
        raise Exception("Toutes les démos du jour ont déjà été achetées sur le panel fournisseur.")

    first_letter = random.choice(string.ascii_lowercase)
    rest_letters = "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
    gen_username = first_letter + rest_letters

    demo_payload = {
        "mac": gen_username,
        "sub_id": "8",
        "comment": f"Achat Démo Bot Telegram: {telegram_id}",
        "bouq_list": BOUQ_LIST,
        "type": "lines",
        "bouq_custom": "",
        "country": '["FR"]'
    }

    json_data = json.dumps(demo_payload)
    api_url = f"https://cms-4k.com/api.php?action=add_new&data={urllib.parse.quote(json_data)}"

    auth = await authenticate_session(account)

    async with AsyncSession(impersonate="chrome146", headers=auth, timeout=35) as s:
        resp = await s.get(api_url)
        text = resp.text.strip()
        is_json = text.startswith("{") or text.startswith("[")

        if not is_json:
            reset_auth_cache()
            auth = await authenticate_session(account)
            async with AsyncSession(impersonate="chrome146", headers=auth, timeout=35) as s2:
                resp = await s2.get(api_url)
                text = resp.text.strip()

        try:
            api_doc = json.loads(text)
        except Exception:
            raise Exception(f"Échec création démo IPTV sur le panel: {text}")

        if not api_doc.get("result"):
            raise Exception(f"Échec création démo IPTV sur le panel: {text}")

    table_json, headers_table = await _charger_table_lignes(auth)
    lines = table_json.get("data", [])
    created = None
    for item in lines:
        if isinstance(item, dict) and item.get("username") == gen_username:
            created = item
            break

    if not created:
        reset_auth_cache()
        auth = await authenticate_session(account)
        table_json, headers_table = await _charger_table_lignes(auth)
        for item in table_json.get("data", []):
            if isinstance(item, dict) and item.get("username") == gen_username:
                created = item
                break

    if not created:
        raise Exception("La ligne créée est introuvable dans la table du panel")

    encrypted_id = created.get("encrypted_id")
    if not encrypted_id:
        raise Exception("encrypted_id manquant pour la ligne démo")

    ts = int(time.time() * 1000)
    vpn_url = (
        f"https://cms-4k.com/options_list.php?reqvalue=copy_m3u&sub=&id={urllib.parse.quote(str(encrypted_id))}"
        f"&action=vpn&_={ts}"
    )

    async with AsyncSession(impersonate="chrome146", headers=headers_table, timeout=30) as s:
        resp_vpn = await s.get(vpn_url)
        if resp_vpn.status_code != 200:
            raise Exception("Échec de la récupération des détails de ligne démo")

        vpn_html = resp_vpn.text
        user_m = re.search(r"var username\s*=\s*'([^']*)'", vpn_html)
        pass_m = re.search(r"var password\s*=\s*'([^']*)'", vpn_html)

        if not user_m or not pass_m:
            raise Exception("Impossible d'extraire les identifiants finaux de la démo")

        extracted_user = user_m.group(1)
        extracted_pass = pass_m.group(1)

    server_base = (host or "").strip().rstrip("/")
    if not server_base:
        server_base = "http://cf.business-cloud-neo.com"

    return {
        "username": extracted_user,
        "password": extracted_pass,
        "host": server_base,
        "url": f"{server_base}/get.php?username={extracted_user}&password={extracted_pass}&type=m3u_plus&output=ts"
    }
