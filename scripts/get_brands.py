import os
import json
import requests

if __name__ == "__main__":
    API_KEY = os.environ['API_KEY']

    r = requests.post('http://api.watchbase.com/v1/brands', data = {'key': API_KEY,
                                                                    'format': 'json'})

    with open('../data/api/brands.json', 'w') as f:
        f.write(r.text)
