import os
from shutil import move as move_file
from collections.abc import Iterable


def filter_check_with_extractor(file_name: str, filter_file: str) -> None:
    pass


def filter_check_with_list(file_name: str, filter_file: str) -> None:
    pass


# Used to create an generator to save memory
def filter_extractor(filter_file: str) -> Iterable[tuple[list[str], str]]:
    with open(filter_file, "r") as filters:
        for filter in filters:
            content = filter.split("/")

            keywords = content[0].split(",")
            folder = content[1]

            yield (keywords, folder)


# Returns an entire list of filters, for use in situations where memory is not an issue
def extract_filters(filter_file: str) -> list[list[str], str]:
    filter_list = []
    with open(filter_file, "r") as filters:
        for filter in filters:
            content = filter.split("/")

            keywords = content[0].split(",")
            folder = content[1]

            filter_list.append(keywords, folder)
    return filter_list
