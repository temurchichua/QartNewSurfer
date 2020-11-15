import scrapy


class TemplateSpider(scrapy.Spider):

    def parse(self, response):
        page = response.url.split(self.target.spliter)[1]
        filename = f'{self.target.name}-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')
