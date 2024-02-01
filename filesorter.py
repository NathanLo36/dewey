from shutil import move
from pathlib import Path


class Filesorter:
    def __init__(self, filter_file_path: str, working_dir: str):
        self._working_dir: Path = Path(working_dir)
        self._filter_file: Path = Path(filter_file_path)
        self._filters: list[Filter] = extract_filters(self._filter_file)
        self._conflicts: list[tuple[Path, list[Path]]] = []
        self._unresolved_moves: list[tuple[Path, Path]] = []

    def filter_file_list_check(self) -> None:
        for file in self._working_dir.glob("*.*"):
            matching_folders = []
            for filter in self._filters:
                if filter_check(file, filter):
                    matching_folders.append(filter.folder)

            if len(matching_folders) == 1:
                self._unresolved_moves.append((file, matching_folders[0]))
            elif len(matching_folders) > 1:
                self._conflicts.append((file, matching_folders))

    def resolve_moves(self) -> None:
        for action in self._unresolved_moves:
            move_file(action[0], action[1])

    def list_conflicts(self) -> None:
        print("Unresolved conflicts:")
        for action in self._conflicts:
            
            print(f"{action[0]} -> ", end='')
            for folder in action[1]:
                print(f"[{folder}]", end=' ')
            print("\n")

    @property
    def unresolved_moves(self) -> list[Path, Path]:
        return self._unresolved_moves

    @property
    def conflicts(self) -> list[Path, list[Path]]:
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
        self._filters = extract_filters(filter_file)


class Filter:
    def __init__(self, keywords: list[str], folder: Path):
        self.keywords: list[str] = keywords
        self.folder: Path = folder


def filter_check(file_path: Path, filter: Filter) -> bool:
    for keyword in filter.keywords:
        if keyword in file_path.stem:
            return True
    return False


def extract_filters(filter_file: Path) -> list[Filter]:
    filter_list = []
    with open(filter_file, "r") as filters:
        for filter in filters:
            content = filter.strip().split("|||")

            if len(content) != 2:
                print(
                    "Error in filter format encountered, filter extraction cancelled."
                )
                return []

            keywords = content[0].split(",")
            folder = Path(content[1]).resolve()

            filter_list.append(Filter(keywords, folder))
    return filter_list


def move_file(fromloc: Path, toloc: Path):
    move(fromloc, toloc)
    print(f"File moved from {fromloc} to {toloc}")
