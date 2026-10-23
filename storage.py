import csv

from datetime import date, datetime

from user import Admin, Client

ADMINS_FILE = "data/admins.csv"
CLIENTS_FILE = "data/clients.csv"

ADMIN_FIELDS = [
    "id",
    "nickname",
    "email",
    "password_hash",
    "password_salt",
    "created_at",
    "is_active",
]

CLIENT_FIELDS = [
    "id",
    "nickname",
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


def user_to_row(user):
    common_fields = {
        "id": user.id,
        "nickname": user.nickname,
        "email": user.email,
        "created_at": user.created_at.isoformat(),
        "is_active": user.is_active,
    }

    if isinstance(user, Admin):
        return {
            **common_fields,
            "password_hash": user.password_hash,
            "password_salt": user.password_salt,
        }

    if isinstance(user, Client):
        latitude, longitude = user.location

        return {
            **common_fields,
            "gender": user.gender,
            "orientation": user.orientation,
            "birth_date": user.birth_date.isoformat(),
            "city": user.city,
            "latitude": latitude,
            "longitude": longitude,
            "balance": user.balance,
            "is_blocked": user.is_blocked,
            "same_orientation": user.same_orientation,
            "same_location": user.same_location,
        }


def get_file_path(user_or_class):
    user_class = (
        user_or_class
        if isinstance(user_or_class, type)
        else type(user_or_class)
    )

    if issubclass(user_class, Admin):
        return ADMINS_FILE

    if issubclass(user_class, Client):
        return CLIENTS_FILE


def save_user(user):
    file_path = get_file_path(user)
    fields = ADMIN_FIELDS if isinstance(user, Admin) else CLIENT_FIELDS
    row = user_to_row(user)

    with open(file_path, "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)

        if file.tell() == 0:
            writer.writeheader()

        writer.writerow(row)

    if isinstance(user, Client):
        input(
            f"\n¡TE DOY LA BIENVENIDA {user} A LOVEFINDERRZ!\n"
            + "Ahora puedes:\n"
            + "- mirar perfiles.\n"
            + "- cambiar tus preferencias.\n"
            + "- mirar tus matches."
            + "\nPresiona Enter para volver al menú principal..."
        )
    else:
        input(f"\n¡BUEN DIA {user} !\n" + "\nPresiona Enter para volver...")


def load_users(file_path=None):
    files_to_load = (
        [(CLIENTS_FILE, Client), (ADMINS_FILE, Admin)]
        if file_path is None
        else [
            (
                file_path,
                Admin if file_path == ADMINS_FILE else Client,
            )
        ]
    )

    users = []

    for path, user_class in files_to_load:
        try:
            with open(path, "r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    created_at = datetime.fromisoformat(row["created_at"])

                    common = {
                        "id": int(row["id"]),
                        "nickname": row["nickname"],
                        "email": row["email"],
                        "created_at": created_at,
                    }

                    user = None

                    if user_class == Admin:
                        user = Admin(**common)

                    else:
                        birth_date = date.fromisoformat(row["birth_date"])
                        location = (
                            float(row["latitude"]),
                            float(row["longitude"]),
                        )

                        user = Client(
                            **common,
                            gender=row["gender"],
                            orientation=row["orientation"],
                            birth_date=birth_date,
                            city=row["city"],
                            location=location,
                            balance=int(row["balance"]),
                        )

                        user.same_orientation = (
                            row["same_orientation"] == "True"
                        )
                        user.same_location = row["same_location"] == "True"
                        user.is_blocked = row["is_blocked"] == "True"

                    user.is_active = row["is_active"] == "True"

                    users.append(user)
        except FileNotFoundError:
            continue

    return users


def get_next_user_id(user_class=Client, file_path=None):
    if file_path is None:
        file_path = get_file_path(user_class)

    users = load_users(file_path)

    if not users:
        return 1

    return max(user.id for user in users) + 1


def save_records(records, file_path, fields):
    """Save records to a CSV file."""
    with open(file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()

        for record in records:
            writer.writerow(user_to_row(record))


def save_users(users, user_class=None):
    """Save users to their corresponding CSV files."""
    if user_class is Client:
        records = [user for user in users if isinstance(user, Client)]
        save_records(records, CLIENTS_FILE, CLIENT_FIELDS)
        return

    if user_class is Admin:
        records = [user for user in users if isinstance(user, Admin)]
        save_records(records, ADMINS_FILE, ADMIN_FIELDS)
        return

    clients = [user for user in users if isinstance(user, Client)]
    admins = [user for user in users if isinstance(user, Admin)]

    save_records(clients, CLIENTS_FILE, CLIENT_FIELDS)
    save_records(admins, ADMINS_FILE, ADMIN_FIELDS)
