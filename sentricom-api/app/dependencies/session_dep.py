# app/dependencises/session_dep.py

from fastapi import Header, HTTPException, Request, Depends
from app.services.session_service import SessionService

async def require_session(
        request: Request,
        x_session_token: str = Header(None, alias="X-Session-Token")
):
    """
    Dependency to require a valid session token.
    Validates Token, IP and User Agent
    """
    if not x_session_token:
        raise HTTPException(status_code=401, detail="X-Session-Token header missing")
    
    client_ip = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent", "")

    session = session_service.validate_session(
        session_token=x_session_token,
        ip_address=client_ip or "",
        user_agent=user_agent or "",
    )

    if not session:
        raise HTTPException(status_code=401, detail="Invalid or expired session")
    
    return session
