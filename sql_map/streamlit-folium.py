

import streamlit as st
from streamlit_folium import folium_static
import folium
from folium.plugins import MarkerCluster
import pandas as pd
from datetime import datetime

# states = gpd.read_file(file_path)
# states.head()
st.title("아 이제 추워요")
# save_dir = "daum_news_list"
# d = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
file_path = "daum_news_list/2025-10-23-12-20-46.csv"

df = pd.read_csv(file_path, encoding='utf-8')
print(type(df))
st.dataframe(df, height=200)

df[["lat","lon"]] = df[["X","Y"]]

m = folium.Map(location=[37.4562557, 126.7052062], zoom_start=13)

marker_cluster = MarkerCluster().add_to(m)

for idx, row in df.iterrows():
    popup_text = f"<b>{row['STAT_NM']}</b><br>{row['ADRES']}"
    folium.Marker(
        location=[row["lat"], row["lon"]],
        popup=folium.Popup(popup_text, max_width=200)
    ).add_to(marker_cluster)
    # popup_text = f"<b>{row['STAT_NM']}</b><br>{row['OBJT_ID']}"

    # if a == 0 and b == 0:
    #     if '공영주차장' not in row["ADRES"] and row["is_24h"] == 0 :
    #         folium.Marker(
    #         location=[row["lat"], row["lon"]],
    #         popup=folium.Popup(popup_text, max_width=200)
    #         ).add_to(marker_cluster)
    # elif a == 0 and b == 1:
    #     popup_text = f"<b>9999999</b><br>{row['OBJT_ID']}"
    # elif a == 1 and b == 0:
    #     popup_text = f"<b>{row['STAT_NM']}</b><br>{row['OBJT_ID']}"
    # else:
    #     popup_text = f"<b>{row['STAT_NM']}</b><br>{row['OBJT_ID']}"

folium_static(m)