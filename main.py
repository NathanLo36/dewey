import filesorter as fs
import tkinter as tk
from tkinter import filedialog


def main():
    print("Main called")

if __name__ == "__main__":
    # filter_file = input("Enter filter file path: ")

    root = tk.Tk()
    root.withdraw()

    filter_file = filedialog.askopenfilename()
    fs1 = fs.Filesorter(filter_file)
    fs1.sort()