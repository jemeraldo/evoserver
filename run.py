from eve import Eve
import os

app = Eve()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = os.environ.get('PORT', 5000))
