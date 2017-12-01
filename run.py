# coding: utf8

import json, random, os, sys
import settings, tbot
from eve import Eve
from flask import request
from pymongo import MongoClient, errors as mongo_errors
from evotor_settings import *
from evodb import *


app = Eve()
client = MongoClient(settings.MONGO_URI)
db = client[EVODB_NAME]
server_port = os.environ.get('PORT', 5000)

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
    if not request.data and datafields:
        return datafields[0]
    D = json.loads(request.data)
    for df in datafields:
        res = D[df]
        if res is None:
            return df
    return None



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

    try:
        result = add_new_bind(deviceid)
        return json_response({BINDS_CODE: result[BINDS_CODE]}, 200)
    except Exception as e:
        return json_error('Error while adding new bind')


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
        item = set_bind(code, screenid)
    except Exception as e:
        return json_error('error while setting bind: ' + str(e))

    return json_response(
        {
            BINDS_EVOTOR_BINDED: True, BINDS_IP: item[BINDS_IP], BINDS_DEVICEID: item[BINDS_DEVICEID]
        }, 200)

@app.route(ep_evotor_binded['url'], methods=ep_evotor_binded['methods'])
def evotor_binded():
    ch = check_headers(X_EVOTOR_DEVICEID)
    if ch:
        return json_error('No header ' + X_EVOTOR_DEVICEID + ' provided')

    deviceid = request.headers.get(X_EVOTOR_DEVICEID)
    return json_response({BINDS_EVOTOR_BINDED: is_device_binded(deviceid)})


@app.route(ep_screen_binded['url'], methods=ep_screen_binded['methods'])
def screen_binded():
    ch = check_headers(X_SCREENID)
    if ch:
        return json_error('No header ' + X_SCREENID + ' provided')

    screenid = request.headers.get(X_SCREENID)
    return json_response({BINDS_SCREEN_BINDED: is_screen_binded(screenid)})

@app.route(ep_unbind['url'], methods=ep_unbind['methods'])
def unbind():
    ch = check_data(BINDS_CODE)
    if ch is not None:
        return json_error('No field "' + ch + '" provided')
    code = json.loads(request.data)[BINDS_CODE]
    item = db[DB_BINDS].find_one({BINDS_CODE: code})
    if not item:
        return json_error('No such bind in database')
    try:
        unbind_screen(code)
        return json_response({BINDS_SCREEN_BINDED: False})
    except Exception as e:
        return json_error('Error while unbinding')

@app.route(ep_ip['url'], methods=ep_ip['methods'])
def setgetip():
    if request.method == 'POST':
        ch = check_headers(X_EVOTOR_DEVICEID)
        if ch:
            return json_error('No header ' + X_EVOTOR_DEVICEID + ' provided')
        deviceid = request.headers.get(X_EVOTOR_DEVICEID)
        ch = check_data(BINDS_IP)
        if ch:
            return json_error('No field "' + ch + '" provided')
        ip = json.loads(request.data)[BINDS_IP]

        item = db[DB_BINDS].find_one({BINDS_DEVICEID: deviceid})
        if not item:
            return json_error('No such device in database')
        try:
            if set_ip(deviceid, ip):
                return json_response({'status': 'ok'})
        except Exception as e:
            return json_error('error while setting ip')
    if request.method == 'GET':
        ch = check_headers(X_SCREENID)
        if ch:
            return json_error('No header ' + X_SCREENID + ' provided')
        screenid = request.headers.get(X_SCREENID)
        item = db[DB_BINDS].find_one({BINDS_SCREENID: screenid})
        if not item:
            return json_error('No such screen in binds')

        ip = get_ip(screenid)

        if ip:
            return json_response({BINDS_IP: ip}, 200)
        else:
            return json_error('Screen has not binded to any evotor device')

@app.route(ep_feedback['url'], methods=ep_feedback['methods'])
def post_feedback():
    ch = check_headers(X_SCREENID)
    if ch:
        return json_error('No header ' + X_SCREENID + ' provided')
    screenid = request.headers.get(X_SCREENID)

    ch = check_data(CASHIERS_ID, RATES_RATING, TIMESTAMP)
    if ch:
        return json_error('No field "' + ch + '" provided')
    cid = request.headers.get(CASHIERS_ID)
    rating = request.headers.get(RATES_RATING)
    timestamp = request.headers.get(TIMESTAMP)
    cashierName = db[DB_CASHIERS].find_one({CASHIERS_ID: cid})[CASHIERS_NAME]

    try:
        add_feedback(cid, rating, timestamp)
        tuid = get_settings_telegramUserId(cid)
        tbot.send_feedback(tuid, cashierName, rating)
    except Exception:
        print(Exception)
        return json_error('Error while post feedback')

    return json_response({'status': 'ok'})


do_test = True
def run_tests():
    add_new_bind('ev-99122331')
    add_new_bind('ev-00011233')
    add_new_bind('ev-00112234')
    bc2 = db[DB_BINDS].find_one({BINDS_DEVICEID: 'ev-00011233'})[BINDS_CODE]
    bc3 = db[DB_BINDS].find_one({BINDS_DEVICEID: 'ev-00112234'})[BINDS_CODE]
    set_bind(bc2, 'sc-111')
    set_bind(bc3, 'sc-123')
    unbind_screen(bc2)
    set_ip('ev-00112234', '192.168.14.19')
    print('Device ev-99122331 is binded: ', is_device_binded('ev-99122331'))
    print('Device ev-00011233 is binded: ', is_device_binded('ev-00011233'))
    print('Device ev-00112234 is binded: ', is_device_binded('ev-00112234'))
    print('Screen sc-111 is binded: ', is_screen_binded('sc-111'))
    print('Screen sc-123 is binded: ', is_screen_binded('sc-123'))
    print('Screen sc-123 gets evotor ip: ', get_ip('sc-123'))

def init_db():
    binds = db[DB_BINDS]
    indexes = binds.index_information()
    if BINDS_DEVICEID not in indexes:
        binds.create_index(BINDS_DEVICEID, unique=True)

if __name__ == '__main__':
    init_db()
    if do_test:
        run_tests()
    app.run(host='0.0.0.0', port=server_port)
