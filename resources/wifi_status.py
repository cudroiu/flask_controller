from flask import request
from flask_restful import Resource
from http import HTTPStatus

from models.wifi_status import WifiStatus
from validators.validators import validate_wifi_status
from config import ROUTER, CHANGE_USER
import router_utils


class WifiStatusResource(Resource):
    def __init__(self, **kwargs):
        self.router = router_utils.get_router(ROUTER)
        self.log = kwargs.get('logger')

    def get(self):
        # get wifi_status
        wifi_status = None
        try:
            wifi_status = self.router.getWifiStatus()
        except Exception as exc:
            self.log.error(exc)
        if wifi_status is None:
            return {'message': 'Unable to determine wifi status'}, HTTPStatus.NOT_FOUND
        return {'data': {'wifi_status': wifi_status}}, HTTPStatus.OK
    
    def put(self):
        try:
            data = request.get_json()
        except Exception as exc:
            self.log.error(exc)
            return {'errors': f'Unable to parse input json: {exc}'}, HTTPStatus.BAD_REQUEST
        validation_status, messages = validate_wifi_status(data)
        if not validation_status:
            error_message = '\n'.join(messages)
            self.log.error(f"Invalid input json: {error_message}")
            return {'errors': messages}, HTTPStatus.BAD_REQUEST
        wifi_status = WifiStatus()
        wifi_status.status = data['status']
        wifi_status.change_user = CHANGE_USER
        if data['status'] == True:
            result = self.router.startWifi()
            self.log.info(f'Received status code {result} from router when trying to start wifi')
        elif data['status'] == False:
            result = self.router.stopWifi()
            self.log.info(f'Received status code {result} from router when trying to stop wifi')
        try:
            wifi_status.save()
        except Exception as exc:
            self.log.error(f'Unable to save wifi status to DB: {exc}')
        return {'data': {'wifi_status': wifi_status.status}}, HTTPStatus.OK