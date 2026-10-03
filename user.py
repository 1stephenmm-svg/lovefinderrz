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

    def __str__(self):
        return self.name
