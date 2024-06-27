from shutil import move
from pathlib import Path
from dataclasses import dataclass


@dataclass(init=True)
class Filter:
    keywords: list[str]
    folder: Path


@dataclass(init=True)
class MoveAction:
    file_path: Path
    to_path: Path


@dataclass(init=True)
class Conflict:
    file_path: Path
    to_paths: list[Path]


class Filesorter:
    def __init__(self, filter_file_path: str, working_dir: str):
        self._working_dir: Path = Path(working_dir)
        self._filter_file: Path = Path(filter_file_path)
        self._filters: list[Filter] = self.extract_filters_from_file(self._filter_file)
        self._conflicts: list[Conflict] = []
        self._unresolved_moves: list[MoveAction] = []

    def sort(self) -> None:
        for file in self._working_dir.glob("*.*"):
            matching_folders = []
            for filter in self._filters:
                if self.filter_check(file, filter):
                    matching_folders.append(filter.folder)

            if len(matching_folders) == 1:
                self._unresolved_moves.append(MoveAction(file, matching_folders[0]))
            elif len(matching_folders) > 1:
                self._conflicts.append(Conflict(file, matching_folders))

    def resolve_moves(self) -> None:
        for action in self._unresolved_moves:
            self.move_file(action)

    def list_conflicts(self) -> None:
        print("Unresolved conflicts:")
        for action in self._conflicts:
            print(f"{action.file_path} -> ", end="")
            for folder in action.to_paths:
                print(f"[{folder}]", end=" ")
            print("\n")

    def filter_check(self, file_path: Path, filter: Filter) -> bool:
        if file_path == self._filter_file:
            return False
        for keyword in filter.keywords:
            if keyword in file_path.stem:
                return True
        return False

    @property
    def unresolved_moves(self) -> list[MoveAction]:
        return self._unresolved_moves

    @property
    def conflicts(self) -> list[Conflict]:
        return self._conflicts

    @property
    def working_dir(self) -> Path:
        return self.current_dir

    @working_dir.setter
    def working_dir(self, current_dir) -> None:
        self.current_dir = current_dir

    @property
    def filter_file(self) -> Path:
        return self._filter_file

    @filter_file.setter
    def filter_file(self, filter_file) -> None:
        self._filter_file = filter_file
        self._filters = self.extract_filters_from_file(filter_file)
    
    def move_file(self, action: MoveAction):
        move(action.file_path, action.to_path)

    def extract_filters_from_file(self, filter_file: Path) -> list[Filter]:
        filter_list = []
        with open(filter_file, "r") as filters:
            for filter in filters:
                filter_list.append(self.extract_filter(filter))
        return filter_list

    def extract_filter(self, filter: str) -> Filter:
        content = filter.strip().split("|||")

        if len(content) != 2:
            print("Error in filter format encountered, filter extraction cancelled.")
            return []

        keywords = content[0].split(",")
        folder = Path(content[1]).resolve()
        return Filter(keywords, folder)



