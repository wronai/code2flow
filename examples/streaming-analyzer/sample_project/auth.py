"""Authentication module with various auth methods."""

import hashlib
import secrets
from typing import Optional, Dict, List


class AuthManager:
    """Manages user authentication and authorization."""
    
    def __init__(self):
        self.sessions: Dict[str, int] = {}
        self.users: Dict[int, Dict] = {
            1: {"password_hash": self._hash("admin123"), "role": "admin"},
            2: {"password_hash": self._hash("user123"), "role": "user"},
            3: {"password_hash": self._hash("guest123"), "role": "guest"},
        }
    
    def _hash(self, password: str) -> str:
        """Hash password with salt."""
        salt = secrets.token_hex(16)
        return hashlib.sha256(f"{salt}{password}".encode()).hexdigest()
    
    def authenticate(self, user_id: int, password: Optional[str] = None) -> bool:
        """Authenticate user."""
        if user_id not in self.users:
            return False
        
        if password:
            return self._verify_password(user_id, password)
        
        # For demo, accept any known user without password
        return True
    
    def _verify_password(self, user_id: int, password: str) -> bool:
        """Verify user password."""
        user = self.users.get(user_id)
        if not user:
            return False
        
        # Simplified verification for demo
        return password in ["admin123", "user123", "guest123"]
    
    def create_session(self, user_id: int) -> str:
        """Create user session."""
        session_id = secrets.token_urlsafe(32)
        self.sessions[session_id] = user_id
        return session_id
    
    def validate_session(self, session_id: str) -> Optional[int]:
        """Validate session and return user ID."""
        return self.sessions.get(session_id)
    
    def revoke_session(self, session_id: str) -> bool:
        """Revoke user session."""
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False
    
    def get_user_role(self, user_id: int) -> str:
        """Get user role."""
        user = self.users.get(user_id)
        return user.get("role", "unknown") if user else "unknown"
    
    def has_permission(self, user_id: int, resource: str, action: str) -> bool:
        """Check if user has permission for resource/action."""
        role = self.get_user_role(user_id)
        
        permissions = {
            "admin": ["read", "write", "delete"],
            "user": ["read", "write"],
            "guest": ["read"],
        }
        
        allowed_actions = permissions.get(role, [])
        return action in allowed_actions
    
    def list_active_sessions(self) -> List[Dict]:
        """List all active sessions."""
        sessions = []
        for session_id, user_id in self.sessions.items():
            sessions.append({
                "session_id": session_id[:8] + "...",
                "user_id": user_id,
                "role": self.get_user_role(user_id)
            })
        return sessions
