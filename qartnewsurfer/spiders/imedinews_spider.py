import scrapy


class ImediNewsSpider(scrapy.Spider):
    name = "imedinews"
    start_urls = ['https://imedinews.ge/ge/politika/207030/kakha-kuchava-sotsialur-kodeqsze-es-aris-namdvilad-gardamtekhi-momenti-chveni-qveknis-ganvitarebisa-da-im-sakitkhebis-gadatskvetistvis-romelits-namdvilad-schirdeba-chvens-sazogadoebas']


    def parse(self, response):
        category = response.xpath('/html/body/div[3]/div[1]/div[2]/section/div/section/div/div[1]/div[1]/div/a/text()').get()
        date = response.xpath('/html/body/div[3]/div[1]/div[2]/section/div/section/div/div[1]/div[2]/div/div/div[1]/span[1]/text()').get()
        article_title = response.xpath('/html/body/div[3]/div[1]/div[2]/section/div/section/div/div[1]/div[2]/div/div/h1/text()').get()
        article_body = response.xpath('/html/body/div[3]/div[1]/div[2]/section/div/section/div/div[1]/div[2]/div/div/div[5]').xpath('p/text()').getall()

        page_dict = {'category': category,
                     'date' : date,
                     'article title' : article_title,
                     'article body' : article_body}

        yield page_dict
