import streamlit as st
import pandas as pd
import pydeck as pdk

# 데이터 불러오기
@st.cache_data
def load_data():
    return pd.read_csv("Delivery.csv")

df = load_data()

st.title("배달 위치 시각화")

# 지도 시각화
st.subheader("기본 지도 표시")
st.map(df[['Latitude', 'Longitude']])

# pydeck 고급 지도
st.subheader("고급 시각화 (Pydeck)")
layer = pdk.Layer(
    "ScatterplotLayer",
    data=df,
    get_position='[Longitude, Latitude]',
    get_radius=100,
    get_color='[200, 30, 0, 160]',
    pickable=True
)

view_state = pdk.ViewState(
    latitude=df["Latitude"].mean(),
    longitude=df["Longitude"].mean(),
    zoom=11,
    pitch=0
)

st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))
