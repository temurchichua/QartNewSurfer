import scrapy


class RadioTavisuplebaSpider(scrapy.Spider):
    name = 'radio_tavisupleba'

    def start_requests(self):
        start_urls = ['https://www.radiotavisupleba.ge/a/31333277.html', ]
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        date = \
            response.xpath('//*[@id="content"]/div[1]/div[1]/div/div[3]/div/div/span/time/text()').get()
        img = \
            response.xpath('//*[@id="content"]/div[1]/div[1]/div/div[5]/div/figure/div/div/img/@src').get()

        title = response.xpath('//*[@id="content"]/div[1]/div[1]/div/div[2]/h1/text()').get()
        text = " ".join(response.xpath('//*[@id="article-content"]/div[1]/p/text()').getall())
        url = response.request.url

        yield {
            'date': date,
            'img': img,
            'title': title,
            'text': text,
            'url': url
        }
