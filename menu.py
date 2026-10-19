from datetime import datetime

from pyfiglet import Figlet
from tabulate import tabulate
from user import User
from validator_collection import checkers

from data import CITIES

figlet = Figlet()
figlet.setFont(font="graffiti")


def show_header():
    main_title = figlet.renderText("Lovefinderrz")
    print(main_title)


def input_nickname(users):
    while True:
        candidate = input("¿Tu Nickname?: ").strip().lower()

        try:
            User.validate_nickname(candidate)
        except ValueError as error:
            print(error)
            continue

        if any(user.nickname.lower() == candidate for user in users):
            print("Alguien predijo tu elección. Escoge otro")
            continue

        nickname = candidate

        return nickname


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
    print("2. Mira perfiles")
    print("3. Tus preferencias")
    print("4. Mira tus matches")
    print("5. Salir")


def show_register_menu(users):
    show_header()

    nickname = input_nickname(users)
    gender = select_gender()
    orientation = select_sexual_orientation()
    birth_date = input_birth_date()
    email = input_email()
    city = select_city()

    confirmation = input("¿Registrar usuario? (S/N): ").strip().upper()

    if confirmation == "S":
        return nickname, gender, orientation, birth_date, email, city

    return None


def show_profiles(users, current_user):
    profiles = []

    show_header()

    for user in users:
        if user == current_user:
            continue
        if user.is_blocked:
            continue
        if not user.is_active:
            continue

        profiles.append(
            [
                user.nickname,
                f"{user.age} años",
                "Masculino" if user.gender == "M" else "Femenino",
                "Heterosexual" if user.orientation == "H" else "Otro",
                user.city,
            ]
        )

    if not profiles:
        print(
            "No encontré perfiles compatibles contigo."
            "Intenta de nuevo más tarde o actualiza tus preferencias."
        )
    else:
        print(
            tabulate(
                profiles,
                headers=[
                    "Nickname",
                    "Edad",
                    "Género",
                    "Orientación",
                    "Ubicación",
                ],
                tablefmt="grid",
            )
        )

    input("\nPresiona Enter para volver al menú principal...")


def show_preferences_menu():
    show_header()

    orientation_preference = (
        input(
            "¿Quieres conocer gente sólo del sexo opuesto?\n"
            + "Sí(S)/Me da igual(Enter): "
        )
        .strip()
        .upper()
    )
    same_orientation = orientation_preference == "S"

    location_preference = (
        input("¿Gente solo en tu ciudad?\n" + "Sí(S)/Me da igual(Enter): ")
        .strip()
        .upper()
    )
    same_location = location_preference == "S"

    return same_orientation, same_location
