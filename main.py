from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import Dict, Optional, Any
import os
import json
import sqlite3
import urllib.request
import urllib.parse
from dotenv import load_dotenv
from campus_blueprint import CAMPUS_BLUEPRINT, CAMPUS_METADATA
from sandbox_engine import evaluate_sandbox_state, generate_random_timetable, format_12h
from cad_sandbox_view import render_cad_sandbox_html
from campus_systems_view import render_campus_systems_html
import random

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://rzdrqgwmmfliyksuiknx.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "sb_publishable_LPVQ_Mzxl8AK8c_JLhMNAw_CoumpNyK")

# Server-persisted / env-backed notification credentials (zero-prompt auto-dispatch)
CONFIG_FILE = "notification_config.json"
DEFAULT_NOTIFY_CONFIG = {
    "telegram_bot_token": os.getenv("TELEGRAM_BOT_TOKEN", "9222503668:AAER9GfSgmqEQ3s-maK9Ljx1eTfBXM5NRg8"),
    "telegram_chat_id": os.getenv("TELEGRAM_CHAT_ID", "7308787759"),
    "webhook_url": os.getenv("WEBHOOK_URL", "https://theone14.app.n8n.cloud/webhook/gridsense-alert"),
    "whatsapp_phone": os.getenv("WHATSAPP_PHONE", ""),
    "whatsapp_apikey": os.getenv("WHATSAPP_APIKEY", "")
}

def load_notify_config():
    cfg = dict(DEFAULT_NOTIFY_CONFIG)
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                saved = json.load(f)
                for k, v in saved.items():
                    if v:
                        cfg[k] = v
        except Exception:
            pass
    return cfg

def save_notify_config(new_cfg: dict):
    cfg = load_notify_config()
    for k in ["telegram_bot_token", "telegram_chat_id", "webhook_url", "whatsapp_phone", "whatsapp_apikey"]:
        if k in new_cfg and new_cfg[k] is not None:
            cfg[k] = str(new_cfg[k]).strip()
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2)
    except Exception:
        pass
    return cfg

# Time-stamped Session Suggestions Log (SQLite-persisted, shared between Sandbox and Dashboard)
SUGGESTIONS_DB = "gridsense_logs.db"
DEFAULT_SUGGESTIONS = [
    {
        "time_12h": "12:00 PM",
        "mode": "Daylight Harvest",
        "title": "Move 3 Afternoon Classes to Block C (Natural Sunlight)",
        "suggestion": "3 classes active at 12:00 PM (CR B-101, CR B-102, CR B-108). Relocate to Block C sun-facing studios (>450 lux natural daylight) to shut down Block B artificial lighting and central chiller loop.",
        "actions_taken": "Block B lighting banks isolated; Lifts L3 & L4 in Deep Sleep; AC setpoints raised to 26°C.",
        "energy_saved": "Saved 26.4 kW (63.5% reduction | INR 237.60/hr saved)"
    },
    {
        "time_12h": "02:30 PM",
        "mode": "Wing Consolidation",
        "title": "Consolidate Right Wing Class to Left Wing",
        "suggestion": "3 classes active in Left Wing (B-101, B-102, B-103) and 1 class in Right Wing (B-108). Move CR B-108 (24 students) to CR B-104 to shut down the entire Right Wing.",
        "actions_taken": "Lifts L1 & L2 active for Left Wing; Lifts L3 & L4 OFF. Right Corridor and SE Stairs powered OFF.",
        "energy_saved": "Saved 24.9 kW (59.8% reduction | INR 224.10/hr saved)"
    },
    {
        "time_12h": "07:30 PM",
        "mode": "Evening Lockdown",
        "title": "Relocate Far-Wing Evening Study Group to Main Entrance",
        "suggestion": "1 isolated evening class in CR B-108 (25 students). Relocate to CR B-101 near Main Staircase to cut off East Wing corridor and far-wing circuits.",
        "actions_taken": "Lifts L1 & L2 active; Lifts L3 & L4 in Deep Sleep; 10 vacant rooms and Faculty Lounge powered OFF.",
        "energy_saved": "Saved 31.2 kW (74.8% reduction | INR 280.80/hr saved)"
    }
]


def _init_suggestions_db():
    with sqlite3.connect(SUGGESTIONS_DB) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS session_suggestions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                time_12h TEXT NOT NULL,
                mode TEXT NOT NULL,
                title TEXT NOT NULL,
                suggestion TEXT NOT NULL,
                actions_taken TEXT NOT NULL,
                energy_saved TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        count = conn.execute("SELECT COUNT(*) FROM session_suggestions").fetchone()[0]
        if count == 0:
            for item in reversed(DEFAULT_SUGGESTIONS):
                conn.execute(
                    "INSERT INTO session_suggestions (time_12h, mode, title, suggestion, actions_taken, energy_saved) VALUES (?, ?, ?, ?, ?, ?)",
                    (item["time_12h"], item["mode"], item["title"], item["suggestion"], item["actions_taken"], item["energy_saved"])
                )
        conn.commit()


def get_persisted_suggestions(limit: int = 15) -> list:
    _init_suggestions_db()
    with sqlite3.connect(SUGGESTIONS_DB) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT time_12h, mode, title, suggestion, actions_taken, energy_saved FROM session_suggestions ORDER BY id DESC LIMIT ?",
            (limit,)
        ).fetchall()
    return [dict(r) for r in rows]


