from storage import get_next_user_id


def register_user(users, user_class, data):
    """Create a user, add it to the user list, and return it."""
    user_id = get_next_user_id(user_class)
    user = user_class.create(user_id, **data)

    users.append(user)

    return user
