import folium
import pandas as pd

from utlis.marker_util import MarkerUtil

# Define coordinates of where we want to center our map
austria_coords = [47.517201, 14.238281]

data = pd.read_excel("input/eurocontrol-2408-fra-points-08aug2024.xlsx", sheet_name="FRA Points")

base_map = folium.Map(location=austria_coords, zoom_start=6)

fras = []
group = ""
group_internal = None
for it, datarow in data.iterrows():
    if datarow.iloc[MarkerUtil.FRA_ZONE] != group:
        group = datarow.iloc[MarkerUtil.FRA_ZONE]
        group_internal = folium.FeatureGroup(group).add_to(base_map)
    MarkerUtil.create_marker(group_internal, MarkerUtil.convert_lat(datarow.iloc[MarkerUtil.LAT]),
                             MarkerUtil.convert_lon(datarow.iloc[MarkerUtil.LON]),
                             MarkerUtil.parse_purpose(datarow.iloc[MarkerUtil.EXI], datarow.iloc[MarkerUtil.AD]),
                             MarkerUtil.create_marker_header(datarow),
                             MarkerUtil.create_text(datarow))

# MarkerUtil.create_marker(base_map, 47.5, 14.23, PointType.INTERMEDIATE, "LOL")
folium.LayerControl().add_to(base_map)

base_map.save("output/map.html")
