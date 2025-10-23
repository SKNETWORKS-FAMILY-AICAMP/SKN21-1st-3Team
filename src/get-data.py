# ...existing code...
import requests
from dotenv import load_dotenv
import os
import csv
import math
import time
import json

# .env 환경 변수 load
load_dotenv()

base_url = "https://www.safemap.go.kr/openApiService/data"
api_key = os.environ.get("API_KEY")
if not api_key:
    raise SystemExit("API_KEY not found in environment (.env).")

# 한 페이지에 요청할 개수 (API 허용 범위에 맞게 조정)
data_size = 10000
output_csv = os.path.join(os.path.dirname(__file__), "..", "charging_stations.csv")


def extract_items_from_response(resp_json):
    body = resp_json.get("response", {}).get("body", {})
    items = body.get("items")
    if items is None:
        return []
    item = items.get("item") if isinstance(items, dict) else items
    if item is None:
        return []
    if isinstance(item, list):
        return item
    if isinstance(item, dict):
        return [item]
    return []


# 첫 요청으로 totalCount 조회
params = {
    "serviceKey": api_key,
    "numOfRows": data_size,
    "pageNo": 1,
    "dataType": "JSON",
}
first_resp = requests.get(
    f"{base_url}/getChargingStationData1.do", params=params, timeout=30
)
first_resp.raise_for_status()
first_json = first_resp.json()

body = first_json.get("response", {}).get("body", {})
total_count = int(body.get("totalCount", 0) or 0)
if total_count == 0:
    print("No data found.")
    items_all = []
else:
    total_pages = math.ceil(total_count / data_size)
    print(f"Total records: {total_count}, pages: {total_pages} (page size {data_size})")

    items_all = []
    items_all.extend(extract_items_from_response(first_json))

    for page in range(2, total_pages + 1):
        params["pageNo"] = page
        try:
            resp = requests.get(
                f"{base_url}/getChargingStationData1.do", params=params, timeout=30
            )
            resp.raise_for_status()
            resp_json = resp.json()
        except Exception as e:
            print(f"Request failed on page {page}: {e}")
            break
        page_items = extract_items_from_response(resp_json)
        items_all.extend(page_items)
        print(
            f"Fetched page {page}/{total_pages}, items this page: {len(page_items)}, total so far: {len(items_all)}"
        )
        time.sleep(0.2)  # 서버에 부담을 주지 않도록 짧은 대기

# CSV로 저장
if items_all:
    fieldnames = set()
    for it in items_all:
        if isinstance(it, dict):
            fieldnames.update(it.keys())
    fieldnames = sorted(fieldnames)

    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    with open(output_csv, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for it in items_all:
            row = {k: ("" if it.get(k) is None else it.get(k)) for k in fieldnames}
            writer.writerow(row)

    print(f"Saved {len(items_all)} records to {output_csv}")
else:
    print("No records to save.")


# 작성자: 박내은
# 목적: open API를 활용해 전기차 충전소 관련 data를 가져와서 json으로 저장

api_key = os.environ.get("API_KEY")
data_size = 10000
page = 1

all_items = []

while True:
    # api 호출
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

# 모든 API 호출이 끝난 후 임시 변수에 담긴 데이터를 json 파일로 변경 후 저장
with open("src/temp_data_2.json", "w", encoding="utf-8") as file:
    json.dump(all_items, file, indent=4, ensure_ascii=False)
