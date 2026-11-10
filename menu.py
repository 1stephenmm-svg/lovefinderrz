import sys

import emoji

from datetime import datetime
from getpass import getpass

from pyfiglet import Figlet
from tabulate import tabulate

from auth import authenticate_user, hash_password
from data import CITIES
from likes import register_like
from location import calculate_distance
from matching import find_compatible_clients
from storage import load_likes, save_user, save_users_to_csv
from user import Admin, Client
from user_service import register_user

figlet = Figlet()
figlet.setFont(font="graffiti")


# 1. Auxiliary display and security functions
def show_header():
    main_title = figlet.renderText("Lovefinderrz")
    print(main_title)


# 2. Input and data selection functions
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


def input_password():
    while True:
        password = getpass("Contraseña: ")
        confirmation = getpass("Confirma la contraseña: ")

        if password != confirmation:
            input("Las contrasenas no coinciden.")
            continue

        salt, password_hash = hash_password(password)

        return salt, password_hash


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


# 3. Forms and submenus


def show_register_menu(users, user_class=Client, username=None):
    """Collect the information required to register a user."""
    show_header()

    nickname = input_nickname(users, user_class=user_class, username=username)
    email = f"{nickname}@lovefinderrz.com" if username else input_email()
    password = nickname if not username else input_password()

    if user_class is Admin:
        salt, password_hash = password

        confirmation = (
            input("¿Registrar administrador? (S/N): ").strip().upper()
        )

        if confirmation == "S":
            return {
                "nickname": nickname,
                "email": email,
                "password_hash": password_hash,
                "password_salt": salt,
            }

        return None

    gender = select_gender()
    orientation = select_sexual_orientation()
    birth_date = input_birth_date()
    city = select_city()

    confirmation = input("¿Registrar usuario? (S/N): ").strip().upper()

    if confirmation == "S":
        return {
            "nickname": nickname,
            "gender": gender,
            "orientation": orientation,
            "birth_date": birth_date,
            "email": email,
            "city": city,
        }

    return None


def show_client_access_menu():
    """Display the client access submenu and return the selected option."""
    show_header()

    print("¿QUÉ QUIERES HACER?\n")
    print(emoji.emojize(":waving_hand: 1. Registrarme"))
    print(emoji.emojize(":locked_with_key: 2. Iniciar sesión"))
    print(emoji.emojize(":door: 3. Volver al menú principal"))

    return input("\nSelecciona una opción: ").strip()


def register_user_from_menu(users, user_class=Client, username=None):
    """Register a user or display the client access submenu."""

    if user_class is Client:

        option = show_client_access_menu()

        if option == "2":
            return show_login_menu(users, user_class=Client)

        if option == "3":
            return None

        if option != "1":
            return None

    """Register and save a user through the console menu."""
    data = show_register_menu(users, user_class=user_class, username=username)

    if not data:
        return None

    user = register_user(users, user_class, data)
    save_user(user)

    return user


def show_login_menu(users, user_class=None, username=None):
    """Request credentials and authenticate a user."""
    nickname = username or input("¿Cual es tu Nickname?: ").strip()

    user = None

    for candidate in users:
        if candidate.nickname == nickname:
            if not user_class or isinstance(candidate, user_class):
                user = candidate
                break
    if user is None:
        input(
            emoji.emojize(
                "No te encontré en mi memoria. :face_without_mouth:"
                + "\nPresiona Enter para volver..."
            )
        )
        return None

    if isinstance(user, Client) and user.is_blocked:
        sys.exit(
            emoji.emojize(
                "Tu cuenta está bloqueada. Seguro algo malo hiciste "
                + ":slightly_frowning_face:"
            )
        )

    password = getpass("Escribe tu Contraseña: ")

    user = authenticate_user(
        users,
        nickname,
        password,
        user_class=user_class,
    )

    if user is None:
        print("Contraseña incorrecta.")
        return None

    welcome_msg = (
        emoji.emojize(":sparkles: Bienvenido de vuelta")
        if user.is_active
        else emoji.emojize(
            ":smiling_face: Me alegra que estés de nuevo acá. Te extrañé resto"
        )
    )
    user.is_active = True
    user.last_login = datetime.now()

    save_users_to_csv(users, user_class)

    nickname = user.nickname if isinstance(user, Client) else user

    input(
        f"¡¡{welcome_msg}, {nickname}.!!."
        + "\nPresiona Enter para continuar..."
    )
    return user


