from datetime import datetime


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


class Contact(Base):
    
    def __init__(self, name, user_id: int) -> None:
        super().__init__()
        self.__name = name
        self.__user_id = user_id
        
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
        
    
class PhoneNumber(Base):
    
    def __init__(self, phone_number, contact_id) -> None:
        super().__init__()
        self.__phone_number = phone_number
        self.__contact_id = contact_id
            
    @property
    def phone_number(self) -> str:
        return str(self.__phone_number)
    
    @phone_number.setter
    def name(self, phone_number: str) -> None:
        if len(phone_number) == 10 and phone_number.startswith('0') and phone_number.isdigit():
            self.__phone_number = phone_number
        else:
            print("Inccorect phone number format!")
    
    @property
    def contact_id(self) -> int:
        return self.__contact_id

    @contact_id.setter
    def contact_id(self, contact_id: int) -> None:
        self.__contact_id = contact_id
