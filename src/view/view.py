import streamlit as st
from streamlit_folium import st_folium
import folium as fol
from region_name import regions

# import find_region_code
#

st.set_page_config(layout="wide")

########## 페이지 제목 ##########
st.title("전기차 충전소 찾기")

########## 검색 조건 ##########
st.subheader("검색 조건")
st.markdown("지역")

# 첫 번째 선택박스: 도/광역시 선택
col1, col2 = st.columns(2)
with col1:
    dosi = st.selectbox(
        "도/시를 선택하세요",
        regions,
    )
with col2:
    # 조건에 따라 두 번째 selectbox 동적으로 생성
    sigungu = st.selectbox("시/군/구 또는 읍/면/동을 선택하세요", regions[dosi])

st.divider()
st.markdown(
    "<style>.area_1 { padding: 8px; border: 1px solid white}</style> <div class='area_1'>",
    unsafe_allow_html=True,
)
col3, col4 = st.columns(2)
st.markdown("</div>", unsafe_allow_html=True)
# 24시간 선택 구역
is_24hr = None

with col3:
    st.markdown("운영 시간")
    options = ["지정 시간제 운영", "24시간 운영"]
    selection = st.pills(
        "선택 취소 시 버튼 한 번 더 클릭",
        options,
        selection_mode="single",
    )
    is_24hr = options.index(selection) if selection else None


# 공영주차장 선택 구역
is_public = None
with col4:
    st.markdown("주차장 형태")
    options = ["민영주차장", "공영주차장"]
    selection = st.pills(
        "선택 취소 시 버튼 한 번 더 클릭",
        options,
        selection_mode="single",
    )
    is_public = options.index(selection) if selection else None


st.markdown("\n")
st.markdown("\n")

print(is_24hr, is_public)
st.button("검색", on_click=None, disabled=False, use_container_width=True)


########## 지도 데이터 구역 ##########
st.subheader("검색 결과")
st.markdown("지도 보기")
m = fol.Map(location=[37.58403, 126.96997], zoom_start=20)
## 여러개의 지도 마커
locations = [
    (37.58403, 126.96997, "신교공영주차장"),
    (37.58186, 126.97328, "청와대 사랑채 주차장"),
    (37.57456, 126.97405, "적선동 공영주차장"),
]
for lat, lon, name in locations:
    fol.Marker([lat, lon], popup=name, icon=fol.Icon(icon="📍")).add_to(m)
st_folium(m)


# 표 데이터 구역
