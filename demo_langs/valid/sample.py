"""Python - valid code."""
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class User:
    id: int
    name: str


class UserService:
    def __init__(self):
        self.users: List[User] = []

    def add_user(self, user: User) -> None:
        self.users.append(user)

    def get_user(self, user_id: int) -> Optional[User]:
        for user in self.users:
            if user.id == user_id:
                return user
        return None

    def process_users(self) -> None:
        for user in self.users:
            print(f"User: {user.name}")

    def list_users(self) -> List[User]:
        return list(self.users)

    def remove_user(self, user_id: int) -> bool:
        for i, user in enumerate(self.users):
            if user.id == user_id:
                del self.users[i]
                return True
        return False

    def count(self) -> int:
        return len(self.users)


def main():
    service = UserService()
    service.add_user(User(id=1, name="Alice"))

    user = service.get_user(1)
    if user:
        print(f"Found: {user.name}")


if __name__ == "__main__":
    main()
