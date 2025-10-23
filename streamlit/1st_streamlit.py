import streamlit as st
import pandas as pd
from streamlit_folium import st_folium as st_fol
import folium as fol

########## 페이지 제목 ##########
st.title('전기차 충전소 찾기')

########## 옵션 선택 구역 ##########
option_map = {
    0: ":material/add:",
    1: ":material/zoom_in:",
    2: ":material/zoom_out:",
    3: ":material/zoom_out_map:",
}
selection = st.pills(
    "Tool",
    options=option_map.keys(),
    format_func=lambda option: option_map[option],
    selection_mode="single",
)
st.write(
    "Your selected option: "
    f"{None if selection is None else option_map[selection]}"
)

########## 지도 데이터 구역 ##########
st.subheader('지도 보기')
m = fol.Map(location=[14134232.89, 4520828.353], zoom_start=20)
## 여러개의 지도 마커
locations = [
    (14134232.89, 4520828.353, "신교공영주차장"),
    (14134232.89, 14134232.89, "청와대 사랑채 주차장"),
    (14134232.89,4519498.913, "적선동 공영주차장")
]
for lat, lon, name in locations:
    fol.Marker(
    [lat,lon],
    popup=name,
    icon=fol.Icon(icon='📍')
).add_to(m)
st_fol(m, width=900, height=900)

# 표 데이터 구역

