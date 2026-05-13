import bcrypt
from app.db.connection import fetch_one

class AuthService:
    def authenticate_user(self, identifier: str, password: str):
        """
        Authenticate user - accepts username or email as identifier
        """
        user = fetch_one(
            """
            SELECT * FROM users WHERE username = ? OR email = ?
            LIMIT 1
            """,
            (identifier, identifier)
        )

        if not user:
            return None
        
        #compare provided password to stored hash
        password_hash = user["password_hash"]

        if not bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8")):
            return None
        
        return user
    
# exports the service instance
auth_service = AuthService()