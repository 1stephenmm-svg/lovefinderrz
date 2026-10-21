import re

from datetime import date, datetime

from validator_collection import checkers

from location import get_random_location


class User:
    def __init__(self, id, nickname, email, balance=0, created_at=None):
        self.validate_nickname(nickname)
        self.validate_email(email)

        self.id = id
        self.nickname = nickname
        self.email = email
        self.balance = balance
        self.is_active = True
        self.created_at = created_at or datetime.now()

    # Validations

    @staticmethod
    def validate_nickname(nickname):
        if not 3 <= len(nickname) <= 20:
            raise ValueError("Debe tener entre 3 y 20 caracteres de longitud.")
        if not re.fullmatch(r"[a-z0-9._-]+", nickname):
            raise ValueError(
                "Sólo puede contener letras, numeros, puntos o guiones."
            )
        if not re.match(r"[a-z0-9]+", nickname) or not re.search(
            r"[a-z0-9]+$", nickname
        ):
            raise ValueError(
                "Tu nickname debe comenzar y terminar con letras o números."
            )

    @staticmethod
    def validate_email(email):
        if not checkers.is_email(email):
            raise ValueError("Email inválido")

    # Properties

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        self.validate_email(email)
        self._email = email

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, balance):
        if balance < 0:
            raise ValueError("El balance no puede ser negativo.")

        self._balance = balance

    # Factory

    @classmethod
    def create(cls, id, nickname, email, **kwargs):
        return cls(
            id=id,
            nickname=nickname,
            email=email,
            **kwargs,
        )

    # Representation

    def __str__(self):
        return self.nickname


class Admin(User):
    def __init__(
        self,
        id,
        nickname,
        email,
        balance=0,
        created_at=None,
        password_hash=None,
        password_salt=None,
    ):
        super().__init__(id, nickname, email, balance, created_at)

        self.password_hash = password_hash
        self.password_salt = password_salt

    def __str__(self):
        return f"{self.nickname.upper()} MI AMO Y SEÑOR"


class Client(User):
    def __init__(
        self,
        id,
        nickname,
        gender,
        orientation,
        birth_date,
        email,
        city,
        location,
        balance=0,
        created_at=None,
    ):
        super().__init__(id, nickname, email, balance, created_at)

        self.validate_gender(gender)
        self.validate_sexual_orientation(orientation)
        self.validate_birth_date(birth_date)

        self.gender = gender
        self.orientation = orientation
        self.birth_date = birth_date
        self.city = city
        self.location = location
        self.is_blocked = False
        self.same_orientation = True
        self.same_location = True

    # Validations

    @staticmethod
    def validate_gender(gender):
        if gender not in ("F", "M"):
            raise ValueError("Opción inválida. Ingresa F o M.")

    @staticmethod
    def validate_sexual_orientation(orientation):
        if orientation not in ("H", "O"):
            raise ValueError("Opción inválida. Ingresa H u O.")

    @staticmethod
    def validate_birth_date(birth_date):
        if birth_date > date.today():
            raise ValueError("¿Vienes del futuro?")

        if Client.calculate_age(birth_date) < 18:
            raise ValueError("Debes ser mayor de edad para registrarte.")

        if birth_date.year <= 1900:
            raise ValueError("¿Eres el hijo famoso de Enoc?")

    # Calculations

    @staticmethod
    def calculate_age(birth_date):
        today = date.today()

        age = today.year - birth_date.year

        if (today.month, today.day) < (
            birth_date.month,
            birth_date.day,
        ):
            age -= 1

        return age

    # client actions

    def update_preferences(self, same_orientation, same_location):
        self.same_orientation = same_orientation
        self.same_location = same_location

    # Properties

    @property
    def age(self):
        return Client.calculate_age(self.birth_date)

    # Factory

    @classmethod
    def create(
        cls,
        id,
        nickname,
        gender,
        orientation,
        birth_date,
        email,
        city,
        **kwargs,
    ):
        location = get_random_location(city)

        return cls(
            id=id,
            nickname=nickname,
            gender=gender,
            orientation=orientation,
            birth_date=birth_date,
            email=email,
            city=city,
            location=location,
            **kwargs,
        )

    # Representation

    def __str__(self):
        return self.nickname
