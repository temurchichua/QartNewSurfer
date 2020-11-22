import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from qartnewsurfer.spiders import OngeSpider
from qartnewsurfer.models import Session, engine, create_table
from qartnewsurfer.models.onge_model import Category
from qartnewsurfer.page_setup import OnGe, sources

session = Session()
create_table(engine)
onge = OnGe()


class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)


for category in onge.categories:
    category = Struct(**onge.categories[category])
    category = Category(geo=category.geo, url_tag=category.url, eng=category.eng, number_of_posts=1)
    # check whether the current tag already exists in the database
    exist_category = session.query(Category).filter_by(geo=category.geo).first()
    if exist_category is not None:  # the current tag exists
        category = exist_category

    try:
        session.add(category)
        session.commit()

    except:
        session.rollback()
        raise

    finally:
        session.close()

process = CrawlerProcess(get_project_settings())

process.crawl('onge')
process.start()  # the script will block here until the crawling is finished
