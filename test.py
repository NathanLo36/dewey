import os
import filesorter as fs


def create_file(name: str) -> None:
    with open(name, "w") as f:
        f.write(name + " created")


def create_dir(name: str) -> None:
    os.makedirs(name, exist_ok=True)


def clear_test_folder(testdir) -> None:
    for file in os.listdir(testdir):
        file_dir = os.path.join(testdir, file)

        if os.path.isfile(file_dir):
            try:
                # os.remove(file_dir)
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
    dir = os.path.normcase(os.path.join(os.getcwd(), "test"))
    os.chdir(dir)

    clear_test_folder(dir)

    create_file("test1.txt")
    create_file("test2.txt")
    create_file("test12.txt")
    create_file("test1-2.txt")
    create_file("test2-3.txt")
    create_dir("test1")
    create_dir("test2")

    input("Files created. Press a key to start sorting")

    filter_file = r"C:\Users\natef\Downloads\projects\dewey\test_filters.txt"
    working_dir = r"C:\Users\natef\Downloads\projects\dewey\test"

    fs1 = fs.Filesorter(filter_file, working_dir)
    fs1.filter_file_list_check()
    fs1.resolve_moves()
    fs1.resolve_conflicts()

if __name__ == "__main__":
    main()
