def main():

    while True:
        print("Lovefinderrz\n")
        print("1. Regístrate")
        print("2. Mira perfiles")
        print("3. Da likes")
        print("4. Mira tus matches")
        print("5. Configuración")
        print("6. Salir")

        option = input("Selecciona una opción: ").strip()
        match option:
            case "1":
                show_register_user()
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


def show_register_user(): ...


def show_profiles(): ...


def give_like(): ...


def show_matches(): ...


def show_settings(): ...


if __name__ == "__main__":
    main()
