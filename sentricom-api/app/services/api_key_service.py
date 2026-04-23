# app/services/api_key_service.py

import secrets
from datetime import datetime

"""API Key Service for managing API keys for authentication and access control"""

class APIKeyService:
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

    def generate_key(self, client_name: str) -> str:
        """Generates a new API key for a client"""
        new_key = secrets.token_hex(32)
        self.keys[new_key] = {
            "client_name": client_name,
            "created_at": datetime.now(datetime.timezone.utc),
            "revoked": False
        }
        return new_key

    def validate_key(self, key: str) -> bool:
        """Check if API key exists and is not revoked"""
        return key in self.keys and not self.keys[key]["revoked"]
    
    def revoke_key(self, key: str) -> bool:
        """Revoke an existing API key"""
        if key in self.keys and not self.keys[key]["revoked"]:
            self.keys[key]["revoked"] = True
            return True
        return False
    
    def list_keys(self) -> dict:
        """List all API keys with their metadata"""
        return self.keys.copy()
    
    def delete_key(self, key: str) -> bool:
        """Permanently delete a key from system memory"""
        if key in self.keys:
            del self.keys[key]
            return True
        return False
    
# Singleton instance
api_key_service = APIKeyService()