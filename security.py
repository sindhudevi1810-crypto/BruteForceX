from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

# Initialize Argon2 password hasher
password_hasher = PasswordHasher(
    time_cost=2,
    memory_cost=19456,
    parallelism=1
)


def hash_password(password):
    """Securely hash a password."""
    return password_hasher.hash(password)


def verify_password(stored_hash, entered_password):
    """Verify an entered password."""
    try:
        return password_hasher.verify(
            stored_hash,
            entered_password
        )
    except Exception:
        return False