#coding: utf-8
from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Test API"
    author: str = "WSM"
    development_time: str = "2022-08-23"
    debug: bool = True
    mysql_host: str = None
    mysql_port: int = None
    mysql_user: str = None
    mysql_passwd: str = None
    mysql_table: str = None
    redis_host: str = None
    redis_port: int = None
    redis_passwd: str = None
    redis_db: int = None
    redis_user: str = None

    class Config:
        env_file = ".env"

