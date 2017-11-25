# Headers
X_EVOTOR_USERID = 'X-Evotor-User-Id'
X_EVOTOR_DEVICEID = 'X-Evotor-Device-Id'
X_SCREENID = 'X-Screen-Id'

#DB

EVODB_NAME = 'evodb'
DB_APPS = 'apps'
APPS_USERID = 'userId'
DB_BINDS = 'binds'
BINDS_DEVICEID = 'deviceid'
BINDS_CODE = 'code'
BINDS_SCREENID = 'screenid'
BINDS_IP = 'evotorip'
BINDS_BINDED = 'binded'

#ENDPOINTS

ep_binding = dict(url='/api/v1/binding', methods=['GET'])
ep_bind = dict(url='/api/v1/bind', methods=['POST'])
ep_evotor_binded = dict(url='/api/v1/evotor-binded', methods=['GET'])
ep_unbind = dict(url='/api/v1/unbind', methods=['GET'])

ep_ip = dict(url='/api/v1/ip', methods=['GET', 'POST'])

ep_event = dict(url='/api/v1/install-event', methods=['POST'])
