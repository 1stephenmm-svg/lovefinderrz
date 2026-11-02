import hashlib
import secrets


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
