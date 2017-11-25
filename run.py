import json, random, os, sys
from eve import Eve
from flask import request
import settings
from pymongo import MongoClient, errors as mongo_errors
from evotor_settings import *


app = Eve()
client = MongoClient(settings.MONGO_URI)
db = client[EVODB_NAME]
server_port = os.environ.get('PORT', 5000)


def add_new_bind(code, deviceid, ip=''):
    binds = db[DB_BINDS]
    result = binds.insert_one({BINDS_DEVICEID: deviceid, BINDS_CODE: code, BINDS_IP: ip})
    return result

def set_bind(code, screenid):
    binds = db[DB_BINDS]
    binds.update_one({BINDS_CODE: code}, {'$set': {BINDS_SCREENID: screenid}}, upsert=False)
    result = binds.find_one({BINDS_CODE: code})
    if result[BINDS_IP] is not None:
        return result[BINDS_IP]
    else:
        return 'None'

def json_response(body, status=200, **headers):
    s = json.dumps(body)
    resp = app.make_response((s, status, headers))

    resp.headers.set("Content-Type", "Application/json")
    return resp

def json_error(text, status=400, **headers):
    return json_response({'error': text}, status, **headers)

def check_headers(*headers):
    for h in headers:
        res = request.headers.get(h)
        if res is None:
            return h
    return None

def check_data(*datafields):
    D = json.loads(request.data)
    for df in datafields:
        res = D[df]
        if res is None:
            return df
    return None

def render_code():
    binds = db[DB_BINDS]
    symbols = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    random.seed()
    code = ''.join(random.choices(symbols, k=8))
    item = binds.find_one({BINDS_CODE: code})
    while item is not None:
        code =''.join(random.choices(symbols, k=8))
        item = binds.find_one({BINDS_CODE: code})
    return code

@app.route(ep_binding['url'], methods=ep_binding['methods'])
def initiate_binding():
    ch = check_headers(X_EVOTOR_DEVICEID, X_EVOTOR_USERID)
    if ch is not None:
        return json_error('No header ' + ch + ' provided')

    userid = request.headers.get(X_EVOTOR_USERID)
    deviceid = request.headers.get(X_EVOTOR_DEVICEID)

    apps = db[DB_APPS]
    item = apps.find_one({APPS_USERID: userid})
    if item is None:
        return json_error('No such userid in db')

    binds = db[DB_BINDS]
    item = binds.find_one({BINDS_DEVICEID: deviceid})
    if item is not None:
        return json_response({BINDS_CODE: item[BINDS_CODE]}, 200)
    else:
        code = render_code()
        add_new_bind(code, deviceid)
        return json_response({BINDS_CODE: code}, 200)


@app.route(ep_bind['url'], methods=ep_bind['methods'])
def bind_screen():
    ch = check_headers(X_SCREENID)
    if ch is not None:
        return json_error('No header ' + ch + ' provided')
    ch = check_data(BINDS_CODE)
    if ch is not None:
        return json_error('No field "' + ch + '" provided')

    code = json.loads(request.data)[BINDS_CODE]
    screenid = request.headers.get(X_SCREENID)

    binds = db[DB_BINDS]
    item = binds.find_one({BINDS_CODE: code})
    if item is None:
        return json_error('Wrong code')

    try:
        ip = set_bind(code, screenid)
    except Exception as e:
        return json_error('error while setting bind: ' + str(e))

    return json_response({BINDS_BINDED: True, BINDS_IP: ip}, 200)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=server_port)
