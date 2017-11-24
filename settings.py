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

DOMAIN = {
    'apps': Apps,
}