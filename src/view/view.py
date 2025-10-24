import streamlit as st
from region_name import regions
from streamlit_folium import folium_static
from folium import folium, plugins, Marker
from find_region_code import find_region_code, find_sigungu_code
from get_station_list import get_station_table_list, get_station_map_list
import pandas as pd

# import find_region_code
#

st.set_page_config(layout="wide")

if "station_list" not in st.session_state:
    st.session_state.station_list = []

########## 페이지 제목 ##########


with st.sidebar:
    st.title("전기차 충전소 찾기")
    # 첫 번째 선택박스: 도/광역시 선택
    dosi = st.selectbox(
        "도/시를 선택하세요",
        regions,
    )
    # 조건에 따라 두 번째 selectbox 동적으로 생성
    sigungu = st.selectbox("시/군/구 또는 읍/면/동을 선택하세요", regions[dosi])

    st.divider()
    st.markdown(
        "<style>.st-key-search_button { margin-top: 20px; }</style>",
        unsafe_allow_html=True,
    )
    # 24시간 선택 구역

    st.markdown("운영 시간")
    options = ["지정 시간제 운영", "24시간 운영"]
    selection_time = st.pills(
        "선택 취소 시 버튼 한 번 더 클릭",
        options,
        selection_mode="single",
    )
    is_24hr = options.index(selection_time) if selection_time else None

    # 공영주차장 선택 구역
    is_public = None
    st.markdown("주차장 형태")
    options = ["민영주차장", "공영주차장"]
    selection_park = st.pills(
        "선택 취소 시 버튼 한 번 더 클릭",
        options,
        selection_mode="single",
    )
    is_public = options.index(selection_park) if selection_park else None


########## 지도 데이터 구역 ##########
region_code = find_region_code(dosi)
sigungu_code = find_sigungu_code(sigungu)
positions = (
    get_station_map_list(region_code or 0, sigungu_code or 0, is_24hr, is_public) or []
)

map = folium.Map(location=[37.5652, 126.9774], zoom_start=13)
map_cluster = plugins.MarkerCluster()
latitudes = []
longitudes = []

# 마커 추가
for row in positions:
    map_cluster.add_child(Marker(location=[row[1], row[0]], popup=row[2]))
    latitudes.append(row[1])
    longitudes.append(row[0])
map.add_child(map_cluster)

# 마커가 여러개인 경우 마커의 중심으로 지도 이동
if len(latitudes) > 1:
    map.fit_bounds(
        [
            [min(latitudes), min(longitudes)],
            [max(latitudes), max(longitudes)],
        ]
    )
# 마커가 한개라면 마커가 지도의 중심
elif len(latitudes) == 1:
    map.location = [latitudes[0], longitudes[0]]
folium_static(map)

# 표 데이터 구역
st.subheader("상세 목록")
matrix = pd.DataFrame(
    get_station_table_list(region_code or 0, sigungu_code or 0, is_24hr, is_public),
)
st.dataframe(matrix, width=1000)
