import scrapy


class UrlsSpider(scrapy.Spider):
    name = "urls"

    start_urls = ['https://hidemyna.me/en/proxy-list/?type=s#list']

    def parse(self, response):
        # if response.css('form::attr(action)').extract_first() == 'captcha':
            # yield scrapy.Request(url=response.url, dont_filter=True)

        for watch in response.css('div.watch-block'):
            yield {
                'url': watch.css('a::attr(href)').extract_first()
            }
