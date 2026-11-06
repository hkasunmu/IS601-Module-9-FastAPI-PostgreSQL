
from pwdlib import PasswordHash

# Set up secure password hashing
password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """Turn a plain-text password into a secure hash."""
    return password_hash.hash(password)


def verify_password(
    password: str, hashed_password: str
) -> bool:
    """Check whether a password matches the stored hash."""
    return password_hash.verify(password, hashed_password)
