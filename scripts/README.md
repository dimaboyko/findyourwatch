To get all families of watches brands urls:

```bash
scrapy crawl brands -o ../data/brands.json
```

Set env variable `API_KEY` with api key for watchbase before running scripts to fetch data through the API (`get_brands.py`, `get_models.py`).
