<?php
// PHP - invalid code

class User {
    public int $id
    public string $name  // brak średników

    public function __construct(int $id, string $name) {  // brak ciała
        $this->id = $id
        $this->name = $name  // brak średnika
    }  // brak zamknięcia

class UserService {  // brak zamknięcia klasy User
    private array $users = []
    
    public function addUser(User $user  // brak zamknięcia nawiasu
        $this->users[] = $user  // brak średnika
    }  // brak średnika
}  // brak średnika

$service = new UserService()
$service->addUser(new User(1, "Alice"))  // brak średnika
