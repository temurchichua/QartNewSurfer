import scrapy
import json


class Nsecurity(scrapy.Spider):
    name = "national_security"
    start_urls =["https://www.nsc.gov.ge/ka/%E1%83%A1%E1%83%98%E1%83%90%E1%83%AE%E1%83%9A%E1%83%94%E1%83%94%E1%83%91%E1%83%98/%E1%83%94%E1%83%A0%E1%83%9D%E1%83%95%E1%83%9C%E1%83%A3%E1%83%9A%E1%83%98-%E1%83%A3%E1%83%A1%E1%83%90%E1%83%A4%E1%83%A0%E1%83%97%E1%83%AE%E1%83%9D%E1%83%94%E1%83%91%E1%83%98%E1%83%A1-%E1%83%A1%E1%83%90%E1%83%91%E1%83%AD%E1%83%9D%E1%83%A1-%E1%83%90.html-25"]


    def __init__(self, **kwargs):
            super().__init__(**kwargs)
            print("#"*50)




    def parse(self, response):
        title = response.css('div.section-info h3::text').get()
        moment = response.css('div.section-info span.date::text').get()
        text = "".join(response.css('div.section-info div.news-inner-text p::text').getall())
        img_src = response.css('div.section-info div.news-inner-text img[src]').attrib['src']
        data = {
            "page_title":title,
            "moment": moment,
            "text": text,
            "img_src": img_src,
            }
        yield data
