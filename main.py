import streamlit as st
import pandas as pd
import plotly.express as px

# 데이터 로드
@st.cache_data
def load_data():
    return pd.read_csv("Delivery.csv")

df = load_data()

st.title("배달 위치 시각화 (Plotly 사용)")

# Plotly 지도
fig = px.scatter_mapbox(
    df,
    lat="Latitude",
    lon="Longitude",
    hover_name="Num",
    zoom=11,
    height=600
)

# 지도 스타일 설정
fig.update_layout(
    mapbox_style="open-street-map",
    margin={"r":0, "t":0, "l":0, "b":0}
)

st.plotly_chart(fig, use_container_width=True)
