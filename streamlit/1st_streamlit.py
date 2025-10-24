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
######## 사용자의 검색 조건 선택 구역 ##########
#########################################
with st.sidebar:
    st.title('⚡️ 전국 전기차 충전소 찾기')
    st.subheader('STEP 1 | 지역 선택')
    sido_list = db.get_SD_NM()
    
    ### 지역 선택
    # 첫 번째 선택박스: 도/광역시 선택
    dosi = st.selectbox("도/시를 선택하세요. [가나다순]", sorted(sido_list))
    # 두 번째 선택박스: 시/군/구 선택
    sigungu_list = getl(dosi)
    sigungu = st.selectbox("시/군/구 또는 읍/면/동을 선택하세요. [가나다순]", sigungu_list)
    st.divider()

    ## 시간 및 공영주차장 선택
    # 운영시간 선택
    st.subheader('STEP 2 | 운영 정보 선택')
    st.markdown("###### 선택 취소를 원하시면 버튼을 한 번 더 클릭하세요.")
    st.markdown("**주차장 형태**")
    options = ["24시간 운영", "지정 시간제 운영"]
    selection_time = st.pills(" ", options, selection_mode="single", label_visibility="collapsed")
    # 공영주차장 선택
    st.markdown("**주차장 형태**")
    options = ["공영주차장", "민영주차장"]
    selection_type = st.pills(" ", options, selection_mode="single", label_visibility="collapsed")
    st.markdown("\n")
    st.markdown("\n")
    st.button("검색", on_click=None, disabled=False, use_container_width=True)

########################################
############# SQL select ###############
########################################
def save_sido_key():
    with db.connection.cursor() as cursor:
        sql = "select * from ctprvn_info where CTPRVN_NM = %s"
        cursor.execute(sql, (dosi))
        save_sido_result = cursor.fetchall()
        df = pd.DataFrame(save_sido_result)
        if not save_sido_result:
            print("쿼리 실패")
    return df.iloc[0, 0]

def save_sigungo_key():
    with db.connection.cursor() as cursor:
        sql = "select * from sgg_info where SGG_NM = %s"
        cursor.execute(sql, (sigungu))
        ssk_result= cursor.fetchall()
        df = pd.DataFrame(ssk_result)
        if not ssk_result:
            sql = "select * from emd_info where EMD_CD = %s"
            cursor.execute(sql, (sigungu))
            ssk_result = cursor.fetchall()
            df = pd.DataFrame(ssk_result)
        else:
            print("쿼리 실패")
    return df.loc[0, 0]
 
sido_key = save_sigungo_key()
sigungo_key = save_sigungo_key()

user_selected = [sido_key, sigungo_key, selection_time, selection_type]
with db.connection.cursor() as cursor:
    format_strings = ','.join(['%s'] * len(user_selected))
    sql2 = """select * from charging_stations where
            {format_strings} """
print(sql2)

    # cursor.execute(sql2, user_selected)
    # result2

#########################################
############# 결과값 출력 구역 ##############
#########################################

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
