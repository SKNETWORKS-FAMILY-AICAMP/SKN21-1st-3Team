import streamlit as st
import pandas as pd
import pymysql as pms
from streamlit_folium import st_folium as st_fol
from streamlit_folium import folium_static
import folium as fol
from folium.plugins import MarkerCluster
from region_name import get_list as getl
from src.queries.insert_all_data import return_cur as rc
from datetime import datetime

#########################################
######## 사용자의 검색 조건 선택 구역 #########
#########################################

st.title('전기차 충전소 찾기')
st.subheader('검색 조건')
st.markdown('지역')

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
st.subheader('검색 결과')
st.markdown('지도 보기')
m = fol.Map(location=[37.58403, 126.96997], zoom_start=20)
## 여러개의 지도 마커
locations = [
    (37.58403, 126.96997, "신교공영주차장"),
    (37.58186, 126.97328, "청와대 사랑채 주차장"),
    (37.57456, 126.97405, "적선동 공영주차장")
]
for lat, lon, name in locations:
    fol.Marker(
    [lat,lon],
    popup=name,
    icon=fol.Icon(icon='📍')
).add_to(m)
st_fol(m, width=900, height=700)

# 표 데이터 구역
