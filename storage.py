import csv

from datetime import date, datetime

from user import User

FILE = "data/users.csv"
FIELDS = [
    "id",
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
    "same_orientation",
    "same_location",
    "created_at",
]


def save_user(user):
    latitude, longitude = user.location
    with open(FILE, "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)

        if file.tell() == 0:
            writer.writeheader()

        writer.writerow(
            {
                "id": user.id,
                "name": user.name,
                "gender": user.gender,
                "orientation": user.orientation,
                "birth_date": user.birth_date.isoformat(),
                "city": user.city,
                "email": user.email,
                "latitude": latitude,
                "longitude": longitude,
                "balance": user.balance,
                "is_active": user.is_active,
                "is_blocked": user.is_blocked,
                "same_orientation": user.same_orientation,
                "same_location": user.same_location,
                "created_at": user.created_at.isoformat(),
            }
        )

    input(
        f"\n¡TE DOY LA BIENVENIDA {user} A LOVEFINDERRZ!\n"
        + "Ahora puedes:\n"
        + "- mirar perfiles.\n"
        + "- cambiar tus preferencias.\n"
        + "- mirar tus matches."
        + "\nPresiona Enter para volver al menú principal..."
    )


def load_users(file_path=FILE):
    users = []

    with open(file_path, "r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            birth_date = date.fromisoformat(row["birth_date"])
            created_at = datetime.fromisoformat(row["created_at"])

            location = (
                float(row["latitude"]),
                float(row["longitude"]),
            )

            user = User(
                id=int(row["id"]),
                name=row["name"],
                gender=row["gender"],
                orientation=row["orientation"],
                birth_date=birth_date,
                email=row["email"],
                city=row["city"],
                location=location,
                balance=int(row["balance"]),
                created_at=created_at,
            )

            user.is_active = row["is_active"] == "True"
            user.is_blocked = row["is_blocked"] == "True"
            user.same_orientation = row["same_orientation"] == "True"
            user.same_location = row["same_location"] == "True"

            users.append(user)

    return users


def get_next_user_id(users=None, file_path=FILE):
    users = load_users(file_path)
    
    if not users:
        return 1

    return max(user.id for user in users) + 1


def save_users(users, file_path=FILE):
    with open(file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()

        for user in users:
            latitude, longitude = user.location

            writer.writerow(
                {
                    "id": user.id,
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
                    "same_orientation": user.same_orientation,
                    "same_location": user.same_location,
                    "created_at": user.created_at,
                }
            )
