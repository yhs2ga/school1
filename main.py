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

st.title("📍 배달 위치 군집 시각화 (고급 분류 강조)")

# 클러스터 수 선택
k = st.slider("클러스터 수 (K)", min_value=2, max_value=10, value=4)

# KMeans 적용
kmeans = KMeans(n_clusters=k, random_state=42)
df["cluster"] = kmeans.fit_predict(df[["lat", "lon"]])
centroids = pd.DataFrame(kmeans.cluster_centers_, columns=["lat", "lon"])
centroids["cluster"] = range(k)

# 군집별로 필터링할 수 있도록 selectbox 추가
selected_cluster = st.selectbox("특정 클러스터만 보기 (전체 보기: '전체')", ["전체"] + list(map(str, range(k))))
if selected_cluster != "전체":
    df = df[df["cluster"] == int(selected_cluster)]

# 색상 팔레트 고정
color_map = px.colors.qualitative.Set2

# 지도 시각화
fig = px.scatter_mapbox(
    df,
    lat="lat",
    lon="lon",
    color=df["cluster"].astype(str),
    hover_name="Num",
    zoom=11,
    height=650,
    size_max=15,
    opacity=0.75,
    color_discrete_sequence=color_map,
)

# 군집 중심점 표시 (크고 흰색)
fig.add_scattermapbox(
    lat=centroids["lat"],
    lon=centroids["lon"],
    mode="markers+text",
    marker=dict(size=22, color="white", opacity=0.9, symbol="star"),
    text=[f"Cluster {i}" for i in range(k)],
    textposition="top center",
    name="Cluster Center"
)

# 스타일 적용
fig.update_layout(
    mapbox_style="carto-positron",
    margin={"r":0, "t":40, "l":0, "b":0},
    legend_title_text="클러스터 번호"
)

st.plotly_chart(fig, use_container_width=True)
