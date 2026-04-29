# app/services/api_key_service.py

import secrets
import bcrypt
from datetime import datetime, timezone
from typing import Optional
from app.db.connection import fetch_one, fetch_all, execute, execute_and_return

"""API Key Service for managing API keys for authentication and access control"""

from app.db.connection import (
    fetch_one,
    fetch_all,
    execute,
    execute_and_return
)

class APIKeyService:
    
    """
    def __init__(self):
        # key -> metadata
        self.keys = {} # to be replaced later
        '''
        api_keys (
            id,
            key_hash,
            client_name,
            created_at,
            revoked
        )
        '''
    """

    # ----- Generate new API key ----- #
    def generate_key(self, client_name: str, description: Optional[str] = None) -> str:
        """Generates a new API key for a client"""
        new_key = secrets.token_hex(32)
        # apply hash
        hashed_key = bcrypt.hashpw(new_key.encode(), bcrypt.gensalt()).decode()
        # store the key hash in db
        execute_and_return("""
            INSERT INTO keys (key_hash, client_name, description)
            VALUES (?, ?, ?)
            """,               
            (hashed_key, client_name, description)
        )
        """
        self.keys[new_key] = {
            "client_name": client_name,
            "created_at": datetime.now(datetime.timezone.utc),
            "revoked": False
        }
        """
        return new_key

    # ----- Validate plaintext key ----- #
    #def validate_key(self, key: str) -> bool:
    def validate_key(self, key: str):
        """Check if API key exists and is not revoked"""
        # Fetch all non-revoked keys
        res = fetch_all(
            "SELECT * FROM keys WHERE revoked = 0",
            ()
        )
        for r in res:
            stored_hash = r["key_hash"]
            # compare the provided key with the stored hash
            if bcrypt.checkpw(key.encode(), stored_hash.encode()):
                # Update the last used record
                execute(
                    "UPDATE keys SET last_used = ? WHERE key_id = ?",
                    (datetime.now(timezone.utc), r["key_id"])
                )
                return r
        
        #return key in self.keys and not self.keys[key]["revoked"]
        return None # May need to handle this with correct response in route handler
    
    # ----- Revoke key ----- #
    def revoke_key(self, key_id: int) -> bool:
        """Revoke an existing API key"""
        res = fetch_one(
            "SELECT * FROM keys WHERE key_id = ?",
            (key_id,))
        if not res:
            return False
        
        execute(
            "UPDATE keys SET revoked = 1 WHERE key_id = ?",
            (key_id,)
        )
        return True
    
    # ----- Delete key ----- #
    def delete_key(self, key_id: int) -> bool:
        """Permanently delete a key from system memory"""
        res = fetch_one(
            "SELECT * FROM keys WHERE key_id = ?",
            (key_id,)
        )
        if not res:
            return False

        execute(
            "DELETE FROM keys WHERE key_id = ?",
            (key_id,)
        )
        return True
    
    # ----- List keys ----- #
    def list_keys(self) -> dict:
        """List all API keys with their metadata"""
        #return self.keys.copy()
        return fetch_all(
            """
            SELECT key_id, client_name, description, created_at, revoked, last_used
            FROM keys
            ORDER BY created_at DESC
            """,
            ()
        )
    
    # ----- Get by plaintext ----- #
    def get_by_plaintext(self, key: str) -> Optional[dict]:
        """
        Compare the plaintext key provided to the match aginst key rows by comparing hash.
        Returns row dict data or none.
        """
        rows = fetch_all("SELECT * FROM keys WHERE revoked = 0", ())
        for r in rows:
            stored_hash = r["key_hash"]
            if bcrypt.checkpw(key.encode(), stored_hash.encode()):
                return r
        return None
    
# Singleton instance
api_key_service = APIKeyService()