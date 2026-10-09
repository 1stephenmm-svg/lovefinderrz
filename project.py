from matching import find_compatible_users
from menu import (
    show_main_menu,
    show_register_menu,
    show_profiles,
    show_preferences_menu,
)
from storage import save_user, load_users, save_users
from user import User


def main():
    users = load_users()
    current_user = None

    while True:
        show_main_menu()

        option = input("Selecciona una opción: ").strip()
        match option:
            case "1":
                current_user = register_user(users) or current_user
            case "2":
                compatible_users = find_compatible_users(
                    current_user,
                    users,
                )
                show_profiles(compatible_users, current_user)
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

def register_user(users):
    data = show_register_menu()

    if not data:
        return None

    user = User.create(*data)
    users.append(user)
    save_user(user)

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
