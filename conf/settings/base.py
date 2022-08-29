#coding: utf-8
from pydantic import BaseSettings, RedisDsn
from typing import Dict, Any


class Settings(BaseSettings):
    author: str = "WSM"
    development_time: str = "2022-08-23"
    title: str = "FastAPI example application"
    version: str = "1.0.0"
    debug: bool = True

    redis_dsn: RedisDsn


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
        validate_assignment = True   # 是否对属性赋值进行验证

    @property
    def fastapi_kwargs(self) -> Dict[str, Any]:
        return {
            "author": self.author,
            "development_time": self.development_time,
            "debug": self.debug,
            "title": self.title,
            "version": self.version,
        }

# settings = Settings(_env_file='prod.env', _env_file_encoding='utf-8')   实例化优先于Config
# settings = Settings(_env_file=None) 不加载任何变量文件
