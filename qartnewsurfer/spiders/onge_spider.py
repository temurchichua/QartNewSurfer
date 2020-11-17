import scrapy
from qartnewsurfer.page_setup import OnGe


class OngeSpider(scrapy.Spider):
    target = OnGe()
    name = 'onge'

    def start_requests(self):
        start_url = self.target.get_url(0, 1)
        category = getattr(self, 'category', None)
        start_page = getattr(self, 'start_page', None)

        if category is not None:
            start_url = self.target.get_url(int(category), int(start_page))

        yield scrapy.Request(start_url, self.parse)

    def parse(self, response):
        yield from response.follow_all(css='a.overlay-link', callback=self.parse_post)

        next_page = response.css('a.pager-left::attr(href)').get()
        next_page_id = int(next_page.split("=")[1])
        max_page = getattr(self, 'max_page', None)
        if next_page is not None and max_page is None or next_page_id < int(max_page):
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_post(self, response):

        yield {
            'title': response.css('title::text').get(),
            'url': response.request.url,
            'img': response.xpath("/html/body/div[3]/div[1]/div/div/article/figure/div/div/div/img/@src").get(),
            'date': response.xpath("/html/body/div[3]/div[1]/div/div/article/header/div/time/@datetime").get(),
            'text': " ".join(response.xpath("/html/body/div[3]/div[1]/div/div/article/div[3]/p/text()").getall()),
            'tags': [tag.strip() for tag in
                     response.xpath("/html/body/div[3]/div[1]/div/div/article/footer/p/a/text()").getall()
                     ],
            'categories': response.xpath("/html/body/div[3]/div[1]/div/div/article/header/div/ul/li/a/text()").getall()
        }
