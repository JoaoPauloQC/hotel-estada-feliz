from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from src.Model.models import Base
# Create an engine connected to a SQLite database file named 'my_database.db'
# The 'echo=True' argument logs all SQL commands executed, useful for debugging.
engine = create_engine('sqlite:///hotel.db', echo=True)

Session = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)