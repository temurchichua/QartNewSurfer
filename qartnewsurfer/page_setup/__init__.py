from string import Template

from sqlalchemy.orm import sessionmaker

from qartnewsurfer.models import Session
from qartnewsurfer.models.onge_model import Category


class SetupTemplate:
    def __init__(self, **source):
        self.__dict__.update(source)


class OnGe(SetupTemplate):
    def __init__(self):
        SetupTemplate.__init__(self, **sources['onge'])

    def get_url(self, category=1, page=1):
        session = Session()
        try:
            category = session.query(Category).get(category)

        except Exception as e:
            print(e)
            raise ValueError("page or/and category is/are out of range")

        else:
            return (f"{self.base_url}"  # base
                    f"/category/{category.url_tag}"  # category
                    f"?page={page}")  # page


sources = {
    "onge": {
        'name': 'onge',
        'base_url': 'https://on.ge',
        'splitter': '=',
        'categories': {
            0: {'geo': 'პოლიტიკა',
                'eng': 'politics',
                'url': 'პოლიტიკა',},
            1: {'geo': 'საზოგადოება',
                'eng': 'social',
                'url': 'საზოგადოება'},
            2: {'geo': 'ეკონომიკა',
                'eng': 'economics',
                'url': 'ეკონომიკა'},
            3: {'geo': 'Sci-Tech',
                'eng': 'science technologies',
                'url': 'sci-tech'},
            4: {'geo': 'კულტურა',
                'eng': 'culture',
                'url': 'კულტურა'},
            5: {'geo': 'ცხოვრების სტილი',
                'eng': 'lifestyle',
                'url': 'ცხოვრება'},
            6: {'geo': 'ტექნოლოგიები',
                'eng': 'technologies',
                'url': 'ტექნოლოგიები'},
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
