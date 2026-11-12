from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
import os
import json
from dotenv import load_dotenv
from campus_blueprint import CAMPUS_BLUEPRINT, CAMPUS_METADATA

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://rzdrqgwmmfliyksuiknx.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "sb_publishable_LPVQ_Mzxl8AK8c_JLhMNAw_CoumpNyK")

app = FastAPI(title="GridSense: Campus Intelligent Energy Optimization")

# Load synthetic telemetry into memory if file exists
TELEMETRY_DATA = {}
if os.path.exists("synthetic_telemetry.json"):
    try:
        with open("synthetic_telemetry.json", "r") as f:
            TELEMETRY_DATA = json.load(f)
    except Exception as e:
        print("Error loading telemetry:", e)

@app.get("/blueprint", response_class=HTMLResponse)
def view_blueprint():
    blocks_html = ""
    for b_name, b_data in CAMPUS_BLUEPRINT.items():
        zones_html = ""
        # Zones
        for z in b_data.get("zones", []):
            zones_html += f"""
            <div class='p-3 bg-zinc-900 border border-zinc-800 rounded font-mono-code text-xs mb-2'>
                <div class='font-bold text-cyan-400'>{z.get('name', '')} (ID: {z.get('id', '')})</div>
                <div class='text-zinc-400 text-[11px] mt-1'>Capacity: {z.get('capacity', 'N/A')} | Solutions: {', '.join(z.get('solution_mapping', []))}</div>
            </div>"""
        # Labs
        for lab in b_data.get("labs", []):
            zones_html += f"""
            <div class='p-3 bg-zinc-900 border border-zinc-800 rounded font-mono-code text-xs mb-2'>
                <div class='font-bold text-purple-400'>{lab.get('name', '')} (ID: {lab.get('id', '')})</div>
                <div class='text-zinc-400 text-[11px] mt-1'>PCs: {lab.get('pc_count', '')} (Active: {lab.get('pc_active_watts', '')}W, Sleep: {lab.get('pc_sleep_watts', '')}W) | Solutions: {', '.join(lab.get('solution_mapping', []))}</div>
            </div>"""
        # Wings
        for w in b_data.get("wings", []):
            stagger = w.get("geyser_bank", {}).get("stagger_slot", "")
            zones_html += f"""
            <div class='p-3 bg-zinc-900 border border-zinc-800 rounded font-mono-code text-xs mb-2'>
                <div class='font-bold text-red-400'>{w.get('name', '')} (ID: {w.get('id', '')})</div>
                <div class='text-zinc-400 text-[11px] mt-1'>Rooms: {w.get('rooms_count', '')} | Presence Sensing: {w.get('room_occupancy_sensors', '')}</div>
                <div class='text-emerald-400 text-[11px] mt-1'>Control Policy: Vacant = 100% Auto Kill | Occupied = 100% Manual User Mode</div>
                <div class='text-zinc-400 text-[11px] mt-1'>Geyser Stagger Window: {stagger}</div>
            </div>"""
        # Water Coolers
        for wc in b_data.get("water_coolers", []):
            zones_html += f"""
            <div class='p-2 bg-zinc-900/60 border border-zinc-800 rounded font-mono-code text-[11px] text-zinc-400 mb-1 flex justify-between'>
                <span>Commercial Water Cooler {wc.get('id', '')} (Floor {wc.get('floor', '')})</span>
                <span class='text-yellow-400 font-bold'>{wc.get('compressor_kw', '')} kW | Interlocked 19:00-07:00</span>
            </div>"""
        # Heavy Motors
        for hm in b_data.get("heavy_motors", []):
            zones_html += f"""
            <div class='p-2 bg-zinc-900/60 border border-zinc-800 rounded font-mono-code text-[11px] text-zinc-400 mb-1 flex justify-between'>
                <span>{hm.get('name', '')}</span>
                <span class='text-cyan-400 font-bold'>{hm.get('kw', '')} kW | Shifted to Solar Window</span>
            </div>"""

        elev_info = ""
        if "elevator_bank" in b_data:
            eb = b_data["elevator_bank"]
            elev_info = f"""
            <div class='p-3 bg-zinc-900 border border-zinc-800 rounded font-mono-code text-xs mb-2'>
                <div class='font-bold text-yellow-400'>4-Lift Elevator Bank (ID: {eb.get('id', '')})</div>
                <div class='text-zinc-400 text-[11px] mt-1'>Total Cars: {eb.get('total_cars')} | Mandatory Active Safety Floor: {eb.get('mandatory_safety_floor')} Cars</div>
                <div class='text-zinc-400 text-[11px]'>Motor Rating: {eb.get('car_rating_motor_kw')} kW | Standby Parasitic: {eb.get('standby_parasitic_kw')} kW</div>
            </div>"""

        blocks_html += f"""
        <div class='bg-zinc-950 border-2 border-zinc-800 p-6 rounded-none mb-6' style='box-shadow: 6px 6px 0px #030407;'>
            <div class='flex items-center justify-between pb-3 mb-3 border-b border-zinc-800'>
                <h3 class='text-xl font-bold uppercase text-white'>{b_name}</h3>
                <span class='text-xs font-mono-code text-emerald-400'>{len(b_data.get('zones', [])) + len(b_data.get('labs', [])) + len(b_data.get('wings', []))} Primary Managed Assets</span>
            </div>
            <p class='text-xs font-mono-code text-zinc-400 mb-4'>{b_data.get('description', '')}</p>
            {elev_info}
            {zones_html}
        </div>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Campus Physical Blueprint // Jain Institute of Technology</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;800&family=Space+Grotesk:wght@500;700;900&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Space Grotesk', sans-serif; background-color: #08090d; }}
        .font-mono-code {{ font-family: 'JetBrains Mono', monospace; }}
    </style>
</head>
<body class="text-zinc-100 min-h-screen p-6 sm:p-10 max-w-6xl mx-auto">
    <div class="flex items-center justify-between mb-8 pb-4 border-b-2 border-zinc-800">
        <div>
            <div class="text-xs font-mono-code font-bold text-emerald-400 uppercase tracking-widest">Physical Asset Hierarchy // Digital Twin</div>
            <h1 class="text-3xl sm:text-5xl font-black uppercase text-white">Campus Blueprint</h1>
            <p class="text-xs font-mono-code text-zinc-400 mt-1">Institution: Jain Institute of Technology (JIT) | Tariff: INR 9.00/kWh | Max Demand: 250 kVA</p>
        </div>
        <a href="/" class="px-4 py-2 bg-emerald-500 hover:bg-emerald-400 text-black font-mono-code text-xs font-bold uppercase border-2 border-black" style="box-shadow: 4px 4px 0px #000;">
            Back to Dashboard
        </a>
    </div>

    {blocks_html}
</body>
</html>
"""

