from models import User, Contact, PhoneNumber



def migrations():
    User.create_schema_query()
    Contact.create_schema_query()
    PhoneNumber.create_schema_query()
    
    
def sing_up():
    print("Sing up!\n\n")
    username = input("Enter username (max 20, min 10 symboals): ").strip().lower()
    password_one = input("Enter password (max 20, min 10 symboals): ")
    password_two = input("Password confirm: ")
    
    if 8 <= len(username) <= 20:
        if password_one == password_two:
            user = User(
                username=username,
                password=password_two
            )
            user.create()
            print(f"Congratulations! User {user.username} your singed up! 😁")
        else:
            print("Password missmatch!")
    else:
        print("Inncorect! Username length should be (max 20, min 10 symboals)! Try again!")
        
        
def login():
    print("Log In!\n\n")
    username = input("Enter your username: ").strip().lower()
    password = input("Enter your password: ")
    
    user = User.get_or_none(username=username)
    if user is not None:
        if user.check_password(password=password):
            User.SESSION_USER = user
        else:
            print("Password or username incorect 🤨!")
    else:
        print(f"User with {username} is not definded 😅!")
    
    
def get_current_user():
    return User.SESSION_USER    
 