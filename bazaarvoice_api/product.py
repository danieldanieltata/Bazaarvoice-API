import json
from math import floor

import requests


class Product(object):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/51.0.2704.103 Safari/537.36'
    }

    reviews_url = ''

    def __init__(self, product_dict, url):
        self.reviews = []
        self.Id = product_dict.pop('Id')
        for k, v in product_dict.items():
            self.__setattr__(k, v)

        self.reviews_url = url.replace('products', 'reviews') + '&Filter=ProductId:' + self.Id + '&offset=0'

    def get_review(self):
        reviews_gen = self._get_reviews(self.reviews_url)
        for review_list in reviews_gen:
            for rev in review_list:
                review_object = Review(rev)

                yield review_object

    def _get_reviews(self, review_url):
        review_content = requests.get(review_url, headers=self.headers).text

        review_json = json.loads(review_content)
        review_max_offset = floor(int(review_json['TotalResults']) / 100.0) * 100

        for i in range(0, review_max_offset + 100, 100):
            offset = i

            review_url = self._make_new_page_url(offset, review_url)

            yield review_json['Results']

            review_content = requests.get(review_url, headers=self.headers).text
            review_json = json.loads(review_content)

    @staticmethod
    def _make_new_page_url(offset, review_url):
        new_offset = offset + 100

        current_offset_str = 'offset=%d' % offset
        new_offset_str = 'offset=%d' % new_offset

        new_reviews_url = review_url.replace(current_offset_str, new_offset_str)

        return new_reviews_url


class Review(object):
    def __init__(self, review_dict):
        for k, v in review_dict.items():
            self.__setattr__(k, v)