def save_persisted_suggestion(entry: dict):
    _init_suggestions_db()
    with sqlite3.connect(SUGGESTIONS_DB) as conn:
        conn.execute(
            "INSERT INTO session_suggestions (time_12h, mode, title, suggestion, actions_taken, energy_saved) VALUES (?, ?, ?, ?, ?, ?)",
            (entry["time_12h"], entry["mode"], entry["title"], entry["suggestion"], entry["actions_taken"], entry["energy_saved"])
        )
        conn.commit()


_init_suggestions_db()


class SandboxEvalRequest(BaseModel):
    time: Any = Field(default="07:30 PM", description="Time in 12-hr AM/PM string or 24-hr float")
    temperature: float = Field(default=32.0, ge=10.0, le=55.0)
    weather: str = Field(default="Sunny / Daylight")
    rooms: Dict[str, int] = Field(default_factory=dict)
    simulate: bool = Field(default=False)
    mode: str = Field(default="Variable Mode")
    notify_config: Optional[Dict[str, Any]] = None

def dispatch_auto_notification(report: dict, time_12h: str, inline_cfg: dict = None) -> dict:
    """Automatically dispatch the 3-part simulation message to n8n/Power Automate Webhook, Telegram, or WhatsApp."""
    cfg = load_notify_config()
    if inline_cfg:
        for k, v in inline_cfg.items():
            if v:
                cfg[k] = str(v).strip()

    msg = report.get("formatted_message", "GridSense Simulation Completed")
    channels_sent = []

    # 1. Webhook (n8n / Microsoft Power Automate / Make)
    webhook_url = cfg.get("webhook_url", "")
    if webhook_url:
        try:
            suggestion_only = report.get("suggestion", "")
            mail_text = (
                f"Classroom Update ({time_12h} // JIT Block B):\n\n"
                f"{suggestion_only}"
            )
            payload = json.dumps({
                "time_12h": time_12h,
                "suggestion": suggestion_only,
                "actions_taken": report.get("actions_taken", ""),
                "energy_saved": report.get("energy_saved", ""),
                "text": mail_text
            }).encode("utf-8")
            req = urllib.request.Request(webhook_url, data=payload, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=10) as _:
                channels_sent.append("Webhook (n8n/Power Automate)")
        except Exception:
            pass

    # 2. Telegram Bot API
    tg_token = cfg.get("telegram_bot_token", "")
    tg_chat = cfg.get("telegram_chat_id", "")
    if tg_token and tg_chat:
        try:
            url = f"https://api.telegram.org/bot{tg_token}/sendMessage"
            payload = json.dumps({"chat_id": tg_chat, "text": msg}).encode("utf-8")
            req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                res_data = json.loads(resp.read().decode())
                if res_data.get("ok"):
                    channels_sent.append("Telegram Mobile")
        except Exception:
            pass

    # 3. CallMeBot Free WhatsApp API
    wa_phone = cfg.get("whatsapp_phone", "")
    wa_key = cfg.get("whatsapp_apikey", "")
    if wa_phone and wa_key:
        try:
            encoded_msg = urllib.parse.quote(msg)
            url = f"https://api.callmebot.com/whatsapp.php?phone={wa_phone}&text={encoded_msg}&apikey={wa_key}"
            with urllib.request.urlopen(url, timeout=10) as _:
                channels_sent.append("WhatsApp Mobile")
        except Exception:
            pass

    return {
        "dispatched": len(channels_sent) > 0,
        "channels": channels_sent,
        "status": "sent" if channels_sent else "logged_locally"
    }

app = FastAPI(title="GridSense: Campus Intelligent Energy Optimization")

TELEMETRY_DATA = {}
if os.path.exists("synthetic_telemetry.json"):
    try:
        with open("synthetic_telemetry.json", "r") as f:
            TELEMETRY_DATA = json.load(f)
    except Exception as e:
        print("Error loading telemetry:", e)

@app.get("/block_b_floorplan.png")
def get_floorplan_image():
    if os.path.exists("block_b_floorplan.png"):
        return FileResponse("block_b_floorplan.png")
    return JSONResponse(status_code=404, content={"error": "Image not found"})

@app.get("/api/telemetry")
def get_telemetry():
    return TELEMETRY_DATA

@app.get("/api/blueprint")
def get_blueprint():
    return {
        "institution": "JIT",
        "metadata": CAMPUS_METADATA,
        "blueprint": CAMPUS_BLUEPRINT
    }

@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "system": "GridSense v1.0",
        "institution": "JIT",
        "telemetry_intervals": len(TELEMETRY_DATA.get("telemetry", [])),
        "savings_kwh_7day": TELEMETRY_DATA.get("summary", {}).get("total_saved_kwh", 0)
    }

@app.get("/api/sandbox/timetable")
def api_get_timetable(seed: int = None):
    return generate_random_timetable(seed)

@app.get("/api/suggestions")
def api_get_suggestions():
    return {"suggestions": get_persisted_suggestions(15)}

@app.get("/api/notification-config")
def api_get_notify_config():
    cfg = load_notify_config()
    return {
        "has_telegram": bool(cfg.get("telegram_bot_token") and cfg.get("telegram_chat_id")),
        "has_webhook": bool(cfg.get("webhook_url")),
        "has_whatsapp": bool(cfg.get("whatsapp_phone") and cfg.get("whatsapp_apikey")),
        "webhook_url": cfg.get("webhook_url", "")
    }