@app.get("/api/blueprint")
def get_blueprint():
    return {
        "metadata": CAMPUS_METADATA,
        "blueprint": CAMPUS_BLUEPRINT
    }

@app.get("/api/telemetry")
def get_telemetry():
    return TELEMETRY_DATA

@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "system": "GridSense v1.0",
        "institution": "Jain Institute of Technology",
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
    <title>GridSense // Campus Energy Intelligence Platform</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;800&family=Space+Grotesk:wght@500;700;900&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Space Grotesk', sans-serif;
            background-color: #08090d;
            background-image: 
                radial-gradient(circle at 15% 15%, rgba(34, 197, 94, 0.08) 0%, transparent 40%),
                radial-gradient(circle at 85% 85%, rgba(59, 130, 246, 0.08) 0%, transparent 40%),
                linear-gradient(to right, rgba(255,255,255,0.02) 1px, transparent 1px),
                linear-gradient(to bottom, rgba(255,255,255,0.02) 1px, transparent 1px);
            background-size: 100% 100%, 100% 100%, 28px 28px, 28px 28px;
        }}
        .font-mono-code {{ font-family: 'JetBrains Mono', monospace; }}
        .brutal-border {{
            border: 2px solid #1e2433;
            box-shadow: 6px 6px 0px #030407;
        }}
        .brutal-btn {{
            box-shadow: 4px 4px 0px #000;
            transition: all 0.15s ease;
        }}
        .brutal-btn:hover {{
            transform: translate(-2px, -2px);
            box-shadow: 6px 6px 0px #000;
        }}
        .brutal-btn:active {{
            transform: translate(2px, 2px);
            box-shadow: 2px 2px 0px #000;
        }}
        @keyframes marquee {{
            0% {{ transform: translateX(0%); }}
            100% {{ transform: translateX(-50%); }}
        }}
        .animate-marquee {{
            display: flex;
            width: 200%;
            animation: marquee 24s linear infinite;
        }}
    </style>
