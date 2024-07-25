import requests
import re
import os


class EurocontrolFileDownloader:

    _base_uri: str = "https://www.eurocontrol.int"
    _point_overview_uri: str = (
        f"{_base_uri}/publication/free-route-airspace-fra-points-list-ecac-area"
    )
    _file_directory: str

    def __init__(self, file_directory: str) -> None:
        self._file_directory = file_directory

    def check_and_download_missing_files(self) -> None:
        current_files = os.listdir(self._file_directory)
        available_files = self.discover_files_to_download()

        for available in available_files:
            link = self.get_link_for_file(available)
            file_name_for_available = link.split("/")[-1]
            if not current_files.__contains__(file_name_for_available):
                self.write_to_fs(requests.get(link), file_name_for_available)

    def write_to_fs(self, file, file_name: str) -> None:
        with open(f"{self._file_directory}/{file_name}", "wb") as fh:
            fh.write(file.content)
            fh.flush()

    def discover_files_to_download(self) -> list[str]:
        site_content = str(requests.get(self._point_overview_uri).content)
        available_docs = re.findall(
            r'class="file__download">(.*?)</div>', site_content.replace("\n", "")
        )
        return available_docs

    # 'https://www.eurocontrol.int/sites/default/files/2024-06/eurocontrol-2407-fra-points-11jul2024.xlsx'
    def get_cycle_for_file_name(self, file_name: str) -> str:
        return re.search("eurocontrol-(.*?)-", file_name).group(1)

    def get_link_for_file(self, file_name: str) -> str:
        return self._base_uri + re.search('href="(.*?)"', file_name).group(1)

    def get_file_name_for_link(self, link: str) -> str:
        return link.split("/")[-1]
