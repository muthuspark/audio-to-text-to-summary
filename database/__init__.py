from dotenv import dotenv_values
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

config = dotenv_values(".env")

DB_URL = (f"postgresql://{config.get('POSTGRES_USER')}:"
          f"{config.get('POSTGRES_PASSWORD')}@{config.get('POSTGRES_HOST')}:"
          f"{config.get('POSTGRES_PORT')}/{config.get('POSTGRES_DB')}")

# Create an SQLAlchemy engine
engine = create_engine(DB_URL)

# Create a sessionmaker
Session = sessionmaker(bind=engine)
