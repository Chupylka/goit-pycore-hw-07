from collections import UserDict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Name is a required field")
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        self.validate_phone(value)
        super().__init__(value)

    @staticmethod
    def validate_phone(value):
        if not (value.isdigit() and len(value) == 10):
            raise ValueError("Phone number must be 10 digits")


class Birthday(Field):
    def __init__(self, value):
        self.value = self.validate_birthday(value)

    @staticmethod
    def validate_birthday(value):
        try:
            return datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone_number):
        phone = Phone(phone_number)
        self.phones.append(phone)

    def remove_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                self.phones.remove(phone)
                return True
        return False

    def edit_phone(self, old_number, new_number):
        for phone in self.phones:
            if phone.value == old_number:
                phone.value = new_number
                return True
        return False

    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        birthday_str = f", birthday: {self.birthday.value.strftime('%d.%m.%Y')}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}{birthday_str}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return True
        return False

    def get_upcoming_birthdays(self):
        upcoming_birthdays = []
        today = datetime.now()
        next_week = today + timedelta(days=7)
        
        for record in self.data.values():
            if record.birthday:
                birthday_this_year = record.birthday.value.replace(year=today.year)
                if today <= birthday_this_year < next_week:
                    upcoming_birthdays.append(record.name.value)
        
        return upcoming_birthdays

    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())


if __name__ == "__main__":
    book = AddressBook()
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    john_record.add_birthday("15.11.1990")  

    book.add_record(john_record)

    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    jane_record.add_birthday("20.11.1992")  
    book.add_record(jane_record)

    print("Entries in the address book:")
    print(book)

    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print("\nAfter editing the phone in John:")
    print(john)

    found_phone = john.find_phone("5555555555")
    print(f"\nPhone search 5555555555 for John: {found_phone}")

    upcoming_birthdays = book.get_upcoming_birthdays()
    print("\nUpcoming birthdays next week:", upcoming_birthdays)

    book.delete("Jane")
    print("\nAfter deleting the record Jane:")
    print(book)