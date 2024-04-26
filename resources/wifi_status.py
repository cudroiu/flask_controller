from flask import request
from flask_restful import Resource
from http import HTTPStatus

from models.wifi_status import WifiStatus
from config import ROUTER
import router_utils


class WifiStatusResource(Resource):
    def __init__(self):
        self.router = router_utils.get_router(ROUTER)

    def get(self):
        # get wifi_status
        wifi_status = None
        try:
            wifi_status = self.router.getWifiStatus()
        except Exception as exc:
            print(exc)
        if wifi_status is None:
            return {'message': 'Unable to determine wifi status'}, HTTPStatus.NOT_FOUND
        return {'data': {'wifi_status': wifi_status}}, HTTPStatus.OK
    
    def put(self):
        try:
            data = request.get_json()
        except Exception as exc:
            print(exc.message)
        wifi_status = WifiStatus(wifi_status=data['status'])
        if data['status'] == True:
            self.router.startWifi()
        elif data['status'] == False:
            self.router.stopWifi()
        return {'data': {'wifi_status': wifi_status.wifi_status}}, HTTPStatus.OK