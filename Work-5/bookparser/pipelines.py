# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
import logging

class BookparserPipeline:
    def __init__(self):
        # Настраиваем клиент MongoDB (IP, порт)
        self.client = MongoClient('localhost', 27017)
        # Задаём название базы данных ('books')
        self.mongo_base = self.client.books # Счетчик обработанных страниц
        self.count_page = 0

    def open_spider(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)

    def close_spider(self, spider):
        self.client.close()
        spider.logger.info("Spider closed: %s" % spider.name)

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        collection = self.mongo_base[spider.name]

        # Задание id
        try:
            *_, id, _ = adapter.get('link').split('/')
            adapter['_id'] = id except (ValueError, AttributeError):
            adapter['_id'] = None
            spider.logger.warning("Failed to extract ID from link: %s", adapter.get('link'))

        # Обработка названия книги
        try:
            _, name = adapter.get('name').split(':')
            adapter['name'] = name.strip()
        except (ValueError, AttributeError):
            spider.logger.warning("Failed to process name: %s", adapter.get('name'))

        # Обработка полей с множественными значениями
        for field in ['author', 'translator', 'artist', 'editor', 'publishing', 'series', 'collection', 'genre']:
            adapter[field] = ', '.join(adapter.get(field, []))

        # Обработка года издания книги
        try:
            *_, year, _ = adapter.get('year', '').split(' ')
            adapter['year'] = int(year)
        except (ValueError, AttributeError):
            adapter['year'] = None

        # Обработка массы книги
        try:
            *_, weight, _ = adapter.get('weight', '').split(' ')
            adapter['weight'] = int(weight)
        except (ValueError, AttributeError):
            adapter['weight'] = None # Обработка размеров книги
        try:
            *_, dimensions, _ = adapter.get('dimensions', '').split(' ')
            length, width, height = dimensions.split('x')
            adapter['dimensions'] = {'length': int(length), 'width': int(width), 'height': int(height)}
        except (ValueError, AttributeError):
            adapter['dimensions'] = {'length': None, 'width': None, 'height': None}

        # Обработка рейтинга книги try:
            adapter['rating'] = float(adapter.get('rating'))
        except (ValueError, TypeError):
            adapter['rating'] = None

        # Обработка цены книги
        try:
            adapter['price'] = float(adapter.get('price'))
        except (ValueError, TypeError):
            adapter['price'] = None

        try:
            # Добавляем запись в базу данных collection.insert_one(adapter.asdict())
        except Exception as e:
            spider.logger.error("Ошибка добавления документа: %s", e)

        # Выводим информацию о состоянии процесса
        self.count_page += 1
        spider.logger.info('Обработано %d книг', self.count_page)

        return item