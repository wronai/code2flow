<?php
// PHP - valid code

class User {
    public int $id;
    public string $name;

    public function __construct(int $id, string $name) {
        $this->id = $id;
        $this->name = $name;
    }
}

class UserService {
    private array $users = [];

    public function addUser(User $user): void {
        $this->users[] = $user;
    }

    public function getUser(int $id): ?User {
        foreach ($this->users as $user) {
            if ($user->id === $id) {
                return $user;
            }
        }
        return null;
    }

    public function processUsers(): void {
        foreach ($this->users as $user) {
            echo "User: {$user->name}\n";
        }
    }
}

$service = new UserService();
$service->addUser(new User(1, "Alice"));

$user = $service->getUser(1);
if ($user !== null) {
    echo "Found: {$user->name}\n";
}
?>
