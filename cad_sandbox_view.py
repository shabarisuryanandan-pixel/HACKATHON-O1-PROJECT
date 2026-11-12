"""
CAD Architectural Floor Plan View for Block B (8 Classrooms per floor)
Renders real-life desks, lighting luminaires, 4-lift elevator bank,
fire staircase, and 3-zone arterial corridor in Neumorphic style.
"""

def render_cad_sandbox_html():
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GridSense // Architectural CAD Blueprint & Testing Sandbox</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background-color: #121418;
            color: #d1d5db;
        }
        .font-mono-code { font-family: 'JetBrains Mono', monospace; }

        .neu-card {
            background: #17191f;
            border-radius: 16px;
            box-shadow: 8px 8px 18px #0c0d10, -8px -8px 18px #22252e;
            border: 1px solid rgba(255, 255, 255, 0.03);
        }
        .neu-inset {
            background: #111216;
            border-radius: 12px;
            box-shadow: inset 4px 4px 10px #08090b, inset -4px -4px 10px #1a1c22;
            border: 1px solid rgba(255, 255, 255, 0.02);
        }
        .neu-btn {
            background: #17191f;
            border-radius: 10px;
            box-shadow: 4px 4px 10px #0c0d10, -4px -4px 10px #22252e;
            border: 1px solid rgba(255, 255, 255, 0.04);
            transition: all 0.15s ease;
        }
        .neu-btn:hover { color: #10b981; }
        .neu-btn:active {
            box-shadow: inset 3px 3px 6px #08090b, inset -3px -3px 6px #1a1c22;
        }

        /* CAD Architectural Styling */
        .cad-room {
            background: #14161c;
            border: 1.5px solid #232733;
            border-radius: 8px;
            position: relative;
            transition: all 0.3s ease;
        }
        .cad-room-lit {
            background: radial-gradient(circle at center, rgba(251, 191, 36, 0.15) 0%, rgba(20, 22, 28, 0.95) 85%);
            border: 1.5px solid rgba(251, 191, 36, 0.45) !important;
            box-shadow: 0 0 16px rgba(251, 191, 36, 0.12), inset 0 0 14px rgba(251, 191, 36, 0.05);
        }
        .cad-room-dark {
            background: #0f1014;
            border: 1px solid #1a1c24 !important;
            opacity: 0.6;
        }

        .cad-desk {
            background: #1d212b;
            border: 1px solid #2d3342;
            border-radius: 2px;
        }
        .cad-desk-lit {
            background: #2b261a;
            border: 1px solid rgba(251, 191, 36, 0.4);
        }
        .cad-light {
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: #333a4a;
        }
        .cad-light-lit {
            background: #fbbf24;
            box-shadow: 0 0 8px #fbbf24, 0 0 14px rgba(251, 191, 36, 0.6);
        }

        .corridor-lit {
            background: rgba(251, 191, 36, 0.08);
            border: 1px solid rgba(251, 191, 36, 0.25);
        }
        .corridor-dark {
            background: #0b0c0f;
            border: 1px dashed rgba(255, 255, 255, 0.05);
            opacity: 0.4;
        }
    </style>
</head>
<body class="min-h-screen p-4 sm:p-8 max-w-7xl mx-auto">

    <!-- HEADER NAVIGATION -->
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6 pb-4 border-b border-white/5">
        <div>
            <div class="text-xs font-mono-code font-bold text-emerald-400 uppercase tracking-widest">Architectural CAD Blueprint // Digital Twin</div>
            <h1 class="text-2xl sm:text-3xl font-bold text-white tracking-tight mt-1">Block B: 8-Classroom Floor Plan</h1>
            <p class="text-xs text-zinc-400 font-mono-code mt-0.5">Real-life architectural layout with physical desks, luminaires, 4-lift bank, and zoned hallway relays</p>
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
        <div class="lg:col-span-4 space-y-5">

            <!-- FLOOR SELECTOR -->
            <div class="p-4 neu-card">
                <div class="text-xs font-mono-code uppercase text-zinc-400 mb-2 font-bold">Floor Level</div>
                <div class="grid grid-cols-2 gap-3">
                    <button id="btnFloor1" onclick="switchFloor(1)" class="py-2.5 neu-btn text-xs font-mono-code font-bold text-emerald-400 text-center">
                        Floor 1 (B101 - B108)
                    </button>
                    <button id="btnFloor2" onclick="switchFloor(2)" class="py-2.5 neu-btn text-xs font-mono-code font-bold text-zinc-400 text-center">
                        Floor 2 (B201 - B208)
                    </button>
                </div>
            </div>

            <!-- PRESET QUICK SELECTOR -->
            <div class="p-4 neu-card">
                <div class="text-xs font-mono-code uppercase text-zinc-400 mb-2 font-bold">Scenario Presets</div>
                <div class="grid grid-cols-3 gap-2">
                    <button onclick="applyPreset('morning')" class="py-2 px-1 neu-btn text-[11px] font-mono-code font-bold text-zinc-300 text-center">
                        09:00 AM<br><span class="text-[9px] text-zinc-500 font-normal">Full Rush</span>
                    </button>
                    <button onclick="applyPreset('afternoon')" class="py-2 px-1 neu-btn text-[11px] font-mono-code font-bold text-zinc-300 text-center">
                        02:30 PM<br><span class="text-[9px] text-zinc-500 font-normal">Peak Heat</span>
                    </button>
                    <button onclick="applyPreset('night_waste')" class="py-2 px-1 neu-btn text-[11px] font-mono-code font-bold text-amber-400 text-center">
                        07:30 PM<br><span class="text-[9px] text-zinc-500 font-normal">Far Hallway</span>
                    </button>
                </div>
            </div>

            <!-- TIME & ENVIRONMENT SLIDERS -->
            <div class="p-4 neu-card space-y-3">
                <div class="text-xs font-mono-code uppercase text-zinc-400 font-bold">Environmental Controls</div>
                
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
                    <div class="text-xs font-mono-code text-zinc-400 mb-1">Sky Condition</div>
                    <select id="weatherSelect" onchange="onParamChange()" class="w-full p-2 neu-inset text-xs font-mono-code text-zinc-200 outline-none">
                        <option value="Sunny / Daylight">Sunny / Daylight (High Lux)</option>
                        <option value="Overcast / Rainy">Overcast / Rainy (Low Lux)</option>
                        <option value="Night" selected>Night (Zero Daylight)</option>
                    </select>
                </div>
            </div>

            <!-- 8-ROOM OCCUPANCY INPUTS -->
            <div class="p-4 neu-card space-y-2">
                <div class="text-xs font-mono-code uppercase text-zinc-400 font-bold mb-1">Headcount per Room (Max 60)</div>
                <div class="grid grid-cols-2 gap-2 text-[11px] font-mono-code text-zinc-400">
                    <div>
                        <div class="flex justify-between">
                            <span id="lbl_r1">B101 (Entrance):</span>
                            <span id="val_r1" class="text-white font-bold">0</span>
                        </div>
                        <input type="range" id="occ_r1" min="0" max="60" value="0" oninput="onParamChange()" class="w-full accent-blue-500 cursor-pointer">
                    </div>
                    <div>
                        <div class="flex justify-between">
                            <span id="lbl_r5">B105 (Entrance):</span>
                            <span id="val_r5" class="text-white font-bold">0</span>
                        </div>
                        <input type="range" id="occ_r5" min="0" max="60" value="0" oninput="onParamChange()" class="w-full accent-blue-500 cursor-pointer">
                    </div>
                    <div>
                        <div class="flex justify-between">
                            <span id="lbl_r2">B102 (Mid):</span>
                            <span id="val_r2" class="text-white font-bold">0</span>
                        </div>
                        <input type="range" id="occ_r2" min="0" max="60" value="0" oninput="onParamChange()" class="w-full accent-blue-500 cursor-pointer">
                    </div>
                    <div>
                        <div class="flex justify-between">
                            <span id="lbl_r6">B106 (Mid):</span>
                            <span id="val_r6" class="text-white font-bold">0</span>
                        </div>
                        <input type="range" id="occ_r6" min="0" max="60" value="0" oninput="onParamChange()" class="w-full accent-blue-500 cursor-pointer">
                    </div>
                    <div>
                        <div class="flex justify-between">
                            <span id="lbl_r3">B103 (Mid-Far):</span>
                            <span id="val_r3" class="text-white font-bold">0</span>
                        </div>
                        <input type="range" id="occ_r3" min="0" max="60" value="0" oninput="onParamChange()" class="w-full accent-blue-500 cursor-pointer">
                    </div>
                    <div>
                        <div class="flex justify-between">
                            <span id="lbl_r7">B107 (Mid-Far):</span>
                            <span id="val_r7" class="text-white font-bold">0</span>
                        </div>
                        <input type="range" id="occ_r7" min="0" max="60" value="0" oninput="onParamChange()" class="w-full accent-blue-500 cursor-pointer">
                    </div>
                    <div>
                        <div class="flex justify-between">
                            <span id="lbl_r4">B104 (Far End):</span>
                            <span id="val_r4" class="text-white font-bold">0</span>
                        </div>
                        <input type="range" id="occ_r4" min="0" max="60" value="0" oninput="onParamChange()" class="w-full accent-blue-500 cursor-pointer">
                    </div>
                    <div>
                        <div class="flex justify-between">
                            <span id="lbl_r8">B108 (Far End):</span>
                            <span id="val_r8" class="text-amber-400 font-bold">25</span>
                        </div>
                        <input type="range" id="occ_r8" min="0" max="60" value="25" oninput="onParamChange()" class="w-full accent-amber-500 cursor-pointer">
                    </div>
                </div>
            </div>

            <!-- TELEGRAM BOT ALERT CONFIG -->
            <div class="p-4 neu-card space-y-2.5">
                <div class="text-xs font-mono-code uppercase text-zinc-400 font-bold">Telegram Mobile Alerts</div>
                <input type="text" id="tgToken" placeholder="Bot Token from @BotFather" class="w-full p-2 neu-inset text-[11px] font-mono-code text-zinc-200 outline-none">
                <input type="text" id="tgChatId" placeholder="Chat ID from @userinfobot" class="w-full p-2 neu-inset text-[11px] font-mono-code text-zinc-200 outline-none">
                <button onclick="sendTelegramAlert()" class="w-full py-2 neu-btn text-xs font-mono-code font-bold text-emerald-400">
                    Send Live Test Ping to Mobile
                </button>
                <div id="tgStatus" class="text-[10px] font-mono-code text-zinc-500 text-center"></div>
            </div>

        </div>

        <!-- RIGHT COLUMN: CAD ARCHITECTURAL BLUEPRINT & GAUGES (8 COLS) -->
        <div class="lg:col-span-8 space-y-5">

            <!-- COMPARISON METERS -->
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div class="p-4 neu-card">
                    <div class="text-[11px] font-mono-code uppercase text-zinc-500">Unmanaged Baseline</div>
                    <div id="baselineMeter" class="text-2xl font-bold text-red-400 mt-1">28.40 kW</div>
                    <div class="text-[11px] text-zinc-500 font-mono-code mt-0.5">All Lights + Fixed AC</div>
                </div>

                <div class="p-4 neu-card">
                    <div class="text-[11px] font-mono-code uppercase text-zinc-500">GridSense Optimized</div>
                    <div id="optimizedMeter" class="text-2xl font-bold text-emerald-400 mt-1">6.25 kW</div>
                    <div class="text-[11px] text-zinc-500 font-mono-code mt-0.5">Zoned Cutoffs + Adaptive AC</div>
                </div>

                <div class="p-4 neu-card">
                    <div class="text-[11px] font-mono-code uppercase text-zinc-500">Immediate Savings Rate</div>
                    <div id="savingsMeter" class="text-2xl font-bold text-yellow-400 mt-1">22.15 kW</div>
                    <div id="inrMeter" class="text-[11px] text-emerald-400 font-mono-code mt-0.5">INR 199.35 / Hour</div>
                </div>
            </div>

            <!-- AUTOMATION CONSOLIDATION POPUP CARD -->
            <div id="alertCard" class="p-4 neu-card border-l-4 border-l-yellow-400 flex items-start justify-between gap-4">
                <div>
                    <div class="flex items-center gap-2 text-xs font-mono-code font-bold text-yellow-400 uppercase">
                        <span class="w-2 h-2 rounded-full bg-yellow-400 animate-ping"></span>
                        Spatial Consolidation Nudge Triggered
                    </div>
                    <p id="alertText" class="text-xs font-mono-code text-zinc-300 mt-1">
                        Isolated class in B108 (Far End). Relocate to B101 near staircase to shut down 40m of corridor lighting.
                    </p>
                </div>
                <button onclick="applyConsolidation()" class="px-3.5 py-1.5 neu-btn text-xs font-mono-code font-bold text-emerald-400 shrink-0">
                    Apply Relocation
                </button>
            </div>

            <!-- THE ARCHITECTURAL CAD 2D FLOOR BLUEPRINT -->
            <div class="p-6 neu-card space-y-4">
                <div class="flex justify-between items-center border-b border-white/5 pb-3">
                    <div>
                        <h2 id="blueprintTitle" class="text-sm font-bold text-white uppercase tracking-wider font-mono-code">
                            BLOCK B // FLOOR 1 CAD ARCHITECTURAL BLUEPRINT
                        </h2>
                        <p class="text-[11px] text-zinc-500 font-mono-code">8 Classrooms | 80m Arterial Hallway | 4-Lift Elevator Bank | Fire Staircase</p>
                    </div>
                    <div id="elevState" class="text-[10px] font-mono-code text-zinc-400 neu-inset px-2.5 py-1">
                        Lifts: 2 Active (Mandatory Safety Floor)
                    </div>
                </div>

                <!-- CAD DRAWING CONTAINER -->
                <div class="neu-inset p-4 rounded-xl space-y-3 overflow-x-auto">
                    
                    <!-- NORTH WING: 4 CLASSROOMS (x01 to x04) -->
                    <div class="grid grid-cols-4 gap-3 min-w-[620px]">
                        <!-- ROOM 1 -->
                        <div id="cad_r1" class="cad-room p-3 cad-room-dark">
                            <div class="flex justify-between items-start">
                                <span class="text-xs font-mono-code font-bold text-white" id="name_r1">B101</span>
                                <span class="text-[9px] font-mono-code font-bold px-1.5 py-0.5 rounded bg-black/50 text-zinc-500" id="badge_r1">OFF</span>
                            </div>
                            <div class="grid grid-cols-3 gap-1.5 my-2.5">
                                <div class="cad-desk h-3" id="d1_r1"></div>
                                <div class="cad-desk h-3" id="d2_r1"></div>
                                <div class="cad-desk h-3" id="d3_r1"></div>
                                <div class="cad-desk h-3" id="d4_r1"></div>
                                <div class="cad-desk h-3" id="d5_r1"></div>
                                <div class="cad-desk h-3" id="d6_r1"></div>
                            </div>
                            <div class="flex justify-between items-center pt-1 border-t border-white/5">
                                <div class="flex gap-1.5">
                                    <div class="cad-light" id="l1_r1"></div>
                                    <div class="cad-light" id="l2_r1"></div>
                                </div>
                                <span class="text-[9px] font-mono-code text-zinc-400" id="ac_r1">AC: OFF</span>
                            </div>
                        </div>

                        <!-- ROOM 2 -->
                        <div id="cad_r2" class="cad-room p-3 cad-room-dark">
                            <div class="flex justify-between items-start">
                                <span class="text-xs font-mono-code font-bold text-white" id="name_r2">B102</span>
                                <span class="text-[9px] font-mono-code font-bold px-1.5 py-0.5 rounded bg-black/50 text-zinc-500" id="badge_r2">OFF</span>
                            </div>
                            <div class="grid grid-cols-3 gap-1.5 my-2.5">
                                <div class="cad-desk h-3" id="d1_r2"></div>
                                <div class="cad-desk h-3" id="d2_r2"></div>
                                <div class="cad-desk h-3" id="d3_r2"></div>
                                <div class="cad-desk h-3" id="d4_r2"></div>
                                <div class="cad-desk h-3" id="d5_r2"></div>
                                <div class="cad-desk h-3" id="d6_r2"></div>
                            </div>
                            <div class="flex justify-between items-center pt-1 border-t border-white/5">
                                <div class="flex gap-1.5">
                                    <div class="cad-light" id="l1_r2"></div>
                                    <div class="cad-light" id="l2_r2"></div>
                                </div>
                                <span class="text-[9px] font-mono-code text-zinc-400" id="ac_r2">AC: OFF</span>
                            </div>
                        </div>

                        <!-- ROOM 3 -->
                        <div id="cad_r3" class="cad-room p-3 cad-room-dark">
                            <div class="flex justify-between items-start">
                                <span class="text-xs font-mono-code font-bold text-white" id="name_r3">B103</span>
                                <span class="text-[9px] font-mono-code font-bold px-1.5 py-0.5 rounded bg-black/50 text-zinc-500" id="badge_r3">OFF</span>
                            </div>
                            <div class="grid grid-cols-3 gap-1.5 my-2.5">
                                <div class="cad-desk h-3" id="d1_r3"></div>
                                <div class="cad-desk h-3" id="d2_r3"></div>
                                <div class="cad-desk h-3" id="d3_r3"></div>
                                <div class="cad-desk h-3" id="d4_r3"></div>
                                <div class="cad-desk h-3" id="d5_r3"></div>
                                <div class="cad-desk h-3" id="d6_r3"></div>
                            </div>
                            <div class="flex justify-between items-center pt-1 border-t border-white/5">
                                <div class="flex gap-1.5">
                                    <div class="cad-light" id="l1_r3"></div>
                                    <div class="cad-light" id="l2_r3"></div>
                                </div>
                                <span class="text-[9px] font-mono-code text-zinc-400" id="ac_r3">AC: OFF</span>
                            </div>
                        </div>

                        <!-- ROOM 4 (FAR END) -->
                        <div id="cad_r4" class="cad-room p-3 cad-room-dark">
                            <div class="flex justify-between items-start">
                                <span class="text-xs font-mono-code font-bold text-white" id="name_r4">B104 (Far)</span>
                                <span class="text-[9px] font-mono-code font-bold px-1.5 py-0.5 rounded bg-black/50 text-zinc-500" id="badge_r4">OFF</span>
                            </div>
                            <div class="grid grid-cols-3 gap-1.5 my-2.5">
                                <div class="cad-desk h-3" id="d1_r4"></div>
                                <div class="cad-desk h-3" id="d2_r4"></div>
                                <div class="cad-desk h-3" id="d3_r4"></div>
                                <div class="cad-desk h-3" id="d4_r4"></div>
                                <div class="cad-desk h-3" id="d5_r4"></div>
                                <div class="cad-desk h-3" id="d6_r4"></div>
                            </div>
                            <div class="flex justify-between items-center pt-1 border-t border-white/5">
                                <div class="flex gap-1.5">
                                    <div class="cad-light" id="l1_r4"></div>
                                    <div class="cad-light" id="l2_r4"></div>
                                </div>
                                <span class="text-[9px] font-mono-code text-zinc-400" id="ac_r4">AC: OFF</span>
                            </div>
                        </div>
                    </div>

                    <!-- ARTERIAL 80M CENTRAL CORRIDOR WITH LIFTS & STAIRS -->
                    <div class="grid grid-cols-12 gap-2 py-2 min-w-[620px]">
                        
                        <!-- STAIRCASE & 4-LIFT SHAFT -->
                        <div class="col-span-3 p-2 bg-[#171a22] border border-[#2b3140] rounded flex flex-col justify-between">
                            <div class="flex justify-between items-center text-[10px] font-mono-code text-zinc-400 border-b border-white/5 pb-1">
                                <span>MAIN STAIRS</span>
                                <span class="text-emerald-400">4x LIFTS</span>
                            </div>
                            <!-- 4 ELEVATOR SHAFTS -->
                            <div class="grid grid-cols-4 gap-1 my-1.5">
                                <div class="h-5 bg-[#232836] border border-emerald-500/40 rounded flex items-center justify-center text-[8px] font-mono-code text-emerald-400 font-bold">C1</div>
                                <div class="h-5 bg-[#232836] border border-emerald-500/40 rounded flex items-center justify-center text-[8px] font-mono-code text-emerald-400 font-bold">C2</div>
                                <div id="cad_c3" class="h-5 bg-[#161820] border border-zinc-700 rounded flex items-center justify-center text-[8px] font-mono-code text-zinc-500">C3</div>
                                <div id="cad_c4" class="h-5 bg-[#161820] border border-zinc-700 rounded flex items-center justify-center text-[8px] font-mono-code text-zinc-500">C4</div>
                            </div>
                            <div class="text-[8px] font-mono-code text-zinc-500 text-center">Cars 1 & 2 Active | Cars 3 & 4 Sleep</div>
                        </div>

                        <!-- 3-ZONE SEQUENTIAL CORRIDOR STRIP -->
                        <div class="col-span-9 grid grid-cols-3 gap-2">
                            <div id="cad_corridor_z1" class="p-2 rounded flex flex-col justify-center items-center text-center font-mono-code text-[10px] corridor-dark">
                                <span class="font-bold">Zone 1 (Entrance)</span>
                                <span id="txt_corridor_z1" class="text-[9px] text-zinc-500">[DARK]</span>
                            </div>
                            <div id="cad_corridor_z2" class="p-2 rounded flex flex-col justify-center items-center text-center font-mono-code text-[10px] corridor-dark">
                                <span class="font-bold">Zone 2 (Mid-Way)</span>
                                <span id="txt_corridor_z2" class="text-[9px] text-zinc-500">[DARK]</span>
                            </div>
                            <div id="cad_corridor_z3" class="p-2 rounded flex flex-col justify-center items-center text-center font-mono-code text-[10px] corridor-dark">
                                <span class="font-bold">Zone 3 (Far End)</span>
                                <span id="txt_corridor_z3" class="text-[9px] text-zinc-500">[DARK]</span>
                            </div>
                        </div>

                    </div>

                    <!-- SOUTH WING: 4 CLASSROOMS (x05 to x08) -->
                    <div class="grid grid-cols-4 gap-3 min-w-[620px]">
                        <!-- ROOM 5 -->
                        <div id="cad_r5" class="cad-room p-3 cad-room-dark">
                            <div class="flex justify-between items-start">
                                <span class="text-xs font-mono-code font-bold text-white" id="name_r5">B105</span>
                                <span class="text-[9px] font-mono-code font-bold px-1.5 py-0.5 rounded bg-black/50 text-zinc-500" id="badge_r5">OFF</span>
                            </div>
                            <div class="grid grid-cols-3 gap-1.5 my-2.5">
                                <div class="cad-desk h-3" id="d1_r5"></div>
                                <div class="cad-desk h-3" id="d2_r5"></div>
                                <div class="cad-desk h-3" id="d3_r5"></div>
                                <div class="cad-desk h-3" id="d4_r5"></div>
                                <div class="cad-desk h-3" id="d5_r5"></div>
                                <div class="cad-desk h-3" id="d6_r5"></div>
                            </div>
                            <div class="flex justify-between items-center pt-1 border-t border-white/5">
                                <div class="flex gap-1.5">
                                    <div class="cad-light" id="l1_r5"></div>
                                    <div class="cad-light" id="l2_r5"></div>
                                </div>
                                <span class="text-[9px] font-mono-code text-zinc-400" id="ac_r5">AC: OFF</span>
                            </div>
                        </div>

                        <!-- ROOM 6 -->
                        <div id="cad_r6" class="cad-room p-3 cad-room-dark">
                            <div class="flex justify-between items-start">
                                <span class="text-xs font-mono-code font-bold text-white" id="name_r6">B106</span>
                                <span class="text-[9px] font-mono-code font-bold px-1.5 py-0.5 rounded bg-black/50 text-zinc-500" id="badge_r6">OFF</span>
                            </div>
                            <div class="grid grid-cols-3 gap-1.5 my-2.5">
                                <div class="cad-desk h-3" id="d1_r6"></div>
                                <div class="cad-desk h-3" id="d2_r6"></div>
                                <div class="cad-desk h-3" id="d3_r6"></div>
                                <div class="cad-desk h-3" id="d4_r6"></div>
                                <div class="cad-desk h-3" id="d5_r6"></div>
                                <div class="cad-desk h-3" id="d6_r6"></div>
                            </div>
                            <div class="flex justify-between items-center pt-1 border-t border-white/5">
                                <div class="flex gap-1.5">
                                    <div class="cad-light" id="l1_r6"></div>
                                    <div class="cad-light" id="l2_r6"></div>
                                </div>
                                <span class="text-[9px] font-mono-code text-zinc-400" id="ac_r6">AC: OFF</span>
                            </div>
                        </div>

                        <!-- ROOM 7 -->
                        <div id="cad_r7" class="cad-room p-3 cad-room-dark">
                            <div class="flex justify-between items-start">
                                <span class="text-xs font-mono-code font-bold text-white" id="name_r7">B107</span>
                                <span class="text-[9px] font-mono-code font-bold px-1.5 py-0.5 rounded bg-black/50 text-zinc-500" id="badge_r7">OFF</span>
                            </div>
                            <div class="grid grid-cols-3 gap-1.5 my-2.5">
                                <div class="cad-desk h-3" id="d1_r7"></div>
                                <div class="cad-desk h-3" id="d2_r7"></div>
                                <div class="cad-desk h-3" id="d3_r7"></div>
                                <div class="cad-desk h-3" id="d4_r7"></div>
                                <div class="cad-desk h-3" id="d5_r7"></div>
                                <div class="cad-desk h-3" id="d6_r7"></div>
                            </div>
                            <div class="flex justify-between items-center pt-1 border-t border-white/5">
                                <div class="flex gap-1.5">
                                    <div class="cad-light" id="l1_r7"></div>
                                    <div class="cad-light" id="l2_r7"></div>
                                </div>
                                <span class="text-[9px] font-mono-code text-zinc-400" id="ac_r7">AC: OFF</span>
                            </div>
                        </div>

                        <!-- ROOM 8 (FAR END) -->
                        <div id="cad_r8" class="cad-room p-3 cad-room-lit">
                            <div class="flex justify-between items-start">
                                <span class="text-xs font-mono-code font-bold text-white" id="name_r8">B108 (Far)</span>
                                <span class="text-[9px] font-mono-code font-bold px-1.5 py-0.5 rounded bg-black/50 text-amber-300" id="badge_r8">LIT</span>
                            </div>
                            <div class="grid grid-cols-3 gap-1.5 my-2.5">
                                <div class="cad-desk cad-desk-lit h-3" id="d1_r8"></div>
                                <div class="cad-desk cad-desk-lit h-3" id="d2_r8"></div>
                                <div class="cad-desk cad-desk-lit h-3" id="d3_r8"></div>
                                <div class="cad-desk cad-desk-lit h-3" id="d4_r8"></div>
                                <div class="cad-desk cad-desk-lit h-3" id="d5_r8"></div>
                                <div class="cad-desk cad-desk-lit h-3" id="d6_r8"></div>
                            </div>
                            <div class="flex justify-between items-center pt-1 border-t border-white/5">
                                <div class="flex gap-1.5">
                                    <div class="cad-light cad-light-lit" id="l1_r8"></div>
                                    <div class="cad-light cad-light-lit" id="l2_r8"></div>
                                </div>
                                <span class="text-[9px] font-mono-code text-amber-300" id="ac_r8">AC: 26°C</span>
                            </div>
                        </div>
                    </div>

                </div>

            </div>

        </div>

    </div>

    <!-- JAVASCRIPT CONTROLLER -->
    <script>
        let currentFloor = 1;
        let currentRelocation = null;

        function switchFloor(fl) {
            currentFloor = fl;
            document.getElementById('btnFloor1').className = (fl === 1) ? 
                "py-2.5 neu-btn text-xs font-mono-code font-bold text-emerald-400 text-center" : 
                "py-2.5 neu-btn text-xs font-mono-code font-bold text-zinc-400 text-center";
            document.getElementById('btnFloor2').className = (fl === 2) ? 
                "py-2.5 neu-btn text-xs font-mono-code font-bold text-emerald-400 text-center" : 
                "py-2.5 neu-btn text-xs font-mono-code font-bold text-zinc-400 text-center";

            document.getElementById('blueprintTitle').innerText = `BLOCK B // FLOOR ${fl} CAD ARCHITECTURAL BLUEPRINT`;

            for (let i = 1; i <= 8; i++) {
                const rNum = `B${fl}0${i}`;
                const isFar = (i === 4 || i === 8) ? " (Far)" : "";
                document.getElementById(`lbl_r${i}`).innerText = `${rNum}${isFar}:`;
                document.getElementById(`name_r${i}`).innerText = `${rNum}${isFar}`;
            }

            onParamChange();
        }

        function onParamChange() {
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
                roomsPayload[`B${currentFloor}0${i}`] = occ;
            }

            const payload = {
                floor: currentFloor,
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
            .then(data => renderCADState(data))
            .catch(err => console.error(err));
        }

        function renderCADState(data) {
            document.getElementById('baselineMeter').innerText = `${data.total_baseline_kw} kW`;
            document.getElementById('optimizedMeter').innerText = `${data.total_optimized_kw} kW`;
            document.getElementById('savingsMeter').innerText = `${data.kw_saved} kW (${data.savings_percentage}%)`;
            document.getElementById('inrMeter').innerText = `INR ${data.inr_per_hour_saved} / Hour`;
            document.getElementById('elevState').innerText = data.elevator_mode;

            const rooms = data.rooms;
            for (let i = 1; i <= 8; i++) {
                const r_id = `B${currentFloor}0${i}`;
                const r = rooms[r_id];
                if (!r) continue;

                const card = document.getElementById(`cad_r${i}`);
                const badge = document.getElementById(`badge_r${i}`);
                const ac = document.getElementById(`ac_r${i}`);

                if (r.lighting_glow) {
                    card.className = "cad-room p-3 cad-room-lit";
                    badge.innerText = `${r.occupancy} OCC / LIT`;
                    badge.className = "text-[9px] font-mono-code font-bold px-1.5 py-0.5 rounded bg-black/60 text-amber-300";
                    ac.innerText = `AC: ${r.ac_setpoint}`;
                    ac.className = "text-[9px] font-mono-code text-amber-300 font-semibold";

                    for (let d = 1; d <= 6; d++) document.getElementById(`d${d}_r${i}`).className = "cad-desk cad-desk-lit h-3";
                    document.getElementById(`l1_r${i}`).className = "cad-light cad-light-lit";
                    document.getElementById(`l2_r${i}`).className = "cad-light cad-light-lit";
                } else {
                    card.className = "cad-room p-3 cad-room-dark";
                    badge.innerText = "OFF";
                    badge.className = "text-[9px] font-mono-code font-bold px-1.5 py-0.5 rounded bg-black/60 text-zinc-500";
                    ac.innerText = "AC: OFF";
                    ac.className = "text-[9px] font-mono-code text-zinc-500";

                    for (let d = 1; d <= 6; d++) document.getElementById(`d${d}_r${i}`).className = "cad-desk h-3";
                    document.getElementById(`l1_r${i}`).className = "cad-light";
                    document.getElementById(`l2_r${i}`).className = "cad-light";
                }
            }

            const cz = data.corridor_state;
            updateCorridorUI('cad_corridor_z1', 'txt_corridor_z1', cz.zone1_entrance === "LIT");
            updateCorridorUI('cad_corridor_z2', 'txt_corridor_z2', cz.zone2_mid === "LIT");
            updateCorridorUI('cad_corridor_z3', 'txt_corridor_z3', cz.zone3_far === "LIT");

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

        function updateCorridorUI(elemId, txtId, isLit) {
            const el = document.getElementById(elemId);
            const txt = document.getElementById(txtId);
            if (!el || !txt) return;

            if (isLit) {
                el.className = "p-2 rounded flex flex-col justify-center items-center text-center font-mono-code text-[10px] corridor-lit text-amber-300 font-bold";
                txt.innerText = "[LIT]";
                txt.className = "text-[9px] text-amber-300 font-bold";
            } else {
                el.className = "p-2 rounded flex flex-col justify-center items-center text-center font-mono-code text-[10px] corridor-dark text-zinc-600 font-normal";
                txt.innerText = "[DARK]";
                txt.className = "text-[9px] text-zinc-500";
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
                onParamChange();
            }
        }

        function applyPreset(type) {
            if (type === 'morning') {
                document.getElementById('timeSlider').value = 9.5;
                document.getElementById('tempSlider').value = 28;
                document.getElementById('weatherSelect').value = "Sunny / Daylight";
                for (let i = 1; i <= 8; i++) document.getElementById(`occ_r${i}`).value = (i <= 6) ? 45 : 0;
            } else if (type === 'afternoon') {
                document.getElementById('timeSlider').value = 14.5;
                document.getElementById('tempSlider').value = 36;
                document.getElementById('weatherSelect').value = "Sunny / Daylight";
                for (let i = 1; i <= 8; i++) document.getElementById(`occ_r${i}`).value = (i === 1 || i === 2) ? 50 : 0;
            } else if (type === 'night_waste') {
                document.getElementById('timeSlider').value = 19.5;
                document.getElementById('tempSlider').value = 32;
                document.getElementById('weatherSelect').value = "Night";
                for (let i = 1; i <= 7; i++) document.getElementById(`occ_r${i}`).value = 0;
                document.getElementById(`occ_r8`).value = 25;
            }
            onParamChange();
        }

        function sendTelegramAlert() {
            const token = document.getElementById('tgToken').value.trim();
            const chatId = document.getElementById('tgChatId').value.trim();
            const statusDiv = document.getElementById('tgStatus');

            if (!token || !chatId) {
                statusDiv.innerText = "Please provide both Bot Token and Chat ID.";
                statusDiv.className = "text-[10px] font-mono-code text-red-400 text-center";
                return;
            }

            statusDiv.innerText = "Dispatching alert to mobile...";
            statusDiv.className = "text-[10px] font-mono-code text-yellow-400 text-center";

            fetch('/api/sandbox/notify-telegram', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    token: token,
                    chat_id: chatId,
                    message: "GridSense Alert [JIT Campus]: Spatial Consolidation Triggered. Isolated class in far hallway relocated near entrance. 40m corridor darkened. Instant savings: 22.15 kW (INR 199.35/hr)."
                })
            })
            .then(res => res.json())
            .then(data => {
                if (data.status === "success") {
                    statusDiv.innerText = "Alert delivered to phone successfully.";
                    statusDiv.className = "text-[10px] font-mono-code text-emerald-400 text-center";
                } else {
                    statusDiv.innerText = `Error: ${data.message}`;
                    statusDiv.className = "text-[10px] font-mono-code text-red-400 text-center";
                }
            })
            .catch(err => {
                statusDiv.innerText = "Network error communicating with Telegram.";
                statusDiv.className = "text-[10px] font-mono-code text-red-400 text-center";
            });
        }

        window.onload = () => onParamChange();
    </script>
</body>
</html>
"""
