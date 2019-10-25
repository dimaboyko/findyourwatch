import os
import scrapy

BASE_URL = os.environ['BASE_URL']

class BrandsSpider(scrapy.Spider):
    name = "brands"
    start_urls = [
        '%s/watches' % BASE_URL
    ]

    def parse(self, response):
        for brand in response.css('div.brand-box'):
            for family in brand.css('.link-color')[1: ]:
                yield {
                    'url': family.css('a::attr(href)').extract_first()
                }
