# 지도 확대/축소 슬라이더 추가
zoom_level = st.slider("초기 지도 확대 수준", min_value=1, max_value=15, value=11)

# 지도 시각화
fig = px.scatter_mapbox(
    df,
    lat="lat",
    lon="lon",
    color=df["cluster"].astype(str),
    hover_name="Num",
    zoom=zoom_level,  # 👈 여기에 적용
    height=650,
    size_max=15,
    opacity=0.75,
    color_discrete_sequence=color_map,
)

# 나머지 동일
