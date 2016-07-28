class Review(object):
    def __init__(self, review_dict):
        for k, v in review_dict.items():
            self.__setattr__(k, v)
