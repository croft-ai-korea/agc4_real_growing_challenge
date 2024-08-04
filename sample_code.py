import requests 

username = "Agrifusion"
password = "78G$dV32La"   

response = requests.post( 
    "https://api.letsgrow.com/token", 
    headers={ 
        "Content-Type": "application/x-www-form-urlencoded", 
        "accept": "application/json", 
    }, 
    data={"username": username, "password": password}, 
).json() 
  
token = response["access_token"] 
print(token)
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
    
print("=========================================================================")
module_id = 68112
# module_id = 14821
# module_id = 14822
response = requests.get(     
"https://api.letsgrow.com/api/ModuleDefinitions/{}/Items".format(module_id), 
    headers={ 
        "Content-Type": "application/x-www-form-urlencoded", 
        "accept": "application/json", 
        "Authorization": "Bearer " + token, 
    }, 
).json() 
  
for collection in response["ModuleItems"]: 
    if collection['IsWriteable'] == False:
        continue
    name = collection['Description'].replace(" ", "")
    name = name.replace("µmol/m²/s", "")
    name = name.replace("W/m²", "")
    name = name.replace("m/s", "")
    name = name.replace("J/cm²", "")
    name = name.replace("(status1=rain,0=dry)", "")
    name = name.replace("", "")  
    name = name.replace(":", "")
    name = name.replace("-", "")
    name = name.replace("%", "")
    name = name.replace("°C","")
    name = name.replace("°", "")
    name = name.replace("g/","")
    name = name.replace("(1=on2=out)","")
    name = name.replace("l/","") 
    name = name.replace("(from3276,8till3276,8)","")
    name = name.replace("(from-3276,8till3276,8)","")
    name = name.replace("/","")
    name = name.replace("#","")
    name = name.replace("m²","")    
    name = name.replace("m³","")  
    id = collection['ColId']
    # print(f"'{name}':{id},") 
    # print(f"'{id}',")
    print(f"'{name}',")  
    
print("=========================================================================")
# collection_id = 2607102
# timestamp =  "2024-07-29T11:10:00"  # 예제 타임스탬프
# value_data = {"TimeStamp": timestamp, "Value": 23.45, "Offset": 0}


# response = requests.put( 
#     "https://api.letsgrow.com/api/ModuleDefinitions/{}/Items/{}/Value".format( module_id, collection_id), 
#     headers={ 
#     "Content-Type": "application/json", 
#     "accept": "application/json", 
#     "Authorization": "Bearer " + token, 
#     },
#     json=value_data
# )  

# print(response.status_code)

value_data = [
  {
    "timeStamp": "2024-07-29T20:00:00",
    "value": 20,
    "offset": 0,
    "colId": 2607102
  },
  {
    "timeStamp": "2024-07-29T20:10:00",
    "value": 20,
    "offset": 0,
    "colId": 2607102
  }
]
response = requests.put( 
    "https://api.letsgrow.com/api/ModuleDefinitions/{}/Values".format( module_id), 
    headers={ 
    "Content-Type": "application/json", 
    "accept": "application/json", 
    "Authorization": "Bearer " + token, 
    },
    json=value_data
)                          
print(response.status_code)
    
    
print("=========================================================================")
collection_id = "2607102"
dateTimeStart = "2024-07-29T00%3A00%3A00"
dateTimeEnd = "2024-07-30T00%3A00%3A00"
response = requests.get(     
"https://api.letsgrow.com/api/ModuleDefinitions/{}/Items/{}/Values?dateTimeStart={}&dateTimeEnd={}".format( 
        module_id, collection_id, dateTimeStart, dateTimeEnd
    ), 
    headers={ 
        "Content-Type": "application/x-www-form-urlencoded", 
        "accept": "application/json", 
        "Authorization": "Bearer " + token, 
    }, 
).json() 
  
for value in response: 
    print(value)