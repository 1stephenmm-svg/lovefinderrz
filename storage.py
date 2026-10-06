import csv

FILE = "data/users.csv"
FIELDS = [
    "name",
    "gender",
    "orientation",
    "birth_date",
    "city",
    "email",
    "latitude",
    "longitude",
    "balance",
    "is_active",
]


def save_user(user):
    latitude, longitude = user.location
    with open(FILE, "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)

        if file.tell() == 0:
            writer.writeheader()

        writer.writerow(
            {
                "name": user.name,
                "gender": user.gender,
                "orientation": user.orientation,
                "birth_date": user.birth_date,
                "city": user.city,
                "email": user.email,
                "latitude": latitude,
                "longitude": longitude,
                "balance": user.balance,
                "is_active": user.is_active,
            }
        )

def load_users():
    ...
