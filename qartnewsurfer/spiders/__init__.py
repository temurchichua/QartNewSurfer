# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
from qartnewsurfer.page_setup import OnGe
from .template_spider import TemplateSpider


class OngeSpider(TemplateSpider):
    target = OnGe()
    name = 'onge'
    start_urls = [
        target.get_url(0,1)
    ]
