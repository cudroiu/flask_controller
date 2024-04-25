import requests
import json
from config import ROUTER


class OwrtException(Exception):
    def __init__(self, message):
        self.message = message

# TODO Implement singleton OwrtRouter class
class OwrtRouter():
    def __init__(self):
        self.ip = ROUTER.get('ip')
        self.user = ROUTER.get('username')
        self.password = ROUTER.get('password')
        self.port = ROUTER.get('port')
        self.base_url = f'http://{self.ip}:{self.port}/cgi-bin/luci/rpc'
        self.req_id = 1
        self.token = None

    def _authenticate(self):
        auth_data = {
            "id": self.req_id,
            "method": "login",
            "params": [
                self.user,
                self.password
                ]
            }
        resp = requests.post(f'{self.base_url}/auth', data=json.dumps(auth_data))
        self.req_id += 1  # TODO increment req_id in a decorator
        self.token = resp.json()['result']
    
    def _request(self, method, url, headers={}, data={}):
        response = getattr(requests, method)(f'{url}?auth={self.token}', headers=headers, data=json.dumps(data))
        if response.status_code == 403:
            self._authenticate()
            response = getattr(requests, method)(f'{url}?auth={self.token}', headers=headers, data=json.dumps(data))
        return response
            
                
    def startWifiStatus(self):
        url = f'{self.base_url}/sys'
        data = { "jsonrpc": "2.0", "id": self.req_id, "method": "exec", "params": ["/scripts/start_wifi.sh"] }
        result = self._request(method='post', url=url, data=data)
        if result.status_code != 200 or 'error' in result.json():
            raise OwrtException(f'Received status code {result.status_code} when trying to start wifi: {result.text}')

    def stopWifiStatus(self):
        url = f'{self.base_url}/sys'
        data = { "jsonrpc": "2.0", "id": self.req_id, "method": "exec", "params": ["/scripts/stop_wifi.sh"] }
        result = self._request(method='post', url=url, data=data)
        self.req_id += 1  # TODO increment req_id in a decorator
        if result.status_code != 200 or 'error' in result.json():
            raise OwrtException(f'Received status code {result.status_code} when trying to stop wifi: {result.text}')

    def getWifiStatus(self):
        url = f'{self.base_url}/sys'
        data = {
            "jsonrpc": "2.0",
            "id": self.req_id,
            "method": "exec",
            "params": ["/sbin/uci show wireless | grep disabled | cut -d '=' -f2"]
        }
        result = self._request(method='post', url=url, data=data)
        self.req_id += 1  # TODO increment req_id in a decorator
        if result.status_code != 200 or 'error' in result.json():
            raise OwrtException(
                f'Received status code {result.status_code} when trying to get wifi status: {result.text}')
        if "\'0\'" in result.json().get('result', ''):
            return True
        elif "\'1\'" in result.json().get('result', ''):
            return False
        else:
            raise OwrtException('Unable to determine wifi status')