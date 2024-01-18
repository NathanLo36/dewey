import os
from shutil import move as move_file
from collections.abc import Iterable
from pathlib import Path


def filter_file_list_check(file_dir: Path, filter_list: Path) -> Iterable[list[str]]:
    path = Path(file_dir)
    filters = filter_extractor(filter_list)
    for filter in filters:
        matching_filters = [i for i in path.glob('*.*') if ((filter in str(i)) and i.is_file())]
        yield(matching_filters)


def filter_extractor(filter_file: Path) -> Iterable[tuple[list[str], str]]:
    with open(filter_file, "r") as filters:
        for filter in filters:
            content = filter.split("/")

            keywords = content[0].split(",")
            folder = content[1]

            yield (keywords, folder)


# Returns an entire list of filters, for use in situations where memory is not an issue
# TODO delete later
def extract_filters(filter_file: str) -> list[list[str], str]:
    filter_list = []
    with open(filter_file, "r") as filters:
        for filter in filters:
            content = filter.split("/")

            keywords = content[0].split(",")
            folder = content[1]

            filter_list.append(keywords, folder)
    return filter_list
