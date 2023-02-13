from views import (migrations, sing_up, login, get_current_user, 
                   create_contact, get_contact, show_contacts, delete_contact)


def main():
    migrations()
    
    while True:
        user = get_current_user()
        if user is None:
            action = input("Enter 1 to log in\nEnter 2 to sing up\nEnter 3 to exit\n")
            if action == '1':
                login()
            elif action == '2':
                sing_up()
            elif action == '3':
                print("Goodbye! See you soon!\n")
                break
            else:
                print("Inccorect command!\n")
        else:
            action = input("Enter 1 to create contact\nEnter 2 to find contact\nEnter 3 to get all contacts\nEnter 4 to delete contact\nEnter 5 to exit\n")
            if action == '1':
                create_contact()
            elif action == '2':
                get_contact()
            elif action == '3':
                show_contacts()
            elif action == '4':
                delete_contact()
            elif action == '5':
                print(f"Goodbye! See you soon {user.username}!\n")
                break             
            else:
                print("Inccorect command!")


if __name__ == '__main__':
    main()