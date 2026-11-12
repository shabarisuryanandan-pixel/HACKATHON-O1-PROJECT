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
    <title>GridSense // JIT Campus Energy Intelligence</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Inter', sans-serif;
            background-color: #16181d;
            color: #d1d5db;
        }}
        .font-mono-code {{ font-family: 'JetBrains Mono', monospace; }}

        .neu-card {{
            background: #191b22;
            border-radius: 16px;
            box-shadow: 8px 8px 18px #0f1014, -8px -8px 18px #232630;
            border: 1px solid rgba(255, 255, 255, 0.03);
        }}
        .neu-inset {{
            background: #14151a;
            border-radius: 14px;
            box-shadow: inset 5px 5px 12px #0c0d10, inset -5px -5px 12px #1c1d24;
            border: 1px solid rgba(255, 255, 255, 0.02);
        }}
        .neu-btn {{
            background: #191b22;
            border-radius: 12px;
            box-shadow: 5px 5px 12px #0f1014, -5px -5px 12px #232630;
            border: 1px solid rgba(255, 255, 255, 0.04);
            transition: all 0.2s ease;
        }}
        .neu-btn:hover {{
            box-shadow: 2px 2px 6px #0f1014, -2px -2px 6px #232630;
            color: #10b981;
        }}
        .glow-emerald {{
            box-shadow: 0 0 12px rgba(16, 185, 129, 0.25);
        }}
    </style>
