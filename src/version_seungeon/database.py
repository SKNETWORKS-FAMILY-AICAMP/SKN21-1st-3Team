import pymysql as sql
from dotenv import load_dotenv
import os
import pandas as pd
import streamlit as st

# .env 환경 변수 load
load_dotenv()

# 환경 변수 설정
db_host = os.environ.get("DB_HOST")
db_user = os.environ.get("DB_USER")
db_password = os.environ.get("DB_PASSWORD") or ""
db_name = os.environ.get("DB_NAME")
db_port = int(os.environ.get("DB_PORT") or 0)

# sql 서버 연동 모듈
connection = sql.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    port=db_port,
    db=db_name,
)

cursor = connection.cursor()

def get_SD_NM():
    get_sql = "SELECT CTPRVN_NM FROM ctprvn_info"
    try:
        cursor.execute(get_sql)
        rows = cursor.fetchall()
        return [row[0] for row in rows]
    except Exception as e:
        # 간단한 오류 처리: 필요하면 로깅이나 예외 재발생으로 변경하세요.
        print(f"DB error in get_SD_NM: {e}")
        return []
def get_SGG_NM():
    pass


@st.cache_data(show_spinner="충전소 데이터 조회 중...")
def get_charging_stations_by_sigungu(dosi, sigungu, selection_time, selection_park):
    """
    선택된 시군구의 코드를 기반으로 충전소 데이터를 조회하고,
    선택된 운영 시간 및 주차장 형태 조건을 적용하여 DataFrame으로 반환합니다.
    """
    
    # 1. 시군구 이름(sigungu)을 이용해 시군구 코드(SGG_CD)를 가져오는 쿼리
    sgg_code_query = f"SELECT SGG_CD FROM sgg_info WHERE SGG_NM = '{sigungu}'LIMIT 1"

    try:
        cursor.execute(sgg_code_query)
        sgg_code_result = cursor.fetchone()
        
        if not sgg_code_result:
            print(f"SGG_NM: '{sigungu}'에 해당하는 SGG_CD를 찾을 수 없습니다.")
            return pd.DataFrame() # 코드를 찾지 못하면 빈 DataFrame 반환
            
        sgg_cd = sgg_code_result[0]
        
    except Exception as e:
        print(f"SGG_CD 조회 중 DB 오류 발생: {e}")
        return pd.DataFrame()

    SD_code_query = f"SELECT CTPRVN_CD FROM ctprvn_info WHERE CTPRVN_NM = '{dosi}'LIMIT 1"
    
    try:
        cursor.execute(SD_code_query)
        SD_code_result = cursor.fetchone()
        
        if not SD_code_result:
            print(f"CTRVN_CD: '{dosi}'에 해당하는 CTRVN_CD를 찾을 수 없습니다.")
            return pd.DataFrame() # 코드를 찾지 못하면 빈 DataFrame 반환
            
        sd_cd = SD_code_result[0]
        
    except Exception as e:
        print(f"SD_CD 조회 중 DB 오류 발생: {e}")
        return pd.DataFrame()  
    # 2. 충전소 검색 조건 동적 생성
    
    time_condition = ""
    if selection_time == "24시간 운영":
        time_condition = "AND is_24h = 1"
    elif selection_time == "지정 시간제 운영":
        time_condition = "AND is_24h = 0"

    park_condition = ""
    if selection_park == "공영주차장":
        park_condition = "AND is_public = 1"
    elif selection_park == "민영주차장":
        park_condition = "AND is_public = 0"


    # 3. 최종 충전소 데이터 조회 쿼리 생성
    # SGG_CD를 기준으로 필터링하고, 집계하여 표시합니다.
    final_query = f"""
    SELECT 
        STAT_NM, ADRES, 
        if(is_24h = 1, 'O', 'X') as '24시간여부', 
        latitude, longitude, 
        COUNT(*) as '충전기_수' 
    FROM 
        charging_station 
    WHERE 
        SGG_CD = '{sgg_cd}' 
        AND CTPRVN_CD = '{sd_cd}'
        {time_condition} 
        {park_condition}
    GROUP BY 
        STAT_NM, ADRES, is_24h, latitude, longitude
    """

    # 4. 데이터 조회 및 반환
    try:
        result_df = get_data_as_dataframe(final_query)
        return result_df
    except Exception as e:
        print(f"충전소 데이터 조회 중 DB 오류 발생: {e}")
        return pd.DataFrame()

# @st.cache_resource
# def get_db_connection():
#     conn=pymysql.connect(
#         host="192.168.0.37", port=3306, user='project1', password='1111', db='elecar_parking')
#     return conn

# 데이터 조회 함수
def get_data_as_dataframe(query):
    df = pd.read_sql_query(query, connection)
    return df
    
# if __name__ == "__main__":
#     print(get_SD_NM())