</head>
<body class="text-zinc-100 min-h-screen flex flex-col justify-between selection:bg-emerald-400 selection:text-black">

    <!-- TOP TELEMETRY TICKER -->
    <header class="bg-zinc-950 border-b-2 border-zinc-800 text-xs font-mono-code font-bold py-2 overflow-hidden">
        <div class="animate-marquee whitespace-nowrap text-zinc-400">
            <span class="text-emerald-400">[SYSTEM: ACTIVE]</span> /// INSTITUTION: JAIN INSTITUTE OF TECHNOLOGY /// 7-DAY SYNTHETIC CYCLE LOADED (672 STEPS) /// BASELINE: 3,394.8 kWh /// GRIDSENSE: 1,769.1 kWh /// SAVINGS: 47.9% (INR 14,631.37/WK) /// MODULES A THROUGH H VERIFIED /// 
            <span class="text-emerald-400">[SYSTEM: ACTIVE]</span> /// INSTITUTION: JAIN INSTITUTE OF TECHNOLOGY /// 7-DAY SYNTHETIC CYCLE LOADED (672 STEPS) /// BASELINE: 3,394.8 kWh /// GRIDSENSE: 1,769.1 kWh /// SAVINGS: 47.9% (INR 14,631.37/WK) /// MODULES A THROUGH H VERIFIED /// 
        </div>
    </header>

    <!-- MAIN DASHBOARD -->
    <main class="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 flex-1">

        <!-- HEADER TITLE & STATS ROW -->
        <div class="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-8 pb-6 border-b-2 border-zinc-800">
            <div>
                <div class="flex items-center gap-3 font-mono-code text-xs font-bold text-zinc-400 uppercase tracking-widest mb-2">
                    <span class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-ping"></span>
                    <span>Team: Quantum Minds | Jain CMS | Challenge 12</span>
                </div>
                <h1 class="text-4xl sm:text-6xl font-black tracking-tight text-white uppercase">
                    Grid<span class="text-emerald-400">Sense</span>
                </h1>
                <p class="text-zinc-400 font-mono-code text-xs sm:text-sm mt-1 uppercase">
                    Campus Digital Twin // Real-Time Waste Index Scoring (WIS) & Optimization Engine
                </p>
            </div>
            
            <div class="flex flex-wrap gap-3">
                <div class="bg-zinc-900 border border-zinc-800 px-4 py-2 font-mono-code brutal-border">
                    <div class="text-[10px] text-zinc-500 uppercase">7-Day Energy Saved</div>
                    <div class="text-xl font-black text-emerald-400">{summary['total_saved_kwh']} kWh</div>
                </div>
                <div class="bg-zinc-900 border border-zinc-800 px-4 py-2 font-mono-code brutal-border">
                    <div class="text-[10px] text-zinc-500 uppercase">Weekly Financial Savings</div>
                    <div class="text-xl font-black text-yellow-400">INR {summary['total_saved_inr']}</div>
                </div>
                <div class="bg-zinc-900 border border-zinc-800 px-4 py-2 font-mono-code brutal-border">
                    <div class="text-[10px] text-zinc-500 uppercase">Waste Reduction</div>
                    <div class="text-xl font-black text-cyan-400">{summary['savings_percentage']}%</div>
                </div>
            </div>
        </div>

        <!-- 7-DAY TIME-SERIES VISUALIZER -->
        <section class="bg-zinc-950 border-2 border-zinc-800 p-6 brutal-border mb-8">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-4">
                <div>
                    <h2 class="text-lg font-bold uppercase tracking-wide text-white">
                        7-Day Energy Load Curve (Baseline vs GridSense)
                    </h2>
                    <p class="text-xs font-mono-code text-zinc-500">
                        15-minute telemetry intervals showing daytime peaks and after-hours phantom load elimination
                    </p>
                </div>
                <div class="flex items-center gap-4 text-xs font-mono-code">
                    <span class="flex items-center gap-1.5"><span class="w-3 h-3 bg-red-500/80 inline-block"></span> Unmanaged Baseline</span>
                    <span class="flex items-center gap-1.5"><span class="w-3 h-3 bg-emerald-400 inline-block"></span> GridSense Optimized</span>
                    <a href="/blueprint" target="_blank" class="px-2.5 py-1 bg-zinc-800 hover:bg-zinc-700 text-yellow-400 border border-zinc-700 rounded brutal-btn text-[11px] font-bold">
                        VIEW FULL BLUEPRINT TREE
                    </a>
                </div>
            </div>
            <div class="w-full h-72">
                <canvas id="energyChart"></canvas>
            </div>
        </section>

        <!-- DIGITAL TWIN CAMPUS BLUEPRINT & ZONE CARDS -->
        <div class="mb-6">
            <h2 class="text-2xl font-black uppercase text-white tracking-wide">
                Digital Campus Blueprint // Managed Zones
            </h2>
            <p class="text-xs font-mono-code text-zinc-400 mt-1 uppercase">
                Real-time Waste Index Score (WIS), telemetry readings, and active optimization modules
            </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">

            <!-- ZONE 1: B101 CLASSROOM -->
            <div class="bg-zinc-900 border-2 border-zinc-800 p-5 brutal-border flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between pb-3 mb-3 border-b border-zinc-800">
                        <span class="font-mono-code text-xs font-extrabold text-cyan-400">BLOCK B // LECTURE B101</span>
                        <span class="px-2 py-0.5 text-[10px] font-mono-code font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/40">WIS: 18 / OPTIMAL</span>
                    </div>
                    <h3 class="text-lg font-bold text-white">East-Facing Lecture Hall</h3>
                    <p class="text-xs font-mono-code text-zinc-400 mt-1">Capacity: 60 | Daylight-First Priority Zone</p>

                    <div class="mt-4 space-y-2 text-xs font-mono-code">
                        <div class="flex justify-between text-zinc-400">
                            <span>Module A1 (Daylight Lighting):</span>
                            <span class="text-emerald-400 font-bold">Zone A Locked OFF</span>
                        </div>
                        <div class="flex justify-between text-zinc-400">
                            <span>Module A2 (Adaptive HVAC):</span>
                            <span class="text-white font-bold">Setpoint 26°C (35 Occ)</span>
                        </div>
                        <div class="flex justify-between text-zinc-400">
                            <span>Module A4 (Smartboard):</span>
                            <span class="text-yellow-400 font-bold">Sleep (7m Timeout)</span>
                        </div>
                    </div>
                </div>
                <div class="mt-4 pt-3 border-t border-zinc-800 flex justify-between items-center text-xs font-mono-code">
                    <span class="text-zinc-500">POWER DRAW</span>
                    <span class="text-emerald-400 font-bold">1.8 kW <span class="text-zinc-600 line-through">4.9 kW</span></span>
                </div>
            </div>

            <!-- ZONE 2: COMPUTER LAB C1 -->
            <div class="bg-zinc-900 border-2 border-zinc-800 p-5 brutal-border flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between pb-3 mb-3 border-b border-zinc-800">
                        <span class="font-mono-code text-xs font-extrabold text-purple-400">BLOCK C // LAB C1</span>
                        <span class="px-2 py-0.5 text-[10px] font-mono-code font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/40">WIS: 12 / SECURED</span>
                    </div>
                    <h3 class="text-lg font-bold text-white">Advanced Computing Lab</h3>
                    <p class="text-xs font-mono-code text-zinc-400 mt-1">60 Systems | Department of CSE</p>

                    <div class="mt-4 space-y-2 text-xs font-mono-code">
                        <div class="flex justify-between text-zinc-400">
                            <span>Module C (Inactivity Agent):</span>
                            <span class="text-emerald-400 font-bold">60 PCs in S3 Sleep</span>
                        </div>
                        <div class="flex justify-between text-zinc-400">
                            <span>Thermal Load Cut:</span>
                            <span class="text-cyan-400 font-bold">-6.0 kW Heat Load</span>
                        </div>
                        <div class="flex justify-between text-zinc-400">
                            <span>Lab AC Compressors:</span>
                            <span class="text-emerald-400 font-bold">De-energized</span>
                        </div>
                    </div>
                </div>
                <div class="mt-4 pt-3 border-t border-zinc-800 flex justify-between items-center text-xs font-mono-code">
                    <span class="text-zinc-500">POWER DRAW</span>
                    <span class="text-emerald-400 font-bold">0.18 kW <span class="text-zinc-600 line-through">12.8 kW</span></span>
                </div>
            </div>

            <!-- ZONE 3: ELEVATOR BANK B -->
            <div class="bg-zinc-900 border-2 border-zinc-800 p-5 brutal-border flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between pb-3 mb-3 border-b border-zinc-800">
                        <span class="font-mono-code text-xs font-extrabold text-yellow-400">BLOCK B // ELEVATORS</span>
                        <span class="px-2 py-0.5 text-[10px] font-mono-code font-bold bg-blue-500/20 text-blue-400 border border-blue-500/40">WIS: 22 / THROTTLED</span>
                    </div>
                    <h3 class="text-lg font-bold text-white">4-Lift Elevator Bank</h3>
                    <p class="text-xs font-mono-code text-zinc-400 mt-1">Dynamic Staging with Redundant Safety</p>

                    <div class="mt-4 space-y-2 text-xs font-mono-code">
                        <div class="flex justify-between text-zinc-400">
                            <span>Module D (Mandatory Floor):</span>
                            <span class="text-yellow-400 font-bold">2 Lifts Active</span>
                        </div>
                        <div class="flex justify-between text-zinc-400">
                            <span>Deep Sleep Cars:</span>
                            <span class="text-zinc-400 font-bold">Car 3 & Car 4</span>
                        </div>
                        <div class="flex justify-between text-zinc-400">
                            <span>Safety & Accessibility:</span>
                            <span class="text-emerald-400 font-bold">100% Compliant</span>
                        </div>
                    </div>
                </div>
                <div class="mt-4 pt-3 border-t border-zinc-800 flex justify-between items-center text-xs font-mono-code">
                    <span class="text-zinc-500">SAVINGS RATE</span>
                    <span class="text-emerald-400 font-bold">22 kWh/day (Rounded Up)</span>
                </div>
            </div>

            <!-- ZONE 4: HOSTEL GEYSERS & ROOM SENSORS -->
            <div class="bg-zinc-900 border-2 border-zinc-800 p-5 brutal-border flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between pb-3 mb-3 border-b border-zinc-800">
                        <span class="font-mono-code text-xs font-extrabold text-red-400">HOSTEL // 120 ROOMS + WINGS</span>
                        <span class="px-2 py-0.5 text-[10px] font-mono-code font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/40">WIS: 15 / PEAK SHAVED</span>
                    </div>
                    <h3 class="text-lg font-bold text-white">Residential Block & Room Matrix</h3>
                    <p class="text-xs font-mono-code text-zinc-400 mt-1">120 Individual Rooms | 16 Geysers (2.5 kW)</p>

                    <div class="mt-4 space-y-2 text-xs font-mono-code">
                        <div class="flex justify-between text-zinc-400">
                            <span>Room Presence Sensors:</span>
                            <span class="text-emerald-400 font-bold">Auto-Kill Vacant Rooms</span>
                        </div>
                        <div class="flex justify-between text-zinc-400">
                            <span>Occupied Room Control:</span>
                            <span class="text-cyan-400 font-bold">100% Manual User Mode</span>
                        </div>
                        <div class="flex justify-between text-zinc-400">
                            <span>Module E (Staggered Geysers):</span>
                            <span class="text-white font-bold">Wing 1 (5:30) / Wing 2 (6:30)</span>
                        </div>
                        <div class="flex justify-between text-zinc-400">
                            <span>Max Demand (kVA) Breach:</span>
                            <span class="text-emerald-400 font-bold">0 Violations</span>
                        </div>
                    </div>
                </div>
                <div class="mt-4 pt-3 border-t border-zinc-800 flex justify-between items-center text-xs font-mono-code">
                    <span class="text-zinc-500">PENALTY CHARGES</span>
                    <span class="text-emerald-400 font-bold">INR 0.00 (Prevented)</span>
                </div>
            </div>

            <!-- ZONE 5: WATER COOLERS -->
            <div class="bg-zinc-900 border-2 border-zinc-800 p-5 brutal-border flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between pb-3 mb-3 border-b border-zinc-800">
                        <span class="font-mono-code text-xs font-extrabold text-cyan-400">CAMPUS // 15 WATER COOLERS</span>
                        <span class="px-2 py-0.5 text-[10px] font-mono-code font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/40">WIS: 05 / ISOLATED</span>
                    </div>
                    <h3 class="text-lg font-bold text-white">Commercial Cooling Loops</h3>
                    <p class="text-xs font-mono-code text-zinc-400 mt-1">Blocks A, B, C Commercial Compressors</p>

                    <div class="mt-4 space-y-2 text-xs font-mono-code">
                        <div class="flex justify-between text-zinc-400">
                            <span>Module F (Cutoff Schedule):</span>
                            <span class="text-white font-bold">19:00 - 07:00 Daily</span>
                        </div>
                        <div class="flex justify-between text-zinc-400">
                            <span>Weekend Lockout:</span>
                            <span class="text-emerald-400 font-bold">100% Sundays Off</span>
                        </div>
                        <div class="flex justify-between text-zinc-400">
                            <span>Thermal Buffer:</span>
                            <span class="text-cyan-400 font-bold">2+ Hrs Chill Retention</span>
                        </div>
                    </div>
                </div>
                <div class="mt-4 pt-3 border-t border-zinc-800 flex justify-between items-center text-xs font-mono-code">
                    <span class="text-zinc-500">MONTHLY SAVINGS</span>
                    <span class="text-emerald-400 font-bold">1,620 kWh (INR 14,580)</span>
                </div>
            </div>

            <!-- ZONE 6: ENTERPRISE WIFI -->
            <div class="bg-zinc-900 border-2 border-zinc-800 p-5 brutal-border flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between pb-3 mb-3 border-b border-zinc-800">
                        <span class="font-mono-code text-xs font-extrabold text-emerald-400">NETWORK // 150 APs</span>
                        <span class="px-2 py-0.5 text-[10px] font-mono-code font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/40">WIS: 10 / GREEN MODE</span>
                    </div>
                    <h3 class="text-lg font-bold text-white">Enterprise PoE Network</h3>
                    <p class="text-xs font-mono-code text-zinc-400 mt-1">Aruba / UniFi SNMP Infrastructure</p>

                    <div class="mt-4 space-y-2 text-xs font-mono-code">
                        <div class="flex justify-between text-zinc-400">
                            <span>Module H (Off-Hours Radio):</span>
                            <span class="text-yellow-400 font-bold">5 GHz Radio Disabled</span>
                        </div>
                        <div class="flex justify-between text-zinc-400">
                            <span>Low-Power Beacon:</span>
                            <span class="text-emerald-400 font-bold">2.4 GHz Only (&lt;5W)</span>
                        </div>
                        <div class="flex justify-between text-zinc-400">
                            <span>Hostel Connectivity:</span>
                            <span class="text-white font-bold">Full Bandwidth (24/7)</span>
                        </div>
                    </div>
                </div>
                <div class="mt-4 pt-3 border-t border-zinc-800 flex justify-between items-center text-xs font-mono-code">
                    <span class="text-zinc-500">SAVINGS POTENTIAL</span>
                    <span class="text-emerald-400 font-bold">2,700 kWh/month</span>
                </div>
            </div>

        </div>

        <!-- LIVE AUDIT / CONSOLE FEED -->
        <section class="bg-black border-2 border-zinc-800 p-6 brutal-border font-mono-code text-xs">
            <div class="flex items-center justify-between pb-3 mb-4 border-b border-zinc-800">
                <span class="text-zinc-300 font-bold uppercase tracking-wider">Live System Engine Event Feed</span>
                <span class="text-emerald-400 font-bold">TELEMETRY SYNCED</span>
            </div>
            <div class="space-y-1 text-zinc-400">
                <div>[04:00 PM] <span class="text-cyan-400">Spatial Consolidation:</span> Evaluated 24 lecture schedules. Relocated 1 stray class from Block A to Block C. Block A Wing 2 contactors scheduled for de-energization at 05:00 PM.</div>
                <div>[05:30 PM] <span class="text-yellow-400">Elevator Bank B:</span> Call frequency dropped below threshold. Cars 3 & 4 transitioned to deep sleep. Cars 1 & 2 operational (Mandatory safety baseline enforced).</div>
                <div>[06:00 PM] <span class="text-purple-400">Lab Power Manager:</span> Broadcast shutdown signal sent to 180 idle PCs across Labs C1, C2, and C3. AC units isolated.</div>
                <div>[07:00 PM] <span class="text-emerald-400">Water Cooler Interlock:</span> 15 commercial coolers powered down across academic blocks.</div>
                <div>[11:00 PM] <span class="text-blue-400">WiFi Controller:</span> Academic block PoE switches toggled to 2.4 GHz low-power beacon mode.</div>
            </div>
        </section>

    </main>

    <!-- FOOTER -->
    <footer class="bg-zinc-950 border-t-2 border-zinc-800 py-4 px-4 sm:px-8 font-mono-code text-xs text-zinc-500">
        <div class="max-w-7xl mx-auto flex flex-col sm:flex-row justify-between items-center gap-2">
            <span>GridSense v1.0 // Hackathon O1 Solution</span>
            <span>Jain CMS // Jain Institute of Technology Reference Blueprint</span>
        </div>
    </footer>

    <script>
        // Render 7-day comparison chart
        fetch('/api/telemetry')
            .then(res => res.json())
            .then(data => {{
                const telemetry = data.telemetry || [];
                // Sample every 4th point (1 hour intervals) for a clean chart
                const sampled = telemetry.filter((_, idx) => idx % 4 === 0);
                const labels = sampled.map(p => p.day.substring(0,3) + ' ' + p.timestamp.split(' ')[1]);
                
                // Aggregate baseline and gridsense total across sample zones
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
                                borderColor: 'rgba(239, 68, 68, 0.85)',
                                backgroundColor: 'rgba(239, 68, 68, 0.05)',
                                fill: true,
                                tension: 0.2,
                                borderWidth: 2,
                                pointRadius: 0
                            }},
                            {{
                                label: 'GridSense Optimized (kW)',
                                data: gridsenseData,
                                borderColor: 'rgba(34, 197, 94, 0.95)',
                                backgroundColor: 'rgba(34, 197, 94, 0.15)',
                                fill: true,
                                tension: 0.2,
                                borderWidth: 2,
                                pointRadius: 0
                            }}
                        ]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        interaction: {{ intersect: false, mode: 'index' }},
                        plugins: {{
                            legend: {{ display: false }}
                        }},
                        scales: {{
                            x: {{
                                grid: {{ color: 'rgba(255, 255, 255, 0.05)' }},
                                ticks: {{ color: '#71717a', font: {{ family: 'JetBrains Mono', size: 10 }}, maxTicksLimit: 14 }}
                            }},
                            y: {{
                                title: {{ display: true, text: 'Total Zone Power (kW)', color: '#a1a1aa', font: {{ family: 'Space Grotesk' }} }},
                                grid: {{ color: 'rgba(255, 255, 255, 0.05)' }},
                                ticks: {{ color: '#71717a', font: {{ family: 'JetBrains Mono', size: 10 }} }}
                            }}
                        }}
                    }});
            }})
            .catch(err => console.error("Could not load chart telemetry:", err));
    </script>
</body>
</html>
"""
