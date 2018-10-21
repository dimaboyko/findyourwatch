import scrapy


class ModelesSpider(scrapy.Spider):
    name = "models"

    def _load_urls():
        import json
        f = open('../data/brands.json')
        return [x['url'] for x in json.load(f)][ :1]

    start_urls = _load_urls()

    # def process_request(self,request,spider):
    #     # agent=UserAgent().firefox
    #     countries = ['fr', 'jp', 'nl', 'de', 'sg', 'us-ny', 'uk', 'us', 'open']
    #     request.meta['proxy']='http://{country}.proxymesh.com:31280'.format(country=random.choice(countries))
    #     # request.headers.update({'User-Agent':agent})

    def parse(self, response):
        # if response.css('form::attr(action)').extract_first() == 'captcha':
            # yield scrapy.Request(url=response.url, dont_filter=True)

        for watch in response.css('div.watch-block'):
            yield {
                'url': watch.css('a::attr(href)').extract_first()
            }
