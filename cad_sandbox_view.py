"""
High-Fidelity Pure Vector CAD Architectural Floor Plan for Block B (7,500 m2, G+4)
JIT Campus Energy Optimization Platform
"""

def render_cad_sandbox_html():
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GridSense // Block B Architectural Vector Blueprint</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background-color: #0c0e12;
            color: #d1d5db;
        }
        .font-mono-code { font-family: 'JetBrains Mono', monospace; }

        /* Neumorphic Dark Design System */
        .neu-card {
            background: #14171f;
            border-radius: 16px;
            box-shadow: 8px 8px 22px #07080b, -8px -8px 22px #1d222e;
            border: 1px solid rgba(255, 255, 255, 0.04);
        }
        .neu-inset {
            background: #0d0f14;
            border-radius: 12px;
            box-shadow: inset 4px 4px 10px #06070a, inset -4px -4px 10px #181c26;
            border: 1px solid rgba(255, 255, 255, 0.02);
        }
        .neu-btn {
            background: #161922;
            border-radius: 10px;
            box-shadow: 4px 4px 12px #07080b, -4px -4px 12px #202634;
            border: 1px solid rgba(255, 255, 255, 0.05);
            transition: all 0.15s ease;
        }
        .neu-btn:hover {
            color: #10b981;
            box-shadow: 2px 2px 6px #07080b, -2px -2px 6px #202634;
        }
        .neu-btn:active {
            box-shadow: inset 3px 3px 6px #07080b, inset -3px -3px 6px #202634;
        }

        /* Blueprint Canvas Styling */
        .blueprint-board {
            background-color: #080c16;
            background-image: 
                linear-gradient(rgba(37, 99, 235, 0.15) 1px, transparent 1px),
                linear-gradient(90deg, rgba(37, 99, 235, 0.15) 1px, transparent 1px),
                linear-gradient(rgba(37, 99, 235, 0.05) 1px, transparent 1px),
                linear-gradient(90deg, rgba(37, 99, 235, 0.05) 1px, transparent 1px);
            background-size: 80px 80px, 80px 80px, 16px 16px, 16px 16px;
            border: 2px solid #1e3a5f;
            border-radius: 16px;
            box-shadow: inset 0 0 40px rgba(0, 0, 0, 0.95), 0 12px 36px rgba(0, 0, 0, 0.8);
        }

        /* Room Lighting States */
        .room-bg {
            transition: fill 0.35s ease, stroke 0.35s ease, filter 0.35s ease;
        }
        .room-lit-bg {
            fill: #221a0d !important;
            stroke: #f59e0b !important;
            stroke-width: 2.5 !important;
            filter: drop-shadow(0 0 14px rgba(245, 158, 11, 0.35));
        }
        .room-dark-bg {
            fill: #0a101d !important;
            stroke: #1e3a5f !important;
            stroke-width: 1.5 !important;
            opacity: 0.85;
        }

        /* Furniture & Desks */
        .cad-desk {
            fill: #111a2d;
            stroke: #223759;
            stroke-width: 1;
            transition: all 0.3s ease;
        }
        .cad-desk-lit {
            fill: #342611 !important;
            stroke: #d97706 !important;
            stroke-width: 1.2 !important;
        }
        .cad-chair {
            fill: #0c121e;
            stroke: #1c2e4a;
            stroke-width: 0.8;
            transition: all 0.3s ease;
        }
        .cad-chair-lit {
            fill: #271c0b !important;
            stroke: #92400e !important;
        }
        .cad-student-dot {
            fill: #38bdf8;
            filter: drop-shadow(0 0 3px #38bdf8);
            transition: opacity 0.3s ease;
        }

        /* Ceiling Luminaires (Lights) */
        .light-glow {
            transition: all 0.35s ease;
        }
        .light-on {
            fill: #fef08a;
            stroke: #f59e0b;
            stroke-width: 1.5;
            filter: drop-shadow(0 0 6px #facc15) drop-shadow(0 0 16px rgba(250, 204, 21, 0.85));
        }
        .light-off {
            fill: #1e293b;
            stroke: #334155;
            stroke-width: 1;
            filter: none;
        }

        /* Hallway Corridors */
        .corridor-path-lit {
            stroke: #facc15 !important;
            stroke-width: 3.5 !important;
            stroke-dasharray: none !important;
            filter: drop-shadow(0 0 10px rgba(250, 204, 21, 0.85));
            transition: all 0.4s ease;
        }
        .corridor-path-dark {
            stroke: #1e3a5f !important;
            stroke-width: 1.5 !important;
            stroke-dasharray: 6 6 !important;
            filter: none;
            transition: all 0.4s ease;
        }

        /* Architectural Elements */
        .cad-column {
            fill: #1d4ed8;
            stroke: #60a5fa;
            stroke-width: 1.5;
        }
        .cad-door-swing {
            stroke: #38bdf8;
            stroke-width: 1.2;
            stroke-dasharray: 2 2;
            fill: none;
        }
    </style>
</head>
<body class="min-h-screen p-3 sm:p-5 max-w-[1600px] mx-auto">

    <!-- TOP HEADER -->
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 mb-5 pb-4 border-b border-white/5">
        <div>
            <div class="text-[11px] font-mono-code font-bold text-emerald-400 uppercase tracking-widest">
                JIT Campus Intelligent Energy System // Architectural Digital Twin
            </div>
            <h1 class="text-xl sm:text-2xl font-bold text-white tracking-tight mt-0.5">
                Block B Architectural Vector Blueprint (7,500 m², G+4)
            </h1>
            <p class="text-xs text-zinc-400 font-mono-code mt-0.5">
                Exact radial architectural layout with individual student desks, ceiling luminaires, 4-lift banks, and hallway relays
            </p>
        </div>
        <div class="flex items-center gap-3">
            <a href="/" class="px-3.5 py-1.5 neu-btn font-mono-code text-xs font-semibold text-zinc-300">
                Back to Campus Dashboard
            </a>
        </div>
    </div>

    <!-- MAIN TWO-COLUMN LAYOUT -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-5">

        <!-- LEFT PANEL: CONTROLS & TEST PARAMS (4 COLS) -->
        <div class="lg:col-span-4 space-y-4">

            <!-- SCENARIO PRESETS -->
            <div class="p-4 neu-card">
                <div class="flex justify-between items-center mb-2.5">
                    <span class="text-xs font-mono-code uppercase text-zinc-400 font-bold">Quick Scenarios</span>
                    <span class="text-[10px] font-mono-code text-emerald-400">1-Click Test</span>
                </div>
                <div class="grid grid-cols-2 gap-2">
                    <button onclick="applyPreset('morning')" class="p-2 neu-btn text-left">
                        <div class="text-xs font-mono-code font-bold text-zinc-200">09:00 AM</div>
                        <div class="text-[10px] text-zinc-500 font-mono-code">Full Morning Rush</div>
                    </button>
                    <button onclick="applyPreset('afternoon')" class="p-2 neu-btn text-left">
                        <div class="text-xs font-mono-code font-bold text-zinc-200">02:30 PM</div>
                        <div class="text-[10px] text-zinc-500 font-mono-code">Peak Heat & Solar</div>
                    </button>
                    <button onclick="applyPreset('night_waste')" class="p-2 neu-btn text-left border border-amber-500/30">
                        <div class="text-xs font-mono-code font-bold text-amber-400">07:30 PM</div>
                        <div class="text-[10px] text-amber-500/80 font-mono-code">After-Hours Waste</div>
                    </button>
                    <button onclick="applyPreset('lockdown')" class="p-2 neu-btn text-left">
                        <div class="text-xs font-mono-code font-bold text-blue-400">22:00 PM</div>
                        <div class="text-[10px] text-zinc-500 font-mono-code">Night Lockdown (0 Occ)</div>
                    </button>
                </div>
            </div>

            <!-- ENVIRONMENTAL CONTROLS -->
            <div class="p-4 neu-card space-y-3">
                <div class="text-xs font-mono-code uppercase text-zinc-400 font-bold">Environmental Inputs</div>
                
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
                    <div class="text-xs font-mono-code text-zinc-400 mb-1">Sky & Natural Daylight</div>
                    <select id="weatherSelect" onchange="onParamChange()" class="w-full p-2 neu-inset text-xs font-mono-code text-zinc-200 outline-none">
                        <option value="Sunny / Daylight">Sunny / Bright (Daylight Harvesting Enabled)</option>
                        <option value="Overcast / Rainy">Overcast / Rainy (Low Natural Lux)</option>
                        <option value="Night" selected>Night (Zero Daylight)</option>
                    </select>
                </div>
            </div>

            <!-- CLASSROOM OCCUPANCY HEADCOUNT SLIDERS -->
            <div class="p-4 neu-card space-y-2">
                <div class="flex justify-between items-center mb-1">
                    <span class="text-xs font-mono-code uppercase text-zinc-400 font-bold">Room Headcounts</span>
                    <button onclick="clearAllOccupants()" class="text-[10px] font-mono-code text-zinc-500 hover:text-white">Clear All</button>
                </div>

                <div class="grid grid-cols-2 gap-2 text-[11px] font-mono-code text-zinc-400">
                    <div class="p-1.5 neu-inset">
                        <div class="flex justify-between">
                            <span>CR B-101 (W1):</span>
                            <span id="val_r1" class="text-white font-bold">0</span>
                        </div>
                        <input type="range" id="occ_r1" min="0" max="60" value="0" oninput="onParamChange()" class="w-full accent-blue-500 cursor-pointer">
                    </div>
                    <div class="p-1.5 neu-inset">
                        <div class="flex justify-between">
                            <span>CR B-105 (E1):</span>
                            <span id="val_r5" class="text-white font-bold">0</span>
                        </div>
                        <input type="range" id="occ_r5" min="0" max="60" value="0" oninput="onParamChange()" class="w-full accent-blue-500 cursor-pointer">
                    </div>
                    <div class="p-1.5 neu-inset">
                        <div class="flex justify-between">
                            <span>CR B-102 (W2):</span>
                            <span id="val_r2" class="text-white font-bold">0</span>
                        </div>
                        <input type="range" id="occ_r2" min="0" max="60" value="0" oninput="onParamChange()" class="w-full accent-blue-500 cursor-pointer">
                    </div>
                    <div class="p-1.5 neu-inset">
                        <div class="flex justify-between">
                            <span>CR B-106 (E2):</span>
                            <span id="val_r6" class="text-white font-bold">0</span>
                        </div>
                        <input type="range" id="occ_r6" min="0" max="60" value="0" oninput="onParamChange()" class="w-full accent-blue-500 cursor-pointer">
                    </div>
                    <div class="p-1.5 neu-inset">
                        <div class="flex justify-between">
                            <span>CR B-103 (W3):</span>
                            <span id="val_r3" class="text-white font-bold">0</span>
                        </div>
                        <input type="range" id="occ_r3" min="0" max="60" value="0" oninput="onParamChange()" class="w-full accent-blue-500 cursor-pointer">
                    </div>
                    <div class="p-1.5 neu-inset">
                        <div class="flex justify-between">
                            <span>CR B-107 (E3):</span>
                            <span id="val_r7" class="text-white font-bold">0</span>
                        </div>
                        <input type="range" id="occ_r7" min="0" max="60" value="0" oninput="onParamChange()" class="w-full accent-blue-500 cursor-pointer">
                    </div>
                    <div class="p-1.5 neu-inset">
                        <div class="flex justify-between">
                            <span>CR B-104 (W4):</span>
                            <span id="val_r4" class="text-white font-bold">0</span>
                        </div>
                        <input type="range" id="occ_r4" min="0" max="60" value="0" oninput="onParamChange()" class="w-full accent-blue-500 cursor-pointer">
                    </div>
                    <div class="p-1.5 neu-inset border border-amber-500/20">
                        <div class="flex justify-between">
                            <span class="text-amber-300">CR B-108 (E4):</span>
                            <span id="val_r8" class="text-amber-400 font-bold">25</span>
                        </div>
                        <input type="range" id="occ_r8" min="0" max="60" value="25" oninput="onParamChange()" class="w-full accent-amber-500 cursor-pointer">
                    </div>
                </div>
            </div>

            <!-- AUTOMATIC TELEGRAM PUSH NOTIFICATION -->
            <div class="p-4 neu-card space-y-2.5">
                <div class="flex justify-between items-center">
                    <span class="text-xs font-mono-code uppercase text-zinc-400 font-bold">Mobile Dispatch (Telegram)</span>
                    <span class="inline-flex items-center gap-1.5 text-[10px] font-mono-code text-emerald-400">
                        <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span> Auto-Push
                    </span>
                </div>
                <input type="text" id="tgToken" placeholder="Bot Token (e.g. 7829...)" class="w-full p-2 neu-inset text-[11px] font-mono-code text-zinc-200 outline-none">
                <input type="text" id="tgChatId" placeholder="Chat ID (e.g. 9821...)" class="w-full p-2 neu-inset text-[11px] font-mono-code text-zinc-200 outline-none">
                <div class="flex gap-2">
                    <button onclick="saveAndTestTelegram()" class="w-full py-2 neu-btn text-xs font-mono-code font-bold text-emerald-400">
                        Connect Phone & Test Alert
                    </button>
                </div>
                <div id="tgStatus" class="text-[10px] font-mono-code text-zinc-500 text-center">
                    Configuration saved locally. Actions dispatch live to your device.
                </div>
            </div>

        </div>

        <!-- RIGHT PANEL: VECTOR CAD BLUEPRINT & COMPARISON METERS (8 COLS) -->
        <div class="lg:col-span-8 space-y-4">

            <!-- COMPARISON GAUGES -->
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
                <div class="p-3.5 neu-card">
                    <div class="text-[10px] font-mono-code uppercase text-zinc-500">Unmanaged Baseline</div>
                    <div id="baselineMeter" class="text-xl font-bold text-rose-400 mt-0.5">28.40 kW</div>
                    <div class="text-[10px] text-zinc-500 font-mono-code">Blind Power Draw (Zero Sensing)</div>
                </div>

                <div class="p-3.5 neu-card">
                    <div class="text-[10px] font-mono-code uppercase text-zinc-500">GridSense Optimized</div>
                    <div id="optimizedMeter" class="text-xl font-bold text-emerald-400 mt-0.5">6.25 kW</div>
                    <div class="text-[10px] text-zinc-500 font-mono-code">Adaptive HVAC & Corridor Cutoffs</div>
                </div>

                <div class="p-3.5 neu-card">
                    <div class="text-[10px] font-mono-code uppercase text-zinc-500">Immediate Savings Rate</div>
                    <div id="savingsMeter" class="text-xl font-bold text-amber-400 mt-0.5">22.15 kW (78.0%)</div>
                    <div id="inrMeter" class="text-[10px] text-emerald-400 font-mono-code">INR 199.35 / Hour Saved</div>
                </div>
            </div>

            <!-- SPATIAL CONSOLIDATION NUDGE BANNER -->
            <div id="alertCard" class="p-3.5 neu-card border-l-4 border-l-amber-400 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
                <div class="space-y-0.5">
                    <div class="flex items-center gap-2 text-xs font-mono-code font-bold text-amber-400 uppercase">
                        <span class="w-2 h-2 rounded-full bg-amber-400 animate-ping"></span>
                        Spatial Consolidation Nudge Triggered
                    </div>
                    <p id="alertText" class="text-xs font-mono-code text-zinc-300">
                        Isolated class in CR B-108 (Far East Wing). Relocate to CR B-101 (near main stairs) to shut down East Corridor & cut 3.8 kW.
                    </p>
                </div>
                <button onclick="applyConsolidation()" class="px-4 py-2 neu-btn text-xs font-mono-code font-bold text-emerald-400 shrink-0">
                    Apply Relocation
                </button>
            </div>

            <!-- ARCHITECTURAL VECTOR BLUEPRINT CANVAS -->
            <div class="p-4 neu-card space-y-2">
                <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 border-b border-white/5 pb-2.5">
                    <div>
                        <div class="flex items-center gap-2">
                            <span class="px-2 py-0.5 rounded bg-blue-600 text-white font-mono-code text-[11px] font-bold">BLOCK B</span>
                            <span class="text-xs font-bold text-white uppercase tracking-wider font-mono-code">ARCHITECTURAL CAD BLUEPRINT</span>
                        </div>
                        <p class="text-[10px] text-zinc-400 font-mono-code mt-0.5">
                            Built-up Area: ~7,500 m² | G+4 | Radial Arc Geometry with Desks, Luminaires & Relays
                        </p>
                    </div>
                    <div id="elevState" class="text-[10px] font-mono-code text-emerald-400 neu-inset px-3 py-1 font-bold">
                        Lifts 1 & 2 Active | Lifts 3 & 4 Deep Sleep
                    </div>
                </div>

                <!-- SVG BLUEPRINT BOARD -->
                <div class="blueprint-board p-2 sm:p-3 overflow-x-auto">
                    <svg viewBox="0 0 1100 920" class="w-full h-auto min-w-[750px]">
                        <defs>
                            <!-- Filter for Soft Radial Luminaire Glow -->
                            <filter id="luminaireGlow" x="-50%" y="-50%" width="200%" height="200%">
                                <feGaussianBlur stdDeviation="7" result="blur" />
                                <feMerge>
                                    <feMergeNode in="blur" />
                                    <feMergeNode in="SourceGraphic" />
                                </feMerge>
                            </filter>

                            <!-- Stair Hatch Pattern -->
                            <pattern id="stairTreads" width="8" height="8" patternUnits="userSpaceOnUse">
                                <line x1="0" y1="4" x2="8" y2="4" stroke="#38bdf8" stroke-width="1.2" opacity="0.4" />
                            </pattern>

                            <!-- Restroom Tile Pattern -->
                            <pattern id="tilePattern" width="12" height="12" patternUnits="userSpaceOnUse">
                                <rect width="12" height="12" fill="none" stroke="#1e293b" stroke-width="0.8" />
                            </pattern>
                        </defs>

                        <!-- BLUEPRINT TITLE BLOCK IN SVG -->
                        <g transform="translate(420, 20)">
                            <rect width="260" height="28" rx="6" fill="#1e40af" stroke="#60a5fa" stroke-width="1.2" />
                            <text x="130" y="19" fill="#ffffff" font-family="'JetBrains Mono'" font-size="11" font-weight="bold" text-anchor="middle" letter-spacing="1">
                                BLOCK B - FLOOR PLAN (G+4)
                            </text>
                        </g>

                        <!-- ================= 1. CENTRAL ATRIUM ================= -->
                        <g id="central_atrium">
                            <!-- Outer Atrium Boundary -->
                            <circle cx="550" cy="490" r="165" fill="#090d16" stroke="#2563eb" stroke-width="2.5" />
                            <circle cx="550" cy="490" r="140" fill="#0b111e" stroke="#1e3a5f" stroke-width="1.5" stroke-dasharray="6 4" />
                            <circle cx="550" cy="490" r="95" fill="#060910" stroke="#38bdf8" stroke-width="2" />
                            
                            <!-- Skylight Geometric Radial Spokes -->
                            <line x1="455" y1="490" x2="645" y2="490" stroke="#1e3a5f" stroke-width="1.2" />
                            <line x1="550" y1="395" x2="550" y2="585" stroke="#1e3a5f" stroke-width="1.2" />
                            <line x1="483" y1="423" x2="617" y2="557" stroke="#1e3a5f" stroke-width="1.2" />
                            <line x1="483" y1="557" x2="617" y2="423" stroke="#1e3a5f" stroke-width="1.2" />

                            <!-- Atrium Labels -->
                            <text x="550" y="485" fill="#93c5fd" font-family="'JetBrains Mono'" font-size="13" font-weight="bold" text-anchor="middle">
                                Central Atrium
                            </text>
                            <text x="550" y="505" fill="#60a5fa" font-family="'JetBrains Mono'" font-size="9.5" text-anchor="middle">
                                (Open to Above)
                            </text>

                            <!-- Curved Atrium Seating Counters -->
                            <path d="M 445 440 A 120 120 0 0 1 445 540" fill="none" stroke="#3b82f6" stroke-width="8" stroke-linecap="round" />
                            <path d="M 655 440 A 120 120 0 0 0 655 540" fill="none" stroke="#3b82f6" stroke-width="8" stroke-linecap="round" />

                            <!-- Planter Greenery Accents -->
                            <circle cx="465" cy="415" r="9" fill="#065f46" stroke="#10b981" stroke-width="1.5" />
                            <circle cx="635" cy="415" r="9" fill="#065f46" stroke="#10b981" stroke-width="1.5" />
                            <circle cx="465" cy="565" r="9" fill="#065f46" stroke="#10b981" stroke-width="1.5" />
                            <circle cx="635" cy="565" r="9" fill="#065f46" stroke="#10b981" stroke-width="1.5" />
                        </g>

                        <!-- ================= 2. CORRIDOR LIGHTING RELAYS ================= -->
                        <!-- West Corridor Relay Arc -->
                        <path id="corridor_west_arc" d="M 330 260 A 250 250 0 0 0 280 730" fill="none" class="corridor-path-dark" />
                        <!-- East Corridor Relay Arc -->
                        <path id="corridor_east_arc" d="M 770 260 A 250 250 0 0 1 820 730" fill="none" class="corridor-path-lit" />
                        <!-- North Concourse Link -->
                        <line x1="330" y1="260" x2="770" y2="260" stroke="#1e3a5f" stroke-width="2" stroke-dasharray="4 4" />

                        <!-- Corridor Luminaire Dots (West) -->
                        <circle cx="315" cy="340" r="3" class="light-glow light-off" id="cw1" />
                        <circle cx="285" cy="450" r="3" class="light-glow light-off" id="cw2" />
                        <circle cx="275" cy="560" r="3" class="light-glow light-off" id="cw3" />
                        <circle cx="290" cy="670" r="3" class="light-glow light-off" id="cw4" />

                        <!-- Corridor Luminaire Dots (East) -->
                        <circle cx="785" cy="340" r="3.5" class="light-glow light-on" id="ce1" />
                        <circle cx="815" cy="450" r="3.5" class="light-glow light-on" id="ce2" />
                        <circle cx="825" cy="560" r="3.5" class="light-glow light-on" id="ce3" />
                        <circle cx="810" cy="670" r="3.5" class="light-glow light-on" id="ce4" />

                        <!-- ================= 3. NORTH WING ================= -->
                        <!-- MAIN NORTH STAIRCASE -->
                        <g transform="translate(500, 70)">
                            <rect width="100" height="150" fill="#0a1222" stroke="#38bdf8" stroke-width="2" rx="4" />
                            <rect width="100" height="150" fill="url(#stairTreads)" />
                            <line x1="50" y1="10" x2="50" y2="140" stroke="#38bdf8" stroke-width="1.5" />
                            <text x="50" y="80" fill="#38bdf8" font-family="'JetBrains Mono'" font-size="10" font-weight="bold" text-anchor="middle">
                                MAIN STAIRS
                            </text>
                            <path d="M 50 120 L 50 40 L 45 48 M 50 40 L 55 48" stroke="#38bdf8" stroke-width="2" fill="none" stroke-linecap="round" />
                        </g>

                        <!-- LAB B-1 (NORTH-WEST) -->
                        <g id="group_lab1">
                            <path d="M 240 80 L 480 80 L 480 230 L 240 250 Z" class="room-bg room-dark-bg" id="poly_lab1" />
                            <text x="350" y="115" fill="#93c5fd" font-family="'JetBrains Mono'" font-size="12" font-weight="bold" text-anchor="middle">
                                Lab B-1 (150 m²)
                            </text>
                            <text x="350" y="132" fill="#64748b" font-family="'JetBrains Mono'" font-size="9" text-anchor="middle">
                                Hardware & Embedded Systems
                            </text>
                            <!-- Lab Workbenches -->
                            <rect x="270" y="150" width="85" height="16" class="cad-desk" />
                            <rect x="375" y="150" width="85" height="16" class="cad-desk" />
                            <rect x="270" y="185" width="85" height="16" class="cad-desk" />
                            <rect x="375" y="185" width="85" height="16" class="cad-desk" />
                            <!-- Luminaires -->
                            <circle cx="310" cy="115" r="4.5" class="light-glow light-off" />
                            <circle cx="410" cy="115" r="4.5" class="light-glow light-off" />
                            <circle cx="310" cy="215" r="4.5" class="light-glow light-off" />
                            <circle cx="410" cy="215" r="4.5" class="light-glow light-off" />
                        </g>

                        <!-- LAB B-2 (NORTH-EAST) -->
                        <g id="group_lab2">
                            <path d="M 620 80 L 860 80 L 860 250 L 620 230 Z" class="room-bg room-dark-bg" id="poly_lab2" />
                            <text x="750" y="115" fill="#93c5fd" font-family="'JetBrains Mono'" font-size="12" font-weight="bold" text-anchor="middle">
                                Lab B-2 (150 m²)
                            </text>
                            <text x="750" y="132" fill="#64748b" font-family="'JetBrains Mono'" font-size="9" text-anchor="middle">
                                RF & Communication Lab
                            </text>
                            <!-- Lab Workbenches -->
                            <rect x="640" y="150" width="85" height="16" class="cad-desk" />
                            <rect x="745" y="150" width="85" height="16" class="cad-desk" />
                            <rect x="640" y="185" width="85" height="16" class="cad-desk" />
                            <rect x="745" y="185" width="85" height="16" class="cad-desk" />
                            <!-- Luminaires -->
                            <circle cx="680" cy="115" r="4.5" class="light-glow light-off" />
                            <circle cx="780" cy="115" r="4.5" class="light-glow light-off" />
                            <circle cx="680" cy="215" r="4.5" class="light-glow light-off" />
                            <circle cx="780" cy="215" r="4.5" class="light-glow light-off" />
                        </g>

                        <!-- ================= 4. WEST WING RADIAL ARC CLASSROOMS ================= -->
                        <!-- CR B-101 (WEST 1) -->
                        <g id="grp_r1">
                            <path d="M 40 230 L 220 250 L 210 360 L 30 340 Z" class="room-bg room-dark-bg" id="poly_r1" />
                            <text x="125" y="260" fill="#e2e8f0" font-family="'JetBrains Mono'" font-size="11" font-weight="bold">CR B-101 (96 m²)</text>
                            
                            <!-- Smartboard & Podium -->
                            <line x1="185" y1="275" x2="185" y2="325" stroke="#38bdf8" stroke-width="3" stroke-linecap="round" />
                            <rect x="175" y="295" width="8" height="10" fill="#1e3a5f" stroke="#60a5fa" stroke-width="1" />

                            <!-- 6 Dual Student Desks + Chairs -->
                            <g transform="translate(60, 275)">
                                <rect x="0" y="0" width="45" height="12" class="cad-desk" id="d1_r1" rx="2" />
                                <rect x="55" y="0" width="45" height="12" class="cad-desk" id="d2_r1" rx="2" />
                                <rect x="0" y="20" width="45" height="12" class="cad-desk" id="d3_r1" rx="2" />
                                <rect x="55" y="20" width="45" height="12" class="cad-desk" id="d4_r1" rx="2" />
                                <rect x="0" y="40" width="45" height="12" class="cad-desk" id="d5_r1" rx="2" />
                                <rect x="55" y="40" width="45" height="12" class="cad-desk" id="d6_r1" rx="2" />

                                <!-- Dynamic Student Headcount Dots -->
                                <circle cx="12" cy="6" r="3.5" class="cad-student-dot" id="dot1_r1" opacity="0" />
                                <circle cx="33" cy="6" r="3.5" class="cad-student-dot" id="dot2_r1" opacity="0" />
                                <circle cx="67" cy="6" r="3.5" class="cad-student-dot" id="dot3_r1" opacity="0" />
                                <circle cx="88" cy="6" r="3.5" class="cad-student-dot" id="dot4_r1" opacity="0" />
                                <circle cx="12" cy="26" r="3.5" class="cad-student-dot" id="dot5_r1" opacity="0" />
                                <circle cx="33" cy="26" r="3.5" class="cad-student-dot" id="dot6_r1" opacity="0" />
                            </g>

                            <!-- Ceiling Luminaires -->
                            <circle cx="85" cy="255" r="5" class="light-glow light-off" id="l1_r1" />
                            <circle cx="165" cy="260" r="5" class="light-glow light-off" id="l2_r1" />
                            <circle cx="80" cy="330" r="5" class="light-glow light-off" id="l3_r1" />
                            <circle cx="160" cy="335" r="5" class="light-glow light-off" id="l4_r1" />

                            <!-- Status Badge -->
                            <text x="195" y="352" fill="#64748b" font-family="'JetBrains Mono'" font-size="9" font-weight="bold" text-anchor="end" id="ac_r1">AC: OFF</text>
                        </g>

                        <!-- CR B-102 (WEST 2) -->
                        <g id="grp_r2">
                            <path d="M 30 355 L 210 375 L 200 485 L 20 465 Z" class="room-bg room-dark-bg" id="poly_r2" />
                            <text x="115" y="385" fill="#e2e8f0" font-family="'JetBrains Mono'" font-size="11" font-weight="bold">CR B-102 (84 m²)</text>
                            
                            <line x1="175" y1="400" x2="175" y2="450" stroke="#38bdf8" stroke-width="3" stroke-linecap="round" />
                            <rect x="165" y="420" width="8" height="10" fill="#1e3a5f" stroke="#60a5fa" stroke-width="1" />

                            <g transform="translate(50, 400)">
                                <rect x="0" y="0" width="45" height="12" class="cad-desk" id="d1_r2" rx="2" />
                                <rect x="55" y="0" width="45" height="12" class="cad-desk" id="d2_r2" rx="2" />
                                <rect x="0" y="20" width="45" height="12" class="cad-desk" id="d3_r2" rx="2" />
                                <rect x="55" y="20" width="45" height="12" class="cad-desk" id="d4_r2" rx="2" />
                                <rect x="0" y="40" width="45" height="12" class="cad-desk" id="d5_r2" rx="2" />
                                <rect x="55" y="40" width="45" height="12" class="cad-desk" id="d6_r2" rx="2" />

                                <circle cx="12" cy="6" r="3.5" class="cad-student-dot" id="dot1_r2" opacity="0" />
                                <circle cx="33" cy="6" r="3.5" class="cad-student-dot" id="dot2_r2" opacity="0" />
                                <circle cx="67" cy="6" r="3.5" class="cad-student-dot" id="dot3_r2" opacity="0" />
                                <circle cx="88" cy="6" r="3.5" class="cad-student-dot" id="dot4_r2" opacity="0" />
                            </g>

                            <circle cx="75" cy="380" r="5" class="light-glow light-off" id="l1_r2" />
                            <circle cx="155" cy="385" r="5" class="light-glow light-off" id="l2_r2" />
                            <circle cx="70" cy="455" r="5" class="light-glow light-off" id="l3_r2" />
                            <circle cx="150" cy="460" r="5" class="light-glow light-off" id="l4_r2" />

                            <text x="185" y="477" fill="#64748b" font-family="'JetBrains Mono'" font-size="9" font-weight="bold" text-anchor="end" id="ac_r2">AC: OFF</text>
                        </g>

                        <!-- CR B-103 (WEST 3) -->
                        <g id="grp_r3">
                            <path d="M 20 480 L 200 500 L 190 610 L 10 590 Z" class="room-bg room-dark-bg" id="poly_r3" />
                            <text x="105" y="510" fill="#e2e8f0" font-family="'JetBrains Mono'" font-size="11" font-weight="bold">CR B-103 (84 m²)</text>
                            
                            <line x1="165" y1="525" x2="165" y2="575" stroke="#38bdf8" stroke-width="3" stroke-linecap="round" />
                            <rect x="155" y="545" width="8" height="10" fill="#1e3a5f" stroke="#60a5fa" stroke-width="1" />

                            <g transform="translate(40, 525)">
                                <rect x="0" y="0" width="45" height="12" class="cad-desk" id="d1_r3" rx="2" />
                                <rect x="55" y="0" width="45" height="12" class="cad-desk" id="d2_r3" rx="2" />
                                <rect x="0" y="20" width="45" height="12" class="cad-desk" id="d3_r3" rx="2" />
                                <rect x="55" y="20" width="45" height="12" class="cad-desk" id="d4_r3" rx="2" />
                                <rect x="0" y="40" width="45" height="12" class="cad-desk" id="d5_r3" rx="2" />
                                <rect x="55" y="40" width="45" height="12" class="cad-desk" id="d6_r3" rx="2" />

                                <circle cx="12" cy="6" r="3.5" class="cad-student-dot" id="dot1_r3" opacity="0" />
                                <circle cx="33" cy="6" r="3.5" class="cad-student-dot" id="dot2_r3" opacity="0" />
                            </g>

                            <circle cx="65" cy="505" r="5" class="light-glow light-off" id="l1_r3" />
                            <circle cx="145" cy="510" r="5" class="light-glow light-off" id="l2_r3" />
                            <circle cx="60" cy="580" r="5" class="light-glow light-off" id="l3_r3" />
                            <circle cx="140" cy="585" r="5" class="light-glow light-off" id="l4_r3" />

                            <text x="175" y="602" fill="#64748b" font-family="'JetBrains Mono'" font-size="9" font-weight="bold" text-anchor="end" id="ac_r3">AC: OFF</text>
                        </g>

                        <!-- CR B-104 (WEST 4 - FAR END) -->
                        <g id="grp_r4">
                            <path d="M 10 605 L 190 625 L 180 735 L 0 715 Z" class="room-bg room-dark-bg" id="poly_r4" />
                            <text x="95" y="635" fill="#e2e8f0" font-family="'JetBrains Mono'" font-size="11" font-weight="bold">CR B-104 (96 m²)</text>
                            
                            <line x1="155" y1="650" x2="155" y2="700" stroke="#38bdf8" stroke-width="3" stroke-linecap="round" />
                            <rect x="145" y="670" width="8" height="10" fill="#1e3a5f" stroke="#60a5fa" stroke-width="1" />

                            <g transform="translate(30, 650)">
                                <rect x="0" y="0" width="45" height="12" class="cad-desk" id="d1_r4" rx="2" />
                                <rect x="55" y="0" width="45" height="12" class="cad-desk" id="d2_r4" rx="2" />
                                <rect x="0" y="20" width="45" height="12" class="cad-desk" id="d3_r4" rx="2" />
                                <rect x="55" y="20" width="45" height="12" class="cad-desk" id="d4_r4" rx="2" />
                                <rect x="0" y="40" width="45" height="12" class="cad-desk" id="d5_r4" rx="2" />
                                <rect x="55" y="40" width="45" height="12" class="cad-desk" id="d6_r4" rx="2" />
                            </g>

                            <circle cx="55" cy="630" r="5" class="light-glow light-off" id="l1_r4" />
                            <circle cx="135" cy="635" r="5" class="light-glow light-off" id="l2_r4" />
                            <circle cx="50" cy="705" r="5" class="light-glow light-off" id="l3_r4" />
                            <circle cx="130" cy="710" r="5" class="light-glow light-off" id="l4_r4" />

                            <text x="165" y="727" fill="#64748b" font-family="'JetBrains Mono'" font-size="9" font-weight="bold" text-anchor="end" id="ac_r4">AC: OFF</text>
                        </g>

                        <!-- ================= 5. EAST WING RADIAL ARC CLASSROOMS ================= -->
                        <!-- CR B-105 (EAST 1) -->
                        <g id="grp_r5">
                            <path d="M 880 250 L 1060 230 L 1070 340 L 890 360 Z" class="room-bg room-dark-bg" id="poly_r5" />
                            <text x="980" y="260" fill="#e2e8f0" font-family="'JetBrains Mono'" font-size="11" font-weight="bold" text-anchor="middle">CR B-105 (96 m²)</text>
                            
                            <line x1="915" y1="275" x2="915" y2="325" stroke="#38bdf8" stroke-width="3" stroke-linecap="round" />
                            <rect x="918" y="295" width="8" height="10" fill="#1e3a5f" stroke="#60a5fa" stroke-width="1" />

                            <g transform="translate(940, 275)">
                                <rect x="0" y="0" width="45" height="12" class="cad-desk" id="d1_r5" rx="2" />
                                <rect x="55" y="0" width="45" height="12" class="cad-desk" id="d2_r5" rx="2" />
                                <rect x="0" y="20" width="45" height="12" class="cad-desk" id="d3_r5" rx="2" />
                                <rect x="55" y="20" width="45" height="12" class="cad-desk" id="d4_r5" rx="2" />
                                <rect x="0" y="40" width="45" height="12" class="cad-desk" id="d5_r5" rx="2" />
                                <rect x="55" y="40" width="45" height="12" class="cad-desk" id="d6_r5" rx="2" />

                                <circle cx="12" cy="6" r="3.5" class="cad-student-dot" id="dot1_r5" opacity="0" />
                                <circle cx="33" cy="6" r="3.5" class="cad-student-dot" id="dot2_r5" opacity="0" />
                            </g>

                            <circle cx="940" cy="260" r="5" class="light-glow light-off" id="l1_r5" />
                            <circle cx="1020" cy="255" r="5" class="light-glow light-off" id="l2_r5" />
                            <circle cx="945" cy="335" r="5" class="light-glow light-off" id="l3_r5" />
                            <circle cx="1025" cy="330" r="5" class="light-glow light-off" id="l4_r5" />

                            <text x="1055" y="352" fill="#64748b" font-family="'JetBrains Mono'" font-size="9" font-weight="bold" text-anchor="end" id="ac_r5">AC: OFF</text>
                        </g>

                        <!-- CR B-106 (EAST 2) -->
                        <g id="grp_r6">
                            <path d="M 890 375 L 1070 355 L 1080 465 L 900 485 Z" class="room-bg room-dark-bg" id="poly_r6" />
                            <text x="990" y="385" fill="#e2e8f0" font-family="'JetBrains Mono'" font-size="11" font-weight="bold" text-anchor="middle">CR B-106 (84 m²)</text>
                            
                            <line x1="925" y1="400" x2="925" y2="450" stroke="#38bdf8" stroke-width="3" stroke-linecap="round" />
                            <rect x="928" y="420" width="8" height="10" fill="#1e3a5f" stroke="#60a5fa" stroke-width="1" />

                            <g transform="translate(950, 400)">
                                <rect x="0" y="0" width="45" height="12" class="cad-desk" id="d1_r6" rx="2" />
                                <rect x="55" y="0" width="45" height="12" class="cad-desk" id="d2_r6" rx="2" />
                                <rect x="0" y="20" width="45" height="12" class="cad-desk" id="d3_r6" rx="2" />
                                <rect x="55" y="20" width="45" height="12" class="cad-desk" id="d4_r6" rx="2" />
                                <rect x="0" y="40" width="45" height="12" class="cad-desk" id="d5_r6" rx="2" />
                                <rect x="55" y="40" width="45" height="12" class="cad-desk" id="d6_r6" rx="2" />
                            </g>

                            <circle cx="950" cy="385" r="5" class="light-glow light-off" id="l1_r6" />
                            <circle cx="1030" cy="380" r="5" class="light-glow light-off" id="l2_r6" />
                            <circle cx="955" cy="460" r="5" class="light-glow light-off" id="l3_r6" />
                            <circle cx="1035" cy="455" r="5" class="light-glow light-off" id="l4_r6" />

                            <text x="1065" y="477" fill="#64748b" font-family="'JetBrains Mono'" font-size="9" font-weight="bold" text-anchor="end" id="ac_r6">AC: OFF</text>
                        </g>

                        <!-- CR B-107 (EAST 3) -->
                        <g id="grp_r7">
                            <path d="M 900 500 L 1080 480 L 1090 590 L 910 610 Z" class="room-bg room-dark-bg" id="poly_r7" />
                            <text x="1000" y="510" fill="#e2e8f0" font-family="'JetBrains Mono'" font-size="11" font-weight="bold" text-anchor="middle">CR B-107 (84 m²)</text>
                            
                            <line x1="935" y1="525" x2="935" y2="575" stroke="#38bdf8" stroke-width="3" stroke-linecap="round" />
                            <rect x="938" y="545" width="8" height="10" fill="#1e3a5f" stroke="#60a5fa" stroke-width="1" />

                            <g transform="translate(960, 525)">
                                <rect x="0" y="0" width="45" height="12" class="cad-desk" id="d1_r7" rx="2" />
                                <rect x="55" y="0" width="45" height="12" class="cad-desk" id="d2_r7" rx="2" />
                                <rect x="0" y="20" width="45" height="12" class="cad-desk" id="d3_r7" rx="2" />
                                <rect x="55" y="20" width="45" height="12" class="cad-desk" id="d4_r7" rx="2" />
                                <rect x="0" y="40" width="45" height="12" class="cad-desk" id="d5_r7" rx="2" />
                                <rect x="55" y="40" width="45" height="12" class="cad-desk" id="d6_r7" rx="2" />
                            </g>

                            <circle cx="960" cy="510" r="5" class="light-glow light-off" id="l1_r7" />
                            <circle cx="1040" cy="505" r="5" class="light-glow light-off" id="l2_r7" />
                            <circle cx="965" cy="585" r="5" class="light-glow light-off" id="l3_r7" />
                            <circle cx="1045" cy="580" r="5" class="light-glow light-off" id="l4_r7" />

                            <text x="1075" y="602" fill="#64748b" font-family="'JetBrains Mono'" font-size="9" font-weight="bold" text-anchor="end" id="ac_r7">AC: OFF</text>
                        </g>

                        <!-- CR B-108 (EAST 4 - FAR END) -->
                        <g id="grp_r8">
                            <path d="M 910 625 L 1090 605 L 1100 715 L 920 735 Z" class="room-bg room-lit-bg" id="poly_r8" />
                            <text x="1010" y="635" fill="#facc15" font-family="'JetBrains Mono'" font-size="11" font-weight="bold" text-anchor="middle">CR B-108 (96 m²)</text>
                            
                            <line x1="945" y1="650" x2="945" y2="700" stroke="#facc15" stroke-width="3" stroke-linecap="round" />
                            <rect x="948" y="670" width="8" height="10" fill="#2d2208" stroke="#f59e0b" stroke-width="1" />

                            <g transform="translate(970, 650)">
                                <rect x="0" y="0" width="45" height="12" class="cad-desk cad-desk-lit" id="d1_r8" rx="2" />
                                <rect x="55" y="0" width="45" height="12" class="cad-desk cad-desk-lit" id="d2_r8" rx="2" />
                                <rect x="0" y="20" width="45" height="12" class="cad-desk cad-desk-lit" id="d3_r8" rx="2" />
                                <rect x="55" y="20" width="45" height="12" class="cad-desk cad-desk-lit" id="d4_r8" rx="2" />
                                <rect x="0" y="40" width="45" height="12" class="cad-desk cad-desk-lit" id="d5_r8" rx="2" />
                                <rect x="55" y="40" width="45" height="12" class="cad-desk cad-desk-lit" id="d6_r8" rx="2" />

                                <!-- Active Student Dots -->
                                <circle cx="12" cy="6" r="3.5" class="cad-student-dot" id="dot1_r8" opacity="1" />
                                <circle cx="33" cy="6" r="3.5" class="cad-student-dot" id="dot2_r8" opacity="1" />
                                <circle cx="67" cy="6" r="3.5" class="cad-student-dot" id="dot3_r8" opacity="1" />
                                <circle cx="88" cy="6" r="3.5" class="cad-student-dot" id="dot4_r8" opacity="1" />
                                <circle cx="12" cy="26" r="3.5" class="cad-student-dot" id="dot5_r8" opacity="1" />
                                <circle cx="33" cy="26" r="3.5" class="cad-student-dot" id="dot6_r8" opacity="1" />
                            </g>

                            <circle cx="970" cy="635" r="5.5" class="light-glow light-on" id="l1_r8" />
                            <circle cx="1050" cy="630" r="5.5" class="light-glow light-on" id="l2_r8" />
                            <circle cx="975" cy="710" r="5.5" class="light-glow light-on" id="l3_r8" />
                            <circle cx="1055" cy="705" r="5.5" class="light-glow light-on" id="l4_r8" />

                            <text x="1085" y="727" fill="#facc15" font-family="'JetBrains Mono'" font-size="9" font-weight="bold" text-anchor="end" id="ac_r8">AC: 26°C</text>
                        </g>

                        <!-- ================= 6. ELEVATOR BANKS & RESTROOMS ================= -->
                        <!-- WEST CORE: LIFT 1 & 2 + RESTROOMS -->
                        <g transform="translate(270, 410)">
                            <!-- Outer Frame -->
                            <rect width="100" height="210" fill="#080c14" stroke="#2563eb" stroke-width="2" rx="4" />

                            <!-- LIFT 1 -->
                            <rect x="8" y="8" width="40" height="52" fill="#064e3b" stroke="#10b981" stroke-width="1.8" rx="2" id="box_lift1" />
                            <line x1="28" y1="8" x2="28" y2="60" stroke="#047857" stroke-width="1.5" />
                            <text x="28" y="38" fill="#a7f3d0" font-family="'JetBrains Mono'" font-size="10" font-weight="bold" text-anchor="middle">L-1</text>

                            <!-- LIFT 2 -->
                            <rect x="52" y="8" width="40" height="52" fill="#064e3b" stroke="#10b981" stroke-width="1.8" rx="2" id="box_lift2" />
                            <line x1="72" y1="8" x2="72" y2="60" stroke="#047857" stroke-width="1.5" />
                            <text x="72" y="38" fill="#a7f3d0" font-family="'JetBrains Mono'" font-size="10" font-weight="bold" text-anchor="middle">L-2</text>

                            <!-- Lift Status Pill -->
                            <rect x="8" y="65" width="84" height="20" fill="#091410" stroke="#10b981" rx="3" />
                            <text x="50" y="79" fill="#10b981" font-family="'JetBrains Mono'" font-size="8" font-weight="bold" text-anchor="middle" id="lift_west_label">ACTIVE STANDBY</text>

                            <!-- RESTROOM (M) -->
                            <rect x="8" y="95" width="84" height="50" fill="#0c1220" stroke="#1e3a5f" rx="2" />
                            <rect x="8" y="95" width="84" height="50" fill="url(#tilePattern)" opacity="0.3" />
                            <text x="50" y="125" fill="#38bdf8" font-family="'JetBrains Mono'" font-size="9" font-weight="bold" text-anchor="middle">Toilet (M)</text>

                            <!-- RESTROOM (F) -->
                            <rect x="8" y="152" width="84" height="50" fill="#0c1220" stroke="#1e3a5f" rx="2" />
                            <rect x="8" y="152" width="84" height="50" fill="url(#tilePattern)" opacity="0.3" />
                            <text x="50" y="182" fill="#f472b6" font-family="'JetBrains Mono'" font-size="9" font-weight="bold" text-anchor="middle">Toilet (F)</text>
                        </g>

                        <!-- EAST CORE: LIFT 3 & 4 + RESTROOMS -->
                        <g transform="translate(730, 410)">
                            <rect width="100" height="210" fill="#080c14" stroke="#2563eb" stroke-width="2" rx="4" />

                            <!-- LIFT 3 -->
                            <rect x="8" y="8" width="40" height="52" fill="#111827" stroke="#374151" stroke-width="1.5" stroke-dasharray="3 3" rx="2" id="box_lift3" />
                            <line x1="28" y1="8" x2="28" y2="60" stroke="#1f2937" stroke-width="1.5" />
                            <text x="28" y="38" fill="#64748b" font-family="'JetBrains Mono'" font-size="10" font-weight="bold" text-anchor="middle">L-3</text>

                            <!-- LIFT 4 -->
                            <rect x="52" y="8" width="40" height="52" fill="#111827" stroke="#374151" stroke-width="1.5" stroke-dasharray="3 3" rx="2" id="box_lift4" />
                            <line x1="72" y1="8" x2="72" y2="60" stroke="#1f2937" stroke-width="1.5" />
                            <text x="72" y="38" fill="#64748b" font-family="'JetBrains Mono'" font-size="10" font-weight="bold" text-anchor="middle">L-4</text>

                            <!-- Lift Status Pill -->
                            <rect x="8" y="65" width="84" height="20" fill="#0e131d" stroke="#374151" rx="3" />
                            <text x="50" y="79" fill="#64748b" font-family="'JetBrains Mono'" font-size="8" font-weight="bold" text-anchor="middle" id="lift_east_label">DEEP SLEEP (0 W)</text>

                            <!-- RESTROOM (M) -->
                            <rect x="8" y="95" width="84" height="50" fill="#0c1220" stroke="#1e3a5f" rx="2" />
                            <rect x="8" y="95" width="84" height="50" fill="url(#tilePattern)" opacity="0.3" />
                            <text x="50" y="125" fill="#38bdf8" font-family="'JetBrains Mono'" font-size="9" font-weight="bold" text-anchor="middle">Toilet (M)</text>

                            <!-- RESTROOM (F) -->
                            <rect x="8" y="152" width="84" height="50" fill="#0c1220" stroke="#1e3a5f" rx="2" />
                            <rect x="8" y="152" width="84" height="50" fill="url(#tilePattern)" opacity="0.3" />
                            <text x="50" y="182" fill="#f472b6" font-family="'JetBrains Mono'" font-size="9" font-weight="bold" text-anchor="middle">Toilet (F)</text>
                        </g>

                        <!-- ================= 7. SOUTH WING ================= -->
                        <!-- STAIRCASE (SOUTH-WEST) -->
                        <g transform="translate(60, 760)">
                            <rect width="110" height="95" fill="#0a1222" stroke="#38bdf8" stroke-width="1.8" rx="4" />
                            <rect width="110" height="95" fill="url(#stairTreads)" />
                            <line x1="55" y1="10" x2="55" y2="85" stroke="#38bdf8" stroke-width="1.2" />
                            <text x="55" y="52" fill="#38bdf8" font-family="'JetBrains Mono'" font-size="9.5" font-weight="bold" text-anchor="middle">
                                STAIRS SW
                            </text>
                            <path d="M 55 20 L 55 75 L 50 67 M 55 75 L 60 67" stroke="#38bdf8" stroke-width="1.5" fill="none" />
                        </g>

                        <!-- FACULTY LOUNGE (80 m²) -->
                        <g transform="translate(190, 760)">
                            <rect width="160" height="100" fill="#0c1322" stroke="#1e3a5f" stroke-width="2" rx="4" />
                            <text x="80" y="40" fill="#93c5fd" font-family="'JetBrains Mono'" font-size="11" font-weight="bold" text-anchor="middle">Faculty Lounge</text>
                            <text x="80" y="58" fill="#64748b" font-family="'JetBrains Mono'" font-size="9" text-anchor="middle">(80 m²)</text>
                            
                            <!-- Conference Table + Armchairs -->
                            <rect x="35" y="70" width="90" height="20" rx="4" class="cad-desk" />
                            <circle cx="50" cy="65" r="4" class="cad-chair" />
                            <circle cx="80" cy="65" r="4" class="cad-chair" />
                            <circle cx="110" cy="65" r="4" class="cad-chair" />
                            <circle cx="50" cy="95" r="4" class="cad-chair" />
                            <circle cx="80" cy="95" r="4" class="cad-chair" />
                            <circle cx="110" cy="95" r="4" class="cad-chair" />
                        </g>

                        <!-- SEMINAR HALL (180 m²) -->
                        <g transform="translate(370, 750)">
                            <rect width="360" height="120" fill="#090e18" stroke="#2563eb" stroke-width="2" rx="4" />
                            <text x="180" y="32" fill="#ffffff" font-family="'JetBrains Mono'" font-size="13" font-weight="bold" text-anchor="middle">
                                Seminar Hall (180 m²)
                            </text>
                            <text x="180" y="48" fill="#64748b" font-family="'JetBrains Mono'" font-size="9" text-anchor="middle">
                                120-Seat Auditorium // Standby Cutoff Active
                            </text>

                            <!-- Stage & Podium -->
                            <rect x="130" y="60" width="100" height="16" fill="#1e293b" stroke="#38bdf8" rx="2" />
                            <rect x="172" y="62" width="16" height="12" fill="#38bdf8" rx="2" />

                            <!-- 3 Curved Tiered Seating Rows -->
                            <path d="M 50 90 Q 180 115 310 90" fill="none" stroke="#334155" stroke-width="4" stroke-linecap="round" />
                            <path d="M 60 105 Q 180 130 300 105" fill="none" stroke="#334155" stroke-width="4" stroke-linecap="round" />
                            <path d="M 70 120 Q 180 145 290 120" fill="none" stroke="#334155" stroke-width="4" stroke-linecap="round" />
                        </g>

                        <!-- COMPUTER LAB B-3 (150 m²) -->
                        <g transform="translate(750, 760)">
                            <rect width="170" height="100" fill="#0c1322" stroke="#1e3a5f" stroke-width="2" rx="4" />
                            <text x="85" y="38" fill="#93c5fd" font-family="'JetBrains Mono'" font-size="11" font-weight="bold" text-anchor="middle">Computer Lab B-3</text>
                            <text x="85" y="54" fill="#64748b" font-family="'JetBrains Mono'" font-size="9" text-anchor="middle">(150 m²)</text>

                            <!-- Workstation Rows with Dual Monitors -->
                            <g transform="translate(25, 68)">
                                <rect x="0" y="0" width="55" height="10" class="cad-desk" />
                                <rect x="65" y="0" width="55" height="10" class="cad-desk" />
                                <rect x="0" y="16" width="55" height="10" class="cad-desk" />
                                <rect x="65" y="16" width="55" height="10" class="cad-desk" />
                            </g>
                        </g>

                        <!-- STAIRCASE (SOUTH-EAST) -->
                        <g transform="translate(940, 760)">
                            <rect width="110" height="95" fill="#0a1222" stroke="#38bdf8" stroke-width="1.8" rx="4" />
                            <rect width="110" height="95" fill="url(#stairTreads)" />
                            <line x1="55" y1="10" x2="55" y2="85" stroke="#38bdf8" stroke-width="1.2" />
                            <text x="55" y="52" fill="#38bdf8" font-family="'JetBrains Mono'" font-size="9.5" font-weight="bold" text-anchor="middle">
                                STAIRS SE
                            </text>
                            <path d="M 55 20 L 55 75 L 50 67 M 55 75 L 60 67" stroke="#38bdf8" stroke-width="1.5" fill="none" />
                        </g>

                        <!-- ================= 8. ARCHITECTURAL CAD STRUCTURAL COLUMNS ================= -->
                        <g id="structural_columns">
                            <rect x="235" y="75" width="10" height="10" class="cad-column" />
                            <rect x="475" y="75" width="10" height="10" class="cad-column" />
                            <rect x="615" y="75" width="10" height="10" class="cad-column" />
                            <rect x="855" y="75" width="10" height="10" class="cad-column" />

                            <rect x="35" y="225" width="10" height="10" class="cad-column" />
                            <rect x="215" y="245" width="10" height="10" class="cad-column" />
                            <rect x="205" y="355" width="10" height="10" class="cad-column" />
                            <rect x="195" y="480" width="10" height="10" class="cad-column" />
                            <rect x="185" y="605" width="10" height="10" class="cad-column" />
                            <rect x="175" y="730" width="10" height="10" class="cad-column" />

                            <rect x="875" y="245" width="10" height="10" class="cad-column" />
                            <rect x="885" y="370" width="10" height="10" class="cad-column" />
                            <rect x="895" y="495" width="10" height="10" class="cad-column" />
                            <rect x="905" y="620" width="10" height="10" class="cad-column" />
                            <rect x="915" y="730" width="10" height="10" class="cad-column" />
                        </g>

                    </svg>
                </div>
            </div>

        </div>

    </div>

    <!-- JAVASCRIPT LOGIC & TELEGRAM PERSISTENCE -->
    <script>
        let currentRelocation = null;

        // Load stored telegram credentials on init
        window.addEventListener('DOMContentLoaded', () => {
            const savedToken = localStorage.getItem('gridsense_tg_token') || "";
            const savedChat = localStorage.getItem('gridsense_tg_chat') || "";
            if (savedToken) document.getElementById('tgToken').value = savedToken;
            if (savedChat) document.getElementById('tgChatId').value = savedChat;
            onParamChange(false);
        });

        function onParamChange(triggerPing = false) {
            const timeVal = parseFloat(document.getElementById('timeSlider').value);
            const hours = Math.floor(timeVal);
            const mins = (timeVal % 1 === 0.5) ? "30" : "00";
            const timeStr = `${hours < 10 ? '0' + hours : hours}:${mins}`;
            document.getElementById('timeVal').innerText = timeStr;

            const temp = document.getElementById('tempSlider').value;
            document.getElementById('tempVal').innerText = `${temp}°C`;

            const weather = document.getElementById('weatherSelect').value;

            const roomsPayload = {};
            for (let i = 1; i <= 8; i++) {
                const occ = parseInt(document.getElementById(`occ_r${i}`).value);
                document.getElementById(`val_r${i}`).innerText = occ;
                roomsPayload[`B10${i}`] = occ;
            }

            const payload = {
                floor: 1,
                time: timeStr,
                temperature: parseFloat(temp),
                weather: weather,
                rooms: roomsPayload
            };

            fetch('/api/sandbox/evaluate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            })
            .then(res => res.json())
            .then(data => {
                renderVectorState(data);
                if (triggerPing) triggerAutoTelegramPing(data);
            })
            .catch(err => console.error(err));
        }

        function renderVectorState(data) {
            document.getElementById('baselineMeter').innerText = `${data.total_baseline_kw} kW`;
            document.getElementById('optimizedMeter').innerText = `${data.total_optimized_kw} kW`;
            document.getElementById('savingsMeter').innerText = `${data.kw_saved} kW (${data.savings_percentage}%)`;
            document.getElementById('inrMeter').innerText = `INR ${data.inr_per_hour_saved} / Hour Saved`;
            document.getElementById('elevState').innerText = data.elevator_mode;

            // Room states update
            const rooms = data.rooms;
            for (let i = 1; i <= 8; i++) {
                const r_id = `B10${i}`;
                const r = rooms[r_id];
                if (!r) continue;

                const poly = document.getElementById(`poly_r${i}`);
                const ac = document.getElementById(`ac_r${i}`);
                const occCount = parseInt(document.getElementById(`occ_r${i}`).value);

                if (r.lighting_glow) {
                    if (poly) poly.setAttribute('class', 'room-bg room-lit-bg');
                    for (let l = 1; l <= 4; l++) {
                        const light = document.getElementById(`l${l}_r${i}`);
                        if (light) light.setAttribute('class', 'light-glow light-on');
                    }
                    for (let d = 1; d <= 6; d++) {
                        const desk = document.getElementById(`d${d}_r${i}`);
                        if (desk) desk.setAttribute('class', 'cad-desk cad-desk-lit');
                    }
                    for (let dt = 1; dt <= 6; dt++) {
                        const dot = document.getElementById(`dot${dt}_r${i}`);
                        if (dot) dot.setAttribute('opacity', (occCount > (dt - 1) * 7) ? '1' : '0');
                    }
                    if (ac) {
                        ac.textContent = `AC: ${r.ac_setpoint}`;
                        ac.setAttribute('fill', '#facc15');
                    }
                } else {
                    if (poly) poly.setAttribute('class', 'room-bg room-dark-bg');
                    for (let l = 1; l <= 4; l++) {
                        const light = document.getElementById(`l${l}_r${i}`);
                        if (light) light.setAttribute('class', 'light-glow light-off');
                    }
                    for (let d = 1; d <= 6; d++) {
                        const desk = document.getElementById(`d${d}_r${i}`);
                        if (desk) desk.setAttribute('class', 'cad-desk');
                    }
                    for (let dt = 1; dt <= 6; dt++) {
                        const dot = document.getElementById(`dot${dt}_r${i}`);
                        if (dot) dot.setAttribute('opacity', '0');
                    }
                    if (ac) {
                        ac.textContent = `AC: OFF`;
                        ac.setAttribute('fill', '#64748b');
                    }
                }
            }

            // Hallway relay arcs & luminaire dots
            const westLit = (rooms['B101']?.lighting_glow || rooms['B102']?.lighting_glow || rooms['B103']?.lighting_glow || rooms['B104']?.lighting_glow);
            const eastLit = (rooms['B105']?.lighting_glow || rooms['B106']?.lighting_glow || rooms['B107']?.lighting_glow || rooms['B108']?.lighting_glow);

            const westArc = document.getElementById('corridor_west_arc');
            const eastArc = document.getElementById('corridor_east_arc');

            if (westArc) westArc.setAttribute('class', westLit ? 'corridor-path-lit' : 'corridor-path-dark');
            if (eastArc) eastArc.setAttribute('class', eastLit ? 'corridor-path-lit' : 'corridor-path-dark');

            for (let i = 1; i <= 4; i++) {
                const cw = document.getElementById(`cw${i}`);
                const ce = document.getElementById(`ce${i}`);
                if (cw) cw.setAttribute('class', westLit ? 'light-glow light-on' : 'light-glow light-off');
                if (ce) ce.setAttribute('class', eastLit ? 'light-glow light-on' : 'light-glow light-off');
            }

            // Lift status update
            const b1 = document.getElementById('box_lift1');
            const b2 = document.getElementById('box_lift2');
            const b3 = document.getElementById('box_lift3');
            const b4 = document.getElementById('box_lift4');
            const wl = document.getElementById('lift_west_label');
            const el = document.getElementById('lift_east_label');

            if (data.total_optimized_kw > 15) {
                // All 4 lifts active
                if (b1) b1.setAttribute('fill', '#064e3b');
                if (b2) b2.setAttribute('fill', '#064e3b');
                if (b3) b3.setAttribute('fill', '#064e3b');
                if (b4) b4.setAttribute('fill', '#064e3b');
                if (wl) wl.innerText = "ACTIVE STANDBY";
                if (el) el.innerText = "ACTIVE STANDBY";
            } else {
                // Lifts 3 & 4 in Deep Sleep
                if (b3) b3.setAttribute('fill', '#111827');
                if (b4) b4.setAttribute('fill', '#111827');
                if (el) el.innerText = "DEEP SLEEP (0 W)";
            }

            // Relocation nudge banner
            const relocs = data.relocations || [];
            const alertCard = document.getElementById('alertCard');
            const alertText = document.getElementById('alertText');

            if (relocs.length > 0) {
                currentRelocation = relocs[0];
                alertCard.style.display = "flex";
                alertText.innerText = currentRelocation.reason;
            } else {
                currentRelocation = null;
                alertCard.style.display = "none";
            }
        }

        function applyConsolidation() {
            if (currentRelocation) {
                const fromId = currentRelocation.from_room;
                const toId = currentRelocation.to_room;
                const fromIdx = parseInt(fromId.slice(-1));
                const toIdx = parseInt(toId.slice(-1));

                const students = parseInt(document.getElementById(`occ_r${fromIdx}`).value);
                document.getElementById(`occ_r${fromIdx}`).value = 0;
                document.getElementById(`occ_r${toIdx}`).value = students;
                onParamChange(true);
            }
        }

        function applyPreset(type) {
            if (type === 'morning') {
                document.getElementById('timeSlider').value = 9.0;
                document.getElementById('tempSlider').value = 27;
                document.getElementById('weatherSelect').value = "Sunny / Daylight";
                for (let i = 1; i <= 8; i++) document.getElementById(`occ_r${i}`).value = (i <= 6) ? 45 : 0;
            } else if (type === 'afternoon') {
                document.getElementById('timeSlider').value = 14.5;
                document.getElementById('tempSlider').value = 35;
                document.getElementById('weatherSelect').value = "Sunny / Daylight";
                for (let i = 1; i <= 8; i++) document.getElementById(`occ_r${i}`).value = 40;
            } else if (type === 'night_waste') {
                document.getElementById('timeSlider').value = 19.5;
                document.getElementById('tempSlider').value = 32;
                document.getElementById('weatherSelect').value = "Night";
                for (let i = 1; i <= 7; i++) document.getElementById(`occ_r${i}`).value = 0;
                document.getElementById(`occ_r8`).value = 25;
            } else if (type === 'lockdown') {
                document.getElementById('timeSlider').value = 22.0;
                document.getElementById('tempSlider').value = 25;
                document.getElementById('weatherSelect').value = "Night";
                for (let i = 1; i <= 8; i++) document.getElementById(`occ_r${i}`).value = 0;
            }
            onParamChange(false);
        }

        function clearAllOccupants() {
            for (let i = 1; i <= 8; i++) document.getElementById(`occ_r${i}`).value = 0;
            onParamChange(false);
        }

        function saveAndTestTelegram() {
            const token = document.getElementById('tgToken').value.trim();
            const chatId = document.getElementById('tgChatId').value.trim();

            if (!token || !chatId) {
                alert("Please enter both Bot Token and Chat ID to connect your phone.");
                return;
            }

            localStorage.setItem('gridsense_tg_token', token);
            localStorage.setItem('gridsense_tg_chat', chatId);

            const st = document.getElementById('tgStatus');
            st.innerText = "Dispatching test handshake ping...";

            fetch('/api/sandbox/notify-telegram', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    token: token,
                    chat_id: chatId,
                    message: "GridSense Connected: JIT Block B Digital Twin linked to your mobile. Automatic optimization nudges active."
                })
            })
            .then(res => res.json())
            .then(data => {
                if (data.status === 'success') {
                    st.innerText = "Verified! Connected to your mobile phone.";
                    st.classList.add('text-emerald-400');
                } else {
                    st.innerText = "Telegram Error: " + data.message;
                    st.classList.add('text-rose-400');
                }
            })
            .catch(err => {
                st.innerText = "Network Error: " + err;
            });
        }

        function triggerAutoTelegramPing(data) {
            const token = localStorage.getItem('gridsense_tg_token');
            const chatId = localStorage.getItem('gridsense_tg_chat');
            if (!token || !chatId) return;

            let msg = `GridSense Alert [JIT Block B]: Relocation executed. Total power cut to ${data.total_optimized_kw} kW. Immediate savings: ${data.kw_saved} kW (${data.savings_percentage}%). Hourly financial savings: INR ${data.inr_per_hour_saved}/hr.`;

            fetch('/api/sandbox/notify-telegram', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    token: token,
                    chat_id: chatId,
                    message: msg
                })
            }).catch(e => console.log('Telegram ping error:', e));
        }
    </script>
</body>
</html>
"""
