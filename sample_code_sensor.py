import requests 
from typing import List, Dict, Any
from a_util.letsgrow_const import COLID_MAP_NAME, COLID_MAP_NUMBER
from a_util.letsgrow_const import LETGROW_FORCAST, LETSGROW_MOD_COLS_MAP
from a_util.letsgrow_const import GREENHOUSE_MODULE_ID, WEATHER_MODULE_ID, FORCAST_MODULE_ID
from datetime import datetime, timedelta

def get_token(username:str, password:str):
    response = requests.post( 
        "https://api.letsgrow.com/token", 
        headers={ 
            "Content-Type": "application/x-www-form-urlencoded", 
            "accept": "application/json", 
        }, 
        data={"username": username, "password": password}, 
    ).json() 
    
    token = response["access_token"] 
    return token

def get_module_ids(token:str):
    response = requests.get( 
        "https://api.letsgrow.com/api/ModuleDefinitions/", 
        headers={ 
            "Content-Type": "application/x-www-form-urlencoded", 
            "accept": "application/json", 
            "Authorization": "Bearer " + token, 
        }, 
    ).json()
    
    for module in response: 
        print(module)
    
    return response

def get_collectionId(token:str, module_id:str):
    # module_id = "68112"
    # module_id = "14821"
    # module_id = "14822"
    response = requests.get(     
    "https://api.letsgrow.com/api/ModuleDefinitions/{}/Items".format(module_id), 
        headers={ 
            "Content-Type": "application/x-www-form-urlencoded", 
            "accept": "application/json", 
            "Authorization": "Bearer " + token, 
        }, 
    ).json() 
      
    # print("collection id names")
    # for collection in response["ModuleItems"]: 
    #     if collection['IsWriteable'] == False:
    #         continue
    #     name = collection['Description'].replace(" ", "")
    #     name = name.replace("µmol/m²/s", "")
    #     name = name.replace("W/m²", "")
    #     name = name.replace("m/s", "")
    #     name = name.replace("J/cm²", "")
    #     name = name.replace("(status1=rain,0=dry)", "")
    #     name = name.replace("", "")  
    #     name = name.replace(":", "")
    #     name = name.replace("-", "")
    #     name = name.replace("%", "")
    #     name = name.replace("°C","")
    #     name = name.replace("°", "")
    #     name = name.replace("g/","")
    #     name = name.replace("(1=on2=out)","")
    #     name = name.replace("l/","") 
    #     name = name.replace("(from3276,8till3276,8)","")
    #     name = name.replace("(from-3276,8till3276,8)","")
    #     name = name.replace("/","")
    #     name = name.replace("#","")
    #     name = name.replace("m²","")    
    #     name = name.replace("m³","")  
    #     id = collection['ColId']
    #     # print(f"'{name}':{id},") 
    #     # print(f"'{id}',")
    #     print(f"'{name}',")  
    
    return response
        
def put_value(token:str, module_id:str, collection_id:str, value_data:Dict[str,Any]):
    # collection_id = 2607102
    # timestamp =  "2024-07-29T11:10:00"  # 예제 타임스탬프
    # value_data = {"TimeStamp": timestamp, "Value": 23.45, "Offset": 0}
    
    response = requests.put( 
        "https://api.letsgrow.com/api/ModuleDefinitions/{}/Items/{}/Value".format( module_id, collection_id), 
        headers={ 
        "Content-Type": "application/json", 
        "accept": "application/json", 
        "Authorization": "Bearer " + token, 
        },
        json=value_data
    )  

    print(response.status_code)

def put_values(token:str, module_id:str, value_data:List[Dict[str,Any]]):
    # value_data = [
    # {
    #     "timeStamp": "2024-07-29T20:00:00",
    #     "value": 20,
    #     "offset": 0,
    #     "colId": 2607102
    # },
    # {
    #     "timeStamp": "2024-07-29T20:10:00",
    #     "value": 20,
    #     "offset": 0,
    #     "colId": 2607102
    # }
    # ]
    response = requests.put( 
        "https://api.letsgrow.com/api/ModuleDefinitions/{}/Values".format(module_id), 
        headers={ 
        "Content-Type": "application/json", 
        "accept": "application/json", 
        "Authorization": "Bearer " + token, 
        },
        json=value_data
    )                          
    print(response.status_code)
    
def get_data(token:str, module_id:str, collection_id:str, date_time_start:str, date_time_end:str):
    # collection_id = "2607102"
    # date_time_start = "2024-07-29T00%3A00%3A00"
    # date_time_end = "2024-07-30T00%3A00%3A00"
    response = requests.get(     
    "https://api.letsgrow.com/api/ModuleDefinitions/{}/Items/{}/Values?dateTimeStart={}&dateTimeEnd={}".format( 
            module_id, collection_id, date_time_start, date_time_end
        ), 
        headers={ 
            "Content-Type": "application/x-www-form-urlencoded", 
            "accept": "application/json", 
            "Authorization": "Bearer " + token, 
        }, 
    ).json() 
    
    # for value in response: 
    #     print(value)
        
    return response

        
if __name__ == "__main__":
    # ## Access Letsgrow for the autonomous greenhouse control
    # username = "Agrifusion"
    # password = "78G$dV32La"  
    
    ## Access Letsgrow for only write extra sensor data
    # not working now..
    username = "agrifusionsensors"
    password = "Vg5#sLkSa8"  
    
    token = get_token(username=username, password=password)
    
    ## Access Module ID
    moduleID_response = get_module_ids(token=token)    
    print(moduleID_response)
    
    ## Access Collection ID
    moduleId = 69296    
    collectionID_response = get_collectionId(token=token, module_id=moduleId)
    
    for data in collectionID_response['ModuleItems']:
        print(f"ColID : {data['ColId']}  Description : {data['CustomerDescription']}")
    
    ## Write sensor data
    ## use put_value for single value 
    ## use put_values for multiple value
    
    # collectionId = 2664621 # plant biosignals
    
    # ts = datetime(2024,8,2,0,0,0).isoformat()
    # # ts = '2024-08-02T00:00:00'  
    # value_data = {"TimeStamp" : ts, "Value" : 100, "Offset": 0}               
    
    # put_value(token=token, 
    #           module_id=moduleId, 
    #           collection_id=collectionId, 
    #           value_data=value_data)
    
    