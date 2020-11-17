from sqlalchemy import create_engine, Column, Table, ForeignKey, MetaData
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Integer, String, Date, DateTime, Float, Boolean, Text)
from scrapy.utils.project import get_project_settings

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


# Association Table for Many-to-Many relationship between Page and Tag
# https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html#many-to-many
post_tag = Table('post_tag', Base.metadata,
                 Column('post_id', Integer, ForeignKey('post.id')),
                 Column('tag_id', Integer, ForeignKey('tag.id'))
                 )

post_category = Table('post_category', Base.metadata,
                      Column('post_id', Integer, ForeignKey('post.id')),
                      Column('category_id', Integer, ForeignKey('category.id'))
                      )


class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True)
    text = Column('text', Text())
    page_id = Column(Integer, ForeignKey('page.id'))  # One quotes to one page
    tags = relationship('Tag', secondary='post_tag',
                        lazy='dynamic', backref="post")  # M-to-M for post and tag
    categories = relationship('Category', secondary='post_category',
                              lazy='dynamic', backref="post")  # M-to-M for post and category


class Page(Base):
    __tablename__ = "page"

    id = Column(Integer, primary_key=True)
    title = Column('title', Text(), unique=True)
    url = Column('url', Text(), unique=True)
    date = Column('date', String(30))
    img = Column('img', Text())
    post = relationship('Post', backref='page')  # One author to one Posts


class Tag(Base):
    __tablename__ = "tag"

    id = Column(Integer, primary_key=True)
    name = Column('name', String(30), unique=True)
    posts = relationship('Post', secondary='post_tag',
                         lazy='dynamic', backref="tag")  # M-to-M for quote and tag


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True)
    geo = Column('geo', String(30), unique=True)
    eng = Column('eng', String(30), unique=True)
    url_tag = Column('url_tag', String(30), unique=True)
    max_pages = Column('max_pages', Integer)
    posts = relationship('Post', secondary='post_category',
                         lazy='dynamic', backref="category")  # M-to-M for quote and tag
