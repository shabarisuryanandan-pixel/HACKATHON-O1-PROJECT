from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
import os
import json
import urllib.request
from dotenv import load_dotenv
from campus_blueprint import CAMPUS_BLUEPRINT, CAMPUS_METADATA
from sandbox_engine import evaluate_sandbox_state

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://rzdrqgwmmfliyksuiknx.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "sb_publishable_LPVQ_Mzxl8AK8c_JLhMNAw_CoumpNyK")

app = FastAPI(title="GridSense: Campus Intelligent Energy Optimization")

TELEMETRY_DATA = {}
if os.path.exists("synthetic_telemetry.json"):
    try:
        with open("synthetic_telemetry.json", "r") as f:
            TELEMETRY_DATA = json.load(f)
    except Exception as e:
        print("Error loading telemetry:", e)

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

        /* Neumorphic Extruded Surface (Cards & Buttons) */
        .neu-card {{
            background: #191b22;
            border-radius: 16px;
            box-shadow: 8px 8px 18px #0f1014, -8px -8px 18px #232630;
            border: 1px solid rgba(255, 255, 255, 0.03);
        }}

        /* Neumorphic Inset Well (Meters, Display Panels, Input Wells) */
        .neu-inset {{
            background: #14151a;
            border-radius: 14px;
            box-shadow: inset 5px 5px 12px #0c0d10, inset -5px -5px 12px #1c1d24;
            border: 1px solid rgba(255, 255, 255, 0.02);
        }}

        /* Neumorphic Raised Button */
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
        .neu-btn:active {{
            box-shadow: inset 4px 4px 8px #0c0d10, inset -4px -4px 8px #1c1d24;
        }}

        /* Subtle Glow Accents */
        .glow-emerald {{
            box-shadow: 0 0 12px rgba(16, 185, 129, 0.25);
        }}
    </style>
