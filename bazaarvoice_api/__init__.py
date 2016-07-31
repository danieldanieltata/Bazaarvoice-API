import json
from math import floor

import requests

from bazaarvoice_api.product import Product


class BazaarvoiceAPI:
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/51.0.2704.103 Safari/537.36'
    }

    api_key = None
    searched_brand = None

    reviews_list = []

    def __init__(self, api_key, searched_brand):
        self.api_key = api_key
        self.searched_brand = searched_brand

        if not isinstance(searched_brand, str):
            raise Exception('You must provide string in searched_brand var, got: ' + str(type(searched_brand)))

        if 'http://' in searched_brand:
            raise Exception('You cant provide url')

    def make_url(self):
        searched_brand = self.searched_brand
        api_key = self.api_key

        base_url = 'https://api.bazaarvoice.com/data/'

        start_url = base_url + "products.json?apiversion=5.4&passkey=" + api_key + \
                    "&ExcludeFamily=true&limit=100&include=Categories&search=" + searched_brand + '&offset=0'

        return start_url

    # Check if the response received is OK
    @staticmethod
    def _check_response(json_data):
        has_errors = bool(json_data['HasErrors'])
        if has_errors:
            errors = json_data['Errors']

            errors_str_handler = ''
            for error in errors:
                errors_str_handler += '\n' + error['Message']

            raise Exception('Bad response: ' + errors_str_handler)

    def get_product(self):
        products_url = self.make_url()

        products = self._get_products(products_url)
        for products_list in products:
            for product_data in products_list:
                product_obj = Product(product_data, products_url)

                review_list = []
                for review_obj in product_obj.get_review():
                        review_list.append(review_obj)

                product_obj.__setattr__('reviews', review_list)

                yield product_obj

    def _get_products(self, products_url):
        products_content = requests.get(products_url, headers=self.headers).text
        products_json = json.loads(products_content)

        self._check_response(products_json)

        product_max_offset = int(floor(int(products_json['TotalResults']) / 100.0)) * 100
        for i in range(0, product_max_offset + 100, 100):
            offset = i

            products_url = self._make_next_page_url(offset, products_url)

            yield products_json['Results']

            products_content = requests.get(products_url, headers=self.headers).text
            products_json = json.loads(products_content)

    @staticmethod
    def _make_next_page_url(offset, product_url):
        new_offset = offset + 100

        current_offset_str = 'offset=%d' % offset
        new_offset_str = 'offset=%d' % new_offset

        new_reviews_url = product_url.replace(current_offset_str, new_offset_str)

        return new_reviews_url


bazzare = BazaarvoiceAPI('caKM8b618jM7usc0wJfL98n9Ospp9LvgNilEMqrBHOXSo', 'Aussie')

data_container = []

for prod in bazzare.get_product():
    data_container.append(prod)

pass
