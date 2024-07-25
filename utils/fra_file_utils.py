import re


class FraFileUtils:

    @staticmethod
    def get_cycle_for_file_name(file_name: str) -> str:
        cycle = re.search("eurocontrol-(.*?)-", file_name).group(1)
        return cycle
