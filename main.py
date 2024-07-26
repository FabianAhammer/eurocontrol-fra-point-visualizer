import json
import os
from dash import Dash, html, dcc, State, callback, Output, Input, no_update
import dash_leaflet as dl
from dash_extensions.javascript import assign

from utils.eurocontrol_file_downloader import EurocontrolFileDownloader
from utils.fra_file_utils import FraFileUtils
from utils.xlsx_to_geojson_converter_service import XlsxToGeojsonConverterService
from flask import Flask

server = Flask(__name__)

app = Dash(server=server)
input_file_dir = "./input"
output_file_dir = "./output"


def update_loop_date() -> list[str]:

    if not os.path.exists("./input"):
        os.mkdir("./input")
    downloader = EurocontrolFileDownloader(file_directory=input_file_dir)
    downloader.check_and_download_missing_files()

    if not os.path.exists("./output"):
        os.mkdir("./output")
    converter = XlsxToGeojsonConverterService(
        source_file_directory=input_file_dir, output_file_directory=output_file_dir
    )
    return converter.check_geo_json_available_for_source_files()


def build_data_with_labels(files: list[str]) -> list:
    files = sorted(
        files, key=lambda f: int(FraFileUtils.get_cycle_for_file_name(f)), reverse=True
    )
    return [
        {"label": FraFileUtils.get_cycle_for_file_name(file), "value": file}
        for file in files
    ]


def read_output_file(file_name: str) -> str:
    with open(f"{output_file_dir}/{file_name}", "r") as fr:
        return json.loads(fr.read())


icon_function = assign(
    """function(feature, latlng){
    const flag = L.icon({iconUrl: `./assets/${feature.properties.role}.svg`, iconSize: [24, 24] });
    return L.marker(latlng, {icon: flag});
    }"""
)

# geojson_filter = assign("function(feature, context){return context.hideout.includes(feature.properties.name);}")
# Any Feature without a name, is a cluster!
geojson_filter = assign(
    """function(feature, context){
        if(!feature?.properties?.name)
        return true
        return context.hideout.length == 0 || context.hideout.find(e => feature.properties.name.toLowerCase().includes(e.toLowerCase()))
        }"""
)
app.layout = [
    dcc.Store(id="session", storage_type="session"),  # data={"files": cycles}),
    html.Div(
        children=[
            html.Div(),
            dcc.Dropdown(
                id="cycle-selector",
                clearable=False,
            ),
            html.H2("Eurocontrol FRA Points", style={"text-align": "center"}),
            dcc.Input(
                id="search",
                type="text",
                placeholder="Search Point ...",
                style={"padding": "0.5rem"},
            ),
        ],
        style={
            "display": "grid",
            "grid-template-columns": "1fr 1fr 2fr 1fr 1fr",
            "font-family": "Sans-Serif",
            "align-items": "center",
        },
    ),
    dl.Map(
        center=[48, 12],
        zoom=5,
        children=[
            dl.TileLayer(),
            dl.GeoJSON(
                id="frapoints-geojson",
                cluster=True,
                zoomToBoundsOnClick=True,
                superClusterOptions={"radius": 100, "minPoints": 8, "minZoom": 2},
                filter=geojson_filter,
                pointToLayer=icon_function,
                hideout=[],
            ),
        ],
        style={"height": "90vh"},
    ),
]


@callback(
    Output("cycle-selector", "options"),
    Output("cycle-selector", "value"),
    State("cycle-selector", "value"),
    Input("session", "data"),
)
def session_action(selected_value, _):
    built_dropdown = build_data_with_labels(update_loop_date())
    if selected_value == None:
        return [built_dropdown, built_dropdown[0]["value"]]
    return [built_dropdown, no_update]


@callback(
    Output("frapoints-geojson", "data"),
    Input("cycle-selector", "value"),
)
def dropdown_action(cycle_as_file):
    file = read_output_file(cycle_as_file)
    return file


app.clientside_callback(
    "function(x){return (!x || x == '')? true : false}",
    Output("frapoints-geojson", "cluster"),
    Input("search", "value"),
)

app.clientside_callback(
    "function(x){return x ? x.split(',').map(e => (e??'').trim()) : []}",
    Output("frapoints-geojson", "hideout", allow_duplicate=True),
    Input("search", "value"),
    prevent_initial_call=True,
)

if __name__ == "__main__":

    app.run_server()
