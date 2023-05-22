from scrapy import signals
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message

# useful for handling different item types with a single interface
from lazy_crawler.lib.user_agent import get_user_agent

class CrawlerSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

"""Set User-Agent header per spider or use a default value from settings"""
class RandomUserAgentMiddleware(object):

    """This middleware allows spiders to override the user_agent"""

    def __init__(self, user_agent=''):
        self.user_agent = get_user_agent('random')

    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler.settings['USER_AGENT'])
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        return o

    def spider_opened(self, spider):
        self.user_agent = getattr(spider, 'user_agent', self.user_agent)

    def process_request(self, request, spider):
        if self.user_agent:
            request.headers.setdefault(b'User-Agent', self.user_agent)

#you can find list of user-agent in https://www.useragentstring.com/pages/useragentstring.php

class CustomRetryMiddleware(RetryMiddleware):
    def process_response(self, request, response, spider):
        if response.status in self.retry_http_codes:
            reason = response_status_message(response.status)
            print('now waiting for shor time......')
            spider.logger.warning(f'Retrying request {request} (failed with {response.status}): {reason}')
            return self._retry(request, reason, spider) or response
        return response
