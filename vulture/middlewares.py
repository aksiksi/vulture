import re
import random

from scrapy import Item
from scrapy.http import Request

class UserAgentMiddleware(object):
    '''Randomizes the user agent for each Request.'''
    def __init__(self, user_agents):
        self.user_agents = user_agents

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        cls(settings['USER_AGENTS'])

    def process_spider_output(self, response, result, spider):
        for i, r in enumerate(result):
            if isinstance(r, Request):
                r.headers['User-Agent'] = random.choice(self.user_agents)
        return result
