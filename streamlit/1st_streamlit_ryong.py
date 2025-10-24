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

print(sido_list)

### 지역 선택
col1, col2 = st.columns(2)
# 첫 번째 선택박스: 도/광역시 선택
with col1:
    dosi = st.selectbox("도/시를 선택하세요. (가다나순)",
                    ['강원특별자치도', '경기도', '경상남도', '경상북도', '광주광역시',
                     '대구광역시', '대전광역시', '부산광역시', '서울특별시', '세종특별자치시',
                     '울산광역시', '인천광역시', '전라남도', '전북특별자치도', '제주특별자치도',
                     '충청남도', '충청북도'])

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
    options1 = ["24시간 운영", "지정 시간제 운영"]
    selection_optime = st.pills("선택 취소 시 버튼 한 번 더 클릭", options1, selection_mode="single")

# 공영주차장 선택
with col4:
    st.markdown("주차장 형태")
    options2 = ["공영주차장", "민영주차장"]
    selection_park_type = st.pills("선택 취소 시 버튼 한 번 더 클릭", options2, selection_mode="single")
st.markdown("\n")
st.markdown("\n")

CTPRVN_CD = '11'
# 첫 가운데 좌표 쿼리
query_1st_geo = "SELECT min(latitude) '1st_latitude' , min(longitude) '1st_longtitude' FROM charging_station WHERE CTPRVN_CD = '" + CTPRVN_CD + "';"
# query_1st_geo = "SELECT min(latitude) '1st_latitude' , min(longitude) '1st_longtitude' FROM charging_station WHERE CTPRVN_CD = '11' group by CTPRVN_CD;"

result_df_geo = db.get_data_as_dataframe(query_1st_geo)
for idx, row in result_df_geo.iterrows():
    global first_latitude
    global first_longitude
    first_latitude = row['1st_latitude']
    first_longtitude = row['1st_longtitude']

if st.button("검색", on_click=None, disabled=False, use_container_width=True) :

    # 쿼리 결과 출력
    st.subheader("쿼리 결과")

    # 버튼 선택별 쿼리 분기
    # 1. 선택 사항을 아무것도 클릭 안했을 때
    # selection_optime : 24시간 운영, 지정 시간제 운영
    # selection_park_type : 공영주차장, 민영주차장
    if (selection_optime == None) and (selection_park_type == None):
        # SQL 쿼리 입력
         query = "SELECT STAT_NM '주차장명', ADRES '주소', if(is_24h = 1, 'O', 'X') as '24시간여부', latitude '위도', longitude '경도', COUNT(*) '충전기수' FROM charging_station WHERE CTPRVN_CD = '" + CTPRVN_CD + "' GROUP BY STAT_NM, ADRES, is_24h, latitude, longitude;"
    elif (selection_optime == '24시간 운영') and (selection_park_type == '공영주차장'):
        print("24시간 운영!!")
    elif (selection_optime == '24시간 운영') and (selection_park_type == '민영주차장'):
        print("지정 시간제 운영!!")
    elif (selection_optime == '지정 시간제 운영') and (selection_park_type == '공영주차장'):
        print("지정 시간제 운영!!")
    elif (selection_optime == '지정 시간제 운영') and (selection_park_type == '민영주차장'):
        print("지정 시간제 운영!!")
    # SQL 쿼리 입력
    # query = "SELECT STAT_NM '주차장명', ADRES '주소', if(is_24h = 1, 'O', 'X') as '24시간여부', latitude '위도', longitude '경도', COUNT(*) '충전기수' FROM charging_station WHERE CTPRVN_CD = '" + CTPRVN_CD + "' GROUP BY STAT_NM, ADRES, is_24h, latitude, longitude;" 
    result_df = db.get_data_as_dataframe(query)  

    # '위도', '경도' 열 삭제 후, 테이블로 보여주기.
    df = pd.DataFrame(result_df)
    df_new = df.drop(['위도', '경도'], axis=1)
    st.dataframe(df_new, height=500)
    
    # 2.  
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

# 표 데이터 구역
