import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

# We manually build the string to ensure no weird hidden characters 
# from the environment interfere.
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
database = os.getenv("DB_NAME")

# NOTICE: We changed the driver to 'postgresql+psycopg' (No '2')
DATABASE_URL = f"postgresql+psycopg://{user}:{password}@{host}:{port}/{database}"

engine = create_engine(
    DATABASE_URL,
    client_encoding='utf8' # Force UTF8 at the engine level
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()