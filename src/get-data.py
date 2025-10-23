import requests
from dotenv import load_dotenv
import os

# .env 환경 변수 load

load_dotenv()

base_url = "https://www.safemap.go.kr/openApiService/data"
api_key = os.environ.get('API_KEY')
data_size = 1000
page = 1

response = requests.api.get(
    f"{base_url}/getChargingStationData1.do?serviceKey={api_key}&numOfRows={data_size}&pageNo={page}&dataType=JSON",
    timeout=30,
)

data = response.json()
print(data)
