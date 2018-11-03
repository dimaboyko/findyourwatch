import os
import time
import json
import random
import requests
from multiprocessing import Pool


BASE_URL = os.environ['BASE_URL']

class ProxyList:
    def __init__(self):
        self.proxies = []

    def read_proxies(self, source='list.txt'):
        with open(source, 'r') as f:
            for line in f.readlines():
                self.proxies.append(line.strip())

    def random_proxy(self):
        return random.choice(self.proxies)

    def remove_invalid(self, proxy):
        self.proxies.remove(proxy)
        print('Removed proxy %s. Now %s proxies in the list' % (proxy, len(self.proxies)))

proxy_list = ProxyList()
proxy_list.read_proxies()


def get_all_links():
    with open('../data/watches_links.json') as f:
        watches_links = json.load(f)
    watches = [tuple(x.split('/')[-3: ]) for x in watches_links]

    return watches


def get_downloaded_watches():
    brands = [x for x in os.listdir('../data/html') if x != '.DS_Store']

    downloaded_watches = []
    for brand in brands:
        families = os.listdir('../data/html/%s' % brand)
        families = [x for x in families if x != '.DS_Store']
        for family in families:
            watches = os.listdir('../data/html/%s/%s' % (brand, family))
            watches = ['.'.join(w.split('.')[ :-1]) for w in watches if w != '.DS_Store']
            downloaded_watches.extend([(brand, family, w) for w in watches])

    return downloaded_watches


def get_needs_to_download():
    watches = get_all_links()
    downloaded_watches = get_downloaded_watches()

    print("Total watches: %s" % len(watches))
    print("Downloaded watches: %s" % len(downloaded_watches))

    watches_to_download = list(set(watches) - set(downloaded_watches))
    print("Remains to download: %s" % len(watches_to_download))

    return watches_to_download


def process_page(watch):
    brand, family, model = watch
    url = '%s/%s/%s/%s' % (BASE_URL, brand, family, model)

    proxy_address = proxy_list.random_proxy()
    session = requests.session()
    session.proxies = {}
    session.proxies['https'] = proxy_address

    try:
        r = session.get(url, timeout=3)
    except (requests.exceptions.Timeout, requests.exceptions.ProxyError,
            requests.exceptions.ConnectionError):
        print('FAILED %s' % url)
        proxy_list.remove_invalid(proxy_address)
        return None

    if r.history:
        print('FAILED %s' % url)
        proxy_list.remove_invalid(proxy_address)
        return None

    path = '../data/html/%s/%s/%s.html' % (brand, family, model)
    with open(path, 'w') as f:
        f.write(r.text)

    print('SUCCESS %s through %s; len=%s' % (url, proxy_address, len(r.text)))


def download_all_watches():
    watches = get_needs_to_download()

    pool = Pool(10)
    pool.map(process_page, watches)


if __name__ == '__main__':
    download_all_watches()
