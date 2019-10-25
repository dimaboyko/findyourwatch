import os
import json
import requests

BASE_API_URL = os.environ['BASE_API_URL']

if __name__ == "__main__":
    API_KEY = os.environ['API_KEY']

    r = requests.post('%s/v1/brands' % BASE_API_URL, data = {'key': API_KEY,
                                                             'format': 'json'})

    with open('../data/api/brands.json', 'w') as f:
        f.write(r.text)
