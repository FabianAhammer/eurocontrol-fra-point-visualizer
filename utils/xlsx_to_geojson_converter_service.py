import json
import os
import pandas as pd

from model.fra_point import FraPoint
from utils.fra_file_utils import FraFileUtils


class XlsxToGeojsonConverterService:
    _sheet_name = "FRA Points"
    _source_file_directory: str
    _output_file_directory: str

    def __init__(self, source_file_directory: str, output_file_directory) -> None:
        self._source_file_directory = source_file_directory
        self._output_file_directory = output_file_directory

    def check_geo_json_available_for_source_files(self) -> list[str]:

        (input_files_no_ext, output_files_no_ext) = self.get_files()
        for file_name in input_files_no_ext:
            if not output_files_no_ext.__contains__(file_name):
                data = self.convert_file(
                    pd.read_excel(
                        f"{self._source_file_directory}/{file_name}.xlsx",
                        sheet_name="FRA Points",
                    ),
                    FraFileUtils.get_cycle_for_file_name(file_name),
                )
                with open(f"{self._output_file_directory}/{file_name}.json", "w") as fw:
                    fw.write(data)
        return self.get_available_files()

    def get_available_files(self) -> list[str]:
        return list(
            filter(
                lambda x: x.split(".").__len__() > 1 and x.split(".")[1] == "json",
                os.listdir(self._output_file_directory),
            )
        )

    def unique_string_internals(self, first: str, second: str) -> str:
        arr = []
        if first:
            arr += first.split(",")
        if second:
            arr += second.split(",")
        return ",".join(set(arr))

    def convert_file(self, xlsx_data: pd.DataFrame, cycle: str) -> json:
        fra_dict: dict[str, FraPoint] = {}
        for _, series in xlsx_data.iterrows():
            point = FraPoint(series, cycle)
            # Copy over data to already set point
            if point.identity() in fra_dict:
                fra_dict[point.identity()].roles = list(
                    set(point.roles + fra_dict[point.identity()].roles)
                )
                fra_dict[point.identity()].arrival_airports = (
                    self.unique_string_internals(
                        fra_dict[point.identity()].arrival_airports,
                        point.arrival_airports,
                    )
                )
                fra_dict[point.identity()].departure_airports = (
                    self.unique_string_internals(
                        fra_dict[point.identity()].departure_airports,
                        point.departure_airports,
                    )
                )
                fra_dict[point.identity()].fra_zone = self.unique_string_internals(
                    fra_dict[point.identity()].fra_zone, point.fra_zone
                )
            else:
                fra_dict[point.identity()] = point

        return json.dumps(
            {
                "type": "FeatureCollection",
                "features": list(map(lambda x: x.to_geo_json(), fra_dict.values())),
            },
            separators=(",", ":"),
        )

    def get_files(self):
        input_xlsx_files = list(
            filter(
                lambda x: x.split(".")[1] == "xlsx",
                os.listdir(self._source_file_directory),
            )
        )
        input_files_no_ext = list(map(lambda of: of.split(".")[0], input_xlsx_files))

        output_json_files = list(
            filter(
                lambda x: x.split(".")[1] == "json",
                os.listdir(self._output_file_directory),
            )
        )
        output_files_no_ext = list(
            map(lambda of: of.split(".")[0], output_json_files),
        )
        return (input_files_no_ext, output_files_no_ext)
