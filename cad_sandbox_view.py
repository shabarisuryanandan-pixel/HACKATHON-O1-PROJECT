"""
Interactive CAD Architectural Blueprint Sandbox View for Block B
Overlays authentic radial-arc floor plan image (CR B-101 to B-108,
Lab B-1/B-2, Seminar Hall, Computer Lab B-3, 4 Lifts, and Central Atrium)
with dynamic luminaire illumination, spatial consolidation, and automatic Telegram mobile alerts.
"""

def render_cad_sandbox_html():
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GridSense // Block B Architectural Blueprint Sandbox</title>
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

        /* Blueprint Interactive Overlay */
        .blueprint-container {
            position: relative;
            width: 100%;
            max-width: 820px;
            margin: 0 auto;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 0 24px rgba(0, 0, 0, 0.8);
        }
        .blueprint-img {
            width: 100%;
            display: block;
            filter: contrast(1.1) brightness(0.92);
        }

        /* SVG Hot-Zone Polygons */
        .zone-poly {
            transition: all 0.3s ease;
            cursor: pointer;
        }
        .poly-lit {
            fill: rgba(251, 191, 36, 0.38);
            stroke: #fbbf24;
            stroke-width: 2.5;
            filter: drop-shadow(0 0 8px rgba(251, 191, 36, 0.7));
        }
        .poly-dark {
            fill: rgba(10, 12, 16, 0.78);
            stroke: rgba(255, 255, 255, 0.1);
            stroke-width: 1;
        }
        .lift-active {
            fill: rgba(16, 185, 129, 0.55);
            stroke: #10b981;
            stroke-width: 2;
        }
        .lift-sleep {
            fill: rgba(20, 22, 28, 0.85);
            stroke: rgba(255, 255, 255, 0.15);
            stroke-width: 1;
        }
    </style>
