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
                data = show_register_menu()
                if data:
                    current_user = User.create(*data)
                    users.append(current_user)
                    save_user(current_user)
            case "2":
                compatible_users = find_compatible_users(
                    current_user,
                    users,
                )
                show_profiles(compatible_users, current_user)
            case "3":
                data = show_preferences_menu()
                current_user.update_preferences(*data)
                save_users(users)
            case "4":
                show_matches()
            case "5":
                give_like()
            case "6":
                break
            case _:
                pass


def give_like(): ...


def show_matches(): ...


if __name__ == "__main__":
    main()
