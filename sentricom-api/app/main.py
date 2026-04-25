# app/main.py

from fastapi import FastAPI
from app.api.v1.routes import health
from app.api.v1.routes import zones
from app.api.v1.routes import auth
from fastapi.middleware.cors import CORSMiddleware
import os
import sys
print("app.api.v1.routes module file:", sys.modules.get("app.api.v1.routes").__file__)
print("app.api.v1.routes.auth in sys.modules:", "app.api.v1.routes.auth" in sys.modules)
if "app.api.v1.routes.auth" in sys.modules:
    print("auth router file:", sys.modules["app.api.v1.routes.auth"].__file__)
print("app.dependencies.auth_dep in sys.modules:", "app.dependencies.auth_dep" in sys.modules)
if "app.dependencies.auth_dep" in sys.modules:
    print("auth_dep file:", sys.modules["app.dependencies.auth_dep"].__file__)

app = FastAPI()

# configure allowed origins via env var, fallback to local + deployed frontend
origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,https://afert-umber.vercel.app")
origins = [o.strip() for o in origins.split(",") if o.strip()]

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    #allow_origins=["*"],
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Default root welcome 
@app.get("/")
def read_root():
    return {"message": "Sentricom API is running"}

# Health check
app.include_router(health.router, prefix="/api/v1")
# Zones
app.include_router(zones.router, prefix="/api/v1")
# Auth
app.include_router(auth.router, prefix="/api/v1/auth")

# DEBUG
for r in app.routes:
    print(f"ROUTE: {r.name} -> {r.path} [{','.join(sorted(r.methods))}]")

# DB initialisation if it doesn't exist
if not os.path.exists("/tmp/sentricom.db"):
    from app.db.init_db import init_db
    init_db()