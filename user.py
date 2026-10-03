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
        self.name = name
        self.gender = gender
        self.orientation = orientation
        self.birth_date = birth_date
        self.city = city
        self.email = email
        self.is_active = True
        self.balance = balance

    def __str__(self):
        return self.name
