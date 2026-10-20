import sys

from matching import find_compatible_clients
from menu import (
    show_main_menu,
    show_profiles,
    show_preferences_menu,
    show_register_menu,
)
from storage import get_next_user_id, load_users, save_user, save_users
from user import Admin, Client


def main():
    users = load_users()
    current_user = None

    if len(sys.argv) > 3:
        sys.exit("Too many command-line arguments")

    if len(sys.argv) > 1:
        if sys.argv[1] not in ["-r", "-l"]:
            sys.exit("Invalid command-line argument")

        if len(sys.argv) != 3:
            sys.exit("Missing nickname")

        if sys.argv[1] == "-r":
            current_user = register_user_from_menu(
                users, user_class=Admin, nickname=sys.argv[2]
            )

        elif sys.argv[1] == "-l":
            # TODO
            pass

    while True:
        show_main_menu()

        option = input("Selecciona una opción: ").strip()
        match option:
            case "1":
                current_user = register_user_from_menu(users) or current_user
            case "2":
                compatible_clients = find_compatible_clients(
                    current_user,
                    users,
                )
                show_profiles(compatible_clients, current_user)
            case "3":
                if current_user := require_current_user(users, current_user):
                    data = show_preferences_menu()
                    current_user.update_preferences(*data)
                    save_users(users)
            case "4":
                if current_user := require_current_user(users, current_user):
                    show_matches()
            case "5":
                break
            case _:
                pass


def show_matches(): ...


def register_user_from_menu(users, user_class=Client, nickname=None):
    data = show_register_menu(users, user_class=user_class, nickname=nickname)

    if not data:
        return None

    user = register_user(users, user_class, *data)
    save_user(user)

    return user


def register_user(users, user_class, *data):
    user_id = get_next_user_id(user_class)

    if user_class is Admin:
        nickname, email = data

        user = Admin.create(
            user_id,
            nickname=nickname,
            email=email,
        )

    else:
        nickname, gender, orientation, birth_date, email, city = data
        
        user = Client.create(
            user_id,
            nickname,
            gender,
            orientation,
            birth_date,
            email,
            city,
        )

    users.append(user)

    return user


def require_current_user(users, current_user):
    if current_user:
        return current_user

    answer = (
        input(
            "Necesitas registrarte para acceder a esta opción. "
            "¿Quieres hacerlo ahora? (S/N): "
        )
        .strip()
        .upper()
    )

    if answer != "S":
        return None

    return register_user(users)


if __name__ == "__main__":
    main()
