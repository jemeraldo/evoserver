# coding: utf8
import settings
import random
from pymongo import MongoClient
from evotor_settings import *

client = MongoClient(settings.MONGO_URI)
db = client[EVODB_NAME]

def set_user_telegram_chat_id(tcode, chat_id):
    item = db[DB_SETTINGS].find_one({SETTINGS_TCODE: tcode})
    if not item:
        return None
    res = db[DB_SETTINGS].update_one({SETTINGS_TCODE: tcode}, {'$set': {SETTINGS_TCHATID: chat_id}}, upsert=True)
    return res

def init_settings(userId):
    code = render_code(8)
    while db[DB_SETTINGS].find_one({SETTINGS_TCODE: code}):
        code = render_code(8)

    return db[DB_SETTINGS].insert_one({APPS_USERID: userId, SETTINGS_TCODE: code})

def set_token(userId, token):
    item = db[DB_APPS].find_one({APPS_USERID: userId})
    if item:
        res = db[DB_APPS].update_one({APPS_USERID: userId}, {'$set': {APPS_TOKEN: token}}, upsert=True)
    else:
        db[DB_APPS].insert_one({APPS_USERID: userId, APPS_TOKEN: token})
        res = init_settings(userId)
    return res

def app_install(apid, userId, timestamp, installed):
    apps = db[DB_APPS]
    item = apps.find_one({APPS_USERID: userId})
    if item:
        res = apps.update_one({APPS_USERID: userId}, {'$set': {APPS_INSTALLED: installed, TIMESTAMP: timestamp}})
        return res
    else:
        res = apps.insert_one({APPS_USERID: userId, APPS_INSTALLED: installed, TIMESTAMP: timestamp})
        return res
    return None

def render_code(k=8):
    binds = db[DB_BINDS]
    symbols = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    random.seed()
    code = ''.join(random.choices(symbols, k=k))
    item = binds.find_one({BINDS_CODE: code})
    while item is not None:
        code =''.join(random.choices(symbols, k=k))
        item = binds.find_one({BINDS_CODE: code})
    return code

def add_new_bind(deviceid, userid, ip=''):
    '''Returns inserted or existing item'''
    binds = db[DB_BINDS]
    item = binds.find_one({BINDS_DEVICEID: deviceid})
    if item:
        return item
    else:
        code = render_code()
        result = binds.insert_one({BINDS_DEVICEID: deviceid, BINDS_CODE: code, BINDS_IP: ip, APPS_USERID: userid})
        return result


def set_bind(code, screenid):
    binds = db[DB_BINDS]
    binds.update_one({BINDS_CODE: code}, {'$set': {BINDS_SCREENID: screenid}})
    result = binds.find_one({BINDS_CODE: code})
    return result

def unbind_screen(deviceid):
    binds = db[DB_BINDS]
    res = binds.delete_one({BINDS_DEVICEID: deviceid})
    return binds.find_one({BINDS_DEVICEID: deviceid})

def is_device_binded(deviceid):
    binds = db[DB_BINDS]
    item = binds.find_one({BINDS_DEVICEID: deviceid})
    if item and BINDS_SCREENID in item:
        return bool(item[BINDS_SCREENID])
    else:
        return False


def is_screen_binded(screenid):
    binds = db[DB_BINDS]
    item = binds.find_one({BINDS_SCREENID: screenid})
    return bool(item)

def set_ip(screenid, ip):
    binds = db[DB_BINDS]
    return binds.update_one({BINDS_SCREENID: screenid}, {'$set': {BINDS_IP: ip}}, upsert=True)


def get_ip(deviceid):
    binds = db[DB_BINDS]
    item = binds.find_one({BINDS_DEVICEID: deviceid})
    if item:
        return item[BINDS_IP]
    else:
        return None

def add_feedback(cid, rating, timestamp):
    rates = db[DB_RATES]
    result = rates.insert_one({CASHIERS_ID: cid, RATES_RATING: rating, TIMESTAMP: timestamp})
    return result

def get_settings_telegram_chat_id(userId):
    settings = db[DB_SETTINGS]
    item = settings.find_one({APPS_USERID: userId})
    if item:
        return item[SETTINGS_TCHATID]
    else:
        return None

def get_settings_telegramUserId(cashierId):
    cashiers = db[DB_CASHIERS]
    userid = cashiers.find_one({CASHIERS_ID: cashierId})[APPS_USERID]
    if not userid:
        return None
    settings = db[DB_SETTINGS]
    item = settings.find_one({APPS_USERID: userid})
    if not item:
        return None
    return item[SETTINGS_TELEGRAMUSERID]


