from datetime import datetime

from pyfiglet import Figlet
from tabulate import tabulate

from data import CITIES
from user import Admin, Client

figlet = Figlet()
figlet.setFont(font="graffiti")


def show_header():
    main_title = figlet.renderText("Lovefinderrz")
    print(main_title)


def input_nickname(users, user_class=Client, username=None):
    candidate_from_args = username is not None

    while True:

        if candidate_from_args:
            candidate = username.strip().lower()
        else:
            candidate = input("¿Tu Nickname?: ").strip().lower()

        try:
            user_class.validate_nickname(candidate)
        except ValueError as error:
            print(error)
            candidate_from_args = False
            continue

        if any(user.nickname.lower() == candidate for user in users):
            print("Alguien predijo tu elección. Escoge otro")
            candidate_from_args = False
            continue

        nickname = candidate

        return nickname


def select_gender():
    while True:
        gender = input("Género (F/M): ").strip().upper()

        try:
            Client.validate_gender(gender)
        except ValueError as error:
            print(error)
            continue

        return gender


def select_sexual_orientation():
    while True:

        orientation = (
            input("Orientación sexual Hetero(H) u Otros(O): ").strip().upper()
        )

        try:
            Client.validate_sexual_orientation(orientation)
        except ValueError as error:
            print(error)
            continue

        return orientation


def input_birth_date():
    while True:
        birth_date = input("Fecha de nacimiento (DD/MM/YYYY): ").strip()

        try:
            birth_date = datetime.strptime(birth_date, "%d/%m/%Y").date()
        except ValueError:
            print("Fecha inválida.")
            continue

        try:
            Client.validate_birth_date(birth_date)
        except ValueError as error:
            print(error)
            continue

        return birth_date


def input_email():
    while True:
        email = input("Email: ").strip()

        try:
            Client.validate_email(email)
        except ValueError as error:
            print(error)
            continue

        return email


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


def show_register_menu(users, user_class=Client, username=None):
    show_header()

    nickname = input_nickname(users, user_class=user_class, username=username)
    email = f"{username}@lovefinderrz.com" if username else input_email()

    if user_class is Admin:
        confirmation = (
            input("¿Registrar administrador? (S/N): ").strip().upper()
        )

        if confirmation == "S":
            return nickname, email

        return None

    gender = select_gender()
    orientation = select_sexual_orientation()
    birth_date = input_birth_date()
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
