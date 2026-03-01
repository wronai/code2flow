package main

import "fmt"

// Go - valid code

type User struct {
	ID   int
	Name string
}

type UserService struct {
	users []User
}

func NewUserService() *UserService {
	return &UserService{users: make([]User, 0)}
}

func (s *UserService) AddUser(user User) {
	s.users = append(s.users, user)
}

func (s *UserService) GetUser(id int) (*User, bool) {
	for i := range s.users {
		if s.users[i].ID == id {
			return &s.users[i], true
		}
	}
	return nil, false
}

func (s *UserService) ProcessUsers() {
	for _, user := range s.users {
		fmt.Printf("User: %s\n", user.Name)
	}
}

func main() {
	service := NewUserService()
	service.AddUser(User{ID: 1, Name: "Alice"})

	if user, found := service.GetUser(1); found {
		fmt.Printf("Found: %s\n", user.Name)
	}
}
