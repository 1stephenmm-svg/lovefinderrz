import csv

from datetime import date

from user import User

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
    "is_blocked",
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
                "is_blocked": user.is_blocked,
            }
        )


def load_users():
    users = []
    
    with open(FILE, "r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            birth_date = date.fromisoformat(row["birth_date"])

            location = (
                float(row["latitude"]),
                float(row["longitude"]),
            )

            user = User(
                name=row["name"],
                gender=row["gender"],
                orientation=row["orientation"],
                birth_date=birth_date,
                email=row["email"],
                city=row["city"],
                location=location,
                balance=int(row["balance"]),
            )

            user.is_active = row["is_active"] == "True"
            user.is_blocked = row["is_blocked"] == "True"

            users.append(user)

    return users