import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

MYSQL_USER = os.getenv("DB_USER")
# MYSQL_PASSWORD = os.getenv("DB_PASSWORD")
MYSQL_PASSWORD = quote_plus(os.getenv("DB_PASSWORD"))
MYSQL_HOST = os.getenv("DB_HOST")
MYSQL_PORT = os.getenv("DB_PORT")
MYSQL_DATABASE = os.getenv("DB_NAME")

# DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"

DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"

# print(DATABASE_URL)

## Connection
engine = create_engine(DATABASE_URL)

## Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally: 
        db.close()

## Base
Base = declarative_base()