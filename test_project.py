import pytest

from datetime import date, datetime

from matching import find_compatible_users
from project import register_user
from project import User
from storage import load_users, save_users, get_next_user_id


@pytest.fixture
def test_file(tmp_path):
    return tmp_path / "test_users.csv"


def make_user(
    test_file,
    nickname="cliente",
    gender="M",
    orientation="H",
    birth_date=date(1990, 5, 15),
    email="cliente@example.com",
    city="Pasto",
):
    return User.create(
        id=get_next_user_id(test_file),
        nickname=nickname,
        gender=gender,
        orientation=orientation,
        birth_date=birth_date,
        email=email,
        city=city,
    )


def clear_file(test_file, users=None):
    if users is None:
        users = []

    save_users(users, test_file)


# user.py


def test_created_at_is_assigned_automatically(test_file):
    clear_file(test_file)

    user = make_user(test_file)

    assert isinstance(user.created_at, datetime)


def test_autoincrement_with_three_users(test_file):
    clear_file(test_file)

    users = []

    for nickname in ["cliente", "otro_cliente", "otro_cliente_mas"]:
        user = make_user(test_file, nickname=nickname)
        user.id = get_next_user_id(file_path=test_file)
        users.append(user)

        save_users(users, test_file)

    loaded_users = load_users(test_file)

    assert [user.id for user in loaded_users] == [1, 2, 3]


def test_register_user_valid():
    users = []

    user = register_user(
        users,
        "cliente",
        "M",
        "H",
        date(1990, 5, 15),
        "cliente@example.com",
        "Pasto",
    )

    assert len(users) == 1
    assert users[0] is user
    assert user.nickname == "cliente"
    assert user.gender == "M"
    assert user.orientation == "H"
    assert user.birth_date == date(1990, 5, 15)
    assert user.email == "cliente@example.com"
    assert user.city == "Pasto"
    assert user.balance == 0
    assert user.is_active
    assert not user.is_blocked
    assert user.same_orientation
    assert user.same_location


def test_register_user_invalid_age(test_file):
    clear_file(test_file)

    with pytest.raises(
        ValueError, match="Debes ser mayor de edad para registrarte."
    ):
        User.create(
            id=get_next_user_id(file_path=test_file),
            nickname="cliente",
            gender="M",
            orientation="H",
            birth_date=date(2016, 10, 13),
            email="cliente@example.com",
            city="Pasto",
        )


def test_user_age_calculation(test_file):
    clear_file(test_file)

    user = make_user(test_file)

    assert user.age == 36  # in 2026, after may 15


# storage.py


def test_save_and_load_user(test_file):
    clear_file(test_file)

    user = make_user(test_file)
    save_users([user], test_file)

    users = load_users(test_file)

    assert len(users) == 1

    loaded_user = users[0]

    assert loaded_user.nickname == user.nickname
    assert loaded_user.gender == "M"
    assert loaded_user.orientation == "H"
    assert loaded_user.birth_date == user.birth_date
    assert loaded_user.city == "Pasto"
    assert loaded_user.email == user.email
    assert loaded_user.location == user.location
    assert loaded_user.balance == user.balance
    assert loaded_user.is_active
    assert not loaded_user.is_blocked
    assert loaded_user.same_orientation
    assert loaded_user.same_location


# matching.py


def test_exclude_own_profile(test_file):
    clear_file(test_file)

    current_user = make_user(test_file)
    users = [current_user]

    matches = find_compatible_users(current_user, users)

    assert current_user not in matches


def test_excludes_inactive_and_blocked_users(test_file):
    clear_file(test_file)

    current_user = make_user(test_file)

    inactive_user = make_user(
        test_file,
        nickname="otro_cliente",
        email="otro_cliente@example.com",
        gender="F",
        orientation="H",
    )
    inactive_user.is_active = False
    inactive_user.location = (1.19, -77.25)

    blocked_user = make_user(
        test_file,
        nickname="otro_cliente_mas",
        email="otro_cliente_mas@example.com",
        gender="F",
        orientation="H",
    )
    blocked_user.is_blocked = True
    blocked_user.location = (1.24, -77.29)

    users = [inactive_user, blocked_user]

    matches = find_compatible_users(current_user, users)
    assert inactive_user not in matches
    assert blocked_user not in matches


def test_filters_by_preferences(test_file):
    clear_file(test_file)

    current_user = make_user(test_file)
    current_user.same_location = True
    current_user.same_orientation = True

    compatible_user = make_user(
        test_file,
        nickname="otro_cliente",
        email="otro_cliente@example.com",
        gender="F",
        orientation="H",
    )
    compatible_user.location = (1.19, -77.25)

    different_city = make_user(
        test_file,
        nickname="otro_cliente_mas",
        email="otro_cliente_mas@example.com",
        city="Bogotá D.C.",
        gender="F",
        orientation="H",
    )

    different_orientation = make_user(
        test_file,
        nickname="y_un_cliente_mas",
        email="y_un_cliente_mas@example.com",
        gender="M",
        orientation="O",
    )
    different_city.location = (1.24, -77.29)

    users = [
        current_user,
        compatible_user,
        different_city,
        different_orientation,
    ]

    result = find_compatible_users(current_user, users)

    assert result == [compatible_user]


def test_returns_empty_list_when_no_matches(test_file):
    clear_file(test_file)

    current_user = make_user(test_file)
    current_user.same_location = True
    current_user.same_orientation = True

    other_user = make_user(  # different city
        test_file,
        nickname="otro_cliente",
        email="otro_cliente@example.com",
        city="Bogotá D.C.",
        gender="F",
        orientation="H",
    )

    another_user = make_user(  # different gender and sexual orientation
        test_file,
        nickname="otro_cliente_mas",
        email="otro_cliente_mas@example.com",
        gender="M",
        orientation="O",
    )
    another_user.location = (1.24, -77.29)

    users = [other_user, another_user]

    matches = find_compatible_users(current_user, users)

    assert not matches
