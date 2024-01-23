from shutil import move
from collections.abc import Iterable
from pathlib import Path


class Filesorter:
    def __init__(self, filter_file_path: Path, current_dir: Path):
        self.current_dir = current_dir
        self.filters = Filesorter.extract_filters(filter_file_path)
        self.conflicts = []
        self.unresolved_moves = []

    @staticmethod
    def filter_check(file_path: Path, filter: str):
        for keyword in filter[0]:
            if keyword in file_path.stem:
                return True
        return False

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

    #!MOVE TO mem eff version
    @staticmethod
    def filter_extractor(filter_file: Path) -> Iterable[tuple[list[str], str]]:
        with open(filter_file, "r") as filters:
            for filter in filters:
                content = filter.split("/")

                keywords = content[0].split(",")
                folder = content[1]

                yield ([keywords, folder])

    def filter_file_list_check(self, file_dir: Path, filter_list: Path) -> None:
        for file in self.current_dir.glob("*.*"):
            matching_folders = []
            for filter in self.filters:
                if Filesorter.filter_check(file.stem, filter):
                    matching_folders.append(filter[1])
            if len(matching_folders) == 1:
                self.unresolved_moves.append(file, matching_folders[0])
            elif len(matching_folders) > 1:
                self.conflicts.append(file, matching_folders)
            matching_folders.clear()

    def change_filter_file(self, filter_file_path) -> None:
        self.filters = Filesorter.extract_filters(filter_file_path)

    def get_filters(self) -> Path:
        return self.filters

    def get_current_dir(self) -> Path:
        return self.current_dir

    def change_current_dir(self, current_dir) -> None:
        self.current_dir = current_dir
