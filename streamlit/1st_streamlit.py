import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
import folium as fol
import region_name
# from src.queries.insert_all_data import return_cur

st.set_page_config(layout="wide")

########## 페이지 제목 ##########
st.title('전기차 충전소 찾기')

########## 검색 조건 ##########
st.subheader('검색 조건')
st.markdown('지역')

gangwon_list = region_name.gangwon
gyeonggi_list = region_name.gyeonggi
gyeongnam_list = region_name.gyeongnam
gyeongbuk_list = region_name.gyeongbuk
gwangju_list = region_name.gwangju
daegu_list = region_name.daegu
daejeon_list = region_name.daejeon
busan_list = region_name.busan
seoul_list = region_name.seoul
sejong_list = region_name.sejong
ulsan_list = region_name.ulsan
incheon_list = region_name.incheon
jeonbuk_list = region_name.jeonbuk
jeonnam_list = region_name.jeonnam
chungbuk_list = region_name.chungbuk
chungnam_list = region_name.chungnam
jeju_list = region_name.jeju

# 첫 번째 선택박스: 도/광역시 선택
col1, col2 = st.columns(2)
with col1:
    dosi = st.selectbox("도/시를 선택하세요",
                    ['강원특별자치도', '경기도', '경상남도', '경상북도', '광주광역시',
                     '대구광역시', '대전광역시', '부산광역시', '서울특별시', '세종특별자치시',
                     '울산광역시', '인천광역시', '전라남도', '전북특별자치도', '제주특별자치도',
                     '충청남도', '충청북도'])
with col2:
    # 조건에 따라 두 번째 selectbox 동적으로 생성
    if dosi == "강원특별자치도":
        sigungu = st.selectbox("시/군/구 또는 읍/면/동을 선택하세요", gangwon_list)
    elif dosi == "경기도":
        sigungu = st.selectbox("시/군/구 또는 읍/면/동을 선택하세요", gyeonggi_list)
    elif dosi == "경상남도":
        sigungu = st.selectbox("시/군/구 또는 읍/면/동을 선택하세요", gyeongnam_list)
    elif dosi == "경상북도":
        sigungu = st.selectbox("시/군/구 또는 읍/면/동을 선택하세요", gyeongbuk_list)
    elif dosi == "광주광역시":
        sigungu = st.selectbox("시/군/구 또는 읍/면/동을 선택하세요", gwangju_list)
    elif dosi == "대구광역시":
        sigungu = st.selectbox("시/군/구 또는 읍/면/동을 선택하세요", daegu_list)
    elif dosi == "대전광역시":
        sigungu = st.selectbox("시/군/구 또는 읍/면/동을 선택하세요", daejeon_list)
    elif dosi == "부산광역시":
        sigungu = st.selectbox("시/군/구 또는 읍/면/동을 선택하세요", busan_list)
    elif dosi == "서울특별시":
        sigungu = st.selectbox("시/군/구 또는 읍/면/동을 선택하세요", seoul_list)
    elif dosi == "세종특별자치시":
        sigungu = st.selectbox("시/군/구 또는 읍/면/동을 선택하세요", sejong_list)
    elif dosi == "울산광역시":
        sigungu = st.selectbox("시/군/구 또는 읍/면/동을 선택하세요", ulsan_list)
    elif dosi == "인천광역시":
        sigungu = st.selectbox("시/군/구 또는 읍/면/동을 선택하세요", incheon_list)
    elif dosi == "전라남도":
        sigungu = st.selectbox("시/군/구 또는 읍/면/동을 선택하세요", jeonnam_list)
    elif dosi == "전라북도":
        sigungu = st.selectbox("시/군/구 또는 읍/면/동을 선택하세요", jeonbuk_list)
    elif dosi == "제주특별자치도":
        sigungu = st.selectbox("시/군/구 또는 읍/면/동을 선택하세요", jeju_list)
    elif dosi == "충청남도":
        sigungu = st.selectbox("시/군/구 또는 읍/면/동을 선택하세요", chungnam_list)
    elif dosi == "충청북도":
        sigungu = st.selectbox("시/군/구 또는 읍/면/동을 선택하세요", chungbuk_list)
st.divider()

col3, col4 = st.columns(2)
# 24시간 선택 구역
with col3:
    st.markdown("운영 시간")
    options = ["24시간 운영", "지정 시간제 운영"]
    selection = st.pills("선택 취소 시 버튼 한 번 더 클릭", options, selection_mode="single")
# 공영주차장 선택 구역
with col4:
    st.markdown("주차장 형태")
    options = ["공영주차장", "민영주차장"]
    selection = st.pills("선택 취소 시 버튼 한 번 더 클릭", options, selection_mode="single")
st.markdown("\n")
st.markdown("\n")
st.button("검색", on_click=None, disabled=False, use_container_width=True)

# def find_sidogungu_key():
#     connection, cursor = return_cur()
#     cursor.execute


########## 지도 데이터 구역 ##########
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
st_folium(m, width=1000, height=600, key="initial_map")


# 표 데이터 구역

# if option == "공영주차장" 1 else 0