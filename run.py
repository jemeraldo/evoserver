from eve import Eve
import os

app = Eve()


@app.route('/api/v1/')
def hello_api():
    return "Hello, I'm EvoServer API"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000))
