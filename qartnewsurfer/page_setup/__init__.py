from string import Template


class SetupTemplate:
    def __init__(self, **source):
        self.__dict__.update(source)


class OnGe(SetupTemplate):
    def __init__(self):
        SetupTemplate.__init__(self, **sources['onge'])

    def get_url(self, category=0, page=0):
        if category in self.categories and self.categories[category]['max_pages'] is None or page in range(self.categories[category]['max_pages']):
            return (f"{self.base_url}"                                   # base
                    f"/category/{self.categories[category]['url']}"      # category
                    f"?page={page}")                                     # page
        else:
            raise ValueError("page or/and category is/are out of range")


sources = {
    "onge": {
        'name': 'onge',
        'base_url': 'https://on.ge',
        'splitter': '=',
        'categories': {
            0: {'geo': 'პოლიტიკა',
                'eng': 'politics',
                'url': 'პოლიტიკა',
                'max_pages': None},
            1: {'geo': 'საზოგადოება',
                'eng': 'social',
                'url': 'საზოგადოება',
                'max_pages': 5},
            2: {'geo': 'ეკონომიკა',
                'eng': 'economics',
                'url': 'ეკონომიკა',
                'max_pages': 5},
        },

    }
}

source_template = {
    'name': '',
    'base_url': '',
    'categories': {

    },
}

categories_template = {
    '0': {'geo': '',
          'eng': '',
          'url': '',
          'max_pages': 0},
}
