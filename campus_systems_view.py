"""
GridSense Campus Systems View
Covers Campus-Wide Total ROI & CO2 Calculator + Interactive Modules (RO Plant, WiFi APs, Hostel Geysers, Water Coolers, Lab PCs)
plus a visual "How GridSense Works" System Flowchart tab.
Color Scheme: #2B2D31 (bg), #36393F (cards), #D9DAD0 (silver), #FFC93C (yellow accent).
"""


def render_campus_systems_html() -> str:
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GridSense // Campus Systems</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        body {
            background-color: #2B2D31;
            color: #D9DAD0;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            margin: 0;
        }
        .font-data { font-family: 'JetBrains Mono', monospace; }
        .card {
            background-color: #36393F;
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 14px;
        }
        .nav-link {
            color: #8E9297;
            font-weight: 500;
            font-size: 14px;
            padding: 8px 0;
            border-bottom: 2px solid transparent;
            transition: all 0.15s ease;
        }
        .nav-link:hover { color: #FFFFFF; }
        .nav-link.active { color: #FFFFFF; border-bottom-color: #FFC93C; }
        input[type="range"] {
            accent-color: #FFC93C;
            cursor: pointer;
        }
        .tab-btn {
            padding: 8px 18px;
            border-radius: 9px;
            font-size: 13px;
            font-weight: 600;
            transition: all 0.15s ease;
            border: 1px solid rgba(255, 255, 255, 0.08);
        }
        .tab-btn.active {
            background-color: #FFC93C;
            color: #2B2D31;
            border-color: #FFC93C;
        }
        .tab-btn:not(.active) {
            background-color: #2B2D31;
            color: #D9DAD0;
        }
        .toggle-pill {
            padding: 4px 12px;
            border-radius: 999px;
            font-size: 11px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.15s ease;
        }
        .toggle-pill.on {
            background-color: #FFC93C;
            color: #2B2D31;
        }
        .toggle-pill.off {
            background-color: #2B2D31;
            color: #8E9297;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
    </style>
</head>
<body class="min-h-screen flex flex-col">

    <!-- TOP NAVIGATION -->
    <header class="w-full" style="background-color: #2B2D31; border-bottom: 1px solid rgba(255,255,255,0.06);">
        <div class="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
            <div class="flex items-center gap-3">
                <div class="w-8 h-8 rounded-lg flex items-center justify-center font-bold text-sm" style="background-color: #FFC93C; color: #2B2D31;">
                    GS
                </div>
                <span class="text-lg font-bold text-white tracking-tight">GridSense</span>
            </div>

            <nav class="flex items-center gap-8">
                <a href="/" class="nav-link">Dashboard</a>
                <a href="/sandbox" class="nav-link">Sandbox</a>
                <a href="/systems" class="nav-link active">Campus Systems</a>
                <a href="/blueprint" class="nav-link">Blueprint</a>
            </nav>
        </div>
    </header>

    <main class="flex-1 w-full max-w-7xl mx-auto px-6 py-8 space-y-6">

        <!-- PAGE HEADER + TAB SWITCHER -->
        <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
            <div>
                <h1 class="text-2xl font-bold text-white tracking-tight">Campus Systems &amp; Total Impact</h1>
                <p class="text-sm mt-1" style="color: #8E9297;">
                    Campus-wide automation beyond Block B: RO Plant, WiFi APs, Hostel Geysers, Water Coolers, and Computer Labs.
                </p>
            </div>
            <div class="flex items-center gap-2">
                <button id="btnTabSimulator" onclick="switchSystemsTab('simulator')" class="tab-btn active">
                    Systems &amp; ROI Calculator
                </button>
                <button id="btnTabExplainer" onclick="switchSystemsTab('explainer')" class="tab-btn">
                    How GridSense Works
                </button>
            </div>
        </div>

        <!-- =============================================================== -->
        <!-- TAB 1: CAMPUS SYSTEMS SIMULATOR + TOTAL ROI & CO2 CALCULATOR    -->
        <!-- =============================================================== -->
        <div id="tabSimulator" class="space-y-6">

            <!-- CAMPUS-WIDE TOTAL ROI & CO2 CALCULATOR -->
            <div class="card p-6">
                <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-2 mb-5">
                    <div>
                        <div class="text-xs font-semibold uppercase tracking-wider" style="color: #FFC93C;">
                            Campus-Wide Total ROI &amp; Carbon Calculator
                        </div>
                        <h2 class="text-lg font-bold text-white mt-0.5">
                            Combined Savings (Block B Sandbox + Active Campus Systems)
                        </h2>
                    </div>
                    <div class="flex items-center gap-2">
                        <label class="text-xs" style="color: #8E9297;">Tariff (INR/kWh):</label>
                        <input id="tariffInput" type="number" value="9" min="4" max="20" step="0.5" oninput="recalcCampusROI()"
                            class="w-16 px-2 py-1 rounded text-xs font-data text-white outline-none"
                            style="background: #2B2D31; border: 1px solid rgba(255,255,255,0.1);">
                    </div>
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                    <div class="p-4 rounded-xl" style="background: #2B2D31; border: 1px solid rgba(255,255,255,0.06);">
                        <div class="text-[11px] font-semibold uppercase tracking-wider" style="color: #8E9297;">Monthly Energy Saved</div>
                        <div id="kpiMonthlyKwh" class="text-2xl font-bold font-data text-white mt-1">15,000 kWh</div>
                        <div class="text-[11px] mt-1" style="color: #8E9297;">Includes 7,660 kWh from Block B (A, B, D)</div>
                    </div>

                    <div class="p-4 rounded-xl" style="background: #2B2D31; border: 1px solid rgba(255,201,60,0.3);">
                        <div class="text-[11px] font-semibold uppercase tracking-wider" style="color: #FFC93C;">Monthly Cost Savings</div>
                        <div id="kpiMonthlyInr" class="text-2xl font-bold font-data mt-1" style="color: #FFC93C;">INR 1,35,000</div>
                        <div id="kpiAnnualInr" class="text-[11px] font-data mt-1" style="color: #D9DAD0;">INR 16,20,000 / year projected</div>
                    </div>

                    <div class="p-4 rounded-xl" style="background: #2B2D31; border: 1px solid rgba(255,255,255,0.06);">
                        <div class="text-[11px] font-semibold uppercase tracking-wider" style="color: #8E9297;">CO2 Avoided Annually</div>
                        <div id="kpiCo2Tons" class="text-2xl font-bold font-data text-white mt-1">147.6 Tons</div>
                        <div class="text-[11px] mt-1" style="color: #8E9297;">CEA India grid factor: 0.82 kg CO2/kWh</div>
                    </div>

                    <div class="p-4 rounded-xl" style="background: #2B2D31; border: 1px solid rgba(255,255,255,0.06);">
                        <div class="text-[11px] font-semibold uppercase tracking-wider" style="color: #8E9297;">Active Modules &amp; Payback</div>
                        <div id="kpiActiveModules" class="text-2xl font-bold font-data text-white mt-1">5 / 5 Active</div>
                        <div class="text-[11px] mt-1" style="color: #FFC93C;">Hardware ROI: 4 to 6 months</div>
                    </div>
                </div>
            </div>

            <!-- 5 INTERACTIVE CAMPUS SYSTEM CARDS -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-5">

                <!-- 1. CENTRAL RO PLANT & STP LOAD SHIFTING (MODULE G) -->
                <div class="card p-5 space-y-4">
                    <div class="flex items-start justify-between gap-3">
                        <div>
                            <div class="text-[11px] font-semibold uppercase tracking-wider" style="color: #FFC93C;">Module G // Heavy Infrastructure</div>
                            <h3 class="text-base font-bold text-white mt-0.5">Central RO Plant &amp; STP Load Shifting</h3>
                            <p class="text-xs mt-1" style="color: #8E9297;">
                                Locks out high-draw RO &amp; STP motors during peak tariff (06:00 PM - 10:00 PM) and shifts them to Solar Surplus (11:00 AM - 02:00 PM).
                            </p>
                        </div>
                        <button id="toggleRO" onclick="toggleSystem('ro')" class="toggle-pill on">ACTIVE</button>
                    </div>

                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
                        <div class="p-3 rounded-lg" style="background: #2B2D31;">
                            <div class="flex justify-between mb-1.5">
                                <span style="color: #8E9297;">Tariff Window</span>
                                <span id="roWindowBadge" class="font-data font-semibold" style="color: #FFC93C;">Peak (6-10 PM)</span>
                            </div>
                            <select id="roWindow" onchange="recalcCampusROI()" class="w-full p-1.5 rounded text-xs font-data text-white outline-none" style="background: #36393F; border: 1px solid rgba(255,255,255,0.08);">
                                <option value="peak">Peak Tariff (06:00 PM - 10:00 PM)</option>
                                <option value="solar">Solar Surplus (11:00 AM - 02:00 PM)</option>
                                <option value="offpeak">Off-Peak (10:00 PM - 06:00 AM)</option>
                            </select>
                        </div>

                        <div class="p-3 rounded-lg" style="background: #2B2D31;">
                            <div class="flex justify-between mb-1.5">
                                <span style="color: #8E9297;">RO Storage Tank</span>
                                <span id="roTankVal" class="font-data font-semibold text-white">72%</span>
                            </div>
                            <input id="roTank" type="range" min="15" max="100" value="72" oninput="recalcCampusROI()" class="w-full">
                        </div>
                    </div>

                    <div class="p-3 rounded-lg flex items-center justify-between text-xs" style="background: #2B2D31;">
                        <span id="roDecision" style="color: #D9DAD0;">RO &amp; STP motors locked OFF during Peak Tariff (tank at 72%).</span>
                        <span id="roSavings" class="font-data font-bold ml-3 whitespace-nowrap" style="color: #FFC93C;">820 kWh/mo</span>
                    </div>
                </div>

                <!-- 2. ENTERPRISE WIFI AP POE SCHEDULING (MODULE H) -->
                <div class="card p-5 space-y-4">
                    <div class="flex items-start justify-between gap-3">
                        <div>
                            <div class="text-[11px] font-semibold uppercase tracking-wider" style="color: #FFC93C;">Module H // Network PoE</div>
                            <h3 class="text-base font-bold text-white mt-0.5">Enterprise WiFi AP Night Power Reduction</h3>
                            <p class="text-xs mt-1" style="color: #8E9297;">
                                Drops Academic Block PoE Access Points from 20W (5 GHz + 2.4 GHz) to &lt;5W IoT-only mode from 11:00 PM - 06:00 AM. Hostel APs stay 100% ON.
                            </p>
                        </div>
                        <button id="toggleWifi" onclick="toggleSystem('wifi')" class="toggle-pill on">ACTIVE</button>
                    </div>

                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
                        <div class="p-3 rounded-lg" style="background: #2B2D31;">
                            <div class="flex justify-between mb-1.5">
                                <span style="color: #8E9297;">Academic Block APs</span>
                                <span id="wifiAcadVal" class="font-data font-semibold text-white">110 APs</span>
                            </div>
                            <input id="wifiAcad" type="range" min="20" max="180" step="5" value="110" oninput="recalcCampusROI()" class="w-full">
                        </div>

                        <div class="p-3 rounded-lg" style="background: #2B2D31;">
                            <div class="flex justify-between mb-1.5">
                                <span style="color: #8E9297;">Night Hours Dimmed</span>
                                <span id="wifiHoursVal" class="font-data font-semibold text-white">7 hrs/night</span>
                            </div>
                            <input id="wifiHours" type="range" min="4" max="10" value="7" oninput="recalcCampusROI()" class="w-full">
                        </div>
                    </div>

                    <div class="p-3 rounded-lg flex items-center justify-between text-xs" style="background: #2B2D31;">
                        <span id="wifiDecision" style="color: #D9DAD0;">110 Academic APs in &lt;5W PoE Eco Mode; 40 Hostel APs at 100%.</span>
                        <span id="wifiSavings" class="font-data font-bold ml-3 whitespace-nowrap" style="color: #FFC93C;">700 kWh/mo</span>
                    </div>
                </div>

                <!-- 3. HOSTEL GEYSER STAGGERING & KVA PEAK SHAVING (MODULE E) -->
                <div class="card p-5 space-y-4">
                    <div class="flex items-start justify-between gap-3">
                        <div>
                            <div class="text-[11px] font-semibold uppercase tracking-wider" style="color: #FFC93C;">Module E // Hostel Peak Guard</div>
                            <h3 class="text-base font-bold text-white mt-0.5">Hostel Geyser Staggering &amp; Solar Pumping</h3>
                            <p class="text-xs mt-1" style="color: #8E9297;">
                                Staggers Wing 1 (05:30-06:30 AM) and Wing 2 (06:30-07:30 AM) geysers so campus stays below contracted Maximum Demand (kVA) limit.
                            </p>
                        </div>
                        <button id="toggleHostel" onclick="toggleSystem('hostel')" class="toggle-pill on">ACTIVE</button>
                    </div>

                    <div class="p-3 rounded-lg space-y-2 text-xs" style="background: #2B2D31;">
                        <div class="flex justify-between">
                            <span style="color: #8E9297;">06:00 AM Peak Demand Load</span>
                            <span id="hostelKvaText" class="font-data font-semibold" style="color: #FFC93C;">310 kVA (Safe: Below 400 kVA MD Limit)</span>
                        </div>
                        <div class="w-full h-2.5 rounded-full overflow-hidden" style="background: #36393F;">
                            <div id="hostelKvaBar" class="h-full rounded-full transition-all" style="width: 68%; background: #FFC93C;"></div>
                        </div>
                        <div class="flex justify-between text-[11px]" style="color: #8E9297;">
                            <span>Wing 1: 05:30-06:30 AM</span>
                            <span>Wing 2: 06:30-07:30 AM</span>
                            <span>Insulated Tank: 2+ hr hold</span>
                        </div>
                    </div>

                    <div class="p-3 rounded-lg flex items-center justify-between text-xs" style="background: #2B2D31;">
                        <span id="hostelDecision" style="color: #D9DAD0;">Wing-by-wing contactor stagger active; MD penalty avoided.</span>
                        <span id="hostelSavings" class="font-data font-bold ml-3 whitespace-nowrap" style="color: #FFC93C;">1,800 kWh/mo</span>
                    </div>
                </div>

                <!-- 4. CAMPUS WATER COOLERS & COLD-CHAIN (MODULE F) -->
                <div class="card p-5 space-y-4">
                    <div class="flex items-start justify-between gap-3">
                        <div>
                            <div class="text-[11px] font-semibold uppercase tracking-wider" style="color: #FFC93C;">Module F // Cold-Chain Interlock</div>
                            <h3 class="text-base font-bold text-white mt-0.5">Water Coolers &amp; Cafeteria Interlocking</h3>
                            <p class="text-xs mt-1" style="color: #8E9297;">
                                Cuts commercial 1.5 kW water coolers overnight (07:00 PM - 07:00 AM) and all Sunday/Holidays. Insulated steel tanks hold chill for 2+ hrs.
                            </p>
                        </div>
                        <button id="toggleCooler" onclick="toggleSystem('cooler')" class="toggle-pill on">ACTIVE</button>
                    </div>

                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
                        <div class="p-3 rounded-lg" style="background: #2B2D31;">
                            <div class="flex justify-between mb-1.5">
                                <span style="color: #8E9297;">Water Coolers (1.5 kW)</span>
                                <span id="coolerCountVal" class="font-data font-semibold text-white">15 Units</span>
                            </div>
                            <input id="coolerCount" type="range" min="5" max="30" value="15" oninput="recalcCampusROI()" class="w-full">
                        </div>

                        <div class="p-3 rounded-lg" style="background: #2B2D31;">
                            <div class="flex justify-between mb-1.5">
                                <span style="color: #8E9297;">Schedule Mode</span>
                            </div>
                            <select id="coolerMode" onchange="recalcCampusROI()" class="w-full p-1.5 rounded text-xs font-data text-white outline-none" style="background: #36393F; border: 1px solid rgba(255,255,255,0.08);">
                                <option value="weekday">Weekday Night Cutoff (7 PM - 7 AM)</option>
                                <option value="holiday">Sunday / Holiday Full Shutdown (24h)</option>
                            </select>
                        </div>
                    </div>

                    <div class="p-3 rounded-lg flex items-center justify-between text-xs" style="background: #2B2D31;">
                        <span id="coolerDecision" style="color: #D9DAD0;">15 coolers locked OFF overnight; cafeteria frost-cycle optimized.</span>
                        <span id="coolerSavings" class="font-data font-bold ml-3 whitespace-nowrap" style="color: #FFC93C;">1,620 kWh/mo</span>
                    </div>
                </div>

                <!-- 5. COMPUTER LAB PHANTOM PC DRAIN & WOL (MODULE C) -->
                <div class="card p-5 space-y-4 lg:col-span-2">
                    <div class="flex items-start justify-between gap-3">
                        <div>
                            <div class="text-[11px] font-semibold uppercase tracking-wider" style="color: #FFC93C;">Module C // Zero-Hardware Software Policy</div>
                            <h3 class="text-base font-bold text-white mt-0.5">Computer Lab Phantom PC Drain &amp; Wake-on-LAN</h3>
                            <p class="text-xs mt-1" style="color: #8E9297;">
                                OS agent drops idle PCs (80-120W) to S3 Sleep (&lt;2W) after 15 mins, broadcasts 06:00 PM shutdown, and boots via Wake-on-LAN at 07:45 AM. Eliminates 6 kW heat load so split AC shuts off too.
                            </p>
                        </div>
                        <button id="toggleLabs" onclick="toggleSystem('labs')" class="toggle-pill on">ACTIVE</button>
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
                        <div class="p-3 rounded-lg" style="background: #2B2D31;">
                            <div class="flex justify-between mb-1.5">
                                <span style="color: #8E9297;">Managed Lab PCs</span>
                                <span id="labPcVal" class="font-data font-semibold text-white">120 PCs</span>
                            </div>
                            <input id="labPcCount" type="range" min="30" max="240" step="10" value="120" oninput="recalcCampusROI()" class="w-full">
                        </div>

                        <div class="p-3 rounded-lg flex flex-col justify-center" style="background: #2B2D31;">
                            <div style="color: #8E9297;">Idle Heat Eliminated</div>
                            <div id="labHeatText" class="font-data font-semibold text-white mt-1">12.0 kW thermal load removed</div>
                        </div>

                        <div class="p-3 rounded-lg flex items-center justify-between" style="background: #2B2D31;">
                            <span style="color: #D9DAD0;">Estimated Savings</span>
                            <span id="labSavings" class="font-data font-bold" style="color: #FFC93C;">2,400 kWh/mo</span>
                        </div>
                    </div>
                </div>

            </div>
        </div>

        <!-- =============================================================== -->
        <!-- TAB 2: HOW GRIDSENSE WORKS (SIMPLE TERMS + VISUAL FLOWCHART)    -->
        <!-- =============================================================== -->
        <div id="tabExplainer" class="hidden space-y-6">

            <!-- SIMPLE 30-SECOND EXPLANATION -->
            <div class="card p-6">
                <div class="text-xs font-semibold uppercase tracking-wider" style="color: #FFC93C;">Plain-English Overview</div>
                <h2 class="text-xl font-bold text-white mt-1">How GridSense Works in 4 Simple Steps</h2>
                <p class="text-sm mt-2" style="color: #D9DAD0;">
                    Colleges waste 30%-45% of their electricity after hours because buildings stay ON even when students leave.
                    Instead of buying expensive IoT sensors for 200 rooms, GridSense uses data the campus <b>already has</b> (WiFi, Timetable, Weather, Smart Meter) to safely turn off empty wings, shift heavy motors, and notify staff automatically.
                </p>

                <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mt-5">
                    <div class="p-4 rounded-xl" style="background: #2B2D31;">
                        <div class="text-xs font-data font-bold" style="color: #FFC93C;">STEP 01 // SENSE</div>
                        <div class="text-sm font-bold text-white mt-1">Read Existing Signals</div>
                        <p class="text-xs mt-1.5" style="color: #8E9297;">
                            Reads WiFi connected phones, ERP class timetable, outdoor temperature/daylight, and sub-meter kW every 15 mins.
                        </p>
                    </div>
                    <div class="p-4 rounded-xl" style="background: #2B2D31;">
                        <div class="text-xs font-data font-bold" style="color: #FFC93C;">STEP 02 // SCORE</div>
                        <div class="text-sm font-bold text-white mt-1">Waste Index (0-100)</div>
                        <p class="text-xs mt-1.5" style="color: #8E9297;">
                            Calculates a Waste Index Score (WIS) per zone. Empty room + high kW = High WIS. Scheduled class = Safety Veto (+20).
                        </p>
                    </div>
                    <div class="p-4 rounded-xl" style="background: #2B2D31;">
                        <div class="text-xs font-data font-bold" style="color: #FFC93C;">STEP 03 // OPTIMIZE</div>
                        <div class="text-sm font-bold text-white mt-1">Consolidate &amp; Shift</div>
                        <p class="text-xs mt-1.5" style="color: #8E9297;">
                            Moves lone classes into one wing, stages 2/3/4 lifts, shifts RO/STP motors off peak tariff, and sleeps idle lab PCs.
                        </p>
                    </div>
                    <div class="p-4 rounded-xl" style="background: #2B2D31;">
                        <div class="text-xs font-data font-bold" style="color: #FFC93C;">STEP 04 // NOTIFY</div>
                        <div class="text-sm font-bold text-white mt-1">Auto-Alert &amp; Log</div>
                        <p class="text-xs mt-1.5" style="color: #8E9297;">
                            Pushes classroom move emails via n8n + Gmail, logs savings to Google Sheets, and alerts staff on Telegram.
                        </p>
                    </div>
                </div>
            </div>

            <!-- VISUAL SYSTEM FLOWCHART (SVG) -->
            <div class="card p-6">
                <div class="flex items-center justify-between mb-4">
                    <div>
                        <div class="text-xs font-semibold uppercase tracking-wider" style="color: #FFC93C;">Visual Architecture</div>
                        <h3 class="text-lg font-bold text-white mt-0.5">End-to-End GridSense Decision Flowchart</h3>
                    </div>
                    <span class="text-xs font-data px-2.5 py-1 rounded" style="background: #2B2D31; color: #D9DAD0;">15-Min Cycle</span>
                </div>

                <div class="w-full overflow-x-auto rounded-xl p-4" style="background: #2B2D31; border: 1px solid rgba(255,255,255,0.06);">
                    <svg viewBox="0 0 980 340" class="w-full min-w-[780px] h-auto" xmlns="http://www.w3.org/2000/svg">
                        <defs>
                            <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                                <path d="M 0 1 L 10 5 L 0 9 z" fill="#FFC93C" />
                            </marker>
                            <marker id="arrowGray" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                                <path d="M 0 1 L 10 5 L 0 9 z" fill="#8E9297" />
                            </marker>
                        </defs>

                        <!-- COL 1: INPUT SIGNALS -->
                        <rect x="15" y="25" width="205" height="290" rx="12" fill="#36393F" stroke="rgba(255,255,255,0.12)" stroke-width="1.5"/>
                        <text x="117" y="50" text-anchor="middle" fill="#FFC93C" font-size="11" font-weight="700" font-family="JetBrains Mono, monospace">1. CAMPUS INPUTS</text>

                        <rect x="30" y="68" width="175" height="44" rx="8" fill="#2B2D31" stroke="rgba(255,255,255,0.08)"/>
                        <text x="117" y="88" text-anchor="middle" fill="#FFFFFF" font-size="11" font-weight="600">WiFi AP Clients + ERP</text>
                        <text x="117" y="103" text-anchor="middle" fill="#8E9297" font-size="9.5">Occupancy Weight: 0.60</text>

                        <rect x="30" y="124" width="175" height="44" rx="8" fill="#2B2D31" stroke="rgba(255,255,255,0.08)"/>
                        <text x="117" y="144" text-anchor="middle" fill="#FFFFFF" font-size="11" font-weight="600">Weather &amp; Daylight Lux</text>
                        <text x="117" y="159" text-anchor="middle" fill="#8E9297" font-size="9.5">Climate Weight: 0.23</text>

                        <rect x="30" y="180" width="175" height="44" rx="8" fill="#2B2D31" stroke="rgba(255,255,255,0.08)"/>
                        <text x="117" y="200" text-anchor="middle" fill="#FFFFFF" font-size="11" font-weight="600">Smart Meter + ToD Tariff</text>
                        <text x="117" y="215" text-anchor="middle" fill="#8E9297" font-size="9.5">Energy Weight: 0.21</text>

                        <rect x="30" y="236" width="175" height="44" rx="8" fill="#2B2D31" stroke="rgba(255,255,255,0.08)"/>
                        <text x="117" y="256" text-anchor="middle" fill="#FFFFFF" font-size="11" font-weight="600">Time, Curfew &amp; Holidays</text>
                        <text x="117" y="271" text-anchor="middle" fill="#8E9297" font-size="9.5">Schedule Weight: 0.12</text>

                        <!-- ARROW COL 1 -> COL 2 -->
                        <line x1="222" y1="170" x2="265" y2="170" stroke="#FFC93C" stroke-width="2" marker-end="url(#arrow)"/>

                        <!-- COL 2: WIS ENGINE + SAFETY VETO -->
                        <rect x="270" y="65" width="210" height="140" rx="12" fill="#36393F" stroke="#FFC93C" stroke-width="1.5"/>
                        <text x="375" y="92" text-anchor="middle" fill="#FFC93C" font-size="11" font-weight="700" font-family="JetBrains Mono, monospace">2. GRIDSENSE ENGINE</text>
                        <text x="375" y="118" text-anchor="middle" fill="#FFFFFF" font-size="13" font-weight="700">Waste Index Score</text>
                        <text x="375" y="138" text-anchor="middle" fill="#D9DAD0" font-size="11" font-family="JetBrains Mono, monospace">WIS = 0 to 100 / zone</text>
                        <rect x="290" y="154" width="170" height="36" rx="7" fill="#2B2D31" stroke="rgba(255,201,60,0.35)"/>
                        <text x="375" y="176" text-anchor="middle" fill="#FFC93C" font-size="10.5" font-weight="600">Safety Veto: ERP Class +20</text>

                        <!-- CURFEW BOX UNDER ENGINE -->
                        <rect x="270" y="225" width="210" height="68" rx="10" fill="#36393F" stroke="rgba(255,255,255,0.12)"/>
                        <text x="375" y="250" text-anchor="middle" fill="#FFFFFF" font-size="11.5" font-weight="700">09:30 PM Curfew Rule</text>
                        <text x="375" y="268" text-anchor="middle" fill="#8E9297" font-size="10">No classes after 9:30 PM</text>
                        <text x="375" y="282" text-anchor="middle" fill="#FFC93C" font-size="10" font-family="JetBrains Mono, monospace">Full Shutdown -&gt; 0.0 kW</text>
                        <line x1="375" y1="205" x2="375" y2="222" stroke="#8E9297" stroke-width="1.5" marker-end="url(#arrowGray)"/>

                        <!-- ARROW COL 2 -> COL 3 -->
                        <line x1="482" y1="135" x2="525" y2="135" stroke="#FFC93C" stroke-width="2" marker-end="url(#arrow)"/>

                        <!-- COL 3: 5-TIER ACTIONS -->
                        <rect x="530" y="25" width="210" height="290" rx="12" fill="#36393F" stroke="rgba(255,255,255,0.12)" stroke-width="1.5"/>
                        <text x="635" y="50" text-anchor="middle" fill="#FFC93C" font-size="11" font-weight="700" font-family="JetBrains Mono, monospace">3. SMART ACTIONS</text>

                        <rect x="546" y="68" width="178" height="48" rx="8" fill="#2B2D31"/>
                        <text x="635" y="88" text-anchor="middle" fill="#FFFFFF" font-size="11" font-weight="600">Wing Consolidation</text>
                        <text x="635" y="104" text-anchor="middle" fill="#8E9297" font-size="9.5">Move lone class, kill empty wing</text>

                        <rect x="546" y="126" width="178" height="48" rx="8" fill="#2B2D31"/>
                        <text x="635" y="146" text-anchor="middle" fill="#FFFFFF" font-size="11" font-weight="600">2 / 3 / 4 Lift Staging</text>
                        <text x="635" y="162" text-anchor="middle" fill="#8E9297" font-size="9.5">Scale lifts by active wing load</text>

                        <rect x="546" y="184" width="178" height="48" rx="8" fill="#2B2D31"/>
                        <text x="635" y="204" text-anchor="middle" fill="#FFFFFF" font-size="11" font-weight="600">RO, Geysers &amp; Coolers</text>
                        <text x="635" y="220" text-anchor="middle" fill="#8E9297" font-size="9.5">Peak lockout &amp; kVA stagger</text>

                        <rect x="546" y="242" width="178" height="48" rx="8" fill="#2B2D31"/>
                        <text x="635" y="262" text-anchor="middle" fill="#FFFFFF" font-size="11" font-weight="600">Lab PCs &amp; WiFi PoE</text>
                        <text x="635" y="278" text-anchor="middle" fill="#8E9297" font-size="9.5">S3 Sleep + Night Eco Mode</text>

                        <!-- ARROW COL 3 -> COL 4 -->
                        <line x1="742" y1="170" x2="780" y2="170" stroke="#FFC93C" stroke-width="2" marker-end="url(#arrow)"/>

                        <!-- COL 4: OUTPUTS -->
                        <rect x="785" y="45" width="180" height="250" rx="12" fill="#36393F" stroke="rgba(255,255,255,0.12)" stroke-width="1.5"/>
                        <text x="875" y="70" text-anchor="middle" fill="#FFC93C" font-size="11" font-weight="700" font-family="JetBrains Mono, monospace">4. LIVE OUTPUTS</text>

                        <rect x="800" y="88" width="150" height="42" rx="8" fill="#2B2D31"/>
                        <text x="875" y="106" text-anchor="middle" fill="#FFFFFF" font-size="11" font-weight="600">n8n -&gt; Gmail</text>
                        <text x="875" y="121" text-anchor="middle" fill="#8E9297" font-size="9.5">Classroom move notices</text>

                        <rect x="800" y="140" width="150" height="42" rx="8" fill="#2B2D31"/>
                        <text x="875" y="158" text-anchor="middle" fill="#FFFFFF" font-size="11" font-weight="600">n8n -&gt; Google Sheets</text>
                        <text x="875" y="173" text-anchor="middle" fill="#8E9297" font-size="9.5">Permanent kWh audit log</text>

                        <rect x="800" y="192" width="150" height="42" rx="8" fill="#2B2D31"/>
                        <text x="875" y="210" text-anchor="middle" fill="#FFFFFF" font-size="11" font-weight="600">Telegram Mobile</text>
                        <text x="875" y="225" text-anchor="middle" fill="#8E9297" font-size="9.5">Instant 3-part alert</text>

                        <rect x="800" y="244" width="150" height="42" rx="8" fill="#2B2D31" stroke="rgba(255,201,60,0.35)"/>
                        <text x="875" y="262" text-anchor="middle" fill="#FFC93C" font-size="11" font-weight="700">INR 1.35L / mo Saved</text>
                        <text x="875" y="277" text-anchor="middle" fill="#D9DAD0" font-size="9.5">15,000 kWh/mo campus-wide</text>
                    </svg>
                </div>
            </div>

            <!-- 5-LEVEL INTERVENTION LADDER -->
            <div class="card p-6">
                <div class="text-xs font-semibold uppercase tracking-wider" style="color: #FFC93C;">Graduated Control (No Abrupt Shutoffs)</div>
                <h3 class="text-lg font-bold text-white mt-0.5 mb-4">The 5-Level Intervention Ladder</h3>
                <div class="overflow-x-auto">
                    <table class="w-full text-left text-xs border-collapse">
                        <thead>
                            <tr style="border-bottom: 1px solid rgba(255,255,255,0.1); color: #8E9297;">
                                <th class="py-2.5 px-3">WIS Score</th>
                                <th class="py-2.5 px-3">Severity</th>
                                <th class="py-2.5 px-3">System Action</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y" style="border-color: rgba(255,255,255,0.06);">
                            <tr>
                                <td class="py-2.5 px-3 font-data font-bold text-white">0 - 20</td>
                                <td class="py-2.5 px-3 text-white">Normal / Efficient</td>
                                <td class="py-2.5 px-3" style="color: #D9DAD0;">No action. Continue 15-minute monitoring cycle.</td>
                            </tr>
                            <tr>
                                <td class="py-2.5 px-3 font-data font-bold text-white">21 - 40</td>
                                <td class="py-2.5 px-3 text-white">Low Waste</td>
                                <td class="py-2.5 px-3" style="color: #D9DAD0;">Soft nudge notification to class rep / lab assistant.</td>
                            </tr>
                            <tr>
                                <td class="py-2.5 px-3 font-data font-bold" style="color: #FFC93C;">41 - 60</td>
                                <td class="py-2.5 px-3" style="color: #FFC93C;">Medium Waste</td>
                                <td class="py-2.5 px-3" style="color: #D9DAD0;">AC setpoint raised +2 C, window-row lights dimmed, admin alert sent.</td>
                            </tr>
                            <tr>
                                <td class="py-2.5 px-3 font-data font-bold" style="color: #FFC93C;">61 - 80</td>
                                <td class="py-2.5 px-3" style="color: #FFC93C;">High Waste</td>
                                <td class="py-2.5 px-3" style="color: #D9DAD0;">Relay trigger: Zone A lights OFF, AC 28 C, AV/Smartboards sleep.</td>
                            </tr>
                            <tr>
                                <td class="py-2.5 px-3 font-data font-bold" style="color: #FFC93C;">81 - 100</td>
                                <td class="py-2.5 px-3" style="color: #FFC93C;">Critical Waste</td>
                                <td class="py-2.5 px-3" style="color: #D9DAD0;">Full Distribution Board isolation of verified empty wing + audit log.</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

        </div>

    </main>

    <script>
        const sysState = {
            ro: true,
            wifi: true,
            hostel: true,
            cooler: true,
            labs: true
        };

        function switchSystemsTab(tab) {
            const sim = document.getElementById('tabSimulator');
            const exp = document.getElementById('tabExplainer');
            const bSim = document.getElementById('btnTabSimulator');
            const bExp = document.getElementById('btnTabExplainer');
            if (tab === 'simulator') {
                sim.classList.remove('hidden');
                exp.classList.add('hidden');
                bSim.classList.add('active');
                bExp.classList.remove('active');
            } else {
                sim.classList.add('hidden');
                exp.classList.remove('hidden');
                bSim.classList.remove('active');
                bExp.classList.add('active');
            }
        }

        function toggleSystem(key) {
            sysState[key] = !sysState[key];
            const map = {
                ro: 'toggleRO',
                wifi: 'toggleWifi',
                hostel: 'toggleHostel',
                cooler: 'toggleCooler',
                labs: 'toggleLabs'
            };
            const btn = document.getElementById(map[key]);
            if (sysState[key]) {
                btn.className = 'toggle-pill on';
                btn.innerText = 'ACTIVE';
            } else {
                btn.className = 'toggle-pill off';
                btn.innerText = 'OFF';
            }
            recalcCampusROI();
        }

        function formatINR(num) {
            return 'INR ' + Math.round(num).toLocaleString('en-IN');
        }

        function recalcCampusROI() {
            const tariff = Math.max(1, parseFloat(document.getElementById('tariffInput').value) || 9);

            // 1. RO & STP
            const roWindow = document.getElementById('roWindow').value;
            const roTank = parseInt(document.getElementById('roTank').value, 10);
            document.getElementById('roTankVal').innerText = roTank + '%';
            const roWinLabels = { peak: 'Peak (6-10 PM)', solar: 'Solar (11 AM-2 PM)', offpeak: 'Off-Peak (10 PM-6 AM)' };
            document.getElementById('roWindowBadge').innerText = roWinLabels[roWindow];
            let roKwh = 0;
            if (sysState.ro) {
                roKwh = 820;
                if (roWindow === 'peak' && roTank >= 40) {
                    document.getElementById('roDecision').innerText = `RO & STP locked OFF during Peak Tariff (tank at ${roTank}%).`;
                } else if (roWindow === 'solar') {
                    roKwh = 950;
                    document.getElementById('roDecision').innerText = `Running RO & STP on Solar Surplus (11 AM-2 PM), zero peak tariff.`;
                } else {
                    document.getElementById('roDecision').innerText = `Running on Off-Peak tariff to refill tank (${roTank}%).`;
                }
            } else {
                document.getElementById('roDecision').innerText = 'Bypassed: RO & STP running on unmanaged schedule.';
            }
            document.getElementById('roSavings').innerText = roKwh.toLocaleString() + ' kWh/mo';

            // 2. WiFi APs
            const acadAps = parseInt(document.getElementById('wifiAcad').value, 10);
            const wifiHrs = parseInt(document.getElementById('wifiHours').value, 10);
            document.getElementById('wifiAcadVal').innerText = acadAps + ' APs';
            document.getElementById('wifiHoursVal').innerText = wifiHrs + ' hrs/night';
            let wifiKwh = 0;
            if (sysState.wifi) {
                // ~18W saved per AP during night hours * 30 days (baseline KB: 110 APs -> ~700 kWh/mo)
                wifiKwh = Math.round((acadAps * 0.015 * wifiHrs * 30) * 0.65);
                if (acadAps === 110 && wifiHrs === 7) wifiKwh = 700;
                document.getElementById('wifiDecision').innerText = `${acadAps} Academic APs in <5W PoE Eco Mode; 40 Hostel APs at 100%.`;
            } else {
                document.getElementById('wifiDecision').innerText = 'Bypassed: All Academic APs running 5 GHz at 100% 24/7.';
            }
            document.getElementById('wifiSavings').innerText = wifiKwh.toLocaleString() + ' kWh/mo';

            // 3. Hostel Geysers
            let hostelKwh = 0;
            if (sysState.hostel) {
                hostelKwh = 1800;
                document.getElementById('hostelKvaText').innerText = '310 kVA (Safe: Below 400 kVA MD Limit)';
                document.getElementById('hostelKvaText').style.color = '#FFC93C';
                document.getElementById('hostelKvaBar').style.width = '68%';
                document.getElementById('hostelKvaBar').style.background = '#FFC93C';
                document.getElementById('hostelDecision').innerText = 'Wing-by-wing contactor stagger active; MD penalty avoided.';
            } else {
                document.getElementById('hostelKvaText').innerText = '445 kVA (BREACH: Exceeds 400 kVA MD Limit!)';
                document.getElementById('hostelKvaText').style.color = '#F87171';
                document.getElementById('hostelKvaBar').style.width = '98%';
                document.getElementById('hostelKvaBar').style.background = '#F87171';
                document.getElementById('hostelDecision').innerText = 'All wings firing at 06:00 AM simultaneously -> utility penalty!';
            }
            document.getElementById('hostelSavings').innerText = hostelKwh.toLocaleString() + ' kWh/mo';

            // 4. Water Coolers
            const coolers = parseInt(document.getElementById('coolerCount').value, 10);
            const coolerMode = document.getElementById('coolerMode').value;
            document.getElementById('coolerCountVal').innerText = coolers + ' Units';
            let coolerKwh = 0;
            if (sysState.cooler) {
                coolerKwh = Math.round((coolers / 15) * (coolerMode === 'holiday' ? 2100 : 1620));
                document.getElementById('coolerDecision').innerText = coolerMode === 'holiday'
                    ? `${coolers} coolers in 24h Sunday/Holiday shutdown.`
                    : `${coolers} coolers locked OFF 07:00 PM - 07:00 AM; 2+ hr chill hold.`;
            } else {
                document.getElementById('coolerDecision').innerText = 'Bypassed: Water coolers chilling empty blocks 24/7.';
            }
            document.getElementById('coolerSavings').innerText = coolerKwh.toLocaleString() + ' kWh/mo';

            // 5. Lab PCs
            const labPcs = parseInt(document.getElementById('labPcCount').value, 10);
            document.getElementById('labPcVal').innerText = labPcs + ' PCs';
            const heatKw = (labPcs * 0.10).toFixed(1);
            let labKwh = 0;
            if (sysState.labs) {
                labKwh = Math.round((labPcs / 120) * 2400);
                document.getElementById('labHeatText').innerText = `${heatKw} kW internal heat load removed`;
            } else {
                document.getElementById('labHeatText').innerText = `0.0 kW removed (${heatKw} kW heating empty lab)`;
            }
            document.getElementById('labSavings').innerText = labKwh.toLocaleString() + ' kWh/mo';

            // Total Campus ROI (Block B modules A+B+D = 7,660 kWh/mo + active Campus Systems)
            const blockBKwh = 7660;
            const totalMonthlyKwh = blockBKwh + roKwh + wifiKwh + hostelKwh + coolerKwh + labKwh;
            const monthlyInr = totalMonthlyKwh * tariff;
            const annualInr = monthlyInr * 12;
            const annualCo2Tons = ((totalMonthlyKwh * 12 * 0.82) / 1000).toFixed(1);
            const activeCount = Object.values(sysState).filter(Boolean).length;

            document.getElementById('kpiMonthlyKwh').innerText = totalMonthlyKwh.toLocaleString() + ' kWh';
            document.getElementById('kpiMonthlyInr').innerText = formatINR(monthlyInr);
            document.getElementById('kpiAnnualInr').innerText = formatINR(annualInr) + ' / year projected';
            document.getElementById('kpiCo2Tons').innerText = annualCo2Tons + ' Tons';
            document.getElementById('kpiActiveModules').innerText = activeCount + ' / 5 Active';
        }

        window.addEventListener('DOMContentLoaded', recalcCampusROI);
    </script>
</body>
</html>
"""
