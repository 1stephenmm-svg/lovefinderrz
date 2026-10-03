from datetime import date

from validator_collection import checkers

from location import get_random_location


class User:
    def __init__(
        self,
        name,
        gender,
        orientation,
        birth_date,
        email,
        city,
        balance=0,
    ):
        self.validate_gender(gender)
        self.validate_sexual_orientation(orientation)
        self.validate_email(email)
        self.validate_birth_date(birth_date)

        self.name = name
        self.gender = gender
        self.orientation = orientation
        self.birth_date = birth_date
        self.city = city
        self.email = email
        self.is_active = True
        self.balance = balance

    @staticmethod
    def validate_gender(gender):
        if gender not in ("F", "M"):
            raise ValueError("Opción inválida")

    @staticmethod
    def validate_sexual_orientation(orientation):
        if orientation not in ("H", "O"):
            raise ValueError("Opción inválida")

    @staticmethod
    def validate_email(email):
        if not checkers.is_email(email):
            raise ValueError("Email inválido")

    @staticmethod
    def validate_birth_date(birth_date):
        if birth_date > date.today():
            raise ValueError("¿Vienes del futuro?")

        today = date.today()
        age = today.year - birth_date.year

        if (today.month, today.day) < (
            birth_date.month,
            birth_date.day,
        ):
            age -= 1

        if age < 18:
            raise ValueError("Debes ser mayor de edad para registrarte.")

    @classmethod
    def create(cls, name, gender, orientation, birth_date, email, city):
        location = get_random_location(city)

        return cls(
            name, gender, orientation, birth_date, email, city, location
        )

    def __str__(self):
        return self.name
