"""Serve the compiled Vite frontend and the existing API in one process."""
from pathlib import Path
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from .main import app

DIST = Path(__file__).resolve().parents[2] / "frontend" / "dist"
if not (DIST / "index.html").is_file():
    raise RuntimeError("Frontend build missing; use the multi-stage Dockerfile")

assets = DIST / "assets"
if assets.exists():
    app.mount("/assets", StaticFiles(directory=assets), name="assets")

@app.get("/{full_path:path}", include_in_schema=False)
def serve_frontend(full_path: str):
    if full_path.startswith("api/"):
        from fastapi import HTTPException
        raise HTTPException(status_code=404)
    requested = (DIST / full_path).resolve()
    if requested.is_relative_to(DIST.resolve()) and requested.is_file():
        return FileResponse(requested)
    return FileResponse(DIST / "index.html")
