import streamlit as st
import pandas as pd
import pymysql
import sqlite3
from streamlit_folium import st_folium
from streamlit_folium import folium_static
import folium
from folium.plugins import MarkerCluster
from region_name import get_list as getl
from datetime import datetime
import database as db

#########################################
######## 사용자의 검색 조건 선택 구역 #########
#########################################

st.title('전기차 충전소 찾기')
st.subheader('검색 조건')
st.markdown('지역')
sido_list = db.get_SD_NM()

### 지역 선택
col1, col2 = st.columns(2)
# 첫 번째 선택박스: 도/광역시 선택
with col1:
    dosi = st.selectbox("도/시를 선택하세요.", sorted(sido_list))
# 두 번째 선택박스: 시/군/구 선택
with col2:
    sigungu_list = getl(dosi)
    sigungu = st.selectbox("시/군/구", sigungu_list)
st.divider()

## 시간 및 공영주차장 선택
col3, col4 = st.columns(2)
# 운영시간 선택
with col3:
    st.markdown("운영 시간")
    options = ["24시간 운영", "지정 시간제 운영"]
    selection = st.pills("선택 취소 시 버튼 한 번 더 클릭", options, selection_mode="single")
# 공영주차장 선택
with col4:
    st.markdown("주차장 형태")
    options = ["공영주차장", "민영주차장"]
    selection = st.pills("선택 취소 시 버튼 한 번 더 클릭", options, selection_mode="single")
st.markdown("\n")
st.markdown("\n")
st.button("검색", on_click=None, disabled=False, use_container_width=True)

#########################################
############## SQL select ###############
#########################################
def find_sidogungu_key():
    connection, cursor = rc()
    try:
        with cursor.execute():
    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM your_table WHERE code_col = %s"
            cursor.execute(sql, (code,))
            result = cursor.fetchall()
            df = pd.DataFrame(result)
    finally:
        conn.close()
    return df

#########################################
############# 결과값 출력 구역 ##############
#########################################
# st.subheader('검색 결과')
# st.markdown('지도 보기')
# m = fol.Map(location=[37.58403, 126.96997], zoom_start=20)
# ## 여러개의 지도 마커
# locations = [
#     (37.58403, 126.96997, "신교공영주차장"),
#     (37.58186, 126.97328, "청와대 사랑채 주차장"),
#     (37.57456, 126.97405, "적선동 공영주차장")
# ]
# for lat, lon, name in locations:
#     fol.Marker(
#     [lat,lon],
#     popup=name,
#     icon=fol.Icon(icon='📍')
# ).add_to(m)
# st_fol(m, width=900, height=700)

##### 작성자 : 승룡

# 데이터베이스 연결 함수
# @st.cache_resource 데코레이터를 사용하여 DB 연결을 캐싱합니다.
# 이렇게 하면 앱을 다시 실행할 때마다 연결이 새로 생성되는 것을 방지합니다.


# Streamlit 앱 시작
st.title('SQLite DB 쿼리 결과 출력 앱')

# 데이터베이스 연결
# conn = get_db_connection()
# @st.cache_resource
# def get_db_connection():
#     conn=pymysql.connect(
#         host="192.168.0.37", port=3306, user='project1', password='1111', db='elecar_parking')
#     return conn

# # 데이터 조회 함수
# def get_data_as_dataframe(conn, query):
#     df = pd.read_sql_query(query, conn)
#     return df

# SQL 쿼리 입력
query = "SELECT STAT_NM, ADRES, if(is_24h = 1, 'O', 'X') as '24시간여부', latitude, longitude, COUNT(*) as row_count FROM charging_station WHERE ADRES LIKE '서울특별시_금천구%' GROUP BY STAT_NM, ADRES, is_24h, latitude, longitude;" 



result_df = db.get_data_as_dataframe(query)
if st.button("검색") :

    # 쿼리 결과 출력
    st.subheader("쿼리 결과")

    st.dataframe(result_df, height=1000)

    result_df[["lat","lon"]] = result_df[["latitude","longitude"]]

    m = folium.Map(location=[37.4562557, 126.7052062], zoom_start=13)

    marker_cluster = MarkerCluster().add_to(m)

    for idx, row in result_df.iterrows():
        popup_text = f"<b>{row['STAT_NM']}</b><br>{row['ADRES']}"
        folium.Marker(
            location=[row["lat"], row["lon"]],
            popup=folium.Popup(popup_text, max_width=200)
        ).add_to(marker_cluster)

    folium_static(m)

# 표 데이터 구역
