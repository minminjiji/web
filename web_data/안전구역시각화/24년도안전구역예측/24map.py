import pandas as pd
import geopandas as gpd
import folium
from folium import Choropleth

# 데이터 로딩
data = pd.read_csv('nor_24.csv', encoding='EUC-KR')

# GeoJSON 파일 로딩
geo_data = gpd.read_file('skorea_municipalities_geo_simple24.json')

# 데이터 병합
merged = geo_data.set_index('id').join(data.set_index('구'))

# Folium 지도 생성
m = folium.Map(location=[37.5665, 126.9780], zoom_start=10)

# Choropleth 레이어 생성
choropleth = Choropleth(
    geo_data=merged.__geo_interface__,
    data=data,
    columns=['구', '안전도'],
    key_on="feature.properties.name",
    fill_color='YlOrBr',
    legend_name='Safety Index'
).add_to(m)

# 각 구역에 이름과 안전도를 표시하는 툴팁 추가
folium.GeoJsonTooltip(fields=['name', '안전도']).add_to(choropleth.geojson)

# 지도 출력
m