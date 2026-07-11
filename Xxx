#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════╗
║        NEXUS MULTI-TOOL KIT v3.0                         ║
║        Bot Hosting Manager + Temp Mail                   ║
║        Author: Mavis  |  Status: Online & Ready          ║
╚══════════════════════════════════════════════════════════╝

Requires: Python 3.6+
Optional: requests (for the auto-generated bot scripts)
Optional: termux-api (for clipboard in Temp Mail)

Run:   python3 nexus_multitool.py
"""

import os
import sys
import re
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

# ────────────────────────── ANSI COLORS ──────────────────────────
R  = "\033[91m"   # Red
G  = "\033[92m"   # Green
Y  = "\033[93m"   # Yellow
B  = "\033[94m"   # Blue
M  = "\033[95m"   # Magenta
C  = "\033[96m"   # Cyan
W  = "\033[97m"   # White
GR = "\033[90m"   # Gray
BD = "\033[1m"    # Bold
N  = "\033[0m"    # Reset

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
    """Pause execution.  This was MISSING in the original code, which
    caused the NameError you saw on line 313 / 833."""
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
    print(Y + "  ☀ NEXUS MULTI-TOOL KIT v3.0 ☀" + N)
    print(W + "  + Bot Hosting Manager + Temp Mail" + N)
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

# ────────────────────────── TOOL 1: SYSTEM CHECK ───────────────
def tool_check_system():
    header()
    print(C + "  ▶ System & Public IP\n" + N)
    try:
        host = socket.gethostname()
    except Exception:
        host = "unknown"
    local = "N/A"
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(3)
        s.connect(("8.8.8.8", 80))
        local = s.getsockname()[0]
        s.close()
    except Exception:
        pass
    pub = "N/A"
    try:
        pub = urllib.request.urlopen(
            "https://api.ipify.org", timeout=5
        ).read().decode().strip()
    except Exception:
        pass
    print(G + "  Hostname     : " + W + host)
    print(G + "  Local IP     : " + W + local)
    print(G + "  Public IP    : " + W + pub)
    print(G + "  Platform     : " + W + sys.platform)
    print(G + "  Python       : " + W + sys.version.split()[0])
    print(G + "  User         : " + W + os.environ.get("USER", "unknown"))
    print(G + "  CWD          : " + W + os.getcwd())
    print(G + "  Termux       : " + W + ("Yes" if os.path.exists("/data/data/com.termux") else "No"))
    pause(3)

# ────────────────────────── TOOL 2: WEBSITE STATUS ─────────────
def tool_website_status():
    header()
    print(C + "  ▶ Website Status Checker\n" + N)
    url = input(Y + "  URL (with or without https://): " + N).strip()
    if not url:
        return
    if not url.startswith("http"):
        url = "https://" + url
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "Mozilla/5.0 NexusTool/3.0"}
        )
        t0 = time.time()
        r = urllib.request.urlopen(req, timeout=10)
        ms = (time.time() - t0) * 1000
        print(G + f"\n  ✔ Status    : " + W + f"{r.status} {r.reason}")
        print(G + f"  ✔ Time      : " + W + f"{ms:.2f} ms")
        print(G + f"  ✔ Server    : " + W + r.headers.get("Server", "N/A"))
        print(G + f"  ✔ Type      : " + W + r.headers.get("Content-Type", "N/A"))
    except urllib.error.HTTPError as e:
        print(R + f"  ✘ HTTP {e.code} {e.reason}" + N)
    except urllib.error.URLError as e:
        print(R + f"  ✘ URL Error: {e.reason}" + N)
    except Exception as e:
        print(R + f"  ✘ {e}" + N)
    pause(3)

# ────────────────────────── TOOL 3: PASSWORD GEN ───────────────
def tool_password_gen():
    header()
    print(C + "  ▶ Secure Password Generator\n" + N)
    try:
        length = int(input(Y + "  Length (8-128, default 20): " + N) or "20")
    except ValueError:
        length = 20
    length = max(8, min(128, length))
    upper = input(Y + "  Include uppercase? (Y/n): " + N).strip().lower() != "n"
    digits = input(Y + "  Include digits? (Y/n): " + N).strip().lower() != "n"
    syms = input(Y + "  Include symbols? (Y/n): " + N).strip().lower() != "n"
    pool = string.ascii_lowercase
    if upper:
        pool += string.ascii_uppercase
    if digits:
        pool += string.digits
    if syms:
        pool += "!@#$%^&*()-_=+[]{}<>?/"
    pw = "".join(random.SystemRandom().choice(pool) for _ in range(length))
    print(G + "\n  Generated Password:\n" + N)
    print(C + "  " + pw + N)
    print(G + f"\n  Length: {len(pw)} chars | Pool: {len(pool)}" + N)
    pause(3)

# ────────────────────────── TOOL 4: IP GEOLOCATION ─────────────
def tool_ip_lookup():
    header()
    print(C + "  ▶ IP Geolocation Lookup\n" + N)
    ip = input(Y + "  IP (blank = your public IP): " + N).strip()
    try:
        url = f"http://ip-api.com/json/{ip}"
        data = json.loads(urllib.request.urlopen(url, timeout=10).read().decode())
        if data.get("status") == "success":
            for k in ["query", "country", "countryCode", "regionName",
                      "city", "zip", "lat", "lon", "timezone", "isp", "org", "as"]:
                v = data.get(k, "N/A")
                print(G + f"  {k:<14}: " + W + str(v))
        else:
            print(R + f"  ✘ {data.get('message', 'failed')}" + N)
    except Exception as e:
        print(R + f"  ✘ {e}" + N)
    pause(4)

# ────────────────────────── TOOL 5: DNS LOOKUP ─────────────────
def tool_dns_lookup():
    header()
    print(C + "  ▶ DNS Records Lookup\n" + N)
    domain = input(Y + "  Domain (e.g. google.com): " + N).strip()
    if not domain:
        return
    types = ["A", "AAAA", "MX", "NS", "TXT", "CNAME"]
    for t in types:
        try:
            url = f"https://dns.google/resolve?name={domain}&type={t}"
            data = json.loads(
                urllib.request.urlopen(url, timeout=10).read().decode()
            )
            answers = data.get("Answer", [])
            if answers:
                print(G + f"\n  ── {t} Records ──" + N)
                for a in answers[:5]:
                    print(W + f"  {a.get('name', ''):<32} TTL={a.get('TTL', ''):<6} {a.get('data', '')}" + N)
        except Exception as e:
            print(R + f"  ✘ {t}: {e}" + N)
    pause(4)

# ────────────────────────── TOOL 6: HASH GEN ───────────────────
def tool_hash_gen():
    header()
    print(C + "  ▶ Hash Generator\n" + N)
    text = input(Y + "  Text: " + N)
    enc = text.encode("utf-8", errors="ignore")
    print()
    print(G + "  MD5     : " + W + hashlib.md5(enc).hexdigest())
    print(G + "  SHA1    : " + W + hashlib.sha1(enc).hexdigest())
    print(G + "  SHA256  : " + W + hashlib.sha256(enc).hexdigest())
    print(G + "  SHA512  : " + W + hashlib.sha512(enc).hexdigest())
    print(G + "  BLAKE2b : " + W + hashlib.blake2b(enc).hexdigest())
    pause(3)

# ────────────────────────── TOOL 7: UUID GEN ───────────────────
def tool_uuid_gen():
    header()
    print(C + "  ▶ UUID Generator\n" + N)
    try:
        n = int(input(Y + "  Count (1-20, default 5): " + N) or "5")
    except ValueError:
        n = 5
    n = max(1, min(20, n))
    print()
    for i in range(n):
        u = uuid.uuid4()
        print(W + f"  [{i+1:02d}] " + C + str(u) + N)
    pause(3)

# ────────────────────────── TOOL 8: BASE64 ─────────────────────
def tool_base64():
    header()
    print(C + "  ▶ Base64 Encode/Decode\n" + N)
    print(Y + "  [1] Encode")
    print(Y + "  [2] Decode" + N)
    ch = input(Y + "  Choice: " + N).strip()
    if ch == "1":
        text = input(Y + "  Text: " + N)
        try:
            enc = base64.b64encode(text.encode()).decode()
            print(G + f"\n  Encoded: {enc}" + N)
        except Exception as e:
            print(R + f"  ✘ {e}" + N)
    elif ch == "2":
        text = input(Y + "  Base64: " + N).strip()
        try:
            dec = base64.b64decode(text + "==").decode("utf-8", errors="replace")
            print(G + f"\n  Decoded: {dec}" + N)
        except Exception as e:
            print(R + f"  ✘ {e}" + N)
    pause(3)

# ────────────────────────── TOOL 9: COLOR PICKER ───────────────
def tool_color_picker():
    header()
    print(C + "  ▶ Color Picker\n" + N)
    palette = [
        (R, "Red"),     (G, "Green"),   (Y, "Yellow"),
        (B, "Blue"),    (M, "Magenta"), (C, "Cyan"),
        (W, "White"),
    ]
    print(R + "  ■ Red     " + G + "■ Green   " + Y + "■ Yellow")
    print(B + "  ■ Blue    " + M + "■ Magenta " + C + "■ Cyan")
    print(W + "  ■ White\n" + N)
    code = "#" + "".join(random.choices("0123456789ABCDEF", k=6))
    print(G + f"  Random hex : " + W + code + N)
    idx = random.randint(0, len(palette) - 1)
    col, name = palette[idx]
    print(G + f"  Random pick: " + col + "■ " + name + N)
    pause(2)

# ────────────────────────── TOOL 10: PORT SCANNER ──────────────
def tool_port_scanner():
    header()
    print(C + "  ▶ Port Scanner\n" + N)
    host = input(Y + "  Host (default 127.0.0.1): " + N).strip() or "127.0.0.1"
    try:
        sp = int(input(Y + "  Start port (default 1): " + N) or "1")
        ep = int(input(Y + "  End port (default 1024): " + N) or "1024")
    except ValueError:
        sp, ep = 1, 1024
    sp = max(1, sp)
    ep = min(ep, sp + 500)
    print(G + f"\n  Scanning {host}:{sp}-{ep} ...\n" + N)
    open_ports = []
    for p in range(sp, ep + 1):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.3)
            if s.connect_ex((host, p)) == 0:
                open_ports.append(p)
                print(G + f"  ✔ Port {p} open" + N)
            s.close()
        except Exception:
            pass
    print(G + f"\n  Done. {len(open_ports)} open port(s)." + N)
    pause(3)

# ══════════════════════════════════════════════════════════════
#  TOOL 11: TEMP MAIL  (powered by 1secmail.com — no API key)
# ══════════════════════════════════════════════════════════════
MAIL_STATE = {"email": None, "login": None, "domain": None}

def mail_generate():
    try:
        url = "https://www.1secmail.com/api/v1/?action=generateEmail"
        data = json.loads(
            urllib.request.urlopen(url, timeout=10).read().decode()
        )
        if isinstance(data, list) and data:
            email = data[0]
        elif isinstance(data, str):
            email = data
        else:
            return None
        login, _, domain = email.partition("@")
        MAIL_STATE["email"] = email
        MAIL_STATE["login"] = login
        MAIL_STATE["domain"] = domain
        return email
    except Exception as e:
        print(R + f"  ✘ {e}" + N)
        return None

def mail_list():
    if not MAIL_STATE.get("email"):
        return None
    try:
        url = (
            f"https://www.1secmail.com/api/v1/?action=getMessages"
            f"&login={MAIL_STATE['login']}&domain={MAIL_STATE['domain']}"
        )
        return json.loads(
            urllib.request.urlopen(url, timeout=10).read().decode()
        )
    except Exception as e:
        print(R + f"  ✘ {e}" + N)
        return None

def mail_read(mid):
    try:
        url = (
            f"https://www.1secmail.com/api/v1/?action=readMessage"
            f"&login={MAIL_STATE['login']}&domain={MAIL_STATE['domain']}&id={mid}"
        )
        return json.loads(
            urllib.request.urlopen(url, timeout=10).read().decode()
        )
    except Exception as e:
        print(R + f"  ✘ {e}" + N)
        return None

def mail_delete(mid):
    try:
        url = (
            f"https://www.1secmail.com/api/v1/?action=deleteMessage"
            f"&login={MAIL_STATE['login']}&domain={MAIL_STATE['domain']}&id={mid}"
        )
        urllib.request.urlopen(url, timeout=10).read()
        return True
    except Exception:
        return False

def temp_mail_menu():
    while True:
        header()
        items = [
            "[01] Generate New Email",
            "[02] Show Current Address",
            "[03] Refresh Inbox",
            "[04] Read Message",
            "[05] Delete Message",
            "[06] Copy Address (Termux)",
            "[00] Back to Main Menu",
        ]
        active = 1 if MAIL_STATE.get("email") else 0
        box("TEMP MAIL", items, active=active, active_label="Inbox")
        try:
            ch = input(Y + "\n  temp >> " + N).strip()
        except (KeyboardInterrupt, EOFError):
            return
        try:
            if ch in ("01", "1"):
                print()
                addr = mail_generate()
                if addr:
                    print(G + f"  ✔ Generated: {addr}" + N)
                else:
                    print(R + "  ✘ Failed to generate." + N)
                pause(2)
            elif ch in ("02", "2"):
                print()
                if MAIL_STATE.get("email"):
                    print(G + f"  {MAIL_STATE['email']}" + N)
                else:
                    print(R + "  ✘ No active inbox." + N)
                pause(2)
            elif ch in ("03", "3"):
                print()
                msgs = mail_list()
                if msgs is None:
                    pass
                elif not msgs:
                    print(Y + "  Inbox is empty." + N)
                else:
                    for m in msgs:
                        print(C + f"  [{m['id']}] " + W +
                              m.get("subject", "(no subject)") + N)
                        print(GR + f"        from: {m.get('from', '?')}  •  "
                              f"{m.get('date', '?')}" + N)
                pause(3)
            elif ch in ("04", "4"):
                msgs = mail_list() or []
                if not msgs:
                    print(R + "  ✘ Inbox is empty." + N)
                else:
                    for m in msgs:
                        print(C + f"  [{m['id']}] " + W +
                              m.get("subject", "(no subject)") + N)
                    mid = input(Y + "  Message ID: " + N).strip()
                    msg = mail_read(mid)
                    if msg:
                        print(G + f"\n  From    : {msg.get('from')}")
                        print(f"  To      : {msg.get('to')}")
                        print(f"  Subject : {msg.get('subject')}")
                        print(f"  Date    : {msg.get('date')}\n")
                        body = msg.get("textBody") or msg.get("htmlBody") or "(empty)"
                        print(W + body[:2000] + N)
                    else:
                        print(R + "  ✘ Could not read message." + N)
                pause(4)
            elif ch in ("05", "5"):
                msgs = mail_list() or []
                if not msgs:
                    print(R + "  ✘ Inbox is empty." + N)
                else:
                    for m in msgs:
                        if mail_delete(m["id"]):
                            print(G + f"  ✔ Deleted {m['id']}" + N)
                        else:
                            print(R + f"  ✘ Failed to delete {m['id']}" + N)
                pause(2)
            elif ch in ("06", "6"):
                if MAIL_STATE.get("email"):
                    print(G + f"  {MAIL_STATE['email']}" + N)
                    try:
                        subprocess.run(
                            ["termux-clipboard-set"],
                            input=MAIL_STATE["email"].encode(),
                            check=True,
                        )
                        print(Y + "  (Copied to clipboard via termux-api)" + N)
                    except FileNotFoundError:
                        print(GR + "  (termux-api not installed; run: "
                              "pkg install termux-api)" + N)
                    except Exception as e:
                        print(GR + f"  (clipboard error: {e})" + N)
                else:
                    print(R + "  ✘ No active address." + N)
                pause(2)
            elif ch in ("00", "0"):
                return
            else:
                print(R + "  ✘ Invalid option." + N)
                pause(1)
        except KeyboardInterrupt:
            return
        except Exception as e:
            print(R + f"  ✘ Error: {e}" + N)
            pause(2)

# ══════════════════════════════════════════════════════════════
#  TOOL 12: BOT HOSTING MANAGER
# ══════════════════════════════════════════════════════════════
BOT_DIR  = os.path.expanduser("~/.nexus/bots")
LOG_DIR  = os.path.expanduser("~/.nexus/logs")
DB_PATH  = os.path.expanduser("~/.nexus/bots.json")
os.makedirs(BOT_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)
PROCS = {}   # name -> Popen

# This template is injected with the user's name + token.  It produces a
# real, working Telegram bot in pure Python (uses `requests`, auto-installs).
BOT_SCRIPT_TEMPLATE = '''#!/usr/bin/env python3
# Auto-generated by NEXUS MULTI-TOOL v3.0
# Bot: ##NAME##
import os, sys, time
try:
    import requests
except ImportError:
    print("Installing requests ...")
    os.system("pip install requests")
    try:
        import requests
    except ImportError:
        print("Failed to install requests. Run: pip install requests")
        sys.exit(1)

TOKEN = "##TOKEN##"
API   = f"https://api.telegram.org/bot{TOKEN}"
NAME  = "##NAME##"


def get_updates(offset=None):
    try:
        r = requests.get(API + "/getUpdates",
                         params={"offset": offset, "timeout": 30},
                         timeout=35)
        return r.json().get("result", [])
    except Exception as e:
        print(f"[{NAME}] get_updates error: {e}", flush=True)
        return []


def send(chat_id, text):
    try:
        requests.post(API + "/sendMessage",
                      json={"chat_id": chat_id, "text": text},
                      timeout=10)
    except Exception as e:
        print(f"[{NAME}] send error: {e}", flush=True)


def main():
    print(f"[{NAME}] Bot started.", flush=True)
    offset = None
    while True:
        for u in get_updates(offset):
            offset = u["update_id"] + 1
            msg  = u.get("message") or {}
            chat = msg.get("chat", {})
            cid  = chat.get("id")
            text = msg.get("text", "")
            if not cid:
                continue
            if text == "/start":
                send(cid, f"Hello! I am {NAME}. Send /help for info.")
            elif text == "/help":
                send(cid,
                     "/start - greet\\n"
                     "/help - this help\\n"
                     "/ping - pong\\n"
                     "/echo <text> - echo back")
            elif text == "/ping":
                send(cid, "Pong! :ping_pong:")
            elif text.startswith("/echo "):
                send(cid, text[6:])
            else:
                send(cid, f"You said: {text}")
        time.sleep(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"[{NAME}] Stopped.")
'''

def load_db():
    if os.path.exists(DB_PATH):
        try:
            return json.loads(open(DB_PATH).read())
        except Exception:
            return {}
    return {}

def save_db(db):
    open(DB_PATH, "w").write(json.dumps(db, indent=2))

def verify_token(token):
    try:
        url = f"https://api.telegram.org/bot{token}/getMe"
        r = urllib.request.urlopen(url, timeout=10).read().decode()
        data = json.loads(r)
        if data.get("ok"):
            return data["result"]
    except Exception:
        pass
    return None

def bot_write_script(name, token):
    script = (BOT_SCRIPT_TEMPLATE
              .replace("##NAME##", name)
              .replace("##TOKEN##", token))
    path = os.path.join(BOT_DIR, f"{name}.py")
    with open(path, "w") as f:
        f.write(script)
    try:
        os.chmod(path, 0o755)
    except Exception:
        pass
    return path

def bot_start(name):
    db = load_db()
    if name not in db:
        print(R + f"  ✘ Bot '{name}' not found." + N)
        return False
    if name in PROCS and PROCS[name].poll() is None:
        print(Y + f"  [*] '{name}' is already running (PID {PROCS[name].pid})." + N)
        return True
    script = os.path.join(BOT_DIR, f"{name}.py")
    if not os.path.exists(script):
        bot_write_script(name, db[name]["token"])
    log_path = os.path.join(LOG_DIR, f"{name}.log")
    log = open(log_path, "ab", buffering=0)
    try:
        proc = subprocess.Popen(
            [sys.executable, "-u", script],
            stdout=log,
            stderr=subprocess.STDOUT,
            stdin=subprocess.DEVNULL,
            cwd=BOT_DIR,
        )
        PROCS[name] = proc
        time.sleep(0.6)
        if proc.poll() is None:
            print(G + f"  [✓] Bot '{name}' started! PID: {proc.pid}" + N)
            return True
        else:
            print(R + f"  ✘ '{name}' exited immediately. Check log: {log_path}" + N)
            return False
    except Exception as e:
        print(R + f"  ✘ Failed to start: {e}" + N)
        return False

def bot_stop(name):
    if name not in PROCS:
        print(Y + f"  [*] '{name}' is not running." + N)
        return
    p = PROCS[name]
    try:
        p.terminate()
        try:
            p.wait(timeout=5)
        except subprocess.TimeoutExpired:
            p.kill()
    except Exception as e:
        print(R + f"  ✘ Stop error: {e}" + N)
    if name in PROCS:
        del PROCS[name]
    print(G + f"  [✓] '{name}' stopped." + N)

def bot_active_count():
    db = load_db()
    return sum(1 for n in db if n in PROCS and PROCS[n].poll() is None)

def bot_list():
    db = load_db()
    if not db:
        print(Y + "  No bots yet. Add one first." + N)
        return
    print(W + f"  {'NAME':<14} {'USERNAME':<20} {'STATUS':<10} {'PID':<7}" + N)
    print(GR + "  " + "─" * 55 + N)
    for n, info in db.items():
        p = PROCS.get(n)
        running = p and p.poll() is None
        st = (G + "running") if running else (R + "stopped")
        pid = str(p.pid) if running else "-"
        print(W + f"  {n:<14} {('@' + info.get('username', '?')):<20} " +
              N + f"{st:<17}{N} {pid:<7}")

def bot_view_logs(name):
    p = os.path.join(LOG_DIR, f"{name}.log")
    if not os.path.exists(p):
        print(R + f"  ✘ No log for '{name}'." + N)
        return
    try:
        data = open(p, errors="ignore").read()
    except Exception:
        data = "(unreadable)"
    print(G + f"  ── Last 80 lines of {name}.log ──\n" + N)
    lines = data.splitlines()[-80:]
    for ln in lines:
        print(W + "  " + ln + N)

def bot_send_test(name):
    db = load_db()
    if name not in db:
        print(R + "  ✘ Bot not found." + N)
        return
    cid = input(Y + "  Chat ID: " + N).strip()
    txt = input(Y + "  Message: " + N)
    try:
        data = urllib.parse.urlencode({"chat_id": cid, "text": txt}).encode()
        url = f"https://api.telegram.org/bot{db[name]['token']}/sendMessage"
        urllib.request.urlopen(url, data=data, timeout=10).read()
        print(G + "  [✓] Sent." + N)
    except Exception as e:
        print(R + f"  ✘ {e}" + N)

def bot_delete(name):
    db = load_db()
    if name not in db:
        print(R + "  ✘ Bot not found." + N)
        return
    if name in PROCS:
        bot_stop(name)
    for path in [os.path.join(BOT_DIR, f"{name}.py"),
                 os.path.join(LOG_DIR, f"{name}.log")]:
        try:
            if os.path.exists(path):
                os.remove(path)
        except Exception:
            pass
    del db[name]
    save_db(db)
    print(G + f"  [✓] '{name}' removed." + N)

def bot_manager():
    while True:
        header()
        items = [
            "[01] Add New Bot",
            "[02] List My Bots",
            "[03] Start a Bot",
            "[04] Stop a Bot",
            "[05] View Bot Logs",
            "[06] Send Test Message",
            "[07] Delete a Bot",
            "[08] Start ALL Bots",
            "[09] Stop ALL Bots",
            "[00] Back to Main Menu",
        ]
        box("BOT HOSTING MANAGER", items,
            active=bot_active_count(), active_label="Active")
        try:
            ch = input(Y + "\n  bot >> " + N).strip()
        except (KeyboardInterrupt, EOFError):
            return
        try:
            if ch in ("01", "1"):
                header()
                print(C + "  ▶ ADD NEW BOT\n" + N)
                name = input(Y + "  Bot name (no spaces): " + N).strip()
                if not name or not re.match(r'^[A-Za-z0-9_-]+$', name):
                    print(R + "  ✘ Invalid name (letters/digits/_/- only)." + N)
                    pause(2)
                    continue
                token = input(Y + "  Bot token (from @BotFather): " + N).strip()
                if not token or ":" not in token or len(token) < 20:
                    print(R + "  ✘ Invalid token." + N)
                    pause(2)
                    continue
                print(Y + "  [*] Verifying token..." + N)
                info = verify_token(token)
                if not info:
                    print(R + "  ✘ Token verification failed." + N)
                    pause(2)
                    continue
                user = info.get("username", "unknown")
                print(G + f"  [✓] Token valid! Bot: @{user}" + N)
                db = load_db()
                db[name] = {"token": token, "username": user}
                save_db(db)
                sp = bot_write_script(name, token)
                print(G + f"  [✓] Bot '{name}' added!\n" + N)
                print(W + f"  Script  : {sp}")
                print(f"  Log     : {os.path.join(LOG_DIR, name + '.log')}")
                print(f"  User    : @{user}\n" + N)
                if input(Y + "  Start bot now? (y/n): " + N).strip().lower() == "y":
                    bot_start(name)
                pause(2)
            elif ch in ("02", "2"):
                header()
                print(C + "  ▶ YOUR BOTS\n" + N)
                bot_list()
                print()
                pause(3)
            elif ch in ("03", "3"):
                header()
                print(C + "  ▶ START A BOT\n" + N)
                db = load_db()
                if not db:
                    print(R + "  No bots." + N)
                else:
                    for n in db:
                        print(W + f"  - {n}" + N)
                    name = input(Y + "\n  Bot name: " + N).strip()
                    bot_start(name)
                pause(2)
            elif ch in ("04", "4"):
                header()
                print(C + "  ▶ STOP A BOT\n" + N)
                running = [n for n in PROCS if PROCS[n].poll() is None]
                if not running:
                    print(Y + "  No bots running." + N)
                else:
                    for n in running:
                        print(W + f"  - {n}" + N)
                    name = input(Y + "\n  Bot name: " + N).strip()
                    bot_stop(name)
                pause(2)
            elif ch in ("05", "5"):
                header()
                print(C + "  ▶ VIEW BOT LOGS\n" + N)
                db = load_db()
                if not db:
                    print(R + "  No bots." + N)
                else:
                    for n in db:
                        print(W + f"  - {n}" + N)
                    name = input(Y + "\n  Bot name: " + N).strip()
                    bot_view_logs(name)
                pause(4)
            elif ch in ("06", "6"):
                header()
                print(C + "  ▶ SEND TEST MESSAGE\n" + N)
                db = load_db()
                if not db:
                    print(R + "  No bots." + N)
                else:
                    for n in db:
                        print(W + f"  - {n}" + N)
                    name = input(Y + "\n  Bot name: " + N).strip()
                    bot_send_test(name)
                pause(2)
            elif ch in ("07", "7"):
                header()
                print(C + "  ▶ DELETE A BOT\n" + N)
                db = load_db()
                if not db:
                    print(R + "  No bots." + N)
                else:
                    for n in db:
                        print(W + f"  - {n}" + N)
                    name = input(Y + "\n  Bot name: " + N).strip()
                    if input(R + f"  Confirm delete '{name}'? (y/n): " + N)\
                            .strip().lower() == "y":
                        bot_delete(name)
                pause(2)
            elif ch in ("08", "8"):
                db = load_db()
                for n in db:
                    bot_start(n)
                pause(2)
            elif ch in ("09", "9"):
                for n in list(PROCS.keys()):
                    bot_stop(n)
                pause(2)
            elif ch in ("00", "0"):
                return
            else:
                print(R + "  ✘ Invalid option." + N)
                pause(1)
        except KeyboardInterrupt:
            return
        except Exception as e:
            print(R + f"  ✘ Error: {e}" + N)
            pause(2)

# ══════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════
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
            "[11] Temp Mail (NEW)",
            "[12] Bot Hosting Manager (NEW)",
            "[00] Exit Tool",
        ]
        box("SELECT AN OPTION", items,
            active=bot_active_count(), active_label="Active Bots")
        try:
            ch = input(Y + "\n  Select an option >> " + N).strip()
        except (KeyboardInterrupt, EOFError):
            ch = "0"
        try:
            if ch in ("01", "1"):
                tool_check_system()
            elif ch in ("02", "2"):
                tool_website_status()
            elif ch in ("03", "3"):
                tool_password_gen()
            elif ch in ("04", "4"):
                tool_ip_lookup()
            elif ch in ("05", "5"):
                tool_dns_lookup()
            elif ch in ("06", "6"):
                tool_hash_gen()
            elif ch in ("07", "7"):
                tool_uuid_gen()
            elif ch in ("08", "8"):
                tool_base64()
            elif ch in ("09", "9"):
                tool_color_picker()
            elif ch in ("10",):
                tool_port_scanner()
            elif ch in ("11",):
                temp_mail_menu()
            elif ch in ("12",):
                bot_manager()
            elif ch in ("00", "0"):
                print(G + "\n  Stopping all bots ..." + N)
                for n in list(PROCS.keys()):
                    try:
                        bot_stop(n)
                    except Exception:
                        pass
                print(G + "  Bye! :wave:\n" + N)
                sys.exit(0)
            else:
                print(R + "  ✘ Invalid option." + N)
                pause(1)
        except KeyboardInterrupt:
            print()
            if input(Y + "  Exit tool? (y/n): " + N).strip().lower() == "y":
                for n in list(PROCS.keys()):
                    try:
                        bot_stop(n)
                    except Exception:
                        pass
                print(G + "  Bye!\n" + N)
                sys.exit(0)
        except Exception as e:
            print(R + f"  ✘ Error: {e}" + N)
            pause(2)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(G + "\n  Interrupted. Bye!\n" + N)
        sys.exit(0)
