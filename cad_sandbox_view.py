"""
GridSense Block B Interactive Sandbox & Vector CAD Blueprint
Minimalist UI (#2B2D31 Gray, #D9DAD0 Silver, #FFC93C Yellow)
Features:
- 12-Hour AM/PM time formatting everywhere
- Mode 1 (Variable Mode): Time slider, Temp slider, and ON/OFF toggle + headcount slider for all 8 Classrooms & 3 Labs
- Mode 2 (Set / Timetable Mode): Auto-generated realistic academic schedule by time of day with 1-click slot loading
- Two-stage workflow: Preview Unmanaged Baseline (random/partial lights ON in empty rooms) -> Click "Simulate" to execute relocations, wing shutdowns, dynamic lift staging, and AC optimization
- 3-Part Natural Report Template + Time-Indexed Session Suggestions Log
- Zero-Prompt Automatic Phone / Webhook Dispatch (n8n, Power Automate, Telegram, WhatsApp)
"""


def _render_svg_room(rid: str, label: str, sub: str, x: int, y: int, w: int, h: int) -> str:
    """Generate a perfectly aligned architectural CAD room block with 0 text overlap."""
    cx = x + w // 2
    # 4 ceiling luminaires positioned in a clean horizontal row
    l_y = y + 54
    l1_x = x + int(w * 0.20)
    l2_x = x + int(w * 0.40)
    l3_x = x + int(w * 0.60)
    l4_x = x + int(w * 0.80)

    # Desks positioned in 2 neat rows in the middle
    d_y1 = y + 74
    d_y2 = y + 92
    dw = int(w * 0.36)
    d1_x = x + int(w * 0.10)
    d2_x = x + int(w * 0.54)

    # Bottom status bar for AC setpoint and Relocation tag
    ac_y = y + h - 24

    return f"""
    <g id="room_grp_{rid}" class="cad-room-group">
        <!-- Main Room Structural Box -->
        <rect id="poly_{rid}" x="{x}" y="{y}" width="{w}" height="{h}" rx="6" class="room-box room-unlit" />

        <!-- Top Header Bar -->
        <rect x="{x+1}" y="{y+1}" width="{w-2}" height="28" rx="5" fill="#1E2024" opacity="0.85" />
        <text x="{x+10}" y="{y+19}" fill="#FFFFFF" font-family="Inter, sans-serif" font-size="11.5" font-weight="700">{label}</text>
        <text id="occ_badge_{rid}" x="{x+w-10}" y="{y+19}" fill="#8E9297" font-family="Inter, sans-serif" font-size="10.5" font-weight="700" text-anchor="end">OFF</text>

        <!-- Subtitle / Wing Area -->
        <text id="sub_badge_{rid}" x="{x+10}" y="{y+40}" fill="#8E9297" font-family="Inter, sans-serif" font-size="9.5" font-weight="500">{sub}</text>

        <!-- 4 Individual Ceiling Luminaires (L1, L2, L3, L4) -->
        <g>
            <circle id="l1_{rid}" cx="{l1_x}" cy="{l_y}" r="6" class="luminaire lum-off" />
            <circle id="l2_{rid}" cx="{l2_x}" cy="{l_y}" r="6" class="luminaire lum-off" />
            <circle id="l3_{rid}" cx="{l3_x}" cy="{l_y}" r="6" class="luminaire lum-off" />
            <circle id="l4_{rid}" cx="{l4_x}" cy="{l_y}" r="6" class="luminaire lum-off" />
        </g>

        <!-- Student Desks / Lab Workbenches -->
        <rect id="d1_{rid}" x="{d1_x}" y="{d_y1}" width="{dw}" height="11" rx="2" class="desk-box desk-off" />
        <rect id="d2_{rid}" x="{d2_x}" y="{d_y1}" width="{dw}" height="11" rx="2" class="desk-box desk-off" />
        <rect id="d3_{rid}" x="{d1_x}" y="{d_y2}" width="{dw}" height="11" rx="2" class="desk-box desk-off" />
        <rect id="d4_{rid}" x="{d2_x}" y="{d_y2}" width="{dw}" height="11" rx="2" class="desk-box desk-off" />

        <!-- Bottom AC & Power Pill -->
        <rect id="ac_bg_{rid}" x="{x+8}" y="{ac_y}" width="{w-16}" height="18" rx="4" fill="#1E2024" />
        <text id="ac_{rid}" x="{x+14}" y="{ac_y+12.5}" fill="#8E9297" font-family="Inter, sans-serif" font-size="9.5" font-weight="600">AC: OFF</text>
        <text id="kw_{rid}" x="{x+w-14}" y="{ac_y+12.5}" fill="#8E9297" font-family="Inter, sans-serif" font-size="9.5" font-weight="600" text-anchor="end">0.0 kW</text>
    </g>
    """


