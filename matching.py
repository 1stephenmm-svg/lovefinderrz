def find_compatible_users(current_user, users):
    compatible_users = []

    for user in users:
        if user == current_user:
            continue

        if not user.is_active or user.is_blocked:
            continue

        if (
            current_user.same_orientation
            and user.orientation != current_user.orientation
        ):
            continue

        if (
            current_user.same_location
            and user.city != current_user.city
        ):
            continue

        compatible_users.append(user)

    return compatible_users