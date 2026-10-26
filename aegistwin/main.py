"""FastAPI application entrypoint for Vercel deployment."""
import sys
from pathlib import Path

# Add current directory and repo root to Python path
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from aegistwin.serving.api import app

# Export app for ASGI / Vercel
__all__ = ["app"]
