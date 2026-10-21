import pytest

from datetime import date, datetime

from matching import find_compatible_clients
from menu import hash_password
from project import validate_arguments
from storage import get_next_user_id, load_users, save_users
from user import Admin, Client
from user_service import register_user


@pytest.fixture
def test_admins_file(tmp_path):
    return tmp_path / "test_admins.csv"


@pytest.fixture
def test_file(tmp_path):
    return tmp_path / "test_clients.csv"


# project.py


def test_validate_arguments_valid_registration():
    assert validate_arguments(["-r", "admin"]) == ("-r", "admin")


def test_validate_arguments_invalid_command():
    with pytest.raises(ValueError, match="Invalid command-line argument"):
        validate_arguments(["-x", "admin"])


def test_validate_arguments_missing_username():
    with pytest.raises(ValueError, match="Missing username"):
        validate_arguments(["-r"])


# user.py


def make_admin(
    test_admins_file,
    nickname="admin",
    email="admin@lovefinderrz.com",
):
    password_salt, password_hash = hash_password("admin123")

    return Admin.create(
        id=get_next_user_id(test_admins_file),
        nickname=nickname,
        email=email,
        password_hash=password_hash,
        password_salt=password_salt,
    )


def make_client(
    test_file,
    nickname="cliente",
    gender="M",
    orientation="H",
    birth_date=date(1990, 5, 15),
    email="cliente@example.com",
    city="Pasto",
):
    return Client.create(
        id=get_next_user_id(test_file),
        nickname=nickname,
        gender=gender,
        orientation=orientation,
        birth_date=birth_date,
        email=email,
        city=city,
    )


def test_admin_created_at_is_assigned_automatically(test_admins_file):
    clear_file(test_admins_file)

    admin = make_admin(test_admins_file)

    assert isinstance(admin.created_at, datetime)


def test_same_admin_password_generates_different_salts():
    salt1, hash1 = hash_password("admin123")
    salt2, hash2 = hash_password("admin123")

    assert salt1 != salt2
    assert hash1 != hash2


def test_client_created_at_is_assigned_automatically(test_file):
    clear_file(test_file)

    client = make_client(test_file)

    assert isinstance(client.created_at, datetime)


def test_autoincrement_with_three_clients(test_file):
    clear_file(test_file)

    clients = []

    for nickname in ["cliente", "otro_cliente", "otro_cliente_mas"]:
        client = make_client(test_file, nickname=nickname)
        client.id = get_next_user_id(file_path=test_file)
        clients.append(client)

        save_users(clients, test_file)

    loaded_clients = load_users(test_file)

    assert [client.id for client in loaded_clients] == [1, 2, 3]


def test_register_admin_valid():
    password_salt, password_hash = hash_password("admin123")

    admins = []

    admin = register_user(
        admins,
        Admin,
        "admin",
        "admin@lovefinderrz.com",
        password_salt,
        password_hash,
    )

    assert len(admins) == 1
    assert admins[0] is admin
    assert admin.nickname == "admin"
    assert admin.email == "admin@lovefinderrz.com"
    assert admin.password_hash
    assert admin.password_salt
    assert admin.balance == 0
    assert admin.is_active


def test_register_client_valid():
    clients = []

    client = register_user(
        clients,
        Client,
        "cliente",
        "M",
        "H",
        date(1990, 5, 15),
        "cliente@example.com",
        "Pasto",
    )

    assert len(clients) == 1
    assert clients[0] is client
    assert client.nickname == "cliente"
    assert client.gender == "M"
    assert client.orientation == "H"
    assert client.birth_date == date(1990, 5, 15)
    assert client.email == "cliente@example.com"
    assert client.city == "Pasto"
    assert client.balance == 0
    assert client.is_active
    assert not client.is_blocked
    assert client.same_orientation
    assert client.same_location


