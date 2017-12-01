# coding: utf8
from evotor_settings import *

MONGO_URI = "mongodb://admin:admin@ds042527.mlab.com:42527/evodb"

# По умолчанию Eve запускает API в режиме "read-only" (т.е. поддерживаются только GET запросы),
# мы включаем поддержку методов POST, PUT, PATCH, DELETE.
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

IF_MATCH = False

URL_PREFIX = 'api'
API_VERSION = 'v1'

Apps = {
    'item_title': 'app',
    'additional_lookup': {
        'url': "regex('[0-9]{2}-[0-9]{15}$')",
        'field': 'userId',
    },
    'resource_methods': ['GET', 'POST', 'DELETE'],
    'schema': {
        'userId': {
            'type': 'string',
            'regex': "^[0-9]{2}-[0-9]{15}$",
            'required': True,
            'unique': True,
        },
        'timestamp': {
            'type': 'string',
            'required': True,
        },
        'installed': {
            'type': 'integer',
            'allowed': [0, 1],
            'default': 0,
            'required': True,
        }
    }
}

Settings = {
    'item_title': 'user-settings',
    'additional_lookup': {
            'url': "regex('[0-9]{2}-[0-9]{15}$')",
            'field': 'userId',
    },
    'resource_methods': ['GET', 'POST'],
    'item_methods': ['GET', 'PATCH', 'DELETE'],
    'schema': {
        'userId': {
            'type': 'string',
            'regex': "^[0-9]{2}-[0-9]{15}$",
            'required': True,
            'unique': True,
        },
        'adType': {
            'type': 'string',
            'allowed': ['text', 'video', 'slideshow'],
            'default': 'text'
        },
        'text': {
            'type': 'string',
            'default': u'Рекламный текст',
        },
        'adVideoUrl': {
            'type': 'string',
            'default': 'https://www.youtube.com/watch?v=sQZKiDIzft8&t=0s',
        },
        'feedbackType': {
            'type': 'string',
            'allowed': ['none', 'smiles', 'stars'],
            'default': 'none'
        },
        'ssDelay': {
            'type': 'integer',
            'default': 10,
        },
        'reportTelegramUserid': {
            'type': 'string',
            'default': ''
        }
    }
}

Recs = {
    'item_title': 'rec',
    'resource_methods': ['GET', 'POST'],
    'item_methods': ['GET', 'PATCH', 'DELETE'],
    'schema': {
        'userId': {
            'type': 'string',
            'regex': "^[0-9]{2}-[0-9]{15}$",
            'required': True,
        },
        'timestart': {
            'type': 'string',
            'default': '00:00'
        },
        'timeend': {
            'type': 'string',
            'default': '00:00'
        },
        'keywords': {
            'type': 'list',
            'schema': {'type': 'string'},
            'default': '[]'
        },
        'kwmethod': {
            'type': 'string',
            'allowed': ['all', 'any'],
            'default': 'any'
        },
        'text': {
            'type': 'string',
            'default': ''
        }
    }
}

testmedias = {
    'resource_methods': ['GET', 'POST'],
    'item_methods': ['GET', 'PATCH', 'DELETE'],
    'schema': {
        'image': {
            'type': 'binary'
        }
    }
}

Slides = {
    'item_title': 'user-slides',
    'additional_lookup': {
            'url': "regex('[0-9]{2}-[0-9]{15}$')",
            'field': 'userId',
    },
    'resource_methods': ['GET', 'POST'],
    'item_methods': ['GET', 'PATCH', 'DELETE'],
    'schema': {
        'userId': {
            'type': 'string',
            'regex': "^[0-9]{2}-[0-9]{15}$",
            'required': True,
            'unique': True
        },
        'image': {
            'type': 'media',
            'required': True
        }
    }
}

DOMAIN = {
    DB_APPS: Apps,
    DB_SETTINGS: Settings,
    DB_RECS: Recs,
    DB_SLIDES: Slides,
    'test-medias': testmedias,
}
