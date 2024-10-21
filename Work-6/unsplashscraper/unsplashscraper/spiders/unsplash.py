import scrapy
from unsplashscraper.items import UnsplashscraperItem

class UnsplashSpider(scrapy.Spider):
    name = "unsplash"
    allowed_domains = ["unsplash.com"]
    start_urls = ["https://unsplash.com"]

    def parse(self, response):
        # Найдем категории на главной странице categories = response.css('a[class="wuIW2 R6ToQ"]::attr(href)').getall()
        for category in categories[4:]:
            yield scrapy.Request(url=response.urljoin(category), callback=self.parse_category)

    def parse_category(self, response):
        # Извлечение ссылок на фотографии в категории
        photos = response.css('a[itemprop="contentUrl"]::attr(href)').getall()
        self.logger.info(f"Found {len(photos)} photos in category: {response.url}")
        for photo in photos:
            yield scrapy.Request(url=response.urljoin(photo), callback=self.parse_photo)

        # Обработка пагинации (если есть)
        next_page = response.css('a[aria-label="Next"]::attr(href)').get()
        if next_page:
            yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse_category)

    def parse_photo(self, response):
        # Извлечение информации о фотографии item = UnsplashscraperItem()

        img_tag = response.css('div.wdUrX img::attr(srcset)').get()
        if img_tag:
            srcset_links = img_tag.split(',')
            first_img_url = srcset_links[0].split()[0]
            item['image_url'] = first_img_url
        else:
            item['image_url'] = None  # Если изображение не найдено

        item['image_name'] = response.css('h1.vev3s::text').get(default='No title').strip()
        item['category'] = response.css('a[class="ZTh7D kXLw7"]::text').get(default='No category').strip()

        yield item