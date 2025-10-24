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

st.sidebar.subheader('검색 조건')
st.sidebar.markdown('지역')

sido_list = db.get_SD_NM()

### 지역 선택
# 사이드바 내에서 컬럼 분할을 위해 st.sidebar.columns 사용
col1, col2 = st.sidebar.columns(2) 
# st.columns(2)를 st.sidebar.columns(2)로 수정

# 첫 번째 선택박스: 도/광역시 선택
with col1:
    dosi = st.sidebar.selectbox("도/시를 선택하세요. (가다나순)",
                                 ['강원특별자치도', '경기도', '경상남도', '경상북도', '광주광역시',
                                  '대구광역시', '대전광역시', '부산광역시', '서울특별시', '세종특별자치시',
                                  '울산광역시', '인천광역시', '전라남도', '전북특별자치도', '제주특별자치도',
                                  '충청남도', '충청북도'], key="dosi_select") # key 추가
# 두 번째 선택박스: 시/군/구 선택
with col2:
    sigungu_list = getl(dosi)
    sigungu = st.sidebar.selectbox("시/군/구", sigungu_list, key="sigungu_select") # key 추가
st.sidebar.divider() # st.divider()를 st.sidebar.divider()로 수정

## 시간 및 공영주차장 선택
col3, col4 = st.sidebar.columns(2) # st.columns(2)를 st.sidebar.columns(2)로 수정
# 운영시간 선택
with col3:
    st.sidebar.markdown("운영 시간")
    options_time = ["24시간 운영", "지정 시간제 운영"]
    selection_time = st.sidebar.pills("선택 취소 시 버튼 한 번 더 클릭", options_time, selection_mode="single", key="time_pills")
# 공영주차장 선택
with col4:
    st.sidebar.markdown("주차장 형태")
    options_park = ["공영주차장", "민영주차장"]
    selection_park = st.sidebar.pills("선택 취소 시 버튼 한 번 더 클릭", options_park, selection_mode="single", key="park_pills")
st.sidebar.markdown("\n")
st.sidebar.markdown("\n")

# 검색 버튼을 누를 때만 데이터 로드 및 표시
search_button = st.sidebar.button("검색")


# =========================================================================
# 검색 버튼 클릭 시 실행되는 메인 로직 (지도 -> 테이블 순서)
# =========================================================================
if search_button:
    
    # 1. DB 함수 호출: 사용자가 선택한 조건에 따라 데이터 조회
    result_df = db.get_charging_stations_by_sigungu(
        dosi, 
        sigungu, 
        selection_time, 
        selection_park
    )

    # 2. 데이터 유효성 검사
    if result_df.empty:
        st.warning(f"선택하신 지역 ({dosi} {sigungu})과 조건에 맞는 충전소 데이터를 찾을 수 없습니다. 조건을 변경해 주세요.")
    else:
        st.subheader(f"{dosi} {sigungu} 충전소 검색 결과")

        # 3. 지도 준비 및 출력 (테이블보다 먼저 표시)
        
        # 'latitude'와 'longitude' 컬럼은 이미 존재하므로 별도의 'lat', 'lon' 생성 로직 제거
        # 다만, 기존 코드에서 'lat', 'lon'을 생성했다면 그 코드를 유지해도 무방합니다.
        # 여기서는 컬럼 이름을 직접 사용합니다. (result_df["latitude"], result_df["longitude"])
        
        # 지도 중심 좌표 설정 (검색 결과의 첫 번째 충전소 위치로 설정)
        center_lat = result_df["latitude"].iloc[0]
        center_lon = result_df["longitude"].iloc[0]
        
        # 지도를 생성하고 마커 클러스터를 추가
        m = folium.Map(location=[center_lat, center_lon], zoom_start=13)
        marker_cluster = MarkerCluster().add_to(m)

        # 마커 추가
        for idx, row in result_df.iterrows():
            # '충전기_수' 컬럼은 db 함수에서 정의했으므로 이를 사용
            popup_text = f"<b>{row['STAT_NM']}</b><br>{row['ADRES']}<br>충전기 수: {row['충전기_수']}대" 
            
            folium.Marker(
                location=[row["latitude"], row["longitude"]],
                popup=folium.Popup(popup_text, max_width=250),
                icon=folium.Icon(color="green", icon="fa-charging-station", prefix='fa')
            ).add_to(marker_cluster)

        # 4. Streamlit에 Folium 지도 출력
        folium_static(m)
        
        st.markdown('---') 

        # 5. 데이터프레임 (리스트) 출력 (지도보다 아래로 이동)
        st.subheader("상세 정보")
        st.dataframe(result_df, height=700)