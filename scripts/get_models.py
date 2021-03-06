import os
import json
import time
import requests

BASE_API_URL = os.environ['BASE_API_URL']

def main():
    with open('../data/api/brands.json') as f:
        data = f.read()

    brands = json.loads(data)['brands']

    API_KEY = os.environ['API_KEY']

    for brand in brands:
        brand_name = brand['name']
        brand_id = brand['id']
        print(brand_name)

        r = requests.post('%s/v1/watches' % BASE_API_URL, data = {'key': API_KEY,
                                                                  'brand-id': brand_id,
                                                                  'format': 'json'})



        with open('../data/api/watches/%s.json' % brand_name, 'w') as f:
            f.write(r.text)

        time.sleep(1)


if __name__ == '__main__':
    main()
