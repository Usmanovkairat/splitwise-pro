"""Attach the built SPA without shadowing missing API endpoints."""
from pathlib import Path
from fastapi import HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

DIST = Path(__file__).resolve().parents[2] / "frontend" / "dist"


def mount_frontend(app, directory=DIST):
    directory = Path(directory).resolve()
    if not (directory / "index.html").is_file():
        raise RuntimeError("Frontend build missing; use the multi-stage Dockerfile")
    if (directory / "assets").is_dir():
        app.mount("/assets", StaticFiles(directory=directory / "assets"), name="assets")

    @app.get("/{full_path:path}", include_in_schema=False)
    def serve_frontend(full_path: str):
        if full_path == "api" or full_path.startswith("api/"):
            raise HTTPException(status_code=404)
        requested = (directory / full_path).resolve()
        if requested.is_relative_to(directory) and requested.is_file():
            return FileResponse(requested)
        return FileResponse(directory / "index.html")
