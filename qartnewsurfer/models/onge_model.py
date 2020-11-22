from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy import (
    Integer, String, Text)
from sqlalchemy.orm import relationship
from qartnewsurfer.models import Base, Session
from sqlalchemy.orm import sessionmaker
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
    url_tag = Column('url_tag', Text(), unique=True)


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True)
    geo = Column('geo', String(30), unique=True)
    eng = Column('eng', String(30), unique=True)
    url_tag = Column('url_tag', Text(), unique=True)
    number_of_posts = Column('post_count', Integer)
    posts = relationship('Post', secondary='post_category',
                         lazy='dynamic', backref="category")  # M-to-M for quote and tag
