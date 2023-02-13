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
            print(f"Congratulations! User {user.username} your singed up! 😁\n")
        else:
            print("Password missmatch!\n")
    else:
        print("Inncorect! Username length should be (max 20, min 10 symboals)! Try again!\n")
        
        
def login():
    print("Log In!\n\n")
    username = input("Enter your username: ").strip().lower()
    password = input("Enter your password: ")
    
    user = User.get_or_none(username=username)
    if user is not None:
        if user.check_password(password=password):
            User.SESSION_USER = user
        else:
            print("Password or username incorect 🤨!\n")
    else:
        print(f"User with {username} is not definded 😅!\n")
    
  
def create_contact():
    contact_name = input("Enter contact name (max symboals 50): ")
    contact = Contact(
        name=contact_name,
        user_id=User.SESSION_USER.id
    )
    contact_id = contact.create()
    
    numbers = []
    
    while True:
        number = input("Enter phone number (0222010101): ")
        is_valid = PhoneNumber.is_valid_number(number=number)
        if is_valid:
            number = PhoneNumber(
                    number=number,
                    contact_id=contact_id
                )
            numbers.append(number)
            
            add_additional_number = input("Enter 1 to add aditional number\nEnter 2 to finish\n")
            if add_additional_number == '2':
                break
        else:
            print("Inccorect phone number format!\n")
    
    for number in numbers:
        number.create()
    
    
def show_contacts():
    contacts = Contact.all(user_id=User.SESSION_USER.id)
    for contact in contacts:
        contact_name, phone_numbers = contact
        print(f"Contact: {contact_name} - {phone_numbers if phone_numbers is not None else 'Phones is empty! 😅'}")
    
    
def get_contact():
    name = input("Enter contact name for search (max symboals 50): ")
    contact = Contact.get_or_none(
            name=name,
            user_id=User.SESSION_USER.id
        )
    if contact is not None:
        contact_name, phone_numbers = contact
        print(f"Contact: {contact_name} - {phone_numbers}\n")
    else:
        print(f"Contact with {name} is not definded 😅!\n")
        

def delete_contact():
    name = input("Enter contact name to delete (max symboals 50): ")
    is_deleted = Contact.delete(
        name=name,
        user_id=User.SESSION_USER.id
    )
    if is_deleted:
        print(f"Contact {name} deleted success! 😁")
    else:
        print(f"Contact with {name} is not definded 😅!\n")
        
    
def get_current_user():
    return User.SESSION_USER    
