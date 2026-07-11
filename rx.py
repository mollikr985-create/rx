#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║       NEXUS MULTI-TOOL KIT v3.2                              ║
║       + Flexible Bot Hosting (any Python code)               ║
║       + Web Hosting (HTML → public URL via cloudflared)      ║
║       + Temp Mail                                             ║
║       Author: Mavis                                          ║
╚══════════════════════════════════════════════════════════════╝

Run:  python3 nexus_multitool_v3.2.py

Data lives in:
  ~/.nexus/bots/         — bot scripts
  ~/.nexus/logs/         — bot + site logs
  ~/.nexus/sites/<name>/ — hosted site files (index.html + assets)
  ~/.nexus/bots.json     — bot registry
  ~/.nexus/sites.json    — site registry
"""

import os
import sys
import re
import shutil
import time
import json
import random
import string
import socket
import hashlib
import base64
import uuid
import subprocess
import urllib.request
import urllib.error
import urllib.parse
import http.server
import socketserver
from datetime import datetime

# ────────────────────────── ANSI COLORS ──────────────────────────
R  = "\033[91m"
G  = "\033[92m"
Y  = "\033[93m"
B  = "\033[94m"
M  = "\033[95m"
C  = "\033[96m"
W  = "\033[97m"
GR = "\033[90m"
BD = "\033[1m"
N  = "\033[0m"

# ────────────────────────── BANNER ──────────────────────────────
BANNER_LINES = [
    "  ███╗   ███╗██╗   ██╗██╗  ██╗████████╗██╗",
    "  ████╗ ████║██║   ██║██║  ██║╚══██╔══╝██║",
    "  ██╔████╔██║██║   ██║███████║   ██║   ██║",
    "  ██║╚██╔╝██║██║   ██║██╔══██║   ██║   ██║",
    "  ██║ ╚═╝ ██║╚██████╔╝██║  ██║   ██║   ██║",
    "  ╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝",
]

# ────────────────────────── HELPERS ─────────────────────────────
def pause(seconds=1):
    try:
        time.sleep(seconds)
    except KeyboardInterrupt:
        raise

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def line(c="─", n=60):
    print(GR + c * n + N)

def header():
    clear()
    for ln in BANNER_LINES:
        print(C + ln + N)
    line()
    print(Y + "  ☀ NEXUS MULTI-TOOL KIT v3.2 ☀" + N)
    print(W + "  + Bot Hosting + Web Hosting + Temp Mail" + N)
    line()
    print(G + "  Author  : " + W + "Mavis")
    print(G + "  Status  : " + G + BD + "Online & Ready" + N)
    line()

def box(title, items, active=0, active_label="Active"):
    width = 58
    print(C + "  ┌" + "─" * width + "┐")
    print(C + "  │ " + Y + BD + title.center(width - 2) + N + C + " │")
    if active_label:
        line_text = f"{active_label}: {active}"
        print(C + "  │ " + W + line_text.ljust(width - 2) + C + " │")
    print(C + "  ├" + "─" * width + "┤")
    for it in items:
        print(C + "  │ " + W + it.ljust(width - 2) + C + " │")
    print(C + "  └" + "─" * width + "┘" + N)

def format_uptime(seconds):
    s = int(seconds)
    if s < 60:
        return f"{s}s"
    if s < 3600:
        return f"{s//60}m{s%60}s"
    if s < 86400:
        return f"{s//3600}h{(s%3600)//60}m"
    return f"{s//86400}d{(s%86400)//3600}h"

def find_free_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    p = s.getsockname()[1]
    s.close()
    return p

def read_multiline(marker="###END###"):
    print(Y + f"  Paste below. Finish with a line containing only: {marker}" + N)
    print()
    lines = []
    try:
        while True:
            line = input()
            if line.strip() == marker:
                break
            lines.append(line)
    except EOFError:
        print(GR + "  (Ctrl+D received — ending input)" + N)
    return "\n".join(lines)

# ────────────────────────── TOOL 1-10 (compact) ─────────────────
def tool_check_system():
    header()
    print(C + "  ▶ System & Public IP\n" + N)
    try: host = socket.gethostname()
    except: host = "?"
    local = "N/A"
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(3); s.connect(("8.8.8.8", 80))
        local = s.getsockname()[0]; s.close()
    except: pass
    pub = "N/A"
    try:
        pub = urllib.request.urlopen("https://api.ipify.org", timeout=5).read().decode().strip()
    except: pass
    print(G + "  Hostname : " + W + host)
    print(G + "  Local IP : " + W + local)
    print(G + "  Public IP: " + W + pub)
    print(G + "  Platform : " + W + sys.platform)
    print(G + "  Python   : " + W + sys.version.split()[0])
    print(G + "  Termux   : " + W + ("Yes" if os.path.exists("/data/data/com.termux") else "No"))
    pause(3)

def tool_website_status():
    header()
    print(C + "  ▶ Website Status Checker\n" + N)
    url = input(Y + "  URL: " + N).strip()
    if not url: return
    if not url.startswith("http"): url = "https://" + url
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        t0 = time.time()
        r = urllib.request.urlopen(req, timeout=10)
        ms = (time.time() - t0) * 1000
        print(G + f"\n  ✔ {r.status} {r.reason}  •  {ms:.1f} ms" + N)
        print(G + "  ✔ Server: " + W + r.headers.get("Server", "N/A"))
    except urllib.error.HTTPError as e:
        print(R + f"  ✘ HTTP {e.code}" + N)
    except Exception as e:
        print(R + f"  ✘ {e}" + N)
    pause(3)

def tool_password_gen():
    header()
    print(C + "  ▶ Password Generator\n" + N)
    try: length = int(input(Y + "  Length (8-128): " + N) or "20")
    except: length = 20
    length = max(8, min(128, length))
    pool = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
    pw = "".join(random.SystemRandom().choice(pool) for _ in range(length))
    print(G + f"\n  Password: " + C + pw + N)
    pause(3)

def tool_ip_lookup():
    header()
    print(C + "  ▶ IP Geolocation\n" + N)
    ip = input(Y + "  IP (blank = public): " + N).strip()
    try:
        data = json.loads(urllib.request.urlopen(f"http://ip-api.com/json/{ip}", timeout=10).read().decode())
        if data.get("status") == "success":
            for k in ["query", "country", "regionName", "city", "zip", "isp", "org"]:
                print(G + f"  {k:<12}: " + W + str(data.get(k, "N/A")))
        else:
            print(R + f"  ✘ {data.get('message', 'failed')}" + N)
    except Exception as e:
        print(R + f"  ✘ {e}" + N)
    pause(3)

def tool_dns_lookup():
    header()
    print(C + "  ▶ DNS Lookup\n" + N)
    domain = input(Y + "  Domain: " + N).strip()
    if not domain: return
    for t in ["A", "MX", "NS", "TXT", "CNAME"]:
        try:
            data = json.loads(urllib.request.urlopen(
                f"https://dns.google/resolve?name={domain}&type={t}", timeout=10
            ).read().decode())
            for a in data.get("Answer", [])[:3]:
                print(G + f"  {t:<6} " + W + f"{a.get('data','')}" + N)
        except: pass
    pause(3)

def tool_hash_gen():
    header()
    print(C + "  ▶ Hash Generator\n" + N)
    text = input(Y + "  Text: " + N)
    e = text.encode("utf-8", errors="ignore")
    print(G + "  MD5    : " + W + hashlib.md5(e).hexdigest())
    print(G + "  SHA1   : " + W + hashlib.sha1(e).hexdigest())
    print(G + "  SHA256 : " + W + hashlib.sha256(e).hexdigest())
    print(G + "  SHA512 : " + W + hashlib.sha512(e).hexdigest())
    pause(3)

def tool_uuid_gen():
    header()
    print(C + "  ▶ UUID Generator\n" + N)
    for _ in range(int(input(Y + "  Count: " + N) or "5")):
        print(W + "  " + str(uuid.uuid4()) + N)
    pause(3)

def tool_base64():
    header()
    print(C + "  ▶ Base64\n" + N)
    ch = input(Y + "  [1] Encode [2] Decode: " + N).strip()
    text = input(Y + "  Input: " + N)
    try:
        if ch == "1":
            print(G + "  " + base64.b64encode(text.encode()).decode() + N)
        else:
            print(G + "  " + base64.b64decode(text + "==").decode("utf-8", errors="replace") + N)
    except Exception as e:
        print(R + f"  ✘ {e}" + N)
    pause(3)

def tool_color_picker():
    header()
    print(C + "  ▶ Color Picker\n" + N)
    print(R + "  ■ Red  " + G + "■ Green  " + Y + "■ Yellow  " + B + "■ Blue  " + M + "■ Magenta  " + C + "■ Cyan  " + W + "■ White" + N)
    print(G + "  Random: " + W + "#" + "".join(random.choices("0123456789ABCDEF", k=6)) + N)
    pause(2)

def tool_port_scanner():
    header()
    print(C + "  ▶ Port Scanner\n" + N)
    host = input(Y + "  Host: " + N).strip() or "127.0.0.1"
    try:
        sp = int(input(Y + "  Start: " + N) or "1")
        ep = int(input(Y + "  End: " + N) or "200")
    except: sp, ep = 1, 200
    ep = min(ep, sp + 300)
    for p in range(sp, ep + 1):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.3)
            if s.connect_ex((host, p)) == 0:
                print(G + f"  ✔ Port {p}" + N)
            s.close()
        except: pass
    pause(3)

# ══════════════════════════════════════════════════════════════
#  TOOL 11: TEMP MAIL
# ══════════════════════════════════════════════════════════════
MAIL_STATE = {"email": None, "login": None, "domain": None}

def mail_generate():
    try:
        data = json.loads(urllib.request.urlopen(
            "https://www.1secmail.com/api/v1/?action=generateEmail", timeout=10
        ).read().decode())
        email = data[0] if isinstance(data, list) and data else (
            data if isinstance(data, str) else None)
        if not email: return None
        login, _, domain = email.partition("@")
        MAIL_STATE["email"] = email
        MAIL_STATE["login"] = login
        MAIL_STATE["domain"] = domain
        return email
    except Exception as e:
        print(R + f"  ✘ {e}" + N)
        return None

def mail_list():
    if not MAIL_STATE.get("email"): return None
    try:
        return json.loads(urllib.request.urlopen(
            f"https://www.1secmail.com/api/v1/?action=getMessages"
            f"&login={MAIL_STATE['login']}&domain={MAIL_STATE['domain']}",
            timeout=10).read().decode())
    except: return None

def mail_read(mid):
    try:
        return json.loads(urllib.request.urlopen(
            f"https://www.1secmail.com/api/v1/?action=readMessage"
            f"&login={MAIL_STATE['login']}&domain={MAIL_STATE['domain']}&id={mid}",
            timeout=10).read().decode())
    except: return None

def mail_delete(mid):
    try:
        urllib.request.urlopen(
            f"https://www.1secmail.com/api/v1/?action=deleteMessage"
            f"&login={MAIL_STATE['login']}&domain={MAIL_STATE['domain']}&id={mid}",
            timeout=10).read()
        return True
    except: return False

def temp_mail_menu():
    while True:
        header()
        items = [
            "[01] Generate Email", "[02] Show Address", "[03] Refresh Inbox",
            "[04] Read Message", "[05] Delete Message",
            "[06] Copy Address (Termux)", "[00] Back",
        ]
        box("TEMP MAIL", items, active=1 if MAIL_STATE.get("email") else 0, active_label="Inbox")
        try: ch = input(Y + "\n  temp >> " + N).strip()
        except (KeyboardInterrupt, EOFError): return
        try:
            if ch in ("01", "1"):
                print()
                addr = mail_generate()
                if addr: print(G + f"  ✔ {addr}" + N)
                else: print(R + "  ✘ Failed." + N)
                pause(2)
            elif ch in ("02", "2"):
                print()
                if MAIL_STATE.get("email"):
                    print(G + f"  {MAIL_STATE['email']}" + N)
                else:
                    print(R + "  ✘ None." + N)
                pause(2)
            elif ch in ("03", "3"):
                msgs = mail_list()
                if not msgs: print(Y + "  Empty." + N)
                else:
                    for m in msgs:
                        print(C + f"  [{m['id']}] " + W + m.get("subject", "?") + N)
                pause(2)
            elif ch in ("04", "4"):
                msgs = mail_list() or []
                if not msgs: print(R + "  ✘ Empty." + N)
                else:
                    for m in msgs:
                        print(C + f"  [{m['id']}] " + W + m.get("subject", "?") + N)
                    mid = input(Y + "  ID: " + N).strip()
                    msg = mail_read(mid)
                    if msg:
                        print(G + f"  From: {msg.get('from')}\n  Subject: {msg.get('subject')}\n" + N)
                        print(W + (msg.get("textBody") or msg.get("htmlBody") or "(empty)")[:2000] + N)
                pause(3)
            elif ch in ("05", "5"):
                for m in (mail_list() or []):
                    print(G + ("  ✔ " if mail_delete(m["id"]) else R + "  ✘ ") + f"deleted {m['id']}" + N)
                pause(2)
            elif ch in ("06", "6"):
                if MAIL_STATE.get("email"):
                    print(G + f"  {MAIL_STATE['email']}" + N)
                    try:
                        subprocess.run(["termux-clipboard-set"],
                                       input=MAIL_STATE["email"].encode(), check=True)
                        print(Y + "  (copied)" + N)
                    except: pass
                else:
                    print(R + "  ✘ None." + N)
                pause(2)
            elif ch in ("00", "0"): return
            else: print(R + "  ✘ Invalid." + N); pause(1)
        except KeyboardInterrupt: return
        except Exception as e: print(R + f"  ✘ {e}" + N); pause(2)

# ══════════════════════════════════════════════════════════════
#  TOOL 12: BOT HOSTING MANAGER
# ══════════════════════════════════════════════════════════════
BOT_DIR  = os.path.expanduser("~/.nexus/bots")
LOG_DIR  = os.path.expanduser("~/.nexus/logs")
REQ_DIR  = os.path.expanduser("~/.nexus/reqs")
DB_PATH  = os.path.expanduser("~/.nexus/bots.json")
os.makedirs(BOT_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(REQ_DIR, exist_ok=True)
PROCS = {}

def detect_telegram_token(code):
    patterns = [
        r'(?:BOT_?TOKEN|TOKEN|bot_token|BOT)\s*=\s*["\']([0-9]+:[A-Za-z0-9_-]{20,})["\']',
        r'telegram\.org/bot([0-9]+:[A-Za-z0-9_-]{20,})',
    ]
    for p in patterns:
        m = re.search(p, code)
        if m: return m.group(1)
    return None

def validate_python(code):
    try: compile(code, "<bot>", "exec"); return True, None
    except SyntaxError as e: return False, str(e)

def load_db():
    if os.path.exists(DB_PATH):
        try: return json.loads(open(DB_PATH).read())
        except: return {}
    return {}

def save_db(db):
    open(DB_PATH, "w").write(json.dumps(db, indent=2))

def verify_token(token):
    try:
        r = json.loads(urllib.request.urlopen(
            f"https://api.telegram.org/bot{token}/getMe", timeout=10).read().decode())
        if r.get("ok"): return r["result"]
    except: pass
    return None

def bot_active_count():
    return sum(1 for n in load_db() if n in PROCS and PROCS[n]["proc"].poll() is None)

def bot_add():
    header()
    print(C + "  ▶ ADD BOT (file / URL / code)\n" + N)
    name = input(Y + "  Bot name: " + N).strip()
    if not name or not re.match(r'^[A-Za-z0-9_-]+$', name):
        print(R + "  ✘ Invalid name." + N); pause(2); return
    if name in load_db():
        if input(Y + f"  '{name}' exists. Overwrite? (y/n): " + N).strip().lower() != "y":
            return
    print(Y + "\n  [1] Local file  [2] URL  [3] Paste code" + N)
    src = input(Y + "  Source: " + N).strip() or "1"
    code = None
    if src == "1":
        path = os.path.expanduser(input(Y + "  File path: " + N).strip())
        if not os.path.exists(path):
            for guess in [f"~/{name}.py", f"/sdcard/{name}.py", f"/sdcard/Download/{name}.py"]:
                gp = os.path.expanduser(guess)
                if os.path.exists(gp): path = gp; break
        if not os.path.exists(path):
            print(R + f"  ✘ Not found." + N); pause(2); return
        code = open(path, encoding="utf-8", errors="ignore").read()
        print(G + f"  [✓] Read {len(code)} chars" + N)
    elif src == "2":
        url = input(Y + "  URL: " + N).strip()
        try:
            code = urllib.request.urlopen(url, timeout=30).read().decode("utf-8", errors="ignore")
            print(G + f"  [✓] Downloaded {len(code)} chars" + N)
        except Exception as e:
            print(R + f"  ✘ {e}" + N); pause(2); return
    elif src == "3":
        code = read_multiline()
        if not code.strip():
            print(R + "  ✘ Empty." + N); pause(2); return
    print(Y + "  [*] Validating..." + N)
    ok, err = validate_python(code)
    if not ok and input(Y + f"  Syntax error: {err}. Save anyway? (y/n): " + N).strip().lower() != "y":
        pause(2); return
    token = detect_telegram_token(code)
    user = None
    if token:
        print(G + f"  [✓] Token: {token[:10]}..." + N)
        if input(Y + "  Verify? (y/n): " + N).strip().lower() == "y":
            info = verify_token(token)
            if info: user = info.get("username", "?"); print(G + f"  [✓] @{user}" + N)
    else:
        ans = input(Y + "  Token (optional): " + N).strip()
        if ans:
            token = ans
            info = verify_token(token)
            if info: user = info.get("username", "?")
    req_path = os.path.expanduser(input(Y + "  Requirements file (Enter to skip): " + N).strip()) or None
    if req_path and not os.path.exists(req_path): req_path = None
    if req_path and input(Y + "  pip install now? (y/n): " + N).strip().lower() == "y":
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", req_path], timeout=600)
    script_path = os.path.join(BOT_DIR, f"{name}.py")
    open(script_path, "w", encoding="utf-8").write(code)
    try: os.chmod(script_path, 0o755)
    except: pass
    db = load_db()
    db[name] = {
        "name": name, "script": script_path,
        "log": os.path.join(LOG_DIR, f"{name}.log"),
        "token": token, "username": user, "requirements": req_path,
        "added": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    save_db(db)
    print(G + f"\n  [✓] Bot '{name}' added!" + N)
    if input(Y + "  Start now? (y/n): " + N).strip().lower() == "y":
        bot_start(name)
    pause(2)

def bot_start(name):
    db = load_db()
    if name not in db: print(R + f"  ✘ Not found." + N); return False
    info = db[name]
    if name in PROCS and PROCS[name]["proc"].poll() is None:
        print(Y + f"  [*] Running PID {PROCS[name]['proc'].pid}." + N); return True
    script = info.get("script") or os.path.join(BOT_DIR, f"{name}.py")
    if not os.path.exists(script): print(R + f"  ✘ Script missing." + N); return False
    log = open(info["log"], "ab", buffering=0)
    try:
        proc = subprocess.Popen(
            [sys.executable, "-u", script],
            stdout=log, stderr=subprocess.STDOUT,
            stdin=subprocess.DEVNULL, cwd=os.path.dirname(script),
        )
        PROCS[name] = {"proc": proc, "script": script,
                       "log": info["log"], "started_at": time.time()}
        time.sleep(0.6)
        if proc.poll() is None:
            print(G + f"  [✓] Started PID {proc.pid}" + N); return True
        print(R + "  ✘ Exited." + N); 
        if name in PROCS: del PROCS[name]
        return False
    except Exception as e:
        print(R + f"  ✘ {e}" + N); return False

def bot_stop(name):
    if name not in PROCS: print(Y + "  [*] Not running." + N); return
    p = PROCS[name]["proc"]
    try:
        p.terminate()
        try: p.wait(timeout=5)
        except subprocess.TimeoutExpired: p.kill()
    except: pass
    del PROCS[name]
    print(G + f"  [✓] Stopped." + N)

def bot_list():
    db = load_db()
    if not db: print(Y + "  No bots." + N); return
    print(W + "  " + f"{'NAME':<14} {'STATUS':<10} {'PID':<7} {'UPTIME':<10} {'USER':<15}" + N)
    print(GR + "  " + "─" * 60 + N)
    for n, info in db.items():
        e = PROCS.get(n)
        if e and e["proc"].poll() is None:
            st = G + "running"; pid = str(e["proc"].pid)
            up = format_uptime(time.time() - e["started_at"])
        else: st = R + "stopped"; pid = "-"; up = "-"
        user = ("@" + info.get("username", "?")) if info.get("username") else "-"
        print(W + f"  {n:<14} " + N + f"{st:<17}{N} {pid:<7} {up:<10} {user:<15}")

def bot_view_logs(name):
    db = load_db()
    if name not in db: print(R + "  ✘ Not found." + N); return
    p = db[name].get("log")
    if not p or not os.path.exists(p): print(R + "  ✘ No log." + N); return
    data = open(p, errors="ignore").read()
    for ln in data.splitlines()[-60:]:
        print(W + "  " + ln + N)
    if input(Y + "\n  Follow live? (y/n): " + N).strip().lower() == "y":
        try:
            f = open(p, errors="ignore"); f.seek(0, 2)
            while True:
                line = f.readline()
                if line: print(W + "  " + line.rstrip() + N)
                else: time.sleep(0.5)
        except KeyboardInterrupt: pass

def bot_view_script(name):
    db = load_db()
    if name not in db: print(R + "  ✘ Not found." + N); return
    p = db[name].get("script")
    if not p or not os.path.exists(p): print(R + "  ✘ Missing." + N); return
    code = open(p, encoding="utf-8", errors="ignore").read()
    print(G + f"  ── {p} ({len(code.splitlines())} lines) ──\n" + N)
    for i, line in enumerate(code.splitlines(), 1):
        print(W + f"  {i:4d}  {line}" + N)

def bot_install_reqs(name):
    db = load_db()
    if name not in db: print(R + "  ✘ Not found." + N); return
    req = db[name].get("requirements")
    if not req or not os.path.exists(req):
        print(Y + "  No requirements set." + N)
        path = os.path.expanduser(input(Y + "  Path (Enter to skip): " + N).strip())
        if not path or not os.path.exists(path): return
        db[name]["requirements"] = path; save_db(db); req = path
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", req], timeout=600)

def bot_send_test(name):
    db = load_db()
    if name not in db: print(R + "  ✘ Not found." + N); return
    token = db[name].get("token") or input(Y + "  Token: " + N).strip()
    cid = input(Y + "  Chat ID: " + N).strip()
    txt = input(Y + "  Message: " + N)
    try:
        urllib.request.urlopen(
            f"https://api.telegram.org/bot{token}/sendMessage",
            data=urllib.parse.urlencode({"chat_id": cid, "text": txt}).encode(),
            timeout=10).read()
        print(G + "  [✓] Sent." + N)
    except Exception as e: print(R + f"  ✘ {e}" + N)

def bot_delete(name):
    db = load_db()
    if name not in db: print(R + "  ✘ Not found." + N); return
    if name in PROCS: bot_stop(name)
    if input(Y + "  Delete files too? (y/n): " + N).strip().lower() == "y":
        for p in [db[name].get("script"), db[name].get("log")]:
            try:
                if p and os.path.exists(p): os.remove(p)
            except: pass
    del db[name]; save_db(db)
    print(G + f"  [✓] Removed." + N)

def bot_manager():
    while True:
        header()
        items = [
            "[01] Add Bot (file/URL/code)", "[02] List My Bots",
            "[03] Start", "[04] Stop", "[05] Restart",
            "[06] View Logs (+ follow)", "[07] View Script",
            "[08] Install Requirements", "[09] Send Test Message",
            "[10] Delete a Bot",
            "[11] Start ALL", "[12] Stop ALL",
            "[00] Back",
        ]
        box("BOT HOSTING", items, active=bot_active_count(), active_label="Active")
        try: ch = input(Y + "\n  bot >> " + N).strip()
        except (KeyboardInterrupt, EOFError): return
        try:
            if ch in ("01", "1"): bot_add()
            elif ch in ("02", "2"):
                header(); print(C + "  ▶ YOUR BOTS\n" + N); bot_list(); print(); pause(3)
            elif ch in ("03", "3"):
                header(); print(C + "  ▶ START\n" + N)
                db = load_db()
                if not db: print(R + "  No bots." + N)
                else:
                    for n in db: print(W + f"  - {n}" + N)
                    name = input(Y + "\n  Name: " + N).strip()
                    bot_start(name)
                pause(2)
            elif ch in ("04", "4"):
                header(); print(C + "  ▶ STOP\n" + N)
                running = [n for n in PROCS if PROCS[n]["proc"].poll() is None]
                if not running: print(Y + "  None running." + N)
                else:
                    for n in running: print(W + f"  - {n}" + N)
                    name = input(Y + "\n  Name: " + N).strip()
                    bot_stop(name)
                pause(2)
            elif ch in ("05", "5"):
                header(); print(C + "  ▶ RESTART\n" + N)
                db = load_db()
                for n in db: print(W + f"  - {n}" + N)
                name = input(Y + "\n  Name: " + N).strip()
                if name in PROCS: bot_stop(name)
                bot_start(name)
                pause(2)
            elif ch in ("06", "6"):
                header(); print(C + "  ▶ LOGS\n" + N)
                db = load_db()
                for n in db: print(W + f"  - {n}" + N)
                name = input(Y + "\n  Name: " + N).strip()
                bot_view_logs(name)
                pause(2)
            elif ch in ("07", "7"):
                header(); print(C + "  ▶ SCRIPT\n" + N)
                db = load_db()
                for n in db: print(W + f"  - {n}" + N)
                name = input(Y + "\n  Name: " + N).strip()
                bot_view_script(name)
                pause(3)
            elif ch in ("08", "8"):
                header(); print(C + "  ▶ INSTALL REQS\n" + N)
                db = load_db()
                for n in db: print(W + f"  - {n}" + N)
                name = input(Y + "\n  Name: " + N).strip()
                bot_install_reqs(name); pause(2)
            elif ch in ("09", "9"):
                header(); print(C + "  ▶ SEND TEST\n" + N)
                db = load_db()
                for n in db: print(W + f"  - {n}" + N)
                name = input(Y + "\n  Name: " + N).strip()
                bot_send_test(name); pause(2)
            elif ch in ("10",):
                header(); print(C + "  ▶ DELETE\n" + N)
                db = load_db()
                for n in db: print(W + f"  - {n}" + N)
                name = input(Y + "\n  Name: " + N).strip()
                if input(R + f"  Delete '{name}'? (y/n): " + N).strip().lower() == "y":
                    bot_delete(name)
                pause(2)
            elif ch in ("11",):
                for n in load_db(): bot_start(n)
                pause(2)
            elif ch in ("12",):
                for n in list(PROCS.keys()): bot_stop(n)
                pause(2)
            elif ch in ("00", "0"): return
            else: print(R + "  ✘ Invalid." + N); pause(1)
        except KeyboardInterrupt: return
        except Exception as e: print(R + f"  ✘ {e}" + N); pause(2)

# ══════════════════════════════════════════════════════════════
#  TOOL 13: WEB HOSTING MANAGER  ← NEW!
#  Paste HTML → free public URL via cloudflared tunnel
# ══════════════════════════════════════════════════════════════
SITE_DIR = os.path.expanduser("~/.nexus/sites")
SITE_DB  = os.path.expanduser("~/.nexus/sites.json")
os.makedirs(SITE_DIR, exist_ok=True)
SITE_PROCS = {}   # name -> {"http": Popen, "tunnel": Popen, "port": int, "url": str, "started_at": float}

def detect_tunnel_tool():
    for tool in ["cloudflared", "ngrok", "lt"]:
        try:
            r = subprocess.run(["which", tool], capture_output=True, text=True)
            if r.returncode == 0 and r.stdout.strip(): return tool
        except: continue
    return None

def install_cloudflared():
    arch = subprocess.run(["uname", "-m"], capture_output=True, text=True).stdout.strip()
    if "aarch64" in arch or "arm64" in arch:
        url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64"
    elif "arm" in arch:
        url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm"
    else:
        url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64"
    target_dir = os.path.expanduser("~/bin")
    os.makedirs(target_dir, exist_ok=True)
    target = os.path.join(target_dir, "cloudflared")
    print(Y + f"  Downloading cloudflared ({arch}) ..." + N)
    urllib.request.urlretrieve(url, target)
    os.chmod(target, 0o755)
    # Add ~/bin to PATH for this session
    os.environ["PATH"] = target_dir + os.pathsep + os.environ.get("PATH", "")
    return target

def start_tunnel(port, tool, log):
    """Start a tunnel, return (process, public_url)."""
    if tool == "cloudflared":
        cf = subprocess.run(["which", "cloudflared"],
                            capture_output=True, text=True).stdout.strip()
        if not cf: raise RuntimeError("cloudflared not found")
        proc = subprocess.Popen(
            [cf, "tunnel", "--url", f"http://localhost:{port}", "--no-autoupdate"],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, bufsize=1,
        )
        url = None
        deadline = time.time() + 30
        while time.time() < deadline:
            line = proc.stdout.readline()
            if not line:
                time.sleep(0.1); continue
            log.write(line.encode())
            m = re.search(r'https://[a-z0-9-]+\.trycloudflare\.com', line, re.IGNORECASE)
            if m: url = m.group(0); break
        if not url:
            proc.kill(); raise RuntimeError("Tunnel URL not found in 30s")
        return proc, url
    elif tool == "ngrok":
        ng = subprocess.run(["which", "ngrok"],
                            capture_output=True, text=True).stdout.strip()
        if not ng: raise RuntimeError("ngrok not found")
        proc = subprocess.Popen(
            [ng, "http", str(port), "--log", "stdout"],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, bufsize=1,
        )
        url = None
        deadline = time.time() + 30
        while time.time() < deadline:
            line = proc.stdout.readline()
            if not line:
                time.sleep(0.1); continue
            log.write(line.encode())
            m = re.search(r'https://[a-z0-9-]+\.ngrok[a-z0-9.-]*', line, re.IGNORECASE)
            if m: url = m.group(0); break
        if not url:
            proc.kill(); raise RuntimeError("ngrok URL not found")
        return proc, url
    else:
        raise RuntimeError(f"Unknown tunnel tool: {tool}")

def load_sites_db():
    if os.path.exists(SITE_DB):
        try: return json.loads(open(SITE_DB).read())
        except: return {}
    return {}

def save_sites_db(db):
    open(SITE_DB, "w").write(json.dumps(db, indent=2))

def site_active_count():
    return sum(1 for n in load_sites_db()
               if n in SITE_PROCS and SITE_PROCS[n]["http"].poll() is None)

def site_add():
    header()
    print(C + "  ▶ HOST NEW SITE (HTML)\n" + N)
    name = input(Y + "  Site name: " + N).strip()
    if not name or not re.match(r'^[A-Za-z0-9_-]+$', name):
        print(R + "  ✘ Invalid name." + N); pause(2); return
    if name in load_sites_db():
        if input(Y + f"  '{name}' exists. Overwrite? (y/n): " + N).strip().lower() != "y":
            return
    print(Y + "\n  Source:\n    [1] Paste HTML\n    [2] Local file\n    [3] URL" + N)
    src = input(Y + "  Source: " + N).strip() or "1"
    html = None
    if src == "1":
        html = read_multiline()
        if not html.strip():
            print(R + "  ✘ Empty." + N); pause(2); return
    elif src == "2":
        path = os.path.expanduser(input(Y + "  File path: " + N).strip())
        if not os.path.exists(path):
            for guess in [f"~/{name}.html", f"/sdcard/{name}.html",
                          f"/sdcard/Download/{name}.html"]:
                gp = os.path.expanduser(guess)
                if os.path.exists(gp): path = gp; break
        if not os.path.exists(path):
            print(R + "  ✘ Not found." + N); pause(2); return
        html = open(path, encoding="utf-8", errors="ignore").read()
        print(G + f"  [✓] Read {len(html)} chars" + N)
    elif src == "3":
        url = input(Y + "  URL: " + N).strip()
        try:
            html = urllib.request.urlopen(url, timeout=30).read().decode("utf-8", errors="ignore")
            print(G + f"  [✓] Downloaded {len(html)} chars" + N)
        except Exception as e:
            print(R + f"  ✘ {e}" + N); pause(2); return
    site_path = os.path.join(SITE_DIR, name)
    os.makedirs(site_path, exist_ok=True)
    index_path = os.path.join(site_path, "index.html")
    open(index_path, "w", encoding="utf-8").write(html)
    print(G + f"  [✓] Saved to {index_path}" + N)
    # Allow user to drop extra asset files
    extra = input(Y + "  Extra asset files? (file paths, comma-separated, Enter to skip): " + N).strip()
    if extra:
        for src_path in extra.split(","):
            src_path = src_path.strip()
            if not src_path: continue
            sp = os.path.expanduser(src_path)
            if os.path.isfile(sp):
                fname = os.path.basename(sp)
                try:
                    shutil.copy2(sp, os.path.join(site_path, fname))
                    print(G + f"  [✓] Copied {fname}" + N)
                except Exception as e:
                    print(R + f"  ✘ {e}" + N)
            else:
                print(R + f"  ✘ Not found: {sp}" + N)
    db = load_sites_db()
    db[name] = {
        "name": name, "path": site_path, "index": index_path,
        "log": os.path.join(LOG_DIR, f"site_{name}.log"),
        "port": None, "url": None,
        "added": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    save_sites_db(db)
    print(G + f"\n  [✓] Site '{name}' added!" + N)
    if input(Y + "  Start hosting now? (y/n): " + N).strip().lower() == "y":
        site_start(name)
    pause(2)

def site_start(name):
    db = load_sites_db()
    if name not in db: print(R + f"  ✘ Not found." + N); return False
    info = db[name]
    if name in SITE_PROCS and SITE_PROCS[name]["http"].poll() is None:
        print(Y + f"  [*] Already running at {SITE_PROCS[name]['url']}" + N)
        return True
    if not os.path.exists(info["index"]):
        print(R + "  ✘ index.html missing." + N); return False
    port = find_free_port()
    log = open(info["log"], "ab", buffering=0)
    try:
        http_proc = subprocess.Popen(
            [sys.executable, "-m", "http.server", str(port),
             "--bind", "0.0.0.0", "--directory", info["path"]],
            stdout=log, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
        )
        time.sleep(0.5)
        if http_proc.poll() is not None:
            print(R + "  ✘ HTTP server failed to start." + N); return False
        print(G + f"  [✓] HTTP on port {port}" + N)
    except Exception as e:
        print(R + f"  ✘ HTTP error: {e}" + N); return False
    url = f"http://localhost:{port}"
    tunnel_proc = None
    tool = detect_tunnel_tool()
    if not tool:
        print(Y + "  [*] No tunnel tool found." + N)
        if input(Y + "  Install cloudflared? (y/n): " + N).strip().lower() == "y":
            try:
                install_cloudflared()
                tool = "cloudflared"
                print(G + "  [✓] Installed." + N)
            except Exception as e:
                print(R + f"  ✘ Install failed: {e}" + N)
    if tool:
        try:
            print(Y + f"  [*] Starting {tool} tunnel ..." + N)
            tunnel_proc, url = start_tunnel(port, tool, log)
            print(G + f"  [✓] Tunnel up" + N)
        except Exception as e:
            print(R + f"  ✘ Tunnel error: {e}" + N)
            print(Y + f"  [*] Site is local only at http://localhost:{port}" + N)
            url = f"http://localhost:{port}"
    SITE_PROCS[name] = {
        "http": http_proc, "tunnel": tunnel_proc, "port": port,
        "url": url, "started_at": time.time(),
    }
    info["port"] = port; info["url"] = url
    db[name] = info; save_sites_db(db)
    print(G + f"\n  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" + N)
    print(G + f"  ✓ Site '{name}' is LIVE:" + N)
    print(C + BD + f"    {url}" + N)
    print(G + f"  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" + N)
    # Auto-copy to clipboard
    try:
        subprocess.run(["termux-clipboard-set"], input=url.encode(), check=True)
        print(Y + "  (URL copied to clipboard)" + N)
    except: pass
    pause(4)
    return True

def site_stop(name):
    if name not in SITE_PROCS: print(Y + "  [*] Not running." + N); return
    e = SITE_PROCS[name]
    for k in ["tunnel", "http"]:
        p = e.get(k)
        if p and p.poll() is None:
            try:
                p.terminate()
                try: p.wait(timeout=3)
                except subprocess.TimeoutExpired: p.kill()
            except: pass
    del SITE_PROCS[name]
    db = load_sites_db()
    if name in db:
        db[name]["url"] = None; save_sites_db(db)
    print(G + f"  [✓] Stopped." + N)

def site_list():
    db = load_sites_db()
    if not db: print(Y + "  No sites." + N); return
    print(W + "  " + f"{'NAME':<14} {'STATUS':<10} {'PORT':<6} {'URL':<44}" + N)
    print(GR + "  " + "─" * 78 + N)
    for n, info in db.items():
        e = SITE_PROCS.get(n)
        if e and e["http"].poll() is None:
            st = G + "live"; port = str(e["port"]); url = e["url"]
            if len(url) > 42: url = url[:39] + "..."
        else: st = R + "offline"; port = "-"; url = "-"
        print(W + f"  {n:<14} " + N + f"{st:<17}{N} {port:<6} {url}")

def site_view_logs(name):
    db = load_sites_db()
    if name not in db: print(R + "  ✘ Not found." + N); return
    p = db[name].get("log")
    if not p or not os.path.exists(p): print(R + "  ✘ No log." + N); return
    data = open(p, errors="ignore").read()
    for ln in data.splitlines()[-60:]:
        print(W + "  " + ln + N)
    if input(Y + "\n  Follow live? (y/n): " + N).strip().lower() == "y":
        try:
            f = open(p, errors="ignore"); f.seek(0, 2)
            while True:
                line = f.readline()
                if line: print(W + "  " + line.rstrip() + N)
                else: time.sleep(0.5)
        except KeyboardInterrupt: pass

def site_view_files(name):
    db = load_sites_db()
    if name not in db: print(R + "  ✘ Not found." + N); return
    p = db[name].get("path")
    if not p or not os.path.exists(p): print(R + "  ✘ Path missing." + N); return
    print(G + f"  Files in {p}:\n" + N)
    for root, dirs, files in os.walk(p):
        for f in files:
            full = os.path.join(root, f)
            rel = os.path.relpath(full, p)
            size = os.path.getsize(full)
            print(W + f"    {rel:<40} {size:>8} bytes" + N)

def site_replace_html(name):
    db = load_sites_db()
    if name not in db: print(R + "  ✘ Not found." + N); return
    p = db[name]["index"]
    print(Y + "  Paste new HTML. End with: ###END###" + N)
    html = read_multiline()
    if not html.strip(): print(R + "  ✘ Empty." + N); return
    open(p, "w", encoding="utf-8").write(html)
    print(G + f"  [✓] Updated {p}" + N)

def site_show_url(name):
    db = load_sites_db()
    e = SITE_PROCS.get(name)
    if e and e["http"].poll() is None:
        url = e["url"]
        print(G + f"  ✓ {name} is live at:" + N)
        print(C + BD + f"    {url}" + N)
        try:
            subprocess.run(["termux-clipboard-set"], input=url.encode(), check=True)
            print(Y + "  (copied)" + N)
        except: pass
    else:
        print(R + f"  ✘ '{name}' is not running." + N)
    pause(3)

def site_delete(name):
    db = load_sites_db()
    if name not in db: print(R + "  ✘ Not found." + N); return
    if name in SITE_PROCS: site_stop(name)
    if input(Y + f"  Delete all files for '{name}'? (y/n): " + N).strip().lower() == "y":
        p = db[name].get("path")
        try:
            if p and os.path.exists(p): shutil.rmtree(p)
        except: pass
        log = db[name].get("log")
        try:
            if log and os.path.exists(log): os.remove(log)
        except: pass
    del db[name]; save_sites_db(db)
    print(G + f"  [✓] Removed." + N)

def site_manager():
    while True:
        header()
        items = [
            "[01] Host New Site (paste/file/URL)",
            "[02] List My Sites",
            "[03] Start a Site (get URL)",
            "[04] Stop a Site",
            "[05] Restart a Site",
            "[06] View Site Logs (+ follow)",
            "[07] View Site Files",
            "[08] Edit HTML (replace)",
            "[09] Show URL (copy)",
            "[10] Delete a Site",
            "[11] Start ALL Sites",
            "[12] Stop ALL Sites",
            "[00] Back",
        ]
        box("WEB HOSTING", items, active=site_active_count(), active_label="Live")
        try: ch = input(Y + "\n  site >> " + N).strip()
        except (KeyboardInterrupt, EOFError): return
        try:
            if ch in ("01", "1"): site_add()
            elif ch in ("02", "2"):
                header(); print(C + "  ▶ YOUR SITES\n" + N); site_list(); print(); pause(3)
            elif ch in ("03", "3"):
                header(); print(C + "  ▶ START\n" + N)
                db = load_sites_db()
                if not db: print(R + "  No sites." + N)
                else:
                    for n in db: print(W + f"  - {n}" + N)
                    name = input(Y + "\n  Name: " + N).strip()
                    site_start(name)
                pause(2)
            elif ch in ("04", "4"):
                header(); print(C + "  ▶ STOP\n" + N)
                running = [n for n in SITE_PROCS if SITE_PROCS[n]["http"].poll() is None]
                if not running: print(Y + "  None running." + N)
                else:
                    for n in running: print(W + f"  - {n}" + N)
                    name = input(Y + "\n  Name: " + N).strip()
                    site_stop(name)
                pause(2)
            elif ch in ("05", "5"):
                header(); print(C + "  ▶ RESTART\n" + N)
                db = load_sites_db()
                for n in db: print(W + f"  - {n}" + N)
                name = input(Y + "\n  Name: " + N).strip()
                if name in SITE_PROCS: site_stop(name)
                site_start(name)
                pause(2)
            elif ch in ("06", "6"):
                header(); print(C + "  ▶ LOGS\n" + N)
                db = load_sites_db()
                for n in db: print(W + f"  - {n}" + N)
                name = input(Y + "\n  Name: " + N).strip()
                site_view_logs(name); pause(2)
            elif ch in ("07", "7"):
                header(); print(C + "  ▶ FILES\n" + N)
                db = load_sites_db()
                for n in db: print(W + f"  - {n}" + N)
                name = input(Y + "\n  Name: " + N).strip()
                site_view_files(name); pause(3)
            elif ch in ("08", "8"):
                header(); print(C + "  ▶ EDIT HTML\n" + N)
                db = load_sites_db()
                for n in db: print(W + f"  - {n}" + N)
                name = input(Y + "\n  Name: " + N).strip()
                site_replace_html(name); pause(2)
            elif ch in ("09", "9"):
                header(); print(C + "  ▶ SHOW URL\n" + N)
                db = load_sites_db()
                for n in db: print(W + f"  - {n}" + N)
                name = input(Y + "\n  Name: " + N).strip()
                site_show_url(name)
            elif ch in ("10",):
                header(); print(C + "  ▶ DELETE\n" + N)
                db = load_sites_db()
                for n in db: print(W + f"  - {n}" + N)
                name = input(Y + "\n  Name: " + N).strip()
                if input(R + f"  Delete '{name}'? (y/n): " + N).strip().lower() == "y":
                    site_delete(name)
                pause(2)
            elif ch in ("11",):
                for n in load_sites_db(): site_start(n)
                pause(2)
            elif ch in ("12",):
                for n in list(SITE_PROCS.keys()): site_stop(n)
                pause(2)
            elif ch in ("00", "0"): return
            else: print(R + "  ✘ Invalid." + N); pause(1)
        except KeyboardInterrupt: return
        except Exception as e: print(R + f"  ✘ {e}" + N); pause(2)

# ══════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════
def cleanup_all():
    for n in list(PROCS.keys()):
        try: bot_stop(n)
        except: pass
    for n in list(SITE_PROCS.keys()):
        try: site_stop(n)
        except: pass

def main():
    while True:
        header()
        items = [
            "[01] Check System & Public IP",
            "[02] Website Status Checker",
            "[03] Secure Password Generator",
            "[04] IP Geolocation Lookup",
            "[05] DNS Records Lookup",
            "[06] Hash Generator",
            "[07] UUID Generator",
            "[08] Base64 Encode/Decode",
            "[09] Color Picker",
            "[10] Port Scanner",
            "[11] Temp Mail",
            "[12] Bot Hosting Manager",
            "[13] Web Hosting Manager (NEW!)",
            "[00] Exit Tool",
        ]
        box("SELECT AN OPTION", items,
            active=bot_active_count(), active_label="Bots/Sites")
        try: ch = input(Y + "\n  Select an option >> " + N).strip()
        except (KeyboardInterrupt, EOFError): ch = "0"
        try:
            if ch in ("01", "1"): tool_check_system()
            elif ch in ("02", "2"): tool_website_status()
            elif ch in ("03", "3"): tool_password_gen()
            elif ch in ("04", "4"): tool_ip_lookup()
            elif ch in ("05", "5"): tool_dns_lookup()
            elif ch in ("06", "6"): tool_hash_gen()
            elif ch in ("07", "7"): tool_uuid_gen()
            elif ch in ("08", "8"): tool_base64()
            elif ch in ("09", "9"): tool_color_picker()
            elif ch in ("10",): tool_port_scanner()
            elif ch in ("11",): temp_mail_menu()
            elif ch in ("12",): bot_manager()
            elif ch in ("13",): site_manager()
            elif ch in ("00", "0"):
                print(G + "\n  Cleaning up ..." + N)
                cleanup_all()
                print(G + "  Bye!\n" + N)
                sys.exit(0)
            else: print(R + "  ✘ Invalid option." + N); pause(1)
        except KeyboardInterrupt:
            print()
            if input(Y + "  Exit? (y/n): " + N).strip().lower() == "y":
                cleanup_all()
                print(G + "  Bye!\n" + N)
                sys.exit(0)
        except Exception as e:
            print(R + f"  ✘ {e}" + N); pause(2)


if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt:
        cleanup_all()
        print(G + "\n  Bye!\n" + N)
        sys.exit(0)
