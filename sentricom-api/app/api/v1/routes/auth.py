# app/api/v1/routes/auth.py

from fastapi import APIRouter
from app.services.api_key_service import api_key_service

router = APIRouter()

@router.post("/generate-key", tags=["Auth"])
def generate_key(client_name: str):
    """
    Generate a new API key for a client.
    """
    new_key = api_key_service.generate_key(client_name)
    return {"client": client_name, "api_key": new_key}
