"""Database connection and operations."""

import json
from typing import Dict, List, Optional, Any
from pathlib import Path


class DatabaseConnection:
    """Simple database connection simulator."""
    
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = Path(db_path or "sample_db.json")
        self.data = self._load_data()
    
    def _load_data(self) -> Dict:
        """Load data from file."""
        if self.db_path.exists():
            try:
                with open(self.db_path, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        # Default data structure
        return {
            "users": {
                1: {
                    "id": 1,
                    "name": "Admin User",
                    "email": "admin@example.com",
                    "settings": {"theme": "dark", "notifications": True}
                },
                2: {
                    "id": 2,
                    "name": "Regular User",
                    "email": "user@example.com",
                    "settings": {"theme": "light", "notifications": False}
                },
                3: {
                    "id": 3,
                    "name": "Guest User",
                    "email": "guest@example.com",
                    "settings": {"theme": "light", "notifications": True}
                }
            },
            "logs": [],
            "sessions": {}
        }
    
    def _save_data(self) -> None:
        """Save data to file."""
        try:
            with open(self.db_path, 'w') as f:
                json.dump(self.data, f, indent=2)
        except:
            pass
    
    def get_user(self, user_id: int) -> Optional[Dict]:
        """Get user by ID."""
        return self.data["users"].get(user_id)
    
    def get_user_settings(self, user_id: int) -> Optional[Dict]:
        """Get user settings."""
        user = self.get_user(user_id)
        return user.get("settings") if user else None
    
    def get_user_logs(self, user_id: int) -> List[Dict]:
        """Get user activity logs."""
        return [
            log for log in self.data["logs"]
            if log.get("user_id") == user_id
        ]
    
    def update_user_settings(self, user_id: int, settings: Dict) -> bool:
        """Update user settings."""
        user = self.get_user(user_id)
        if not user:
            return False
        
        user["settings"].update(settings)
        self._log_action(user_id, "update_settings", settings)
        self._save_data()
        return True
    
    def update_user_profile(self, user_id: int, profile: Dict) -> bool:
        """Update user profile."""
        user = self.get_user(user_id)
        if not user:
            return False
        
        # Update allowed fields
        for field in ["name", "email"]:
            if field in profile:
                user[field] = profile[field]
        
        self._log_action(user_id, "update_profile", profile)
        self._save_data()
        return True
    
    def delete_user(self, user_id: int) -> bool:
        """Delete user."""
        if user_id in self.data["users"]:
            del self.data["users"][user_id]
            self._log_action(user_id, "delete_user", {})
            self._save_data()
            return True
        return False
    
    def clear_user_data(self, user_id: int) -> bool:
        """Clear all user data except basic info."""
        user = self.get_user(user_id)
        if not user:
            return False
        
        user["settings"] = {}
        self._log_action(user_id, "clear_data", {})
        self._save_data()
        return True
    
    def create_user(self, user_data: Dict) -> int:
        """Create new user."""
        new_id = max(self.data["users"].keys()) + 1
        user_data["id"] = new_id
        user_data["settings"] = user_data.get("settings", {})
        self.data["users"][new_id] = user_data
        self._log_action(new_id, "create_user", user_data)
        self._save_data()
        return new_id
    
    def _log_action(self, user_id: int, action: str, details: Dict) -> None:
        """Log user action."""
        log_entry = {
            "user_id": user_id,
            "action": action,
            "details": details,
            "timestamp": "2026-03-01T12:00:00Z"  # Simplified timestamp
        }
        self.data["logs"].append(log_entry)
        
        # Keep only last 100 logs per user
        user_logs = self.get_user_logs(user_id)
        if len(user_logs) > 100:
            # Remove oldest logs for this user
            self.data["logs"] = [
                log for log in self.data["logs"]
                if not (log.get("user_id") == user_id and 
                       log not in user_logs[-100:])
            ]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get database statistics."""
        return {
            "total_users": len(self.data["users"]),
            "total_logs": len(self.data["logs"]),
            "active_sessions": len(self.data.get("sessions", {})),
            "storage_size": len(str(self.data))
        }
