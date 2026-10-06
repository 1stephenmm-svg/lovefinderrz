from menu import show_main_menu, show_register_menu
from storage import save_user
from user import User

users = []


def main():

    while True:
        show_main_menu()

        option = input("Selecciona una opción: ").strip()
        match option:
            case "1":
                data = show_register_menu()
                if data:
                    new_user = User.create(*data)
                    users.append(new_user)
                    save_user(new_user)
            case "2":
                show_profiles()
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


def show_profiles(): ...


def give_like(): ...


def show_matches(): ...


def show_settings(): ...


if __name__ == "__main__":
    main()
