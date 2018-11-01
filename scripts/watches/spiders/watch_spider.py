import os
import re
from bs4 import BeautifulSoup
import scrapy


class WatchSpider(scrapy.Spider):
    name = "watch"

    def get_pages():
        html_folder_parts = os.path.dirname(os.path.realpath(__file__)).split('/')[ :-3] + ['data', 'html']

        links_to_files = []
        brands = [x for x in os.listdir('/'.join(html_folder_parts)) if x != '.DS_Store']
        for brand in brands:
            families = [x for x in os.listdir('/'.join(html_folder_parts + [brand])) if x != '.DS_Store']
            for family in families:
                models = [x for x in os.listdir('/'.join(html_folder_parts + [brand, family])) if x != '.DS_Store']
                for model in models:
                    path = 'file://' + '/'.join(html_folder_parts + [brand, family, model])
                    links_to_files.append(path)

        return links_to_files

    start_urls = get_pages()


    def start_requests(self):
        for path in self.start_urls:
            yield scrapy.http.Request(path, dont_filter=False)


    @staticmethod
    def parse_table(table):
        table_data = {}
        for row in table.css('tr'):
            row_name = row.css('th::text').extract_first()
            row_name_sanitized = row_name[ :-1].lower()
            
            row_value = row.css('td a::text').extract_first()
            if not row_value:
                row_value = row.css('td::text').extract_first()

            table_data[row_name] = row_value

        return table_data


    def parse(self, response):
        watch = {}

        table_names = ['reference', 'case', 'dial', 'movement']
        tables = response.css('table.info-table')

        for i, table in enumerate(tables):
            table_name = table_names[i]
            watch[table_name] = WatchSpider.parse_table(table)

        soup = BeautifulSoup(response.text)

        watch['caliber'] = soup.find('h2', {'class': 'caliber'}).findNextSibling().get_text()
        watch['description'] = soup.find('h2', {'class': 'description'}).findNextSibling().get_text()

        watch['photos'] = [x for x in response.css('img::attr(src)').extract() if re.match('.*\.jpg', x)]

        yield watch
