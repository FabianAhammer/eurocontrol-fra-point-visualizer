import folium
from folium import Map, FeatureGroup
from pandas import Series

from model.point_type import PointType


class MarkerUtil:

    @staticmethod
    def parse_purpose(relev_exi: str, relev_ad: str) -> PointType:
        parsable = relev_ad + relev_exi
        if parsable.__contains__("EX"):
            return PointType.ENTRY_AND_EXIT
        if parsable.__contains__("E"):
            return PointType.ENTRY
        if parsable.__contains__("X"):
            return PointType.EXIT
        if parsable.__contains__("A"):
            return PointType.ARR
        if parsable.__contains__("D"):
            return PointType.DEP
        if parsable.__contains__("I"):
            return PointType.INTERMEDIATE

    @staticmethod
    def create_marker(
        group: FeatureGroup,
        lat: float,
        lon: float,
        type: PointType,
        name: str,
        popup: str,
    ):
        folium.Marker(
            location=[lat, lon], tooltip=name, popup=popup, icon=folium.Icon(type.value)
        ).add_to(group)

    @staticmethod
    def get_relevance(datarow: Series):
        relevance: str = datarow.iloc[MarkerUtil.EXI] + datarow.iloc[MarkerUtil.AD]
        return relevance.replace("-", "")

    @staticmethod
    def create_marker_header(datarow: Series):
        relevance = MarkerUtil.get_relevance(datarow)
        return "%s - |%s|" % (relevance, datarow.iloc[MarkerUtil.NAME])

    @staticmethod
    def create_text(datarow: Series):
        relevance = MarkerUtil.get_relevance(datarow)
        text = """
        <ul>
            <li>Name:         %s</li>
            <li>FRA Zone:     %s</li>
            <li>Relevance:    %s</li>
            
        """ % (
            datarow.iloc[MarkerUtil.NAME],
            datarow.iloc[MarkerUtil.FRA_ZONE],
            relevance,
        )

        if relevance.__contains__("A"):
            text += (
                """
                <li>Arrival:      %s</li>
            """
                % datarow.iloc[MarkerUtil.ARR_AP]
            )

        if relevance.__contains__("D"):
            text += (
                """
                <li>Departure:    %s</li>
            """
                % datarow.iloc[MarkerUtil.DEP_AP]
            )

        return text + "</ul>"
