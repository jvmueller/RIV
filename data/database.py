import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data.models import Base


# Get the directory where your script is located

basedir = os.path.abspath(os.path.dirname(__file__))
database_path = os.path.join(basedir, 'database.db')


# Use absolute path
engine = create_engine(f'sqlite:///{database_path}')

# Create all tables
Base.metadata.create_all(engine)

# Create session factory
Session = sessionmaker(bind=engine)

def get_session():
    return Session()