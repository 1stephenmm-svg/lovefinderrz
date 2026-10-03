from pyfiglet import Figlet

figlet = Figlet()
figlet.setFont(font="graffiti")


def show_header():
    main_title = figlet.renderText("Lovefinderrz")
    print(main_title)


def show_main_menu():
    show_header()

    print("1. Regístrate")
    print("2. Mira perfiles")
    print("3. Da likes")
    print("4. Mira tus matches")
    print("5. Configuración")
    print("6. Salir")


def show_register_menu():
    show_header()

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
