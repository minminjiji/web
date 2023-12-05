import pandas as pd
import geopandas as gpd
import folium
from folium import Choropleth
import matplotlib.pyplot as plt

# 데이터 로딩
data = pd.read_csv('nor_202122.csv')

# GeoJSON 파일 로딩
geo_data = gpd.read_file('skorea_municipalities_geo_simple.json')

# 년도별로 데이터 분리
years = data['year'].unique()
data_years = {year: data[data['year'] == year] for year in years}

# 년도별로 지도 생성
for year, data_year in data_years.items():
    # 데이터 병합
    merged = geo_data.set_index('id').join(data_year.set_index('구'))

    # Folium 지도 생성
    m = folium.Map(location=[37.5665, 126.9780], zoom_start=10)

    # Choropleth 레이어 생성
    choropleth = Choropleth(
        geo_data=merged.__geo_interface__,
        data=data_year,
        columns=['구', '안전도'],
        key_on="feature.properties.name",
        fill_color='OrRd',
        legend_name=f'Safety Index ({year})'
    ).add_to(m)

    # 각 구역에 이름을 표시하는 툴팁 추가
    folium.GeoJsonTooltip(fields=['name']).add_to(choropleth.geojson)

    # 지도 출력
    plt.figure(figsize=(10, 10))
    plt.title(f'Safety Index ({year})')
    display(m)
    plt.axis('off')
    plt.show()