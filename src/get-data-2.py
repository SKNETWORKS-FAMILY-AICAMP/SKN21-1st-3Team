import requests
from dotenv import load_dotenv
import os


# .env 환경 변수 load
load_dotenv()

data_size = (1000,)
page = 1
base_url = "https://www.safemap.go.kr/openApiService/data"
api_key = os.environ.get("API_KEY")
params = {
    "serviceKey": api_key,
    "numOfRows": data_size,
    "pageNo": page,
    "dataType": "JSON",
}


# 1. requests를 사용해서 data를 받아오기 받아온 데이터 print하기.

import requests
from dotenv import load_dotenv
import os


# .env 환경 변수 load
load_dotenv()

data_size = (1000,)
page = 1
base_url = "https://www.safemap.go.kr/openApiService/data"
api_key = os.environ.get("API_KEY")
params = {
    "serviceKey": api_key,
    "numOfRows": data_size,
    "pageNo": page,
    "dataType": "JSON",
}


# 1. requests를 사용해서 data를 받아오기 받아온 데이터 print하기.
import os
import requests
from dotenv import load_dotenv


load_dotenv()
API_KEY = os.environ.get("API_KEY")
if not API_KEY:
    raise SystemExit("API_KEY not found in environment (.env).")


base_url = "https://www.safemap.go.kr/openApiService/data/getChargingStationData1.do"
params = {
    "serviceKey": API_KEY,
    "pageNo": 1,
    "numOfRows": 5,   
    "dataType": "JSON"
}


resp = requests.get(base_url, params=params, timeout=30)
print(resp.text)

import os
import requests
import csv
from dotenv import load_dotenv


load_dotenv()
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise SystemExit(".env 파일에 API_KEY=값 을 넣어주세요")


url = "https://www.safemap.go.kr/openApiService/data/getChargingStationData1.do"
params = {
    "serviceKey": API_KEY,
    "pageNo": 1,
    "numOfRows": 5,
    "dataType": "JSON"
}

resp = requests.get(url, params=params, timeout=30)  
print("요청 상태코드:", resp.status_code)


data = resp.json()
items = data.get("response", {}).get("body", {}).get("items", [])
if not items:
    print("데이터가 없습니다.")
    print(data)
    raise SystemExit()


with open("charging_stations.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=list(items[0].keys()))
    writer.writeheader()
    writer.writerows(items)

print("CSV 저장 완료: charging_stations.csv")

import pymysql

conn = pymysql.connect(
    host='192.168.0.37',
    user='project1',
    password='1111',
    db='elecar_parking',
    charset='utf8mb4'
)
cur = conn.cursor()

cur.execute("SELECT * FROM charging_station, ctprvn_info LIMIT 10;")
rows = cur.fetchall()
for row in rows:
    print(row)

conn.close()

import pymysql


conn = pymysql.connect(
    host='192.168.0.37',
    port=3306,
    user='project1',
    password='1111',
    db='elecar_parking',
    charset='utf8mb4'
)

cur = conn.cursor()


query = """
SELECT 
    STAT_NM,
    ADRES,
    IF(is_24h = 1, 'O', 'X') AS '24시간여부',
    latitude,
    longitude,
    COUNT(*) AS row_count
FROM charging_station
WHERE ADRES LIKE '서울특별시 금천구%'
GROUP BY STAT_NM, ADRES, is_24h, latitude, longitude;
"""

cur.execute(query)

rows = cur.fetchall()

print("=== 🔌 서울특별시 금천구 전기차 충전소 목록 ===")
print(f"총 {len(rows)}개의 충전소를 불러왔습니다.\n")

for row in rows:
    stat_nm, adres, is_24h, lat, lon, count = row
    print(f"충전소명: {stat_nm}")
    print(f"주소: {adres}")
    print(f"24시간 여부: {is_24h}")
    print(f"위도/경도: {lat}, {lon}")
    print(f"등록 충전기 수: {count}")
    print("-" * 50)

conn.close()

import pymysql

conn = pymysql.connect(
    host='192.168.0.37',
    port=3306,
    user='project1',
    password='1111',
    db='elecar_parking',
    charset='utf8mb4'
)

cur = conn.cursor()

query = """
SELECT 
    STAT_NM,
    ADRES,
    IF(is_24h = 1, 'O', 'X') AS '24시간여부',
    latitude,
    longitude,
    COUNT(*) AS row_count
FROM charging_station
WHERE ADRES LIKE '서울특별시%'
GROUP BY STAT_NM, ADRES, is_24h, latitude, longitude;
"""

cur.execute(query)
rows = cur.fetchall()

print("=== 서울특별시 전기차 충전소 목록 ===")
print(f"총 {len(rows)}개 충전소 데이터\n")

for row in rows:
    stat_nm, adres, is_24h, lat, lon, count = row
    print(f"충전소명: {stat_nm}")
    print(f"주소: {adres}")
    print(f"24시간 여부: {is_24h}")
    print(f"위도/경도: {lat}, {lon}")
    print(f"등록 충전기 수: {count}")
    print("-" * 60)

conn.close()
