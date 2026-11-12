from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import os
import json
import urllib.request
from dotenv import load_dotenv
from campus_blueprint import CAMPUS_BLUEPRINT, CAMPUS_METADATA
from sandbox_engine import evaluate_sandbox_state
from cad_sandbox_view import render_cad_sandbox_html

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://rzdrqgwmmfliyksuiknx.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "sb_publishable_LPVQ_Mzxl8AK8c_JLhMNAw_CoumpNyK")

# Telegram credentials (auto-ping)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

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

@app.post("/api/sandbox/evaluate")
async def api_sandbox_eval(request: Request):
    try:
        body = await request.json()
    except Exception:
        body = {}
    result = evaluate_sandbox_state(body)
    return result

@app.post("/api/sandbox/notify-telegram")
async def api_notify_telegram(request: Request):
    try:
        body = await request.json()
        token = body.get("token", "").strip() or TELEGRAM_BOT_TOKEN
        chat_id = body.get("chat_id", "").strip() or TELEGRAM_CHAT_ID
        message = body.get("message", "GridSense Automation Alert")

        if not token or not chat_id:
            return {"status": "error", "message": "Bot token or Chat ID not configured. Please supply once to store."}

        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = json.dumps({"chat_id": chat_id, "text": message}).encode("utf-8")
        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
        
        with urllib.request.urlopen(req, timeout=5) as response:
            res_data = json.loads(response.read().decode())
            if res_data.get("ok"):
                return {"status": "success", "message": "Alert dispatched automatically to your mobile phone."}
            else:
                return {"status": "error", "message": "Telegram API returned failure."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        * {{ box-sizing: border-box; }}
        body {{
            font-family: 'Inter', sans-serif;
            background-color: #2B2D31;
            color: #D9DAD0;
            margin: 0;
        }}
        .font-data {{ font-family: 'JetBrains Mono', monospace; }}
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
                            <span class="font-data text-xs" style="color: #D9DAD0;">W1 05:30 / W2 06:30</span>
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
                            <span class="font-data text-xs" style="color: #D9DAD0;">19:00 - 07:00 Daily</span>
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

    </main>

    <footer class="py-4 px-6 text-center text-xs" style="color: #8E9297; border-top: 1px solid rgba(255,255,255,0.06);">
        GridSense v1.0 / JIT Campus
    </footer>

    <script>
        fetch('/api/telemetry')
            .then(res => res.json())
            .then(data => {{
                const telemetry = data.telemetry || [];
                const sampled = telemetry.filter((_, idx) => idx % 4 === 0);
                const labels = sampled.map(p => p.day.substring(0,3) + ' ' + p.timestamp.split(' ')[1]);
                
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
                                bodyFont: {{ family: 'JetBrains Mono', size: 11 }},
                                padding: 10,
                                cornerRadius: 8,
                                displayColors: true
                            }}
                        }},
                        scales: {{
                            x: {{
                                grid: {{ color: 'rgba(255, 255, 255, 0.03)', drawBorder: false }},
                                ticks: {{ color: '#8E9297', font: {{ family: 'JetBrains Mono', size: 10 }}, maxTicksLimit: 14 }}
                            }},
                            y: {{
                                title: {{ display: true, text: 'Total kW', color: '#8E9297', font: {{ family: 'Inter', size: 11, weight: '500' }} }},
                                grid: {{ color: 'rgba(255, 255, 255, 0.03)', drawBorder: false }},
                                ticks: {{ color: '#8E9297', font: {{ family: 'JetBrains Mono', size: 10 }} }}
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
                <span class='font-semibold' style='color: #FFC93C;'>{wc.get('compressor_kw', '')} kW | Interlocked 19:00 - 07:00</span>
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        * {{ box-sizing: border-box; }}
        body {{
            font-family: 'Inter', sans-serif;
            background-color: #2B2D31;
            color: #D9DAD0;
            margin: 0;
        }}
        .font-data {{ font-family: 'JetBrains Mono', monospace; }}
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
