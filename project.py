from pyfiglet import Figlet

from user import User

figlet = Figlet()
figlet.setFont(font="graffiti")

users = []


def main():

    while True:
        show_main_menu()

        option = input("Selecciona una opción: ").strip()
        match option:
            case "1":
                data = show_register_user()
                if data:
                    new_user = User(*data)
                    users.append(new_user)
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


def show_main_menu():
    main_title = figlet.renderText("Lovefinderrz")
    print(main_title)

    print("Lovefinderrz\n")
    print("1. Regístrate")
    print("2. Mira perfiles")
    print("3. Da likes")
    print("4. Mira tus matches")
    print("5. Configuración")
    print("6. Salir")


def show_register_user():
    main_title = figlet.renderText("Lovefinderrz")
    print(main_title)

    name = input("Nombre: ").strip().capitalize()
    gender = input("Género (F/M): ").strip().upper()
    orientation = (
        input("Orientación sexual Hetero(H) u Otros(O): ").strip().upper()
    )
    birth_date = input("Fecha de nacimiento (DD/MM/YYYY): ").strip()
    email = input("Email: ").strip()

    confirmation = input("¿Registrar usuario? (S/N): ").strip().upper()

    if confirmation == "S":
        return name, gender, orientation, birth_date, email

    return None


def show_profiles(): ...


def give_like(): ...


def show_matches(): ...


def show_settings(): ...


if __name__ == "__main__":
    main()
