import os
import json

def get_scraped_families():
    brands = [x for x in os.listdir('../data/watches') if x != '.DS_Store']
    families = []

    for brand in brands:
        files = os.listdir('../data/watches/%s' % brand)
        files = [x for x in files if x != '.DS_Store']
        families.extend([(brand, f) for f in files])

    return families


def read_file(path):
    with open(path, 'r') as f:
        return json.load(f)


def main():
    families = get_scraped_families()

    all_watches_links = []
    for brand, family in families:
        path = '../data/watches/%s/%s' % (brand, family)
        all_watches_links.extend(read_file(path))
    all_watches_links = list(set(all_watches_links))

    with open('../data/watches_links.json', 'w') as f:
        json.dump(all_watches_links, f)

if __name__ == "__main__":
    main()
