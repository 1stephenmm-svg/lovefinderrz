import hashlib
import secrets

from user import Admin, Client


def verify_password(password, salt_hex, hash_hex):
    """Verify an administrator's password."""
    if not salt_hex or not hash_hex:
        return False

    salt = bytes.fromhex(salt_hex)
    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        600_000,
    )

    return secrets.compare_digest(password_hash.hex(), hash_hex)


def authenticate_user(users, nickname, password, user_class=None):
    """Authenticate an administrator or client."""
    for user in users:
        if user.nickname != nickname:
            continue

        if user_class is not None and not isinstance(user, user_class):
            continue

        if not user.is_active:
            return None

        if isinstance(user, Client):
            return user if password == user.nickname else None

        if isinstance(user, Admin):
            if verify_password(
                password,
                user.password_salt,
                user.password_hash,
            ):
                return user

        return None

    return None


def hash_password(password):
    """
    Generate a salted password hash using PBKDF2-HMAC-SHA256.

    Args:
        password (str): The plaintext password to hash.

    Returns:
        tuple[str, str]: A tuple containing the salt and password hash,
        both encoded as hexadecimal strings.

    A salt is a randomly generated sequence of bytes added to the
    password before hashing. It ensures that identical passwords
    produce different hashes when different salts are used.

    The value 600_000 specifies the number of iterations (600000) performed
    by PBKDF2. Repeated iterations increase the computational cost
    of deriving the hash, making brute-force password attacks more
    expensive. The underscore is a numeric separator in Python
    and has no effect on the value.
    """
    salt = secrets.token_bytes(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        600_000,
    )

    return salt.hex(), password_hash.hex()
