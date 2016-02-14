import re
import scrapy

from datetime import datetime, timedelta
from ..items import DubizzleItem

class DubizzleSpider(scrapy.Spider):
    name = 'dubizzle'
    allowed_domains = ['dubizzle.com']
    start_urls = ['http://uae.dubizzle.com/motors/used-cars/']

    max_page = 0

    # rules = (
    #     # Ad listings
    #     Rule(LinkExtractor(allow=(AD_REGEX,)), callback='parse_listing'),
    #
    #     # Pages
    #     Rule(LinkExtractor(allow=(PAGE_REGEX,), process_value='check_page')),
    # )

    def parse(self, response):
        raise NotImplementedError

    def parse_listing(self, response):
        item = DubizzleItem()
        item['title'] = response.url
        item['make'] = 'Testing'
        item['model'] = 'Yep!'
        yield item



