from sqlmodel import SQLModel, create_engine, Session
from conf.config import get_app_settings


settings = get_app_settings()
db = settings.mysql_dict
db_uri = f"mysql://{db.mysql_user}:{db.mysql_password}@{db.mysql_host}:{db.mysql_port}/{db.mysql_db}"

engine = create_engine(db_uri, future=True, echo=True)


