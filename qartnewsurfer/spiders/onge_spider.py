import scrapy

from qartnewsurfer.models import Session, Status
from qartnewsurfer.models.onge_model import Category
from qartnewsurfer.page_setup import OnGe
from sqlalchemy.orm import sessionmaker

target = OnGe()


class OngeSpider(scrapy.Spider):
    name = 'onge'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def start_requests(self):
        print(target.base_url)
        category = getattr(self, 'category', 1)
        start_page = getattr(self, 'start_page', 1)

        session = Session()
        status = Status()
        current_status = session.query(Status).first()
        if current_status:
            status = current_status
        else:
            status.current_category = category

        try:
            session.add(status)
            session.commit()

        except:
            session.rollback()
            raise

        finally:
            session.close()

        start_url = target.get_url(int(category), int(start_page))

        yield scrapy.Request(start_url, self.parse)

    def parse(self, response):
        yield from response.follow_all(css='a.overlay-link', callback=self.parse_post)

        next_page = response.css('a.pager-left::attr(href)').get()
        next_page_id = int(next_page.split("=")[1])
        max_page = getattr(self, 'max_page', None)
        if next_page is not None and max_page is None or next_page_id < int(max_page):
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

        else:
            session = Session()

            current_status = session.query(Status).first()
            if current_status:
                current_status.current_category += 1

                next_category = session.query(Category).get(current_status.current_category)
                if next_category:
                    next_page = target.get_url(next_category.id)

                    try:
                        session.add(current_status)
                        session.commit()

                    except:
                        session.rollback()
                        raise

                    finally:
                        session.close()

                    yield scrapy.Request(next_page, callback=self.parse)

            else:
                print("can't find the current status")

    def parse_post(self, response):
        text = " ".join(response.xpath("/html/body/div[3]/div[1]/div/div/article/div[3]/p/text()").getall())
        if not text:
            text = " ".join(response.xpath("/html/body/div[3]/div[1]/div/div/article/div[4]/p/text()").getall())
        date = response.xpath("/html/body/div[3]/div[1]/div/div/article/header/div/time/@datetime").get()

        if not date: # onge - quote page.
            date = response.xpath("/html/body/div[3]/div[1]/div[1]/div/dov/section/article/span/@datetime").get()
            text = " ".join(response.xpath("/html/body/div[3]/div[1]/div[1]/div/dov/section/article/blockquote/p/text()").getall())

        yield {
            'title': response.css('title::text').get(),
            'url': response.request.url,
            'img': response.xpath("/html/body/div[3]/div[1]/div/div/article/figure/div/div/div/img/@src").get(),
            'date': date,
            'text': text,
            'tags': [tag.strip() for tag in
                     response.xpath("/html/body/div[3]/div[1]/div/div/article/footer/p/a/text()").getall()
                     ],
            'categories': zip(
                response.xpath("/html/body/div[3]/div[1]/div/div/article/header/div/ul/li/a/text()").getall(),
                response.xpath("/html/body/div[3]/div[1]/div/div/article/header/div/ul/li/a/@href").getall())
        }
