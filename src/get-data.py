# ...existing code...
import requests
from dotenv import load_dotenv
import os
import csv
import math
import time

# .env 환경 변수 load
load_dotenv()

base_url = "https://www.safemap.go.kr/openApiService/data"
api_key = os.environ.get('API_KEY')
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
first_resp = requests.get(f"{base_url}/getChargingStationData1.do", params=params, timeout=30)
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
            resp = requests.get(f"{base_url}/getChargingStationData1.do", params=params, timeout=30)
            resp.raise_for_status()
            resp_json = resp.json()
        except Exception as e:
            print(f"Request failed on page {page}: {e}")
            break
        page_items = extract_items_from_response(resp_json)
        items_all.extend(page_items)
        print(f"Fetched page {page}/{total_pages}, items this page: {len(page_items)}, total so far: {len(items_all)}")
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