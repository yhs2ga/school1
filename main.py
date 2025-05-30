import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans

# 데이터 불러오기 및 전처리
@st.cache_data
def load_data():
    df = pd.read_csv("Delivery.csv")
    df = df.rename(columns={"Latitude": "lat", "Longitude": "lon"})
    return df

df = load_data()

st.title("📍 배달 위치 군집 시각화 (Plotly + KMeans)")

# 클러스터 수 조절
k = st.slider("클러스터 수 (K)", min_value=2, max_value=10, value=4)

# KMeans 군집화
kmeans = KMeans(n_clusters=k, random_state=42)
df["cluster"] = kmeans.fit_predict(df[["lat", "lon"]])
centroids = pd.DataFrame(kmeans.cluster_centers_, columns=["lat", "lon"])
centroids["cluster"] = range(k)

# 지도 시각화
fig = px.scatter_mapbox(
    df,
    lat="lat",
    lon="lon",
    color=df["cluster"].astype(str),
    hover_name="Num",
    zoom=11,
    size_max=15,
    height=650,
    opacity=0.7,
    title=f"🔵 {k}개의 클러스터로 배달 위치 시각화"
)

# 군집 중심점 추가 (흰색 큰 마커)
fig.add_scattermapbox(
    lat=centroids["lat"],
    lon=centroids["lon"],
    mode="markers",
    marker=dict(size=20, color="white", opacity=0.9, symbol="circle"),
    name="Cluster Center"
)

# 지도 스타일과 레이아웃 개선
fig.update_layout(
    mapbox_style="carto-positron",
    margin={"r":0, "t":50, "l":0, "b":0},
    legend_title_text="클러스터 번호"
)

st.plotly_chart(fig, use_container_width=True)
