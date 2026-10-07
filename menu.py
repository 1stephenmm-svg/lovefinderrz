from datetime import datetime

from pyfiglet import Figlet
from tabulate import tabulate
from validator_collection import checkers

figlet = Figlet()
figlet.setFont(font="graffiti")

CITIES = [
    "Pasto, Nariño, Colombia",
    "Ipiales, Nariño, Colombia",
    "Túquerres, Nariño, Colombia",
    "Tumaco, Nariño, Colombia",
    "Cali, Valle del Cauca, Colombia",
    "Tulcán, Carchi, Ecuador",
    "Quito, Pichincha, Ecuador",
    "Bogotá D.C., Bogotá, Colombia",
]


def show_header():
    main_title = figlet.renderText("Lovefinderrz")
    print(main_title)


def input_name():
    while True:
        name = input("Nombre: ").strip().capitalize()

        if name.isalpha():
            return name

        elif not name:
            print("Tu nombre no puede estar vacio.")

        elif not name.isalpha():
            print("Tu nombre sólo puede contener letras.")


def select_gender():
    while True:
        gender = input("Género (F/M): ").strip().upper()

        if gender in ("F", "M"):
            return gender

        print("Opción inválida. Ingresa F o M.")


def select_sexual_orientation():
    while True:
        orientation = (
            input("Orientación sexual Hetero(H) u Otros(O): ").strip().upper()
        )

        if orientation in ("H", "O"):
            return orientation

        print("Opción inválida. Ingresa H u O.")


def input_birth_date():
    while True:
        today = datetime.now().date()

        birth_date = input("Fecha de nacimiento (DD/MM/YYYY): ").strip()

        try:
            birth_date = datetime.strptime(birth_date, "%d/%m/%Y").date()
        except ValueError:
            print("Fecha inválida.")
            continue

        if birth_date > today:
            print("¿Vienes del futuro?")
            continue

        age = today.year - birth_date.year

        if (today.month, today.day) < (birth_date.month, birth_date.day):
            age -= 1

        if age < 18:
            print("Debes ser mayor de edad para poder registrarte.")
            continue

        return birth_date


def input_email():
    while True:
        email = input("Email: ").strip()

        if checkers.is_email(email):
            return email

        print("Email inválido.")


def select_city():
    for number, city in enumerate(CITIES, start=1):
        print(f"{number}. {city}")

    while True:
        try:
            option = int(input("Selecciona tu ciudad: "))
        except ValueError:
            print("Selecciona una opción válida.")
            continue

        if 1 <= option <= len(CITIES):
            return CITIES[option - 1]

        print("Selecciona una opción válida.")


def show_main_menu():
    show_header()

    print("1. Regístrate")
    print("2. Tus preferencias")
    print("3. Mira perfiles")
    print("4. Da likes")
    print("5. Mira tus matches")
    print("6. Salir")


def show_register_menu():
    show_header()

    name = input_name()
    gender = select_gender()
    orientation = select_sexual_orientation()
    birth_date = input_birth_date()
    email = input_email()
    city = select_city()

    confirmation = input("¿Registrar usuario? (S/N): ").strip().upper()

    if confirmation == "S":
        return name, gender, orientation, birth_date, email, city

    return None


def show_profiles(users, current_user):
    profiles = []

    show_header()

    for user in users:
        if user != current_user and user.is_active and not user.is_blocked:
            profiles.append(
                [
                    user.name,
                    f"{user.age} años",
                    "Masculino" if user.gender == "M" else "Femenino",
                    "Heterosexual" if user.orientation == "H" else "Otro",
                    user.city,
                ]
            )

    print(
        tabulate(
            profiles,
            headers=[
                "Nombre",
                "Edad",
                "Género",
                "Orientación",
                "Ubicación",
            ],
            tablefmt="grid",
        )
    )

    input("\nPresiona Enter para volver al menú anterior...")


def show_preferences_menu():
    show_header()

    # todo: add more preferences
