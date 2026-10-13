import pytest

from datetime import date

from matching import find_compatible_users
from project import register_user
from project import User
from storage import load_users, save_users


def make_user(
    name="cliente",
    gender="M",
    orientation="H",
    birth_date=date(1990, 5, 15),
    email="cliente@example.com",
    city="Pasto",
):
    return User.create(
        name=name,
        gender=gender,
        orientation=orientation,
        birth_date=birth_date,
        email=email,
        city=city,
    )


# user.py


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
    assert user.name == "cliente"
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


def test_register_user_invalid_age():
    with pytest.raises(
        ValueError, match="Debes ser mayor de edad para registrarte."
    ):
        User.create(
            "cliente",
            "M",
            "H",
            date(2016, 10, 13),
            "cliente@example.com",
            "Pasto",
        )


def test_user_age_calculation():
    user = make_user()

    assert user.age == 36  # in 2026, after may 15


# storage.py


def test_save_and_load_user():
    file_path = "data/test_users.csv"

    user = make_user()

    save_users([user], file_path)
    users = load_users(file_path)

    assert len(users) == 1
    assert users[0].name == user.name
    assert users[0].gender == "M"
    assert users[0].orientation == "H"
    assert users[0].birth_date == user.birth_date
    assert users[0].city == "Pasto"
    assert users[0].email == user.email
    assert users[0].location == user.location
    assert users[0].balance == user.balance
    assert users[0].is_active
    assert not users[0].is_blocked
    assert users[0].same_orientation
    assert users[0].same_location


# matching.py


def test_exclude_own_profile():
    current_user = make_user()
    users = [current_user]

    matches = find_compatible_users(current_user, users)

    assert current_user not in matches


def test_excludes_inactive_and_blocked_users():
    current_user = make_user()

    inactive_user = make_user(
        name="otro_cliente",
        email="otro_cliente@example.com",
        gender="F",
        orientation="H",
    )
    inactive_user.is_active = False
    inactive_user.location = (1.19, -77.25)

    blocked_user = make_user(
        name="otro_cliente_mas",
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


def test_filters_by_preferences():
    current_user = make_user()
    current_user.same_location = True
    current_user.same_orientation = True

    compatible_user = make_user(
        name="otro_cliente",
        email="otro_cliente@example.com",
        gender="F",
        orientation="H",
    )
    compatible_user.location = (1.19, -77.25)

    different_city = make_user(
        name="otro_cliente_mas",
        email="otro_cliente_mas@example.com",
        city="Bogotá D.C.",
        gender="F",
        orientation="H",
    )

    different_orientation = make_user(
        name="y_un_cliente_mas",
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


def test_returns_empty_list_when_no_matches():
    current_user = make_user()
    current_user.same_location = True
    current_user.same_orientation = True

    other_user = make_user(  # different city
        name="otro_cliente",
        email="otro_cliente@example.com",
        city="Bogotá D.C.",
        gender="F",
        orientation="H",
    )

    another_user = make_user(  # different gender and sexual orientation
        name="otro_cliente_mas",
        email="otro_cliente_mas@example.com",
        gender="M",
        orientation="O",
    )
    another_user.location = (1.24, -77.29)

    users = [other_user, another_user]

    matches = find_compatible_users(current_user, users)

    assert not matches
