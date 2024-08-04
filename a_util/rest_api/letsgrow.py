from datetime import datetime, timedelta
import requests
import json
import sys

sys.path.append('./')

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
    
    def get_module_template(self):
        response = requests.get(base_url + "/api/ModuleTemplates", headers=self.headers)
        #print(response)
        rslt = json.loads(response.text)
        print(rslt)
        return rslt

    def get_module_definition(self):
        response = requests.get(base_url + "/api/ModuleDefinitions", headers=self.headers)
        #print(response)
        rslt = json.loads(response.text)
        print(rslt)
        return rslt   
         
    def read_last_val(self, moduleId, colId):
        response = requests.get(base_url + F"/api/ModuleDefinitions/{moduleId}/Items/{colId}/LastValue",
                                headers=self.headers)
        #print(response)
        rslt = json.loads(response.text)
        print(rslt)
        return rslt

    def read_values(self, moduleId, colIds, beginTime, endTime):
        # moduleId = '42984'
        # colId = '1593815'

        col_str = ""
        for value in colIds:
            col_str = col_str + 'colIds= ' + value + '&'
            # moduleNcols['42984']
        response = requests.get(
            base_url + F"/api/ModuleDefinitions/{moduleId}/Values?{col_str}dateTimeStart={beginTime}&dateTimeEnd={endTime}",
            headers=self.headers)
        #print(response)
        rslt = json.loads(response.text)
        print(rslt)
        return rslt

    def read_values_oneday(self, moduleId, colIds, begin_time: datetime):
        begin_date_str: str = begin_time.strftime("%Y-%m-%dT%H:%M:%S")
        endtime_str: str = (begin_time + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S")

        col_str = ""
        for value in colIds:
            col_str = col_str + 'colIds= ' + value + '&'
            # moduleNcols['42984']
        response = requests.get(
            base_url + F"/api/ModuleDefinitions/{moduleId}/Values?{col_str}dateTimeStart={begin_date_str}&dateTimeEnd={endtime_str}",
            headers=self.headers)
        #print(response)
        rslt = json.loads(response.text)
        # print(rslt)
        return rslt

    def read_all_values_oneday(self, moduleId, begin_time: datetime):
        colIds = LETSGROW_MOD_COLS_MAP[moduleId]
        begin_date_str: str = begin_time.strftime("%Y-%m-%dT%H:%M:%S")
        endtime_str: str = (begin_time + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S")

        col_str = ""
        for value in colIds:
            col_str = col_str + 'colIds= ' + value + '&'
            
        response = requests.get(
            base_url + F"/api/ModuleDefinitions/{moduleId}/Values?{col_str}dateTimeStart={begin_date_str}&dateTimeEnd={endtime_str}",
            headers=self.headers)
        # print(response)
        rslt = json.loads(response.text)

        if ('Message' in rslt):
            print(rslt)
            raise "error in response body text Message"


        return rslt

    def read_all_values_onehour(self, moduleId, begin_time: datetime):
        colIds = LETSGROW_MOD_COLS_MAP[moduleId]
        begin_date_str: str = begin_time.strftime("%Y-%m-%dT%H:%M:%S")
        endtime_str: str = (begin_time + timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%S")

        col_str = ""
        for value in colIds:
            col_str = col_str + 'colIds= ' + value + '&'
            
        response = requests.get(
            base_url + F"/api/ModuleDefinitions/{moduleId}/Values?{col_str}dateTimeStart={begin_date_str}&dateTimeEnd={endtime_str}",
            headers=self.headers)
        # print(response)
        rslt = json.loads(response.text)

        if ('Message' in rslt):
            print(rslt)
            raise "error in response body text Message"


        return rslt

    def write_value(self, moduleId, colId, value):
        hdr = {'Authorization': self.headers['Authorization'], 'Content-Type': 'application/json'}
        response = requests.put(base_url + F"/api/ModuleDefinitions/{moduleId}/Items/{colId}/Value", headers=hdr,
                                data=json.dumps(value))
        #print(response)
        rslt = json.loads(response.text)
        print(response)
        #print(rslt)
        return response

    def write_values(self, moduleId, values):
        #print("######",json.dumps(values))
        #with open('./a_util/rest_api/save_control.json','w') as f:
        #    json.dump(values,f)
        hdr = {'Authorization': self.headers['Authorization'], 'Content-Type': 'application/json'}
        response = requests.put(base_url + F"/api/ModuleDefinitions/{moduleId}/Values", headers=hdr,
                                json=values)
        #print(response, response.text)
        print(response)
        # rslt = json.loads(response.text)
        # print(rslt)
        return response
                
if __name__ == "__main__":
    letgrow = LetGrow(
        id = "Agrifusion",
        pwd = "78G$dV32La" 
    )
    
    # letgrow.get_module_template()
    letgrow.get_module_definition()
    
    