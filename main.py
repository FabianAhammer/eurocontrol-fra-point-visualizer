import os
from threading import Thread
import sys

from utils.eurocontrol_file_downloader import EurocontrolFileDownloader
from utils.fra_file_utils import FraFileUtils
from utils.xlsx_to_geojson_converter_service import XlsxToGeojsonConverterService

import flask
from flask import Flask, render_template


STATIC_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
server = Flask(__name__)

input_file_dir = "./input"
output_file_dir = "./output"


def update_loop_date() -> None:
    if not os.path.exists("./input"):
        os.mkdir("./input")
    worker: Thread = Thread(target=async_update_loop)
    worker.daemon = True
    worker.start()


def async_update_loop() -> None:
    downloader = EurocontrolFileDownloader(file_directory=input_file_dir)
    downloader.check_and_download_missing_files()
    if not os.path.exists("./output"):
        os.mkdir("./output")
    converter = XlsxToGeojsonConverterService(
        source_file_directory=input_file_dir, output_file_directory=output_file_dir
    )
    return converter.check_geo_json_available_for_source_files()


@server.route("/")
def serve_html():
    return render_template("index.html")


@server.route("/static/<resource>")
def serve_static(resource):
    return flask.send_from_directory(STATIC_PATH, resource)


@server.route("/static/available")
def serve_static_2():
    update_loop_date()
    return list(filter(lambda x: ".json" in x, os.listdir(STATIC_PATH)))


if __name__ == "__main__":
    print(os.listdir(STATIC_PATH))
    if sys.argv.__len__() == 2 and sys.argv[1] == "debug":
        debug_app = server
        debug_app.run(debug=True)
    else:
        server.run_server()
