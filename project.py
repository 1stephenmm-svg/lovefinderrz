from matching import find_compatible_clients
from menu import (
    show_main_menu,
    show_profiles,
    show_preferences_menu,
    show_register_menu,
)
from storage import get_next_user_id, load_users, save_user, save_users
from user import Client


def main():
    users = load_users()
    current_user = None

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


def register_user_from_menu(users):
    data = show_register_menu(users)

    if not data:
        return None

    user = register_client(users, *data)
    save_user(user)

    return user


def register_client(
    users, nickname, gender, orientation, birth_date, email, city
):
    user_id = get_next_user_id(users)

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

    return register_client(users)


if __name__ == "__main__":
    main()
