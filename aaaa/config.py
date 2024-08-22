from datetime import date

# 재배를 시작한 날자 nthdate 를 결정하는데 필요
crop_begin_date = date(2024, 7, 15)

# letgrow api 호출하는데 필요
config = {
    'letsgrow': {
        'username': 'Agrifusion',
        'password': '78G$dV32La',
        'endpoint': 'https://api.letsgrow.com/',
        'token': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZ3JpZnVzaW9uIiwianRpIjoiMTYzZDFhMzUtMzhlYS00NmIyLTg5MWItYjAyYzVlZjE2ZDkyIiwiaWF0IjoiMDgvMDQvMjAyNCAwNzoxMTo1NiIsImV4cCI6MTcyMjg0MTkxNiwiaXNzIjoiTGV0c0dyb3ciLCJhdWQiOiJMZXRzR3JvdyJ9.SbFQ-OtOtKPrMjgbXGGZVha_tPk2qO5d7OEkPDQr1bo"
    },
    'timescale' : {
        'db':'postgres',
        'username':'postgres',
        'password':'admin1234',
        'host':'localhost',
        'port': 5432
    }
}
