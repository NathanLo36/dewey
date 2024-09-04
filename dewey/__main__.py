from .util import filesorter as fs
import customtkinter as ctk
from tkinter import filedialog
from pathlib import Path


def main():
    print("Main called")

if __name__ == "__main__":
    # filter_file = input("Enter filter file path: ")

    root = ctk.CTk()
    root.withdraw()

    filter_file = Path(filedialog.askopenfilename())

    fs1 = fs.Filesorter()
    fs1.configure(filter_file)
    fs1.sort()
    fs1.print_conflicts()