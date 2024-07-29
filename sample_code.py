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
response = requests.get(     
"https://api.letsgrow.com/api/ModuleDefinitions/{}/Items".format(module_id), 
    headers={ 
        "Content-Type": "application/x-www-form-urlencoded", 
        "accept": "application/json", 
        "Authorization": "Bearer " + token, 
    }, 
).json() 
  
for collection in response["ModuleItems"]: 
    print(collection) 
    
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