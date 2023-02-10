from views import migrations, sing_up, login, get_current_user


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
                print("Goodbye! See you soon!")
                break
            else:
                print("Inccorect command!")
        else:
            action = input("Enter 1 to create contact\nEnter 2 to exit\n")
            if action == '1':
                pass
            elif action == '2':
                print(f"Goodbye! See you soon {user.username}!")
                break             
            else:
                print("Inccorect command!")


if __name__ == '__main__':
    main()