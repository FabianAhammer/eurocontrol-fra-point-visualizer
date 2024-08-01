import json
import math
from pandas import Series

from model.point_type import point_type


class FraPoint:
    NAME = 2
    LAT = 3
    LON = 4
    FRA_ZONE = 5
    EXI = 6
    AD = 7
    ARR_AP = 8
    DEP_AP = 9

    name: str
    latitude: float
    longitude: float
    arrival_airports: str
    departure_airports: str
    fra_zone: str
    roles: list[point_type]
    cycle: str = "N/A"

    def __init__(self, row: Series, cycle: str) -> None:
        self.name = row.iloc[FraPoint.NAME]
        self.latitude = FraPoint._convert_lat(row.iloc[FraPoint.LAT])
        self.longitude = FraPoint._convert_lon(row.iloc[FraPoint.LON])
        roles: list[str] = row.iloc[FraPoint.EXI] + row.iloc[FraPoint.AD]
        self.roles = [
            point_type(r) for r in list(filter(lambda role: role.isalpha(), roles))
        ]
        self.arrival_airports = (
            row.iloc[FraPoint.ARR_AP] if str(row.iloc[FraPoint.ARR_AP]) != "nan" else ""
        )
        self.departure_airports = (
            row.iloc[FraPoint.DEP_AP] if str(row.iloc[FraPoint.DEP_AP]) != "nan" else ""
        )
        self.fra_zone = row.iloc[FraPoint.FRA_ZONE]
        self.cycle = cycle
        # print(self.arrival_airports)
        # print(self.departure_airports)

    def to_geo_json(self) -> dict:
        return {
            "type": "Feature",
            "properties": {
                "name": f"{self.name}",
                "tooltip": self.generate_tooltip(),
                "role": "".join(sorted([role.value for role in self.roles])),
            },
            "geometry": {
                "coordinates": [self.longitude, self.latitude],
                "type": "Point",
            },
        }

    def identity(self) -> str:
        return f"{self.name}{self.latitude}{self.longitude}"

    def generate_tooltip(self) -> str:
        return f"<b>{self.name}</b>      Roles: {FraPoint.generate_html_for_roles(self.roles)} <br/> <b>FRA Zone:</b> {self.fra_zone} <br/> {self.generate_arrival_and_departure()} <b>Cycle</b> {self.cycle}"

    def generate_arrival_and_departure(self) -> str:
        arr_and_dep: str = ""
        if self.arrival_airports:
            arr_and_dep += f"<b>Arr. Airports:</b> {self.arrival_airports}"

        if self.arrival_airports and self.departure_airports:
            arr_and_dep += " <br /> "
        if self.departure_airports:
            arr_and_dep += f"<b>Dep. Airports: </b> {self.departure_airports}"
        return arr_and_dep + "<br/> "

    @staticmethod
    def generate_html_for_roles(roles: list[point_type]) -> str:
        role_html = ""
        for role in roles:
            if role == point_type.ENTRY:
                role_html += '<span style="color:#00bd16ff;font-weight:bold">E</span> '
            elif role == point_type.EXIT:
                role_html += '<span style="color:#ff3c00ff;font-weight:bold">X</span> '
            elif role == point_type.INTERMEDIATE:
                role_html += '<span style="color:grey;font-weight:bold">I</span> '
            elif role == point_type.DEP:
                role_html += '<span style="color:#ff1c7fff;font-weight:bold">D</span> '
            elif role == point_type.ARR:
                role_html += '<span style="color:#0000ffff;font-weight:bold">A</span> '
        return role_html

    @staticmethod
    def _convert_lat(lat: str) -> float:
        lat = str(lat)
        if lat[0] != "N" and lat[0] != "S":
            lat = "N" + lat
        d_str = lat[1:3]
        min_str = lat[3:5]
        sec_str = lat[5:7]
        calc = int(d_str) + (int(min_str) / 60) + (int(sec_str) / 3600)
        if lat[0] == "S":
            return -calc
        return calc

    @staticmethod
    def _convert_lon(lon: str) -> float:
        d_str = lon[1:4]
        min_str = lon[4:6]
        sec_str = lon[6:8]
        calc = int(d_str) + (int(min_str) / 60) + (int(sec_str) / 3600)
        if lon[0] == "W":
            return -calc
        return calc
