"""
Vercel serverless entry: expose the FastAPI app and strip /api prefix so routes match.
"""
import os
import sys

# Ensure backend is on the path (api/ is next to backend/)
_backend = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "backend")
sys.path.insert(0, _backend)
os.chdir(_backend)

from main import app as _app


class StripAPIPrefix:
    """ASGI middleware: strip /api from path so FastAPI sees /patients, /patient/1, etc."""

    def __init__(self, app, prefix: str = "/api"):
        self.app = app
        self.prefix = prefix.rstrip("/")
        self.prefix_len = len(self.prefix)

    async def __call__(self, scope, receive, send):
        if scope.get("type") == "http" and scope.get("path", "").startswith(self.prefix):
            path = scope["path"][self.prefix_len:] or "/"
            scope = dict(scope)
            scope["path"] = path
            if "raw_path" in scope:
                scope["raw_path"] = path.encode("utf-8")
        await self.app(scope, receive, send)


app = StripAPIPrefix(_app)
