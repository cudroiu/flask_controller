from flask import Flask
from flask_restful import Api

from resources.wifi_status import WifiStatusResource


app = Flask(__name__)
api = Api(app)
api.add_resource(WifiStatusResource, '/wifi')

if __name__ == '__main__':
    app.run(port=5000, debug = True)