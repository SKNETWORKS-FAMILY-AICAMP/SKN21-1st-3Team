import requests

base_url = "https://www.safemap.go.kr/openApiService/data"
api_key = "0KEH6JLX-0KEH-0KEH-0KEH-0KEH6JLX28"
data_size = 1000
page = 1


response = requests.api.get(
    f"{base_url}/getChargingStationData1.do?serviceKey={api_key}&numOfRows={data_size}&pageNo={page}&dataType=JSON",
    timeout=30,
)

data = response.json()
print(data)
