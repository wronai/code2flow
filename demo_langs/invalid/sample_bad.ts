// TypeScript - invalid code (syntax error)
interface User {
    id: number;
    name: string  // brak średnika
}

class UserService {
    private users: User[] = []
    
    addUser(user: User) {  // brak typu zwracanego
        this.users.push(user
    }  // brak zamknięcia nawiasu
    
    getUser(id: number) User | undefined {  // brak =>
        return this.users.find(u => u.id === id)
    }
}

const service = new UserService()
service.addUser({ id: 1, name: "Alice" }  // brak zamknięcia nawiasu i średnika
