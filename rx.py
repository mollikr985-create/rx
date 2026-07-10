#!/usr/bin/env python3
"""
 ███╗   ███╗██╗   ██╗██╗  ████████╗██╗   ██╗ ████████╗ ██████╗  ██████╗ ██╗     
 ████╗ ████║██║   ██║██║  ╚══██╔══╝██║   ██║ ╚══██╔══╝██╔═══██╗██╔═══██╗██║     
 ██╔████╔██║██║   ██║██║     ██║   ██║   ██║    ██║   ██║   ██║██║   ██║██║     
 ██║╚██╔╝██║██║   ██║██║     ██║   ██║   ██║    ██║   ██║   ██║██║   ██║██║     
 ██║ ╚═╝ ██║╚██████╔╝███████╗██║   ╚██████╔╝    ██║   ╚██████╔╝╚██████╔╝███████╗
 ╚═╝     ╚═╝ ╚═════╝ ╚══════╝╚═╝    ╚═════╝     ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝

  NEXUS MULTI-TOOL KIT v3.0 — Termux CLI Tool
  + Bot Hosting Manager
  + Temp Mail (3-layer fallback)
  Single file. Just run: python multitool.py
"""

import os
import sys
import subprocess
import signal
import time
import json
import re
import random
import string
import uuid
import hashlib
import secrets
import base64
import socket
import asyncio
from datetime import datetime
from pathlib import Path

