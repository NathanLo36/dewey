import customtkinter as ctk
import filesorter as fs

app = ctk.CTk()
app.title("dewey Filesorter")
# app.geometry("400x150")

fs1 = fs.Filesorter(filter_file)


def sort_button():
    fs.sort()

def select_filter_file():
    filter_file = ctk.filedialog.askopenfilename()

app.mainloop()