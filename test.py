import os
import filesorter as fs
from pathlib import Path
import shutil

def create_file(name: str) -> None:
    with open(name, "w") as f:
        f.write(name + " created")


def create_dir(name: str) -> None:
    os.makedirs(name, exist_ok=True)


def clear_test_folder(testdir: Path) -> None:
    for file in os.listdir(testdir):
        file_dir = os.path.join(testdir, file)

        if os.path.isfile(file_dir):
            try:
                os.remove(file_dir)
                print(f"Deleted file: {file_dir}")
            except Exception as e:
                print(f"Error deleting file {file_dir}: {e}")
        elif os.path.isdir(file_dir):
            try:
                os.rmdir(file_dir)
                print(f"Deleted dir: {file_dir}")
            except Exception as e:
                print(f"Error deleting file {file_dir}: {e}")


def main():
    dir = Path('.') / 'test'
    dir = dir.resolve()
    os.chdir(dir)

    clear_test_folder(dir)

    input("Folders deleted. Press enter to continue.")

    create_file("test1.txt")
    create_file("test2.txt")
    create_file("test12.txt")
    create_file("test1-2.txt")
    create_file("test2-3.txt")
    create_file("test2-test3.txt")
    create_file("test_filters.txt")

    create_dir("folder1")
    create_dir("folder2")
    create_dir("folder3")
    create_dir("folder4")

    print( (dir / "test_filters.txt").resolve())

    with open((dir / "test_filters.txt").resolve(), "w") as test_filter:
        test_filter.write("test1|||folder1\n")
        test_filter.write("test2|||folder2\n")
        test_filter.write("test3|||folder3\n")
        test_filter.write("test4|||folder4\n")
        test_filter.write("test5|||folder1\n")

    input("Files created. Press enter to start sorting")

    filter_file = r"C:\Users\natef\Downloads\projects\dewey\test\test_filters.txt"
    working_dir = r"C:\Users\natef\Downloads\projects\dewey\test"

    fs1 = fs.Filesorter(filter_file, working_dir)
    fs1.filter_file_list_check()
    fs1.resolve_moves()
    fs1.resolve_conflicts()

if __name__ == "__main__":
    main()
