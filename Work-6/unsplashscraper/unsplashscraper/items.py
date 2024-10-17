# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class UnsplashscraperItem(scrapy.Item):
    image_url = scrapy.Field()
    image_name = scrapy.Field()
    category = scrapy.Field()
    image_path = scrapy.Field()
