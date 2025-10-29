"""
open API를 활용해 전기차 충전소 관련 data를 가져와서 json으로 저장
"""

import os
import json
import requests

base_url = "https://www.safemap.go.kr/openApiService/data"
api_key = os.environ.get("API_KEY")
data_size = 10000
page = 1

all_items = []

while True:
    # api 호출
    try:
        response = requests.api.get(
            f"{base_url}/getChargingStationData1.do?serviceKey={api_key}&numOfRows={data_size}&pageNo={page}&dataType=JSON",
            timeout=30,
        )

        # api response
        converted_response = response.json()
        response = converted_response["response"]

        # 마지막 페이지를 넘어간 경우 반복문 종료
        if "body" not in converted_response["response"]:
            break

        # api response의 실제 데이터 추출
        data_body = converted_response["response"]["body"]
        data = data_body["items"]
        total_count = data_body["totalCount"]

        # 추출한 데이터를 임시 변수에 저장
        all_items += data

        # 다음 불러올 데이터가 없으면 반복문 종료
        if total_count <= len(all_items):
            break

        # 다음 반복문을 위해 다음 페이지로 변경
        page += 1

        # 진행상황 확인을 위해 현재 호출한 page print
        print(page)

    except Exception:
        print("api error", Exception.__str__)


# 모든 API 호출이 끝난 후 임시 변수에 담긴 데이터를 json 파일로 변경 후 저장
with open("src/version_neeun/temp_data.json", "w", encoding="utf-8") as file:
    json.dump(all_items, file, indent=4, ensure_ascii=False)
