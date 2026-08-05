from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError,  InvalidHashError

ph = PasswordHasher(time_cost=2, memory_cost=65536, parallelism=4)

def hash_password(password):
    password_hash = ph.hash(password)
    return password_hash

def verify_password(password, password_hash):
    try:
        ph.verify(password_hash, password)
        return True

    except (VerifyMismatchError, InvalidHashError):
        return False

