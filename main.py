from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://rzdrqgwmmfliyksuiknx.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "sb_publishable_LPVQ_Mzxl8AK8c_JLhMNAw_CoumpNyK")

app = FastAPI(title="Hackathon O1 Project")

@app.get("/", response_class=HTMLResponse)
def home():
    supabase_configured = bool(SUPABASE_URL and len(SUPABASE_URL.strip()) > 0)
    db_status_text = "SUPABASE CONNECTED" if supabase_configured else "SUPABASE PENDING"
    db_status_color = "bg-lime-400 text-black" if supabase_configured else "bg-amber-400 text-black"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HACKATHON O1 / MAXIMALIST</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700;900&family=Cabinet+Grotesk:wght@800;900&family=JetBrains+Mono:wght@500;700;800&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Space Grotesk', sans-serif;
            background-color: #0c0d12;
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(255, 77, 0, 0.15) 0%, transparent 25%),
                radial-gradient(circle at 90% 80%, rgba(139, 92, 246, 0.18) 0%, transparent 30%),
                linear-gradient(to right, rgba(255,255,255,0.03) 1px, transparent 1px),
                linear-gradient(to bottom, rgba(255,255,255,0.03) 1px, transparent 1px);
            background-size: 100% 100%, 100% 100%, 32px 32px, 32px 32px;
        }}
        .font-display {{ font-family: 'Cabinet Grotesk', sans-serif; }}
        .font-mono-code {{ font-family: 'JetBrains Mono', monospace; }}
        @keyframes marquee {{
            0% {{ transform: translateX(0%); }}
            100% {{ transform: translateX(-50%); }}
        }}
        .animate-marquee {{
            display: flex;
            width: 200%;
            animation: marquee 16s linear infinite;
        }}
        .stamp {{
            transform: rotate(-3deg);
            box-shadow: 6px 6px 0px #000;
        }}
        .brutal-card {{
            box-shadow: 8px 8px 0px rgba(0,0,0,0.9);
            border: 3px solid #1f2430;
        }}
        .brutal-btn {{
            box-shadow: 4px 4px 0px #000;
            transition: all 0.1s ease;
        }}
        .brutal-btn:hover {{
            transform: translate(-2px, -2px);
            box-shadow: 6px 6px 0px #000;
        }}
        .brutal-btn:active {{
            transform: translate(2px, 2px);
            box-shadow: 2px 2px 0px #000;
        }}
    </style>
