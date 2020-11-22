# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from sqlalchemy.orm import sessionmaker
from scrapy.exceptions import DropItem

from .models import db_connect, create_table
from .models.onge_model import (Page, Post, Tag, Category)


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
        """Save page in the database
        This method is called for every item pipeline component
        """

        session = self.Session()
        page = Page()
        post = Post()
        if "title" in item:
            page.title = item["title"]
            existing_post = session.query(Page).filter_by(title=page.title).first()  # checks if the post exists
            if existing_post is None:
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
                    for category in item["categories"]:
                        category_name = category[0]
                        category_url = category[1].split('category/')[1].split('?')[0]
                        category = Category(geo=category_name, url_tag=category_url, number_of_posts=1)
                        # check whether the current tag already exists in the database
                        exist_category = session.query(Category).filter_by(geo=category.geo).first()
                        if exist_category is not None:  # the current tag exists
                            category = exist_category
                            category.number_of_posts += 1

                        post.categories.append(category)

                try:
                    session.add(post)
                    session.commit()

                except:
                    session.rollback()
                    raise

                finally:
                    session.close()
            else:
                pass
        return item
