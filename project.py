from menu import show_main_menu, show_register_menu, show_profiles
from storage import save_user, load_users
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
                show_profiles(users, current_user)
            case "3":
                give_like()
            case "4":
                show_matches()
            case "5":
                show_settings()
            case "6":
                break
            case _:
                pass


def give_like(): ...


def show_matches(): ...


def show_settings(): ...


if __name__ == "__main__":
    main()
