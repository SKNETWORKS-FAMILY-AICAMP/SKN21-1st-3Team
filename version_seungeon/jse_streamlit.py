import streamlit as st
import pandas as pd
from streamlit_folium import folium_static
import folium
from folium.plugins import MarkerCluster
from region_name import get_list as getl
import database as db

## 세션 저장 변수
if 'search_performed' not in st.session_state:
    # 검색 수행 여부 플래그
    st.session_state.search_performed = False 
if 'search_results' not in st.session_state:
    # 데이터프레임 저장 공간
    st.session_state.search_results = pd.DataFrame()
if 'search_params' not in st.session_state:
    # 검색 조건 저장 공간
    st.session_state.search_params = {}


with st.sidebar:
    st.title('전기차 충전소 찾기')
    st.subheader('Step 1. 지역 선택')

sido_list = db.get_SD_NM()

col1, col2 = st.sidebar.columns(2) 
# 
with col1:
    dosi = st.sidebar.selectbox("도/시를 선택하세요. (가다나순)",
                                 sido_list, key="dosi_select")
# 두 번째 선택박스: 시/군/구 선택
with col2:
    sigungu_list = getl(dosi)
    sigungu = st.sidebar.selectbox("시/군/구", sigungu_list, key="sigungu_select")
st.sidebar.divider() # st.divider()를 st.sidebar.divider()로 수정

## 시간 및 공영주차장 선택
col3, col4 = st.sidebar.columns(2) # st.columns(2)를 st.sidebar.columns(2)로 수정
# 운영시간 선택
with col3:
    st.subheader('Step 2. 운영정보 선택')
    st.sidebar.markdown("운영 시간")
    options_time = ["24시간 운영", "지정 시간제 운영"]
    selection_time = st.sidebar.pills("선택 취소 시 버튼 한 번 더 클릭", options_time, selection_mode="single", key="time_pills", label_visibility="collapsed")
# 공영주차장 선택
with col4:
    st.sidebar.markdown("주차장 형태")
    options_park = ["공영주차장", "민영주차장"]
    selection_park = st.sidebar.pills("선택 취소 시 버튼 한 번 더 클릭", options_park, selection_mode="single", key="park_pills", label_visibility="collapsed")
st.sidebar.markdown("\n")
st.sidebar.markdown("\n")






# 검색 버튼을 누를 때만 데이터 로드 및 표시
search_button = st.sidebar.button("검색")

df = db.get_charging_stations_by_sigungu(
    dosi, 
    sigungu, 
    selection_time, 
    selection_park
)

# DB 함수 호출: 사용자가 선택한 조건에 따라 데이터 조회
st.session_state.search_results = df
st.session_state.search_performed = True # 검색이 수행되었음을 표시
st.session_state.search_params = {
    'dosi': dosi, 
    'sigungu': sigungu
}

if st.session_state.search_performed:
    result_df = st.session_state.search_results
    params = st.session_state.search_params

    if result_df.empty:
        st.warning(f"선택하신 지역 ({params['dosi']} {params['sigungu']})과 조건에 맞는 충전소 데이터를 찾을 수 없습니다. 조건을 변경해 주세요.")
    else:
        st.subheader(f"{params['dosi']} {params['sigungu']} 충전소 검색 결과")        
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

        # Streamlit에 Folium 지도 출력
        folium_static(m)
        st.markdown('---') 
        # 데이터프레임 (리스트) 출력
        st.subheader("상세 정보")
        st.dataframe(result_df, height=700, width=2000)