from datetime import datetime, timedelta
import requests
import json

from a_util.letsgrow_const import COLID_MAP_NAME,COLID_MAP_NUMBER,LETSGROW_MOD_COLS_MAP

base_url = 'https://api.letsgrow.com'

class LetGrow:
    token = None
    headers = {
        'Accept': 'application/json, text/plain, */*',
    }
    
    def _get_token(self):
        payload = {
            'grant_type': 'password',
            'username': self.id,
            'password': self.pwd
        }

        response = requests.post(base_url + "/Token", headers=self.headers, data=payload)
        print(response.text)
        rslt = json.loads(response.text)
        LetGrow.token = rslt['access_token']
        self.headers['Authorization'] = 'Bearer ' + LetGrow.token
    
    def __init__(self, id, pwd, token=None):
        self.id = id
        self.pwd = pwd
        LetGrow.token = token

        self.headers['Authorization'] = 'Bearer ' + str(LetGrow.token)

        if token == None:
            self._get_token()