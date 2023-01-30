from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import configparser

creden = configparser.ConfigParser()
creden.read_file(open('calter.config'))

host = creden["LOCALPG"]["PG_HOST"]
database = creden["LOCALPG"]["PG_DB_FAST"]
port = creden["LOCALPG"]["PG_PORT"]
passwd = creden["LOCALPG"]["PG_PASS"]
user = creden["LOCALPG"]["PG_UNAME"]

SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{passwd}@{host}/{database}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