</head>
<body class="min-h-screen flex flex-col justify-between selection:bg-emerald-500 selection:text-black">

    <header class="py-4 px-6 border-b border-white/5 bg-[#16181d]">
        <div class="max-w-7xl mx-auto flex flex-col sm:flex-row justify-between items-center gap-4">
            <div class="flex items-center gap-4">
                <div class="w-10 h-10 rounded-xl neu-card flex items-center justify-center font-mono-code font-bold text-emerald-400">
                    GS
                </div>
                <div>
                    <div class="text-xs font-mono-code tracking-wider text-zinc-400 uppercase">JIT Campus Network</div>
                    <div class="text-xl font-bold text-white tracking-tight">GridSense Intelligence</div>
                </div>
            </div>

            <div class="flex items-center gap-3 text-xs font-mono-code">
                <div class="px-3 py-1.5 neu-inset rounded-lg flex items-center gap-2 text-zinc-400">
                    <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
                    <span>System Active</span>
                </div>
                <a href="/sandbox" class="px-4 py-1.5 neu-btn text-emerald-400 font-semibold glow-emerald">
                    Interactive Sandbox
                </a>
                <a href="/blueprint" class="px-4 py-1.5 neu-btn text-zinc-300 font-semibold">
                    Campus Blueprint
                </a>
            </div>
        </div>
    </header>

    <main class="w-full max-w-7xl mx-auto px-4 sm:px-6 py-8 flex-1">

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5 mb-8">
            <div class="p-5 neu-card">
                <div class="text-xs font-mono-code uppercase text-zinc-400">7-Day Energy Saved</div>
                <div class="text-2xl font-bold text-emerald-400 mt-2">{summary['total_saved_kwh']} <span class="text-sm font-normal text-zinc-400">kWh</span></div>
                <div class="text-xs text-zinc-400 mt-1">47.9% reduction vs baseline</div>
            </div>

            <div class="p-5 neu-card">
                <div class="text-xs font-mono-code uppercase text-zinc-400">Weekly Savings</div>
                <div class="text-2xl font-bold text-amber-400 mt-2">INR {summary['total_saved_inr']}</div>
                <div class="text-xs text-zinc-400 mt-1">Direct utility cost offset</div>
            </div>

            <div class="p-5 neu-card">
                <div class="text-xs font-mono-code uppercase text-zinc-400">Max Demand Status</div>
                <div class="text-2xl font-bold text-blue-400 mt-2">142 <span class="text-sm font-normal text-zinc-400">kVA</span></div>
                <div class="text-xs text-zinc-400 mt-1">250 kVA limit (0 penalties)</div>
            </div>

            <div class="p-5 neu-card">
                <div class="text-xs font-mono-code uppercase text-zinc-400">Managed Zones</div>
                <div class="text-2xl font-bold text-zinc-200 mt-2">14 Assets</div>
                <div class="text-xs text-zinc-400 mt-1">Across Blocks A, B, C & Hostel</div>
            </div>
        </div>

        <section class="p-6 neu-card mb-8">
            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 mb-6">
                <div>
                    <h2 class="text-lg font-bold text-white tracking-tight">7-Day Campus Power Profile (Baseline vs GridSense)</h2>
                    <p class="text-xs text-zinc-400 font-mono-code mt-0.5">672 intervals at 15-minute resolution across JIT infrastructure</p>
                </div>
                <div class="flex items-center gap-4 text-xs font-mono-code">
                    <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-red-400"></span> Baseline Draw</span>
                    <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-emerald-400"></span> GridSense Optimized</span>
                </div>
            </div>
            <div class="w-full h-72 neu-inset p-4">
                <canvas id="energyChart"></canvas>
            </div>
        </section>

        <div class="mb-5 flex justify-between items-end">
            <div>
                <h2 class="text-xl font-bold text-white tracking-tight">Campus Telemetry Nodes</h2>
                <p class="text-xs text-zinc-400 font-mono-code mt-0.5">Live Waste Index Score (WIS) & active automated interventions</p>
            </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
            <div class="p-5 neu-card flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between pb-3 mb-3 border-b border-white/5">
                        <span class="text-xs font-mono-code font-bold text-blue-400">BLOCK B // B101</span>
                        <span class="px-2.5 py-1 text-[11px] font-mono-code font-bold rounded-md neu-inset text-emerald-400">WIS: 18 / OPTIMAL</span>
                    </div>
                    <div class="text-base font-semibold text-white">Lecture Room B101 (East)</div>
                    <div class="text-xs text-zinc-400 mt-0.5">Capacity: 60 Seats | Module A Bio-Climatic</div>

                    <div class="mt-4 space-y-2 text-xs font-mono-code neu-inset p-3">
                        <div class="flex justify-between text-zinc-400">
                            <span>Window Lighting:</span>
                            <span class="text-emerald-400">Zone A Locked OFF</span>
                        </div>
                        <div class="flex justify-between text-zinc-400">
                            <span>Dynamic HVAC:</span>
                            <span class="text-zinc-200">26°C Setpoint (35 Occ)</span>
                        </div>
                        <div class="flex justify-between text-zinc-400">
                            <span>Smartboard State:</span>
                            <span class="text-amber-400">Sleep (7m Timeout)</span>
                        </div>
                    </div>
                </div>
                <div class="mt-4 pt-3 border-t border-white/5 flex justify-between items-center text-xs font-mono-code text-zinc-400">
                    <span>Power Reading</span>
                    <span class="text-emerald-400 font-bold">1.8 kW <span class="text-zinc-500 line-through">4.9 kW</span></span>
                </div>
            </div>

            <div class="p-5 neu-card flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between pb-3 mb-3 border-b border-white/5">
                        <span class="text-xs font-mono-code font-bold text-purple-400">BLOCK C // LAB C1</span>
                        <span class="px-2.5 py-1 text-[11px] font-mono-code font-bold rounded-md neu-inset text-emerald-400">WIS: 12 / SECURED</span>
                    </div>
                    <div class="text-base font-semibold text-white">Advanced Computing Lab</div>
                    <div class="text-xs text-zinc-400 mt-0.5">60 Workstations | Module C Power Policy</div>

                    <div class="mt-4 space-y-2 text-xs font-mono-code neu-inset p-3">
                        <div class="flex justify-between text-zinc-400">
                            <span>PC Power State:</span>
                            <span class="text-emerald-400">60 Systems in S3 Sleep</span>
                        </div>
                        <div class="flex justify-between text-zinc-400">
                            <span>Thermal Load Cut:</span>
                            <span class="text-blue-400">-6.0 kW Heat Removed</span>
                        </div>
                        <div class="flex justify-between text-zinc-400">
                            <span>Lab AC Compressors:</span>
                            <span class="text-emerald-400">Isolated</span>
                        </div>
                    </div>
                </div>
                <div class="mt-4 pt-3 border-t border-white/5 flex justify-between items-center text-xs font-mono-code text-zinc-400">
                    <span>Power Reading</span>
                    <span class="text-emerald-400 font-bold">0.18 kW <span class="text-zinc-500 line-through">12.8 kW</span></span>
                </div>
            </div>

            <div class="p-5 neu-card flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between pb-3 mb-3 border-b border-white/5">
                        <span class="text-xs font-mono-code font-bold text-amber-400">BLOCK B // ELEVATORS</span>
                        <span class="px-2.5 py-1 text-[11px] font-mono-code font-bold rounded-md neu-inset text-blue-400">WIS: 22 / THROTTLED</span>
                    </div>
                    <div class="text-base font-semibold text-white">4-Lift Elevator Bank</div>
                    <div class="text-xs text-zinc-400 mt-0.5">Module D Dynamic Staging</div>

                    <div class="mt-4 space-y-2 text-xs font-mono-code neu-inset p-3">
                        <div class="flex justify-between text-zinc-400">
                            <span>Active Safety Floor:</span>
                            <span class="text-amber-400">2 Lifts Active Minimum</span>
                        </div>
                        <div class="flex justify-between text-zinc-400">
                            <span>Deep Sleep Lifts:</span>
                            <span class="text-zinc-400">Cars 3 & 4 Parked</span>
                        </div>
                        <div class="flex justify-between text-zinc-400">
                            <span>Accessibility Status:</span>
                            <span class="text-emerald-400">100% Compliant</span>
                        </div>
                    </div>
                </div>
                <div class="mt-4 pt-3 border-t border-white/5 flex justify-between items-center text-xs font-mono-code text-zinc-400">
                    <span>Standby Savings</span>
                    <span class="text-emerald-400 font-bold">22 kWh/day</span>
                </div>
            </div>

            <div class="p-5 neu-card flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between pb-3 mb-3 border-b border-white/5">
                        <span class="text-xs font-mono-code font-bold text-red-400">HOSTEL // 120 ROOMS</span>
                        <span class="px-2.5 py-1 text-[11px] font-mono-code font-bold rounded-md neu-inset text-emerald-400">WIS: 15 / BALANCED</span>
                    </div>
                    <div class="text-base font-semibold text-white">Hostel Block & Geyser Grid</div>
                    <div class="text-xs text-zinc-400 mt-0.5">Module E Staggering & Presence Sensing</div>

                    <div class="mt-4 space-y-2 text-xs font-mono-code neu-inset p-3">
                        <div class="flex justify-between text-zinc-400">
                            <span>Vacant Room Mode:</span>
                            <span class="text-emerald-400">100% Sensor Auto-Kill</span>
                        </div>
                        <div class="flex justify-between text-zinc-400">
                            <span>Occupied Room Mode:</span>
                            <span class="text-blue-400">100% Manual User Control</span>
                        </div>
                        <div class="flex justify-between text-zinc-400">
                            <span>Geyser Staggering:</span>
                            <span class="text-zinc-200">Wing 1 (5:30) / Wing 2 (6:30)</span>
                        </div>
                    </div>
                </div>
                <div class="mt-4 pt-3 border-t border-white/5 flex justify-between items-center text-xs font-mono-code text-zinc-400">
                    <span>Demand Breach</span>
                    <span class="text-emerald-400 font-bold">Zero Violations</span>
                </div>
            </div>

            <div class="p-5 neu-card flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between pb-3 mb-3 border-b border-white/5">
                        <span class="text-xs font-mono-code font-bold text-cyan-400">CAMPUS // 15 COOLERS</span>
                        <span class="px-2.5 py-1 text-[11px] font-mono-code font-bold rounded-md neu-inset text-emerald-400">WIS: 05 / ISOLATED</span>
                    </div>
                    <div class="text-base font-semibold text-white">Commercial Cooling Units</div>
                    <div class="text-xs text-zinc-400 mt-0.5">Module F Interlocked Timers</div>

                    <div class="mt-4 space-y-2 text-xs font-mono-code neu-inset p-3">
                        <div class="flex justify-between text-zinc-400">
                            <span>Night Cut-off:</span>
                            <span class="text-zinc-200">19:00 - 07:00 Daily</span>
                        </div>
                        <div class="flex justify-between text-zinc-400">
                            <span>Sunday Policy:</span>
                            <span class="text-emerald-400">100% Locked OFF</span>
                        </div>
                        <div class="flex justify-between text-zinc-400">
                            <span>Thermal Buffer:</span>
                            <span class="text-blue-400">2+ Hours Chill Retention</span>
                        </div>
                    </div>
                </div>
                <div class="mt-4 pt-3 border-t border-white/5 flex justify-between items-center text-xs font-mono-code text-zinc-400">
                    <span>Monthly Savings</span>
                    <span class="text-emerald-400 font-bold">1,620 kWh (INR 14.5K)</span>
                </div>
            </div>

            <div class="p-5 neu-card flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between pb-3 mb-3 border-b border-white/5">
                        <span class="text-xs font-mono-code font-bold text-emerald-400">NETWORK // 150 APs</span>
                        <span class="px-2.5 py-1 text-[11px] font-mono-code font-bold rounded-md neu-inset text-emerald-400">WIS: 10 / GREEN</span>
                    </div>
                    <div class="text-base font-semibold text-white">Enterprise PoE WiFi Grid</div>
                    <div class="text-xs text-zinc-400 mt-0.5">Module H Radio Throttling</div>

                    <div class="mt-4 space-y-2 text-xs font-mono-code neu-inset p-3">
                        <div class="flex justify-between text-zinc-400">
                            <span>Academic APs:</span>
                            <span class="text-amber-400">5 GHz Radios Disabled</span>
                        </div>
                        <div class="flex justify-between text-zinc-400">
                            <span>Off-Hours Mode:</span>
                            <span class="text-emerald-400">2.4 GHz Only (&lt;5W)</span>
                        </div>
                        <div class="flex justify-between text-zinc-400">
                            <span>Hostel APs:</span>
                            <span class="text-zinc-200">Full 24/7 Bandwidth</span>
                        </div>
                    </div>
                </div>
                <div class="mt-4 pt-3 border-t border-white/5 flex justify-between items-center text-xs font-mono-code text-zinc-400">
                    <span>Monthly Potential</span>
                    <span class="text-emerald-400 font-bold">2,700 kWh</span>
                </div>
            </div>
        </div>

    </main>

    <footer class="py-4 px-6 border-t border-white/5 bg-[#14151a] text-xs font-mono-code text-zinc-400">
        <div class="max-w-7xl mx-auto flex flex-col sm:flex-row justify-between items-center gap-2">
            <span>GridSense v1.0 // JIT Campus Architecture</span>
            <span>Zero Watermarks // Neumorphic Protocol</span>
        </div>
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
                                borderColor: 'rgba(239, 68, 68, 0.75)',
                                backgroundColor: 'transparent',
                                borderWidth: 2,
                                pointRadius: 0,
                                tension: 0.2
                            }},
                            {{
                                label: 'GridSense (kW)',
                                data: gridsenseData,
                                borderColor: 'rgba(16, 185, 129, 0.9)',
                                backgroundColor: 'rgba(16, 185, 129, 0.08)',
                                fill: true,
                                borderWidth: 2,
                                pointRadius: 0,
                                tension: 0.2
                            }}
                        ]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        interaction: {{ intersect: false, mode: 'index' }},
                        plugins: {{ legend: {{ display: false }} }},
                        scales: {{
                            x: {{
                                grid: {{ color: 'rgba(255, 255, 255, 0.03)' }},
                                ticks: {{ color: '#71717a', font: {{ family: 'JetBrains Mono', size: 10 }}, maxTicksLimit: 14 }}
                            }},
                            y: {{
                                title: {{ display: true, text: 'Total kW Draw', color: '#71717a', font: {{ family: 'Inter', size: 11 }} }},
                                grid: {{ color: 'rgba(255, 255, 255, 0.03)' }},
                                ticks: {{ color: '#71717a', font: {{ family: 'JetBrains Mono', size: 10 }} }}
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
            <div class='p-3 neu-inset rounded-lg text-xs font-mono-code mb-2'>
                <div class='font-bold text-blue-400'>{z.get('name', '')} (ID: {z.get('id', '')})</div>
                <div class='text-zinc-400 text-[11px] mt-1'>Capacity: {z.get('capacity', 'N/A')} | Solutions: {', '.join(z.get('solution_mapping', []))}</div>
            </div>"""
        for lab in b_data.get("labs", []):
            zones_html += f"""
            <div class='p-3 neu-inset rounded-lg text-xs font-mono-code mb-2'>
                <div class='font-bold text-purple-400'>{lab.get('name', '')} (ID: {lab.get('id', '')})</div>
                <div class='text-zinc-400 text-[11px] mt-1'>PCs: {lab.get('pc_count', '')} (Active: {lab.get('pc_active_watts', '')}W, Sleep: {lab.get('pc_sleep_watts', '')}W) | Solutions: {', '.join(lab.get('solution_mapping', []))}</div>
            </div>"""
        for w in b_data.get("wings", []):
            stagger = w.get("geyser_bank", {}).get("stagger_slot", "")
            zones_html += f"""
            <div class='p-3 neu-inset rounded-lg text-xs font-mono-code mb-2'>
                <div class='font-bold text-red-400'>{w.get('name', '')} (ID: {w.get('id', '')})</div>
                <div class='text-zinc-400 text-[11px] mt-1'>Rooms: {w.get('rooms_count', '')} | Presence Sensing: Dual-Tech PIR</div>
                <div class='text-emerald-400 text-[11px] mt-1'>Policy: Vacant = Auto-Kill | Occupied = 100% Manual User Control</div>
                <div class='text-zinc-400 text-[11px] mt-1'>Geyser Slot: {stagger}</div>
            </div>"""
        for wc in b_data.get("water_coolers", []):
            zones_html += f"""
            <div class='p-2 neu-inset rounded text-[11px] font-mono-code text-zinc-400 mb-1 flex justify-between'>
                <span>Commercial Water Cooler {wc.get('id', '')} (Floor {wc.get('floor', '')})</span>
                <span class='text-amber-400 font-bold'>{wc.get('compressor_kw', '')} kW | Interlocked 19:00 - 07:00</span>
            </div>"""
        for hm in b_data.get("heavy_motors", []):
            zones_html += f"""
            <div class='p-2 neu-inset rounded text-[11px] font-mono-code text-zinc-400 mb-1 flex justify-between'>
                <span>{hm.get('name', '')}</span>
                <span class='text-cyan-400 font-bold'>{hm.get('kw', '')} kW | Shifted to Solar Window</span>
            </div>"""

        elev_info = ""
        if "elevator_bank" in b_data:
            eb = b_data["elevator_bank"]
            elev_info = f"""
            <div class='p-3 neu-inset rounded-lg text-xs font-mono-code mb-2'>
                <div class='font-bold text-amber-400'>4-Lift Elevator Bank (ID: {eb.get('id', '')})</div>
                <div class='text-zinc-400 text-[11px] mt-1'>Total Cars: {eb.get('total_cars')} | Mandatory Active Safety Floor: {eb.get('mandatory_safety_floor')} Cars</div>
                <div class='text-zinc-400 text-[11px]'>Motor Rating: {eb.get('car_rating_motor_kw')} kW | Standby Parasitic: {eb.get('standby_parasitic_kw')} kW</div>
            </div>"""

        blocks_html += f"""
        <div class='p-6 neu-card mb-6'>
            <div class='flex items-center justify-between pb-3 mb-3 border-b border-white/5'>
                <h3 class='text-lg font-bold text-white'>{b_name}</h3>
                <span class='text-xs font-mono-code text-emerald-400'>{len(b_data.get('zones', [])) + len(b_data.get('labs', [])) + len(b_data.get('wings', []))} Managed Asset Groups</span>
            </div>
            <p class='text-xs text-zinc-400 mb-4'>{b_data.get('description', '')}</p>
            {elev_info}
            {zones_html}
        </div>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>JIT Campus Physical Blueprint // GridSense</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Inter', sans-serif;
            background-color: #16181d;
            color: #d1d5db;
        }}
        .font-mono-code {{ font-family: 'JetBrains Mono', monospace; }}
        .neu-card {{
            background: #191b22;
            border-radius: 16px;
            box-shadow: 8px 8px 18px #0f1014, -8px -8px 18px #232630;
            border: 1px solid rgba(255, 255, 255, 0.03);
        }}
        .neu-inset {{
            background: #14151a;
            border-radius: 12px;
            box-shadow: inset 4px 4px 10px #0c0d10, inset -4px -4px 10px #1c1d24;
            border: 1px solid rgba(255, 255, 255, 0.02);
        }}
        .neu-btn {{
            background: #191b22;
            border-radius: 10px;
            box-shadow: 4px 4px 10px #0f1014, -4px -4px 10px #232630;
            border: 1px solid rgba(255, 255, 255, 0.04);
            transition: all 0.2s ease;
        }}
        .neu-btn:hover {{
            color: #10b981;
        }}
    </style>
</head>
<body class="min-h-screen p-6 sm:p-10 max-w-5xl mx-auto">
    <div class="flex items-center justify-between mb-8 pb-4 border-b border-white/5">
        <div>
            <div class="text-xs font-mono-code font-bold text-emerald-400 uppercase tracking-widest">Physical Asset Hierarchy // Digital Twin</div>
            <h1 class="text-2xl sm:text-4xl font-bold text-white tracking-tight mt-1">JIT Campus Blueprint</h1>
            <p class="text-xs text-zinc-400 font-mono-code mt-1">Institution: JIT | Commercial Tariff: INR 9.00/kWh | Max Demand Limit: 250 kVA</p>
        </div>
        <a href="/" class="px-4 py-2 neu-btn font-mono-code text-xs font-semibold text-zinc-300">
            Back to Dashboard
        </a>
    </div>

    {blocks_html}
</body>
</html>
"""
