# app/api/v1/routes/auth.py

from fastapi import APIRouter, Depends
from app.services.api_key_service import api_key_service
#from app.dependencies.auth import require_user_session_admin
from typing import Optional

router = APIRouter()

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


