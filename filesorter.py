from shutil import move
from pathlib import Path


class Filesorter:
    def __init__(self, filter_file_path: Path, current_dir: Path):
        self._current_dir: Path = current_dir
        self._filters: list[Filter] = extract_filters(filter_file_path)
        self._conflicts: list[tuple[Path, list[Path]]] = []
        self._unresolved_moves: list[tuple[Path, Path]] = []

    def filter_file_list_check(self) -> None:
        for file in self.current_dir.glob("*.*"):
            matching_folders = []
            for filter in self._filters:
                if filter_check(file.stem, filter):
                    matching_folders.append(filter[1])

            if len(matching_folders) == 1:
                self._unresolved_moves.append((file, matching_folders[0]))
            elif len(matching_folders) > 1:
                self._conflicts.append((file, matching_folders))

    def resolve_moves(self) -> None:
        for action in self._unresolved_moves:
            move_file(action[0], action[1])

    def resolve_conflicts(self) -> None:
        for action in self._conflicts:
            print(len(action[0]))


    @property
    def filters(self) -> Path:
        return self._filters
    
    @filters.setter
    def change_filter_file(self, filter_file_path: Path):
        self._filters = extract_filters(filter_file_path)

    @property
    def _unresolved_moves(self) -> list[Path, Path]:
        return self._unresolved_moves

    @property
    def _conflicts(self) -> list[Path, list[Path]]:
        return self._conflicts

    @property
    def current_dir(self) -> Path: 
        return self.current_dir

    @current_dir.setter
    def current_dir(self, current_dir):
        self.current_dir = current_dir

class Filter:
    def __init__(self, keywords: list[str], folder: Path):
        self.keywords: list[str] = keywords
        self.folder: Path = folder


def filter_check(file_path: Path, filter: str) -> bool:
    for keyword in filter[0]:
        if keyword in file_path.stem:
            return True
    return False


def extract_filters(filter_file: Path) -> list[Filter]:
    filter_list = []
    with open(filter_file, "r") as filters:
        for filter in filters:
            content = filter.split("/")

            keywords = content[0].split(",")
            folder = content[1]

            filter_list.append([keywords, folder])
    return filter_list


def move_file(fromloc, toloc):
    move(fromloc, toloc)
    # TODO add logging
