import sys

from menu import register_user_from_menu, show_admin_menu, show_client_menu
from storage import load_users
from user import Admin


def main():
    users = load_users()
    current_user = None

    try:
        command, username = validate_arguments(sys.argv[1:])

        if command == "-r":
            current_user = register_user_from_menu(
                users, user_class=Admin, username=username
            )
        elif command == "-l":
            # TODO
            pass
        else:
            show_client_menu(None, users)
    except ValueError as error:
        sys.exit(str(error))

    if isinstance(current_user, Admin):
        show_admin_menu(current_user, users)


def validate_arguments(args):
    """Validate command-line arguments."""
    if len(args) > 2:
        raise ValueError("Too many command-line arguments")

    if not args:
        return None, None

    if args[0] not in ["-r", "-l"]:
        raise ValueError("Invalid command-line argument")

    if len(args) != 2:
        raise ValueError("Missing username")

    return args[0], args[1]


if __name__ == "__main__":
    main()