</head>
<body class="min-h-screen p-4 sm:p-8 max-w-7xl mx-auto">

    <!-- HEADER -->
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6 pb-4 border-b border-white/5">
        <div>
            <div class="text-xs font-mono-code font-bold text-emerald-400 uppercase tracking-widest">Architectural Floor Plan // Digital Twin</div>
            <h1 class="text-2xl sm:text-3xl font-bold text-white tracking-tight mt-1">Block B: 7,500 m² Interactive Floor Plan</h1>
            <p class="text-xs text-zinc-400 font-mono-code mt-0.5">Live visual illumination overlays on the real radial architectural CAD layout</p>
        </div>
        <a href="/" class="px-4 py-2 neu-btn font-mono-code text-xs font-semibold text-zinc-300">
            Back to Dashboard
        </a>
    </div>

    <!-- MAIN GRID -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">

        <!-- LEFT COLUMN: CONTROLS & TEST PARAMS (4 COLS) -->
        <div class="lg:col-span-4 space-y-5">

            <!-- SCENARIO PRESETS -->
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

            <!-- ENVIRONMENTAL INPUTS -->
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

            <!-- OCCUPANCY SLIDERS -->
            <div class="p-4 neu-card space-y-2">
                <div class="text-xs font-mono-code uppercase text-zinc-400 font-bold mb-1">Classroom Occupancies</div>
                <div class="grid grid-cols-2 gap-2 text-[11px] font-mono-code text-zinc-400">
                    <div>
                        <div class="flex justify-between">
                            <span>CR B-101 (West):</span>
                            <span id="val_r1" class="text-white font-bold">0</span>
                        </div>
                        <input type="range" id="occ_r1" min="0" max="60" value="0" oninput="onParamChange()" class="w-full accent-blue-500 cursor-pointer">
                    </div>
                    <div>
                        <div class="flex justify-between">
                            <span>CR B-105 (East):</span>
                            <span id="val_r5" class="text-white font-bold">0</span>
                        </div>
                        <input type="range" id="occ_r5" min="0" max="60" value="0" oninput="onParamChange()" class="w-full accent-blue-500 cursor-pointer">
                    </div>
                    <div>
                        <div class="flex justify-between">
                            <span>CR B-102 (Mid):</span>
                            <span id="val_r2" class="text-white font-bold">0</span>
                        </div>
                        <input type="range" id="occ_r2" min="0" max="60" value="0" oninput="onParamChange()" class="w-full accent-blue-500 cursor-pointer">
                    </div>
                    <div>
                        <div class="flex justify-between">
                            <span>CR B-106 (Mid):</span>
                            <span id="val_r6" class="text-white font-bold">0</span>
                        </div>
                        <input type="range" id="occ_r6" min="0" max="60" value="0" oninput="onParamChange()" class="w-full accent-blue-500 cursor-pointer">
                    </div>
                    <div>
                        <div class="flex justify-between">
                            <span>CR B-103:</span>
                            <span id="val_r3" class="text-white font-bold">0</span>
                        </div>
                        <input type="range" id="occ_r3" min="0" max="60" value="0" oninput="onParamChange()" class="w-full accent-blue-500 cursor-pointer">
                    </div>
                    <div>
                        <div class="flex justify-between">
                            <span>CR B-107:</span>
                            <span id="val_r7" class="text-white font-bold">0</span>
                        </div>
                        <input type="range" id="occ_r7" min="0" max="60" value="0" oninput="onParamChange()" class="w-full accent-blue-500 cursor-pointer">
                    </div>
                    <div>
                        <div class="flex justify-between">
                            <span>CR B-104 (Far End):</span>
                            <span id="val_r4" class="text-white font-bold">0</span>
                        </div>
                        <input type="range" id="occ_r4" min="0" max="60" value="0" oninput="onParamChange()" class="w-full accent-blue-500 cursor-pointer">
                    </div>
                    <div>
                        <div class="flex justify-between">
                            <span>CR B-108 (Far End):</span>
                            <span id="val_r8" class="text-amber-400 font-bold">25</span>
                        </div>
                        <input type="range" id="occ_r8" min="0" max="60" value="25" oninput="onParamChange()" class="w-full accent-amber-500 cursor-pointer">
                    </div>
                </div>
            </div>

            <!-- AUTOMATIC TELEGRAM PING SETUP -->
            <div class="p-4 neu-card space-y-2.5">
                <div class="flex justify-between items-center">
                    <span class="text-xs font-mono-code uppercase text-zinc-400 font-bold">Automatic Mobile Alert</span>
                    <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                </div>
                <p class="text-[11px] text-zinc-500 font-mono-code leading-relaxed">
                    Enter Bot Token & Chat ID once. Any slider change or relocation will <strong>auto-ping your phone</strong> in the background.
                </p>
                <input type="text" id="tgToken" placeholder="Bot Token from @BotFather" class="w-full p-2 neu-inset text-[11px] font-mono-code text-zinc-200 outline-none">
                <input type="text" id="tgChatId" placeholder="Chat ID from @userinfobot" class="w-full p-2 neu-inset text-[11px] font-mono-code text-zinc-200 outline-none">
                <div class="flex gap-2">
                    <button onclick="saveAndTestTelegram()" class="w-full py-2 neu-btn text-xs font-mono-code font-bold text-emerald-400">
                        Test Mobile Ping
                    </button>
                </div>
                <div id="tgStatus" class="text-[10px] font-mono-code text-zinc-500 text-center"></div>
            </div>

        </div>

        <!-- RIGHT COLUMN: AUTHENTIC ARCHITECTURAL BLUEPRINT (8 COLS) -->
        <div class="lg:col-span-8 space-y-5">

            <!-- GAUGES ROW -->
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div class="p-4 neu-card">
                    <div class="text-[11px] font-mono-code uppercase text-zinc-500">Unmanaged Baseline</div>
                    <div id="baselineMeter" class="text-2xl font-bold text-red-400 mt-1">28.40 kW</div>
                    <div class="text-[11px] text-zinc-500 font-mono-code mt-0.5">Blind Power Draw</div>
                </div>

                <div class="p-4 neu-card">
                    <div class="text-[11px] font-mono-code uppercase text-zinc-500">GridSense Optimized</div>
                    <div id="optimizedMeter" class="text-2xl font-bold text-emerald-400 mt-1">6.25 kW</div>
                    <div class="text-[11px] text-zinc-500 font-mono-code mt-0.5">Adaptive Cooling & Cutoffs</div>
                </div>

                <div class="p-4 neu-card">
                    <div class="text-[11px] font-mono-code uppercase text-zinc-500">Immediate Savings Rate</div>
                    <div id="savingsMeter" class="text-2xl font-bold text-yellow-400 mt-1">22.15 kW</div>
                    <div id="inrMeter" class="text-[11px] text-emerald-400 font-mono-code mt-0.5">INR 199.35 / Hour</div>
                </div>
            </div>

            <!-- RELOCATION NUDGE CARD -->
            <div id="alertCard" class="p-4 neu-card border-l-4 border-l-yellow-400 flex items-start justify-between gap-4">
                <div>
                    <div class="flex items-center gap-2 text-xs font-mono-code font-bold text-yellow-400 uppercase">
                        <span class="w-2 h-2 rounded-full bg-yellow-400 animate-ping"></span>
                        Spatial Consolidation Nudge Triggered
                    </div>
                    <p id="alertText" class="text-xs font-mono-code text-zinc-300 mt-1">
                        Isolated class in CR B-108 (Far End). Relocate to CR B-101 near main stairs to shut down East Corridor.
                    </p>
                </div>
                <button onclick="applyConsolidation()" class="px-3.5 py-1.5 neu-btn text-xs font-mono-code font-bold text-emerald-400 shrink-0">
                    Apply Relocation
                </button>
            </div>

            <!-- AUTHENTIC CAD BLUEPRINT DISPLAY -->
            <div class="p-6 neu-card">
                <div class="flex justify-between items-center mb-4 pb-2 border-b border-white/5">
                    <div>
                        <h2 class="text-sm font-bold text-white uppercase tracking-wider font-mono-code">
                            BLOCK B // RADIAL ARCHITECTURAL BLUEPRINT
                        </h2>
                        <p class="text-[11px] text-zinc-500 font-mono-code">Built-up Area: ~7,500 m² | G+4 Floor Plan with Dynamic Luminaire & HVAC Overlays</p>
                    </div>
                    <div id="elevState" class="text-[10px] font-mono-code text-zinc-400 neu-inset px-2.5 py-1">
                        Lifts 1 & 2 Active | Lifts 3 & 4 Deep Sleep
                    </div>
                </div>

                <!-- OVERLAY CONTAINER -->
                <div class="blueprint-container">
                    <img src="/block_b_floorplan.png" alt="Block B Floor Plan" class="blueprint-img">
                    
                    <!-- SVG OVERLAY MAP (VIEWBOX 1000 x 860) -->
                    <svg viewBox="0 0 1000 860" class="absolute inset-0 w-full h-full pointer-events-none">
                        
                        <!-- CR B-101 (WEST WING TOP) -->
                        <polygon id="poly_r1" points="60,280 200,290 195,405 50,380" class="zone-poly poly-dark pointer-events-auto" onclick="selectRoom(1)"></polygon>

                        <!-- CR B-102 -->
                        <polygon id="poly_r2" points="50,400 195,420 190,520 40,510" class="zone-poly poly-dark pointer-events-auto" onclick="selectRoom(2)"></polygon>

                        <!-- CR B-103 -->
                        <polygon id="poly_r3" points="40,530 190,535 185,635 30,645" class="zone-poly poly-dark pointer-events-auto" onclick="selectRoom(3)"></polygon>

                        <!-- CR B-104 (WEST WING FAR END) -->
                        <polygon id="poly_r4" points="30,660 185,650 180,780 20,785" class="zone-poly poly-dark pointer-events-auto" onclick="selectRoom(4)"></polygon>

                        <!-- CR B-105 (EAST WING TOP) -->
                        <polygon id="poly_r5" points="800,290 940,280 950,380 805,405" class="zone-poly poly-dark pointer-events-auto" onclick="selectRoom(5)"></polygon>

                        <!-- CR B-106 -->
                        <polygon id="poly_r6" points="805,420 950,400 960,510 810,520" class="zone-poly poly-dark pointer-events-auto" onclick="selectRoom(6)"></polygon>

                        <!-- CR B-107 -->
                        <polygon id="poly_r7" points="810,535 960,530 970,645 815,635" class="zone-poly poly-dark pointer-events-auto" onclick="selectRoom(7)"></polygon>

                        <!-- CR B-108 (EAST WING FAR END) -->
                        <polygon id="poly_r8" points="815,650 970,660 980,785 820,780" class="zone-poly poly-lit pointer-events-auto" onclick="selectRoom(8)"></polygon>

                        <!-- LAB B-1 (NORTH WEST) -->
                        <polygon id="poly_lab1" points="245,145 440,150 435,320 230,300" class="zone-poly poly-dark"></polygon>

                        <!-- LAB B-2 (NORTH EAST) -->
                        <polygon id="poly_lab2" points="560,150 755,145 770,300 565,320" class="zone-poly poly-dark"></polygon>

                        <!-- SEMINAR HALL (SOUTH BASE) -->
                        <polygon id="poly_seminar" points="370,760 630,760 630,940 370,940" class="zone-poly poly-dark"></polygon>

                        <!-- LIFT 1 & 2 (WEST FLANK) -->
                        <rect id="poly_lift12" x="260" y="425" width="70" height="150" rx="6" class="lift-active"></rect>

                        <!-- LIFT 3 & 4 (EAST FLANK) -->
                        <rect id="poly_lift34" x="670" y="425" width="70" height="150" rx="6" class="lift-sleep"></rect>

                    </svg>
                </div>
            </div>

        </div>

    </div>

    <!-- JAVASCRIPT CONTROLLER -->
    <script>
        let currentRelocation = null;

        function onParamChange(autoPing = false) {
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
                renderFloorplanState(data);
                if (autoPing) triggerAutoTelegramPing(data);
            })
            .catch(err => console.error(err));
        }

        function renderFloorplanState(data) {
            document.getElementById('baselineMeter').innerText = `${data.total_baseline_kw} kW`;
            document.getElementById('optimizedMeter').innerText = `${data.total_optimized_kw} kW`;
            document.getElementById('savingsMeter').innerText = `${data.kw_saved} kW (${data.savings_percentage}%)`;
            document.getElementById('inrMeter').innerText = `INR ${data.inr_per_hour_saved} / Hour`;
            document.getElementById('elevState').innerText = data.elevator_mode;

            // Highlight rooms on the SVG blueprint
            const rooms = data.rooms;
            for (let i = 1; i <= 8; i++) {
                const r_id = `B10${i}`;
                const r = rooms[r_id];
                if (!r) continue;

                const poly = document.getElementById(`poly_r${i}`);
                if (poly) {
                    poly.setAttribute('class', r.lighting_glow ? 'zone-poly poly-lit pointer-events-auto' : 'zone-poly poly-dark pointer-events-auto');
                }
            }

            // Relocation nudge
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
                onParamChange(true); // Triggers auto mobile alert on consolidation
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
                for (let i = 1; i <= 8; i++) document.getElementById(`occ_r${i}`).value = (i === 1 || i === 5) ? 50 : 0;
            } else if (type === 'night_waste') {
                document.getElementById('timeSlider').value = 19.5;
                document.getElementById('tempSlider').value = 32;
                document.getElementById('weatherSelect').value = "Night";
                for (let i = 1; i <= 7; i++) document.getElementById(`occ_r${i}`).value = 0;
                document.getElementById(`occ_r8`).value = 25; // Far room occupied!
            }
            onParamChange(true);
        }

        function triggerAutoTelegramPing(data) {
            const token = localStorage.getItem('gs_tg_token') || document.getElementById('tgToken').value.trim();
            const chatId = localStorage.getItem('gs_tg_chatid') || document.getElementById('tgChatId').value.trim();
            if (!token || !chatId) return;

            let msg = `GridSense [JIT Block B]: Optimized State Updated at ${data.time}. Baseline: ${data.total_baseline_kw}kW | GridSense: ${data.total_optimized_kw}kW | Saving: ${data.kw_saved}kW (INR ${data.inr_per_hour_saved}/hr).`;
            if (data.relocations && data.relocations.length > 0) {
                msg += ` Alert: Class in ${data.relocations[0].from_room} relocated to ${data.relocations[0].to_room}.`;
            }

            fetch('/api/sandbox/notify-telegram', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ token: token, chat_id: chatId, message: msg })
            }).catch(e => console.error("Auto Telegram failed", e));
        }

        function saveAndTestTelegram() {
            const token = document.getElementById('tgToken').value.trim();
            const chatId = document.getElementById('tgChatId').value.trim();
            const statusDiv = document.getElementById('tgStatus');

            if (!token || !chatId) {
                statusDiv.innerText = "Please provide both Bot Token and Chat ID.";
                statusDiv.className = "text-[10px] font-mono-code text-red-400 text-center";
                return;
            }

            localStorage.setItem('gs_tg_token', token);
            localStorage.setItem('gs_tg_chatid', chatId);

            statusDiv.innerText = "Dispatching test ping to mobile...";
            statusDiv.className = "text-[10px] font-mono-code text-yellow-400 text-center";

            fetch('/api/sandbox/notify-telegram', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    token: token,
                    chat_id: chatId,
                    message: "GridSense Test Alert [JIT Block B]: Auto-ping successfully connected to your mobile phone."
                })
            })
            .then(res => res.json())
            .then(data => {
                if (data.status === "success") {
                    statusDiv.innerText = "Alert delivered. Auto-ping active for all future changes.";
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

        window.onload = () => {
            const savedToken = localStorage.getItem('gs_tg_token');
            const savedChat = localStorage.getItem('gs_tg_chatid');
            if (savedToken) document.getElementById('tgToken').value = savedToken;
            if (savedChat) document.getElementById('tgChatId').value = savedChat;
            onParamChange(false);
        };
    </script>
</body>
</html>
"""
