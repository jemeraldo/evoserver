# evoserver

API:
/api/v1/

Endpoint /api/v1/ip

GET /api/v1/ip
Возвращает IP устройства эвотор, связанного с текущим экраном

Header Parameters:

Screen-Id: string
ID экрана

Responses:
200 OK
{DeviceIP: string}

400
{error: "error: no such binded device"}

POST /api/v1/ip
Задать IP устройства эвотор

Header Parameters:

Json Body:

DeviceID: string
ID устройства эвотор
DeviceIP: string
IP

Responses:
200 OK

400
{error: "error: no such binded device"}

Endpoint /api/v1/apps
Установленные приложения

GET /api/v1/apps
Получить весь список установленных приложений

Responses:
200 OK

Sample response:

{
    "_items": [
        {
            "_created": "Sat, 18 Nov 2017 20:56:57 GMT",
            "_etag": "4c9ac7737dc2d6eeda46d43ca2fdc7d911ce218f",
            "_id": "5a109e9a6c269d098878d2de",
            "_links": {
                "self": {
                    "href": "apps/5a109e9a6c269d098878d2de",
                    "title": "App"
                }
            },
            "_updated": "Sat, 18 Nov 2017 20:56:57 GMT",
            "state": 0,
            "timestamp": "66462461124",
            "userid": "ss-ddd"
        }
    ],
    "_links": {
        "parent": {
            "href": "/",
            "title": "home"
        },
        "self": {
            "href": "apps",
            "title": "apps"
        }
    },
    "_meta": {
        "max_results": 25,
        "page": 1,
        "total": 1
    }
}

GET /api/v1/apps/<user-id>

Responses:
200 OK

{
	state: [0,1] # 0 - приложение установлено, 1 - удалено
	timestamp: string #дата установки/удаления
}

400
{ error: "No such user-id" }

POST /api/v1/apps/event
Событие установки/удаления

Headers:
Authorization: string
Content-Type: string # default "application/json"
Accept: "application/json;charset=UTF-8"
Accept-Charset: "UTF-8"

Body:

id: string
timestamp: string
version: 	apiVersion (enum) #default 2
type: string # ApplicationInstalled, ApplicationUninstalled
data:
	productId: 	appId (string)
	userId: userId (string)

Responses:
200 OK

Sample:
{
  "id": "a99fbf70-6307-4acc-b61c-741ee9eef6c0",
  "timestamp": 1504168645290,
  "version": 2,
  "type": "ApplicationInstalled",
  "data": {
    "productId": "string",
    "userId": "01-000000000000001"
  }
}

Endpoint /api/v1/bind
Bind screen

GET /api/v1/evotor-binded

Headers:
X-Evotor-User-Id: string
X-Evotor-Device-Id: string

Responses:
200 OK
{ binded: [0,1] } # 1 - binded

GET /api/v1/binding

Headers:
X-Evotor-User-Id: string
X-Evotor-Device-Id: string

Responses:
200 OK
{ code: [0-9A-Z]{8} }

POST /api/v1/bind

Headers:
X-Screen-Id: string

Body:
{ code: [0-9A-Z]{8} }

Responses:
200 OK

GET /api/v1/unbind
Delete bind

Headers:
X-Evotor-User-Id: string
X-Evotor-Device-Id: string

Responses:
200 OK