@app.post("/api/notification-config")
async def api_save_notify_config(request: Request):
    try:
        body = await request.json()
    except Exception:
        body = {}
    cfg = save_notify_config(body)
    return {"status": "saved", "has_webhook": bool(cfg.get("webhook_url")), "has_telegram": bool(cfg.get("telegram_bot_token"))}

@app.post("/api/sandbox/evaluate")
async def api_sandbox_eval(payload: SandboxEvalRequest, background_tasks: BackgroundTasks):
    body = payload.model_dump()
    result = evaluate_sandbox_state(body)

    # When user clicks "Simulate", persist to SQLite and dispatch alerts non-blocking in background
    if payload.simulate:
        entry = {
            "time_12h": result["time_12h"],
            "mode": payload.mode,
            "title": f"{result['active_classes']} Active Space(s) // {result['total_people']} People",
            "suggestion": result["report"]["suggestion"],
            "actions_taken": result["report"]["actions_taken"],
            "energy_saved": result["report"]["energy_saved"]
        }
        save_persisted_suggestion(entry)
        background_tasks.add_task(dispatch_auto_notification, result["report"], result["time_12h"])
        result["dispatch"] = {"dispatched": True, "status": "queued_background"}

    return result

@app.post("/api/sandbox/notify-telegram")
async def api_notify_telegram(request: Request):
    try:
        body = await request.json()
        if body.get("token") or body.get("chat_id") or body.get("webhook_url"):
            save_notify_config({
                "telegram_bot_token": body.get("token", ""),
                "telegram_chat_id": body.get("chat_id", ""),
                "webhook_url": body.get("webhook_url", ""),
                "whatsapp_phone": body.get("whatsapp_phone", ""),
                "whatsapp_apikey": body.get("whatsapp_apikey", "")
            })
        msg = body.get("message", "GridSense Automation Alert")
        report_obj = {"formatted_message": msg, "suggestion": msg, "actions_taken": "Manual Test", "energy_saved": "Verified"}
        res = dispatch_auto_notification(report_obj, "Live Test")
        return {"status": "success", "dispatch": res, "message": "Configuration saved on server. Simulations will now auto-dispatch without prompting."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/systems", response_class=HTMLResponse)
@app.get("/modules", response_class=HTMLResponse)
def campus_systems():
    return render_campus_systems_html()


@app.get("/", response_class=HTMLResponse)
def home():
    summary = TELEMETRY_DATA.get("summary", {
        "total_baseline_kwh": 3394.8,
        "total_gridsense_kwh": 1769.1,
        "total_saved_kwh": 1625.7,
        "savings_percentage": 47.9,
        "total_saved_inr": 14631.37
    })

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GridSense - JIT Campus Energy Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap" rel="stylesheet">
    <style>
        * {{ box-sizing: border-box; }}
        body {{
            font-family: 'Inter', sans-serif;
            background-color: #2B2D31;
            color: #D9DAD0;
            margin: 0;
        }}
        h1, h2, h3, .font-heading {{ font-family: 'Plus Jakarta Sans', sans-serif; letter-spacing: -0.015em; }}
        .font-data {{ font-family: 'Inter', sans-serif; font-variant-numeric: tabular-nums; }}
        .card {{
            background: #36393F;
            border-radius: 12px;
            border: 1px solid rgba(255,255,255,0.06);
            box-shadow: 0 1px 3px rgba(0,0,0,0.2);
        }}
        .nav-link {{
            position: relative;
            padding: 6px 0;
            color: #8E9297;
            font-weight: 500;
            font-size: 14px;
            text-decoration: none;
            transition: color 0.15s ease;
        }}
        .nav-link:hover {{ color: #D9DAD0; }}
        .nav-link.active {{
            color: #FFC93C;
        }}
        .nav-link.active::after {{
            content: '';
            position: absolute;
            bottom: -2px;
            left: 0;
            right: 0;
            height: 2px;
            background: #FFC93C;
            border-radius: 1px;
        }}
        .kv-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 6px 0;
            font-size: 13px;
        }}
        .kv-row + .kv-row {{
            border-top: 1px solid rgba(255,255,255,0.04);
        }}
    </style>
</head>
<body class="min-h-screen flex flex-col">

    <header class="border-b" style="border-color: rgba(255,255,255,0.06); background: #2B2D31;">
        <div class="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
            <div class="flex items-center gap-3">
                <div class="w-8 h-8 rounded-lg flex items-center justify-center" style="background: #FFC93C;">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#2B2D31" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                        <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon>
                    </svg>
                </div>
                <span class="text-lg font-bold text-white tracking-tight">GridSense</span>
            </div>

            <nav class="flex items-center gap-8">
                <a href="/" class="nav-link active">Dashboard</a>
                <a href="/sandbox" class="nav-link">Sandbox</a>
                <a href="/systems" class="nav-link">Campus Systems</a>
                <a href="/blueprint" class="nav-link">Blueprint</a>
            </nav>
        </div>
    </header>

    <main class="flex-1 w-full max-w-7xl mx-auto px-6 py-8">

        <div class="mb-8">
            <h1 class="text-2xl font-bold text-white tracking-tight">Campus Overview</h1>
            <p class="text-sm mt-1" style="color: #8E9297;">JIT campus energy intelligence and optimization status</p>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5 mb-8">

            <div class="card p-5">
                <div class="text-xs font-semibold uppercase tracking-wider" style="color: #8E9297;">Energy Saved</div>
                <div class="mt-3 text-3xl font-bold" style="color: #FFC93C;">{summary['total_saved_kwh']}<span class="text-sm font-medium ml-1.5" style="color: #8E9297;">kWh</span></div>
                <div class="text-xs mt-2" style="color: #8E9297;">47.9% reduction over 7 days</div>
            </div>

            <div class="card p-5">
                <div class="text-xs font-semibold uppercase tracking-wider" style="color: #8E9297;">Cost Savings</div>
                <div class="mt-3 text-3xl font-bold" style="color: #FFC93C;">INR {summary['total_saved_inr']}</div>
                <div class="text-xs mt-2" style="color: #8E9297;">Direct utility cost offset</div>
            </div>

            <div class="card p-5">
                <div class="text-xs font-semibold uppercase tracking-wider" style="color: #8E9297;">Peak Demand</div>
                <div class="mt-3 text-3xl font-bold text-white">142<span class="text-sm font-medium ml-1.5" style="color: #8E9297;">kVA</span></div>
                <div class="text-xs mt-2" style="color: #8E9297;">250 kVA limit / 0 penalties</div>
            </div>

            <div class="card p-5">
                <div class="text-xs font-semibold uppercase tracking-wider" style="color: #8E9297;">Managed Assets</div>
                <div class="mt-3 text-3xl font-bold text-white">14<span class="text-sm font-medium ml-1.5" style="color: #8E9297;">Zones</span></div>
                <div class="text-xs mt-2" style="color: #8E9297;">Across Blocks A, B, C and Hostel</div>
            </div>

        </div>

        <section class="card p-6 mb-8">
            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 mb-5">
                <div>
                    <h2 class="text-base font-semibold text-white">7-Day Power Profile</h2>
                    <p class="text-xs mt-0.5" style="color: #8E9297;">672 intervals at 15-min resolution across JIT infrastructure</p>
                </div>
                <div class="flex items-center gap-5 text-xs" style="color: #8E9297;">
                    <span class="flex items-center gap-2">
                        <span class="w-3 h-[3px] rounded-full" style="background: #8E9297; opacity: 0.6;"></span>
                        Baseline
                    </span>
                    <span class="flex items-center gap-2">
                        <span class="w-3 h-[3px] rounded-full" style="background: #FFC93C;"></span>
                        GridSense
                    </span>
                </div>
            </div>
            <div class="w-full" style="height: 280px;">
                <canvas id="energyChart"></canvas>
            </div>
        </section>

        <div class="mb-5">
            <h2 class="text-base font-semibold text-white">Telemetry Nodes</h2>
            <p class="text-xs mt-0.5" style="color: #8E9297;">Live Waste Index Score (WIS) and active automated interventions</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 mb-8">

            <div class="card p-5 flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between mb-3">
                        <span class="text-xs font-semibold font-data" style="color: #8E9297;">BLOCK B // B101</span>
                        <span class="text-[11px] font-data font-medium px-2 py-0.5 rounded-md" style="background: rgba(255,201,60,0.1); color: #FFC93C;">WIS: 18</span>
                    </div>
                    <div class="text-sm font-semibold text-white mb-3">Lecture Room B101 (East)</div>
                    <div class="rounded-lg p-3" style="background: #2B2D31;">
                        <div class="kv-row">
                            <span style="color: #8E9297;">Window Lighting</span>
                            <span class="font-data text-xs" style="color: #D9DAD0;">Zone A Locked OFF</span>
                        </div>
                        <div class="kv-row">
                            <span style="color: #8E9297;">Dynamic HVAC</span>
                            <span class="font-data text-xs" style="color: #D9DAD0;">26C Setpoint (35 Occ)</span>
                        </div>
                        <div class="kv-row">
                            <span style="color: #8E9297;">Smartboard</span>
                            <span class="font-data text-xs" style="color: #FFC93C;">Sleep (7m Timeout)</span>
                        </div>
                    </div>
                </div>
                <div class="mt-4 pt-3 flex justify-between items-center text-xs" style="border-top: 1px solid rgba(255,255,255,0.06);">
                    <span style="color: #8E9297;">Power Reading</span>
                    <span class="font-data font-semibold" style="color: #FFC93C;">1.8 kW <span style="color: #8E9297; text-decoration: line-through; font-weight: 400;">4.9 kW</span></span>
                </div>
            </div>

            <div class="card p-5 flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between mb-3">
                        <span class="text-xs font-semibold font-data" style="color: #8E9297;">BLOCK C // LAB C1</span>
                        <span class="text-[11px] font-data font-medium px-2 py-0.5 rounded-md" style="background: rgba(255,201,60,0.1); color: #FFC93C;">WIS: 12</span>
                    </div>
                    <div class="text-sm font-semibold text-white mb-3">Advanced Computing Lab</div>
                    <div class="rounded-lg p-3" style="background: #2B2D31;">
                        <div class="kv-row">
                            <span style="color: #8E9297;">PC Power State</span>
                            <span class="font-data text-xs" style="color: #D9DAD0;">60 Systems in S3 Sleep</span>
                        </div>
                        <div class="kv-row">
                            <span style="color: #8E9297;">Thermal Load Cut</span>
                            <span class="font-data text-xs" style="color: #D9DAD0;">-6.0 kW Heat Removed</span>
                        </div>
                        <div class="kv-row">
                            <span style="color: #8E9297;">Lab AC Compressors</span>
                            <span class="font-data text-xs" style="color: #D9DAD0;">Isolated</span>
                        </div>
                    </div>
                </div>
                <div class="mt-4 pt-3 flex justify-between items-center text-xs" style="border-top: 1px solid rgba(255,255,255,0.06);">
                    <span style="color: #8E9297;">Power Reading</span>
                    <span class="font-data font-semibold" style="color: #FFC93C;">0.18 kW <span style="color: #8E9297; text-decoration: line-through; font-weight: 400;">12.8 kW</span></span>
                </div>
            </div>

            <div class="card p-5 flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between mb-3">
                        <span class="text-xs font-semibold font-data" style="color: #8E9297;">BLOCK B // ELEVATORS</span>
                        <span class="text-[11px] font-data font-medium px-2 py-0.5 rounded-md" style="background: rgba(255,201,60,0.1); color: #FFC93C;">WIS: 22</span>
                    </div>
                    <div class="text-sm font-semibold text-white mb-3">4-Lift Elevator Bank</div>
                    <div class="rounded-lg p-3" style="background: #2B2D31;">
                        <div class="kv-row">
                            <span style="color: #8E9297;">Active Safety Floor</span>
                            <span class="font-data text-xs" style="color: #FFC93C;">2 Lifts Active Min</span>
                        </div>
                        <div class="kv-row">
                            <span style="color: #8E9297;">Deep Sleep Lifts</span>
                            <span class="font-data text-xs" style="color: #D9DAD0;">Cars 3 and 4 Parked</span>
                        </div>
                        <div class="kv-row">
                            <span style="color: #8E9297;">Accessibility</span>
                            <span class="font-data text-xs" style="color: #D9DAD0;">100% Compliant</span>
                        </div>
                    </div>
                </div>
                <div class="mt-4 pt-3 flex justify-between items-center text-xs" style="border-top: 1px solid rgba(255,255,255,0.06);">
                    <span style="color: #8E9297;">Standby Savings</span>
                    <span class="font-data font-semibold" style="color: #FFC93C;">22 kWh/day</span>
                </div>
            </div>

            <div class="card p-5 flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between mb-3">
                        <span class="text-xs font-semibold font-data" style="color: #8E9297;">HOSTEL // 120 ROOMS</span>
                        <span class="text-[11px] font-data font-medium px-2 py-0.5 rounded-md" style="background: rgba(255,201,60,0.1); color: #FFC93C;">WIS: 15</span>
                    </div>
                    <div class="text-sm font-semibold text-white mb-3">Hostel Block and Geyser Grid</div>
                    <div class="rounded-lg p-3" style="background: #2B2D31;">
                        <div class="kv-row">
                            <span style="color: #8E9297;">Vacant Room Mode</span>
                            <span class="font-data text-xs" style="color: #D9DAD0;">Sensor Auto-Kill</span>
                        </div>
                        <div class="kv-row">
                            <span style="color: #8E9297;">Occupied Rooms</span>
                            <span class="font-data text-xs" style="color: #D9DAD0;">100% Manual Control</span>
                        </div>
                        <div class="kv-row">
                            <span style="color: #8E9297;">Geyser Staggering</span>
                            <span class="font-data text-xs" style="color: #D9DAD0;">W1 05:30 AM / W2 06:30 AM</span>
                        </div>
                    </div>
                </div>
                <div class="mt-4 pt-3 flex justify-between items-center text-xs" style="border-top: 1px solid rgba(255,255,255,0.06);">
                    <span style="color: #8E9297;">Demand Breach</span>
                    <span class="font-data font-semibold" style="color: #D9DAD0;">Zero Violations</span>
                </div>
            </div>

            <div class="card p-5 flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between mb-3">
                        <span class="text-xs font-semibold font-data" style="color: #8E9297;">CAMPUS // 15 COOLERS</span>
                        <span class="text-[11px] font-data font-medium px-2 py-0.5 rounded-md" style="background: rgba(255,201,60,0.1); color: #FFC93C;">WIS: 05</span>
                    </div>
                    <div class="text-sm font-semibold text-white mb-3">Commercial Cooling Units</div>
                    <div class="rounded-lg p-3" style="background: #2B2D31;">
                        <div class="kv-row">
                            <span style="color: #8E9297;">Night Cut-off</span>
                            <span class="font-data text-xs" style="color: #D9DAD0;">07:00 PM - 07:00 AM Daily</span>
                        </div>
                        <div class="kv-row">
                            <span style="color: #8E9297;">Sunday Policy</span>
                            <span class="font-data text-xs" style="color: #D9DAD0;">100% Locked OFF</span>
                        </div>
                        <div class="kv-row">
                            <span style="color: #8E9297;">Thermal Buffer</span>
                            <span class="font-data text-xs" style="color: #D9DAD0;">2+ Hours Retention</span>
                        </div>
                    </div>
                </div>
                <div class="mt-4 pt-3 flex justify-between items-center text-xs" style="border-top: 1px solid rgba(255,255,255,0.06);">
                    <span style="color: #8E9297;">Monthly Savings</span>
                    <span class="font-data font-semibold" style="color: #FFC93C;">1,620 kWh (INR 14.5K)</span>
                </div>
            </div>

            <div class="card p-5 flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between mb-3">
                        <span class="text-xs font-semibold font-data" style="color: #8E9297;">NETWORK // 150 APs</span>
                        <span class="text-[11px] font-data font-medium px-2 py-0.5 rounded-md" style="background: rgba(255,201,60,0.1); color: #FFC93C;">WIS: 10</span>
                    </div>
                    <div class="text-sm font-semibold text-white mb-3">Enterprise PoE WiFi Grid</div>
                    <div class="rounded-lg p-3" style="background: #2B2D31;">
                        <div class="kv-row">
                            <span style="color: #8E9297;">Academic APs</span>
                            <span class="font-data text-xs" style="color: #FFC93C;">5 GHz Radios Off</span>
                        </div>
                        <div class="kv-row">
                            <span style="color: #8E9297;">Off-Hours Mode</span>
                            <span class="font-data text-xs" style="color: #D9DAD0;">2.4 GHz Only (&lt;5W)</span>
                        </div>
                        <div class="kv-row">
                            <span style="color: #8E9297;">Hostel APs</span>
                            <span class="font-data text-xs" style="color: #D9DAD0;">Full 24/7 Bandwidth</span>
                        </div>
                    </div>
                </div>
                <div class="mt-4 pt-3 flex justify-between items-center text-xs" style="border-top: 1px solid rgba(255,255,255,0.06);">
                    <span style="color: #8E9297;">Monthly Potential</span>
                    <span class="font-data font-semibold" style="color: #FFC93C;">2,700 kWh</span>
                </div>
            </div>

        </div>

        <!-- SESSION SUGGESTIONS & SPATIAL OPTIMIZATION LOG (BY TIME) -->
        <section class="card p-6 mb-8">
            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 mb-5">
                <div>
                    <h2 class="text-base font-semibold text-white">Session Suggestions &amp; Spatial Optimization Log (By Time)</h2>
                    <p class="text-xs mt-0.5" style="color: #8E9297;">Live time-indexed spatial consolidation, wing shutdowns, and Block C natural daylight harvesting logs</p>
                </div>
                <a href="/sandbox" class="px-3.5 py-1.5 rounded-lg text-xs font-semibold" style="background: #FFC93C; color: #2B2D31;">
                    Open Interactive Simulator
                </a>
            </div>
            <div id="dashboardSuggestionsLog" class="space-y-3"></div>
        </section>

    </main>

    <footer class="py-4 px-6 text-center text-xs" style="color: #8E9297; border-top: 1px solid rgba(255,255,255,0.06);">
        GridSense v1.0 / JIT Campus
    </footer>

    <script>
        function formatTo12Hour(time24) {{
            if (!time24) return '';
            const parts = time24.split(':');
            let h = parseInt(parts[0], 10);
            const m = parts[1] || '00';
            const ampm = h >= 12 ? 'PM' : 'AM';
            h = h % 12;
            if (h === 0) h = 12;
            return (h < 10 ? '0' + h : h) + ':' + m + ' ' + ampm;
        }}

        fetch('/api/suggestions')
            .then(res => res.json())
            .then(data => {{
                const container = document.getElementById('dashboardSuggestionsLog');
                const items = data.suggestions || [];
                container.innerHTML = items.map(item => `
                    <div class="p-4 rounded-xl" style="background: #2B2D31; border: 1px solid rgba(255,255,255,0.06);">
                        <div class="flex flex-wrap items-center justify-between gap-2 mb-2">
                            <div class="flex items-center gap-2.5">
                                <span class="px-2.5 py-0.5 rounded text-xs font-bold font-data" style="background: rgba(255,201,60,0.15); color: #FFC93C;">${{item.time_12h}}</span>
                                <span class="text-sm font-semibold text-white">${{item.title}}</span>
                            </div>
                            <span class="text-xs font-data px-2 py-0.5 rounded" style="background: #36393F; color: #D9DAD0;">${{item.mode}}</span>
                        </div>
                        <div class="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs mt-2">
                            <div class="p-2.5 rounded-lg" style="background: #36393F;">
                                <div class="font-semibold uppercase text-[10px] mb-1" style="color: #FFC93C;">1. Relocation &amp; Spatial Suggestion</div>
                                <div style="color: #D9DAD0;">${{item.suggestion}}</div>
                            </div>
                            <div class="p-2.5 rounded-lg" style="background: #36393F;">
                                <div class="font-semibold uppercase text-[10px] mb-1" style="color: #D9DAD0;">2. Hardware Actions Taken</div>
                                <div style="color: #D9DAD0;">${{item.actions_taken}}</div>
                            </div>
                            <div class="p-2.5 rounded-lg" style="background: #36393F;">
                                <div class="font-semibold uppercase text-[10px] mb-1" style="color: #8E9297;">3. Energy &amp; Cost Saved</div>
                                <div class="font-data font-semibold" style="color: #FFC93C;">${{item.energy_saved}}</div>
                            </div>
                        </div>
                    </div>
                `).join('');
            }});

        fetch('/api/telemetry')
            .then(res => res.json())
            .then(data => {{
                const telemetry = data.telemetry || [];
                const sampled = telemetry.filter((_, idx) => idx % 4 === 0);
                const labels = sampled.map(p => p.day.substring(0,3) + ' ' + formatTo12Hour(p.timestamp.split(' ')[1]));
                
                const baselineData = sampled.map(p => {{
                    let sum = 0;
                    for (let z in p.zones) sum += p.zones[z].baseline_kw;
                    return sum.toFixed(1);
                }});

                const gridsenseData = sampled.map(p => {{
                    let sum = 0;
                    for (let z in p.zones) sum += p.zones[z].gridsense_kw;
                    return sum.toFixed(1);
                }});

                const ctx = document.getElementById('energyChart').getContext('2d');
                new Chart(ctx, {{
                    type: 'line',
                    data: {{
                        labels: labels,
                        datasets: [
                            {{
                                label: 'Baseline Load (kW)',
                                data: baselineData,
                                borderColor: 'rgba(142, 146, 151, 0.45)',
                                backgroundColor: 'rgba(142, 146, 151, 0.04)',
                                fill: true,
                                borderWidth: 1.5,
                                pointRadius: 0,
                                tension: 0.3
                            }},
                            {{
                                label: 'GridSense (kW)',
                                data: gridsenseData,
                                borderColor: '#FFC93C',
                                backgroundColor: 'rgba(255, 201, 60, 0.08)',
                                fill: true,
                                borderWidth: 2,
                                pointRadius: 0,
                                tension: 0.3
                            }}
                        ]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        interaction: {{ intersect: false, mode: 'index' }},
                        plugins: {{
                            legend: {{ display: false }},
                            tooltip: {{
                                backgroundColor: '#36393F',
                                titleColor: '#FFFFFF',
                                bodyColor: '#D9DAD0',
                                borderColor: 'rgba(255,255,255,0.06)',
                                borderWidth: 1,
                                titleFont: {{ family: 'Inter', size: 12, weight: '600' }},
                                bodyFont: {{ family: 'Inter', size: 11 }},
                                padding: 10,
                                cornerRadius: 8,
                                displayColors: true
                            }}
                        }},
                        scales: {{
                            x: {{
                                grid: {{ color: 'rgba(255, 255, 255, 0.03)', drawBorder: false }},
                                ticks: {{ color: '#8E9297', font: {{ family: 'Inter', size: 10 }}, maxTicksLimit: 14 }}
                            }},
                            y: {{
                                title: {{ display: true, text: 'Total kW', color: '#8E9297', font: {{ family: 'Inter', size: 11, weight: '500' }} }},
                                grid: {{ color: 'rgba(255, 255, 255, 0.03)', drawBorder: false }},
                                ticks: {{ color: '#8E9297', font: {{ family: 'Inter', size: 10 }} }}
                            }}
                        }}
                    }}
                }});
            }})
            .catch(err => console.error("Telemetry error:", err));
    </script>
</body>
</html>
"""

@app.get("/sandbox", response_class=HTMLResponse)
def view_sandbox():
    return render_cad_sandbox_html()

@app.get("/blueprint", response_class=HTMLResponse)
def view_blueprint():
    blocks_html = ""
    for b_name, b_data in CAMPUS_BLUEPRINT.items():
        zones_html = ""
        for z in b_data.get("zones", []):
            zones_html += f"""
            <div class='p-3 rounded-lg text-xs mb-2' style='background: #2B2D31; border: 1px solid rgba(255,255,255,0.04);'>
                <div class='font-semibold' style='color: #FFC93C;'>{z.get('name', '')} (ID: {z.get('id', '')})</div>
                <div style='color: #8E9297; font-size: 11px; margin-top: 4px;'>Capacity: {z.get('capacity', 'N/A')} | Solutions: {', '.join(z.get('solution_mapping', []))}</div>
            </div>"""
        for lab in b_data.get("labs", []):
            zones_html += f"""
            <div class='p-3 rounded-lg text-xs mb-2' style='background: #2B2D31; border: 1px solid rgba(255,255,255,0.04);'>
                <div class='font-semibold' style='color: #FFC93C;'>{lab.get('name', '')} (ID: {lab.get('id', '')})</div>
                <div style='color: #8E9297; font-size: 11px; margin-top: 4px;'>PCs: {lab.get('pc_count', '')} (Active: {lab.get('pc_active_watts', '')}W, Sleep: {lab.get('pc_sleep_watts', '')}W) | Solutions: {', '.join(lab.get('solution_mapping', []))}</div>
            </div>"""
        for w in b_data.get("wings", []):
            stagger = w.get("geyser_bank", {}).get("stagger_slot", "")
            zones_html += f"""
            <div class='p-3 rounded-lg text-xs mb-2' style='background: #2B2D31; border: 1px solid rgba(255,255,255,0.04);'>
                <div class='font-semibold' style='color: #FFC93C;'>{w.get('name', '')} (ID: {w.get('id', '')})</div>
                <div style='color: #8E9297; font-size: 11px; margin-top: 4px;'>Rooms: {w.get('rooms_count', '')} | Presence Sensing: Dual-Tech PIR</div>
                <div style='color: #D9DAD0; font-size: 11px; margin-top: 4px;'>Policy: Vacant = Auto-Kill | Occupied = 100% Manual User Control</div>
                <div style='color: #8E9297; font-size: 11px; margin-top: 4px;'>Geyser Slot: {stagger}</div>
            </div>"""
        for wc in b_data.get("water_coolers", []):
            zones_html += f"""
            <div class='p-2 rounded-lg text-xs mb-1 flex justify-between' style='background: #2B2D31; border: 1px solid rgba(255,255,255,0.04); font-size: 11px;'>
                <span style='color: #8E9297;'>Commercial Water Cooler {wc.get('id', '')} (Floor {wc.get('floor', '')})</span>
                <span class='font-semibold' style='color: #FFC93C;'>{wc.get('compressor_kw', '')} kW | Interlocked 07:00 PM - 07:00 AM</span>
            </div>"""
        for hm in b_data.get("heavy_motors", []):
            zones_html += f"""
            <div class='p-2 rounded-lg text-xs mb-1 flex justify-between' style='background: #2B2D31; border: 1px solid rgba(255,255,255,0.04); font-size: 11px;'>
                <span style='color: #8E9297;'>{hm.get('name', '')}</span>
                <span class='font-semibold' style='color: #FFC93C;'>{hm.get('kw', '')} kW | Shifted to Solar Window</span>
            </div>"""

        elev_info = ""
        if "elevator_bank" in b_data:
            eb = b_data["elevator_bank"]
            elev_info = f"""
            <div class='p-3 rounded-lg text-xs mb-2' style='background: #2B2D31; border: 1px solid rgba(255,255,255,0.04);'>
                <div class='font-semibold' style='color: #FFC93C;'>4-Lift Elevator Bank (ID: {eb.get('id', '')})</div>
                <div style='color: #8E9297; font-size: 11px; margin-top: 4px;'>Total Cars: {eb.get('total_cars')} | Mandatory Active Safety Floor: {eb.get('mandatory_safety_floor')} Cars</div>
                <div style='color: #8E9297; font-size: 11px;'>Motor Rating: {eb.get('car_rating_motor_kw')} kW | Standby Parasitic: {eb.get('standby_parasitic_kw')} kW</div>
            </div>"""

        blocks_html += f"""
        <div class='card p-6 mb-5'>
            <div class='flex items-center justify-between pb-3 mb-4' style='border-bottom: 1px solid rgba(255,255,255,0.06);'>
                <h3 class='text-base font-semibold text-white'>{b_name}</h3>
                <span class='text-xs font-medium' style='color: #FFC93C;'>{len(b_data.get('zones', [])) + len(b_data.get('labs', [])) + len(b_data.get('wings', []))} Managed Asset Groups</span>
            </div>
            <p class='text-xs mb-4' style='color: #8E9297;'>{b_data.get('description', '')}</p>
            {elev_info}
            {zones_html}
        </div>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JIT Campus Blueprint - GridSense</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap" rel="stylesheet">
    <style>
        * {{ box-sizing: border-box; }}
        body {{
            font-family: 'Inter', sans-serif;
            background-color: #2B2D31;
            color: #D9DAD0;
            margin: 0;
        }}
        h1, h2, h3, .font-heading {{ font-family: 'Plus Jakarta Sans', sans-serif; letter-spacing: -0.015em; }}
        .font-data {{ font-family: 'Inter', sans-serif; font-variant-numeric: tabular-nums; }}
        .card {{
            background: #36393F;
            border-radius: 12px;
            border: 1px solid rgba(255,255,255,0.06);
            box-shadow: 0 1px 3px rgba(0,0,0,0.2);
        }}
        .nav-link {{
            position: relative;
            padding: 6px 0;
            color: #8E9297;
            font-weight: 500;
            font-size: 14px;
            text-decoration: none;
            transition: color 0.15s ease;
        }}
        .nav-link:hover {{ color: #D9DAD0; }}
        .nav-link.active {{
            color: #FFC93C;
        }}
        .nav-link.active::after {{
            content: '';
            position: absolute;
            bottom: -2px;
            left: 0;
            right: 0;
            height: 2px;
            background: #FFC93C;
            border-radius: 1px;
        }}
    </style>
</head>
<body class="min-h-screen flex flex-col">

    <header class="border-b" style="border-color: rgba(255,255,255,0.06); background: #2B2D31;">
        <div class="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
            <div class="flex items-center gap-3">
                <div class="w-8 h-8 rounded-lg flex items-center justify-center" style="background: #FFC93C;">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#2B2D31" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                        <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon>
                    </svg>
                </div>
                <span class="text-lg font-bold text-white tracking-tight">GridSense</span>
            </div>

            <nav class="flex items-center gap-8">
                <a href="/" class="nav-link">Dashboard</a>
                <a href="/sandbox" class="nav-link">Sandbox</a>
                <a href="/systems" class="nav-link">Campus Systems</a>
                <a href="/blueprint" class="nav-link active">Blueprint</a>
            </nav>
        </div>
    </header>

    <main class="flex-1 w-full max-w-5xl mx-auto px-6 py-8">

        <div class="mb-8">
            <h1 class="text-2xl font-bold text-white tracking-tight">JIT Campus Blueprint</h1>
            <p class="text-sm mt-1" style="color: #8E9297;">Physical asset hierarchy and digital twin mapping</p>
            <p class="text-xs mt-1 font-data" style="color: #8E9297;">Tariff: INR 9.00/kWh | Max Demand Limit: 250 kVA</p>
        </div>

        {blocks_html}

    </main>

    <footer class="py-4 px-6 text-center text-xs" style="color: #8E9297; border-top: 1px solid rgba(255,255,255,0.06);">
        GridSense v1.0 / JIT Campus
    </footer>

</body>
</html>
"""
