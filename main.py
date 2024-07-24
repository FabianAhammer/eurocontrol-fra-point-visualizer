import os
import requests
import re

from utlis.eurocontrol_file_downloader import EurocontrolFileDownloader

if __name__ == "__main__":
    input_file_dir = "./input"

    downloader = EurocontrolFileDownloader(input_file_dir)
    downloader.check_and_download_missing_files()

# if not os.path.exists("./output"):
#     os.mkdir("./output")
#
# # Define coordinates of where we want to center our map
# austria_coords = [47.517201, 14.238281]
#
# available_files = filter(lambda name: name.__contains__(".xlsx"), os.listdir("./input"))
# for file in list(available_files):
#     print("Creating map for file: %s" % file)
#     data = pd.read_excel("input/%s" % file, sheet_name="FRA Points")
#
#     base_map = folium.Map(location=austria_coords, zoom_start=6)
#
#     group = ""
#     group_internal = None
#     for it, datarow in data.iterrows():
#         if datarow.iloc[MarkerUtil.FRA_ZONE] != group:
#             group = datarow.iloc[MarkerUtil.FRA_ZONE]
#             group_internal = folium.FeatureGroup(group).add_to(base_map)
#         MarkerUtil.create_marker(group_internal, MarkerUtil.convert_lat(datarow.iloc[MarkerUtil.LAT]),
#                                  MarkerUtil.convert_lon(datarow.iloc[MarkerUtil.LON]),
#                                  MarkerUtil.parse_purpose(datarow.iloc[MarkerUtil.EXI], datarow.iloc[MarkerUtil.AD]),
#                                  MarkerUtil.create_marker_header(datarow),
#                                  MarkerUtil.create_text(datarow))
#
#     folium.LayerControl().add_to(base_map)
#
#     base_map.save("output/%s.html" % (file.split(".")[0]))
