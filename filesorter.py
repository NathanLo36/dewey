from shutil import move
from collections.abc import Iterable
from pathlib import Path


class Filesorter:
    def __init__(self, filter_file_path: Path, current_dir: Path):
        self.current_dir = current_dir
        self.filters = Filesorter.extract_filters(filter_file_path)

    def change_filter_file(self, filter_file_path):
        self.filters = Filesorter.extract_filters(filter_file_path)

    def change_current_dir(self, current_dir):
        self.current_dir = current_dir

    def filter_file_list_check(self, file_dir: Path, filter_list: Path):
        for file in self.current_dir.glob("*.*"):
            for filter in self.filters:
                matching_folders = []
                if filter_check(file.stem, filter):
                    matching_folders.append()

    @staticmethod
    def filter_check(file_path: Path, filter):
        for keyword in filter[0]:
            if keyword in file_path.stem:
                return True
        return False

    # Returns list of keywords and associated folders
    @staticmethod
    def extract_filters(filter_file: Path) -> list[list[str], str]:
        filter_list = []
        with open(filter_file, "r") as filters:
            for filter in filters:
                content = filter.split("/")

                keywords = content[0].split(",")
                folder = content[1]

                filter_list.append([keywords, folder])
        return filter_list

    @staticmethod
    def filter_extractor(filter_file: Path) -> Iterable[tuple[list[str], str]]:
        with open(filter_file, "r") as filters:
            for filter in filters:
                content = filter.split("/")

                keywords = content[0].split(",")
                folder = content[1]

                yield ([keywords, folder])
