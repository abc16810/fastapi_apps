from functools import lru_cache
from config import Settings
import bcrypt


@lru_cache()
def get_settings():
    return Settings()


def check_password(password: str, password_hash: str):
    return bcrypt.checkpw(password.encode(), password_hash.encode())


def hash_password(password: str):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
