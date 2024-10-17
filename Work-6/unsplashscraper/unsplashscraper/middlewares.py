from scrapy import signals
from itemadapter import is_item, ItemAdapter


class UnsplashscraperSpiderMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        # Создаем экземпляр класса и подключаем сигнал открытия паука
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Вызывается для каждого ответа, который проходит через middleware и попадает в паука.
        return None  # Здесь можно добавить логику обработки входящих ответов.

    def process_spider_output(self, response, result, spider):
        # Вызывается с результатами, возвращенными от паука после обработки ответа.
        for i in result:
            yield i  # Возвращаем результаты, полученные от паука.

    def process_spider_exception(self, response, exception, spider):
        # Вызывается, когда возникает исключение в пауке или в process_spider_input().
        spider.logger.error(f"Spider error: {exception}")  # Логируем ошибку.
        return None  # Можно вернуть запросы или элементы, если нужно.

    def process_start_requests(self, start_requests, spider):
        # Вызывается с начальными запросами паука.
        for r in start_requests:
            yield r  # Возвращаем начальные запросы.

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s", spider.name)


class UnsplashscraperDownloaderMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        # Создаем экземпляр класса и подключаем сигнал открытия паука
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Вызывается для каждого запроса, который проходит через downloader middleware.
        return None  # Здесь можно добавить логику обработки запросов.

    def process_response(self, request, response, spider):
        # Вызывается с ответом, возвращенным от downloader.
        return response  # Здесь можно добавить логику обработки ответов.

    def process_exception(self, request, exception, spider):
        # Вызывается при возникновении исключения во время обработки запроса.
        spider.logger.error(f"Downloader error: {exception}")  # Логируем ошибку.
        return None  # Можно вернуть запросы или элементы, если нужно.

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s", spider.name)
