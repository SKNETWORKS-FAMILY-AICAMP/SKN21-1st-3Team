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

# def search_result():
#     #########################################
#     ############# 결과값 출력 구역 ##############
#     #########################################

#     ##### 작성자 : 승룡

#     CTPRVN_CD = '11'
#     # 첫 가운데 좌표 쿼리
#     query_1st_geo = "SELECT min(latitude) '1st_latitude' , min(longitude) '1st_longtitude' FROM charging_station WHERE CTPRVN_CD = '" + CTPRVN_CD + "';"
#     # query_1st_geo = "SELECT min(latitude) '1st_latitude' , min(longitude) '1st_longtitude' FROM charging_station WHERE CTPRVN_CD = '11' group by CTPRVN_CD;"

#     result_df_geo = db.get_data_as_dataframe(query_1st_geo)
#     for idx, row in result_df_geo.iterrows():
#         global first_latitude
#         global first_longitude
#         first_latitude = row['1st_latitude']
#         first_longtitude = row['1st_longtitude']

#     # if st.button("검색", on_click=None, disabled=False, use_container_width=True) :

#         # 쿼리 결과 출력
#     st.subheader("쿼리 결과")

#     # 버튼 선택별 쿼리 분기
#     # 1. 선택 사항을 아무것도 클릭 안했을 때
#     # selection_optime : 24시간 운영, 지정 시간제 운영
#     # selection_park_type : 공영주차장, 민영주차장
#     if (selection_time == None) and (selection_type == None):
#         # SQL 쿼리 입력
#         query = "SELECT STAT_NM '주차장명', ADRES '주소', if(is_24h = 1, 'O', 'X') as '24시간여부', latitude '위도', longitude '경도', COUNT(*) '충전기수' FROM charging_station WHERE CTPRVN_CD = '" + CTPRVN_CD + "' GROUP BY STAT_NM, ADRES, is_24h, latitude, longitude;"
#     elif (selection_time == '24시간 운영') and (selection_type == '공영주차장'):
#         print("24시간 운영!!")
#     elif (selection_time == '24시간 운영') and (selection_type == '민영주차장'):
#         print("지정 시간제 운영!!")
#     elif (selection_time == '지정 시간제 운영') and (selection_type == '공영주차장'):
#         print("지정 시간제 운영!!")
#     elif (selection_time == '지정 시간제 운영') and (selection_type == '민영주차장'):
#         print("지정 시간제 운영!!")
#     # SQL 쿼리 입력
#     # query = "SELECT STAT_NM '주차장명', ADRES '주소', if(is_24h = 1, 'O', 'X') as '24시간여부', latitude '위도', longitude '경도', COUNT(*) '충전기수' FROM charging_station WHERE CTPRVN_CD = '" + CTPRVN_CD + "' GROUP BY STAT_NM, ADRES, is_24h, latitude, longitude;" 
#     result_df = db.get_data_as_dataframe(query)  

#     # '위도', '경도' 열 삭제 후, 테이블로 보여주기.
#     df = pd.DataFrame(result_df)
#     df_new = df.drop(['위도', '경도'], axis=1)
#     st.dataframe(df_new, height=500)
    
#     # 2.  
#     result_df[["lat","lon"]] = result_df[["위도","경도"]]

#     # 처음 위치의 위도, 경도 설정
#     m = folium.Map(location=[first_latitude, first_longtitude], zoom_start=13)

#     marker_cluster = MarkerCluster().add_to(m)

#     for idx, row in result_df.iterrows():
#         popup_text = f"<b>{row['주차장명']}</b><br>{row['주소']}<br>24시간여부 : {row['24시간여부']}<br>충전기 갯수 : {row['충전기수']}"
#         folium.Marker(
#             location=[row["lat"], row["lon"]],
#             popup=folium.Popup(popup_text, max_width=200)
#         ).add_to(marker_cluster)

#     folium_static(m)
    

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
st.subheader("STEP 2 | 운영 정보 선택")
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


# 검색 버튼을 누를 때만 데이터 로드 및 표시
search_button = st.sidebar.button("검색")
if search_button:
    
    df = db.get_charging_stations_by_sigungu(
        dosi, 
        sigungu, 
        selection_time, 
        selection_park
    )

    # 1. DB 함수 호출: 사용자가 선택한 조건에 따라 데이터 조회
    st.session_state.search_results = df
    st.session_state.search_performed = True # 검색이 수행되었음을 표시
    st.session_state.search_params = {
        'dosi': dosi, 
        'sigungu': sigungu
    }

# 2. 데이터 유효성 검사
if st.session_state.search_performed:
    result_df = st.session_state.search_results
    params = st.session_state.search_params

    # 2. 데이터 유효성 검사
    if result_df.empty:
        st.warning(f"선택하신 지역 ({params['dosi']} {params['sigungu']})과 조건에 맞는 충전소 데이터를 찾을 수 없습니다. 조건을 변경해 주세요.")
    else:
        # 제목 표시
        st.subheader(f"{params['dosi']} {params['sigungu']} 충전소 검색 결과")
        
        # 지도 로직
        center_lat = result_df["latitude"].iloc[0]
        center_lon = result_df["longitude"].iloc[0]
        
        m = folium.Map(location=[center_lat, center_lon], zoom_start=13)
        marker_cluster = MarkerCluster().add_to(m)

        for idx, row in result_df.iterrows():
            popup_text = f"<b>{row['STAT_NM']}</b><br>{row['ADRES']}<br>충전기 수: {row['충전기_수']}대" 
            folium.Marker(
                location=[row["latitude"], row["longitude"]],
                popup=folium.Popup(popup_text, max_width=250),
                icon=folium.Icon(color="green", icon="fa-charging-station", prefix='fa')
            ).add_to(marker_cluster)

        # 4. Streamlit에 Folium 지도 출력
        folium_static(m)
        
        st.markdown('---') 
        
        # 5. 데이터프레임 (리스트) 출력
        st.subheader("상세 정보")
        st.dataframe(result_df, height=700, width=2000)