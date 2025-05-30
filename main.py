import streamlit as st
import pandas as pd
import plotly.express as px

# 데이터 로드
@st.cache_data
def load_data():
    df = pd.read_csv("Delivery.csv")
    df = df.rename(columns={"Latitude": "lat", "Longitude": "lon"})
    return df

df = load_data()

st.title("배달 위치 시각화 (Plotly 사용)")

# Plotly 지도
fig = px.scatter_mapbox(
    df,
    lat="lat",
    lon="lon",
    hover_name="Num",
    zoom=11,
    height=600
)

fig.update_layout(
    mapbox_style="open-street-map",
    margin={"r":0, "t":0, "l":0, "b":0}
)

st.plotly_chart(fig, use_container_width=True)

# st.map을 쓰고 싶다면 이렇게 사용해야 합니다
st.subheader("Streamlit 기본 지도")
st.map(df)
