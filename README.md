# evoserver

# API:
/api/v1/

## Endpoint /api/v1/ip

### GET /api/v1/ip
Возвращает IP устройства эвотор, связанного с текущим экраном

#### Header Parameters:

X-Screen-Id: string
ID экрана

#### Responses:
200 OK
{evotorip: string}

400
{error: string}

### POST /api/v1/ip
Задать IP устройства эвотор

#### Header Parameters:
X-Evotor-Device-Id: string

#### Json Body:

evotorip: string
IP

#### Responses:
200 OK

{'status': 'ok'}

400
{error: "error: no such binded device"}

## Endpoint /api/v1/apps
Установленные приложения

### GET /api/v1/apps
Получить весь список установленных приложений

#### Responses:
200 OK

#### Sample response:


### GET /api/v1/apps/user-id

#### Responses:
200 OK


#### Response sample:
```
{
    "_created": "Tue, 21 Nov 2017 12:49:45 GMT",
    "_etag": "9756c47aea8169dfb6229523ec31bd0b101c7ba3",
    "_id": "5a1420e96c269d21ecb66168",
    "_links": {
        "collection": {
            "href": "apps",
            "title": "apps"
        },
        "parent": {
            "href": "/",
            "title": "home"
        },
        "self": {
            "href": "apps/5a1420e96c269d21ecb66168",
            "title": "app"
        }
    },
    "_updated": "Tue, 21 Nov 2017 12:49:45 GMT",
    "installed": 1,
    "timestamp": "11775133513",
    "userId": "54-995411292457300"
}
```

400
{ error: "No such user-id" }

### POST /api/v1/install-event
Событие установки/удаления

#### Headers:
Authorization: string

Content-Type: string # default "application/json"

Accept: "application/json;charset=UTF-8"

Accept-Charset: "UTF-8"


#### Body:

id: string
timestamp: string
version: 	apiVersion (enum) #default 2
type: string # ApplicationInstalled, ApplicationUninstalled
data:
	productId: 	appId (string)
	userId: userId (string)

#### Responses:
200 OK

#### Request sample:
```
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
```

## Endpoints /api/v1/binding /api/v1/bind /api/v1/evotor-binded /api/v1/screen-binded /api/v1/unbind
Bind screen

### GET /api/v1/evotor-binded

#### Headers:
X-Evotor-Device-Id: string

#### Responses:
200 OK

{ evotor-binded: boolean}

### GET /api/v1/screen-binded
Is screen binded?

#### Headers:
X-Screen-Id: string

#### Responses:
200 OK

{ screen-binded: boolean}

### GET /api/v1/binding
Initiate binding, get code

#### Headers:
X-Evotor-User-Id: string
X-Evotor-Device-Id: string

#### Responses:
200 OK
{ code: [0-9A-Z]{8} }

### POST /api/v1/bind
Bind screen

#### Headers:
X-Screen-Id: string

#### Body:
{ code: [0-9A-Z]{8} }

#### Responses:
200 OK

{ evotor-binded: boolean, evotorip: string, deviceid: string }

### POST /api/v1/unbind
Delete bind

#### Headers:

#### Body:
{ code: [0-9A-Z]{8} }

#### Responses:
200 OK

{screen-binded: boolean }