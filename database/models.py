from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

from database import engine

# Create a base class for declarative class definitions
Base = declarative_base()


# Define the Transcript class
class Transcript(Base):
    __tablename__ = 'transcripts'

    id = Column(String, primary_key=True)
    user_id = Column(String, primary_key=True)
    recording_name = Column(String)
    audio_file_name = Column(String, unique=True)
    tracks = Column(String)
    transcript = Column(String)
    summary = Column(String)
    timestamp = Column(DateTime)


# Create the tables in the database (if they don't exist)
Base.metadata.create_all(engine)
