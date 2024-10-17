import scrapy
from unsplashscraper.items import UnsplashscraperItem

class UnsplashSpider(scrapy.Spider):
    name = "unsplash"
    allowed_domains = ["unsplash.com"]
    start_urls = ["https://unsplash.com"]

    def parse(self, response):
        # Find categories on the main page
        categories = response.css('a[class="wuIW2 R6ToQ"]::attr(href)').getall()
        self.logger.info(f"Found categories: {categories}")
        for category in categories[4:]:
            yield scrapy.Request(url=response.urljoin(category), callback=self.parse_category)

    def parse_category(self, response):
        photos = response.css('a[itemprop="contentUrl"]::attr(href)').getall()
        self.logger.info(f"Found photos in category: {photos}")
        for photo in photos:
            yield scrapy.Request(url=response.urljoin(photo), callback=self.parse_photo)

    def parse_photo(self, response):
        # Extract information about the photo
        item = UnsplashscraperItem()

        # Extract image URL
        img_tag = response.css('div.wdUrX img::attr(srcset)').get()
        if img_tag:
            srcset_links = img_tag.split(',')
            first_img_url = srcset_links[0].split()[0]
            item['image_url'] = first_img_url
        else:
            self.logger.warning("Image URL not found, setting to None.")
            item['image_url'] = None

        # Extract image name
        item['image_name'] = response.css('h1.vev3s::text').get(default='No Title')

        # Extract category
        item['category'] = response.css('a[class="ZTh7D kXLw7"]::text').get(default='No Category')
    
        yield item