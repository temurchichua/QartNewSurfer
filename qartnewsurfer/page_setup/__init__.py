from string import Template


class SetupTemplate:
    def __init__(self, **source):
        self.__dict__.update(source)


class OnGe(SetupTemplate):
    def __init__(self):
        SetupTemplate.__init__(self, **sources['onge'])

    def get_url(self, category, page):
        if category in self.categories and page in range(self.categories[category]['max_pages']):
            return (f"{self.base_url}"                                   # base
                    f"/category/{self.categories[category]['url']}"      # category
                    f"?page={page}")                                     # page
        else:
            raise ValueError("page or/and category is/are out of range")


sources = {
    "onge": {
        'name': 'on.ge',
        'base_url': 'https://on.ge',
        'splitter': '=',
        'categories': {
            0: {'geo': 'პოლიტიკა',
                'eng': 'politics',
                'url': 'პოლიტიკა',
                'max_pages': 5},
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
