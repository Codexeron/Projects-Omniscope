import sys
import json
import argparse
import asyncio
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

from engine import OmniOrchestrator, validate_url
from models import OmniReport

app = FastAPI(title="OmniScope API", version="1.1.0")
orchestrator = OmniOrchestrator()

# Statik dosyalar (CSS, JS) ve template'ler
static_dir = Path(__file__).parent / "static"
templates_dir = Path(__file__).parent / "templates"

if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    """Ana Dashboard sayfası"""
    index_path = templates_dir / "index.html"
    if index_path.exists():
        with open(index_path, "r", encoding="utf-8") as f:
            return f.read()
    return HTMLResponse("<h1>Dashboard not found. Please create templates/index.html</h1>")

@app.get("/analyze", response_model=OmniReport)
async def analyze_endpoint(url: str = Query(..., description="Analiz edilecek URL")):
    if not validate_url(url):
        raise HTTPException(status_code=400, detail="Geçersiz veya güvensiz URL (localhost/IP engeli)")
    
    report = await orchestrator.analyze(url)
    if report.status == "error":
        raise HTTPException(status_code=500, detail=report.error_msg or "Analiz sırasında bilinmeyen hata")
    return report

@app.get("/health")
async def health():
    return {"status": "ready", "version": "1.1.0"}

def run_cli():
    parser = argparse.ArgumentParser(description="OmniScope - Web Sitesi Analiz Aracı")
    parser.add_argument("url", help="Analiz edilecek URL")
    parser.add_argument("--json", action="store_true", help="Çıktıyı JSON formatında göster")
    args = parser.parse_args()
    
    if not validate_url(args.url):
        print(json.dumps({"error": "Geçersiz veya güvensiz URL"}, indent=2))
        sys.exit(1)
    
    report = asyncio.run(orchestrator.analyze(args.url))
    if args.json:
        print(json.dumps(report.model_dump(), indent=2, ensure_ascii=False))
    else:
        print(f"\n🔍 OmniScope Raporu: {args.url}")
        print("-" * 40)
        for k, v in report.scores.items():
            print(f"{k.upper():15} : {v}")
        print("-" * 40)
        print("Detaylar için --json parametresi ile çalıştırın.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_cli()
    else:
        uvicorn.run(app, host="127.0.0.1", port=8080, log_level="info")
