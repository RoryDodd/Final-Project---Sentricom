# app/main.py

from fastapi import FastAPI
from app.api.v1.routes import health

app = FastAPI()

# Default root welcome 
@app.get("/")
def read_root():
    return {"message": "Sentricom API is running"}

# Health check
app.include_router(health.router, prefix="/api/v1")

