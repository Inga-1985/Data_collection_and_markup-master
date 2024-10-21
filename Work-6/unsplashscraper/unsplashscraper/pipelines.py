import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import CsvItemExporter

class CustomImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        # Получаем имя изображения из метаданных запроса
        image_name = request.meta['image_name']
        return f'{image_name}.jpg'

    def get_media_requests(self, item, info):
        # Создаем запрос для загрузки изображения request = scrapy.Request(item['image_url'])
        request.meta['image_name'] = item['image_name']
        return [request]  # Возвращаем список запросов def item_completed(self, results, item, info):
        # Обрабатываем результаты загрузки изображений
        image_path = [x['path'] for ok, x in results if ok]
        if image_path:
            item['image_path'] = image_path[0]  # Сохраняем путь к загруженному изображению return item

class CsvPipeline:
    def open_spider(self, spider):
        # Открываем файл для записи данных при запуске паука
        self.file = open('images_data.csv', 'wb')
        self.exporter = CsvItemExporter(self.file)
        self.exporter.fields_to_export = ['image_name', 'category', 'image_url', 'image_path']
        self.exporter.start_exporting()

    def close_spider(self, spider):
        # Завершаем экспорт и закрываем файл при завершении работы паука self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        # Обрабатываем каждый элемент, экспортируя его в CSV self.exporter.export_item(item)
        return item