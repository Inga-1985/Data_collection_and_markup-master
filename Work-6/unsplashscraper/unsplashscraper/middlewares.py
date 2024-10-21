# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from itemadapter import is_item, ItemAdapter

class UnsplashscraperSpiderMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        # Этот метод используется Scrapy для создания вашего middleware.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Вызывается для каждого ответа, который проходит через middleware.
        # Должен вернуть None или вызвать исключение.
        return None def process_spider_output(self, response, result, spider):
        # Вызывается с результатами, возвращенными от паука, после обработки ответа.
        # Должен вернуть итерируемый объект Request или item.
        for item in result:
            yield item def process_spider_exception(self, response, exception, spider):
        # Вызывается, когда паук или метод process_spider_input() вызывает исключение.
        # Должен вернуть None или итерируемый объект Request или item.
        spider.logger.error(f"Exception occurred: {exception}")
        return None  # или можно вернуть список запросов для повторной попытки def process_start_requests(self, start_requests, spider):
        # Вызывается с начальными запросами паука.
        # Должен вернуть только запросы (не items).
        for request in start_requests:
            yield request

    def spider_opened(self, spider):
        spider.logger.info(f"Spider opened: {spider.name}")


class UnsplashscraperDownloaderMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        # Этот метод используется Scrapy для создания вашего middleware.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Вызывается для каждого запроса, проходящего через downloader middleware.
        # Должен вернуть None, Response, Request или вызвать IgnoreRequest.
        return None def process_response(self, request, response, spider):
        # Вызывается с ответом, возвращенным от downloader.
        # Должен вернуть Response, Request или вызвать IgnoreRequest.
        return response

    def process_exception(self, request, exception, spider):
        # Вызывается, когда обработчик загрузки или метод process_request() вызывает исключение.
        # Должен вернуть None, Response или Request.
        spider.logger.error(f"Download error: {exception}")
        return None  # или можно вернуть запрос для повторной попытки

    def spider_opened(self, spider):
        spider.logger.info(f"Spider opened: {spider.name}")