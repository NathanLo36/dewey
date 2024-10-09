from shutil import move
from shutil import Error as shutilError
from pathlib import Path
from dataclasses import dataclass
import logging.handlers
import logging.config
import json
from os import listdir, remove

LOGGING_CONFIG = Path(__file__).parent / "logging_config.json"
LOGS_DIRECTORY = Path(".") / "dewey_logs"

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

    def __str__(self):
        string = f"{self.file_path} ->"

        for path in self.to_paths:
            string += f"\n\t{path}"

        return string


class Filesorter:
    def __init__(self, filter_file_path: str = "", log_handler: logging.Handler | None = None):
        self.working_dir: Path = None

        self.log_handler: logging.Handler | None = log_handler

        LOGS_DIRECTORY.mkdir(parents=True, exist_ok=True)

        with open(LOGGING_CONFIG) as f_in:
            logger_config = json.load(f_in)

        logging.config.dictConfig(logger_config)
        self.logger = logging.getLogger("Filesorter")
        self.logger.addHandler(log_handler)
        

        self.filter_file: Path = Path(filter_file_path)
        self.filters: list[Filter] = []
        self.configure(self._filter_file)
        
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
            self.logger.warning("No filters found in file")
            return

        files = self._working_dir.glob("*.*")

        self.conflicts.clear()

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
            except shutilError:
                self.logger.warning(f"Could not move {self.unresolved_moves[0].file_path}")
                pass
            self.unresolved_moves.pop(0)

    def get_conflicts(self) -> list[Conflict]:
        return self.conflicts

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
        self.logger.info(f"File {action.file_path} --> {action.to_path}")

    def configure(self, filter_file: Path) -> None:
        if filter_file != Path(""):
            self.filters.clear()
            filter_list = []
            with open(filter_file, "r", encoding="utf=8") as config:
                working_directory = Path(config.readline().strip())
                if not working_directory.exists():
                    self.logger.warning("First line does not contain an existing directory")
                    raise ValueError("First line does not contain an existing directory")
                else:
                    self.working_dir = working_directory
                
                for filter in config:
                    extracted = self.extract_filter(filter)
                    if extracted:
                        filter_list.append(extracted)
                        self.filters.append(extracted)
                self.logger.info(f"Configuration successful using {filter_file}")
        else:
            print("Filter file not selected")
            self.logger.info("Filter file not selected")


    def extract_filter(self, filter: str) -> Filter | None:
        content = filter.strip().split("|||")

        if len(content) == 1 and content[0] == "": #empty line
            return None

        if len(content) != 2: #too many separators
            self.logger.warning(f"Incorrect format for filter {str(filter)}")
            return None

        keywords = content[0].split(",")
        folder = Path(content[1]).resolve()
        if folder.exists():
            return Filter(keywords, folder)
        else:
            self.logger.warning("Directory " + str(folder) + " does not exist")
            return None
        
    def clear_logs(self):
        for file in listdir(Path(LOGS_DIRECTORY)):
            file_path = Path(LOGS_DIRECTORY) / file
            if file.startswith("filesorter.log."):
                remove(file_path)
            if Path(file_path) == Path(LOGS_DIRECTORY) / "filesorter.log":
                open(file_path, 'w').close()