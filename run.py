import json, random, os
from eve import Eve
from flask import request
import settings
from pymongo import MongoClient
from evotor_settings import *


app = Eve()
client = MongoClient(settings.MONGO_URI)
db = client[EVODB_NAME]
server_port = os.environ.get('PORT', 5000)


def add_new_bind(code, deviceid):
    binds = db[DB_BINDS]
    result = binds.insert_one({'deviceid': deviceid, 'code': code})
    return result

def json_response(body, status, **headers):
    s = json.dumps(body)
    resp = app.make_response(s, status, headers)
    resp.headers.set("Content-Type", "Application/json")
    return resp

def json_error(text, status, **headers):
    return json_response({'error': text}, status, headers)

def check_headers(*headers):
    for h in headers:
        res = request.headers.get(h)
        if res is None:
            return h
    return None

def render_code(binds):
    symbols = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    random.seed()
    code = ''.join(random.choices(symbols, k=8))
    item = binds.find_one({'code': code})
    while item is not None:
        code =''.join(random.choices(symbols, k=8))
        item = binds.find_one({'code': code})
    return code

@app.route('/api/v1/binding')
def initiate_binding():
    ch = check_headers(X_EVOTOR_DEVICEID, X_EVOTOR_USERID)
    if ch is not None:
        return json_error('No header ' + ch + ' provided', 400)

    userid = request.headers.get(X_EVOTOR_USERID)
    deviceid = request.headers.get(X_EVOTOR_DEVICEID)

    apps = db[DB_APPS]
    item = apps.find_one({'userId': userid})
    if item is None:
        return json_error('No such userid in db', 400)

    binds = db[DB_BINDS]
    item = binds.find_one({'deviceId': deviceid})
    if item is not None:
        return json_response({'code': item['code']}, 200)
    else:
        code = render_code()
        add_new_bind(code, deviceid)
        return json_response({'code': code}, 200)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=server_port)
