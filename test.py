import os
from pathlib import Path
import shutil
from dewey.gui import App


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

    #should end up in folder1
    create_file("test1.txt")
    create_file("test12.txt")
    create_file("test1-2.txt")

    # should end up in folder 2
    create_file("test2.txt")
    create_file("test2-3.txt")

    #should create a conflict
    create_file("test2-test3.txt")

    # should end up in folder 5
    create_file("test6_test5.txt")
    create_file("test6.txt")

    #should end up in folder 6
    create_file("TeSt78A.txt")

    create_dir("folder1")
    create_dir("folder2")
    create_dir("folder3")
    create_dir("folder4")
    create_dir("folder5")
    create_dir("folder6")

    create_file("test_filters.txt")

    with open((test_dir / "test_filters.txt").resolve(), "w") as test_filter:
        test_filter.write(f"{test_dir}\n\n")
        test_filter.write(f"test1|||{test_dir}\\folder1\n")
        test_filter.write("Subtitle test\n")
        test_filter.write(f"test2|||{test_dir}\\folder2\n")
        test_filter.write(f"test3|||{test_dir}\\folder3\n")
        test_filter.write(f"test4|||{test_dir}\\folder4\n")
        test_filter.write(f"test5,test6|||{test_dir}\\folder5\n")
        test_filter.write(f"*tEsT7|||{test_dir}\\folder6\n")

    input("Files created in test folder, use dewey to sort.")

if __name__ == "__main__":
    main()