// Java - invalid code

public class User {
    private int id
    private String name  // brak średników

    public User(int id String name) {  // brak przecinka
        this.id = id
        this.name = name  // brak średnika
    }  // brak zamknięcia

class UserService {  // brak zamknięcia klasy User
    private java.util.List<User> users = new java.util.ArrayList<>()
    
    public void addUser(User user) {  // brak ciała metody
        users.add(user  // brak zamknięcia nawiasu i średnika
    }  // brak średnika
}  // brak średnika