# ============== AUTO-INSTALL ==============
def setup():
    needed = {'requests': 'requests', 'colorama': 'colorama', 'pyfiglet': 'pyfiglet'}
    for mod, pkg in needed.items():
        try:
            __import__(mod)
        except ImportError:
            print(f"[*] Installing {pkg}...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "-q"],
                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except:
                subprocess.check_call(["pip", "install", pkg, "-q"],
                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

setup()

import requests
from colorama import init, Fore, Style
init(autoreset=True)

# ============== Colors ==============
R  = Fore.RED; G  = Fore.GREEN; Y  = Fore.YELLOW; B  = Fore.BLUE
M  = Fore.MAGENTA; CY = Fore.CYAN; W  = Fore.WHITE
BR = Style.BRIGHT; X  = Style.RESET_ALL

# ============== HTTP Session ==============
NET = requests.Session()
NET.headers.update({
    "User-Agent": "Mozilla/5.0 (Linux; Android 12; Termux) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
})

# ============== Data Dirs ==============
HOME = Path.home() / ".nexus"
HOME.mkdir(exist_ok=True)
BOTS_DIR = HOME / "bots"
BOTS_DIR.mkdir(exist_ok=True)
LOGS_DIR = HOME / "logs"
LOGS_DIR.mkdir(exist_ok=True)
TM_FILE = HOME / "temp_mail.json"
BOTS_FILE = HOME / "bots.json"

# ============== UI ==============
def clear(): os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    clear()
    print(f"""{CY}
 ███╗   ███╗██╗   ██╗██╗  ████████╗██╗   ██╗ ████████╗ ██████╗  ██████╗ ██╗     
 ████╗ ████║██║   ██║██║  ╚══██╔══╝██║   ██║ ╚══██╔══╝██╔═══██╗██╔═══██╗██║     
 ██╔████╔██║██║   ██║██║     ██║   ██║   ██║    ██║   ██║   ██║██║   ██║██║     
 ██║╚██╔╝██║██║   ██║██║     ██║   ██║   ██║    ██║   ██║   ██║██║   ██║██║     
 ██║ ╚═╝ ██║╚██████╔╝███████╗██║   ╚██████╔╝    ██║   ╚██████╔╝╚██████╔╝███████╗
 ╚═╝     ╚═╝ ╚═════╝ ╚══════╝╚═╝    ╚═════╝     ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝{X}""")
    print(f"{R}{'═'*65}{X}")
    print(f"{Y}{BR}  💥 NEXUS MULTI-TOOL KIT v3.0 💥{X}")
    print(f"{CY}  + Bot Hosting Manager + Temp Mail{X}")
    print(f"{R}{'═'*65}{X}")
    print(f"{G}  Author  : {W}Mavis")
    print(f"{G}  Status  : {G}Online & Ready{X}")
    print(f"{R}{'═'*65}{X}\n")

def err(m): print(f"{R}[x] {m}{X}")
def ok(m):  print(f"{G}[✓] {m}{X}")
def info(m):print(f"{CY}[*] {m}{X}")
def warn(m):print(f"{Y}[!] {m}{X}")
def head(t):
    print(f"\n{R}{'─'*65}\n{Y}  {t}\n{R}{'─'*65}{X}\n")
def back(): input(f"\n{Y}  Press Enter to go back...{X}")

# ============== BOT MANAGER ==============
def load_bots():
    try:
        with open(BOTS_FILE, 'r') as f:
            return json.load(f)
    except:
        return {"bots": []}

def save_bots(data):
    with open(BOTS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def is_process_alive(pid):
    try:
        os.kill(pid, 0)
        return True
    except:
        return False

# Default bot template (multi-feature starter bot)
DEFAULT_BOT_TEMPLATE = '''#!/usr/bin/env python3
"""Bot: {name} — Generated by NEXUS Multi-Tool"""
import requests
from datetime import datetime

TOKEN = "{token}"
API = f"https://api.telegram.org/bot{{TOKEN}}"

def send(chat_id, text):
    try:
        requests.post(f"{{API}}/sendMessage", json={{
            "chat_id": chat_id,
            "text": text
        }}, timeout=10)
    except Exception as e:
        print(f"Send error: {{e}}")

def handle(update):
    msg = update.get("message", {{}})
    chat_id = msg.get("chat", {{}}).get("id")
    text = msg.get("text", "")
    
    if not chat_id or not text:
        return
    
    print(f"[{{datetime.now().strftime('%H:%M:%S')}}] {{chat_id}}: {{text}}")
    
    if text == "/start":
        send(chat_id, "👋 Hello! I'm {{name}}.\\n\\nCommands:\\n/myip - Public IP\\n/time - Current time\\n/ping - Pong\\n/echo <text> - Echo\\n/id - Your ID")
    elif text == "/myip":
        try:
            ip = requests.get("https://api.ipify.org", timeout=5).text
            send(chat_id, f"🌐 Your IP: {{ip}}")
        except:
            send(chat_id, "❌ Failed")
    elif text == "/time":
        send(chat_id, f"⏰ {{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}}")
    elif text == "/ping":
        send(chat_id, "🏓 Pong!")
    elif text.startswith("/echo "):
        send(chat_id, text[6:])
    elif text == "/id":
        send(chat_id, f"🆔 Your ID: `{{chat_id}}`")
    else:
        send(chat_id, "❓ Unknown command. Try /start")

def main():
    print(f"[{{datetime.now()}}] Bot {{name}} starting...")
    print(f"[{{datetime.now()}}] Token: {{TOKEN[:10]}}...")
    offset = None
    
    while True:
        try:
            r = requests.get(f"{{API}}/getUpdates", params={{
                "timeout": 30,
                "offset": offset
            }}, timeout=35).json()
            
            if r.get("ok"):
                for update in r.get("result", []):
                    offset = update["update_id"] + 1
                    handle(update)
        except KeyboardInterrupt:
            print(f"\\n[{{datetime.now()}}] Bot {{name}} stopped")
            break
        except Exception as e:
            print(f"[ERROR] {{e}}")
            time.sleep(3)

if __name__ == "__main__":
    import time
    main()
'''

def bot_add():
    head("🤖 ADD NEW BOT")
    name = input(f"  {Y}Bot name (no spaces): {X}").strip().replace(" ", "_")
    if not name: back(); return
    
    data = load_bots()
    if any(b["name"] == name for b in data["bots"]):
        err(f"Bot '{name}' already exists!"); back(); return
    
    token = input(f"  {Y}Bot token (from @BotFather): {X}").strip()
    if not re.match(r'^\d+:[A-Za-z0-9_-]+$', token):
        err("Invalid token format!"); back(); return
    
    # Verify token
    info("Verifying token...")
    try:
        r = NET.get(f"https://api.telegram.org/bot{token}/getMe", timeout=10).json()
        if not r.get("ok"):
            err("Token verification failed!"); back(); return
        bot_info = r.get("result", {})
        ok(f"Token valid! Bot: @{bot_info.get('username', 'N/A')}")
    except Exception as e:
        err(f"Verification error: {e}"); back(); return
    
    # Create bot script
    script_path = BOTS_DIR / f"{name}.py"
    log_path = LOGS_DIR / f"{name}.log"
    
    script_content = DEFAULT_BOT_TEMPLATE.format(name=name, token=token)
    script_path.write_text(script_content)
    
    # Save config
    data["bots"].append({
        "name": name,
        "username": bot_info.get("username", ""),
        "token": token,
        "script": str(script_path),
        "log": str(log_path),
        "pid": None,
        "created": datetime.now().isoformat(),
        "auto_restart": True
    })
    save_bots(data)
    
    ok(f"Bot '{name}' added successfully!")
    print(f"\n  {G}📝 Script: {W}{script_path}")
    print(f"  {G}📋 Log: {W}{log_path}")
    print(f"  {G}🤖 Username: {W}@{bot_info.get('username', 'N/A')}")
    
    if input(f"\n  {Y}Start bot now? (y/n): {X}").lower() == 'y':
        bot_start(name)
    back()

def bot_list():
    head("🤖 MY BOTS")
    data = load_bots()
    bots = data.get("bots", [])
    
    if not bots:
        warn("No bots added yet. Use [01] Add New Bot"); back(); return
    
    print(f"  {'Name':<15} {'Status':<10} {'PID':<8} {'Username'}")
    print(f"  {R}{'─'*60}{X}")
    
    for b in bots:
        pid = b.get("pid")
        if pid and is_process_alive(pid):
            status = f"{G}● RUNNING{X}"
            pid_str = str(pid)
        else:
            status = f"{R}○ STOPPED{X}"
            pid_str = "-"
        print(f"  {CY}{b['name']:<15}{X} {status:<18} {W}{pid_str:<8}{X} @{b.get('username', 'N/A')}")
    
    print(f"\n  {CY}Total: {len(bots)} bot(s){X}")
    back()

def bot_start(name=None):
    if not name:
        data = load_bots()
        bots = [b["name"] for b in data.get("bots", []) if not (b.get("pid") and is_process_alive(b.get("pid")))]
        if not bots:
            warn("No stopped bots to start"); back(); return
        print(f"  {CY}Select bot to start:{X}")
        for i, n in enumerate(bots, 1):
            print(f"  {G}[{i}]{X} {n}")
        try:
            idx = int(input(f"\n  {Y}Number: {X}")) - 1
            name = bots[idx]
        except:
            err("Invalid"); return
    
    data = load_bots()
    bot = next((b for b in data["bots"] if b["name"] == name), None)
    if not bot:
        err(f"Bot '{name}' not found"); return
    
    if bot.get("pid") and is_process_alive(bot["pid"]):
        warn(f"Bot '{name}' is already running (PID {bot['pid']})"); return
    
    info(f"Starting bot '{name}'...")
    try:
        log_file = open(bot["log"], "a")
        process = subprocess.Popen(
            [sys.executable, bot["script"]],
            stdout=log_file,
            stderr=subprocess.STDOUT,
            preexec_fn=os.setsid if hasattr(os, "setsid") else None
        )
        bot["pid"] = process.pid
        save_bots(data)
        ok(f"Bot '{name}' started! PID: {process.pid}")
        info(f"Logs: {bot['log']}")
    except Exception as e:
        err(f"Failed to start: {e}")
    pause(2)

def bot_stop(name=None):
    if not name:
        data = load_bots()
        bots = [b for b in data.get("bots", []) if b.get("pid") and is_process_alive(b.get("pid"))]
        if not bots:
            warn("No running bots"); back(); return
        print(f"  {CY}Select bot to stop:{X}")
        for i, b in enumerate(bots, 1):
            print(f"  {G}[{i}]{X} {b['name']} (PID {b['pid']})")
        try:
            idx = int(input(f"\n  {Y}Number: {X}")) - 1
            name = bots[idx]["name"]
        except:
            err("Invalid"); return
    
    data = load_bots()
    bot = next((b for b in data["bots"] if b["name"] == name), None)
    if not bot:
        err(f"Bot '{name}' not found"); return
    
    pid = bot.get("pid")
    if not pid or not is_process_alive(pid):
        warn(f"Bot '{name}' is not running"); bot["pid"] = None; save_bots(data); return
    
    info(f"Stopping bot '{name}' (PID {pid})...")
    try:
        os.kill(pid, signal.SIGTERM)
        time.sleep(1)
        if is_process_alive(pid):
            os.kill(pid, signal.SIGKILL)
        bot["pid"] = None
        save_bots(data)
        ok(f"Bot '{name}' stopped")
    except Exception as e:
        err(f"Error: {e}")
    pause(2)

def bot_logs():
    head("🤖 VIEW BOT LOGS")
    data = load_bots()
    bots = data.get("bots", [])
    if not bots: warn("No bots"); back(); return
    
    print(f"  {CY}Select bot:{X}")
    for i, b in enumerate(bots, 1):
        print(f"  {G}[{i}]{X} {b['name']}")
    try:
        idx = int(input(f"\n  {Y}Number: {X}")) - 1
        bot = bots[idx]
    except:
        err("Invalid"); back(); return
    
    log_path = Path(bot["log"])
    if not log_path.exists():
        warn("No logs yet"); back(); return
    
    lines = input(f"  {Y}Lines to show (default 30): {X}").strip()
    n = int(lines) if lines else 30
    
    print(f"\n  {CY}═══ Last {n} lines of {bot['name']} ═══{X}\n")
    try:
        with open(log_path, 'r') as f:
            content = f.readlines()
        for line in content[-n:]:
            print(f"  {W}{line.rstrip()}{X}")
    except Exception as e:
        err(f"Error: {e}")
    back()

def bot_test():
    head("🤖 SEND TEST MESSAGE")
    data = load_bots()
    bots = data.get("bots", [])
    if not bots: warn("No bots"); back(); return
    
    print(f"  {CY}Select bot:{X}")
    for i, b in enumerate(bots, 1):
        print(f"  {G}[{i}]{X} {b['name']} (@{b.get('username', 'N/A')})")
    try:
        idx = int(input(f"\n  {Y}Number: {X}")) - 1
        bot = bots[idx]
    except:
        err("Invalid"); back(); return
    
    chat_id = input(f"  {Y}Your chat ID: {X}").strip()
    msg = input(f"  {Y}Message: {X}").strip()
    
    if not chat_id or not msg: back(); return
    
    try:
        r = NET.post(
            f"https://api.telegram.org/bot{bot['token']}/sendMessage",
            json={"chat_id": chat_id, "text": msg},
            timeout=10
        ).json()
        if r.get("ok"):
            ok("Message sent!")
        else:
            err(f"Failed: {r.get('description')}")
    except Exception as e:
        err(f"Error: {e}")
    back()

def bot_delete():
    head("🤖 DELETE BOT")
    data = load_bots()
    bots = data.get("bots", [])
    if not bots: warn("No bots"); back(); return
    
    print(f"  {CY}Select bot to delete:{X}")
    for i, b in enumerate(bots, 1):
        print(f"  {G}[{i}]{X} {b['name']}")
    try:
        idx = int(input(f"\n  {Y}Number: {X}")) - 1
        bot = bots[idx]
    except:
        err("Invalid"); back(); return
    
    if input(f"  {R}Delete '{bot['name']}'? This cannot be undone! (yes/no): {X}").lower() != "yes":
        warn("Cancelled"); back(); return
    
    # Stop if running
    if bot.get("pid") and is_process_alive(bot["pid"]):
        try: os.kill(bot["pid"], signal.SIGTERM)
        except: pass
    
    # Remove files
    for path in [bot.get("script"), bot.get("log")]:
        try:
            if path and Path(path).exists():
                Path(path).unlink()
        except: pass
    
    # Remove from config
    data["bots"] = [b for b in data["bots"] if b["name"] != bot["name"]]
    save_bots(data)
    ok(f"Bot '{bot['name']}' deleted")
    back()

def bot_manager():
    while True:
        clear()
        banner()
        data = load_bots()
        running = sum(1 for b in data.get("bots", []) if b.get("pid") and is_process_alive(b.get("pid")))
        total = len(data.get("bots", []))
        
        print(f"{CY}  ┌─────────────────────────────────────────────┐{X}")
        print(f"{CY}  │{Y}       🤖 BOT HOSTING MANAGER              {CY}│{X}")
        print(f"{CY}  │{W}       Active: {G}{running}{W}/{total} bot(s) running                {CY}│{X}")
        print(f"{CY}  ├─────────────────────────────────────────────┤{X}")
        print(f"{CY}  │  {G}[01]{X} {W}Add New Bot                       {CY}│{X}")
        print(f"{CY}  │  {G}[02]{X} {W}List My Bots                      {CY}│{X}")
        print(f"{CY}  │  {G}[03]{X} {W}Start a Bot                       {CY}│{X}")
        print(f"{CY}  │  {G}[04]{X} {W}Stop a Bot                        {CY}│{X}")
        print(f"{CY}  │  {G}[05]{X} {W}View Bot Logs                     {CY}│{X}")
        print(f"{CY}  │  {G}[06]{X} {W}Send Test Message                 {CY}│{X}")
        print(f"{CY}  │  {G}[07]{X} {W}Delete a Bot                      {CY}│{X}")
        print(f"{CY}  │  {G}[08]{X} {W}Start ALL Bots                    {CY}│{X}")
        print(f"{CY}  │  {G}[09]{X} {W}Stop ALL Bots                     {CY}│{X}")
        print(f"{CY}  │  {G}[00]{X} {W}Back to Main Menu                 {CY}│{X}")
        print(f"{CY}  └─────────────────────────────────────────────┘{X}")
        ch = input(f"\n  {Y}bot >> {X}").strip()
        
        if ch == "01" or ch == "1": bot_add()
        elif ch == "02" or ch == "2": bot_list(); back()
        elif ch == "03" or ch == "3": bot_start()
        elif ch == "04" or ch == "4": bot_stop()
        elif ch == "05" or ch == "5": bot_logs()
        elif ch == "06" or ch == "6": bot_test()
        elif ch == "07" or ch == "7": bot_delete()
        elif ch == "08" or ch == "8":
            data = load_bots()
            for b in data.get("bots", []):
                if not (b.get("pid") and is_process_alive(b.get("pid"))):
                    bot_start(b["name"])
            ok("All bots started"); pause(2)
        elif ch == "09" or ch == "9":
            data = load_bots()
            for b in data.get("bots", []):
                if b.get("pid") and is_process_alive(b.get("pid")):
                    bot_stop(b["name"])
            ok("All bots stopped"); pause(2)
        elif ch == "00" or ch == "0": return
        else: err("Invalid option"); pause()

# ============== TEMP MAIL ==============
def tm_mailtm_create():
    try:
        r = NET.get("https://api.mail.tm/domains", timeout=10).json()
        domain = None
        for d in r.get("hydra:member", []):
            if d.get("isActive") and not d.get("isPrivate"):
                domain = d["domain"]; break
        if not domain: return None
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
        address = f"{username}@{domain}"
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
        r = NET.post("https://api.mail.tm/accounts", json={"address": address, "password": password}, timeout=15)
        if r.status_code in (200, 201):
            tr = NET.post("https://api.mail.tm/token", json={"address": address, "password": password}, timeout=15)
            if tr.status_code == 200:
                return {"service": "mail.tm", "address": address, "token": tr.json().get("token")}
    except: pass
    return None

def tm_gma_create():
    try:
        r = NET.get("https://api.guerrillamail.com/ajax.php?f=get_email_address", timeout=10)
        if r.status_code == 200:
            d = r.json()
            return {"service": "guerrillamail", "address": d.get("email_addr"), "sid": d.get("sid_token")}
    except: pass
    return None

def tool_temp_mail():
    head("📧 TEMPORARY MAIL GENERATOR")
    info("Trying mail.tm → GuerrillaMail...")
    
    account = tm_mailtm_create()
    service = "mail.tm"
    if not account:
        warn("mail.tm failed, trying GuerrillaMail...")
        account = tm_gma_create()
        service = "guerrillamail"
    
    if not account:
        err("All services failed. Check internet."); back(); return
    
    TM_FILE.write_text(json.dumps(account, indent=2))
    ok("Email generated!")
    print(f"\n  {G}📬 Email: {BR}{W}{account['address']}{X}")
    print(f"  {G}🔐 Service: {W}{service}")
    print(f"  {G}💾 Saved: {CY}{TM_FILE}{X}\n")
    
    if input(f"  {Y}Check inbox? (y/n): {X}").lower() == 'y':
        tm_check_inbox(account, service)
    back()

def tm_check_inbox(account, service):
    head(f"📥 INBOX ({service})")
    info("Fetching messages...")
    
    try:
        if service == "mail.tm":
            r = NET.get("https://api.mail.tm/messages", 
                       headers={"Authorization": f"Bearer {account['token']}"}, timeout=10).json()
            msgs = r.get("hydra:member", [])
        else:
            r = NET.get(f"https://api.guerrillamail.com/ajax.php?f=get_email_list&offset=0&sid_token={account['sid']}", timeout=10).json()
            msgs = r.get("mail_list", [])
    except:
        msgs = []
    
    if not msgs:
        warn("No messages yet"); back(); return
    
    ok(f"Found {len(msgs)} message(s)\n")
    for i, m in enumerate(msgs[:10], 1):
        if service == "mail.tm":
            sender = m.get('from', {}).get('address', 'N/A')
            subj = m.get('subject', 'N/A')
        else:
            sender = m.get('mail_from', 'N/A')
            subj = m.get('mail_subject', 'N/A')
        print(f"  {CY}[{i}]{X} {W}{subj}{X}")
        print(f"      {G}From: {W}{sender}{X}\n")
    
    try:
        n = int(input(f"  {Y}Read which? (0=skip): {X}"))
        if n < 1 or n > len(msgs): return
        m = msgs[n-1]
        if service == "mail.tm":
            full = NET.get(f"https://api.mail.tm/messages/{m['id']}",
                          headers={"Authorization": f"Bearer {account['token']}"}, timeout=10).json()
            body = full.get('text', '') or full.get('html', '') or '(empty)'
        else:
            full = NET.get(f"https://api.guerrillamail.com/ajax.php?f=fetch_email&email_id={m['mail_id']}&sid_token={account['sid']}", timeout=10).json()
            body = full.get('mail_body', '') or '(empty)'
        
        if body:
            head(f"📩 MESSAGE #{n}")
            body = re.sub(r'<[^>]+>', '', body)
            print(body[:3000])
    except: pass
    back()

# ============== TOOLS 01-10 (existing) ==============
def tool_system_ip():
    head("[01] CHECK SYSTEM & PUBLIC IP")
    print(f"  {G}╔═══ System Information ═══╗{X}")
    print(f"  {G}║{X} {CY}OS       : {W}{sys.platform}")
    print(f"  {G}║{X} {CY}Python   : {W}{sys.version.split()[0]}")
    print(f"  {G}║{X} {CY}Hostname : {W}{socket.gethostname()}")
    print(f"  {G}║{X} {CY}Time     : {W}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    try:
        stat = os.statvfs('/')
        free_gb = (stat.f_bavail * stat.f_frsize) / (1024**3)
        total_gb = (stat.f_blocks * stat.f_frsize) / (1024**3)
        print(f"  {G}║{X} {CY}Disk     : {W}{free_gb:.1f}GB free / {total_gb:.1f}GB total")
    except: pass
    print(f"  {G}╚{'═'*32}╝{X}\n")
    
    info("Fetching public IP...")
    try:
        ip = NET.get("https://api.ipify.org", timeout=10).text
        d = NET.get(f"http://ip-api.com/json/{ip}", timeout=10).json()
        print(f"  {G}╔═══ Public IP Information ═══╗{X}")
        print(f"  {G}║{X} {CY}IP       : {W}{ip}")
        print(f"  {G}║{X} {CY}Country  : {W}{d.get('country')} ({d.get('countryCode')})")
        print(f"  {G}║{X} {CY}Region   : {W}{d.get('regionName')}")
        print(f"  {G}║{X} {CY}City     : {W}{d.get('city')}")
        print(f"  {G}║{X} {CY}ISP      : {W}{d.get('isp')}")
        print(f"  {G}║{X} {CY}Org      : {W}{d.get('org')}")
        print(f"  {G}╚{'═'*34}╝{X}")
    except Exception as e: err(f"Failed: {e}")
    back()

def tool_website_status():
    head("[02] WEBSITE STATUS CHECKER")
    url = input(f"  {Y}Enter URL: {X}").strip()
    if not url: back(); return
    if not url.startswith("http"): url = "https://" + url
    
    info(f"Checking {url}...")
    try:
        r = NET.get(url, timeout=10, allow_redirects=True)
        print(f"\n  {G}[{r.status_code}]{X} {W}{url}{X}")
        print(f"  {CY}Response time: {W}{r.elapsed.total_seconds():.3f}s{X}")
        print(f"  {CY}Server: {W}{r.headers.get('Server', 'N/A')}{X}")
        print(f"  {CY}Content-Type: {W}{r.headers.get('Content-Type', 'N/A')}{X}")
        sec = ['X-Frame-Options', 'X-XSS-Protection', 'Content-Security-Policy', 'Strict-Transport-Security']
        missing = [h for h in sec if h not in r.headers]
        if missing: warn(f"Missing: {', '.join(missing)}")
        else: ok("Security headers OK ✓")
    except Exception as e: err(f"Failed: {e}")
    back()

def tool_password():
    head("[03] SECURE PASSWORD GENERATOR")
    print(f"  {G}[1]{X} Simple (8, letters)")
    print(f"  {G}[2]{X} Medium (12, mixed)")
    print(f"  {G}[3]{X} Strong (16, all)")
    print(f"  {G}[4]{X} Insane (32, full)")
    print(f"  {G}[5]{X} Custom")
    ch = input(f"\n  {Y}Select: {X}").strip()
    presets = {"1": (8, string.ascii_letters), "2": (12, string.ascii_letters + string.digits),
               "3": (16, string.ascii_letters + string.digits + "!@#$%^&*"),
               "4": (32, string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{}|;:,.<>?")}
    if ch in presets: length, chars = presets[ch]
    elif ch == "5":
        try: length = max(4, min(128, int(input(f"  {Y}Length: {X}").strip())))
        except: length = 16
        chars = string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{}|;:,.<>?"
    else: err("Invalid"); back(); return
    
    pwd = ''.join(secrets.choice(chars) for _ in range(length))
    print(f"\n  {G}╔═══ Password ({length} chars) ═══╗{X}")
    print(f"  {G}║{X}  {BR}{W}{pwd}{X}")
    print(f"  {G}╚{'═'*30}╝{X}")
    warn("Save it now!")
    back()

def tool_ip_lookup():
    head("[04] IP GEOLOCATION LOOKUP")
    ip = input(f"  {Y}IP (blank for yours): {X}").strip()
    if not ip:
        try: ip = NET.get("https://api.ipify.org", timeout=10).text
        except: err("Failed"); back(); return
    if not re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', ip):
        err("Invalid IP"); back(); return
    try:
        d = NET.get(f"http://ip-api.com/json/{ip}", timeout=10).json()
        if d.get("status") == "fail": err("Failed"); back(); return
        print(f"\n  {G}╔═══ {ip} ═══╗{X}")
        print(f"  {G}║{X} {CY}Country : {W}{d.get('country')} ({d.get('countryCode')})")
        print(f"  {G}║{X} {CY}Region  : {W}{d.get('regionName')}")
        print(f"  {G}║{X} {CY}City    : {W}{d.get('city')}")
        print(f"  {G}║{X} {CY}Lat/Lon : {W}{d.get('lat')}, {d.get('lon')}")
        print(f"  {G}║{X} {CY}ISP     : {W}{d.get('isp')}")
        print(f"  {G}║{X} {CY}AS      : {W}{d.get('as')}")
        print(f"  {G}╚{'═'*40}╝{X}")
    except Exception as e: err(f"Error: {e}")
    back()

def tool_dns():
    head("[05] DNS RECORDS LOOKUP")
    dom = input(f"  {Y}Domain: {X}").strip().lower()
    if not dom: back(); return
    dom = dom.replace("http://","").replace("https://","").split("/")[0]
    found = False
    for t in ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME']:
        try:
            r = NET.get(f"https://dns.google/resolve?name={dom}&type={t}", timeout=10).json()
            if r.get("Answer"):
                found = True
                print(f"\n  {Y}[{t}]{X}")
                for a in r["Answer"][:5]:
                    print(f"    {CY}→ {W}{a.get('data', 'N/A')}{X}")
        except: continue
    if not found: err("No records")
    back()

def tool_hash():
    head("[06] HASH GENERATOR")
    t = input(f"  {Y}Text: {X}")
    if not t: back(); return
    print(f"\n  {G}MD5    : {W}{hashlib.md5(t.encode()).hexdigest()}")
    print(f"  {G}SHA1   : {W}{hashlib.sha1(t.encode()).hexdigest()}")
    print(f"  {G}SHA256 : {W}{hashlib.sha256(t.encode()).hexdigest()}")
    print(f"  {G}SHA512 : {W}{hashlib.sha512(t.encode()).hexdigest()}")
    back()

def tool_uuid():
    head("[07] UUID GENERATOR")
    try: n = max(1, min(50, int(input(f"  {Y}How many? (default 5): {X}").strip() or "5")))
    except: n = 5
    print()
    for _ in range(n):
        print(f"  {CY}→ {W}{uuid.uuid4()}")
    back()

def tool_b64():
    head("[08] BASE64")
    print(f"  {G}[1]{X} Encode  {G}[2]{X} Decode")
    m = input(f"  {Y}> {X}").strip()
    t = input(f"  {Y}Text: {X}")
    try:
        if m == "1": print(f"  {G}→ {W}{base64.b64encode(t.encode()).decode()}")
        elif m == "2": print(f"  {G}→ {W}{base64.b64decode(t).decode()}")
        else: err("Invalid")
    except Exception as e: err(f"Error: {e}")
    back()

def tool_colors():
    head("[09] COLOR PICKER")
    colors = {
        "Red": "#FF0000", "Green": "#00FF00", "Blue": "#0000FF",
        "Yellow": "#FFFF00", "Cyan": "#00FFFF", "Magenta": "#FF00FF",
        "Orange": "#FFA500", "Pink": "#FFC0CB", "Purple": "#800080",
        "Black": "#000000", "White": "#FFFFFF", "Gray": "#808080"
    }
    for n, h in colors.items():
        rgb = f"{int(h[1:3],16)}, {int(h[3:5],16)}, {int(h[5:7],16)}"
        print(f"  {G}{n:<10}{W} {h}  RGB({rgb})")
    back()

def tool_portscan():
    head("[10] PORT SCANNER")
    h = input(f"  {Y}Host: {X}").strip()
    p = input(f"  {Y}Port: {X}").strip()
    if not h or not p: back(); return
    try:
        port = int(p)
        s = socket.socket(); s.settimeout(5)
        r = s.connect_ex((h, port)); s.close()
        if r == 0: ok(f"Port {port} OPEN on {h}")
        else: err(f"Port {port} CLOSED on {h}")
    except Exception as e: err(f"Error: {e}")
    back()

# ============== Main Menu ==============
def main_menu():
    banner()
    data = load_bots()
    running = sum(1 for b in data.get("bots", []) if b.get("pid") and is_process_alive(b.get("pid")))
    
    print(f"{CY}  ┌─────────────────────────────────────────────┐{X}")
    print(f"{CY}  │           {Y}SELECT AN OPTION{CY}                  │{X}")
    print(f"{CY}  │{W}       🤖 Active Bots: {G}{running}{W}                       {CY}│{X}")
    print(f"{CY}  ├─────────────────────────────────────────────┤{X}")
    print(f"{CY}  │  {G}[01]{X} {W}Check System & Public IP          {CY}│{X}")
    print(f"{CY}  │  {G}[02]{X} {W}Website Status Checker            {CY}│{X}")
    print(f"{CY}  │  {G}[03]{X} {W}Secure Password Generator        {CY}│{X}")
    print(f"{CY}  │  {G}[04]{X} {W}IP Geolocation Lookup            {CY}│{X}")
    print(f"{CY}  │  {G}[05]{X} {W}DNS Records Lookup               {CY}│{X}")
    print(f"{CY}  │  {G}[06]{X} {W}Hash Generator                   {CY}│{X}")
    print(f"{CY}  │  {G}[07]{X} {W}UUID Generator                   {CY}│{X}")
    print(f"{CY}  │  {G}[08]{X} {W}Base64 Encode/Decode             {CY}│{X}")
    print(f"{CY}  │  {G}[09]{X} {W}Color Picker                     {CY}│{X}")
    print(f"{CY}  │  {G}[10]{X} {W}Port Scanner                     {CY}│{X}")
    print(f"{CY}  │  {BR}{M}[11]{X} {BR}{W}📧 Temp Mail (NEW)               {CY}│{X}")
    print(f"{CY}  │  {BR}{M}[12]{X} {BR}{W}🤖 Bot Hosting Manager (NEW)     {CY}│{X}")
    print(f"{CY}  │  {G}[00]{X} {W}Exit Tool                        {CY}│{X}")
    print(f"{CY}  └─────────────────────────────────────────────┘{X}")
    return input(f"\n  {Y}Select an option >> {X}").strip()

# ============== Main Loop ==============
TOOLS = {
    "1": tool_system_ip, "01": tool_system_ip,
    "2": tool_website_status, "02": tool_website_status,
    "3": tool_password, "03": tool_password,
    "4": tool_ip_lookup, "04": tool_ip_lookup,
    "5": tool_dns, "05": tool_dns,
    "6": tool_hash, "06": tool_hash,
    "7": tool_uuid, "07": tool_uuid,
    "8": tool_b64, "08": tool_b64,
    "9": tool_colors, "09": tool_colors,
    "10": tool_portscan,
    "11": tool_temp_mail,
    "12": bot_manager,
}

def main():
    while True:
        try:
            ch = main_menu()
            if ch == "0" or ch == "00":
                print(f"\n  {G}Thanks for using NEXUS! 👋{X}\n")
                sys.exit(0)
            elif ch in TOOLS:
                TOOLS[ch]()
            else:
                err("Invalid option!"); pause(1)
        except KeyboardInterrupt:
            print(f"\n\n  {Y}Goodbye! 👋{X}\n")
            sys.exit(0)
        except Exception as e:
            err(f"Error: {e}"); pause(2)

if __name__ == "__main__":
    main()
