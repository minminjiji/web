import pandas as pd
import folium
import json

ta = pd.read_csv('./updated_check_num_park.csv', encoding='cp949')
ta = ta.sample(n=600, random_state=1)

geo_path = ('./skorea_municipalities_geo_simple.json')
geo_str = json.load(open(geo_path, encoding='utf-8'))

seoul_ta = folium.Map(location=[37.5502, 126.982], zoom_start=11)
seoul_ta

for i in ta.index:
    x = ta.loc[i, '위도']
    y = ta.loc[i, '경도']

    marker = folium.CircleMarker(location=[x, y], radius=5, line_color='red', fill_color='red', fill_opacity=1)
    marker.add_to(seoul_ta)

folium.GeoJson(geo_str, name='json_data').add_to(seoul_ta)

seoul_ta.save('./seoul_ta.html')
seoul_ta