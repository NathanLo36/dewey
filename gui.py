import customtkinter as ctk
import filesorter as fs


filter_file = ""

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("dewey Filesorter")
        # app.geometry("400x150")
        self.fs1 = None

        self.filter_file = ""

        # buttons
        self.filter_file_select = ctk.CTkButton(self, text="Select Filter File")

    def select_filter_file_button(self):
        self.filter_file = ctk.filedialog.askopenfilename()
        self.fs1 = fs.Filesorter(filter_file)

    def sort_button(self):
        if self.fs1:
            fs.sort()
