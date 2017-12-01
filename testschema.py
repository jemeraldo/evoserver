import requests

f = open('test.jpg', 'rb')
image = f.read()

data = {
    'userId': '54-995411292457300',
    'image': image,
}
r = requests.post('http://127.0.0.1:5000/api/v1/slides', data=data)

print(r)

