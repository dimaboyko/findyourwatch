To get all families of watches brands urls:

```bash
scrapy crawl brands -o ../data/brands.json
```

Set env variable `API_KEY` with api key for watchbase before running scripts to fetch data through the API (`get_brands.py`, `get_models.py`).


To fetch all watches html pages:
- Find some list of HTTPS proxies (e.g. https://free-proxy-list.net/, http://spys.one/en/https-ssl-proxy/)

```bash
python3 get_watch.py
```

Which would save html pages in hierarchy `{watch_brand}/{watch_family}/{watch_name}.html`
You might need to run the script multiple times, since after it has been failed to be fetched - it's not readded to the queue (due to the tricky work of it running in multiple threads)

To scrape all the fields from html run:

```bash
scrapy crawl watch -o ../data/watch.json
```
