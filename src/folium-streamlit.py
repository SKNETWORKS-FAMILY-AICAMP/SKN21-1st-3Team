import streamlit as st
import pandas as pd
import sqlite3
import pymysql
from streamlit_folium import folium_static
import folium
from folium.plugins import MarkerCluster
from datetime import datetime

# 데이터베이스 연결 함수
# @st.cache_resource 데코레이터를 사용하여 DB 연결을 캐싱합니다.
# 이렇게 하면 앱을 다시 실행할 때마다 연결이 새로 생성되는 것을 방지합니다.
@st.cache_resource
def get_db_connection():
    conn = pymysql.connect(
        host="192.168.0.37", port=3306, user='project1', password='1111', db='elecar_parking')
    return conn

# 데이터 조회 함수
def get_data_as_dataframe(conn, query):
    df = pd.read_sql_query(query, conn)
    return df

# Streamlit 앱 시작
st.title('SQLite DB 쿼리 결과 출력 앱')

# 데이터베이스 연결
conn = get_db_connection()

# SQL 쿼리 입력
query = "SELECT STAT_NM, ADRES, if(is_24h = 1, 'O', 'X') as '24시간여부', latitude, longitude, COUNT(*) as row_count FROM charging_station WHERE ADRES LIKE '서울특별시_금천구%' GROUP BY STAT_NM, ADRES, is_24h, latitude, longitude;" 

result_df = get_data_as_dataframe(conn, query)

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