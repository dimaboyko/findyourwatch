import scrapy


class BrandsSpider(scrapy.Spider):
    name = "brands"
    start_urls = [
        'https://watchbase.com/watches'
    ]

    def parse(self, response):
        for brand in response.css('div.brand-box'):
            for family in brand.css('.link-color')[1: ]:
                yield {
                    'url': family.css('a::attr(href)').extract_first()
                }
