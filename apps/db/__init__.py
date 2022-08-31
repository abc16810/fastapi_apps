from .models import Users, Team, Hero, UserCreate, UserRead, UserUpdate
from sqlmodel import SQLModel, Session
from .database import engine


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

