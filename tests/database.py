from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from src.main_withORM import app

from src.databaseORM import get_db
from src.databaseORM import Base
from alembic import command

import configparser

creden = configparser.ConfigParser()
creden.read_file(open('calter.config'))

host = creden["LOCALPG"]["PG_HOST"]
database = creden["LOCALPG"]["PG_DB_FAST"]
port = creden["LOCALPG"]["PG_PORT"]
passwd = creden["LOCALPG"]["PG_PASS"]
user = creden["LOCALPG"]["PG_UNAME"]

# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:password123@localhost:5432/fastapi_test'
SQLALCHEMY_DATABASE_URL = f'postgresql://{user}:{passwd}@{host}:{port}/{database}_test'


engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():

        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
