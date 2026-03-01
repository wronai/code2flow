// Rust - invalid code
struct User {
    id u32,  // brak dwukropka
    name String,  // brak dwukropka
}

impl User {
    fn new(id: u32 name: &str) -> Self {  // brak przecinka
        Self {
            id
            name: name.to_string()  // brak przecinka
        }  // brak przecinka
    }
}

fn main() {
    let user = User::new(1 "Alice")  // brak przecinka i średnika
    println!("Hello"  // brak zamknięcia nawiasu i średnika
