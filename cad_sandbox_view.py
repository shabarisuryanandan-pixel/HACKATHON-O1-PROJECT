"""
Interactive Sandbox - Block B Vector Floor Plan
GridSense Campus Energy Optimization Platform
"""

def render_cad_sandbox_html():
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GridSense // Sandbox</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Inter', sans-serif;
            background-color: #2B2D31;
            color: #D9DAD0;
        }
        .font-mono { font-family: 'JetBrains Mono', monospace; }

        /* Flat Card System */
        .gs-card {
            background: #36393F;
            border-radius: 10px;
            border: 1px solid rgba(255,255,255,0.06);
        }
        .gs-inset {
            background: #2B2D31;
            border-radius: 8px;
            border: 1px solid rgba(255,255,255,0.06);
        }
        .gs-btn {
            background: #2B2D31;
            border-radius: 8px;
            border: 1px solid rgba(255,255,255,0.06);
            transition: all 0.15s ease;
            cursor: pointer;
        }
        .gs-btn:hover {
            border-color: #FFC93C;
            color: #FFC93C;
        }

        /* Nav */
        .gs-nav {
            background: #36393F;
            border-bottom: 1px solid rgba(255,255,255,0.06);
        }
        .gs-nav a {
            color: #8E9297;
            text-decoration: none;
            font-size: 13px;
            font-weight: 600;
            padding: 8px 16px;
            border-radius: 6px;
            transition: all 0.15s ease;
        }
        .gs-nav a:hover { color: #D9DAD0; }
        .gs-nav a.active {
            color: #FFC93C;
            background: rgba(255,201,60,0.08);
        }

        /* Mode Tabs */
        .mode-tab {
            flex: 1;
            padding: 10px 0;
            text-align: center;
            font-family: 'Inter', sans-serif;
            font-size: 13px;
            font-weight: 600;
            color: #8E9297;
            background: transparent;
            border: none;
            border-bottom: 2px solid transparent;
            cursor: pointer;
            transition: all 0.15s ease;
        }
        .mode-tab:hover { color: #D9DAD0; }
        .mode-tab.active {
            color: #FFC93C;
            border-bottom-color: #FFC93C;
        }

        /* Timetable Grid */
        .tt-slot {
            padding: 8px 10px;
            border-radius: 6px;
            border: 1px solid rgba(255,255,255,0.06);
            background: #2B2D31;
            cursor: pointer;
            transition: all 0.15s ease;
        }
        .tt-slot:hover {
            border-color: #FFC93C;
        }
        .tt-slot.active {
            border-color: #FFC93C;
            background: rgba(255,201,60,0.06);
        }

        /* Blueprint Canvas */
        .blueprint-board {
            background-color: #1E2025;
            background-image:
                linear-gradient(rgba(255,255,255,0.04) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255,255,255,0.04) 1px, transparent 1px);
            background-size: 20px 20px;
            border: 1px solid rgba(255,255,255,0.06);
            border-radius: 10px;
        }

        /* Room Lighting States */
        .room-bg {
            transition: fill 0.3s ease, stroke 0.3s ease, filter 0.3s ease;
        }
        .room-lit-bg {
            fill: rgba(255,201,60,0.08) !important;
            stroke: #FFC93C !important;
            stroke-width: 2 !important;
            filter: drop-shadow(0 0 12px rgba(255,201,60,0.25));
        }
        .room-dark-bg {
            fill: #2B2D31 !important;
            stroke: #4A4D52 !important;
            stroke-width: 1.5 !important;
        }

        /* Desks */
        .cad-desk {
            fill: #36393F;
            stroke: #4A4D52;
            stroke-width: 1;
            transition: all 0.3s ease;
        }
        .cad-desk-lit {
            fill: rgba(255,201,60,0.12) !important;
            stroke: #FFC93C !important;
            stroke-width: 1 !important;
        }
        .cad-chair {
            fill: #2B2D31;
            stroke: #4A4D52;
            stroke-width: 0.8;
            transition: all 0.3s ease;
        }
        .cad-student-dot {
            fill: #FFC93C;
            filter: drop-shadow(0 0 3px rgba(255,201,60,0.6));
            transition: opacity 0.3s ease;
        }

        /* Ceiling Lights */
        .light-glow {
            transition: all 0.3s ease;
        }
        .light-on {
            fill: #FFC93C;
            stroke: #FFC93C;
            stroke-width: 1.5;
            filter: drop-shadow(0 0 6px #FFC93C) drop-shadow(0 0 14px rgba(255,201,60,0.7));
        }
        .light-off {
            fill: #4A4D52;
            stroke: #4A4D52;
            stroke-width: 1;
            filter: none;
        }

        /* Corridor */
        .corridor-path-lit {
            stroke: #FFC93C !important;
            stroke-width: 3 !important;
            stroke-dasharray: none !important;
            filter: drop-shadow(0 0 8px rgba(255,201,60,0.7));
            transition: all 0.4s ease;
        }
        .corridor-path-dark {
            stroke: #4A4D52 !important;
            stroke-width: 1.5 !important;
            stroke-dasharray: 6 6 !important;
            filter: none;
            transition: all 0.4s ease;
        }

        /* Structural */
        .cad-column {
            fill: #4A4D52;
            stroke: #8E9297;
            stroke-width: 1;
        }
        .cad-door-swing {
            stroke: #8E9297;
            stroke-width: 1;
            stroke-dasharray: 2 2;
            fill: none;
        }

        /* Slider styling */
        input[type="range"] {
            -webkit-appearance: none;
            appearance: none;
            width: 100%;
            height: 4px;
            background: #2B2D31;
            border-radius: 2px;
            outline: none;
            cursor: pointer;
        }
        input[type="range"]::-webkit-slider-thumb {
            -webkit-appearance: none;
            width: 14px;
            height: 14px;
            border-radius: 50%;
            background: #FFC93C;
            cursor: pointer;
        }
        input[type="range"]::-moz-range-thumb {
            width: 14px;
            height: 14px;
            border-radius: 50%;
            background: #FFC93C;
            border: none;
            cursor: pointer;
        }

        select {
            -webkit-appearance: none;
            appearance: none;
        }

        /* Scrollbar */
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: #2B2D31; }
        ::-webkit-scrollbar-thumb { background: #4A4D52; border-radius: 3px; }
    </style>
</head>
<body class="min-h-screen">

    <!-- NAVIGATION BAR -->
    <nav class="gs-nav px-6 py-3 flex items-center justify-between">
        <div class="flex items-center gap-2">
            <span style="color:#FFC93C; font-weight:800; font-size:18px; letter-spacing:-0.5px;">GridSense</span>
        </div>
        <div class="flex items-center gap-1">
            <a href="/">Dashboard</a>
            <a href="/sandbox" class="active">Sandbox</a>
            <a href="/blueprint">Blueprint</a>
        </div>
    </nav>

    <!-- MAIN LAYOUT -->
    <div class="p-4 max-w-[1560px] mx-auto">
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-4">

            <!-- LEFT PANEL -->
            <div class="lg:col-span-4 space-y-4">

                <!-- MODE SWITCHER -->
                <div class="gs-card overflow-hidden">
                    <div class="flex border-b" style="border-color:rgba(255,255,255,0.06);">
                        <button class="mode-tab active" id="tabVariable" onclick="switchMode('variable')">Variable</button>
                        <button class="mode-tab" id="tabTimetable" onclick="switchMode('timetable')">Timetable</button>
                    </div>

                    <!-- VARIABLE MODE PANEL -->
                    <div id="panelVariable" class="p-4 space-y-4">

                        <!-- Quick Scenarios -->
                        <div>
                            <div class="flex justify-between items-center mb-2">
                                <span class="text-xs font-mono uppercase" style="color:#8E9297; font-weight:700;">Quick Scenarios</span>
                                <span class="text-xs font-mono" style="color:#FFC93C;">1-Click</span>
                            </div>
                            <div class="grid grid-cols-2 gap-2">
                                <button onclick="applyPreset('morning')" class="gs-btn p-2 text-left">
                                    <div class="text-xs font-mono font-bold" style="color:#D9DAD0;">09:00 AM</div>
                                    <div class="text-xs font-mono" style="color:#8E9297; font-size:10px;">Full Morning Rush</div>
                                </button>
                                <button onclick="applyPreset('afternoon')" class="gs-btn p-2 text-left">
                                    <div class="text-xs font-mono font-bold" style="color:#D9DAD0;">02:30 PM</div>
                                    <div class="text-xs font-mono" style="color:#8E9297; font-size:10px;">Peak Heat + Solar</div>
                                </button>
                                <button onclick="applyPreset('night_waste')" class="gs-btn p-2 text-left" style="border-color:rgba(255,201,60,0.3);">
                                    <div class="text-xs font-mono font-bold" style="color:#FFC93C;">07:30 PM</div>
                                    <div class="text-xs font-mono" style="color:rgba(255,201,60,0.7); font-size:10px;">After-Hours Waste</div>
                                </button>
                                <button onclick="applyPreset('lockdown')" class="gs-btn p-2 text-left">
                                    <div class="text-xs font-mono font-bold" style="color:#D9DAD0;">22:00 PM</div>
                                    <div class="text-xs font-mono" style="color:#8E9297; font-size:10px;">Night Lockdown (0 Occ)</div>
                                </button>
                            </div>
                        </div>

                        <!-- Environmental Controls -->
                        <div class="space-y-3">
                            <div class="text-xs font-mono uppercase" style="color:#8E9297; font-weight:700;">Environmental Inputs</div>

                            <div>
                                <div class="flex justify-between text-xs font-mono mb-1">
                                    <span style="color:#8E9297;">Time of Day</span>
                                    <span id="timeVal" class="font-bold" style="color:#FFC93C;">19:30</span>
                                </div>
                                <input type="range" id="timeSlider" min="6" max="23" step="0.5" value="19.5" oninput="onParamChange()">
                            </div>

                            <div>
                                <div class="flex justify-between text-xs font-mono mb-1">
                                    <span style="color:#8E9297;">Outdoor Temperature</span>
                                    <span id="tempVal" class="font-bold" style="color:#FFC93C;">33 C</span>
                                </div>
                                <input type="range" id="tempSlider" min="20" max="40" step="1" value="33" oninput="onParamChange()">
                            </div>

                            <div>
                                <div class="text-xs font-mono mb-1" style="color:#8E9297;">Sky / Natural Daylight</div>
                                <select id="weatherSelect" onchange="onParamChange()" class="w-full p-2 gs-inset text-xs font-mono outline-none" style="color:#D9DAD0;">
                                    <option value="Sunny / Daylight">Sunny / Bright (Daylight Harvesting)</option>
                                    <option value="Overcast / Rainy">Overcast / Rainy (Low Natural Lux)</option>
                                    <option value="Night" selected>Night (Zero Daylight)</option>
                                </select>
                            </div>
                        </div>

                        <!-- Room Headcounts -->
                        <div class="space-y-2">
                            <div class="flex justify-between items-center">
                                <span class="text-xs font-mono uppercase" style="color:#8E9297; font-weight:700;">Room Headcounts</span>
                                <button onclick="clearAllOccupants()" class="text-xs font-mono" style="color:#8E9297; cursor:pointer;" onmouseover="this.style.color='#FFC93C'" onmouseout="this.style.color='#8E9297'">Clear All</button>
                            </div>

                            <div class="grid grid-cols-2 gap-2 text-xs font-mono" style="color:#8E9297;">
                                <div class="p-2 gs-inset">
                                    <div class="flex justify-between mb-1">
                                        <span>B-101 (W1)</span>
                                        <span id="val_r1" class="font-bold" style="color:#FFFFFF;">0</span>
                                    </div>
                                    <input type="range" id="occ_r1" min="0" max="60" value="0" oninput="onParamChange()">
                                </div>
                                <div class="p-2 gs-inset">
                                    <div class="flex justify-between mb-1">
                                        <span>B-105 (E1)</span>
                                        <span id="val_r5" class="font-bold" style="color:#FFFFFF;">0</span>
                                    </div>
                                    <input type="range" id="occ_r5" min="0" max="60" value="0" oninput="onParamChange()">
                                </div>
                                <div class="p-2 gs-inset">
                                    <div class="flex justify-between mb-1">
                                        <span>B-102 (W2)</span>
                                        <span id="val_r2" class="font-bold" style="color:#FFFFFF;">0</span>
                                    </div>
                                    <input type="range" id="occ_r2" min="0" max="60" value="0" oninput="onParamChange()">
                                </div>
                                <div class="p-2 gs-inset">
                                    <div class="flex justify-between mb-1">
                                        <span>B-106 (E2)</span>
                                        <span id="val_r6" class="font-bold" style="color:#FFFFFF;">0</span>
                                    </div>
                                    <input type="range" id="occ_r6" min="0" max="60" value="0" oninput="onParamChange()">
                                </div>
                                <div class="p-2 gs-inset">
                                    <div class="flex justify-between mb-1">
                                        <span>B-103 (W3)</span>
                                        <span id="val_r3" class="font-bold" style="color:#FFFFFF;">0</span>
                                    </div>
                                    <input type="range" id="occ_r3" min="0" max="60" value="0" oninput="onParamChange()">
                                </div>
                                <div class="p-2 gs-inset">
                                    <div class="flex justify-between mb-1">
                                        <span>B-107 (E3)</span>
                                        <span id="val_r7" class="font-bold" style="color:#FFFFFF;">0</span>
                                    </div>
                                    <input type="range" id="occ_r7" min="0" max="60" value="0" oninput="onParamChange()">
                                </div>
                                <div class="p-2 gs-inset">
                                    <div class="flex justify-between mb-1">
                                        <span>B-104 (W4)</span>
                                        <span id="val_r4" class="font-bold" style="color:#FFFFFF;">0</span>
                                    </div>
                                    <input type="range" id="occ_r4" min="0" max="60" value="0" oninput="onParamChange()">
                                </div>
                                <div class="p-2 gs-inset" style="border-color:rgba(255,201,60,0.2);">
                                    <div class="flex justify-between mb-1">
                                        <span style="color:#FFC93C;">B-108 (E4)</span>
                                        <span id="val_r8" class="font-bold" style="color:#FFC93C;">25</span>
                                    </div>
                                    <input type="range" id="occ_r8" min="0" max="60" value="25" oninput="onParamChange()">
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- TIMETABLE MODE PANEL -->
                    <div id="panelTimetable" class="p-4 space-y-3" style="display:none;">
                        <div class="flex justify-between items-center">
                            <span class="text-xs font-mono uppercase" style="color:#8E9297; font-weight:700;">Academic Day Schedule</span>
                            <span class="text-xs font-mono" style="color:#FFC93C;">Block B</span>
                        </div>
                        <p class="text-xs" style="color:#8E9297;">Select a time slot to auto-fill room occupancy from the timetable. Rooms not listed are empty (0).</p>

                        <div class="space-y-2" id="timetableSlots">
                            <!-- Slots injected by JS -->
                        </div>
                    </div>
                </div>

                <!-- TELEGRAM CONFIG -->
                <div class="gs-card p-4 space-y-2">
                    <div class="flex justify-between items-center">
                        <span class="text-xs font-mono uppercase" style="color:#8E9297; font-weight:700;">Mobile Dispatch (Telegram)</span>
                        <span class="flex items-center gap-1.5 text-xs font-mono" style="color:#FFC93C;">
                            <span style="width:6px; height:6px; border-radius:50%; background:#FFC93C; display:inline-block;"></span>
                            Auto-Push
                        </span>
                    </div>
                    <input type="text" id="tgToken" placeholder="Bot Token (e.g. 7829...)" class="w-full p-2 gs-inset text-xs font-mono outline-none" style="color:#D9DAD0;">
                    <input type="text" id="tgChatId" placeholder="Chat ID (e.g. 9821...)" class="w-full p-2 gs-inset text-xs font-mono outline-none" style="color:#D9DAD0;">
                    <button onclick="saveAndTestTelegram()" class="w-full py-2 gs-btn text-xs font-mono font-bold" style="color:#FFC93C;">
                        Connect Phone + Test Alert
                    </button>
                    <div id="tgStatus" class="text-xs font-mono text-center" style="color:#8E9297; font-size:10px;">
                        Configuration saved locally. Actions dispatch live to your device.
                    </div>
                </div>

            </div>

            <!-- RIGHT PANEL -->
            <div class="lg:col-span-8 space-y-4">

                <!-- STAT GAUGES -->
                <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
                    <div class="gs-card p-3">
                        <div class="text-xs font-mono uppercase" style="color:#8E9297; font-size:10px;">Unmanaged Baseline</div>
                        <div id="baselineMeter" class="text-xl font-bold mt-1" style="color:#ED4245;">28.40 kW</div>
                        <div class="text-xs font-mono" style="color:#8E9297; font-size:10px;">Blind Power Draw (Zero Sensing)</div>
                    </div>
                    <div class="gs-card p-3">
                        <div class="text-xs font-mono uppercase" style="color:#8E9297; font-size:10px;">GridSense Optimized</div>
                        <div id="optimizedMeter" class="text-xl font-bold mt-1" style="color:#57F287;">6.25 kW</div>
                        <div class="text-xs font-mono" style="color:#8E9297; font-size:10px;">Adaptive HVAC + Corridor Cutoffs</div>
                    </div>
                    <div class="gs-card p-3">
                        <div class="text-xs font-mono uppercase" style="color:#8E9297; font-size:10px;">Savings Rate</div>
                        <div id="savingsMeter" class="text-xl font-bold mt-1" style="color:#FFC93C;">22.15 kW (78.0%)</div>
                        <div id="inrMeter" class="text-xs font-mono" style="color:#FFC93C; font-size:10px;">INR 199.35 / Hour Saved</div>
                    </div>
                </div>

                <!-- CONSOLIDATION BANNER -->
                <div id="alertCard" class="gs-card p-3 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3" style="border-left: 3px solid #FFC93C;">
                    <div class="space-y-1">
                        <div class="flex items-center gap-2 text-xs font-mono font-bold uppercase" style="color:#FFC93C;">
                            <span style="width:8px; height:8px; border-radius:50%; background:#FFC93C; display:inline-block; animation: pulse 2s infinite;"></span>
                            Spatial Consolidation Nudge Triggered
                        </div>
                        <p id="alertText" class="text-xs font-mono" style="color:#D9DAD0;">
                            Isolated class in CR B-108 (Far East Wing). Relocate to CR B-101 (near main stairs) to shut down East Corridor and cut 3.8 kW.
                        </p>
                    </div>
                    <button onclick="applyConsolidation()" class="px-4 py-2 gs-btn text-xs font-mono font-bold shrink-0" style="color:#FFC93C; border-color:#FFC93C;">
                        Apply Relocation
                    </button>
                </div>

                <!-- BLUEPRINT CANVAS -->
                <div class="gs-card p-4 space-y-2">
                    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 pb-2" style="border-bottom:1px solid rgba(255,255,255,0.06);">
                        <div>
                            <div class="flex items-center gap-2">
                                <span class="px-2 py-0.5 rounded font-mono text-xs font-bold" style="background:#FFC93C; color:#2B2D31;">BLOCK B</span>
                                <span class="text-xs font-bold uppercase tracking-wider font-mono" style="color:#FFFFFF;">Architectural CAD Blueprint</span>
                            </div>
                            <p class="text-xs font-mono mt-0.5" style="color:#8E9297; font-size:10px;">
                                Built-up Area: ~7,500 m2 | G+4 | Radial Arc Geometry with Desks, Luminaires + Relays
                            </p>
                        </div>
                        <div id="elevState" class="text-xs font-mono font-bold gs-inset px-3 py-1" style="color:#FFC93C; font-size:10px;">
                            Lifts 1 + 2 Active | Lifts 3 + 4 Deep Sleep
                        </div>
                    </div>

                    <!-- SVG BLUEPRINT -->
                    <div class="blueprint-board p-2 sm:p-3 overflow-x-auto">
                        <svg viewBox="0 0 1100 920" class="w-full h-auto min-w-[750px]">
                            <defs>
                                <filter id="luminaireGlow" x="-50%" y="-50%" width="200%" height="200%">
                                    <feGaussianBlur stdDeviation="7" result="blur" />
                                    <feMerge>
                                        <feMergeNode in="blur" />
                                        <feMergeNode in="SourceGraphic" />
                                    </feMerge>
                                </filter>

                                <pattern id="stairTreads" width="8" height="8" patternUnits="userSpaceOnUse">
                                    <line x1="0" y1="4" x2="8" y2="4" stroke="#8E9297" stroke-width="0.8" opacity="0.3" />
                                </pattern>

                                <pattern id="tilePattern" width="12" height="12" patternUnits="userSpaceOnUse">
                                    <rect width="12" height="12" fill="none" stroke="#4A4D52" stroke-width="0.6" />
                                </pattern>
                            </defs>

                            <!-- TITLE BLOCK -->
                            <g transform="translate(420, 20)">
                                <rect width="260" height="28" rx="6" fill="#FFC93C" />
                                <text x="130" y="19" fill="#2B2D31" font-family="'JetBrains Mono'" font-size="11" font-weight="bold" text-anchor="middle" letter-spacing="1">
                                    BLOCK B - FLOOR PLAN (G+4)
                                </text>
                            </g>

                            <!-- ================= 1. CENTRAL ATRIUM ================= -->
                            <g id="central_atrium">
                                <circle cx="550" cy="490" r="165" fill="#1E2025" stroke="#4A4D52" stroke-width="2" />
                                <circle cx="550" cy="490" r="140" fill="#2B2D31" stroke="#4A4D52" stroke-width="1" stroke-dasharray="6 4" />
                                <circle cx="550" cy="490" r="95" fill="#1E2025" stroke="#8E9297" stroke-width="1.5" />

                                <!-- Skylight Radial Spokes -->
                                <line x1="455" y1="490" x2="645" y2="490" stroke="#4A4D52" stroke-width="1" />
                                <line x1="550" y1="395" x2="550" y2="585" stroke="#4A4D52" stroke-width="1" />
                                <line x1="483" y1="423" x2="617" y2="557" stroke="#4A4D52" stroke-width="1" />
                                <line x1="483" y1="557" x2="617" y2="423" stroke="#4A4D52" stroke-width="1" />

                                <text x="550" y="485" fill="#D9DAD0" font-family="'JetBrains Mono'" font-size="13" font-weight="bold" text-anchor="middle">
                                    Central Atrium
                                </text>
                                <text x="550" y="505" fill="#8E9297" font-family="'JetBrains Mono'" font-size="9.5" text-anchor="middle">
                                    (Open to Above)
                                </text>

                                <!-- Curved Seating -->
                                <path d="M 445 440 A 120 120 0 0 1 445 540" fill="none" stroke="#4A4D52" stroke-width="6" stroke-linecap="round" />
                                <path d="M 655 440 A 120 120 0 0 0 655 540" fill="none" stroke="#4A4D52" stroke-width="6" stroke-linecap="round" />

                                <!-- Planters -->
                                <circle cx="465" cy="415" r="9" fill="#2B2D31" stroke="#8E9297" stroke-width="1" />
                                <circle cx="635" cy="415" r="9" fill="#2B2D31" stroke="#8E9297" stroke-width="1" />
                                <circle cx="465" cy="565" r="9" fill="#2B2D31" stroke="#8E9297" stroke-width="1" />
                                <circle cx="635" cy="565" r="9" fill="#2B2D31" stroke="#8E9297" stroke-width="1" />
                            </g>

                            <!-- ================= 2. CORRIDOR LIGHTING RELAYS ================= -->
                            <path id="corridor_west_arc" d="M 330 260 A 250 250 0 0 0 280 730" fill="none" class="corridor-path-dark" />
                            <path id="corridor_east_arc" d="M 770 260 A 250 250 0 0 1 820 730" fill="none" class="corridor-path-lit" />
                            <line x1="330" y1="260" x2="770" y2="260" stroke="#4A4D52" stroke-width="1.5" stroke-dasharray="4 4" />

                            <!-- Corridor Luminaires (West) -->
                            <circle cx="315" cy="340" r="3" class="light-glow light-off" id="cw1" />
                            <circle cx="285" cy="450" r="3" class="light-glow light-off" id="cw2" />
                            <circle cx="275" cy="560" r="3" class="light-glow light-off" id="cw3" />
                            <circle cx="290" cy="670" r="3" class="light-glow light-off" id="cw4" />

                            <!-- Corridor Luminaires (East) -->
                            <circle cx="785" cy="340" r="3.5" class="light-glow light-on" id="ce1" />
                            <circle cx="815" cy="450" r="3.5" class="light-glow light-on" id="ce2" />
                            <circle cx="825" cy="560" r="3.5" class="light-glow light-on" id="ce3" />
                            <circle cx="810" cy="670" r="3.5" class="light-glow light-on" id="ce4" />

                            <!-- ================= 3. NORTH WING ================= -->
                            <!-- MAIN STAIRS -->
                            <g transform="translate(500, 70)">
                                <rect width="100" height="150" fill="#1E2025" stroke="#8E9297" stroke-width="1.5" rx="4" />
                                <rect width="100" height="150" fill="url(#stairTreads)" />
                                <line x1="50" y1="10" x2="50" y2="140" stroke="#8E9297" stroke-width="1" />
                                <text x="50" y="80" fill="#8E9297" font-family="'JetBrains Mono'" font-size="10" font-weight="bold" text-anchor="middle">
                                    MAIN STAIRS
                                </text>
                                <path d="M 50 120 L 50 40 L 45 48 M 50 40 L 55 48" stroke="#8E9297" stroke-width="1.5" fill="none" stroke-linecap="round" />
                            </g>

                            <!-- LAB B-1 (NORTH-WEST) -->
                            <g id="group_lab1">
                                <path d="M 240 80 L 480 80 L 480 230 L 240 250 Z" class="room-bg room-dark-bg" id="poly_lab1" />
                                <text x="350" y="115" fill="#D9DAD0" font-family="'JetBrains Mono'" font-size="12" font-weight="bold" text-anchor="middle">
                                    Lab B-1 (150 m2)
                                </text>
                                <text x="350" y="132" fill="#8E9297" font-family="'JetBrains Mono'" font-size="9" text-anchor="middle">
                                    Hardware + Embedded Systems
                                </text>
                                <rect x="270" y="150" width="85" height="16" class="cad-desk" />
                                <rect x="375" y="150" width="85" height="16" class="cad-desk" />
                                <rect x="270" y="185" width="85" height="16" class="cad-desk" />
                                <rect x="375" y="185" width="85" height="16" class="cad-desk" />
                                <circle cx="310" cy="115" r="4.5" class="light-glow light-off" />
                                <circle cx="410" cy="115" r="4.5" class="light-glow light-off" />
                                <circle cx="310" cy="215" r="4.5" class="light-glow light-off" />
                                <circle cx="410" cy="215" r="4.5" class="light-glow light-off" />
                            </g>

                            <!-- LAB B-2 (NORTH-EAST) -->
                            <g id="group_lab2">
                                <path d="M 620 80 L 860 80 L 860 250 L 620 230 Z" class="room-bg room-dark-bg" id="poly_lab2" />
                                <text x="750" y="115" fill="#D9DAD0" font-family="'JetBrains Mono'" font-size="12" font-weight="bold" text-anchor="middle">
                                    Lab B-2 (150 m2)
                                </text>
                                <text x="750" y="132" fill="#8E9297" font-family="'JetBrains Mono'" font-size="9" text-anchor="middle">
                                    RF + Communication Lab
                                </text>
                                <rect x="640" y="150" width="85" height="16" class="cad-desk" />
                                <rect x="745" y="150" width="85" height="16" class="cad-desk" />
                                <rect x="640" y="185" width="85" height="16" class="cad-desk" />
                                <rect x="745" y="185" width="85" height="16" class="cad-desk" />
                                <circle cx="680" cy="115" r="4.5" class="light-glow light-off" />
                                <circle cx="780" cy="115" r="4.5" class="light-glow light-off" />
                                <circle cx="680" cy="215" r="4.5" class="light-glow light-off" />
                                <circle cx="780" cy="215" r="4.5" class="light-glow light-off" />
                            </g>

                            <!-- ================= 4. WEST WING CLASSROOMS ================= -->
                            <!-- CR B-101 (WEST 1) -->
                            <g id="grp_r1">
                                <path d="M 40 230 L 220 250 L 210 360 L 30 340 Z" class="room-bg room-dark-bg" id="poly_r1" />
                                <text x="125" y="260" fill="#D9DAD0" font-family="'JetBrains Mono'" font-size="11" font-weight="bold">CR B-101 (96 m2)</text>

                                <line x1="185" y1="275" x2="185" y2="325" stroke="#8E9297" stroke-width="3" stroke-linecap="round" />
                                <rect x="175" y="295" width="8" height="10" fill="#36393F" stroke="#8E9297" stroke-width="1" />

                                <g transform="translate(60, 275)">
                                    <rect x="0" y="0" width="45" height="12" class="cad-desk" id="d1_r1" rx="2" />
                                    <rect x="55" y="0" width="45" height="12" class="cad-desk" id="d2_r1" rx="2" />
                                    <rect x="0" y="20" width="45" height="12" class="cad-desk" id="d3_r1" rx="2" />
                                    <rect x="55" y="20" width="45" height="12" class="cad-desk" id="d4_r1" rx="2" />
                                    <rect x="0" y="40" width="45" height="12" class="cad-desk" id="d5_r1" rx="2" />
                                    <rect x="55" y="40" width="45" height="12" class="cad-desk" id="d6_r1" rx="2" />

                                    <circle cx="12" cy="6" r="3.5" class="cad-student-dot" id="dot1_r1" opacity="0" />
                                    <circle cx="33" cy="6" r="3.5" class="cad-student-dot" id="dot2_r1" opacity="0" />
                                    <circle cx="67" cy="6" r="3.5" class="cad-student-dot" id="dot3_r1" opacity="0" />
                                    <circle cx="88" cy="6" r="3.5" class="cad-student-dot" id="dot4_r1" opacity="0" />
                                    <circle cx="12" cy="26" r="3.5" class="cad-student-dot" id="dot5_r1" opacity="0" />
                                    <circle cx="33" cy="26" r="3.5" class="cad-student-dot" id="dot6_r1" opacity="0" />
                                </g>

                                <circle cx="85" cy="255" r="5" class="light-glow light-off" id="l1_r1" />
                                <circle cx="165" cy="260" r="5" class="light-glow light-off" id="l2_r1" />
                                <circle cx="80" cy="330" r="5" class="light-glow light-off" id="l3_r1" />
                                <circle cx="160" cy="335" r="5" class="light-glow light-off" id="l4_r1" />

                                <text x="195" y="352" fill="#8E9297" font-family="'JetBrains Mono'" font-size="9" font-weight="bold" text-anchor="end" id="ac_r1">AC: OFF</text>
                            </g>

                            <!-- CR B-102 (WEST 2) -->
                            <g id="grp_r2">
                                <path d="M 30 355 L 210 375 L 200 485 L 20 465 Z" class="room-bg room-dark-bg" id="poly_r2" />
                                <text x="115" y="385" fill="#D9DAD0" font-family="'JetBrains Mono'" font-size="11" font-weight="bold">CR B-102 (84 m2)</text>

                                <line x1="175" y1="400" x2="175" y2="450" stroke="#8E9297" stroke-width="3" stroke-linecap="round" />
                                <rect x="165" y="420" width="8" height="10" fill="#36393F" stroke="#8E9297" stroke-width="1" />

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

                                <text x="185" y="477" fill="#8E9297" font-family="'JetBrains Mono'" font-size="9" font-weight="bold" text-anchor="end" id="ac_r2">AC: OFF</text>
                            </g>

                            <!-- CR B-103 (WEST 3) -->
                            <g id="grp_r3">
                                <path d="M 20 480 L 200 500 L 190 610 L 10 590 Z" class="room-bg room-dark-bg" id="poly_r3" />
                                <text x="105" y="510" fill="#D9DAD0" font-family="'JetBrains Mono'" font-size="11" font-weight="bold">CR B-103 (84 m2)</text>

                                <line x1="165" y1="525" x2="165" y2="575" stroke="#8E9297" stroke-width="3" stroke-linecap="round" />
                                <rect x="155" y="545" width="8" height="10" fill="#36393F" stroke="#8E9297" stroke-width="1" />

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

                                <text x="175" y="602" fill="#8E9297" font-family="'JetBrains Mono'" font-size="9" font-weight="bold" text-anchor="end" id="ac_r3">AC: OFF</text>
                            </g>

                            <!-- CR B-104 (WEST 4) -->
                            <g id="grp_r4">
                                <path d="M 10 605 L 190 625 L 180 735 L 0 715 Z" class="room-bg room-dark-bg" id="poly_r4" />
                                <text x="95" y="635" fill="#D9DAD0" font-family="'JetBrains Mono'" font-size="11" font-weight="bold">CR B-104 (96 m2)</text>

                                <line x1="155" y1="650" x2="155" y2="700" stroke="#8E9297" stroke-width="3" stroke-linecap="round" />
                                <rect x="145" y="670" width="8" height="10" fill="#36393F" stroke="#8E9297" stroke-width="1" />

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

                                <text x="165" y="727" fill="#8E9297" font-family="'JetBrains Mono'" font-size="9" font-weight="bold" text-anchor="end" id="ac_r4">AC: OFF</text>
                            </g>

                            <!-- ================= 5. EAST WING CLASSROOMS ================= -->
                            <!-- CR B-105 (EAST 1) -->
                            <g id="grp_r5">
                                <path d="M 880 250 L 1060 230 L 1070 340 L 890 360 Z" class="room-bg room-dark-bg" id="poly_r5" />
                                <text x="980" y="260" fill="#D9DAD0" font-family="'JetBrains Mono'" font-size="11" font-weight="bold" text-anchor="middle">CR B-105 (96 m2)</text>

                                <line x1="915" y1="275" x2="915" y2="325" stroke="#8E9297" stroke-width="3" stroke-linecap="round" />
                                <rect x="918" y="295" width="8" height="10" fill="#36393F" stroke="#8E9297" stroke-width="1" />

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

                                <text x="1055" y="352" fill="#8E9297" font-family="'JetBrains Mono'" font-size="9" font-weight="bold" text-anchor="end" id="ac_r5">AC: OFF</text>
                            </g>

                            <!-- CR B-106 (EAST 2) -->
                            <g id="grp_r6">
                                <path d="M 890 375 L 1070 355 L 1080 465 L 900 485 Z" class="room-bg room-dark-bg" id="poly_r6" />
                                <text x="990" y="385" fill="#D9DAD0" font-family="'JetBrains Mono'" font-size="11" font-weight="bold" text-anchor="middle">CR B-106 (84 m2)</text>

                                <line x1="925" y1="400" x2="925" y2="450" stroke="#8E9297" stroke-width="3" stroke-linecap="round" />
                                <rect x="928" y="420" width="8" height="10" fill="#36393F" stroke="#8E9297" stroke-width="1" />

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

                                <text x="1065" y="477" fill="#8E9297" font-family="'JetBrains Mono'" font-size="9" font-weight="bold" text-anchor="end" id="ac_r6">AC: OFF</text>
                            </g>

                            <!-- CR B-107 (EAST 3) -->
                            <g id="grp_r7">
                                <path d="M 900 500 L 1080 480 L 1090 590 L 910 610 Z" class="room-bg room-dark-bg" id="poly_r7" />
                                <text x="1000" y="510" fill="#D9DAD0" font-family="'JetBrains Mono'" font-size="11" font-weight="bold" text-anchor="middle">CR B-107 (84 m2)</text>

                                <line x1="935" y1="525" x2="935" y2="575" stroke="#8E9297" stroke-width="3" stroke-linecap="round" />
                                <rect x="938" y="545" width="8" height="10" fill="#36393F" stroke="#8E9297" stroke-width="1" />

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

                                <text x="1075" y="602" fill="#8E9297" font-family="'JetBrains Mono'" font-size="9" font-weight="bold" text-anchor="end" id="ac_r7">AC: OFF</text>
                            </g>

                            <!-- CR B-108 (EAST 4) -->
                            <g id="grp_r8">
                                <path d="M 910 625 L 1090 605 L 1100 715 L 920 735 Z" class="room-bg room-lit-bg" id="poly_r8" />
                                <text x="1010" y="635" fill="#FFC93C" font-family="'JetBrains Mono'" font-size="11" font-weight="bold" text-anchor="middle">CR B-108 (96 m2)</text>

                                <line x1="945" y1="650" x2="945" y2="700" stroke="#FFC93C" stroke-width="3" stroke-linecap="round" />
                                <rect x="948" y="670" width="8" height="10" fill="rgba(255,201,60,0.15)" stroke="#FFC93C" stroke-width="1" />

                                <g transform="translate(970, 650)">
                                    <rect x="0" y="0" width="45" height="12" class="cad-desk cad-desk-lit" id="d1_r8" rx="2" />
                                    <rect x="55" y="0" width="45" height="12" class="cad-desk cad-desk-lit" id="d2_r8" rx="2" />
                                    <rect x="0" y="20" width="45" height="12" class="cad-desk cad-desk-lit" id="d3_r8" rx="2" />
                                    <rect x="55" y="20" width="45" height="12" class="cad-desk cad-desk-lit" id="d4_r8" rx="2" />
                                    <rect x="0" y="40" width="45" height="12" class="cad-desk cad-desk-lit" id="d5_r8" rx="2" />
                                    <rect x="55" y="40" width="45" height="12" class="cad-desk cad-desk-lit" id="d6_r8" rx="2" />

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

                                <text x="1085" y="727" fill="#FFC93C" font-family="'JetBrains Mono'" font-size="9" font-weight="bold" text-anchor="end" id="ac_r8">AC: 26 C</text>
                            </g>

                            <!-- ================= 6. ELEVATOR BANKS + RESTROOMS ================= -->
                            <!-- WEST CORE -->
                            <g transform="translate(270, 410)">
                                <rect width="100" height="210" fill="#1E2025" stroke="#4A4D52" stroke-width="1.5" rx="4" />

                                <rect x="8" y="8" width="40" height="52" fill="rgba(255,201,60,0.08)" stroke="#FFC93C" stroke-width="1.5" rx="2" id="box_lift1" />
                                <line x1="28" y1="8" x2="28" y2="60" stroke="rgba(255,201,60,0.3)" stroke-width="1" />
                                <text x="28" y="38" fill="#FFC93C" font-family="'JetBrains Mono'" font-size="10" font-weight="bold" text-anchor="middle">L-1</text>

                                <rect x="52" y="8" width="40" height="52" fill="rgba(255,201,60,0.08)" stroke="#FFC93C" stroke-width="1.5" rx="2" id="box_lift2" />
                                <line x1="72" y1="8" x2="72" y2="60" stroke="rgba(255,201,60,0.3)" stroke-width="1" />
                                <text x="72" y="38" fill="#FFC93C" font-family="'JetBrains Mono'" font-size="10" font-weight="bold" text-anchor="middle">L-2</text>

                                <rect x="8" y="65" width="84" height="20" fill="#2B2D31" stroke="#FFC93C" rx="3" stroke-width="1" />
                                <text x="50" y="79" fill="#FFC93C" font-family="'JetBrains Mono'" font-size="8" font-weight="bold" text-anchor="middle" id="lift_west_label">ACTIVE STANDBY</text>

                                <rect x="8" y="95" width="84" height="50" fill="#2B2D31" stroke="#4A4D52" rx="2" />
                                <rect x="8" y="95" width="84" height="50" fill="url(#tilePattern)" opacity="0.2" />
                                <text x="50" y="125" fill="#8E9297" font-family="'JetBrains Mono'" font-size="9" font-weight="bold" text-anchor="middle">Toilet (M)</text>

                                <rect x="8" y="152" width="84" height="50" fill="#2B2D31" stroke="#4A4D52" rx="2" />
                                <rect x="8" y="152" width="84" height="50" fill="url(#tilePattern)" opacity="0.2" />
                                <text x="50" y="182" fill="#8E9297" font-family="'JetBrains Mono'" font-size="9" font-weight="bold" text-anchor="middle">Toilet (F)</text>
                            </g>

                            <!-- EAST CORE -->
                            <g transform="translate(730, 410)">
                                <rect width="100" height="210" fill="#1E2025" stroke="#4A4D52" stroke-width="1.5" rx="4" />

                                <rect x="8" y="8" width="40" height="52" fill="#2B2D31" stroke="#4A4D52" stroke-width="1" stroke-dasharray="3 3" rx="2" id="box_lift3" />
                                <line x1="28" y1="8" x2="28" y2="60" stroke="#4A4D52" stroke-width="1" />
                                <text x="28" y="38" fill="#8E9297" font-family="'JetBrains Mono'" font-size="10" font-weight="bold" text-anchor="middle">L-3</text>

                                <rect x="52" y="8" width="40" height="52" fill="#2B2D31" stroke="#4A4D52" stroke-width="1" stroke-dasharray="3 3" rx="2" id="box_lift4" />
                                <line x1="72" y1="8" x2="72" y2="60" stroke="#4A4D52" stroke-width="1" />
                                <text x="72" y="38" fill="#8E9297" font-family="'JetBrains Mono'" font-size="10" font-weight="bold" text-anchor="middle">L-4</text>

                                <rect x="8" y="65" width="84" height="20" fill="#2B2D31" stroke="#4A4D52" rx="3" stroke-width="1" />
                                <text x="50" y="79" fill="#8E9297" font-family="'JetBrains Mono'" font-size="8" font-weight="bold" text-anchor="middle" id="lift_east_label">DEEP SLEEP (0 W)</text>

                                <rect x="8" y="95" width="84" height="50" fill="#2B2D31" stroke="#4A4D52" rx="2" />
                                <rect x="8" y="95" width="84" height="50" fill="url(#tilePattern)" opacity="0.2" />
                                <text x="50" y="125" fill="#8E9297" font-family="'JetBrains Mono'" font-size="9" font-weight="bold" text-anchor="middle">Toilet (M)</text>

                                <rect x="8" y="152" width="84" height="50" fill="#2B2D31" stroke="#4A4D52" rx="2" />
                                <rect x="8" y="152" width="84" height="50" fill="url(#tilePattern)" opacity="0.2" />
                                <text x="50" y="182" fill="#8E9297" font-family="'JetBrains Mono'" font-size="9" font-weight="bold" text-anchor="middle">Toilet (F)</text>
                            </g>

                            <!-- ================= 7. SOUTH WING ================= -->
                            <!-- STAIRS SW -->
                            <g transform="translate(60, 760)">
                                <rect width="110" height="95" fill="#1E2025" stroke="#8E9297" stroke-width="1.5" rx="4" />
                                <rect width="110" height="95" fill="url(#stairTreads)" />
                                <line x1="55" y1="10" x2="55" y2="85" stroke="#8E9297" stroke-width="1" />
                                <text x="55" y="52" fill="#8E9297" font-family="'JetBrains Mono'" font-size="9.5" font-weight="bold" text-anchor="middle">
                                    STAIRS SW
                                </text>
                                <path d="M 55 20 L 55 75 L 50 67 M 55 75 L 60 67" stroke="#8E9297" stroke-width="1.5" fill="none" />
                            </g>

                            <!-- FACULTY LOUNGE -->
                            <g transform="translate(190, 760)">
                                <rect width="160" height="100" fill="#1E2025" stroke="#4A4D52" stroke-width="1.5" rx="4" />
                                <text x="80" y="40" fill="#D9DAD0" font-family="'JetBrains Mono'" font-size="11" font-weight="bold" text-anchor="middle">Faculty Lounge</text>
                                <text x="80" y="58" fill="#8E9297" font-family="'JetBrains Mono'" font-size="9" text-anchor="middle">(80 m2)</text>

                                <rect x="35" y="70" width="90" height="20" rx="4" class="cad-desk" />
                                <circle cx="50" cy="65" r="4" class="cad-chair" />
                                <circle cx="80" cy="65" r="4" class="cad-chair" />
                                <circle cx="110" cy="65" r="4" class="cad-chair" />
                                <circle cx="50" cy="95" r="4" class="cad-chair" />
                                <circle cx="80" cy="95" r="4" class="cad-chair" />
                                <circle cx="110" cy="95" r="4" class="cad-chair" />
                            </g>

                            <!-- SEMINAR HALL -->
                            <g transform="translate(370, 750)">
                                <rect width="360" height="120" fill="#1E2025" stroke="#4A4D52" stroke-width="1.5" rx="4" />
                                <text x="180" y="32" fill="#FFFFFF" font-family="'JetBrains Mono'" font-size="13" font-weight="bold" text-anchor="middle">
                                    Seminar Hall (180 m2)
                                </text>
                                <text x="180" y="48" fill="#8E9297" font-family="'JetBrains Mono'" font-size="9" text-anchor="middle">
                                    120-Seat Auditorium // Standby Cutoff Active
                                </text>

                                <rect x="130" y="60" width="100" height="16" fill="#36393F" stroke="#8E9297" rx="2" />
                                <rect x="172" y="62" width="16" height="12" fill="#8E9297" rx="2" />

                                <path d="M 50 90 Q 180 115 310 90" fill="none" stroke="#4A4D52" stroke-width="4" stroke-linecap="round" />
                                <path d="M 60 105 Q 180 130 300 105" fill="none" stroke="#4A4D52" stroke-width="4" stroke-linecap="round" />
                                <path d="M 70 120 Q 180 145 290 120" fill="none" stroke="#4A4D52" stroke-width="4" stroke-linecap="round" />
                            </g>

                            <!-- COMPUTER LAB B-3 -->
                            <g transform="translate(750, 760)">
                                <rect width="170" height="100" fill="#1E2025" stroke="#4A4D52" stroke-width="1.5" rx="4" />
                                <text x="85" y="38" fill="#D9DAD0" font-family="'JetBrains Mono'" font-size="11" font-weight="bold" text-anchor="middle">Computer Lab B-3</text>
                                <text x="85" y="54" fill="#8E9297" font-family="'JetBrains Mono'" font-size="9" text-anchor="middle">(150 m2)</text>

                                <g transform="translate(25, 68)">
                                    <rect x="0" y="0" width="55" height="10" class="cad-desk" />
                                    <rect x="65" y="0" width="55" height="10" class="cad-desk" />
                                    <rect x="0" y="16" width="55" height="10" class="cad-desk" />
                                    <rect x="65" y="16" width="55" height="10" class="cad-desk" />
                                </g>
                            </g>

                            <!-- STAIRS SE -->
                            <g transform="translate(940, 760)">
                                <rect width="110" height="95" fill="#1E2025" stroke="#8E9297" stroke-width="1.5" rx="4" />
                                <rect width="110" height="95" fill="url(#stairTreads)" />
                                <line x1="55" y1="10" x2="55" y2="85" stroke="#8E9297" stroke-width="1" />
                                <text x="55" y="52" fill="#8E9297" font-family="'JetBrains Mono'" font-size="9.5" font-weight="bold" text-anchor="middle">
                                    STAIRS SE
                                </text>
                                <path d="M 55 20 L 55 75 L 50 67 M 55 75 L 60 67" stroke="#8E9297" stroke-width="1.5" fill="none" />
                            </g>

                            <!-- ================= 8. STRUCTURAL COLUMNS ================= -->
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
    </div>

    <style>
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.3; }
        }
    </style>

    <!-- JAVASCRIPT -->
    <script>
        let currentRelocation = null;
        let currentMode = 'variable';
        let activeTTSlot = null;

        // ============================================================
        // TIMETABLE DATA
        // ============================================================
        const TIMETABLE = [
            {
                label: '08:00 - 09:00',
                hour: 8,
                temp: 27,
                weather: 'Sunny / Daylight',
                tag: 'Morning Session 1',
                rooms: { B101: 48, B102: 42, B103: 0, B104: 0, B105: 45, B106: 0, B107: 0, B108: 0 }
            },
            {
                label: '09:00 - 10:00',
                hour: 9,
                temp: 27,
                weather: 'Sunny / Daylight',
                tag: 'Morning Session 2',
                rooms: { B101: 50, B102: 0, B103: 38, B104: 0, B105: 0, B106: 44, B107: 40, B108: 0 }
            },
            {
                label: '10:00 - 11:00',
                hour: 10,
                temp: 30,
                weather: 'Sunny / Daylight',
                tag: 'Mid-Morning',
                rooms: { B101: 0, B102: 46, B103: 0, B104: 35, B105: 50, B106: 0, B107: 0, B108: 42 }
            },
            {
                label: '11:00 - 12:00',
                hour: 11,
                temp: 32,
                weather: 'Sunny / Daylight',
                tag: 'Late Morning',
                rooms: { B101: 45, B102: 0, B103: 40, B104: 0, B105: 0, B106: 38, B107: 0, B108: 0 }
            },
            {
                label: '12:00 - 13:00',
                hour: 12,
                temp: 34,
                weather: 'Sunny / Daylight',
                tag: 'LUNCH BREAK',
                rooms: { B101: 0, B102: 0, B103: 0, B104: 0, B105: 0, B106: 0, B107: 0, B108: 0 }
            },
            {
                label: '13:00 - 14:00',
                hour: 13,
                temp: 34,
                weather: 'Sunny / Daylight',
                tag: 'Afternoon Session 1',
                rooms: { B101: 0, B102: 42, B103: 0, B104: 0, B105: 48, B106: 0, B107: 36, B108: 0 }
            },
            {
                label: '14:00 - 15:00',
                hour: 14,
                temp: 32,
                weather: 'Sunny / Daylight',
                tag: 'Afternoon Session 2',
                rooms: { B101: 44, B102: 0, B103: 0, B104: 38, B105: 0, B106: 42, B107: 0, B108: 40 }
            },
            {
                label: '15:00 - 16:00',
                hour: 15,
                temp: 32,
                weather: 'Sunny / Daylight',
                tag: 'Winding Down',
                rooms: { B101: 0, B102: 0, B103: 35, B104: 0, B105: 40, B106: 0, B107: 0, B108: 0 }
            },
            {
                label: '16:00 - 17:00',
                hour: 16,
                temp: 30,
                weather: 'Overcast / Rainy',
                tag: 'Late Afternoon',
                rooms: { B101: 0, B102: 0, B103: 0, B104: 0, B105: 0, B106: 0, B107: 0, B108: 25 }
            },
            {
                label: '17:00 - 18:00',
                hour: 17,
                temp: 28,
                weather: 'Night',
                tag: 'After Hours',
                rooms: { B101: 0, B102: 0, B103: 0, B104: 0, B105: 0, B106: 0, B107: 0, B108: 0 }
            },
            {
                label: '18:00 - 19:00',
                hour: 18,
                temp: 28,
                weather: 'Night',
                tag: 'After Hours',
                rooms: { B101: 0, B102: 0, B103: 0, B104: 0, B105: 0, B106: 0, B107: 0, B108: 0 }
            },
            {
                label: '19:00 - 20:00',
                hour: 19,
                temp: 28,
                weather: 'Night',
                tag: 'Evening Study Group',
                rooms: { B101: 0, B102: 0, B103: 0, B104: 0, B105: 0, B106: 0, B107: 0, B108: 20 }
            }
        ];

        // ============================================================
        // MODE SWITCHING
        // ============================================================
        function switchMode(mode) {
            currentMode = mode;
            const tabVar = document.getElementById('tabVariable');
            const tabTT = document.getElementById('tabTimetable');
            const panelVar = document.getElementById('panelVariable');
            const panelTT = document.getElementById('panelTimetable');

            if (mode === 'variable') {
                tabVar.classList.add('active');
                tabTT.classList.remove('active');
                panelVar.style.display = 'block';
                panelTT.style.display = 'none';
            } else {
                tabVar.classList.remove('active');
                tabTT.classList.add('active');
                panelVar.style.display = 'none';
                panelTT.style.display = 'block';
            }
        }

        // ============================================================
        // BUILD TIMETABLE SLOTS
        // ============================================================
        function buildTimetableSlots() {
            const container = document.getElementById('timetableSlots');
            container.innerHTML = '';

            TIMETABLE.forEach(function(slot, idx) {
                const el = document.createElement('div');
                el.className = 'tt-slot';
                el.setAttribute('data-idx', idx);
                el.onclick = function() { applyTimetableSlot(idx); };

                const activeRooms = [];
                const roomKeys = ['B101','B102','B103','B104','B105','B106','B107','B108'];
                roomKeys.forEach(function(rk) {
                    if (slot.rooms[rk] > 0) {
                        activeRooms.push(rk + '=' + slot.rooms[rk]);
                    }
                });

                const isLunch = slot.tag === 'LUNCH BREAK';
                const isEmpty = activeRooms.length === 0 && !isLunch;

                let roomsStr = '';
                if (isLunch) {
                    roomsStr = '<span style="color:#FFC93C;">All rooms empty (break)</span>';
                } else if (isEmpty) {
                    roomsStr = '<span style="color:#8E9297;">All rooms empty</span>';
                } else {
                    roomsStr = '<span style="color:#D9DAD0;">' + activeRooms.join(', ') + '</span>';
                }

                el.innerHTML =
                    '<div class="flex justify-between items-center mb-1">' +
                        '<span class="font-mono font-bold" style="color:#FFFFFF; font-size:12px;">' + slot.label + '</span>' +
                        '<span class="font-mono" style="color:' + (isLunch ? '#FFC93C' : '#8E9297') + '; font-size:10px;">' + slot.tag + '</span>' +
                    '</div>' +
                    '<div class="font-mono" style="font-size:10px; line-height:1.5;">' + roomsStr + '</div>';

                container.appendChild(el);
            });
        }

        // ============================================================
        // APPLY TIMETABLE SLOT
        // ============================================================
        function applyTimetableSlot(idx) {
            const slot = TIMETABLE[idx];
            activeTTSlot = idx;

            // Highlight active slot
            const allSlots = document.querySelectorAll('.tt-slot');
            allSlots.forEach(function(s) { s.classList.remove('active'); });
            allSlots[idx].classList.add('active');

            // Set time slider
            document.getElementById('timeSlider').value = slot.hour;

            // Set temperature
            document.getElementById('tempSlider').value = slot.temp;

            // Set weather
            document.getElementById('weatherSelect').value = slot.weather;

            // Set all 8 room occupancy sliders
            const roomKeys = ['B101','B102','B103','B104','B105','B106','B107','B108'];
            roomKeys.forEach(function(rk, i) {
                document.getElementById('occ_r' + (i + 1)).value = slot.rooms[rk];
            });

            onParamChange();
        }

        // ============================================================
        // INIT
        // ============================================================
        window.addEventListener('DOMContentLoaded', function() {
            const savedToken = localStorage.getItem('gridsense_tg_token') || '';
            const savedChat = localStorage.getItem('gridsense_tg_chat') || '';
            if (savedToken) document.getElementById('tgToken').value = savedToken;
            if (savedChat) document.getElementById('tgChatId').value = savedChat;

            buildTimetableSlots();
            onParamChange(false);
        });

        // ============================================================
        // PARAM CHANGE
        // ============================================================
        function onParamChange(triggerPing) {
            if (triggerPing === undefined) triggerPing = false;

            const timeVal = parseFloat(document.getElementById('timeSlider').value);
            const hours = Math.floor(timeVal);
            const mins = (timeVal % 1 === 0.5) ? '30' : '00';
            const timeStr = (hours < 10 ? '0' + hours : hours) + ':' + mins;
            document.getElementById('timeVal').innerText = timeStr;

            const temp = document.getElementById('tempSlider').value;
            document.getElementById('tempVal').innerText = temp + ' C';

            const weather = document.getElementById('weatherSelect').value;

            const roomsPayload = {};
            for (let i = 1; i <= 8; i++) {
                const occ = parseInt(document.getElementById('occ_r' + i).value);
                document.getElementById('val_r' + i).innerText = occ;
                roomsPayload['B10' + i] = occ;
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
            .then(function(res) { return res.json(); })
            .then(function(data) {
                renderVectorState(data);
                if (triggerPing) triggerAutoTelegramPing(data);
            })
            .catch(function(err) { console.error(err); });
        }

        // ============================================================
        // RENDER VECTOR STATE
        // ============================================================
        function renderVectorState(data) {
            document.getElementById('baselineMeter').innerText = data.total_baseline_kw + ' kW';
            document.getElementById('optimizedMeter').innerText = data.total_optimized_kw + ' kW';
            document.getElementById('savingsMeter').innerText = data.kw_saved + ' kW (' + data.savings_percentage + '%)';
            document.getElementById('inrMeter').innerText = 'INR ' + data.inr_per_hour_saved + ' / Hour Saved';
            document.getElementById('elevState').innerText = data.elevator_mode;

            var rooms = data.rooms;
            for (let i = 1; i <= 8; i++) {
                const r_id = 'B10' + i;
                const r = rooms[r_id];
                if (!r) continue;

                const poly = document.getElementById('poly_r' + i);
                const ac = document.getElementById('ac_r' + i);
                const occCount = parseInt(document.getElementById('occ_r' + i).value);

                if (r.lighting_glow) {
                    if (poly) poly.setAttribute('class', 'room-bg room-lit-bg');
                    for (let l = 1; l <= 4; l++) {
                        const light = document.getElementById('l' + l + '_r' + i);
                        if (light) light.setAttribute('class', 'light-glow light-on');
                    }
                    for (let d = 1; d <= 6; d++) {
                        const desk = document.getElementById('d' + d + '_r' + i);
                        if (desk) desk.setAttribute('class', 'cad-desk cad-desk-lit');
                    }
                    for (let dt = 1; dt <= 6; dt++) {
                        const dot = document.getElementById('dot' + dt + '_r' + i);
                        if (dot) dot.setAttribute('opacity', (occCount > (dt - 1) * 7) ? '1' : '0');
                    }
                    if (ac) {
                        ac.textContent = 'AC: ' + r.ac_setpoint;
                        ac.setAttribute('fill', '#FFC93C');
                    }
                } else {
                    if (poly) poly.setAttribute('class', 'room-bg room-dark-bg');
                    for (let l = 1; l <= 4; l++) {
                        const light = document.getElementById('l' + l + '_r' + i);
                        if (light) light.setAttribute('class', 'light-glow light-off');
                    }
                    for (let d = 1; d <= 6; d++) {
                        const desk = document.getElementById('d' + d + '_r' + i);
                        if (desk) desk.setAttribute('class', 'cad-desk');
                    }
                    for (let dt = 1; dt <= 6; dt++) {
                        const dot = document.getElementById('dot' + dt + '_r' + i);
                        if (dot) dot.setAttribute('opacity', '0');
                    }
                    if (ac) {
                        ac.textContent = 'AC: OFF';
                        ac.setAttribute('fill', '#8E9297');
                    }
                }
            }

            // Corridors
            const westLit = (rooms['B101'] && rooms['B101'].lighting_glow) || (rooms['B102'] && rooms['B102'].lighting_glow) || (rooms['B103'] && rooms['B103'].lighting_glow) || (rooms['B104'] && rooms['B104'].lighting_glow);
            const eastLit = (rooms['B105'] && rooms['B105'].lighting_glow) || (rooms['B106'] && rooms['B106'].lighting_glow) || (rooms['B107'] && rooms['B107'].lighting_glow) || (rooms['B108'] && rooms['B108'].lighting_glow);

            const westArc = document.getElementById('corridor_west_arc');
            const eastArc = document.getElementById('corridor_east_arc');

            if (westArc) westArc.setAttribute('class', westLit ? 'corridor-path-lit' : 'corridor-path-dark');
            if (eastArc) eastArc.setAttribute('class', eastLit ? 'corridor-path-lit' : 'corridor-path-dark');

            for (let i = 1; i <= 4; i++) {
                const cw = document.getElementById('cw' + i);
                const ce = document.getElementById('ce' + i);
                if (cw) cw.setAttribute('class', westLit ? 'light-glow light-on' : 'light-glow light-off');
                if (ce) ce.setAttribute('class', eastLit ? 'light-glow light-on' : 'light-glow light-off');
            }

            // Lifts
            const b1 = document.getElementById('box_lift1');
            const b2 = document.getElementById('box_lift2');
            const b3 = document.getElementById('box_lift3');
            const b4 = document.getElementById('box_lift4');
            const wl = document.getElementById('lift_west_label');
            const el = document.getElementById('lift_east_label');

            if (data.total_optimized_kw > 15) {
                if (b1) b1.setAttribute('fill', 'rgba(255,201,60,0.08)');
                if (b2) b2.setAttribute('fill', 'rgba(255,201,60,0.08)');
                if (b3) b3.setAttribute('fill', 'rgba(255,201,60,0.08)');
                if (b4) b4.setAttribute('fill', 'rgba(255,201,60,0.08)');
                if (wl) wl.innerText = 'ACTIVE STANDBY';
                if (el) el.innerText = 'ACTIVE STANDBY';
            } else {
                if (b3) b3.setAttribute('fill', '#2B2D31');
                if (b4) b4.setAttribute('fill', '#2B2D31');
                if (el) el.innerText = 'DEEP SLEEP (0 W)';
            }

            // Relocation nudge
            const relocs = data.relocations || [];
            const alertCard = document.getElementById('alertCard');
            const alertText = document.getElementById('alertText');

            if (relocs.length > 0) {
                currentRelocation = relocs[0];
                alertCard.style.display = 'flex';
                alertText.innerText = currentRelocation.reason;
            } else {
                currentRelocation = null;
                alertCard.style.display = 'none';
            }
        }

        // ============================================================
        // CONSOLIDATION
        // ============================================================
        function applyConsolidation() {
            if (currentRelocation) {
                const fromId = currentRelocation.from_room;
                const toId = currentRelocation.to_room;
                const fromIdx = parseInt(fromId.slice(-1));
                const toIdx = parseInt(toId.slice(-1));

                const students = parseInt(document.getElementById('occ_r' + fromIdx).value);
                document.getElementById('occ_r' + fromIdx).value = 0;
                document.getElementById('occ_r' + toIdx).value = students;
                onParamChange(true);
            }
        }

        // ============================================================
        // PRESETS
        // ============================================================
        function applyPreset(type) {
            if (type === 'morning') {
                document.getElementById('timeSlider').value = 9.0;
                document.getElementById('tempSlider').value = 27;
                document.getElementById('weatherSelect').value = 'Sunny / Daylight';
                for (let i = 1; i <= 8; i++) document.getElementById('occ_r' + i).value = (i <= 6) ? 45 : 0;
            } else if (type === 'afternoon') {
                document.getElementById('timeSlider').value = 14.5;
                document.getElementById('tempSlider').value = 35;
                document.getElementById('weatherSelect').value = 'Sunny / Daylight';
                for (let i = 1; i <= 8; i++) document.getElementById('occ_r' + i).value = 40;
            } else if (type === 'night_waste') {
                document.getElementById('timeSlider').value = 19.5;
                document.getElementById('tempSlider').value = 32;
                document.getElementById('weatherSelect').value = 'Night';
                for (let i = 1; i <= 7; i++) document.getElementById('occ_r' + i).value = 0;
                document.getElementById('occ_r8').value = 25;
            } else if (type === 'lockdown') {
                document.getElementById('timeSlider').value = 22.0;
                document.getElementById('tempSlider').value = 25;
                document.getElementById('weatherSelect').value = 'Night';
                for (let i = 1; i <= 8; i++) document.getElementById('occ_r' + i).value = 0;
            }
            onParamChange(false);
        }

        function clearAllOccupants() {
            for (let i = 1; i <= 8; i++) document.getElementById('occ_r' + i).value = 0;
            onParamChange(false);
        }

        // ============================================================
        // TELEGRAM
        // ============================================================
        function saveAndTestTelegram() {
            const token = document.getElementById('tgToken').value.trim();
            const chatId = document.getElementById('tgChatId').value.trim();

            if (!token || !chatId) {
                alert('Please enter both Bot Token and Chat ID to connect your phone.');
                return;
            }

            localStorage.setItem('gridsense_tg_token', token);
            localStorage.setItem('gridsense_tg_chat', chatId);

            const st = document.getElementById('tgStatus');
            st.innerText = 'Dispatching test handshake ping...';

            fetch('/api/sandbox/notify-telegram', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    token: token,
                    chat_id: chatId,
                    message: 'GridSense Connected: JIT Block B Digital Twin linked to your mobile. Automatic optimization nudges active.'
                })
            })
            .then(function(res) { return res.json(); })
            .then(function(data) {
                if (data.status === 'success') {
                    st.innerText = 'Verified! Connected to your mobile phone.';
                    st.style.color = '#57F287';
                } else {
                    st.innerText = 'Telegram Error: ' + data.message;
                    st.style.color = '#ED4245';
                }
            })
            .catch(function(err) {
                st.innerText = 'Network Error: ' + err;
                st.style.color = '#ED4245';
            });
        }

        function triggerAutoTelegramPing(data) {
            const token = localStorage.getItem('gridsense_tg_token');
            const chatId = localStorage.getItem('gridsense_tg_chat');
            if (!token || !chatId) return;

            var msg = 'GridSense Alert [JIT Block B]: Relocation executed. Total power cut to ' + data.total_optimized_kw + ' kW. Immediate savings: ' + data.kw_saved + ' kW (' + data.savings_percentage + '%). Hourly financial savings: INR ' + data.inr_per_hour_saved + '/hr.';

            fetch('/api/sandbox/notify-telegram', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    token: token,
                    chat_id: chatId,
                    message: msg
                })
            }).catch(function(e) { console.log('Telegram ping error:', e); });
        }
    </script>
</body>
</html>"""
