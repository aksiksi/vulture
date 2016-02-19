import re

from bs4 import BeautifulSoup
from scrapy import Request, Spider

from ..items import DubizzleItem

BASE_URL = 'https://uae.dubizzle.com/motors/used-cars/'

# Matches make URLs on base page
MAKE_URL_REGEX = re.compile(r'<a href="([\w\-]+/)">')

# Matches listing url ex: dubai.dubizzle.com/motors/used-cars/[make]/[model]/[slug]
# Ignores any URL params i.e. ?back=...
LISTING_URL_REGEX = re.compile(r'https\S+/used-cars/[\w\-]+/[\w\-]+/[^\?\n"]+')

# Matches make and model in URL
MAKE_MODEL_REGEX = re.compile(r'/used-cars/([\w\-]+)/([\w\-])+')

# Selectors for various parts of a listing
LISTING_SELECTORS = {
    'title': 'span.title',
    'date': 'h3.listing-details-header > span',
}

class DubizzleSpider(Spider):
    name = 'dubizzle'

    allowed_domains = ['dubizzle.com']
    start_urls = [BASE_URL]

    def parse(self, response):
        """Parse car model pages, returns list of Requests."""
        makes = re.findall(MAKE_URL_REGEX, response.body)
        make_urls = [BASE_URL + make for make in makes]

        return [Request(url=url, callback=self.parse_make_page) for url in make_urls]

    def parse_make_page(self, response):
        """Parse given make page, returns list of Responses"""

        # List of listing URLs
        listings = re.findall(LISTING_URL_REGEX, response.body)

        # Build Request for each ad listing on page
        reqs = []

        for url in listings:
            # Get model, make from URL
            try:
                m = re.search(MAKE_MODEL_REGEX, url)
                make, model = m.groups()
            except ValueError:
                self.logger.exception('{0}.parse_make_page: m has too few groups.'.format(self.name))
                continue

            meta = {
                'url': url,
                'make': make,
                'model': model
            }

            req = Request(url=url, meta=meta, callback=self.parse_listing_page)
            reqs.append(req)

        return reqs

    def parse_listing_page(self, response):
        """Extract basic info from listing page, returns an Item."""
        body = BeautifulSoup(response.body)

        meta = response.meta

        item = DubizzleItem()

        item['title'] = body.select_one(LISTING_SELECTORS['title']).get_text(strip=True)
        item['date'] = body.select_one(LISTING_SELECTORS['date']).get_text(strip=True)
        item['make'] = meta['make'].title()
        item['model'] = meta['model'].title()

        yield item
