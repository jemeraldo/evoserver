MONGO_URI = "mongodb://admin:admin@ds042527.mlab.com:42527/evodb"

# По умолчанию Eve запускает API в режиме "read-only" (т.е. поддерживаются только GET запросы),
# мы включаем поддержку методов POST, PUT, PATCH, DELETE.
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

DOMAIN = {
    'apps': {
        'schema': {
            'userid': {
                'type': 'string',
                'required': True,
                'unique': True,
            },
            'timestamp': {
                'type': 'string',
                'required': True,
            },
            'state': {
                'type': 'integer',
                'allowed': [0, 1],
                'default': 0,
                'required': True,
            }
        }
    }
}