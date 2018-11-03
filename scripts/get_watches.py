import os
import time
import json
import requests
from bs4 import BeautifulSoup

BASE_URL = os.environ['BASE_URL']

def get_all_families():
    with open('../data/brands_urls.json') as f:
        family_urls = json.load(f)
    families = [tuple(x['url'].split('/')[-2: ]) for x in family_urls]

    return families


def get_scraped_families():
    brands = [x for x in os.listdir('../data/watches') if x != '.DS_Store']
    families = []

    for brand in brands:
        files = os.listdir('../data/watches/%s' % brand)
        files = [x for x in files if x != '.DS_Store']
        families.extend([(brand, f.split('.')[0]) for f in files])

    return families


def get_needs_to_scrape():
    families = get_all_families()
    scraped_families = get_scraped_families()
    print(len(families))
    print(len(scraped_families))

    families_for_scrape = list(set(families) - set(scraped_families))
    print(len(families_for_scrape))

    return families_for_scrape


def get_watches_links_from_family_page(url):
    session = requests.session()
    r = session.get(url, timeout=2)

    if not r.ok:
        print('EMPTY')
        return None

    soup = BeautifulSoup(r.text, "lxml")

    watches_links = [x.attrs['href'] for x in soup.find_all('a', {'class': 'bottomtext'})]
    print(len(watches_links))

    return watches_links


def main():
    families_for_scrape = get_needs_to_scrape()

    for brand, family in families_for_scrape:
        print(brand, family)
        url = '%s/%s/%s' % (BASE_URL, brand, family)

        try:
            watches_links = get_watches_links_from_family_page(url)
        except requests.exceptions.Timeout:
            print('TIMEOUT')
            continue

        if watches_links:
            with open('../data/watches/%s/%s.json' % (brand, family), 'w') as f:
                json.dump(watches_links, f)

        time.sleep(3)
        print()


if __name__ == '__main__':
    main()

