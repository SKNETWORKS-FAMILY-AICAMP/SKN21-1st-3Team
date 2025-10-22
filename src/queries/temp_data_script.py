import requests as api
import json

"""
    임시데이터 생성용
"""

res = api.get(
    "https://www.safemap.go.kr/openApiService/data/getChargingStationData1.do?serviceKey=0KEH6JLX-0KEH-0KEH-0KEH-0KEH6JLX28&numOfRows=20&pageNo=1&dataType=JSON",
    timeout=10,
)

formated_res = json.loads(res.text)
body_data = formated_res["response"]["body"]["items"]

for data in body_data:
    print(
        f"values('{data["OBJT_ID"]}','{data["CHGER_ID"]}','{data["STAT_NM"]}','{data["CHGER_TY"]}','{data["USE_TM"]}','{data["ADRES"]}','{data["RN_ADRES"]}','{data["CTPRVN_CD"]}','{data["SGG_CD"]}','{data["EMD_CD"]}','{data["BUSI_NM"]}','{data["TELNO"]}',{data["X"]},{data["Y"]})"
    )
