import filesorter as fs

def main():
    print("Main called")

if __name__ == "__main__":
    working_dir = input("Enter directory for sorting: ")
    filter_file = input("Enter filter file path: ")


    fs1 = fs.Filesorter(filter_file, working_dir)
    fs1.sort()