</head>
<body class="min-h-screen flex flex-col justify-between selection:bg-emerald-500 selection:text-black">

    <!-- TOP HEADER -->
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

    <!-- MAIN BODY -->
    <main class="w-full max-w-7xl mx-auto px-4 sm:px-6 py-8 flex-1">

        <!-- STATS ROW -->
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

        <!-- 7-DAY LOAD CURVE (INSET WELL) -->
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

        <!-- MANAGED ZONES GRID -->
        <div class="mb-5 flex justify-between items-end">
            <div>
                <h2 class="text-xl font-bold text-white tracking-tight">Campus Telemetry Nodes</h2>
                <p class="text-xs text-zinc-400 font-mono-code mt-0.5">Live Waste Index Score (WIS) & active automated interventions</p>
            </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">

            <!-- ZONE 1: LECTURE B101 -->
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

            <!-- ZONE 2: LAB C1 -->
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

            <!-- ZONE 3: ELEVATORS -->
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

            <!-- ZONE 4: HOSTEL RESIDENCE -->
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

            <!-- ZONE 5: WATER COOLERS -->
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

            <!-- ZONE 6: ENTERPRISE WIFI -->
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

    <!-- FOOTER -->
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
        token = body.get("token", "").strip()
        chat_id = body.get("chat_id", "").strip()
        message = body.get("message", "GridSense Automation Alert")

        if not token or not chat_id:
            return {"status": "error", "message": "Bot token and Chat ID are required."}

        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = json.dumps({"chat_id": chat_id, "text": message}).encode("utf-8")
        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
        
        with urllib.request.urlopen(req, timeout=5) as response:
            res_data = json.loads(response.read().decode())
            if res_data.get("ok"):
                return {"status": "success", "message": "Alert sent to phone successfully."}
            else:
                return {"status": "error", "message": "Telegram API returned failure."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/sandbox", response_class=HTMLResponse)
def view_sandbox():
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GridSense // Interactive Simulation & Testing Sandbox</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Inter', sans-serif;
            background-color: #14161b;
            color: #d1d5db;
        }}
        .font-mono-code {{ font-family: 'JetBrains Mono', monospace; }}
        .neu-card {{
            background: #181a20;
            border-radius: 16px;
            box-shadow: 8px 8px 18px #0d0e12, -8px -8px 18px #23262e;
            border: 1px solid rgba(255, 255, 255, 0.03);
        }}
        .neu-inset {{
            background: #131418;
            border-radius: 12px;
            box-shadow: inset 4px 4px 10px #0a0b0d, inset -4px -4px 10px #1c1d23;
            border: 1px solid rgba(255, 255, 255, 0.02);
        }}
        .neu-btn {{
            background: #181a20;
            border-radius: 10px;
            box-shadow: 4px 4px 10px #0d0e12, -4px -4px 10px #23262e;
            border: 1px solid rgba(255, 255, 255, 0.04);
            transition: all 0.15s ease;
        }}
        .neu-btn:hover {{ color: #10b981; }}
        .neu-btn:active {{
            box-shadow: inset 3px 3px 6px #0a0b0d, inset -3px -3px 6px #1c1d23;
        }}

        /* Room Glow Effect for Lights ON */
        .room-lit {{
            background: radial-gradient(circle at center, rgba(251, 191, 36, 0.18) 0%, rgba(24, 26, 32, 0.95) 85%);
            border: 1.5px solid rgba(251, 191, 36, 0.45) !important;
            box-shadow: 0 0 16px rgba(251, 191, 36, 0.15), inset 0 0 12px rgba(251, 191, 36, 0.08);
        }}
        .room-dark {{
            background: #111216;
            border: 1px solid rgba(255, 255, 255, 0.04) !important;
            opacity: 0.55;
        }}
        .corridor-lit {{
            background: rgba(251, 191, 36, 0.12);
            border: 1px solid rgba(251, 191, 36, 0.3);
        }}
        .corridor-dark {{
            background: #0f1013;
            border: 1px dashed rgba(255, 255, 255, 0.05);
            opacity: 0.4;
        }}
    </style>
</head>
<body class="min-h-screen p-4 sm:p-8 max-w-7xl mx-auto">

    <!-- HEADER NAVIGATION -->
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-8 pb-4 border-b border-white/5">
        <div>
            <div class="text-xs font-mono-code font-bold text-emerald-400 uppercase tracking-widest">Interactive Testing Sandbox // Digital Twin Simulation</div>
            <h1 class="text-2xl sm:text-3xl font-bold text-white tracking-tight mt-1">Block A & B Architectural Simulation</h1>
            <p class="text-xs text-zinc-400 font-mono-code mt-0.5">Adjust environmental inputs, stress-test occupancy, and observe real-time spatial consolidation</p>
        </div>
        <div class="flex items-center gap-3">
            <a href="/" class="px-4 py-2 neu-btn font-mono-code text-xs font-semibold text-zinc-300">
                Back to Dashboard
            </a>
        </div>
    </div>

    <!-- MAIN TWO-COLUMN LAYOUT -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">

        <!-- LEFT COLUMN: CONTROLS & TEST PARAMS (4 COLS) -->
        <div class="lg:col-span-4 space-y-6">

            <!-- PRESET QUICK SELECTOR -->
            <div class="p-5 neu-card">
                <div class="text-xs font-mono-code uppercase text-zinc-400 mb-3 font-bold">1. Quick Scenario Presets</div>
                <div class="grid grid-cols-3 gap-2">
                    <button onclick="applyPreset('morning')" class="py-2 px-1 neu-btn text-[11px] font-mono-code font-bold text-zinc-300 text-center">
                        09:00 AM<br><span class="text-[9px] text-zinc-500 font-normal">Morning Peak</span>
                    </button>
                    <button onclick="applyPreset('afternoon')" class="py-2 px-1 neu-btn text-[11px] font-mono-code font-bold text-zinc-300 text-center">
                        02:30 PM<br><span class="text-[9px] text-zinc-500 font-normal">Afternoon Heat</span>
                    </button>
                    <button onclick="applyPreset('night_waste')" class="py-2 px-1 neu-btn text-[11px] font-mono-code font-bold text-amber-400 text-center">
                        07:30 PM<br><span class="text-[9px] text-zinc-500 font-normal">Stray Late Class</span>
                    </button>
                </div>
            </div>

            <!-- TIME & ENVIRONMENT SLIDERS -->
            <div class="p-5 neu-card space-y-4">
                <div class="text-xs font-mono-code uppercase text-zinc-400 font-bold">2. Environmental Inputs</div>
                
                <div>
                    <div class="flex justify-between text-xs font-mono-code mb-1">
                        <span class="text-zinc-400">Time of Day</span>
                        <span id="timeVal" class="text-emerald-400 font-bold">19:30</span>
                    </div>
                    <input type="range" id="timeSlider" min="6" max="23" step="0.5" value="19.5" oninput="onParamChange()" class="w-full accent-emerald-500 cursor-pointer">
                </div>

                <div>
                    <div class="flex justify-between text-xs font-mono-code mb-1">
                        <span class="text-zinc-400">Outdoor Temperature</span>
                        <span id="tempVal" class="text-amber-400 font-bold">33°C</span>
                    </div>
                    <input type="range" id="tempSlider" min="20" max="40" step="1" value="33" oninput="onParamChange()" class="w-full accent-amber-500 cursor-pointer">
                </div>

                <div>
                    <div class="text-xs font-mono-code text-zinc-400 mb-1">Weather / Sky Condition</div>
                    <select id="weatherSelect" onchange="onParamChange()" class="w-full p-2.5 neu-inset text-xs font-mono-code text-zinc-200 outline-none">
                        <option value="Sunny / Daylight">Sunny / Daylight (High Lux)</option>
                        <option value="Overcast / Rainy">Overcast / Rainy (Low Ambient Lux)</option>
                        <option value="Night" selected>Night (Zero Daylight)</option>
                    </select>
                </div>
            </div>

            <!-- CLASSROOM OCCUPANCY INPUTS -->
            <div class="p-5 neu-card space-y-3">
                <div class="text-xs font-mono-code uppercase text-zinc-400 font-bold">3. Headcount per Room</div>
                
                <div>
                    <div class="flex justify-between text-[11px] font-mono-code text-zinc-400">
                        <span>B101 (Floor 1 Entrance):</span>
                        <span id="occ_B101_val" class="text-white font-bold">0</span>
                    </div>
                    <input type="range" id="occ_B101" min="0" max="60" value="0" oninput="onParamChange()" class="w-full accent-blue-500 cursor-pointer">
                </div>

                <div>
                    <div class="flex justify-between text-[11px] font-mono-code text-zinc-400">
                        <span>B104 (Floor 1 Far Hallway):</span>
                        <span id="occ_B104_val" class="text-white font-bold">20</span>
                    </div>
                    <input type="range" id="occ_B104" min="0" max="60" value="20" oninput="onParamChange()" class="w-full accent-blue-500 cursor-pointer">
                </div>

                <div>
                    <div class="flex justify-between text-[11px] font-mono-code text-zinc-400">
                        <span>B204 (Floor 2 Far Hallway):</span>
                        <span id="occ_B204_val" class="text-white font-bold">0</span>
                    </div>
                    <input type="range" id="occ_B204" min="0" max="60" value="0" oninput="onParamChange()" class="w-full accent-blue-500 cursor-pointer">
                </div>

                <div>
                    <div class="flex justify-between text-[11px] font-mono-code text-zinc-400">
                        <span>A_SEM1 (Block A Seminar 1):</span>
                        <span id="occ_ASEM1_val" class="text-white font-bold">0</span>
                    </div>
                    <input type="range" id="occ_ASEM1" min="0" max="150" value="0" oninput="onParamChange()" class="w-full accent-blue-500 cursor-pointer">
                </div>
            </div>

            <!-- TELEGRAM BOT ALERT CONFIG -->
            <div class="p-5 neu-card space-y-3">
                <div class="text-xs font-mono-code uppercase text-zinc-400 font-bold">4. Telegram Mobile Ping</div>
                <p class="text-[11px] text-zinc-500 font-mono-code leading-relaxed">
                    Test live mobile push alerts. Paste your Telegram Bot Token & Chat ID below to receive real alerts on your phone.
                </p>
                <input type="text" id="tgToken" placeholder="Telegram Bot Token" class="w-full p-2.5 neu-inset text-[11px] font-mono-code text-zinc-200 outline-none">
                <input type="text" id="tgChatId" placeholder="Chat ID (e.g. 123456789)" class="w-full p-2.5 neu-inset text-[11px] font-mono-code text-zinc-200 outline-none">
                <button onclick="sendTelegramAlert()" class="w-full py-2.5 neu-btn text-xs font-mono-code font-bold text-emerald-400">
                    Send Live Test Ping to Mobile
                </button>
                <div id="tgStatus" class="text-[10px] font-mono-code text-zinc-500 text-center"></div>
            </div>

        </div>

        <!-- RIGHT COLUMN: VISUAL FLOOR PLAN & TELEMETRY GAUGES (8 COLS) -->
        <div class="lg:col-span-8 space-y-6">

            <!-- BEFORE VS AFTER COMPARISON GAUGES -->
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div class="p-4 neu-card">
                    <div class="text-[11px] font-mono-code uppercase text-zinc-500">Unmanaged Baseline</div>
                    <div id="baselineMeter" class="text-2xl font-bold text-red-400 mt-1">23.00 kW</div>
                    <div class="text-[11px] text-zinc-500 font-mono-code mt-0.5">Fixed 20°C AC + All Lights</div>
                </div>

                <div class="p-4 neu-card">
                    <div class="text-[11px] font-mono-code uppercase text-zinc-500">GridSense Optimized</div>
                    <div id="optimizedMeter" class="text-2xl font-bold text-emerald-400 mt-1">6.19 kW</div>
                    <div class="text-[11px] text-zinc-500 font-mono-code mt-0.5">Consolidated + Adaptive</div>
                </div>

                <div class="p-4 neu-card">
                    <div class="text-[11px] font-mono-code uppercase text-zinc-500">Immediate Savings Rate</div>
                    <div id="savingsMeter" class="text-2xl font-bold text-yellow-400 mt-1">16.81 kW</div>
                    <div id="inrMeter" class="text-[11px] text-emerald-400 font-mono-code mt-0.5">INR 151.29 / Hour</div>
                </div>
            </div>

            <!-- AUTOMATION ALERT POPUP CARD -->
            <div id="alertCard" class="p-4 neu-card border-l-4 border-l-yellow-400 flex items-start justify-between gap-4">
                <div>
                    <div class="flex items-center gap-2 text-xs font-mono-code font-bold text-yellow-400 uppercase">
                        <span class="w-2 h-2 rounded-full bg-yellow-400 animate-ping"></span>
                        Spatial Consolidation Nudge Triggered
                    </div>
                    <p id="alertText" class="text-xs font-mono-code text-zinc-300 mt-1">
                        Class in B104 isolated in far hallway. Relocate to B101 near staircase to darken 40m corridor.
                    </p>
                </div>
                <button onclick="applyConsolidation()" class="px-3 py-1.5 neu-btn text-xs font-mono-code font-bold text-emerald-400 shrink-0">
                    Apply Move
                </button>
            </div>

            <!-- ARCHITECTURAL BLUEPRINT 2D CANVAS -->
            <div class="p-6 neu-card space-y-6">
                <div class="flex justify-between items-center border-b border-white/5 pb-3">
                    <div>
                        <h2 class="text-base font-bold text-white tracking-tight">Block B: 2D Architectural Layout</h2>
                        <p class="text-xs text-zinc-400 font-mono-code">Visualizing real-time light illumination, corridor relay zones, and HVAC setpoints</p>
                    </div>
                    <div id="elevState" class="text-[11px] font-mono-code text-zinc-400 neu-inset px-3 py-1">
                        Elevators: 2 Active (Mandatory Safety Floor)
                    </div>
                </div>

                <!-- FLOOR 1 BLUEPRINT -->
                <div>
                    <div class="text-xs font-mono-code font-bold text-zinc-400 uppercase mb-2">Floor 1 Layout (Arterial 80m Corridor)</div>
                    <div class="grid grid-cols-12 gap-3">
                        
                        <!-- STAIRCASE & ENTRANCE -->
                        <div class="col-span-2 p-3 neu-inset flex flex-col justify-center items-center text-center">
                            <span class="text-xs font-mono-code font-bold text-zinc-400">MAIN STAIRS & ELEVATORS</span>
                            <span class="text-[10px] font-mono-code text-emerald-400 mt-1">4-Car Bank</span>
                        </div>

                        <!-- ROOM B101 (NEAR ENTRANCE) -->
                        <div id="card_B101" class="col-span-3 p-4 rounded-xl transition-all duration-300 flex flex-col justify-between room-dark">
                            <div class="flex justify-between items-start">
                                <span class="text-xs font-mono-code font-bold text-white">B101</span>
                                <span id="tag_B101" class="text-[9px] font-mono-code font-bold px-1.5 py-0.5 rounded bg-black/40 text-zinc-400">OFF</span>
                            </div>
                            <div class="my-2">
                                <div id="occ_B101_txt" class="text-xs font-bold text-zinc-300 font-mono-code">0 Students</div>
                                <div id="ac_B101_txt" class="text-[10px] font-mono-code text-zinc-400">AC: STANDBY</div>
                            </div>
                            <div class="text-[9px] font-mono-code text-zinc-500">Daylight: East</div>
                        </div>

                        <!-- ROOM B102 -->
                        <div id="card_B102" class="col-span-3 p-4 rounded-xl transition-all duration-300 flex flex-col justify-between room-dark">
                            <div class="flex justify-between items-start">
                                <span class="text-xs font-mono-code font-bold text-white">B102</span>
                                <span id="tag_B102" class="text-[9px] font-mono-code font-bold px-1.5 py-0.5 rounded bg-black/40 text-zinc-400">OFF</span>
                            </div>
                            <div class="my-2">
                                <div id="occ_B102_txt" class="text-xs font-bold text-zinc-300 font-mono-code">0 Students</div>
                                <div id="ac_B102_txt" class="text-[10px] font-mono-code text-zinc-400">AC: STANDBY</div>
                            </div>
                            <div class="text-[9px] font-mono-code text-zinc-500">Daylight: North</div>
                        </div>

                        <!-- ROOM B104 (FAR END) -->
                        <div id="card_B104" class="col-span-4 p-4 rounded-xl transition-all duration-300 flex flex-col justify-between room-lit">
                            <div class="flex justify-between items-start">
                                <span class="text-xs font-mono-code font-bold text-white">B104 (Far End)</span>
                                <span id="tag_B104" class="text-[9px] font-mono-code font-bold px-1.5 py-0.5 rounded bg-black/40 text-amber-300">LIT</span>
                            </div>
                            <div class="my-2">
                                <div id="occ_B104_txt" class="text-xs font-bold text-amber-200 font-mono-code">20 Students</div>
                                <div id="ac_B104_txt" class="text-[10px] font-mono-code text-zinc-300">AC: 26°C Adaptive</div>
                            </div>
                            <div class="text-[9px] font-mono-code text-amber-400 font-semibold">Corridor Draw: Active</div>
                        </div>

                    </div>

                    <!-- 3-ZONE CORRIDOR LIGHTING STRIP -->
                    <div class="mt-3 grid grid-cols-12 gap-1 text-center font-mono-code text-[10px] py-1">
                        <div id="corridor_z1" class="col-span-4 py-1.5 rounded corridor-lit text-amber-300 font-bold">
                            Corridor Zone 1 (Entrance) [LIT]
                        </div>
                        <div id="corridor_z2" class="col-span-4 py-1.5 rounded corridor-lit text-amber-300 font-bold">
                            Corridor Zone 2 (Mid-Way) [LIT]
                        </div>
                        <div id="corridor_z3" class="col-span-4 py-1.5 rounded corridor-lit text-amber-300 font-bold">
                            Corridor Zone 3 (Far End) [LIT]
                        </div>
                    </div>
                </div>

                <!-- BLOCK A OVERVIEW (SEMINAR HALLS) -->
                <div class="pt-4 border-t border-white/5">
                    <div class="text-xs font-mono-code font-bold text-zinc-400 uppercase mb-2">Block A (Executive Wing)</div>
                    <div class="grid grid-cols-2 gap-4">
                        <div id="card_ASEM1" class="p-4 rounded-xl transition-all duration-300 room-dark">
                            <div class="flex justify-between">
                                <span class="text-xs font-mono-code font-bold text-white">Seminar Hall 1</span>
                                <span id="tag_ASEM1" class="text-[9px] font-mono-code font-bold px-1.5 py-0.5 rounded bg-black/40 text-zinc-400">OFF</span>
                            </div>
                            <div class="text-[11px] font-mono-code text-zinc-400 mt-2">Capacity: 150 | 4x 2.0 Ton ACs</div>
                            <div id="ac_ASEM1_txt" class="text-[10px] font-mono-code text-zinc-500 mt-1">AC: Isolated at Distribution Board</div>
                        </div>

                        <div id="card_ASEM2" class="p-4 rounded-xl transition-all duration-300 room-dark">
                            <div class="flex justify-between">
                                <span class="text-xs font-mono-code font-bold text-white">Seminar Hall 2</span>
                                <span class="text-[9px] font-mono-code font-bold px-1.5 py-0.5 rounded bg-black/40 text-zinc-400">OFF</span>
                            </div>
                            <div class="text-[11px] font-mono-code text-zinc-400 mt-2">Capacity: 120 | 3x 2.0 Ton ACs</div>
                            <div class="text-[10px] font-mono-code text-zinc-500 mt-1">AC: Isolated at Distribution Board</div>
                        </div>
                    </div>
                </div>

            </div>

        </div>

    </div>

    <!-- JAVASCRIPT CONTROLLER -->
    <script>
        let currentRelocations = [];

        function onParamChange() {{
            const timeVal = parseFloat(document.getElementById('timeSlider').value);
            const hours = Math.floor(timeVal);
            const mins = (timeVal % 1 === 0.5) ? "30" : "00";
            const timeStr = `${{hours < 10 ? '0' + hours : hours}}:${{mins}}`;
            document.getElementById('timeVal').innerText = timeStr;

            const temp = document.getElementById('tempSlider').value;
            document.getElementById('tempVal').innerText = `${{temp}}°C`;

            const weather = document.getElementById('weatherSelect').value;

            // Update occupancy labels
            const occ_B101 = parseInt(document.getElementById('occ_B101').value);
            const occ_B104 = parseInt(document.getElementById('occ_B104').value);
            const occ_B204 = parseInt(document.getElementById('occ_B204').value);
            const occ_ASEM1 = parseInt(document.getElementById('occ_ASEM1').value);

            document.getElementById('occ_B101_val').innerText = occ_B101;
            document.getElementById('occ_B104_val').innerText = occ_B104;
            document.getElementById('occ_B204_val').innerText = occ_B204;
            document.getElementById('occ_ASEM1_val').innerText = occ_ASEM1;

            const payload = {{
                time: timeStr,
                temperature: parseFloat(temp),
                weather: weather,
                rooms: {{
                    "B101": occ_B101,
                    "B104": occ_B104,
                    "B204": occ_B204,
                    "A_SEM1": occ_ASEM1
                }}
            }};

            fetch('/api/sandbox/evaluate', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify(payload)
            }})
            .then(res => res.json())
            .then(data => renderSandboxState(data))
            .catch(err => console.error(err));
        }}

        function renderSandboxState(data) {{
            document.getElementById('baselineMeter').innerText = `${{data.total_baseline_kw}} kW`;
            document.getElementById('optimizedMeter').innerText = `${{data.total_optimized_kw}} kW`;
            document.getElementById('savingsMeter').innerText = `${{data.kw_saved}} kW (${{data.savings_percentage}}%)`;
            document.getElementById('inrMeter').innerText = `INR ${{data.inr_per_hour_saved}} / Hour`;
            document.getElementById('elevState').innerText = data.elevator_mode;

            // Render room states
            const rooms = data.rooms;
            for (let r_id in rooms) {{
                const r = rooms[r_id];
                const card = document.getElementById(`card_${{r_id}}`);
                const tag = document.getElementById(`tag_${{r_id}}`);
                const occTxt = document.getElementById(`occ_${{r_id}}_txt`);
                const acTxt = document.getElementById(`ac_${{r_id}}_txt`);

                if (card && tag) {{
                    if (r.lighting_glow) {{
                        card.className = card.className.replace('room-dark', 'room-lit');
                        tag.innerText = "LIT";
                        tag.className = "text-[9px] font-mono-code font-bold px-1.5 py-0.5 rounded bg-black/40 text-amber-300";
                    }} else {{
                        card.className = card.className.replace('room-lit', 'room-dark');
                        tag.innerText = "OFF";
                        tag.className = "text-[9px] font-mono-code font-bold px-1.5 py-0.5 rounded bg-black/40 text-zinc-500";
                    }}
                }}

                if (occTxt) occTxt.innerText = `${{r.occupancy}} Students`;
                if (acTxt) acTxt.innerText = `AC: ${{r.ac_mode}}`;
            }}

            // Render corridor zones
            const cz = data.corridor_state;
            updateCorridorZone('corridor_z1', cz.floor1_zone1_entrance === "ON");
            updateCorridorZone('corridor_z2', cz.floor1_zone2_mid === "ON");
            updateCorridorZone('corridor_z3', cz.floor1_zone3_far === "ON");

            // Handle Relocation Alerts
            currentRelocations = data.relocations || [];
            const alertCard = document.getElementById('alertCard');
            const alertText = document.getElementById('alertText');

            if (currentRelocations.length > 0) {{
                alertCard.style.display = "flex";
                alertText.innerText = currentRelocations[0].reason;
            }} else {{
                alertCard.style.display = "none";
            }}
        }}

        function updateCorridorZone(elemId, isLit) {{
            const el = document.getElementById(elemId);
            if (!el) return;
            if (isLit) {{
                el.className = "col-span-4 py-1.5 rounded corridor-lit text-amber-300 font-bold";
                el.innerText = el.innerText.replace('[DARK]', '[LIT]').replace('[LIT]', '[LIT]');
            }} else {{
                el.className = "col-span-4 py-1.5 rounded corridor-dark text-zinc-600 font-normal";
                el.innerText = el.innerText.replace('[LIT]', '[DARK]').replace('[DARK]', '[DARK]');
            }}
        }}

        function applyConsolidation() {{
            if (currentRelocations.length > 0) {{
                // Move headcount from B104 to B101
                const students = parseInt(document.getElementById('occ_B104').value);
                document.getElementById('occ_B104').value = 0;
                document.getElementById('occ_B101').value = students;
                onParamChange();
            }}
        }}

        function applyPreset(type) {{
            if (type === 'morning') {{
                document.getElementById('timeSlider').value = 9.5;
                document.getElementById('tempSlider').value = 27;
                document.getElementById('weatherSelect').value = "Sunny / Daylight";
                document.getElementById('occ_B101').value = 45;
                document.getElementById('occ_B104').value = 40;
                document.getElementById('occ_ASEM1').value = 0;
            }} else if (type === 'afternoon') {{
                document.getElementById('timeSlider').value = 14.5;
                document.getElementById('tempSlider').value = 36;
                document.getElementById('weatherSelect').value = "Sunny / Daylight";
                document.getElementById('occ_B101').value = 30;
                document.getElementById('occ_B104').value = 0;
                document.getElementById('occ_ASEM1').value = 80;
            }} else if (type === 'night_waste') {{
                document.getElementById('timeSlider').value = 19.5;
                document.getElementById('tempSlider').value = 31;
                document.getElementById('weatherSelect').value = "Night";
                document.getElementById('occ_B101').value = 0;
                document.getElementById('occ_B104').value = 20; // Isolated in far hallway!
                document.getElementById('occ_ASEM1').value = 0;
            }}
            onParamChange();
        }}

        function sendTelegramAlert() {{
            const token = document.getElementById('tgToken').value.trim();
            const chatId = document.getElementById('tgChatId').value.trim();
            const statusDiv = document.getElementById('tgStatus');

            if (!token || !chatId) {{
                statusDiv.innerText = "Please provide both Bot Token and Chat ID.";
                statusDiv.className = "text-[10px] font-mono-code text-red-400 text-center";
                return;
            }}

            statusDiv.innerText = "Dispatching alert to mobile...";
            statusDiv.className = "text-[10px] font-mono-code text-yellow-400 text-center";

            fetch('/api/sandbox/notify-telegram', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{
                    token: token,
                    chat_id: chatId,
                    message: "GridSense Alert [JIT Campus]: Spatial Consolidation Triggered. Class B104 shifted to B101 near entrance. 40m corridor lighting de-energized. Instant savings: 16.8 kW (INR 151.29/hr)."
                }})
            }})
            .then(res => res.json())
            .then(data => {{
                if (data.status === "success") {{
                    statusDiv.innerText = "Alert delivered to phone successfully.";
                    statusDiv.className = "text-[10px] font-mono-code text-emerald-400 text-center";
                }} else {{
                    statusDiv.innerText = `Error: ${{data.message}}`;
                    statusDiv.className = "text-[10px] font-mono-code text-red-400 text-center";
                }}
            }})
            .catch(err => {{
                statusDiv.innerText = "Network error communicating with Telegram.";
                statusDiv.className = "text-[10px] font-mono-code text-red-400 text-center";
            }});
        }}

        // Run initial evaluation on load
        window.onload = () => onParamChange();
    </script>
</body>
</html>
"""

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
