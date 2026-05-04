# app/services/session_service.py

import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional

from app.db.connection import fetch_one, execute, execute_and_return

SESSION_LIFETIME_HOURS = 24

class SessionService:
    
    def create_session(self, key_id: int, user_id: int, ip_address: str, user_agent: str) -> str:
        """
        Create a new session for a given Client key
        Returns session token
        """

        session_token = secrets.token_hex(32)
        now = datetime.now(timezone.utc)
        expires_at = now + timedelta(hours=SESSION_LIFETIME_HOURS)

        execute_and_return("""
            INSERT INTO sessions (key_id, user_id, session_token, ip_address, user_agent, created_at, expires_at, active)
            VALUES (?, ?, ?, ?, ?, ?, ?, 1)
            """,
            (key_id, user_id, session_token, ip_address, user_agent, now, expires_at)
        )
        
        return session_token
    
    def validate_session(self, session_token: str, ip_address: str, user_agent: str) -> Optional[dict]:
        """
        Validate a session token and return row dict session info if valid, otherwise None
        """
        rec = fetch_one("""
            SELECT * FROM sessions
            WHERE session_token = ?
            """,
            (session_token,)
        )
        if not rec:
            return None
        
        if not rec["active"]:
            return None
        
        now = datetime.now(timezone.utc)
        if rec["expires_at"] is not None:
            # ISO SQLite timestamp
            expires_at = datetime.fromisoformat(rec["expires_at"])
            if expires_at <= now:
                return None

        # Python syntax here for checking null first before comparing to value (silly pthon way of doing isnull etc)
        if rec["ip_address"] and rec["ip_address"] != ip_address:
            return None
        
        if rec["user_agent"] and rec["user_agent"] != user_agent:
            return None
        
        # no last used time for session token, api key already stores last used.

        return rec
    
    def revoke_session(self, session_token: str) -> bool:
        execute("""
            UPDATE sessions
            SET active = 0
            WHERE session_token = ?
            """, 
            (session_token,)
        )
        
session_service = SessionService()