// Java - valid code

public class User {
    private int id;
    private String name;

    public User(int id, String name) {
        this.id = id;
        this.name = name;
    }

    public int getId() { return id; }
    public String getName() { return name; }
}

class UserService {
    private java.util.List<User> users = new java.util.ArrayList<>();

    public void addUser(User user) {
        users.add(user);
    }

    public User getUser(int id) {
        for (User user : users) {
            if (user.getId() == id) {
                return user;
            }
        }
        return null;
    }

    public void processUsers() {
        for (User user : users) {
            System.out.println("User: " + user.getName());
        }
    }

    public static void main(String[] args) {
        UserService service = new UserService();
        service.addUser(new User(1, "Alice"));

        User user = service.getUser(1);
        if (user != null) {
            System.out.println("Found: " + user.getName());
        }
    }
}
