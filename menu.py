from pyfiglet import Figlet

figlet = Figlet()
figlet.setFont(font="graffiti")

CITIES = [
    "Pasto",
    "Ipiales",
    "Túquerres",
    "Tumaco",
    "Cali",
    "Tulcán",
    "Quito",
    "Bogotá",
]


def show_header():
    main_title = figlet.renderText("Lovefinderrz")
    print(main_title)


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

    city = select_city()

    if confirmation == "S":
        return name, gender, orientation, birth_date, email, city

    return None
