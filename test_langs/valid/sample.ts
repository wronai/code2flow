// TypeScript - valid code
interface User {
    id: number;
    name: string;
}

class UserService {
    private users: User[] = [];

    addUser(user: User): void {
        this.users.push(user);
    }

    getUser(id: number): User | undefined {
        return this.users.find(u => u.id === id);
    }

    processUsers(): void {
        for (const user of this.users) {
            console.log(`User: ${user.name}`);
        }
    }
}

const service = new UserService();
service.addUser({ id: 1, name: "Alice" });
