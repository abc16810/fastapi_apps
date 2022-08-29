from conf.app import AppSettings
from functools import lru_cache


@lru_cache
def get_app_settings() -> AppSettings:
    return AppSettings()
