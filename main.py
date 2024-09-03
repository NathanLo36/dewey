import filesorter as fs
import customtkinter as ctk
from tkinter import filedialog


def main():
    print("Main called")

if __name__ == "__main__":
    # filter_file = input("Enter filter file path: ")

    root = ctk.CTk()
    root.withdraw()

    filter_file = filedialog.askopenfilename()

    if filter_file:
        fs1 = fs.Filesorter(filter_file)
        fs1.sort()
        fs1.print_conflicts()