from shutil import move
from collections.abc import Iterable
from pathlib import Path
from filesorter import filter_check, extract_filters, move_file

# File Sorter Memory Efficient
class FSME:
    def __init__(self, filter_file_path: Path, current_dir: Path):
        self.current_dir = current_dir
        self.filters = extract_filters(filter_file_path)

    def filter_file_list_check(self, file_dir: Path, filter_list: Path) -> None:
        for file in self.current_dir.glob("*.*"):
            matching_folders = []
            for filter in self.filters:
                if filter_check(file.stem, filter):
                    matching_folders.append(filter[1])
            if len(matching_folders) == 1:
                self.unresolved_moves.append(file, matching_folders[0])
            elif len(matching_folders) > 1:
                self.conflicts.append(file, matching_folders)

    def change_filter_file(self, filter_file_path) -> None:
        self.filters = extract_filters(filter_file_path)

    def get_filters(self) -> Path:
        return self.filters

    def get_unresolved_moves(self) -> list[Path, Path]:
        return self.unresolved_moves

    def get_conflicts(self) -> list[Path, list[Path]]:
        return self.conflicts

    def get_current_dir(self) -> Path:
        return self.current_dir

    def change_current_dir(self, current_dir) -> None:
        self.current_dir = current_dir

    #!MOVE TO mem eff version
    @staticmethod
    def filter_extractor(filter_file: Path) -> Iterable[tuple[list[str], str]]:
        with open(filter_file, "r") as filters:
            for filter in filters:
                content = filter.split("/")

                keywords = content[0].split(",")
                folder = content[1]

                yield ([keywords, folder])

def filter_check(file_path: Path, filter: str):
    for keyword in filter[0]:
        if keyword in file_path.stem:
            return True
    return False

def extract_filters(filter_file: Path) -> list[list[str], str]:
    filter_list = []
    with open(filter_file, "r") as filters:
        for filter in filters:
            content = filter.split("/")

            keywords = content[0].split(",")
            folder = content[1]

            filter_list.append([keywords, folder])
    return filter_list