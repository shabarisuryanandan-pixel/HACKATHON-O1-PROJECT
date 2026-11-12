"""
GridSense Campus Systems View
Glanceable Campus-Wide Savings & Carbon Calculator (with editable INR/kWh rate)
plus a plain-English "How GridSense Works" visual flowchart tab.
Color Scheme: #01010D (bg), #12102E (cards), #E4E6F5 (silver), #6BFBCE (yellow accent).
"""


def render_campus_systems_html() -> str:
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GridSense // Campus Systems</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap" rel="stylesheet">
    <style>
        body {
            background-color: #01010D;
            background-image:
                radial-gradient(circle at 14% 12%, rgba(83, 49, 251, 0.28) 0%, transparent 42%),
                radial-gradient(circle at 86% 22%, rgba(107, 251, 206, 0.14) 0%, transparent 38%),
                radial-gradient(circle at 50% 88%, rgba(83, 49, 251, 0.20) 0%, transparent 48%);
            background-attachment: fixed;
            color: #E4E6F5;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            margin: 0;
        }
        header {
            background: rgba(1, 1, 13, 0.72) !important;
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-bottom: 1px solid rgba(107, 251, 206, 0.14) !important;
            position: sticky;
            top: 0;
            z-index: 40;
        }
        h1, h2, h3, .font-heading { font-family: 'Plus Jakarta Sans', sans-serif; letter-spacing: -0.015em; }
        .font-data { font-family: 'Inter', sans-serif; }
        .card {
            background: linear-gradient(135deg, rgba(22, 18, 56, 0.58) 0%, rgba(7, 7, 22, 0.62) 100%) !important;
            backdrop-filter: blur(22px);
            -webkit-backdrop-filter: blur(22px);
            border: 1px solid rgba(107, 251, 206, 0.16) !important;
            border-radius: 14px;
            box-shadow: 0 10px 36px rgba(1, 1, 13, 0.78), 0 0 28px rgba(83, 49, 251, 0.16), inset 0 1px 0 rgba(255, 255, 255, 0.10);
            transition: border-color 0.25s ease, box-shadow 0.25s ease, transform 0.25s ease;
        }
        .card:hover {
            border-color: rgba(107, 251, 206, 0.36) !important;
            box-shadow: 0 14px 44px rgba(1, 1, 13, 0.85), 0 0 36px rgba(83, 49, 251, 0.28), 0 0 18px rgba(107, 251, 206, 0.15), inset 0 1px 0 rgba(255, 255, 255, 0.16);
        }
        .nav-link {
            color: #9499B8;
            font-weight: 500;
            font-size: 14px;
            padding: 8px 0;
            border-bottom: 2px solid transparent;
            transition: all 0.15s ease;
        }
        .nav-link:hover { color: #FFFFFF; }
        .nav-link.active { color: #FFFFFF; border-bottom-color: #6BFBCE; }
        .tab-btn {
            padding: 8px 18px;
            border-radius: 9px;
            font-size: 13px;
            font-weight: 600;
            transition: all 0.15s ease;
            border: 1px solid rgba(255, 255, 255, 0.08);
        }
        .tab-btn.active {
            background-color: #6BFBCE;
            color: #01010D;
            border-color: #6BFBCE;
        }
        .tab-btn:not(.active) {
            background-color: #01010D;
            color: #E4E6F5;
        }
    </style>
</head>
<body class="min-h-screen flex flex-col">

    <!-- TOP NAVIGATION -->
    <header class="w-full" style="background-color: #01010D; border-bottom: 1px solid rgba(255,255,255,0.06);">
        <div class="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
            <div class="flex items-center gap-3">
                <div class="w-8 h-8 rounded-lg flex items-center justify-center font-bold text-sm" style="background-color: #6BFBCE; color: #01010D;">
                    GS
                </div>
                <span class="text-lg font-bold text-white tracking-tight">GridSense</span>
            </div>

            <nav class="flex items-center gap-8">
                <a href="/" class="nav-link">Dashboard</a>
                <a href="/sandbox" class="nav-link">Sandbox</a>
                <a href="/systems" class="nav-link active">Campus Systems</a>
            </nav>
        </div>
    </header>

    <main class="flex-1 w-full max-w-7xl mx-auto px-6 py-8 space-y-6">

        <!-- PAGE HEADER + TAB SWITCHER -->
        <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
            <div>
                <h1 class="text-2xl font-bold text-white tracking-tight">Campus Systems &amp; Total Savings</h1>
                <p class="text-sm mt-1" style="color: #9499B8;">
                    Campus-wide automation across all three academic blocks (Blocks A, B &amp; C) plus Water Purifier Plant, WiFi Routers, Hostel Heaters, Water Coolers, and Computer Labs.
                </p>
            </div>
            <div class="flex items-center gap-2">
                <button id="btnTabSimulator" onclick="switchSystemsTab('simulator')" class="tab-btn active">
                    Systems &amp; Savings Calculator
                </button>
                <button id="btnTabExplainer" onclick="switchSystemsTab('explainer')" class="tab-btn">
                    How GridSense Works
                </button>
            </div>
        </div>

        <!-- =============================================================== -->
        <!-- TAB 1: GLANCEABLE CAMPUS SYSTEMS + TOTAL SAVINGS CALCULATOR     -->
        <!-- =============================================================== -->
        <div id="tabSimulator" class="space-y-6">

            <!-- TOTAL SAVINGS & CARBON CALCULATOR -->
            <div class="card p-6">
                <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-3 mb-5">
                    <div>
                        <div class="text-xs font-semibold uppercase tracking-wider" style="color: #6BFBCE;">
                            Total Campus Impact
                        </div>
                        <h2 class="text-lg font-bold text-white mt-0.5">
                            Combined Monthly &amp; Yearly Savings (Blocks A, B &amp; C + Campus Systems)
                        </h2>
                    </div>
                    <div class="flex items-center gap-2.5 px-3 py-2 rounded-lg" style="background: #01010D; border: 1px solid rgba(107,251,206,0.35);">
                        <label for="tariffInput" class="text-xs font-semibold" style="color: #E4E6F5;">Electricity Price (INR per kWh):</label>
                        <input id="tariffInput" type="number" value="9" min="4" max="20" step="0.5" oninput="recalcCampusROI()"
                            class="w-16 px-2 py-1 rounded text-xs font-data font-bold text-white outline-none text-center"
                            style="background: #12102E; border: 1px solid rgba(255,255,255,0.15);">
                    </div>
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                    <div class="p-4 rounded-xl" style="background: #01010D; border: 1px solid rgba(255,255,255,0.06);">
                        <div class="text-[11px] font-semibold uppercase tracking-wider" style="color: #9499B8;">Monthly Electricity Saved</div>
                        <div class="text-2xl font-bold font-data text-white mt-1">15,000 kWh</div>
                        <div class="text-[11px] mt-1" style="color: #9499B8;">7,660 kWh Blocks A, B &amp; C + 7,340 kWh Campus Systems</div>
                    </div>

                    <div class="p-4 rounded-xl" style="background: #01010D; border: 1px solid rgba(107,251,206,0.35);">
                        <div class="text-[11px] font-semibold uppercase tracking-wider" style="color: #6BFBCE;">Monthly Money Saved</div>
                        <div id="kpiMonthlyInr" class="text-2xl font-bold font-data mt-1" style="color: #6BFBCE;">INR 1,35,000</div>
                        <div id="kpiAnnualInr" class="text-[11px] font-data mt-1" style="color: #E4E6F5;">INR 16,20,000 saved per year</div>
                    </div>

                    <div class="p-4 rounded-xl" style="background: #01010D; border: 1px solid rgba(255,255,255,0.06);">
                        <div class="text-[11px] font-semibold uppercase tracking-wider" style="color: #9499B8;">Carbon Pollution Avoided</div>
                        <div class="text-2xl font-bold font-data text-white mt-1">147.6 Tons / yr</div>
                        <div class="text-[11px] mt-1" style="color: #9499B8;">0.82 kg CO2 prevented per kWh saved</div>
                    </div>

                    <div class="p-4 rounded-xl" style="background: #01010D; border: 1px solid rgba(255,255,255,0.06);">
                        <div class="text-[11px] font-semibold uppercase tracking-wider" style="color: #9499B8;">Payback Period</div>
                        <div class="text-2xl font-bold font-data text-white mt-1">4 to 6 Months</div>
                        <div class="text-[11px] mt-1" style="color: #6BFBCE;">Covered by monthly bill savings</div>
                    </div>
                </div>
            </div>

            <!-- 5 STATIC, GLANCEABLE CAMPUS SYSTEM CARDS -->
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">

                <!-- 1. WATER PURIFICATION PLANT (RO) & PUMPS -->
                <div class="card p-5 flex flex-col justify-between space-y-4">
                    <div>
                        <div class="flex items-center justify-between">
                            <span class="text-[11px] font-semibold uppercase tracking-wider" style="color: #6BFBCE;">Heavy Motors</span>
                            <span class="text-[11px] font-data px-2 py-0.5 rounded" style="background: #01010D; color: #E4E6F5;">11 AM - 2 PM Solar</span>
                        </div>
                        <h3 class="text-base font-bold text-white mt-2">Water Purification Plant (RO) &amp; Pumps</h3>
                        <p class="text-xs mt-1.5 leading-relaxed" style="color: #9499B8;">
                            Stops heavy water purification and sewage motors during expensive evening hours (06:00 PM - 10:00 PM) and runs them during sunny afternoon hours instead.
                        </p>
                    </div>
                    <div class="p-3 rounded-lg flex items-center justify-between text-xs" style="background: #01010D;">
                        <span class="font-data text-white font-semibold">820 kWh / month</span>
                        <span id="cardInrRo" class="font-data font-bold" style="color: #6BFBCE;">INR 7,380 / mo</span>
                    </div>
                </div>

                <!-- 2. CAMPUS WIFI ROUTERS -->
                <div class="card p-5 flex flex-col justify-between space-y-4">
                    <div>
                        <div class="flex items-center justify-between">
                            <span class="text-[11px] font-semibold uppercase tracking-wider" style="color: #6BFBCE;">Campus Network</span>
                            <span class="text-[11px] font-data px-2 py-0.5 rounded" style="background: #01010D; color: #E4E6F5;">11 PM - 6 AM Eco</span>
                        </div>
                        <h3 class="text-base font-bold text-white mt-2">Campus WiFi Routers (Night Sleep)</h3>
                        <p class="text-xs mt-1.5 leading-relaxed" style="color: #9499B8;">
                            Switches 110 classroom-block WiFi routers to low-power mode from 11:00 PM to 06:00 AM when buildings are locked, while keeping Hostel WiFi at 100% power.
                        </p>
                    </div>
                    <div class="p-3 rounded-lg flex items-center justify-between text-xs" style="background: #01010D;">
                        <span class="font-data text-white font-semibold">700 kWh / month</span>
                        <span id="cardInrWifi" class="font-data font-bold" style="color: #6BFBCE;">INR 6,300 / mo</span>
                    </div>
                </div>

                <!-- 3. HOSTEL WATER HEATERS (GEYSERS) -->
                <div class="card p-5 flex flex-col justify-between space-y-4">
                    <div>
                        <div class="flex items-center justify-between">
                            <span class="text-[11px] font-semibold uppercase tracking-wider" style="color: #6BFBCE;">Hostel Block</span>
                            <span class="text-[11px] font-data px-2 py-0.5 rounded" style="background: #01010D; color: #E4E6F5;">5:30 AM Stagger</span>
                        </div>
                        <h3 class="text-base font-bold text-white mt-2">Hostel Water Heaters (Geysers)</h3>
                        <p class="text-xs mt-1.5 leading-relaxed" style="color: #9499B8;">
                            Runs Wing 1 heaters (05:30 - 06:30 AM) before Wing 2 (06:30 - 07:30 AM) instead of all at once, preventing costly electricity board peak-load penalties.
                        </p>
                    </div>
                    <div class="p-3 rounded-lg flex items-center justify-between text-xs" style="background: #01010D;">
                        <span class="font-data text-white font-semibold">1,800 kWh / month</span>
                        <span id="cardInrHostel" class="font-data font-bold" style="color: #6BFBCE;">INR 16,200 / mo</span>
                    </div>
                </div>

                <!-- 4. DRINKING WATER COOLERS -->
                <div class="card p-5 flex flex-col justify-between space-y-4">
                    <div>
                        <div class="flex items-center justify-between">
                            <span class="text-[11px] font-semibold uppercase tracking-wider" style="color: #6BFBCE;">Drinking Water</span>
                            <span class="text-[11px] font-data px-2 py-0.5 rounded" style="background: #01010D; color: #E4E6F5;">7 PM - 7 AM OFF</span>
                        </div>
                        <h3 class="text-base font-bold text-white mt-2">Water Coolers &amp; Cafeteria Fridges</h3>
                        <p class="text-xs mt-1.5 leading-relaxed" style="color: #9499B8;">
                            Turns off 15 commercial water coolers overnight (07:00 PM - 07:00 AM) and on Sundays. Insulated steel tanks keep water cold for 2+ hours after shutdown.
                        </p>
                    </div>
                    <div class="p-3 rounded-lg flex items-center justify-between text-xs" style="background: #01010D;">
                        <span class="font-data text-white font-semibold">1,620 kWh / month</span>
                        <span id="cardInrCooler" class="font-data font-bold" style="color: #6BFBCE;">INR 14,580 / mo</span>
                    </div>
                </div>

                <!-- 5. COMPUTER LABS -->
                <div class="card p-5 flex flex-col justify-between space-y-4 md:col-span-2 lg:col-span-2">
                    <div>
                        <div class="flex items-center justify-between">
                            <span class="text-[11px] font-semibold uppercase tracking-wider" style="color: #6BFBCE;">Zero New Hardware</span>
                            <span class="text-[11px] font-data px-2 py-0.5 rounded" style="background: #01010D; color: #E4E6F5;">Auto-Sleep + 6 PM Shutoff</span>
                        </div>
                        <h3 class="text-base font-bold text-white mt-2">Computer Labs (Idle PC Sleep &amp; Morning Wake-Up)</h3>
                        <p class="text-xs mt-1.5 leading-relaxed" style="color: #9499B8;">
                            Automatically puts idle lab computers to sleep after 15 minutes of no use and shuts them down at 06:00 PM (waking them at 07:45 AM over the network). Turning off idle computers also removes 6 kW of room heat so lab ACs can shut off too.
                        </p>
                    </div>
                    <div class="p-3 rounded-lg flex items-center justify-between text-xs" style="background: #01010D;">
                        <span class="font-data text-white font-semibold">2,400 kWh / month (120 Lab Computers)</span>
                        <span id="cardInrLabs" class="font-data font-bold" style="color: #6BFBCE;">INR 21,600 / mo</span>
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
                <div class="text-xs font-semibold uppercase tracking-wider" style="color: #6BFBCE;">Plain-English Overview</div>
                <h2 class="text-xl font-bold text-white mt-1">How GridSense Works in 4 Simple Steps</h2>
                <p class="text-sm mt-2" style="color: #E4E6F5;">
                    Colleges waste 30%-45% of their electricity after hours because buildings stay ON even when students leave.
                    Instead of buying expensive sensors for 200 rooms, GridSense uses data the campus <b>already has</b> (Class Timetable, WiFi Users, Weather, and Power Meters) to safely turn off empty wings, shift heavy motors, and alert administrators automatically.
                </p>

                <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mt-5">
                    <div class="p-4 rounded-xl" style="background: #01010D;">
                        <div class="text-xs font-data font-bold" style="color: #6BFBCE;">STEP 01 // SENSE</div>
                        <div class="text-sm font-bold text-white mt-1">Read Existing Signals</div>
                        <p class="text-xs mt-1.5" style="color: #9499B8;">
                            Checks the Class Timetable, WiFi connected phones, outdoor weather/sunlight, and power meter readings every 15 minutes.
                        </p>
                    </div>
                    <div class="p-4 rounded-xl" style="background: #01010D;">
                        <div class="text-xs font-data font-bold" style="color: #6BFBCE;">STEP 02 // SCORE</div>
                        <div class="text-sm font-bold text-white mt-1">Waste Score (0-100)</div>
                        <p class="text-xs mt-1.5" style="color: #9499B8;">
                            Scores each zone from 0 to 100. Empty room + high power = High Waste. Scheduled class = Safety Protection (+20 buffer).
                        </p>
                    </div>
                    <div class="p-4 rounded-xl" style="background: #01010D;">
                        <div class="text-xs font-data font-bold" style="color: #6BFBCE;">STEP 03 // OPTIMIZE</div>
                        <div class="text-sm font-bold text-white mt-1">Move &amp; Shut Down</div>
                        <p class="text-xs mt-1.5" style="color: #9499B8;">
                            Moves lone classes into one wing, runs only needed lifts, shifts water motors off peak hours, and enforces 10:30 PM curfew.
                        </p>
                    </div>
                    <div class="p-4 rounded-xl" style="background: #01010D;">
                        <div class="text-xs font-data font-bold" style="color: #6BFBCE;">STEP 04 // NOTIFY</div>
                        <div class="text-sm font-bold text-white mt-1">Alert Administrators</div>
                        <p class="text-xs mt-1.5" style="color: #9499B8;">
                            Sends classroom move emails via n8n + Gmail, logs savings to Google Sheets, and sends instant alerts to campus administrators.
                        </p>
                    </div>
                </div>
            </div>

            <!-- VISUAL SYSTEM FLOWCHART (SVG) -->
            <div class="card p-6">
                <div class="flex items-center justify-between mb-4">
                    <div>
                        <div class="text-xs font-semibold uppercase tracking-wider" style="color: #6BFBCE;">Visual Architecture</div>
                        <h3 class="text-lg font-bold text-white mt-0.5">End-to-End GridSense Decision Flowchart</h3>
                    </div>
                    <span class="text-xs font-data px-2.5 py-1 rounded" style="background: #01010D; color: #E4E6F5;">15-Min Cycle</span>
                </div>

                <div class="w-full overflow-x-auto rounded-xl p-4" style="background: #01010D; border: 1px solid rgba(255,255,255,0.06);">
                    <svg viewBox="0 0 980 340" class="w-full min-w-[780px] h-auto" xmlns="http://www.w3.org/2000/svg">
                        <defs>
                            <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                                <path d="M 0 1 L 10 5 L 0 9 z" fill="#6BFBCE" />
                            </marker>
                            <marker id="arrowGray" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                                <path d="M 0 1 L 10 5 L 0 9 z" fill="#9499B8" />
                            </marker>
                        </defs>

                        <!-- COL 1: INPUT SIGNALS -->
                        <rect x="15" y="25" width="205" height="290" rx="12" fill="#12102E" stroke="rgba(255,255,255,0.12)" stroke-width="1.5"/>
                        <text x="117" y="50" text-anchor="middle" fill="#6BFBCE" font-size="11" font-weight="700" font-family="Inter, sans-serif">1. CAMPUS INPUTS</text>

                        <rect x="30" y="68" width="175" height="44" rx="8" fill="#01010D" stroke="rgba(255,255,255,0.08)"/>
                        <text x="117" y="88" text-anchor="middle" fill="#FFFFFF" font-size="11" font-weight="600">Class Timetable + ERP + WiFi</text>
                        <text x="117" y="103" text-anchor="middle" fill="#9499B8" font-size="9.5">Occupancy Weight: 0.60</text>

                        <rect x="30" y="124" width="175" height="44" rx="8" fill="#01010D" stroke="rgba(255,255,255,0.08)"/>
                        <text x="117" y="144" text-anchor="middle" fill="#FFFFFF" font-size="11" font-weight="600">Weather &amp; Sunlight</text>
                        <text x="117" y="159" text-anchor="middle" fill="#9499B8" font-size="9.5">Climate Weight: 0.23</text>

                        <rect x="30" y="180" width="175" height="44" rx="8" fill="#01010D" stroke="rgba(255,255,255,0.08)"/>
                        <text x="117" y="200" text-anchor="middle" fill="#FFFFFF" font-size="11" font-weight="600">Power Meter + Tariff</text>
                        <text x="117" y="215" text-anchor="middle" fill="#9499B8" font-size="9.5">Energy Weight: 0.21</text>

                        <rect x="30" y="236" width="175" height="44" rx="8" fill="#01010D" stroke="rgba(255,255,255,0.08)"/>
                        <text x="117" y="256" text-anchor="middle" fill="#FFFFFF" font-size="11" font-weight="600">Time, Curfew &amp; Holidays</text>
                        <text x="117" y="271" text-anchor="middle" fill="#9499B8" font-size="9.5">Schedule Weight: 0.12</text>

                        <!-- ARROW COL 1 -> COL 2 -->
                        <line x1="222" y1="170" x2="265" y2="170" stroke="#6BFBCE" stroke-width="2" marker-end="url(#arrow)"/>

                        <!-- COL 2: WIS ENGINE + SAFETY VETO -->
                        <rect x="270" y="65" width="210" height="140" rx="12" fill="#12102E" stroke="#6BFBCE" stroke-width="1.5"/>
                        <text x="375" y="92" text-anchor="middle" fill="#6BFBCE" font-size="11" font-weight="700" font-family="Inter, sans-serif">2. GRIDSENSE ENGINE</text>
                        <text x="375" y="118" text-anchor="middle" fill="#FFFFFF" font-size="13" font-weight="700">Waste Index Score</text>
                        <text x="375" y="138" text-anchor="middle" fill="#E4E6F5" font-size="11" font-family="Inter, sans-serif">Score = 0 to 100 / zone</text>
                        <rect x="290" y="154" width="170" height="36" rx="7" fill="#01010D" stroke="rgba(107,251,206,0.35)"/>
                        <text x="375" y="176" text-anchor="middle" fill="#6BFBCE" font-size="10.5" font-weight="600">Safety Veto: Active Class +20</text>

                        <!-- CURFEW BOX UNDER ENGINE -->
                        <rect x="270" y="225" width="210" height="68" rx="10" fill="#12102E" stroke="rgba(255,255,255,0.12)"/>
                        <text x="375" y="250" text-anchor="middle" fill="#FFFFFF" font-size="11.5" font-weight="700">10:30 PM Curfew Rule</text>
                        <text x="375" y="268" text-anchor="middle" fill="#9499B8" font-size="10">No classes after 10:30 PM</text>
                        <text x="375" y="282" text-anchor="middle" fill="#6BFBCE" font-size="10" font-family="Inter, sans-serif">Full Shutdown -&gt; 0.0 kW</text>
                        <line x1="375" y1="205" x2="375" y2="222" stroke="#9499B8" stroke-width="1.5" marker-end="url(#arrowGray)"/>

                        <!-- ARROW COL 2 -> COL 3 -->
                        <line x1="482" y1="135" x2="525" y2="135" stroke="#6BFBCE" stroke-width="2" marker-end="url(#arrow)"/>

                        <!-- COL 3: SMART ACTIONS -->
                        <rect x="530" y="25" width="210" height="290" rx="12" fill="#12102E" stroke="rgba(255,255,255,0.12)" stroke-width="1.5"/>
                        <text x="635" y="50" text-anchor="middle" fill="#6BFBCE" font-size="11" font-weight="700" font-family="Inter, sans-serif">3. SMART ACTIONS</text>

                        <rect x="546" y="68" width="178" height="48" rx="8" fill="#01010D"/>
                        <text x="635" y="88" text-anchor="middle" fill="#FFFFFF" font-size="11" font-weight="600">Wing Consolidation</text>
                        <text x="635" y="104" text-anchor="middle" fill="#9499B8" font-size="9.5">Move lone class, turn off empty wing</text>

                        <rect x="546" y="126" width="178" height="48" rx="8" fill="#01010D"/>
                        <text x="635" y="146" text-anchor="middle" fill="#FFFFFF" font-size="11" font-weight="600">2 / 3 / 4 Lift Staging</text>
                        <text x="635" y="162" text-anchor="middle" fill="#9499B8" font-size="9.5">Scale lifts by active wing load</text>

                        <rect x="546" y="184" width="178" height="48" rx="8" fill="#01010D"/>
                        <text x="635" y="204" text-anchor="middle" fill="#FFFFFF" font-size="11" font-weight="600">RO, Geysers &amp; Coolers</text>
                        <text x="635" y="220" text-anchor="middle" fill="#9499B8" font-size="9.5">Off-peak motors &amp; heater stagger</text>

                        <rect x="546" y="242" width="178" height="48" rx="8" fill="#01010D"/>
                        <text x="635" y="262" text-anchor="middle" fill="#FFFFFF" font-size="11" font-weight="600">Lab Computers &amp; WiFi</text>
                        <text x="635" y="278" text-anchor="middle" fill="#9499B8" font-size="9.5">Auto-sleep &amp; night eco mode</text>

                        <!-- ARROW COL 3 -> COL 4 -->
                        <line x1="742" y1="170" x2="780" y2="170" stroke="#6BFBCE" stroke-width="2" marker-end="url(#arrow)"/>

                        <!-- COL 4: OUTPUTS -->
                        <rect x="785" y="45" width="180" height="250" rx="12" fill="#12102E" stroke="rgba(255,255,255,0.12)" stroke-width="1.5"/>
                        <text x="875" y="70" text-anchor="middle" fill="#6BFBCE" font-size="11" font-weight="700" font-family="Inter, sans-serif">4. LIVE OUTPUTS</text>

                        <rect x="800" y="88" width="150" height="42" rx="8" fill="#01010D"/>
                        <text x="875" y="106" text-anchor="middle" fill="#FFFFFF" font-size="11" font-weight="600">n8n -&gt; Gmail</text>
                        <text x="875" y="121" text-anchor="middle" fill="#9499B8" font-size="9.5">Classroom move emails</text>

                        <rect x="800" y="140" width="150" height="42" rx="8" fill="#01010D"/>
                        <text x="875" y="158" text-anchor="middle" fill="#FFFFFF" font-size="11" font-weight="600">n8n -&gt; Google Sheets</text>
                        <text x="875" y="173" text-anchor="middle" fill="#9499B8" font-size="9.5">Permanent savings log</text>

                        <rect x="800" y="192" width="150" height="42" rx="8" fill="#01010D"/>
                        <text x="875" y="210" text-anchor="middle" fill="#FFFFFF" font-size="11" font-weight="600">Admin &amp; Staff Alerts</text>
                        <text x="875" y="225" text-anchor="middle" fill="#9499B8" font-size="9.5">Instant phone &amp; team updates</text>

                        <rect x="800" y="244" width="150" height="42" rx="8" fill="#01010D" stroke="rgba(107,251,206,0.35)"/>
                        <text x="875" y="262" text-anchor="middle" fill="#6BFBCE" font-size="11" font-weight="700">INR 1.35L / mo Saved</text>
                        <text x="875" y="277" text-anchor="middle" fill="#E4E6F5" font-size="9.5">15,000 kWh/mo campus-wide</text>
                    </svg>
                </div>
            </div>

            <!-- 5-LEVEL INTERVENTION LADDER -->
            <div class="card p-6">
                <div class="text-xs font-semibold uppercase tracking-wider" style="color: #6BFBCE;">Graduated Control (No Sudden Blackouts)</div>
                <h3 class="text-lg font-bold text-white mt-0.5 mb-4">5-Step Action Ladder</h3>
                <div class="overflow-x-auto">
                    <table class="w-full text-left text-xs border-collapse">
                        <thead>
                            <tr style="border-bottom: 1px solid rgba(255,255,255,0.1); color: #9499B8;">
                                <th class="py-2.5 px-3">Waste Score</th>
                                <th class="py-2.5 px-3">Level</th>
                                <th class="py-2.5 px-3">What GridSense Does</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y" style="border-color: rgba(255,255,255,0.06);">
                            <tr>
                                <td class="py-2.5 px-3 font-data font-bold text-white">0 - 20</td>
                                <td class="py-2.5 px-3 text-white">Normal</td>
                                <td class="py-2.5 px-3" style="color: #E4E6F5;">No action needed. Keeps monitoring every 15 minutes.</td>
                            </tr>
                            <tr>
                                <td class="py-2.5 px-3 font-data font-bold text-white">21 - 40</td>
                                <td class="py-2.5 px-3 text-white">Low Waste</td>
                                <td class="py-2.5 px-3" style="color: #E4E6F5;">Sends a gentle reminder to the class representative or lab assistant.</td>
                            </tr>
                            <tr>
                                <td class="py-2.5 px-3 font-data font-bold" style="color: #6BFBCE;">41 - 60</td>
                                <td class="py-2.5 px-3" style="color: #6BFBCE;">Medium Waste</td>
                                <td class="py-2.5 px-3" style="color: #E4E6F5;">Raises AC temperature by 2 C, dims window-side lights, alerts department admin.</td>
                            </tr>
                            <tr>
                                <td class="py-2.5 px-3 font-data font-bold" style="color: #6BFBCE;">61 - 80</td>
                                <td class="py-2.5 px-3" style="color: #6BFBCE;">High Waste</td>
                                <td class="py-2.5 px-3" style="color: #E4E6F5;">Turns off empty-row lights, sets AC to 28 C, puts projectors/smartboards to sleep.</td>
                            </tr>
                            <tr>
                                <td class="py-2.5 px-3 font-data font-bold" style="color: #6BFBCE;">81 - 100</td>
                                <td class="py-2.5 px-3" style="color: #6BFBCE;">Critical Waste</td>
                                <td class="py-2.5 px-3" style="color: #E4E6F5;">Shuts down power to the verified empty wing and records it in the audit log.</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

        </div>

    </main>

    <script>
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

        function formatINR(num) {
            return 'INR ' + Math.round(num).toLocaleString('en-IN');
        }

        function recalcCampusROI() {
            const tariff = Math.max(1, parseFloat(document.getElementById('tariffInput').value) || 9);
            const totalMonthlyKwh = 15000;
            const monthlyInr = totalMonthlyKwh * tariff;
            const annualInr = monthlyInr * 12;

            document.getElementById('kpiMonthlyInr').innerText = formatINR(monthlyInr);
            document.getElementById('kpiAnnualInr').innerText = formatINR(annualInr) + ' saved per year';

            document.getElementById('cardInrRo').innerText = formatINR(820 * tariff) + ' / mo';
            document.getElementById('cardInrWifi').innerText = formatINR(700 * tariff) + ' / mo';
            document.getElementById('cardInrHostel').innerText = formatINR(1800 * tariff) + ' / mo';
            document.getElementById('cardInrCooler').innerText = formatINR(1620 * tariff) + ' / mo';
            document.getElementById('cardInrLabs').innerText = formatINR(2400 * tariff) + ' / mo';
        }

        window.addEventListener('DOMContentLoaded', recalcCampusROI);
    </script>
</body>
</html>
"""
