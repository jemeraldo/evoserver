# coding: utf8

# Headers
X_EVOTOR_USERID = 'X-Evotor-User-Id'
X_EVOTOR_DEVICEID = 'X-Evotor-Device-Id'
X_SCREENID = 'X-Screen-Id'

#DB
EVODB_NAME = 'evodb'

DB_APPS = 'apps'
DB_BINDS = 'binds'
DB_CASHIERS = 'cashiers'
DB_RATES = 'rates'
DB_SETTINGS = 'settings'
DB_RECS = 'recs'
DB_SLIDES = 'slides'

APPS_USERID = 'userId'

BINDS_DEVICEID = 'deviceid'
BINDS_CODE = 'code'
BINDS_SCREENID = 'screenid'
BINDS_IP = 'evotorip'
BINDS_EVOTOR_BINDED = 'evotor-binded'
BINDS_SCREEN_BINDED = 'screen-binded'

CASHIERS_ID = 'cashierId'
CASHIERS_NAME = 'cashierName'

RATES_RATING = 'rating'
TIMESTAMP = 'timestamp'

SETTINGS_TELEGRAMUSERID = 'reportTelegramUserid'

#ENDPOINTS

ep_binding = dict(url='/api/v1/binding', methods=['GET'])
ep_bind = dict(url='/api/v1/bind', methods=['POST'])
ep_evotor_binded = dict(url='/api/v1/evotor-binded', methods=['GET'])
ep_screen_binded = dict(url='/api/v1/screen-binded', methods=['GET'])
ep_unbind = dict(url='/api/v1/unbind', methods=['POST'])

ep_ip = dict(url='/api/v1/ip', methods=['GET', 'POST'])

ep_event = dict(url='/api/v1/install-event', methods=['POST'])

ep_feedback = dict(url='/api/v1/feedback', methods=['POST'])