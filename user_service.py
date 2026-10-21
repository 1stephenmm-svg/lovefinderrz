from storage import get_next_user_id
from user import Admin, Client

def register_user(users, user_class, *data):
    user_id = get_next_user_id(user_class)

    if user_class is Admin:
        nickname, email, salt, password_hash = data

        user = Admin.create(
            user_id,
            nickname=nickname,
            email=email,
            password_hash=password_hash,
            password_salt=salt,
        )

    else:
        nickname, gender, orientation, birth_date, email, city = data

        user = Client.create(
            user_id,
            nickname,
            gender,
            orientation,
            birth_date,
            email,
            city,
        )

    users.append(user)

    return user