import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans

@st.cache_data
def load_data():
    df = pd.read_csv("Delivery.csv")
    df = df.rename(columns={"Latitude": "lat", "Longitude": "lon"})
    return df

df = load_data()

st.title("📍 배달 위치 클러스터링 시각화 (중심점 포함)")

# 클러스터 수 및 지도 줌 설정
k = st.slider("클러스터 수 선택", 2, 10, 4)
zoom_level = st.slider("지도 줌 수준", 1, 15, 11)

# KMeans 군집화
kmeans = KMeans(n_clusters=k, random_state=42)
df["cluster"] = kmeans.fit_predict(df[["lat", "lon"]])

# 중심점 좌표 가져오기
centroids = pd.DataFrame(kmeans.cluster_centers_, columns=["lat", "lon"])
centroids["cluster"] = [f"C{i}" for i in range(k)]

# Plotly 지도 시각화
color_map = px.colors.qualitative.Set2
fig = px.scatter_mapbox(
    df,
    lat="lat",
    lon="lon",
    color=df["cluster"].astype(str),
    hover_name="Num",
    zoom=zoom_level,
    height=650,
    opacity=1.0,
    color_discrete_sequence=color_map
)

# 중심점 표시 (별 모양 + 텍스트 레이블)
fig.add_scattermapbox(
    lat=centroids["lat"],
    lon=centroids["lon"],
    mode="markers+text",
    marker=dict(size=20, color="white", symbol="star"),
    text=centroids["cluster"],
    textposition="top center",
    name="Cluster Centers"
)

# 스타일 및 레이아웃 (밝은 지도 배경으로 변경)
fig.update_layout(
    mapbox_style="open-street-map",  # 밝은 스타일로 변경
    margin={"r": 0, "t": 40, "l": 0, "b": 0},
    legend_title_text="클러스터 번호"
)

st.plotly_chart(fig, use_container_width=True)
