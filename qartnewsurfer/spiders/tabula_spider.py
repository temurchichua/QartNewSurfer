import scrapy


class TabulaSpider(scrapy.Spider):
    name = 'tabula'

    def start_requests(self):
        urls = [
            'https://tabula.ge/ge/news/668944-rustavshi-khanjlit-sheiaraghebuli-katsi-kuchashi',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        title = response.xpath('//*[@id="__next"]/div/div[1]/article/header/div/h1/text()').get()
        text = " ".join(response.xpath('//*[@id="__next"]/div/div[1]/article/div[1]/div/div/div[5]/div/p/text()').getall())
        datetime = response.xpath('//*[@id="__next"]/div/div[1]/article/header/div/div/div/time/@datetime').get()
        category = response.xpath('//*[@id="__next"]/div/div[1]/article/header/div/a/text()').get()
        tags = response.xpath('//*[@id="__next"]/div/div[1]/article/div[1]/div/div/div[9]/a/text()').getall()
        img = response.xpath('//*[@id="__next"]/div/div[1]/article/div[1]/div/div/figure/img/@src').get()
        url = response.request.url

        yield {
            'article_title': title,
            'text': text,
            'datetime': datetime,
            'category': category,
            'tags': tags,
            'img': img,
            'url': url,
        }
