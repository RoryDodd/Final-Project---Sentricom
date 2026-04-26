# app/dependencies/auth.py

from fastapi import Header, HTTPException, Depends
from app.services.api_key_service import api_key_service

async def require_api_key(x_api_key: str = Header(None)):
    """Dependency to require a valid API key for protected endpoints"""
    if x_api_key is None:
        raise HTTPException(status_code=400, detail="X-API-Key header missing")
    
    if not api_key_service.validate_key(x_api_key):
        raise HTTPException(status_code=401, detail="Invalid or revoked API key")
    
    #return x_api_key #only needed if we would need to know which client is requesting.

    return True