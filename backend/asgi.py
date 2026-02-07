"""ASGI entrypoint for Quart (async)."""
from app import app

# For: hypercorn asgi:app
__all__ = ["app"]
