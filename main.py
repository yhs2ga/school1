import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans

# 데이터 로딩 및 전처리
@st.cache_data
def load_data():
    df = pd.read_csv("Delivery.csv")
    df = df.rename(columns={"Latitude": "lat", "Longitude": "lon"})
    return df

df = load_data()

st.title("배달 위치 군집 시각화")

# 클러스터 수 선택
k = st.slider("클러스터 수 (K)", min_value=2, max_value=10, value=3)

# KMeans 군집화
kmeans = KMeans(n_clusters=k, random_state=0)
df["cluster"] = kmeans.fit_predict(df[["lat", "lon"]])

# Plotly 지도 시각화
fig = px.scatter_mapbox(
    df,
    lat="lat",
    lon="lon",
    color="cluster",
    hover_name="Num",
    zoom=11,
    height=600,
    title=f"{k}개의 클러스터로 배달 위치 시각화"
)

fig.update_layout(
    mapbox_style="open-street-map",
    margin={"r":0, "t":30, "l":0, "b":0}
)

st.plotly_chart(fig, use_container_width=True)
