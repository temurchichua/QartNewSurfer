from scrapy.utils.project import get_project_settings
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

Base = declarative_base()
CONNECTION_STRING = "sqlite:///scrapy_quotes.db"


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(get_project_settings().get("CONNECTION_STRING"))


def create_table(engine):
    Base.metadata.create_all(engine)


engine = db_connect()
create_table(engine)
Session = sessionmaker(bind=engine)


class Status(Base):
    __tablename__ = "status"

    id = Column(Integer, primary_key=True)
    current_category = Column('current_category', Integer)
    current_surfer = Column('current_surfer', String())
