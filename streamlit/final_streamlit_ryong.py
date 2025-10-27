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

# 쿼리 결과 출력
def search_result():
    #########################################
    ############# 결과값 출력 구역 ##############
    #########################################

    ##### 작성자 : 승룡
    # 첫 가운데 좌표 쿼리
    query_1st_geo = "SELECT avg(latitude) '1st_latitude' , avg(longitude) '1st_longtitude' FROM charging_station WHERE ADRES LIKE ('" + dosi + "_" + sigungu + "%') GROUP BY CTPRVN_CD;"
    result_df_geo = db.get_data_as_dataframe(query_1st_geo)
    first_latitude = result_df_geo.iloc[0][0]
    first_longtitude = result_df_geo.iloc[0][1]

    # 제목
    st.subheader("쿼리 결과")

    # 버튼 선택별 쿼리 분기
    # selection_optime : 24시간 운영, 지정 시간제 운영. is_24h : 1, 0
    # selection_park_type : 공영주차장, 민영주차장. is_public : 1, 0
    # 1. 선택 사항을 아무것도 클릭 안했을 때
    if (selection_time == None) and (selection_type == None):
        query = "SELECT STAT_NM '주차장명', ADRES '주소', if(is_24h = 1, 'O', 'X') as '24시간여부', if(is_public = 1, 'O', 'X') as '공영주차장여부', latitude '위도', longitude '경도', COUNT(*) '충전기수' FROM charging_station WHERE ADRES LIKE ('" + dosi + "_" + sigungu + "%') GROUP BY STAT_NM, ADRES, is_24h, is_public, latitude, longitude;"
    # 2. 공영주차장만 클릭했을 때.(is_public이 1일 때). is_public = 1
    elif (selection_time == None) and (selection_type == '공영주차장'):
        query = "SELECT STAT_NM '주차장명', ADRES '주소', if(is_24h = 1, 'O', 'X') as '24시간여부', if(is_public = 1, 'O', 'X') as '공영주차장여부', latitude '위도', longitude '경도', COUNT(*) '충전기수' FROM charging_station WHERE is_public = 1 and ADRES LIKE ('" + dosi + "_" + sigungu + "%') GROUP BY STAT_NM, ADRES, is_24h, is_public, latitude, longitude;"
    # 3. 민영주차장만 클릭했을 때.(is_public이 0일 때). is_public = 0
    elif (selection_time == None) and (selection_type == '민영주차장'):
        query = "SELECT STAT_NM '주차장명', ADRES '주소', if(is_24h = 1, 'O', 'X') as '24시간여부', if(is_public = 1, 'O', 'X') as '공영주차장여부', latitude '위도', longitude '경도', COUNT(*) '충전기수' FROM charging_station WHERE is_public = 0 and ADRES LIKE ('" + dosi + "_" + sigungu + "%') GROUP BY STAT_NM, ADRES, is_24h, is_public, latitude, longitude;"
    # 4. 24시간 운영만 눌렀을 때.   is_24h = 1
    elif (selection_time == '24시간 운영') and (selection_type == None):
        query = "SELECT STAT_NM '주차장명', ADRES '주소', if(is_24h = 1, 'O', 'X') as '24시간여부', if(is_public = 1, 'O', 'X') as '공영주차장여부', latitude '위도', longitude '경도', COUNT(*) '충전기수' FROM charging_station WHERE is_24h = 1 and ADRES LIKE ('" + dosi + "_" + sigungu + "%') GROUP BY STAT_NM, ADRES, is_24h, is_public, latitude, longitude;"
    # 5. 24시간 운영이고 공영주차장일 때. is_public = 1 and is_24h = 1
    elif (selection_time == '24시간 운영') and (selection_type == '공영주차장'):
        query = "SELECT STAT_NM '주차장명', ADRES '주소', if(is_24h = 1, 'O', 'X') as '24시간여부', if(is_public = 1, 'O', 'X') as '공영주차장여부', latitude '위도', longitude '경도', COUNT(*) '충전기수' FROM charging_station WHERE is_public = 1 and is_24h = 1 and ADRES LIKE ('" + dosi + "_" + sigungu + "%') GROUP BY STAT_NM, ADRES, is_24h, is_public, latitude, longitude;"
    #6. 24시간 운영이고 민영주차장일 때 is_public = 0 and is_24h = 1
    elif (selection_time == '24시간 운영') and (selection_type == '민영주차장'):
        query = "SELECT STAT_NM '주차장명', ADRES '주소', if(is_24h = 1, 'O', 'X') as '24시간여부', if(is_public = 1, 'O', 'X') as '공영주차장여부', latitude '위도', longitude '경도', COUNT(*) '충전기수' FROM charging_station WHERE is_public = 0 and is_24h = 1 and ADRES LIKE ('" + dosi + "_" + sigungu + "%') GROUP BY STAT_NM, ADRES, is_24h, is_public, latitude, longitude;"
    #7. 24시간 운영이 아닐 때   is_24h = 0
    elif (selection_time == '지정 시간제 운영') and (selection_type == None):
        query = "SELECT STAT_NM '주차장명', ADRES '주소', if(is_24h = 1, 'O', 'X') as '24시간여부', if(is_public = 1, 'O', 'X') as '공영주차장여부', latitude '위도', longitude '경도', COUNT(*) '충전기수' FROM charging_station WHERE is_24h = 0 and ADRES LIKE ('" + dosi + "_" + sigungu + "%') GROUP BY STAT_NM, ADRES, is_24h, is_public, latitude, longitude;"
    #8. 24시간 운영이 아니고, 공영주차장 일 때. is_public = 1 and is_24h = 0
    elif (selection_time == '지정 시간제 운영') and (selection_type == '공영주차장'):
        query = "SELECT STAT_NM '주차장명', ADRES '주소', if(is_24h = 1, 'O', 'X') as '24시간여부', if(is_public = 1, 'O', 'X') as '공영주차장여부', latitude '위도', longitude '경도', COUNT(*) '충전기수' FROM charging_station WHERE is_public = 1 and is_24h = 0 and ADRES LIKE ('" + dosi + "_" + sigungu + "%') GROUP BY STAT_NM, ADRES, is_24h, is_public, latitude, longitude;"
    #9. 24시간 운영이 아니고, 공영주차장아 아닐 때. is_public = 0 and is_24h = 0
    elif (selection_time == '지정 시간제 운영') and (selection_type == '민영주차장'):
        query = "SELECT STAT_NM '주차장명', ADRES '주소', if(is_24h = 1, 'O', 'X') as '24시간여부', if(is_public = 1, 'O', 'X') as '공영주차장여부', latitude '위도', longitude '경도', COUNT(*) '충전기수' FROM charging_station WHERE is_public = 0 and is_24h = 0 and ADRES LIKE ('" + dosi + "_" + sigungu + "%') GROUP BY STAT_NM, ADRES, is_24h, is_public, latitude, longitude;"
    
    # 쿼리 결과 데이터 프레임에 담기.
    result_df = db.get_data_as_dataframe(query)  

    # '위도', '경도' 열 삭제 후, 테이블로 보여주기.
    df = pd.DataFrame(result_df)
    df_new = df.drop(['위도', '경도'], axis=1)
    st.dataframe(df_new, height=500)
    
    # 위도, 경도 컬럼에 있는 값을 folium의 lat, lon 컬럼에 넣기.
    result_df[["lat","lon"]] = result_df[["위도","경도"]]

    # 처음 위치의 위도, 경도 설정
    m = folium.Map(location=[first_latitude, first_longtitude], zoom_start=13)

    marker_cluster = MarkerCluster().add_to(m)

    for idx, row in result_df.iterrows():
        popup_text = f"<b>{row['주차장명']}</b><br>{row['주소']}<br>24시간여부 : {row['24시간여부']}<br>충전기 갯수 : {row['충전기수']}"
        folium.Marker(
            location=[row["lat"], row["lon"]],
            popup=folium.Popup(popup_text, max_width=200)
        ).add_to(marker_cluster)

    folium_static(m)
    

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
    st.button("검색", on_click=search_result, disabled=False, use_container_width=True)


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
