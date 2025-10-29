"""
DB에 저장된 x,y 좌표값을 위도/경도 형태로 변경 후 DB update
"""

import pyproj
import json
from database import cursor

transformer = pyproj.Transformer.from_crs(
    "EPSG:3857",  # Pseudo-Mercator (X, Y 순서)
    "EPSG:4326",  # WGS84 (경도, 위도 순서)
    always_xy=True,  # 항상 (경도/X, 위도/Y) 순서로 입/출력하도록 설정
)

# 모든 ID를 기준으로 update를 하기위해 임시로 저장해뒀던 json 데이터를 가져옴
json_data = open("src/temp_data.json", "r", encoding="utf-8")
data = json.load(json_data)

query = "UPDATE charging_station SET X=%s, Y=%s where OBJT_ID=%s"

for item in data:
    x_position, y_position = transformer.transform(item["X"], item["Y"])
    cursor.execute(query, (f"{x_position:.5f}", f"{y_position:.5f}", item["OBJT_ID"]))
    cursor.connection.commit()


cursor.close()
json_data.close()
