# coding: utf-8
from pydantic import BaseSettings, RedisDsn, AnyUrl, BaseModel, SecretStr
from typing import Dict, Any, List, Optional


class MysqlModel(BaseModel):
    mysql_host: str = 'localhost'
    mysql_port: int = 3306
    mysql_user: str = 'root'
    mysql_password: str = 'xxx'
    mysql_db: str = 'xx'


class AppSettings(BaseSettings):
    author: str = "WSM"
    development_time: str = "2022-08-23"
    title: str = "FastAPI example application"
    version: str = "1.0.0"
    debug: bool = True
    description: str = """练习测试。。。 🚀"""
    openapi_url: str = "/openapi.json"
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"

    secret_key: SecretStr   # openssl rand -hex 32

    redis_dsn: RedisDsn
    mysql_dict: MysqlModel = MysqlModel()

    allowed_hosts: List[str] = ["*"]
    api_prefix: str = "/api"

    api_manager_prefix: str = "/admin"

    jwt_token_prefix: str = "Token"

    class Config:
        validate_assignment = True  # 是否对属性赋值进行验证
        fields = {
            'redis_dsn': {
                'env': ['service_redis_dsn', 'redis_url']
            },
            'mysql_dict': {
                'env': ['service_mysql_dict', 'mysql_params']
            }
        }
        env_file = ".env"  # python-dotenv
        env_file_encoding = 'utf-8'

    @property
    def fastapi_kwargs(self) -> Dict[str, Any]:
        return {
            "debug": self.debug,
            "title": self.title,
            "version": self.version,
            "description": self.description,
            "openapi_url": self.openapi_url,
            "redoc_url": self.redoc_url,
            "docs_url": self.docs_url,
        }

# settings = Settings(_env_file='prod.env', _env_file_encoding='utf-8')   实例化优先于Config
# settings = Settings(_env_file=None) 不加载任何变量文件
