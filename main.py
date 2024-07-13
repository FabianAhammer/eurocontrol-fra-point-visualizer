import os

import folium
import pandas as pd

from utlis.marker_util import MarkerUtil

if not os.path.exists("./output"):
    os.mkdir("./output")

# Define coordinates of where we want to center our map
austria_coords = [47.517201, 14.238281]

file = "eurocontrol-2408-fra-points-08aug2024.xlsx"
data = pd.read_excel("input/%s" % file, sheet_name="FRA Points")

base_map = folium.Map(location=austria_coords, zoom_start=6)

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

folium.LayerControl().add_to(base_map)

base_map.save("output/%s.html" % (file.split(".")[0]))