def render_cad_sandbox_html():
    # Generate perfectly aligned SVG rooms for Left Wing, Right Wing, and 3 Labs
    svg_rooms = []

    # North Wing Labs: LAB1 (Left/NW) and LAB2 (Right/NE)
    svg_rooms.append(_render_svg_room("LAB1", "Lab B-1", "Left Wing // Hardware Lab (150m²)", 250, 55, 220, 135))
    svg_rooms.append(_render_svg_room("LAB2", "Lab B-2", "Right Wing // Comm Lab (150m²)", 650, 55, 220, 135))

    # Left Wing Classrooms: B101, B102, B103, B104 (Vertical Stack on West Arc)
    svg_rooms.append(_render_svg_room("B101", "CR B-101", "Left Wing // Near Main Stairs", 25, 195, 200, 135))
    svg_rooms.append(_render_svg_room("B102", "CR B-102", "Left Wing // Mid-North", 25, 340, 200, 135))
    svg_rooms.append(_render_svg_room("B103", "CR B-103", "Left Wing // Mid-South", 25, 485, 200, 135))
    svg_rooms.append(_render_svg_room("B104", "CR B-104", "Left Wing // Far SW End", 25, 630, 200, 135))

    # Right Wing Classrooms: B105, B106, B107, B108 (Vertical Stack on East Arc)
    svg_rooms.append(_render_svg_room("B105", "CR B-105", "Right Wing // Near Main Stairs", 895, 195, 200, 135))
    svg_rooms.append(_render_svg_room("B106", "CR B-106", "Right Wing // Mid-North", 895, 340, 200, 135))
    svg_rooms.append(_render_svg_room("B107", "CR B-107", "Right Wing // Mid-South", 895, 485, 200, 135))
    svg_rooms.append(_render_svg_room("B108", "CR B-108", "Right Wing // Far SE End", 895, 630, 200, 135))

    # South-East Computer Lab B-3
    svg_rooms.append(_render_svg_room("LAB3", "Comp Lab B-3", "Right Wing // 50 PCs (150m²)", 685, 705, 200, 135))

    all_svg_rooms_str = "\n".join(svg_rooms)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GridSense // Block B Interactive Simulator</title>
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
            border: 1px solid rgba(255, 255, 255, 0.07);
        }}
        .sub-box {{
            background: #2B2D31;
            border-radius: 8px;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }}
        .nav-link {{
            color: #8E9297;
            font-size: 14px;
            font-weight: 500;
            padding: 8px 4px;
            border-bottom: 2px solid transparent;
            transition: color 0.15s ease, border-color 0.15s ease;
            text-decoration: none;
        }}
        .nav-link:hover {{ color: #D9DAD0; }}
        .nav-link.active {{
            color: #FFFFFF;
            border-bottom-color: #FFC93C;
        }}
        .mode-tab {{
            flex: 1;
            padding: 9px 12px;
            font-size: 12px;
            font-weight: 600;
            text-align: center;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.15s ease;
            color: #8E9297;
            background: transparent;
            border: none;
        }}
        .mode-tab.active {{
            background: #FFC93C;
            color: #2B2D31;
            font-weight: 700;
        }}
        input[type="range"] {{
            -webkit-appearance: none;
            appearance: none;
            height: 5px;
            background: #2B2D31;
            border-radius: 4px;
            outline: none;
        }}
        input[type="range"]::-webkit-slider-thumb {{
            -webkit-appearance: none;
            appearance: none;
            width: 15px;
            height: 15px;
            border-radius: 50%;
            background: #FFC93C;
            cursor: pointer;
            border: 2px solid #2B2D31;
        }}

        /* SVG Blueprint Styles */
        .blueprint-wrap {{
            background-color: #1E2024;
            background-image:
                linear-gradient(rgba(255, 255, 255, 0.025) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255, 255, 255, 0.025) 1px, transparent 1px);
            background-size: 28px 28px;
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.08);
        }}
        .room-box {{
            transition: fill 0.25s ease, stroke 0.25s ease, stroke-width 0.25s ease;
        }}
        .room-unlit {{
            fill: #27292E;
            stroke: #40444B;
            stroke-width: 1.5;
        }}
        .room-lit {{
            fill: #353022;
            stroke: #FFC93C;
            stroke-width: 2.2;
        }}
        .room-wasted {{
            fill: #332B24;
            stroke: #F59E0B;
            stroke-width: 1.8;
            stroke-dasharray: 5 3;
        }}
        .room-relocated {{
            fill: #232A34;
            stroke: #38BDF8;
            stroke-width: 1.8;
            stroke-dasharray: 4 4;
        }}
        .luminaire {{
            transition: all 0.25s ease;
        }}
        .lum-on {{
            fill: #FFC93C;
            stroke: #FEF08A;
            stroke-width: 1.5;
            filter: drop-shadow(0 0 6px #FFC93C);
        }}
        .lum-off {{
            fill: #1E2024;
            stroke: #4F545C;
            stroke-width: 1.2;
            filter: none;
        }}
        .desk-box {{
            transition: all 0.25s ease;
        }}
        .desk-on {{
            fill: #4A412A;
            stroke: #D9A528;
            stroke-width: 1;
        }}
        .desk-off {{
            fill: #2E3136;
            stroke: #3F434A;
            stroke-width: 1;
        }}
        .corridor-line {{
            transition: all 0.3s ease;
            fill: none;
        }}
        .corridor-on {{
            stroke: #FFC93C;
            stroke-width: 4;
            filter: drop-shadow(0 0 6px rgba(255, 201, 60, 0.6));
        }}
        .corridor-off {{
            stroke: #3A3E45;
            stroke-width: 2;
            stroke-dasharray: 6 6;
            filter: none;
        }}
        .lift-car-on {{
            fill: #3A331E;
            stroke: #FFC93C;
            stroke-width: 2;
        }}
        .lift-car-off {{
            fill: #232529;
            stroke: #40444B;
            stroke-width: 1.2;
            stroke-dasharray: 3 3;
        }}
        .zone-box-on {{
            fill: #353022;
            stroke: #FFC93C;
            stroke-width: 2;
        }}
        .zone-box-off {{
            fill: #25272C;
            stroke: #3E4249;
            stroke-width: 1.5;
        }}
    </style>
</head>
<body class="min-h-screen flex flex-col">

    <!-- TOP NAVBAR -->
    <header style="background: #2B2D31; border-bottom: 1px solid rgba(255,255,255,0.07);">
        <div class="max-w-[1560px] mx-auto px-5 h-14 flex items-center justify-between">
            <div class="flex items-center gap-3">
                <div class="w-8 h-8 rounded-lg flex items-center justify-center font-bold text-sm" style="background: #FFC93C; color: #2B2D31;">
                    GS
                </div>
                <span class="text-base font-bold text-white tracking-tight">GridSense</span>
                <span class="text-xs px-2 py-0.5 rounded font-medium" style="background: #36393F; color: #8E9297;">JIT Block B Simulator</span>
            </div>
            <nav class="flex items-center gap-7">
                <a href="/" class="nav-link">Dashboard</a>
                <a href="/sandbox" class="nav-link active">Sandbox</a>
                <a href="/systems" class="nav-link">Campus Systems</a>
                <a href="/blueprint" class="nav-link">Blueprint</a>
            </nav>
        </div>
    </header>

    <!-- MAIN CONTENT GRID -->
    <main class="flex-1 max-w-[1560px] w-full mx-auto px-5 py-5">
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-5 items-start">

            <!-- ================= LEFT COLUMN: CONTROLS (4 COLS) ================= -->
            <div class="lg:col-span-4 space-y-4">

                <!-- 1. MODE SWITCHER (VARIABLE MODE vs SET TIMETABLE MODE) -->
                <div class="card p-3">
                    <div class="text-[11px] font-semibold uppercase tracking-wider mb-2" style="color: #8E9297;">Simulation Operating Mode</div>
                    <div class="flex gap-1.5 p-1 rounded-lg" style="background: #2B2D31;">
                        <button id="tabVariable" onclick="switchMode('variable')" class="mode-tab active">
                            Mode 1: Variable Mode
                        </button>
                        <button id="tabTimetable" onclick="switchMode('timetable')" class="mode-tab">
                            Mode 2: Set Timetable
                        </button>
                    </div>
                </div>

                <!-- 2. ENVIRONMENTAL VARIABLES (TIME IN 12H AM/PM & OUTSIDE TEMP) -->
                <div class="card p-4 space-y-3.5">
                    <div class="flex items-center justify-between">
                        <span class="text-xs font-semibold uppercase tracking-wider" style="color: #8E9297;">1. Time &amp; Weather Variables</span>
                        <span id="daylightBadge" class="text-[11px] font-data px-2 py-0.5 rounded" style="background: #2B2D31; color: #FFC93C;">Daylight</span>
                    </div>

                    <!-- Time of Day (12-Hour AM/PM) -->
                    <div>
                        <div class="flex justify-between items-center text-xs mb-1.5">
                            <span style="color: #D9DAD0;">Time of Day</span>
                            <span id="timeDisplay12h" class="font-data font-bold text-sm" style="color: #FFC93C;">02:00 PM</span>
                        </div>
                        <input type="range" id="timeSlider" min="6" max="23" step="0.5" value="14.0" oninput="onVariableInputChanged()" class="w-full">
                        <div class="flex justify-between text-[10px] font-data mt-1" style="color: #8E9297;">
                            <span>06:00 AM</span>
                            <span>12:00 PM</span>
                            <span>06:00 PM</span>
                            <span>11:00 PM</span>
                        </div>
                    </div>

                    <!-- Outside Temperature -->
                    <div>
                        <div class="flex justify-between items-center text-xs mb-1.5">
                            <span style="color: #D9DAD0;">Outside Temperature</span>
                            <span id="tempDisplay" class="font-data font-bold text-sm text-white">33°C</span>
                        </div>
                        <input type="range" id="tempSlider" min="20" max="40" step="1" value="33" oninput="onVariableInputChanged()" class="w-full">
                        <div class="flex justify-between text-[10px] font-data mt-1" style="color: #8E9297;">
                            <span>20°C (Cool)</span>
                            <span>30°C (Warm)</span>
                            <span>40°C (Peak Heat)</span>
                        </div>
                    </div>

                    <!-- Sky Condition -->
                    <div>
                        <label class="block text-xs mb-1" style="color: #D9DAD0;">Outside Sky Condition</label>
                        <select id="weatherSelect" onchange="onVariableInputChanged()" class="w-full p-2 rounded-lg text-xs font-medium outline-none" style="background: #2B2D31; color: #FFFFFF; border: 1px solid rgba(255,255,255,0.08);">
                            <option value="Sunny / Daylight" selected>Sunny / Clear Sky (High Natural Sunlight)</option>
                            <option value="Overcast / Rainy">Overcast / Cloudy (Low Natural Lux)</option>
                            <option value="Night">Night / Dark Outside</option>
                        </select>
                    </div>
                </div>

                <!-- 3A. VARIABLE MODE: ACTIVE CLASSES & LABS (ON/OFF TOGGLE + PEOPLE SLIDER) -->
                <div id="panelVariable" class="card p-4 space-y-3">
                    <div class="flex items-center justify-between">
                        <div>
                            <div class="text-xs font-semibold uppercase tracking-wider" style="color: #8E9297;">2. Active Classes &amp; Labs</div>
                            <div class="text-[11px] mt-0.5" style="color: #8E9297;">Toggle ON any room to set student headcount</div>
                        </div>
                        <div class="flex gap-1.5">
                            <button onclick="loadDemoScenario('wing_consolidate')" class="px-2 py-1 rounded text-[10px] font-semibold" style="background: #2B2D31; color: #FFC93C; border: 1px solid rgba(255,201,60,0.3);">
                                3 Left + 1 Right
                            </button>
                            <button onclick="clearAllRooms()" class="px-2 py-1 rounded text-[10px] font-semibold" style="background: #2B2D31; color: #8E9297;">
                                All Off
                            </button>
                        </div>
                    </div>

                    <!-- Live Wing Summary Bar -->
                    <div class="grid grid-cols-3 gap-2 p-2 rounded-lg text-center font-data text-[11px]" style="background: #2B2D31;">
                        <div>
                            <span style="color: #8E9297;">Active:</span>
                            <span id="summaryActiveCount" class="font-bold text-white ml-1">4</span>
                        </div>
                        <div>
                            <span style="color: #8E9297;">Left Wing:</span>
                            <span id="summaryLeftPop" class="font-bold" style="color: #FFC93C;">83p</span>
                        </div>
                        <div>
                            <span style="color: #8E9297;">Right Wing:</span>
                            <span id="summaryRightPop" class="font-bold" style="color: #FFC93C;">22p</span>
                        </div>
                    </div>

                    <!-- Left Wing Rooms -->
                    <div>
                        <div class="text-[11px] font-bold uppercase tracking-wider mb-1.5" style="color: #D9DAD0;">Left Wing (West // Lifts L1 &amp; L2)</div>
                        <div id="leftWingControls" class="space-y-1.5"></div>
                    </div>

                    <!-- Right Wing Rooms -->
                    <div class="pt-1">
                        <div class="text-[11px] font-bold uppercase tracking-wider mb-1.5" style="color: #D9DAD0;">Right Wing (East // Lifts L3 &amp; L4)</div>
                        <div id="rightWingControls" class="space-y-1.5"></div>
                    </div>
                </div>

                <!-- 3B. SET TIMETABLE MODE: GENERATED SCHEDULE SLOTS -->
                <div id="panelTimetable" class="card p-4 space-y-3" style="display: none;">
                    <div class="flex items-center justify-between">
                        <div>
                            <div class="text-xs font-semibold uppercase tracking-wider" style="color: #8E9297;">Generated Day Timetable</div>
                            <div class="text-[11px] mt-0.5" style="color: #8E9297;">Peak morning sessions, afternoon classes &amp; evening labs</div>
                        </div>
                        <button onclick="regenerateTimetable()" class="px-2.5 py-1.5 rounded-lg text-xs font-semibold" style="background: #FFC93C; color: #2B2D31;">
                            Regenerate
                        </button>
                    </div>
                    <div id="timetableSlotsList" class="space-y-2 max-h-[430px] overflow-y-auto pr-1"></div>
                </div>

                <!-- 4. PRIMARY ACTION: SIMULATE BUTTON -->
                <div class="card p-4 space-y-2.5">
                    <div class="flex items-center justify-between text-xs">
                        <span style="color: #8E9297;">Floor View State:</span>
                        <span id="viewStateBadge" class="font-data font-bold px-2 py-0.5 rounded text-[11px]" style="background: rgba(245,158,11,0.15); color: #F59E0B;">
                            UNMANAGED BASELINE
                        </span>
                    </div>
                    <div class="flex gap-2">
                        <button onclick="runSimulation()" class="flex-1 py-3 px-4 rounded-xl font-bold text-sm tracking-wide transition-all" style="background: #FFC93C; color: #2B2D31; box-shadow: 0 4px 14px rgba(255,201,60,0.25);">
                            SIMULATE &amp; OPTIMIZE
                        </button>
                        <button onclick="showBaselinePreview()" class="py-3 px-3.5 rounded-xl font-semibold text-xs transition-all" style="background: #2B2D31; color: #D9DAD0; border: 1px solid rgba(255,255,255,0.08);" title="View Unmanaged State Before Simulation">
                            Reset View
                        </button>
                    </div>
                    <div id="autoPingStatus" class="text-[11px] font-data text-center" style="color: #8E9297;">
                        Clicking Simulate optimizes floor &amp; logs suggestions to Dashboard.
                    </div>
                </div>

            </div>

            <!-- ================= RIGHT COLUMN: METERS, BLUEPRINT & REPORT (8 COLS) ================= -->
            <div class="lg:col-span-8 space-y-4">

                <!-- 1. TOP KPI METERS (GLANCEABLE) -->
                <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                    <div class="card p-4">
                        <div class="text-[11px] font-semibold uppercase tracking-wider" style="color: #8E9297;">Unmanaged Baseline Draw</div>
                        <div id="meterBaseline" class="text-2xl font-bold font-data text-white mt-1">41.74 kW</div>
                        <div class="text-[11px] mt-1" style="color: #8E9297;">Random lights &amp; all 4 lifts running</div>
                    </div>

                    <div class="card p-4">
                        <div class="text-[11px] font-semibold uppercase tracking-wider" style="color: #8E9297;">Simulated Optimized Draw</div>
                        <div id="meterOptimized" class="text-2xl font-bold font-data mt-1" style="color: #8E9297;">Click Simulate</div>
                        <div id="meterLiftSub" class="text-[11px] mt-1" style="color: #8E9297;">Awaiting simulation run</div>
                    </div>

                    <div class="card p-4">
                        <div class="text-[11px] font-semibold uppercase tracking-wider" style="color: #8E9297;">Savings Rate (Post-Simulation)</div>
                        <div id="meterSavings" class="text-2xl font-bold font-data mt-1" style="color: #8E9297;">--</div>
                        <div id="meterInr" class="text-[11px] font-data mt-1" style="color: #8E9297;">Press Simulate to calculate</div>
                    </div>
                </div>

                <!-- 2. 3-PART SIMULATION OUTPUT & MESSAGE DISPATCH TEMPLATE -->
                <div id="simulationReportCard" class="card p-5" style="display: none; border-left: 4px solid #FFC93C;">
                    <div class="flex flex-wrap items-center justify-between gap-2 mb-3">
                        <div class="flex items-center gap-2">
                            <span class="px-2.5 py-0.5 rounded text-xs font-bold font-data" style="background: #FFC93C; color: #2B2D31;">SIMULATION COMPLETE</span>
                            <span id="reportTimeHeader" class="text-sm font-bold text-white">JIT Block B @ 02:00 PM</span>
                        </div>
                        <span id="reportDispatchBadge" class="text-xs font-data px-2.5 py-0.5 rounded" style="background: #2B2D31; color: #FFC93C;">
                            Auto-Logged to Dashboard
                        </span>
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
                        <div class="p-3.5 rounded-lg" style="background: #2B2D31;">
                            <div class="font-bold uppercase text-[10px] tracking-wider mb-1.5" style="color: #FFC93C;">1. Relocation Suggestion</div>
                            <p id="repPart1" class="leading-relaxed" style="color: #D9DAD0;"></p>
                        </div>
                        <div class="p-3.5 rounded-lg" style="background: #2B2D31;">
                            <div class="font-bold uppercase text-[10px] tracking-wider mb-1.5 text-white">2. Actions Taken (Lifts &amp; Lights)</div>
                            <p id="repPart2" class="leading-relaxed" style="color: #D9DAD0;"></p>
                        </div>
                        <div class="p-3.5 rounded-lg" style="background: #2B2D31;">
                            <div class="font-bold uppercase text-[10px] tracking-wider mb-1.5" style="color: #FFC93C;">3. Energy &amp; Cost Saved</div>
                            <p id="repPart3" class="leading-relaxed font-data font-semibold" style="color: #FFC93C;"></p>
                        </div>
                    </div>
                </div>

                <!-- 3. ALIGNED VECTOR ARCHITECTURAL FLOOR PLAN (BLOCK B) -->
                <div class="card p-4 space-y-3">
                    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 pb-2" style="border-bottom: 1px solid rgba(255,255,255,0.06);">
                        <div>
                            <div class="flex items-center gap-2">
                                <span class="text-sm font-bold text-white">Block B Architectural Vector Blueprint (G+4 // 7,500 m²)</span>
                                <span id="blueprintTimeTag" class="text-xs font-data font-bold px-2 py-0.5 rounded" style="background: #2B2D31; color: #FFC93C;">02:00 PM</span>
                            </div>
                            <p id="elevatorBannerText" class="text-xs font-data mt-0.5" style="color: #8E9297;">
                                Baseline View: All 4 Lifts Running | Random Unmanaged Room Lights ON
                            </p>
                        </div>
                        <!-- Legend -->
                        <div class="flex flex-wrap items-center gap-3 text-[11px] font-medium" style="color: #D9DAD0;">
                            <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-full inline-block" style="background: #FFC93C;"></span> Light ON</span>
                            <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-full inline-block" style="background: #1E2024; border: 1px solid #4F545C;"></span> Light OFF</span>
                            <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded inline-block" style="background: #353022; border: 1.5px solid #FFC93C;"></span> Active Zone</span>
                        </div>
                    </div>

                    <!-- SVG FLOOR PLAN -->
                    <div class="blueprint-wrap p-3 overflow-x-auto">
                        <svg viewBox="0 0 1120 860" class="w-full h-auto min-w-[780px]">

                            <!-- TOP WING HEADERS -->
                            <g>
                                <rect x="25" y="12" width="310" height="28" rx="5" fill="#27292E" stroke="#40444B" />
                                <text id="svgLeftWingHeader" x="180" y="30" fill="#FFC93C" font-family="Inter, sans-serif" font-size="11" font-weight="700" text-anchor="middle">
                                    LEFT WING (WEST) // 83 PEOPLE
                                </text>

                                <rect x="430" y="12" width="260" height="28" rx="5" fill="#FFC93C" />
                                <text x="560" y="30" fill="#2B2D31" font-family="Inter, sans-serif" font-size="11.5" font-weight="800" text-anchor="middle">
                                    JIT BLOCK B - FLOOR PLAN
                                </text>

                                <rect x="785" y="12" width="310" height="28" rx="5" fill="#27292E" stroke="#40444B" />
                                <text id="svgRightWingHeader" x="940" y="30" fill="#FFC93C" font-family="Inter, sans-serif" font-size="11" font-weight="700" text-anchor="middle">
                                    RIGHT WING (EAST) // 22 PEOPLE
                                </text>
                            </g>

                            <!-- NORTH MAIN STAIRCASE (CENTER TOP) -->
                            <g id="grp_main_stairs">
                                <rect id="box_main_stairs" x="490" y="55" width="140" height="135" rx="6" class="zone-box-on" />
                                <text x="560" y="80" fill="#FFFFFF" font-family="Inter, sans-serif" font-size="11.5" font-weight="700" text-anchor="middle">MAIN STAIRS</text>
                                <text id="status_main_stairs" x="560" y="96" fill="#FFC93C" font-family="Inter, sans-serif" font-size="9.5" font-weight="700" text-anchor="middle">LIGHTS: ON</text>
                                <!-- Stair Treads -->
                                <line x1="515" y1="112" x2="605" y2="112" stroke="#8E9297" stroke-width="1.5" />
                                <line x1="515" y1="124" x2="605" y2="124" stroke="#8E9297" stroke-width="1.5" />
                                <line x1="515" y1="136" x2="605" y2="136" stroke="#8E9297" stroke-width="1.5" />
                                <line x1="515" y1="148" x2="605" y2="148" stroke="#8E9297" stroke-width="1.5" />
                                <line x1="515" y1="160" x2="605" y2="160" stroke="#8E9297" stroke-width="1.5" />
                                <circle id="lum_main_stairs" cx="560" cy="175" r="5.5" class="luminaire lum-on" />
                            </g>

                            <!-- CORRIDOR LIGHTING ARCS (LEFT WING CORRIDOR vs RIGHT WING CORRIDOR) -->
                            <g>
                                <!-- Left Wing Corridor Path -->
                                <path id="corridor_left" d="M 350 210 L 245 210 L 245 685 L 350 685" class="corridor-line corridor-on" />
                                <text id="label_corridor_left" x="255" y="204" fill="#FFC93C" font-family="Inter, sans-serif" font-size="9.5" font-weight="700">LEFT CORRIDOR: ON</text>
                                <circle id="cl_lum1" cx="245" cy="280" r="5" class="luminaire lum-on" />
                                <circle id="cl_lum2" cx="245" cy="410" r="5" class="luminaire lum-on" />
                                <circle id="cl_lum3" cx="245" cy="540" r="5" class="luminaire lum-on" />
                                <circle id="cl_lum4" cx="245" cy="660" r="5" class="luminaire lum-on" />

                                <!-- Right Wing Corridor Path -->
                                <path id="corridor_right" d="M 770 210 L 875 210 L 875 685 L 770 685" class="corridor-line corridor-on" />
                                <text id="label_corridor_right" x="865" y="204" fill="#FFC93C" font-family="Inter, sans-serif" font-size="9.5" font-weight="700" text-anchor="end">RIGHT CORRIDOR: ON</text>
                                <circle id="cr_lum1" cx="875" cy="280" r="5" class="luminaire lum-on" />
                                <circle id="cr_lum2" cx="875" cy="410" r="5" class="luminaire lum-on" />
                                <circle id="cr_lum3" cx="875" cy="540" r="5" class="luminaire lum-on" />
                                <circle id="cr_lum4" cx="875" cy="660" r="5" class="luminaire lum-on" />
                            </g>

                            <!-- LEFT ELEVATOR BANK (LIFT 1 & LIFT 2 + RESTROOMS) -->
                            <g transform="translate(270, 290)">
                                <rect x="0" y="0" width="115" height="295" rx="6" fill="#232529" stroke="#40444B" stroke-width="1.5" />
                                <text x="57" y="20" fill="#FFFFFF" font-family="Inter, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle">LEFT LIFTS</text>

                                <!-- LIFT 1 -->
                                <rect id="lift_box_L1" x="10" y="30" width="44" height="62" rx="4" class="lift-car-on" />
                                <text x="32" y="56" fill="#FFFFFF" font-family="Inter, sans-serif" font-size="11" font-weight="700" text-anchor="middle">L-1</text>
                                <text id="lift_txt_L1" x="32" y="76" fill="#FFC93C" font-family="Inter, sans-serif" font-size="9" font-weight="700" text-anchor="middle">ON</text>

                                <!-- LIFT 2 -->
                                <rect id="lift_box_L2" x="61" y="30" width="44" height="62" rx="4" class="lift-car-on" />
                                <text x="83" y="56" fill="#FFFFFF" font-family="Inter, sans-serif" font-size="11" font-weight="700" text-anchor="middle">L-2</text>
                                <text id="lift_txt_L2" x="83" y="76" fill="#FFC93C" font-family="Inter, sans-serif" font-size="9" font-weight="700" text-anchor="middle">ON</text>

                                <!-- Left Bank Status Pill -->
                                <rect x="10" y="100" width="95" height="22" rx="4" fill="#1E2024" />
                                <text id="left_bank_badge" x="57" y="115" fill="#FFC93C" font-family="Inter, sans-serif" font-size="9" font-weight="700" text-anchor="middle">2 ACTIVE</text>

                                <!-- Restrooms (Left) -->
                                <rect x="10" y="135" width="95" height="68" rx="4" fill="#1E2024" stroke="#36393F" />
                                <text x="57" y="165" fill="#D9DAD0" font-family="Inter, sans-serif" font-size="10" font-weight="600" text-anchor="middle">Toilet (M)</text>
                                <text x="57" y="182" fill="#8E9297" font-family="Inter, sans-serif" font-size="8.5" text-anchor="middle">Exhaust Sensor</text>

                                <rect x="10" y="212" width="95" height="68" rx="4" fill="#1E2024" stroke="#36393F" />
                                <text x="57" y="242" fill="#D9DAD0" font-family="Inter, sans-serif" font-size="10" font-weight="600" text-anchor="middle">Toilet (F)</text>
                                <text x="57" y="259" fill="#8E9297" font-family="Inter, sans-serif" font-size="8.5" text-anchor="middle">Exhaust Sensor</text>
                            </g>

                            <!-- CENTRAL CIRCULAR ATRIUM -->
                            <g>
                                <circle cx="560" cy="440" r="145" fill="#1A1C20" stroke="#40444B" stroke-width="2" />
                                <circle cx="560" cy="440" r="110" fill="#1E2024" stroke="#36393F" stroke-width="1.5" stroke-dasharray="6 4" />
                                <circle cx="560" cy="440" r="70" fill="#16181B" stroke="#FFC93C" stroke-width="1.2" opacity="0.85" />
                                <line x1="450" y1="440" x2="670" y2="440" stroke="#2E3136" stroke-width="1" />
                                <line x1="560" y1="330" x2="560" y2="550" stroke="#2E3136" stroke-width="1" />
                                <text x="560" y="432" fill="#FFFFFF" font-family="Inter, sans-serif" font-size="13" font-weight="700" text-anchor="middle">CENTRAL ATRIUM</text>
                                <text x="560" y="450" fill="#8E9297" font-family="Inter, sans-serif" font-size="9.5" text-anchor="middle">Open to Sky // Natural Lux</text>
                                <text id="atriumRelocArrow" x="560" y="472" fill="#FFC93C" font-family="Inter, sans-serif" font-size="10" font-weight="700" text-anchor="middle"></text>
                            </g>

                            <!-- RIGHT ELEVATOR BANK (LIFT 3 & LIFT 4 + RESTROOMS) -->
                            <g transform="translate(735, 290)">
                                <rect x="0" y="0" width="115" height="295" rx="6" fill="#232529" stroke="#40444B" stroke-width="1.5" />
                                <text x="57" y="20" fill="#FFFFFF" font-family="Inter, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle">RIGHT LIFTS</text>

                                <!-- LIFT 3 -->
                                <rect id="lift_box_L3" x="10" y="30" width="44" height="62" rx="4" class="lift-car-on" />
                                <text x="32" y="56" fill="#FFFFFF" font-family="Inter, sans-serif" font-size="11" font-weight="700" text-anchor="middle">L-3</text>
                                <text id="lift_txt_L3" x="32" y="76" fill="#FFC93C" font-family="Inter, sans-serif" font-size="9" font-weight="700" text-anchor="middle">ON</text>

                                <!-- LIFT 4 -->
                                <rect id="lift_box_L4" x="61" y="30" width="44" height="62" rx="4" class="lift-car-on" />
                                <text x="83" y="56" fill="#FFFFFF" font-family="Inter, sans-serif" font-size="11" font-weight="700" text-anchor="middle">L-4</text>
                                <text id="lift_txt_L4" x="83" y="76" fill="#FFC93C" font-family="Inter, sans-serif" font-size="9" font-weight="700" text-anchor="middle">ON</text>

                                <!-- Right Bank Status Pill -->
                                <rect x="10" y="100" width="95" height="22" rx="4" fill="#1E2024" />
                                <text id="right_bank_badge" x="57" y="115" fill="#FFC93C" font-family="Inter, sans-serif" font-size="9" font-weight="700" text-anchor="middle">2 ACTIVE</text>

                                <!-- Restrooms (Right) -->
                                <rect x="10" y="135" width="95" height="68" rx="4" fill="#1E2024" stroke="#36393F" />
                                <text x="57" y="165" fill="#D9DAD0" font-family="Inter, sans-serif" font-size="10" font-weight="600" text-anchor="middle">Toilet (M)</text>
                                <text x="57" y="182" fill="#8E9297" font-family="Inter, sans-serif" font-size="8.5" text-anchor="middle">Exhaust Sensor</text>

                                <rect x="10" y="212" width="95" height="68" rx="4" fill="#1E2024" stroke="#36393F" />
                                <text x="57" y="242" fill="#D9DAD0" font-family="Inter, sans-serif" font-size="10" font-weight="600" text-anchor="middle">Toilet (F)</text>
                                <text x="57" y="259" fill="#8E9297" font-family="Inter, sans-serif" font-size="8.5" text-anchor="middle">Exhaust Sensor</text>
                            </g>

                            <!-- ALL 8 CLASSROOMS + 3 LABS (PRECISION GENERATED) -->
                            {all_svg_rooms_str}

                            <!-- SOUTH WING: SW STAIRS, FACULTY LOUNGE, SEMINAR HALL, SE STAIRS -->
                            <!-- SW STAIRS -->
                            <g id="grp_sw_stairs">
                                <rect id="box_sw_stairs" x="95" y="775" width="130" height="65" rx="6" class="zone-box-on" />
                                <text x="160" y="800" fill="#FFFFFF" font-family="Inter, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle">STAIRS SW</text>
                                <text id="status_sw_stairs" x="160" y="818" fill="#FFC93C" font-family="Inter, sans-serif" font-size="9" font-weight="700" text-anchor="middle">LIGHTS: ON</text>
                                <circle id="lum_sw_stairs" cx="115" cy="805" r="5" class="luminaire lum-on" />
                            </g>

                            <!-- FACULTY LOUNGE (80 m²) -->
                            <g id="grp_faculty_lounge">
                                <rect id="box_faculty_lounge" x="235" y="705" width="185" height="135" rx="6" class="zone-box-on" />
                                <rect x="236" y="706" width="183" height="26" rx="5" fill="#1E2024" opacity="0.85" />
                                <text x="246" y="723" fill="#FFFFFF" font-family="Inter, sans-serif" font-size="11" font-weight="700">Faculty Lounge</text>
                                <text id="status_faculty_lounge" x="410" y="723" fill="#FFC93C" font-family="Inter, sans-serif" font-size="9.5" font-weight="700" text-anchor="end">ON</text>
                                <text x="246" y="744" fill="#8E9297" font-family="Inter, sans-serif" font-size="9.5">Staff Seating (80 m²)</text>
                                <circle id="lum1_faculty" cx="295" cy="765" r="5.5" class="luminaire lum-on" />
                                <circle id="lum2_faculty" cx="360" cy="765" r="5.5" class="luminaire lum-on" />
                                <rect x="275" y="782" width="105" height="16" rx="3" class="desk-box desk-on" id="desk_faculty" />
                                <text id="ac_faculty" x="327" y="825" fill="#FFC93C" font-family="Inter, sans-serif" font-size="9.5" font-weight="600" text-anchor="middle">AC: 25°C (Daytime)</text>
                            </g>

                            <!-- SEMINAR HALL (180 m²) -->
                            <g id="grp_seminar_hall">
                                <rect x="430" y="705" width="245" height="135" rx="6" class="zone-box-off" />
                                <rect x="431" y="706" width="243" height="26" rx="5" fill="#1E2024" opacity="0.85" />
                                <text x="442" y="723" fill="#FFFFFF" font-family="Inter, sans-serif" font-size="11" font-weight="700">Seminar Hall (180 m²)</text>
                                <text x="664" y="723" fill="#8E9297" font-family="Inter, sans-serif" font-size="9.5" font-weight="700" text-anchor="end">STANDBY</text>
                                <text x="552" y="758" fill="#8E9297" font-family="Inter, sans-serif" font-size="10" text-anchor="middle">120-Seat Auditorium // Event Interlock</text>
                                <rect x="470" y="772" width="165" height="10" rx="2" fill="#2E3136" />
                                <rect x="480" y="790" width="145" height="10" rx="2" fill="#2E3136" />
                                <text x="552" y="825" fill="#8E9297" font-family="Inter, sans-serif" font-size="9.5" text-anchor="middle">Circuit Isolated (0.0 kW)</text>
                            </g>

                            <!-- SE STAIRS -->
                            <g id="grp_se_stairs">
                                <rect id="box_se_stairs" x="895" y="775" width="130" height="65" rx="6" class="zone-box-on" />
                                <text x="960" y="800" fill="#FFFFFF" font-family="Inter, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle">STAIRS SE</text>
                                <text id="status_se_stairs" x="960" y="818" fill="#FFC93C" font-family="Inter, sans-serif" font-size="9" font-weight="700" text-anchor="middle">LIGHTS: ON</text>
                                <circle id="lum_se_stairs" cx="915" cy="805" r="5" class="luminaire lum-on" />
                            </g>

                        </svg>
                    </div>
                </div>

                <!-- 4. SESSION SUGGESTIONS LOG (BY TIME) -->
                <div class="card p-5">
                    <div class="flex items-center justify-between mb-3">
                        <div>
                            <h3 class="text-sm font-bold text-white">Session Suggestions Log (By Time)</h3>
                            <p class="text-xs" style="color: #8E9297;">Chronological log of spatial relocations, wing shutdowns, and Block C sunlight harvesting advisories</p>
                        </div>
                        <span class="text-xs font-data px-2.5 py-1 rounded" style="background: #2B2D31; color: #FFC93C;">Synced with Dashboard</span>
                    </div>
                    <div id="sandboxSuggestionsLog" class="space-y-2.5 max-h-[320px] overflow-y-auto pr-1"></div>
                </div>

            </div>
        </div>
    </main>

    <!-- JAVASCRIPT SIMULATION & UI CONTROLLER -->
    <script>
        const LEFT_ROOMS = [
            {{ id: 'B101', label: 'CR B-101', cap: 60 }},
            {{ id: 'B102', label: 'CR B-102', cap: 60 }},
            {{ id: 'B103', label: 'CR B-103', cap: 60 }},
            {{ id: 'B104', label: 'CR B-104', cap: 60 }},
            {{ id: 'LAB1', label: 'Lab B-1 (HW)', cap: 45 }}
        ];
        const RIGHT_ROOMS = [
            {{ id: 'B105', label: 'CR B-105', cap: 60 }},
            {{ id: 'B106', label: 'CR B-106', cap: 60 }},
            {{ id: 'B107', label: 'CR B-107', cap: 60 }},
            {{ id: 'B108', label: 'CR B-108', cap: 60 }},
            {{ id: 'LAB2', label: 'Lab B-2 (Comm)', cap: 45 }},
            {{ id: 'LAB3', label: 'Comp Lab B-3', cap: 50 }}
        ];
        const ALL_ROOMS = [...LEFT_ROOMS, ...RIGHT_ROOMS];

        // State for each room: {{ active: bool, count: int }}
        const roomState = {{
            B101: {{ active: true, count: 30 }},
            B102: {{ active: true, count: 28 }},
            B103: {{ active: true, count: 25 }},
            B104: {{ active: false, count: 25 }},
            LAB1: {{ active: false, count: 25 }},
            B105: {{ active: false, count: 25 }},
            B106: {{ active: false, count: 25 }},
            B107: {{ active: false, count: 25 }},
            B108: {{ active: true, count: 22 }},
            LAB2: {{ active: false, count: 25 }},
            LAB3: {{ active: false, count: 30 }}
        }};

        let currentMode = 'variable';
        let latestEvalData = null;
        let timetableSchedule = [];
        let selectedTimetableIdx = 0;

        function formatFloatTo12h(val) {{
            const totalMins = Math.round(parseFloat(val) * 60);
            const h24 = Math.floor(totalMins / 60) % 24;
            const mins = totalMins % 60;
            const period = h24 >= 12 ? 'PM' : 'AM';
            let h12 = h24 % 12;
            if (h12 === 0) h12 = 12;
            const hStr = h12 < 10 ? '0' + h12 : '' + h12;
            const mStr = mins < 10 ? '0' + mins : '' + mins;
            return `${{hStr}}:${{mStr}} ${{period}}`;
        }}

        function buildRoomControlRow(rm) {{
            const st = roomState[rm.id];
            return `
            <div class="sub-box p-2.5">
                <div class="flex items-center justify-between">
                    <div class="flex items-center gap-2">
                        <button id="toggle_${{rm.id}}" onclick="toggleRoomActive('${{rm.id}}')"
                            class="px-2.5 py-1 rounded text-[11px] font-data font-bold transition-all"
                            style="${{st.active ? 'background: #FFC93C; color: #2B2D31;' : 'background: #36393F; color: #8E9297;'}}">
                            ${{st.active ? 'ON' : 'OFF'}}
                        </button>
                        <span class="text-xs font-semibold text-white">${{rm.label}}</span>
                    </div>
                    <span id="lbl_count_${{rm.id}}" class="text-xs font-data font-bold" style="color: ${{st.active ? '#FFC93C' : '#8E9297'}};">
                        ${{st.active ? st.count + ' People' : 'Vacant'}}
                    </span>
                </div>
                <div id="slider_wrap_${{rm.id}}" class="mt-2 pt-1.5" style="display: ${{st.active ? 'block' : 'none'}}; border-top: 1px solid rgba(255,255,255,0.05);">
                    <div class="flex items-center gap-2">
                        <span class="text-[10px] font-data" style="color: #8E9297;">People:</span>
                        <input type="range" id="slider_${{rm.id}}" min="5" max="${{rm.cap}}" value="${{st.count}}"
                            oninput="onRoomSliderInput('${{rm.id}}', this.value)" class="flex-1">
                    </div>
                </div>
            </div>`;
        }}

        function renderVariableControls() {{
            document.getElementById('leftWingControls').innerHTML = LEFT_ROOMS.map(buildRoomControlRow).join('');
            document.getElementById('rightWingControls').innerHTML = RIGHT_ROOMS.map(buildRoomControlRow).join('');
            updateWingSummaryCounters();
        }}

        function toggleRoomActive(rid) {{
            roomState[rid].active = !roomState[rid].active;
            if (roomState[rid].active && roomState[rid].count <= 0) {{
                roomState[rid].count = 25;
            }}
            renderVariableControls();
            fetchPreviewEvaluation();
        }}

        function onRoomSliderInput(rid, val) {{
            roomState[rid].count = parseInt(val, 10) || 0;
            const lbl = document.getElementById(`lbl_count_${{rid}}`);
            if (lbl) lbl.innerText = `${{roomState[rid].count}} People`;
            updateWingSummaryCounters();
            fetchPreviewEvaluation();
        }}

        function updateWingSummaryCounters() {{
            let activeCount = 0;
            let leftPop = 0;
            let rightPop = 0;
            LEFT_ROOMS.forEach(r => {{
                if (roomState[r.id].active) {{
                    activeCount++;
                    leftPop += roomState[r.id].count;
                }}
            }});
            RIGHT_ROOMS.forEach(r => {{
                if (roomState[r.id].active) {{
                    activeCount++;
                    rightPop += roomState[r.id].count;
                }}
            }});
            document.getElementById('summaryActiveCount').innerText = activeCount;
            document.getElementById('summaryLeftPop').innerText = `${{leftPop}}p`;
            document.getElementById('summaryRightPop').innerText = `${{rightPop}}p`;
        }}

        function onVariableInputChanged() {{
            const timeVal = parseFloat(document.getElementById('timeSlider').value);
            const time12h = formatFloatTo12h(timeVal);
            document.getElementById('timeDisplay12h').innerText = time12h;
            document.getElementById('blueprintTimeTag').innerText = time12h;

            const temp = document.getElementById('tempSlider').value;
            document.getElementById('tempDisplay').innerText = `${{temp}}°C`;

            // Automatically sync sky condition if night hours
            const weatherSel = document.getElementById('weatherSelect');
            if (timeVal >= 18.0 || timeVal < 6.5) {{
                weatherSel.value = 'Night';
            }} else if (weatherSel.value === 'Night') {{
                weatherSel.value = 'Sunny / Daylight';
            }}

            const isDay = (timeVal >= 7.0 && timeVal <= 17.5 && weatherSel.value !== 'Night');
            const badge = document.getElementById('daylightBadge');
            badge.innerText = isDay ? 'Daylight Window' : 'Night / Off-Peak';
            badge.style.color = isDay ? '#FFC93C' : '#8E9297';

            fetchPreviewEvaluation();
        }}

        function buildPayload(isSimulate) {{
            const timeVal = parseFloat(document.getElementById('timeSlider').value);
            const time12h = formatFloatTo12h(timeVal);
            const temp = parseFloat(document.getElementById('tempSlider').value);
            const weather = document.getElementById('weatherSelect').value;

            const roomsPayload = {{}};
            ALL_ROOMS.forEach(r => {{
                roomsPayload[r.id] = roomState[r.id].active ? roomState[r.id].count : 0;
            }});

            return {{
                time: time12h,
                temperature: temp,
                weather: weather,
                rooms: roomsPayload,
                simulate: isSimulate,
                mode: currentMode === 'timetable' ? 'Set Timetable Mode' : 'Variable Mode'
            }};
        }}

        // Fetch evaluation and show UNMANAGED BASELINE first (or Simulated if in Set Timetable Mode / Simulate clicked)
        function fetchPreviewEvaluation() {{
            const payload = buildPayload(false);
            fetch('/api/sandbox/evaluate', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify(payload)
            }})
            .then(res => res.json())
            .then(data => {{
                latestEvalData = data;
                if (currentMode === 'timetable') {{
                    // In Set Timetable Mode, immediately show active scheduled rooms & stairs
                    renderFloorPlanState(data, 'simulated', false);
                }} else {{
                    // In Variable Mode, show realistic Unmanaged Baseline until user clicks Simulate
                    renderFloorPlanState(data, 'baseline', false);
                }}
            }})
            .catch(err => console.error(err));
        }}

        function showBaselinePreview() {{
            if (!latestEvalData) {{
                fetchPreviewEvaluation();
                return;
            }}
            renderFloorPlanState(latestEvalData, 'baseline', false);
        }}

        function runSimulation() {{
            const payload = buildPayload(true);
            const statusEl = document.getElementById('autoPingStatus');
            statusEl.innerText = 'Running Python optimization engine...';
            statusEl.style.color = '#FFC93C';

            fetch('/api/sandbox/evaluate', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify(payload)
            }})
            .then(res => res.json())
            .then(data => {{
                latestEvalData = data;
                renderFloorPlanState(data, 'simulated', true);
                loadSuggestionsLog();
                statusEl.innerText = `Simulation Complete (${{data.time_12h}}) // Logged to Session Suggestions & Dashboard`;
                statusEl.style.color = '#FFC93C';
            }})
            .catch(err => {{
                console.error(err);
                statusEl.innerText = 'Simulation evaluated locally.';
            }});
        }}

        function renderFloorPlanState(data, whichState, showFullReport) {{
            const isSim = (whichState === 'simulated');
            const stateObj = isSim ? data.simulated_state : data.baseline_state;
            const roomsMap = stateObj.rooms;
            const common = stateObj.common;

            // Update View Badge
            const viewBadge = document.getElementById('viewStateBadge');
            if (isSim) {{
                viewBadge.innerText = 'SIMULATED & OPTIMIZED';
                viewBadge.style.background = 'rgba(255,201,60,0.18)';
                viewBadge.style.color = '#FFC93C';
            }} else {{
                viewBadge.innerText = 'UNMANAGED BASELINE';
                viewBadge.style.background = 'rgba(245,158,11,0.15)';
                viewBadge.style.color = '#F59E0B';
            }}

            // Top KPI Meters
            document.getElementById('meterBaseline').innerText = `${{data.total_baseline_kw}} kW`;
            if (isSim) {{
                document.getElementById('meterOptimized').innerText = `${{data.total_optimized_kw}} kW`;
                document.getElementById('meterOptimized').style.color = '#FFC93C';
                document.getElementById('meterLiftSub').innerText = data.elevator_mode;
                document.getElementById('meterSavings').innerText = `${{data.kw_saved}} kW (${{data.savings_percentage}}%)`;
                document.getElementById('meterSavings').style.color = '#FFC93C';
                document.getElementById('meterInr').innerText = `INR ${{data.inr_per_hour_saved}} / Hr Saved`;
                document.getElementById('meterInr').style.color = '#D9DAD0';
            }} else {{
                document.getElementById('meterOptimized').innerText = 'Click Simulate';
                document.getElementById('meterOptimized').style.color = '#8E9297';
                document.getElementById('meterLiftSub').innerText = 'Baseline has all 4 lifts & corridors ON';
                document.getElementById('meterSavings').innerText = 'Ready';
                document.getElementById('meterSavings').style.color = '#8E9297';
                document.getElementById('meterInr').innerText = 'Press Simulate to view savings';
                document.getElementById('meterInr').style.color = '#8E9297';
            }}

            // Wing Headers in SVG
            document.getElementById('svgLeftWingHeader').innerText = `LEFT WING (WEST) // ${{data.left_wing_people}} PEOPLE`;
            document.getElementById('svgRightWingHeader').innerText = `RIGHT WING (EAST) // ${{data.right_wing_people}} PEOPLE`;
            document.getElementById('blueprintTimeTag').innerText = data.time_12h;

            document.getElementById('elevatorBannerText').innerText = isSim
                ? `Simulated State (${{data.time_12h}}): ${{data.elevator_mode}}`
                : `Unmanaged Baseline (${{data.time_12h}}): All 4 Lifts Running | Vacant Rooms Wasting Power`;

            // Center Atrium Relocation Indicator
            const relocArrow = document.getElementById('atriumRelocArrow');
            if (isSim && data.relocations && data.relocations.length > 0) {{
                const r0 = data.relocations[0];
                relocArrow.textContent = `RELOCATED: ${{r0.from_label}} -> ${{r0.to_label}}`;
            }} else {{
                relocArrow.textContent = '';
            }}

            // Render each of the 11 Rooms
            ALL_ROOMS.forEach(rm => {{
                const rid = rm.id;
                const rData = roomsMap[rid];
                if (!rData) return;

                const poly = document.getElementById(`poly_${{rid}}`);
                const occBadge = document.getElementById(`occ_badge_${{rid}}`);
                const subBadge = document.getElementById(`sub_badge_${{rid}}`);
                const acText = document.getElementById(`ac_${{rid}}`);
                const kwText = document.getElementById(`kw_${{rid}}`);

                // Box styling
                if (rData.is_occupied) {{
                    poly.setAttribute('class', 'room-box room-lit');
                    occBadge.textContent = `${{rData.occupancy}} PPL`;
                    occBadge.setAttribute('fill', '#FFC93C');
                }} else if (rData.relocated_to) {{
                    poly.setAttribute('class', 'room-box room-relocated');
                    occBadge.textContent = `MOVED -> ${{rData.relocated_to}}`;
                    occBadge.setAttribute('fill', '#38BDF8');
                }} else if (!isSim && rData.lights_on_count > 0) {{
                    poly.setAttribute('class', 'room-box room-wasted');
                    occBadge.textContent = `VACANT (${{rData.lights_on_count}}/4 LIT)`;
                    occBadge.setAttribute('fill', '#F59E0B');
                }} else {{
                    poly.setAttribute('class', 'room-box room-unlit');
                    occBadge.textContent = 'VACANT (OFF)';
                    occBadge.setAttribute('fill', '#8E9297');
                }}

                // Relocation subtitle note
                if (isSim && rData.relocated_from) {{
                    subBadge.textContent = `Consolidated from ${{rData.relocated_from}}`;
                    subBadge.setAttribute('fill', '#FFC93C');
                }} else if (isSim && rData.relocated_to) {{
                    subBadge.textContent = `Relocated to ${{rData.relocated_to}} (Wing Shutoff)`;
                    subBadge.setAttribute('fill', '#38BDF8');
                }} else {{
                    subBadge.textContent = `${{rData.wing}} Wing // ${{rData.lights_on_count}}/4 Lights ON`;
                    subBadge.setAttribute('fill', '#8E9297');
                }}

                // 4 Individual Luminaires
                for (let idx = 0; idx < 4; idx++) {{
                    const lumEl = document.getElementById(`l${{idx+1}}_${{rid}}`);
                    if (lumEl) {{
                        const isOn = rData.lights[idx];
                        lumEl.setAttribute('class', isOn ? 'luminaire lum-on' : 'luminaire lum-off');
                    }}
                }}

                // 4 Desks
                for (let d = 1; d <= 4; d++) {{
                    const deskEl = document.getElementById(`d${{d}}_${{rid}}`);
                    if (deskEl) {{
                        deskEl.setAttribute('class', rData.is_occupied ? 'desk-box desk-on' : 'desk-box desk-off');
                    }}
                }}

                // AC & kW Readout
                acText.textContent = `AC: ${{rData.ac_setpoint}}`;
                acText.setAttribute('fill', rData.ac_setpoint === 'OFF' ? '#8E9297' : '#FFC93C');
                kwText.textContent = `${{rData.kw}} kW`;
                kwText.setAttribute('fill', rData.is_occupied ? '#FFFFFF' : '#8E9297');
            }});

            // Render 4 Lifts (L1, L2 in Left Wing; L3, L4 in Right Wing)
            ['L1', 'L2', 'L3', 'L4'].forEach(lid => {{
                const isOn = common.lifts[lid];
                const box = document.getElementById(`lift_box_${{lid}}`);
                const txt = document.getElementById(`lift_txt_${{lid}}`);
                if (box) box.setAttribute('class', isOn ? 'lift-car-on' : 'lift-car-off');
                if (txt) {{
                    txt.textContent = isOn ? 'ON' : 'OFF';
                    txt.setAttribute('fill', isOn ? '#FFC93C' : '#8E9297');
                }}
            }});

            const leftLiftsCount = (common.lifts.L1 ? 1 : 0) + (common.lifts.L2 ? 1 : 0);
            const rightLiftsCount = (common.lifts.L3 ? 1 : 0) + (common.lifts.L4 ? 1 : 0);
            const lbBadge = document.getElementById('left_bank_badge');
            const rbBadge = document.getElementById('right_bank_badge');
            lbBadge.textContent = `${{leftLiftsCount}}/2 ACTIVE`;
            lbBadge.setAttribute('fill', leftLiftsCount > 0 ? '#FFC93C' : '#8E9297');
            rbBadge.textContent = `${{rightLiftsCount}}/2 ACTIVE`;
            rbBadge.setAttribute('fill', rightLiftsCount > 0 ? '#FFC93C' : '#8E9297');

            // Corridors (Left & Right)
            const cLeft = document.getElementById('corridor_left');
            const cRight = document.getElementById('corridor_right');
            const lblLeft = document.getElementById('label_corridor_left');
            const lblRight = document.getElementById('label_corridor_right');

            cLeft.setAttribute('class', common.left_corridor ? 'corridor-line corridor-on' : 'corridor-line corridor-off');
            lblLeft.textContent = common.left_corridor ? 'LEFT CORRIDOR: ON' : 'LEFT CORRIDOR: OFF (ISOLATED)';
            lblLeft.setAttribute('fill', common.left_corridor ? '#FFC93C' : '#8E9297');

            cRight.setAttribute('class', common.right_corridor ? 'corridor-line corridor-on' : 'corridor-line corridor-off');
            lblRight.textContent = common.right_corridor ? 'RIGHT CORRIDOR: ON' : 'RIGHT CORRIDOR: OFF (ISOLATED)';
            lblRight.setAttribute('fill', common.right_corridor ? '#FFC93C' : '#8E9297');

            for (let i = 1; i <= 4; i++) {{
                document.getElementById(`cl_lum${{i}}`).setAttribute('class', common.left_corridor ? 'luminaire lum-on' : 'luminaire lum-off');
                document.getElementById(`cr_lum${{i}}`).setAttribute('class', common.right_corridor ? 'luminaire lum-on' : 'luminaire lum-off');
            }}

            // Stairs & Faculty Lounge
            const setZoneState = (boxId, statusId, lumId, isOn, onText, offText) => {{
                const bx = document.getElementById(boxId);
                const st = document.getElementById(statusId);
                const lm = document.getElementById(lumId);
                if (bx) bx.setAttribute('class', isOn ? 'zone-box-on' : 'zone-box-off');
                if (st) {{
                    st.textContent = isOn ? onText : offText;
                    st.setAttribute('fill', isOn ? '#FFC93C' : '#8E9297');
                }}
                if (lm) lm.setAttribute('class', isOn ? 'luminaire lum-on' : 'luminaire lum-off');
            }};

            setZoneState('box_main_stairs', 'status_main_stairs', 'lum_main_stairs', common.main_stairs, 'LIGHTS: ON', 'LIGHTS: OFF');
            setZoneState('box_sw_stairs', 'status_sw_stairs', 'lum_sw_stairs', common.sw_stairs, 'LIGHTS: ON', 'LIGHTS: OFF');
            setZoneState('box_se_stairs', 'status_se_stairs', 'lum_se_stairs', common.se_stairs, 'LIGHTS: ON', 'LIGHTS: OFF');
            setZoneState('box_faculty_lounge', 'status_faculty_lounge', 'lum1_faculty', common.faculty_lounge, 'ON', 'OFF');
            document.getElementById('lum2_faculty').setAttribute('class', common.faculty_lounge ? 'luminaire lum-on' : 'luminaire lum-off');
            document.getElementById('ac_faculty').textContent = common.faculty_lounge ? 'AC: 25°C (Active)' : 'AC: OFF (After-Hours)';
            document.getElementById('ac_faculty').setAttribute('fill', common.faculty_lounge ? '#FFC93C' : '#8E9297');

            // 3-Part Simulation Report Card
            const repCard = document.getElementById('simulationReportCard');
            if (showFullReport || (currentMode === 'timetable' && isSim)) {{
                repCard.style.display = 'block';
                document.getElementById('reportTimeHeader').innerText = `JIT Block B // ${{data.time_12h}} (${{data.temperature}}°C)`;
                document.getElementById('repPart1').innerText = data.report.suggestion;
                document.getElementById('repPart2').innerText = data.report.actions_taken;
                document.getElementById('repPart3').innerText = data.report.energy_saved;
            }} else {{
                repCard.style.display = 'none';
            }}
        }}

        // ================= MODE SWITCHING & TIMETABLE GENERATOR =================
        function switchMode(mode) {{
            currentMode = mode;
            document.getElementById('tabVariable').className = mode === 'variable' ? 'mode-tab active' : 'mode-tab';
            document.getElementById('tabTimetable').className = mode === 'timetable' ? 'mode-tab active' : 'mode-tab';
            document.getElementById('panelVariable').style.display = mode === 'variable' ? 'block' : 'none';
            document.getElementById('panelTimetable').style.display = mode === 'timetable' ? 'block' : 'none';

            if (mode === 'timetable') {{
                if (timetableSchedule.length === 0) {{
                    regenerateTimetable();
                }} else {{
                    selectTimetableSlot(selectedTimetableIdx);
                }}
            }} else {{
                fetchPreviewEvaluation();
            }}
        }}

        function regenerateTimetable() {{
            const seed = Math.floor(Math.random() * 10000);
            fetch(`/api/sandbox/timetable?seed=${{seed}}`)
                .then(res => res.json())
                .then(data => {{
                    timetableSchedule = data.schedule || [];
                    renderTimetableList();
                    selectTimetableSlot(0);
                }});
        }}

        function renderTimetableList() {{
            const container = document.getElementById('timetableSlotsList');
            container.innerHTML = timetableSchedule.map((slot, idx) => {{
                const isSelected = (idx === selectedTimetableIdx);
                return `
                <div onclick="selectTimetableSlot(${{idx}})" class="p-2.5 rounded-lg cursor-pointer transition-all"
                    style="background: ${{isSelected ? '#353022' : '#2B2D31'}}; border: 1px solid ${{isSelected ? '#FFC93C' : 'rgba(255,255,255,0.05)'}};">
                    <div class="flex items-center justify-between">
                        <span class="font-data font-bold text-xs" style="color: ${{isSelected ? '#FFC93C' : '#FFFFFF'}};">${{slot.time_12h}}</span>
                        <span class="font-data text-[11px] px-2 py-0.5 rounded" style="background: #36393F; color: #D9DAD0;">
                            ${{slot.active_count}} Classes // ${{slot.total_students}}p // ${{slot.temperature}}°C
                        </span>
                    </div>
                    <div class="text-[11px] mt-1 truncate" style="color: #8E9297;">${{slot.summary}}</div>
                </div>`;
            }}).join('');
        }}

        function selectTimetableSlot(idx) {{
            selectedTimetableIdx = idx;
            const slot = timetableSchedule[idx];
            if (!slot) return;

            document.getElementById('timeSlider').value = slot.time_float;
            document.getElementById('tempSlider').value = slot.temperature;
            document.getElementById('weatherSelect').value = slot.weather;
            document.getElementById('timeDisplay12h').innerText = slot.time_12h;
            document.getElementById('tempDisplay').innerText = `${{slot.temperature}}°C`;

            ALL_ROOMS.forEach(r => {{
                const occ = slot.rooms[r.id] || 0;
                roomState[r.id].active = occ > 0;
                roomState[r.id].count = occ > 0 ? occ : 25;
            }});

            renderVariableControls();
            renderTimetableList();
            fetchPreviewEvaluation();
        }}

        // ================= PRESET HELPERS & LOGS =================
        function loadDemoScenario(type) {{
            if (type === 'wing_consolidate') {{
                // 3 classes in Left Wing + 1 class in Right Wing
                document.getElementById('timeSlider').value = 14.0;
                document.getElementById('tempSlider').value = 33;
                document.getElementById('weatherSelect').value = 'Sunny / Daylight';
                ALL_ROOMS.forEach(r => {{ roomState[r.id].active = false; }});
                roomState.B101 = {{ active: true, count: 30 }};
                roomState.B102 = {{ active: true, count: 28 }};
                roomState.B103 = {{ active: true, count: 25 }};
                roomState.B108 = {{ active: true, count: 22 }};
                renderVariableControls();
                onVariableInputChanged();
            }}
        }}

        function clearAllRooms() {{
            ALL_ROOMS.forEach(r => {{ roomState[r.id].active = false; }});
            renderVariableControls();
            fetchPreviewEvaluation();
        }}

        function loadSuggestionsLog() {{
            fetch('/api/suggestions')
                .then(res => res.json())
                .then(data => {{
                    const list = data.suggestions || [];
                    const el = document.getElementById('sandboxSuggestionsLog');
                    el.innerHTML = list.map(item => `
                        <div class="p-3 rounded-lg text-xs" style="background: #2B2D31; border: 1px solid rgba(255,255,255,0.05);">
                            <div class="flex items-center justify-between mb-1.5">
                                <div class="flex items-center gap-2">
                                    <span class="px-2 py-0.5 rounded font-data font-bold text-[11px]" style="background: rgba(255,201,60,0.15); color: #FFC93C;">${{item.time_12h}}</span>
                                    <span class="font-semibold text-white">${{item.title}}</span>
                                </div>
                                <span class="text-[10px] font-data" style="color: #8E9297;">${{item.mode}}</span>
                            </div>
                            <div style="color: #D9DAD0;" class="mb-1"><b>Suggestion:</b> ${{item.suggestion}}</div>
                            <div style="color: #8E9297;" class="mb-1"><b>Actions:</b> ${{item.actions_taken}}</div>
                            <div class="font-data font-semibold" style="color: #FFC93C;">${{item.energy_saved}}</div>
                        </div>
                    `).join('');
                }});
        }}

        window.addEventListener('DOMContentLoaded', () => {{
            renderVariableControls();
            onVariableInputChanged();
            loadSuggestionsLog();
        }});
    </script>
</body>
</html>
"""
