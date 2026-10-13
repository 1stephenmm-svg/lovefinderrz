import pytest

from datetime import date

from project import register_user
from project import User


def test_register_user():
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
    user = User.create(
        "cliente",
        "M",
        "H",
        date(1990, 5, 15),
        "cliente@example.com",
        "Pasto",
    )

    assert user.age == 36 # in 2026, after may 15
