"""Main entry point with complex logic."""

import sys
from dataclasses import dataclass
from typing import List, Optional

from .auth import AuthManager
from .database import DatabaseConnection
from .api import APIHandler
from .utils import validate_input, format_output


@dataclass
class UserRequest:
    """User request data structure."""
    user_id: int
    action: str
    data: dict
    priority: int = 1


class Application:
    """Main application class with multiple responsibilities."""
    
    def __init__(self):
        self.auth = AuthManager()
        self.db = DatabaseConnection()
        self.api = APIHandler()
        self.running = False
    
    def start(self) -> None:
        """Start the application."""
        self.running = True
        print("Application started")
        
        while self.running:
            try:
                request = self.get_next_request()
                if request:
                    self.process_request(request)
                else:
                    self.running = False
            except KeyboardInterrupt:
                print("Shutting down...")
                self.running = False
    
    def get_next_request(self) -> Optional[UserRequest]:
        """Get next request from queue."""
        # Simulate request processing
        if hasattr(self, '_request_count'):
            self._request_count += 1
        else:
            self._request_count = 1
        
        if self._request_count > 5:
            return None
        
        return UserRequest(
            user_id=self._request_count,
            action=f"action_{self._request_count}",
            data={"test": "data"}
        )
    
    def process_request(self, request: UserRequest) -> None:
        """Process a user request with complex logic."""
        # Validate input
        if not validate_input(request.data):
            print(f"Invalid input for request {request.user_id}")
            return
        
        # Authenticate
        if not self.auth.authenticate(request.user_id):
            print(f"Authentication failed for user {request.user_id}")
            return
        
        # Route to appropriate handler
        if request.action.startswith("get_"):
            self.handle_get_request(request)
        elif request.action.startswith("set_"):
            self.handle_set_request(request)
        elif request.action.startswith("delete_"):
            self.handle_delete_request(request)
        else:
            self.handle_default_request(request)
    
    def handle_get_request(self, request: UserRequest) -> None:
        """Handle GET requests."""
        resource = request.action.replace("get_", "")
        
        if resource == "user":
            data = self.db.get_user(request.user_id)
        elif resource == "settings":
            data = self.db.get_user_settings(request.user_id)
        elif resource == "logs":
            data = self.db.get_user_logs(request.user_id)
        else:
            data = {"error": "Unknown resource"}
        
        formatted = format_output(data)
        print(f"GET result: {formatted}")
    
    def handle_set_request(self, request: UserRequest) -> None:
        """Handle SET requests."""
        resource = request.action.replace("set_", "")
        
        if resource == "settings":
            success = self.db.update_user_settings(request.user_id, request.data)
        elif resource == "profile":
            success = self.db.update_user_profile(request.user_id, request.data)
        else:
            success = False
        
        if success:
            print(f"SET {resource} successful")
        else:
            print(f"SET {resource} failed")
    
    def handle_delete_request(self, request: UserRequest) -> None:
        """Handle DELETE requests."""
        resource = request.action.replace("delete_", "")
        
        if resource == "account":
            success = self.db.delete_user(request.user_id)
        elif resource == "data":
            success = self.db.clear_user_data(request.user_id)
        else:
            success = False
        
        if success:
            print(f"DELETE {resource} successful")
        else:
            print(f"DELETE {resource} failed")
    
    def handle_default_request(self, request: UserRequest) -> None:
        """Handle unknown requests."""
        print(f"Unknown action: {request.action}")
        
        # Try to process via API
        try:
            result = self.api.process_request(request)
            print(f"API result: {result}")
        except Exception as e:
            print(f"API error: {e}")


def main():
    """Main entry point."""
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("Sample application for streaming analyzer demo")
        print("Usage: python main.py")
        return
    
    app = Application()
    app.start()


if __name__ == "__main__":
    main()