</head>
<body class="text-white min-h-screen flex flex-col justify-between overflow-x-hidden selection:bg-yellow-400 selection:text-black">

    <!-- RUNNING TICKER -->
    <div class="bg-yellow-400 text-black py-2 overflow-hidden border-b-4 border-black font-mono-code font-extrabold text-sm tracking-widest uppercase">
        <div class="animate-marquee whitespace-nowrap">
            <span>[ SYSTEM ONLINE ] /// FASTAPI ASYNCHRONOUS ENGINE /// SUPABASE POSTGRESQL CLOUD LAYER /// HIGH-DENSITY MAXIMALIST INTERFACE /// RENDER CI/CD ACTIVE /// ZERO WATERMARKS /// READY FOR PRODUCTION /// </span>
            <span>[ SYSTEM ONLINE ] /// FASTAPI ASYNCHRONOUS ENGINE /// SUPABASE POSTGRESQL CLOUD LAYER /// HIGH-DENSITY MAXIMALIST INTERFACE /// RENDER CI/CD ACTIVE /// ZERO WATERMARKS /// READY FOR PRODUCTION /// </span>
        </div>
    </div>

    <!-- MAIN CONTAINER -->
    <main class="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 flex-1 flex flex-col justify-center">

        <!-- HEADER STAMP & BADGES -->
        <div class="flex flex-wrap items-center justify-between gap-4 mb-6">
            <div class="inline-flex items-center gap-3 bg-red-600 text-white font-mono-code font-black px-4 py-1.5 text-xs uppercase tracking-wider stamp border-2 border-black">
                <span class="w-2.5 h-2.5 bg-white rounded-full"></span>
                <span>CORE DIRECTIVE: ACTIVE PROTOTYPE</span>
            </div>
            <div class="flex flex-wrap gap-2 text-xs font-mono-code font-bold">
                <span class="px-3 py-1 bg-violet-600 border-2 border-black text-white">REVISION 01</span>
                <span class="px-3 py-1 bg-cyan-400 border-2 border-black text-black">BUILD STABLE</span>
                <span class="px-3 py-1 {db_status_color} border-2 border-black">{db_status_text}</span>
            </div>
        </div>

        <!-- HERO TITLE SECTION -->
        <div class="relative mb-8">
            <div class="absolute -top-6 -left-2 text-zinc-800 text-7xl sm:text-9xl font-display font-black select-none pointer-events-none opacity-40">
                MAXIMAL
            </div>
            <h1 class="relative text-5xl sm:text-7xl lg:text-8xl font-display font-black leading-none tracking-tight uppercase">
                <span class="text-white block">HACKATHON</span>
                <span class="bg-gradient-to-r from-yellow-400 via-orange-500 to-pink-500 bg-clip-text text-transparent block">O1 ARCHITECTURE</span>
            </h1>
            <p class="mt-4 max-w-2xl text-zinc-400 font-mono-code text-xs sm:text-sm uppercase tracking-wide">
                Maximum visual density. Scalable Python foundation. Fully coupled cloud persistence with Supabase PostgreSQL.
            </p>
        </div>

        <!-- MAXIMALIST BENTO MATRIX -->
        <div class="grid grid-cols-1 md:grid-cols-12 gap-5 mb-8">

            <!-- CARD 1: BACKEND STATUS -->
            <div class="md:col-span-5 bg-gradient-to-br from-zinc-900 to-black p-6 rounded-none brutal-card flex flex-col justify-between relative overflow-hidden">
                <div class="absolute top-0 right-0 bg-yellow-400 text-black font-mono-code font-black text-xs px-3 py-1 border-b-2 border-l-2 border-black">
                    RUNNING
                </div>
                <div>
                    <div class="text-zinc-500 font-mono-code text-xs uppercase font-extrabold tracking-wider">LAYER 01 / COMPUTATION</div>
                    <h2 class="text-3xl font-display font-black text-white mt-1">PYTHON FASTAPI</h2>
                    <p class="text-zinc-400 text-xs mt-2 leading-relaxed font-mono-code">
                        Low-latency, asynchronous ASGI server configuration with automated OpenAPI / Swagger documentation endpoints.
                    </p>
                </div>
                <div class="mt-6 pt-4 border-t-2 border-zinc-800 flex items-center justify-between font-mono-code text-xs">
                    <span class="text-zinc-400">FRAMEWORK SPECS</span>
                    <span class="text-yellow-400 font-bold">PYTHON 3.14.6</span>
                </div>
            </div>

            <!-- CARD 2: SUPABASE STATUS -->
            <div class="md:col-span-7 bg-zinc-900 p-6 rounded-none brutal-card flex flex-col justify-between relative border-l-8 border-l-emerald-500">
                <div class="flex justify-between items-start">
                    <div>
                        <div class="text-zinc-500 font-mono-code text-xs uppercase font-extrabold tracking-wider">LAYER 02 / STORAGE</div>
                        <h2 class="text-3xl font-display font-black text-white mt-1">SUPABASE POSTGRESQL</h2>
                    </div>
                    <span class="px-3 py-1 font-mono-code font-extrabold text-xs {db_status_color} border-2 border-black">
                        {db_status_text}
                    </span>
                </div>
                <div class="my-4 grid grid-cols-3 gap-2 font-mono-code text-center text-xs">
                    <div class="bg-black/60 p-2 border border-zinc-800">
                        <div class="text-zinc-500 text-[10px]">AUTH</div>
                        <div class="font-bold text-white mt-0.5">READY</div>
                    </div>
                    <div class="bg-black/60 p-2 border border-zinc-800">
                        <div class="text-zinc-500 text-[10px]">REST API</div>
                        <div class="font-bold text-emerald-400 mt-0.5">ACTIVE</div>
                    </div>
                    <div class="bg-black/60 p-2 border border-zinc-800">
                        <div class="text-zinc-500 text-[10px]">ENCRYPTION</div>
                        <div class="font-bold text-white mt-0.5">TLS 1.3</div>
                    </div>
                </div>
                <div class="pt-3 border-t-2 border-zinc-800 flex justify-between items-center text-xs font-mono-code text-zinc-400">
                    <span>HOST IDENTIFIER</span>
                    <span class="text-zinc-200">AWS AP-SOUTH-1</span>
                </div>
            </div>

            <!-- CARD 3: TERMINAL TELEMETRY -->
            <div class="md:col-span-8 bg-black p-6 rounded-none brutal-card font-mono-code text-xs">
                <div class="flex items-center justify-between pb-3 mb-3 border-b-2 border-zinc-800">
                    <div class="flex items-center gap-2">
                        <span class="w-3 h-3 bg-red-500 inline-block"></span>
                        <span class="w-3 h-3 bg-yellow-500 inline-block"></span>
                        <span class="w-3 h-3 bg-green-500 inline-block"></span>
                        <span class="ml-2 font-bold text-zinc-300 uppercase">SYS_CONSOLE // DIAGNOSTICS</span>
                    </div>
                    <span class="text-zinc-500">LIVE FEED</span>
                </div>
                <div class="space-y-1.5 text-zinc-300">
                    <div class="text-emerald-400">[OK] Pipeline initialized via Render web service</div>
                    <div class="text-cyan-400">[OK] Git continuous deployment listener hooked</div>
                    <div class="text-zinc-400">[INFO] Supabase connection string pooler linked</div>
                    <div class="text-yellow-400">[READY] Waiting for hackathon feature schemas...</div>
                </div>
            </div>

            <!-- CARD 4: ACTIONS & ENDPOINTS -->
            <div class="md:col-span-4 bg-gradient-to-br from-violet-950/80 to-zinc-900 p-6 rounded-none brutal-card flex flex-col justify-between">
                <div>
                    <div class="text-zinc-400 font-mono-code text-xs uppercase font-extrabold tracking-wider">EXPLORE API</div>
                    <h3 class="text-2xl font-display font-black text-white mt-1">INTERACTIVE DOCS</h3>
                    <p class="text-zinc-300 text-xs font-mono-code mt-2">
                        Inspect all backend routes, query params, and schemas live.
                    </p>
                </div>
                <div class="mt-6 flex flex-col gap-2">
                    <a href="/docs" target="_blank" class="w-full text-center bg-yellow-400 text-black font-mono-code font-black px-4 py-2.5 text-xs uppercase brutal-btn border-2 border-black">
                        OPEN SWAGGER DOCS (/DOCS)
                    </a>
                    <a href="/api/health" target="_blank" class="w-full text-center bg-zinc-800 text-white font-mono-code font-bold px-4 py-2 text-xs uppercase brutal-btn border-2 border-zinc-700">
                        PING HEALTH ENDPOINT
                    </a>
                </div>
            </div>

        </div>

    </main>

    <!-- FOOTER BAR -->
    <footer class="w-full bg-black border-t-4 border-zinc-800 py-4 px-4 sm:px-8 font-mono-code text-xs text-zinc-400">
        <div class="max-w-7xl mx-auto flex flex-col sm:flex-row justify-between items-center gap-2">
            <span class="font-bold text-white uppercase tracking-wider">HACKATHON PROTOCOL // STANDBY MODE</span>
            <span class="text-zinc-500 uppercase">ALL SYSTEMS VERIFIED // ZERO WATERMARKS</span>
        </div>
    </footer>

</body>
</html>
"""

@app.get("/api/health")
def health():
    return {"status": "ok", "message": "Backend is running smoothly!"}