def test_register_client_invalid_age(test_file):
    clear_file(test_file)

    with pytest.raises(
        ValueError, match="Debes ser mayor de edad para registrarte."
    ):
        Client.create(
            id=get_next_user_id(file_path=test_file),
            nickname="cliente",
            gender="M",
            orientation="H",
            birth_date=date(2016, 10, 13),
            email="cliente@example.com",
            city="Pasto",
        )


def test_client_age_calculation(test_file):
    clear_file(test_file)

    client = make_client(test_file)

    assert client.age == 36  # in 2026, after may 15


# storage.py


def clear_file(test_file, users=None):
    if users is None:
        users = []

    save_users(users, test_file)


def test_save_and_load_client(test_file):
    clear_file(test_file)

    client = make_client(test_file)
    save_users([client], test_file)

    clients = load_users(test_file)

    assert len(clients) == 1

    loaded_client = clients[0]

    assert loaded_client.nickname == client.nickname
    assert loaded_client.gender == "M"
    assert loaded_client.orientation == "H"
    assert loaded_client.birth_date == client.birth_date
    assert loaded_client.city == "Pasto"
    assert loaded_client.email == client.email
    assert loaded_client.location == client.location
    assert loaded_client.balance == client.balance
    assert loaded_client.is_active
    assert not loaded_client.is_blocked
    assert loaded_client.same_orientation
    assert loaded_client.same_location


# matching.py


def test_exclude_own_profile(test_file):
    clear_file(test_file)

    current_client = make_client(test_file)
    clients = [current_client]

    matches = find_compatible_clients(current_client, clients)

    assert current_client not in matches


def test_excludes_inactive_and_blocked_clients(test_file):
    clear_file(test_file)

    current_client = make_client(test_file)

    inactive_client = make_client(
        test_file,
        nickname="otro_cliente",
        email="otro_cliente@example.com",
        gender="F",
        orientation="H",
    )
    inactive_client.is_active = False
    inactive_client.location = (1.19, -77.25)

    blocked_client = make_client(
        test_file,
        nickname="otro_cliente_mas",
        email="otro_cliente_mas@example.com",
        gender="F",
        orientation="H",
    )
    blocked_client.is_blocked = True
    blocked_client.location = (1.24, -77.29)

    clients = [inactive_client, blocked_client]

    matches = find_compatible_clients(current_client, clients)
    assert inactive_client not in matches
    assert blocked_client not in matches


def test_filters_by_preferences(test_file):
    clear_file(test_file)

    current_client = make_client(test_file)
    current_client.same_location = True
    current_client.same_orientation = True

    compatible_client = make_client(
        test_file,
        nickname="otro_cliente",
        email="otro_cliente@example.com",
        gender="F",
        orientation="H",
    )
    compatible_client.location = (1.19, -77.25)

    different_city = make_client(
        test_file,
        nickname="otro_cliente_mas",
        email="otro_cliente_mas@example.com",
        city="Bogotá D.C.",
        gender="F",
        orientation="H",
    )

    different_orientation = make_client(
        test_file,
        nickname="y_un_cliente_mas",
        email="y_un_cliente_mas@example.com",
        gender="M",
        orientation="O",
    )
    different_city.location = (1.24, -77.29)

    clients = [
        current_client,
        compatible_client,
        different_city,
        different_orientation,
    ]

    result = find_compatible_clients(current_client, clients)

    assert result == [compatible_client]


def test_returns_empty_list_when_no_matches(test_file):
    clear_file(test_file)

    current_client = make_client(test_file)
    current_client.same_location = True
    current_client.same_orientation = True

    other_client = make_client(  # different city
        test_file,
        nickname="otro_cliente",
        email="otro_cliente@example.com",
        city="Bogotá D.C.",
        gender="F",
        orientation="H",
    )

    another_client = make_client(  # different gender and sexual orientation
        test_file,
        nickname="otro_cliente_mas",
        email="otro_cliente_mas@example.com",
        gender="M",
        orientation="O",
    )
    another_client.location = (1.24, -77.29)

    clients = [other_client, another_client]

    matches = find_compatible_clients(current_client, clients)

    assert not matches
