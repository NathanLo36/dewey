import os
from shutil import move as move_file
from collections.abc import Iterable



def filter_file_list_check(file_dir: str, filters: Iterable[str]) -> list[bool]:
    for filter in filters:
        for file in os.listdir(file_dir):
            if filter in file:



def filter_extractor(filter_file: str) -> Iterable[tuple[list[str], str]]:
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
