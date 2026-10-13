import pytest

from datetime import date

from location import get_random_location
from matching import find_compatible_users
from project import register_user
from project import User
from storage import load_users, save_users


def make_user():
    return User.create(
        name="cliente",
        gender="M",
        orientation="H",
        birth_date=date(1990, 5, 15),
        email="cliente@example.com",
        city="Pasto",
    )


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


def test_exclude_own_profile():
    current_user = make_user()
    users = [current_user]

    matches = find_compatible_users(current_user, users)

    assert current_user not in matches


def test_save_and_load_user():
    file_path = "data/test_users.csv"

    user = make_user()
    user.location = get_random_location(user.city)

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
