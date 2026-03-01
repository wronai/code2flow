"""API handler for external requests."""

import json
from typing import Dict, Any, Optional
from .database import DatabaseConnection


class APIHandler:
    """Handles API requests and responses."""
    
    def __init__(self):
        self.db = DatabaseConnection()
        self.rate_limits: Dict[str, int] = {}
    
    def process_request(self, request) -> Dict[str, Any]:
        """Process API request."""
        # Check rate limits
        if not self._check_rate_limit(request.user_id):
            return {"error": "Rate limit exceeded"}
        
        # Route request
        if request.action == "api_stats":
            return self._get_stats()
        elif request.action == "api_user_info":
            return self._get_user_info(request.user_id)
        elif request.action == "api_health":
            return self._health_check()
        else:
            return {"error": "Unknown API action"}
    
    def _check_rate_limit(self, user_id: int) -> bool:
        """Check if user exceeded rate limit."""
        key = str(user_id)
        self.rate_limits[key] = self.rate_limits.get(key, 0) + 1
        
        # Reset counter if too many requests
        if self.rate_limits[key] > 10:
            return False
        
        return True
    
    def _get_stats(self) -> Dict[str, Any]:
        """Get API statistics."""
        stats = self.db.get_stats()
        return {
            "status": "ok",
            "data": stats,
            "api_version": "1.0"
        }
    
    def _get_user_info(self, user_id: int) -> Dict[str, Any]:
        """Get user information."""
        user = self.db.get_user(user_id)
        if not user:
            return {"error": "User not found"}
        
        return {
            "status": "ok",
            "data": {
                "id": user["id"],
                "name": user["name"],
                "settings": user["settings"]
            }
        }
    
    def _health_check(self) -> Dict[str, Any]:
        """API health check."""
        return {
            "status": "healthy",
            "timestamp": "2026-03-01T12:00:00Z",
            "version": "1.0.0"
        }
    
    def format_response(self, data: Dict[str, Any]) -> str:
        """Format API response."""
        return json.dumps(data, indent=2)
