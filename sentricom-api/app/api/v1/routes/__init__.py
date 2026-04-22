# app/api/v1/routes/__init__.py
# (designates this folder as a Python package)
# (if no router in folder you don't need the router export syntax)
from .health import router as health_router
from .auth import router as auth_router
