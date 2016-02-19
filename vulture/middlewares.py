import random, logging

from scrapy.exceptions import IgnoreRequest


class DubizzleRequestMiddleware(object):
    """
    1. Randomizes the user agent for each Request.
    2. Drops any duplicate requests.
    3. Drops any requests for "other-make".
    """
    def __init__(self, user_agents):
        self.user_agents = user_agents
        self.requests = frozenset()

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        cls(settings['USER_AGENTS'])

    def process_request(self, request, spider):
        request.headers['User-Agent'] = random.choice(self.user_agents)

        # Drop requests for "other-make"
        if 'other-make' in request.url:
            raise IgnoreRequest('Other make ignored.')

        # Drop duplicate Request
        if request.url in self.requests:
            raise IgnoreRequest('Dropping duplicate {0}'.format(request.url))

        # Otherwise, add URL to seen list
        else:
            self.requests |= request.url
