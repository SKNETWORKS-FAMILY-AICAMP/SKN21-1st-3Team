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
