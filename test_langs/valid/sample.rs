// Rust - valid code
struct User {
    id: u32,
    name: String,
}

impl User {
    fn new(id: u32, name: &str) -> Self {
        Self {
            id,
            name: name.to_string(),
        }
    }
}

struct UserService {
    users: Vec<User>,
}

impl UserService {
    fn new() -> Self {
        Self { users: Vec::new() }
    }

    fn add_user(&mut self, user: User) {
        self.users.push(user);
    }

    fn get_user(&self, id: u32) -> Option<&User> {
        self.users.iter().find(|u| u.id == id)
    }

    fn process_users(&self) {
        for user in &self.users {
            println!("User: {}", user.name);
        }
    }
}

fn main() {
    let mut service = UserService::new();
    service.add_user(User::new(1, "Alice"));
    
    if let Some(user) = service.get_user(1) {
        println!("Found: {}", user.name);
    }
}
