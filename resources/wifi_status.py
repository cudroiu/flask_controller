from flask import request
from flask_restful import Resource
from http import HTTPStatus

from models.wifi_status import WifiStatus


class WifiStatusResource(Resource):
    def get(self):
        # get wifi_status
        wifi_status = None
        if wifi_status is None:
            return {'message': 'Unable to determine wifi status'}, HTTPStatus.NOT_FOUND
        return {'data': {'wifi_status': wifi_status}}, HTTPStatus.OK
    
    def put(self):
        data = request.get_json()
        # update wifi_status
        wifi_status = WifiStatus(wifi_status=data['status'])
        return {'data': {'wifi_status': wifi_status.wifi_status}}, HTTPStatus.OK