import os
import filesorter as fs
from pathlib import Path
import shutil


def create_file(name: str) -> None:
    with open(name, "w") as f:
        f.write(name + " created")


def create_dir(name: str) -> None:
    os.makedirs(name, exist_ok=True)


def main():
    dir = Path(".").resolve()
    os.chdir(dir)

    test_dir = dir / "test"

    if test_dir.is_dir():
        shutil.rmtree(test_dir)

    input("Folders deleted. Press enter to continue.")

    create_dir("test")

    os.chdir(test_dir)

    create_file("test1.txt")
    create_file("test2.txt")
    create_file("test12.txt")
    create_file("test1-2.txt")
    create_file("test2-3.txt")
    create_file("test2-test3.txt")
    create_file("test_filters.txt")
    create_file("test6_test5.txt")
    create_file("test6.txt")
    create_file("TeSt78A.txt")

    create_dir("folder1")
    create_dir("folder2")
    create_dir("folder3")
    create_dir("folder4")
    create_dir("folder5")
    create_dir("folder6")


    with open((test_dir / "test_filters.txt").resolve(), "w") as test_filter:
        test_filter.write("test1|||folder1\n")
        test_filter.write("test2|||folder2\n")
        test_filter.write("test3|||folder3\n")
        test_filter.write("test4|||folder4\n")
        test_filter.write("test5,test6|||folder5\n")
        test_filter.write("*tEsT7|||folder6\n")

    input("Files created. Press enter to start sorting")

    filter_file = test_dir / "test_filters.txt"
    working_dir = test_dir

    fs1 = fs.Filesorter(filter_file, working_dir)
    fs1.sort()
    fs1.print_conflicts()


if __name__ == "__main__":
    main()
