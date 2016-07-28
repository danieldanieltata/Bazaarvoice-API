import json

import requests

from bazaarvoice_api.review import Review


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

        if len(review_json['Results']) > 0:
            new_reviews_url = self._make_new_page_url(review_json, review_url)
            yield review_json['Results']
            for rev in self._get_reviews(new_reviews_url):
                yield rev

    @staticmethod
    def _make_new_page_url(review_json_data, review_url):
        current_offset = int(review_json_data['Offset'])
        new_offset = current_offset + 100

        current_offset_str = 'offset=%d' % current_offset
        new_offset_str = 'offset=%d' % new_offset

        new_reviews_url = review_url.replace(current_offset_str, new_offset_str)

        return new_reviews_url
