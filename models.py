from datetime import datetime
from settings import connection


cursor = connection.cursor()


class Base:
    
    def __init__(self) -> None:
        self.__is_active = True
        self.__created_date = datetime.now()
        self.__updated_date = datetime.now()
        
    @property
    def is_active(self) -> bool:
        return self.__is_active
    
    @is_active.setter
    def is_active(self, is_active: bool) -> None:
        if type(is_active) == bool:
            self.__is_active = is_active
        else:
            print("Is active is not boolean!")
        
    @property
    def created_date(self) -> datetime:
        return self.__created_date
    
    @property
    def updated_date(self) -> datetime:
        return self.__updated_date
    
    @updated_date.setter
    def updated_date(self, updated_date: datetime) -> None:
        if type(updated_date) == datetime:
            self.__updated_date = updated_date
        else:
            print("Updated date not datetime data!")
            

class User(Base):
    
    def __init__(self, username: str, password: str) -> None:
        super().__init__()
        self.__username = username
        self.__password = password
        
    SESSION_USER = None    
    
    @staticmethod
    def create_schema_query():
        query = """CREATE TABLE IF NOT EXISTS client(id SERIAL PRIMARY KEY,
                username VARCHAR(20) NOT NULL UNIQUE CHECK(length(username) >= 8) CHECK(length(username) <= 20),
                password VARCHAR(20) NOT NULL CHECK(length(password) >= 8) CHECK(length(password) <= 20),
                is_active BOOLEAN NOT NULL DEFAULT True,
                created_date TIMESTAMP NOT NULL DEFAULT now(),
                updated_date TIMESTAMP NOT NULL DEFAULT now());"""
        cursor.execute(query=query)
        connection.commit()
    
    @property
    def username(self) -> str:
        return str(self.__username)
    
    @username.setter
    def username(self, username: str) -> None:
        if 8 <= len(username) <= 20:
            self.__username = username
        else:
            print("Your username len should be from 8 to 20 symboals")
        
    @property
    def password(self) -> str:
        return '*' * len(self.__password)
    
    @password.setter
    def password(self, password: str) -> None:
        if 8 <= len(password) <= 20:
            self.__password = password
        else:
            print("Your password len should be from 8 to 20 symboals")

    def check_password(self, password):
        if self.__password == password:
            return True
        return False

    def create(self) -> int:
        query = f"""INSERT INTO client(username, password) VALUES ('{self.__username}', '{self.__password}') RETURNING id;"""
        cursor.execute(query=query)
        connection.commit()
        id = cursor.fetchone()[0]
        return id

    @staticmethod
    def get_or_none(username):
        query = f"""SELECT * FROM client WHERE username = '{username}';"""
        cursor.execute(query=query)
        user_data = cursor.fetchone()
        if user_data is not None:
            user = User(
                username=user_data[1],
                password=user_data[2]
            )
            user.id = user_data[0]
            return user
        
    
class Contact(Base):
    
    def __init__(self, name, user_id: int) -> None:
        super().__init__()
        self.__name = name
        self.__user_id = user_id
        
    @staticmethod
    def create_schema_query():
        query = """CREATE TABLE IF NOT EXISTS contact(
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            user_id INTEGER NOT NULL REFERENCES client (id),
            is_active BOOLEAN NOT NULL DEFAULT True,
            created_date TIMESTAMP NOT NULL DEFAULT now(),
            updated_date TIMESTAMP NOT NULL DEFAULT now());"""
        cursor.execute(query=query)
        connection.commit()

    @property
    def name(self) -> str:
        return str(self.__name)
    
    @name.setter
    def name(self, name: str) -> None:
        self.__name = name
    
    @property
    def user_id(self) -> int:
        return self.__user_id

    @user_id.setter
    def user_id(self, user_id: int) -> None:
        self.__user_id = user_id
    
    @staticmethod
    def all(user_id: int) -> list:
        query = f"""SELECT name, string_agg(number, ', ') as phone_numbers FROM contact FULL JOIN phone_number ON contact.id = phone_number.contact_id WHERE contact.user_id = {user_id} GROUP BY name;"""
        cursor.execute(query=query)
        contacts = cursor.fetchall()
        return contacts
    
    @staticmethod
    def get_or_none(name: str, user_id: int) -> tuple or None:
        query = f"""SELECT name, string_agg(number, ', ') as phone_numbers FROM contact FULL JOIN phone_number ON contact.id = phone_number.contact_id WHERE contact.name='{name}' and contact.user_id={user_id} GROUP BY name;"""
        cursor.execute(query=query)
        contact = cursor.fetchone()
        return contact
      
    @staticmethod 
    def delete(name: str, user_id: int) -> bool:
        query_to_get_contact = f"""SELECT id FROM contact WHERE name = '{name}' and user_id={user_id};"""
        cursor.execute(query_to_get_contact)
        contact = cursor.fetchone()
        if contact is not None:
            contact_id = contact[0]
            query_to_delete_contact_phone_numbers = f"""DELETE FROM phone_number WHERE contact_id={contact_id};"""
            cursor.execute(query_to_delete_contact_phone_numbers)
            query_to_delete_contact = f"""DELETE FROM contact WHERE id={contact_id};"""
            cursor.execute(query_to_delete_contact)
            connection.commit()
            return True
        return False
        
    def create(self) -> int:
        query = f"""INSERT INTO contact(name, user_id) VALUES ('{self.__name}', '{self.__user_id}') RETURNING id;"""
        cursor.execute(query=query)
        id = cursor.fetchone()[0]
        connection.commit()
        return id

        
    
    
class PhoneNumber(Base):
    
    def __init__(self, number, contact_id) -> None:
        super().__init__()
        self.__number = number
        self.__contact_id = contact_id
        
    @staticmethod
    def create_schema_query():
        query = """CREATE TABLE IF NOT EXISTS phone_number(
            id SERIAL PRIMARY KEY, 
            number VARCHAR(10) NOT NULL CHECK (length(number) = 10),
            contact_id INTEGER NOT NULL REFERENCES contact (id),
            is_active BOOLEAN NOT NULL DEFAULT True,
            created_date TIMESTAMP NOT NULL DEFAULT now(),
            updated_date TIMESTAMP NOT NULL DEFAULT now());
            """
        cursor.execute(query=query)
        connection.commit()

    @property
    def number(self) -> str:
        return str(self.__number)
    
    @number.setter
    def number(self, number: str) -> None:
        if len(number) == 10 and number.startswith('0') and number.isdigit():
            self.__number = number
        else:
            print("Inccorect phone number format!")
    
    @property
    def contact_id(self) -> int:
        return self.__contact_id

    @contact_id.setter
    def contact_id(self, contact_id: int) -> None:
        self.__contact_id = contact_id

    @staticmethod
    def is_valid_number(number: str) -> bool:
        if len(number) == 10 and number.startswith('0') and number.isdigit():
            return True
        else:
            return False

    def create(self) -> int:
        query = f"""INSERT INTO phone_number(number, contact_id) VALUES ('{self.__number}', '{self.__contact_id}') RETURNING id;"""
        cursor.execute(query=query)
        id = cursor.fetchone()[0]
        connection.commit()
        return id
