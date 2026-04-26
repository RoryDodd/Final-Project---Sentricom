# app/api/v1/routes/auth.py

from fastapi import APIRouter, HTTPException, Request, Depends
from app.services.api_key_service import api_key_service
from app.services.session_service import session_service, SESSION_LIFETIME_HOURS
#from app.dependencies.auth import require_user_session_admin
from typing import Optional

router = APIRouter(prefix="/auth", tags=["Auth"])

# Debug
# print("Loaded routes/auth.py")

# ----- Generate key ----- #
@router.post("/generate-key", tags=["Auth"])
#def generate_key(client_name: str, description: Optional[str] = None, admin: bool = Depends(require_user_session_admin)): # to be implemented later
def generate_key(client_name: str, description: Optional[str] = None):
    """
    Admin User: Generate a new API key for a client.
    Returns one-time plaintext key that should be securely stored by the client
    """
    new_key = api_key_service.generate_key(client_name, description)
    return {
        "client": client_name, 
        "api_key": new_key
    }

# ----- List keys ----- #
@router.get("/list-keys", tags=["Auth"])
def list_keys():
    return api_key_service.list_keys()

# ----- Revoke key ----- #
@router.post("/key/{key_id}/revoke")
def revoke_key(key_id: int):
    ok = api_key_service.revoke_key(key_id)
    return {"success": ok}

# ----- Delete key ----- #
@router.delete("/key/{key_id}/delete")
def delete_key(key_id: int):
    ok = api_key_service.delete_key(key_id)
    return {"success": ok}

# ----- Create session ----- #
@router.post("/session")
async def create_session(request: Request):
    """
    Exchange valid API key for a session token.
    Expects X-API-Key header
    """
    api_key = request.headers.get("X-API-Key")
    if not api_key:
        raise HTTPException(status_code=400, detail="X-API-Key header missing")
    
    api_key_rec = api_key_service.get_by_plaintext(api_key)
    if not api_key_rec:
        raise HTTPException(status_code=401, detail="API key invalid or revoked")
    
    client_ip = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent", "")

    token = session_service.create_session(
        api_key_rec["key_id"],
        ip_address=client_ip,
        user_agent=user_agent,
    )

    return {
        "session_token": token,
        "expires_in_hours": SESSION_LIFETIME_HOURS
    }

