# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from sqlalchemy.orm import sessionmaker
from scrapy.exceptions import DropItem

from .models.onge_model import (db_connect, create_table,
                                Page, Post, Tag, Category)


class QartnewsurferPipeline(object):
    def __init__(self):
        """
        Initializes database connection and sessionmaker
        Creates tables
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """Save quotes in the database
        This method is called for every item pipeline component
        """

        session = self.Session()
        page = Page()
        post = Post()
        tag = Tag()
        category = Category()

        page.title = item["title"]
        page.url = item["url"]
        page.img = item["img"]
        page.date = item["date"]

        post.text = item['text']
        post.page = page

        if "tags" in item:
            for tag_name in item["tags"]:
                tag = Tag(name=tag_name)
                # check whether the current tag already exists in the database
                exist_tag = session.query(Tag).filter_by(name=tag.name).first()
                if exist_tag is not None:  # the current tag exists
                    tag = exist_tag
                post.tags.append(tag)

        if "categories" in item:
            for category_name in item["categories"]:
                category = Category(geo=category_name)
                # check whether the current tag already exists in the database
                exist_category = session.query(Category).filter_by(geo=category.geo).first()
                if exist_category is not None:  # the current tag exists
                    category = exist_category
                post.categories.append(category)

        try:
            session.add(post)
            session.commit()

        except:
            session.rollback()
            raise

        finally:
            session.close()

        return item
