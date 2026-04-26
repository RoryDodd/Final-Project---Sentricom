# app/dependencies/session_dep.py
from typing import Optional
from fastapi import Header, HTTPException, Request, status
import logging
import inspect

logger = logging.getLogger("sentricom.session_dep")
logger.addHandler(logging.NullHandler())

async def require_session(
    x_session_token: str = Header(..., alias="X-Session-Token"),
    user_agent: Optional[str] = Header(None, alias="User-Agent"),
    request: Request = None,
):
    """
    Validate a session token using the app.services.session_service module.
    Lazy-imports session_service to avoid circular imports and supports both
    sync and async validate_session implementations.
    """
    ip_address = None
    try:
        if request is not None and request.client is not None:
            ip_address = request.client.host
    except Exception:
        ip_address = None

    # Lazy import to avoid circular import problems at module import time
    try:
        from app.services.session_service import session_service
    except Exception:
        logger.exception("Failed to import session_service")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Session service unavailable")

    validate = getattr(session_service, "validate_session", None)
    if validate is None or not callable(validate):
        logger.error("session_service.validate_session not found or not callable")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Session service misconfigured")

    try:
        if inspect.iscoroutinefunction(validate):
            session = await validate(x_session_token, ip_address, user_agent)
        else:
            session = validate(x_session_token, ip_address, user_agent)
    except HTTPException:
        raise
    except Exception:
        logger.exception("Error validating session token")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Session validation error")

    if not session:
        logger.warning("Invalid or expired session token; ip=%s ua=%s", ip_address, user_agent)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session token")

    return session
