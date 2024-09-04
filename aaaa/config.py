import os
from datetime import date

# 재배를 시작한 날자 nthdate 를 결정하는데 필요
crop_begin_date = date(2024, 7, 15)

# timescale db 접속 정보
timescale_db = os.getenv('timescale_db', 'postgres')
timescale_user = os.getenv('timescale_user', 'postgres')
timescale_password = os.getenv('timescale_password', 'admin1234')
timescale_host = os.getenv('timescale_host', 'timescaledb')
# timescale_host = os.getenv('timescale_host', '127.0.0.1')
timescale_port = os.getenv('timescale_port', 5432)


# lets grow api 호출하는데 필요한 정보
letsgrow_username = os.getenv('letsgrow_username', 'Agrifusion')
# letsgrow_password = os.getenv('letsgrow_password', '78G$dV32La')
letsgrow_password =  '78G$dV32La'
letsgrow_endpoint = os.getenv('letsgrow_endpoint', 'https://api.letsgrow.com/')
letsgrow_token = os.getenv('letsgrow_token', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZ3JpZnVzaW9uIiwianRpIjoiMTYzZDFhMzUtMzhlYS00NmIyLTg5MWItYjAyYzVlZjE2ZDkyIiwiaWF0IjoiMDgvMDQvMjAyNCAwNzoxMTo1NiIsImV4cCI6MTcyMjg0MTkxNiwiaXNzIjoiTGV0c0dyb3ciLCJhdWQiOiJMZXRzR3JvdyJ9.SbFQ-OtOtKPrMjgbXGGZVha_tPk2qO5d7OEkPDQr1bo')


# letgrow api 호출하는데 필요
config = {
    'letsgrow': {
        'username': letsgrow_username,
        'password':  letsgrow_password,
        'endpoint': letsgrow_endpoint,
        'token': letsgrow_token
    },
    'timescale' : {
        'db':timescale_db,
        'username': timescale_user,
        'password': timescale_password,
        'host': timescale_host,
        'port': timescale_port
    }
}
