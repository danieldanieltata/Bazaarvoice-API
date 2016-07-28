import json
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
    start_url = None

    def __init__(self, api_key, searched_brand):
        self.api_key = api_key
        self.searched_brand = searched_brand

        if not isinstance(searched_brand, str):
            raise Exception('You must provide string in searched_brand var, got: ' + str(type(searched_brand)))

        if 'http://' in searched_brand:
            raise Exception('You cant provide url')

    def start_extracting_products(self):
        self.start_url = self.make_url()

        page_content = requests.get(self.start_url, headers=self.headers).text

        try:
            json_product_data = json.loads(page_content)
        except:
            raise Exception("Page is not json or valid json")

        self._check_response(json_product_data)
        page_data_handler = self._get_products(json_product_data)

        return page_data_handler

    def make_url(self):
        searched_brand = self.searched_brand
        api_key = self.api_key

        base_url = 'https://api.bazaarvoice.com/data/'

        start_url = base_url + "products.json?apiversion=5.4&passkey=" + api_key + \
                    "&ExcludeFamily=true&limit=100&include=Categories&search=" + searched_brand

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

    def _get_products(self, json_product_data):
        products = json_product_data.get('Results', None)

        if products:
            for product_item in products:
                product_obj = Product(product_item, self.start_url)

                yield product_obj


bazzare = BazaarvoiceAPI('caKM8b618jM7usc0wJfL98n9Ospp9LvgNilEMqrBHOXSo', 'Aussie')
gen = bazzare.start_extracting_products()

data_container = []

for prod in gen:
    reviews_list = []
    review_gen = prod.get_review()

    count = 0
    for review in review_gen:
        reviews_list.append(review)

    prod.reviews = reviews_list
    data_container.append(prod)
pass
