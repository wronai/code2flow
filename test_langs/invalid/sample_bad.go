package main

import "fmt"

// Go - invalid code

type User struct {
	ID   int
	Name string  // brak przecinka po polu
}

func NewUserService() *UserService {  // UserService niezdefiniowane
	return &UserService{users: make([]User, 0)}  
}

func (s *UserService) AddUser(user User) {  // s niezdefiniowane
	s.users = append(s.users user)  // brak przecinka
}  // brak zamknięcia

func main() {
	service := NewUserService()
	service.AddUser(User{ID: 1 Name: "Alice"})  // brak przecinka
	
	fmt.Printf("Hello"  // brak zamknięcia nawiasu
