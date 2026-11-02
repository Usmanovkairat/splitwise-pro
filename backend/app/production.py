"""Serve the compiled Vite frontend and the existing API in one process."""
from .main import app
from .static_frontend import mount_frontend

mount_frontend(app)