def show_profiles(users, current_user):
    profiles = []
    ids = []

    likes = load_likes() if current_user else []

    liked_ids = {
        liked_client_id
        for client_id, liked_client_id in likes
        if current_user and client_id == current_user.id
    }

    show_header()

    for user in users:
        if user == current_user:
            continue
        if user.id in liked_ids:
            continue
        if user.is_blocked:
            continue
        if not user.is_active:
            continue

        distance = (
            calculate_distance(current_user.location, user.location)
            if current_user is not None
            else None
        )

        profiles.append(
            {
                "client": user,
                "distance": distance,
            }
        )
        ids.append(user.id)

    if not profiles:
        input(
            emoji.emojize(
                "No encontré perfiles compatibles contigo. "
                + ":face_without_mouth:"
                + "\nIntenta de nuevo más tarde o actualiza tus preferencias."
            )
        )
    else:
        if current_user is not None:
            profiles.sort(key=lambda profile: profile["distance"])
        else:
            profiles.sort(
                key=lambda profile: profile["client"].last_login,
                reverse=True,
            )

        rows = [
            [
                profile["client"].id,
                profile["client"].nickname,
                f"{profile['client'].age} años",
                (
                    emoji.emojize(":man:")
                    if profile["client"].gender == "M"
                    else emoji.emojize(":woman:")
                ),
                (
                    "Heterosexual"
                    if profile["client"].orientation == "H"
                    else emoji.emojize(":rainbow_flag:")
                ),
                profile["client"].city,
            ]
            + (
                [f"{profile['distance']:.2f} km"]
                if profile["distance"] is not None
                else []
            )
            for profile in profiles
        ]

        headers = [
            "ID",
            "Nickname",
            "Edad",
            "Género",
            "Orientación",
            "Ubicación",
        ]

        if current_user is not None:
            headers.append("Distancia")

        print(
            tabulate(
                rows,
                headers,
                tablefmt="grid",
            )
        )

        while True:
            if ids:
                selected_id = input(
                    "\nIngresa el número de ID de quien quieres conocer "
                    "\nó presiona Enter para salir: "
                ).strip()
            else:
                input(
                    emoji.emojize(
                        "\n¡Ya diste like a todos los perfiles disponibles! "
                        + ":grinning_face_with_smiling_eyes:"
                        + "\nIntenta de nuevo más tarde o actualiza tus "
                        + "preferencias."
                    )
                )
                break

            if not selected_id:
                break

            if not selected_id.isdigit():
                continue

            selected_id = int(selected_id)

            if selected_id not in ids:
                print(
                    "El ID del personaje que seleccionaste no existe ó ya le "
                    + "diste like."
                )
                continue

            if current_user is None:
                current_user = require_current_user(
                    users, current_user
                )  # check if client is logged in

                if current_user is None:
                    return None

                likes = load_likes()

            if register_like(current_user.id, selected_id, likes):
                input("¡Tu like ya quedó registrado!")
            else:
                print("Ya le habías dado like a este perfil.")

            ids.remove(selected_id)

            confirmation = (
                input("\n¿Quieres seleccionar otro?" + " (S/N)")
                .strip()
                .upper()
            )

            if confirmation == "S":
                continue

            return None

    return None


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


def show_likes():
    show_header()

    # TODO


def show_matches():
    show_header()

    # TODO


def require_current_user(users, current_user):
    """Request registration if no current user is available."""
    if current_user:
        return current_user

    answer = (
        input(
            emoji.emojize(
                ":hand_with_fingers_splayed:  Necesitas iniciar sesión o "
                + "registrarte para acceder a esta opción."
                + "\n¿Quieres hacerlo ahora? (S/N): "
            )
        )
        .strip()
        .upper()
    )

    if answer != "S":
        return None

    return register_user_from_menu(users)


# 4. Main Menus by Role
def display_client_menu(current_user):
    """Display the main menu options for clients."""
    show_header()

    print(emoji.emojize(":eyes: 1. Chismosea perfiles y reparte likes"))
    if current_user is None:
        print(emoji.emojize(":waving_hand: 2. Iniciar sesión/Regístrate"))
    print(emoji.emojize(":bullseye: 3. Tus preferencias"))
    print(emoji.emojize(":heart_exclamation:  4. Tus likes"))
    print(emoji.emojize(":couple_with_heart: 5. Mira tus matches"))
    print(emoji.emojize(":door: 6. Salir"))


def show_client_menu(current_user, users):
    """Handle client menu interactions."""
    while True:
        display_client_menu(current_user)

        option = input("\nSelecciona una opción: ").strip()
        match option:
            case "1":
                compatible_clients = find_compatible_clients(
                    current_user,
                    users,
                )
                show_profiles(compatible_clients, current_user)
            case "2":
                current_user = register_user_from_menu(users) or current_user
            case "3":
                if current_user := require_current_user(users, current_user):
                    data = show_preferences_menu()
                    current_user.update_preferences(*data)
                    save_users_to_csv(users, Client)
            case "4":
                if current_user := require_current_user(users, current_user):
                    show_likes()
            case "5":
                if current_user := require_current_user(users, current_user):
                    show_matches()
            case "6":
                current_user = None
                break
            case _:
                pass


def display_admin_menu():
    """Display the main menu options for administrators."""
    show_header()

    # TODO


def show_admin_menu(current_user, users):
    """Handle admin menu interactions."""
    display_admin_menu()

    # TODO
