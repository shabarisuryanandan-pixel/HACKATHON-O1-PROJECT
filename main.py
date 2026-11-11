from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Hackathon O1 Project")

@app.get("/", response_class=HTMLResponse)
def home():
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_configured = bool(supabase_url and len(supabase_url.strip()) > 0)
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Hackathon O1 - Live App</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
        <style>
            body {{ font-family: 'Plus Jakarta Sans', sans-serif; }}
        </style>
    </head>
    <body class="bg-slate-950 text-slate-100 min-h-screen flex items-center justify-center p-6">
        <div class="max-w-xl w-full bg-slate-900 border border-slate-800 rounded-3xl p-8 shadow-2xl text-center space-y-6">
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-semibold uppercase tracking-wider">
                <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span> Live & Ready
            </div>
            
            <h1 class="text-4xl font-extrabold tracking-tight bg-gradient-to-r from-blue-400 via-indigo-400 to-purple-400 bg-clip-text text-transparent">
                Hackathon O1 Project
            </h1>
            
            <p class="text-slate-400 text-sm leading-relaxed">
                Full-stack Python backend powered by FastAPI & Supabase PostgreSQL cloud database. 
                Ready to build tomorrow's winning prototype!
            </p>

            <div class="grid grid-cols-2 gap-4 text-left pt-2">
                <div class="p-4 rounded-2xl bg-slate-800/60 border border-slate-700/50">
                    <div class="text-xs text-slate-400 uppercase font-semibold">Backend</div>
                    <div class="text-base font-bold text-slate-200 mt-1">Python FastAPI 🚀</div>
                </div>
                <div class="p-4 rounded-2xl bg-slate-800/60 border border-slate-700/50">
                    <div class="text-xs text-slate-400 uppercase font-semibold">Database</div>
                    <div class="text-base font-bold text-emerald-400 mt-1">
                        {"Supabase Connected ✅" if supabase_configured else "Supabase Pending ⏳"}
                    </div>
                </div>
            </div>

            <div class="pt-4 border-t border-slate-800 text-xs text-slate-500 flex justify-between items-center">
                <span>Status: All Systems Operational</span>
                <span class="text-slate-400 font-mono">v1.0.0</span>
            </div>
        </div>
    </body>
    </html>
    """

@app.get("/api/health")
def health():
    return {"status": "ok", "message": "Backend is running smoothly!"}
