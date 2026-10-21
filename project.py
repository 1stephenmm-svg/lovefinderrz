import sys

from menu import register_user_from_menu, show_admin_menu, show_client_menu
from storage import load_users
from user import Admin


def main():
    users = load_users()
    current_user = None

    if len(sys.argv) > 3:
        sys.exit("Too many command-line arguments")

    if len(sys.argv) == 1:
        show_client_menu(None, users)
        return

    if len(sys.argv) > 1:
        if sys.argv[1] not in ["-r", "-l"]:
            sys.exit("Invalid command-line argument")

        if len(sys.argv) != 3:
            sys.exit("Missing username")

        if sys.argv[1] == "-r":
            current_user = register_user_from_menu(
                users, user_class=Admin, username=sys.argv[2]
            )

        elif sys.argv[1] == "-l":
            # TODO
            pass

    if isinstance(current_user, Admin):
        show_admin_menu(current_user, users)


if __name__ == "__main__":
    main()
