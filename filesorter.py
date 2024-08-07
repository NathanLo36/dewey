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
    def __init__(self, filter_file_path: str):
        self.working_dir: Path = None
        self.filter_file: Path = Path(filter_file_path)
        self.filters: list[Filter] = self.configure(self._filter_file)
        self.conflicts: list[Conflict] = []
        self.unresolved_moves: list[MoveAction] = []

    @property
    def unresolved_moves(self) -> list[MoveAction]:
        return self._unresolved_moves

    @unresolved_moves.setter
    def unresolved_moves(self, moves: list[MoveAction]):
        self._unresolved_moves = moves

    @property
    def conflicts(self) -> list[Conflict]:
        return self._conflicts

    @conflicts.setter
    def conflicts(self, conflicts: list[Conflict]):
        self._conflicts = conflicts

    @property
    def working_dir(self) -> Path:
        return self.current_dir

    @working_dir.setter
    def working_dir(self, dir):
        self._working_dir = dir

    @property
    def filter_file(self) -> Path:
        return self._filter_file

    @filter_file.setter
    def filter_file(self, file: Path):
        self._filter_file = file

    @property
    def filters(self) -> Path:
        return self._filters

    @filters.setter
    def filters(self, filter_list: list[Filter]):
        self._filters = filter_list

    def find_moves(self) -> None:
        if len(self._filters) == 0:
            print("No filters found in file")
            return

        files = self._working_dir.glob("*.*")

        for file in files:
            matching_folders = []
            for filter in self._filters:
                if self.filter_check(file, filter):
                    matching_folders.append(filter.folder)

            if len(matching_folders) == 1:
                self.unresolved_moves.append(MoveAction(file, matching_folders[0]))
            elif len(matching_folders) > 1:
                self.conflicts.append(Conflict(file, matching_folders))

    def resolve_moves(self) -> None:
        while self.unresolved_moves:
            try:
                self.move_file(self.unresolved_moves[0])
            except:
                print(f"Could not move {self.unresolved_moves[0].file_path}")
                pass
            self.unresolved_moves.pop(0)

    def print_conflicts(self) -> None:
        print("Unresolved conflicts:")
        for action in self._conflicts:
            print(f"{action.file_path} -> ", end="")
            for folder in action.to_paths:
                print(f"[{folder}]", end=" ")
            print("\n")

    def sort(self):
        self.find_moves()
        self.resolve_moves()

    def filter_check(self, file_path: Path, filter: Filter) -> bool:
        if file_path.resolve() == self._filter_file.resolve():
            return False
        for keyword in filter.keywords:
            stem = file_path.stem

            if keyword.startswith("*"):
                keyword = keyword.lower()[1:]
                stem = stem.lower()
            if keyword in stem:
                return True
        return False

    def move_file(self, action: MoveAction):
        move(action.file_path, action.to_path)

    def configure(self, filter_file: Path) -> list[Filter]:
        filter_list = []
        with open(filter_file, "r", encoding="utf=8") as config:
            working_dir = Path(config.readline().strip())
            if not working_dir.exists():
                raise ValueError("First line is not a valid path")
            else:
                self.working_dir = working_dir
            
            for filter in config:
                extracted = self.extract_filter(filter)
                if extracted:
                    filter_list.append(extracted)
        return filter_list

    def extract_filter(self, filter: str) -> Filter | None:
        content = filter.strip().split("|||")

        if len(content) == 1 and content[0] == "":
            return None

        if len(content) != 2:
            return None

        keywords = content[0].split(",")
        folder = Path(content[1]).resolve()
        if folder.exists():
            return Filter(keywords, folder)
        else:
            return None
