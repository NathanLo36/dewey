import customtkinter as ctk
import filesorter as fs
from pathlib import Path


filter_file = ""

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("dewey Filesorter")
        self.geometry("1280x720")
        self.fs1 = fs.Filesorter()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.file_info_frame = ctk.CTk.frame(master=self)
        self.file_info_frame.grid(row=0, column=0, padx=20)

        # buttons
        self.filter_file_select_button = ctk.CTkButton(self, text="Select Filter File", command=self.select_filter_file_button_callback)
        self.filter_file_select_button.grid(row = 1, column = 0, padx = 20, pady = 20)

        self.sort_button = ctk.CTkButton(self, text="Sort Files", command=self.sort_button_callback)
        self.sort_button.grid(row = 0, column = 1, padx = 20, pady = 20)

        self.quit_button = ctk.CTkButton(self, text="Quit", command=self.destroy)
        self.quit_button.grid(row = 1, column = 1, padx = 10, pady = 10)

        #log text box
        self.log_box = ctk.CTkTextbox(self)
        self.log_box.insert("0.0", "Log box to be added here")
        self.log_box.configure(state="disabled") #makes it read only
        self.log_box.grid(row = 0, column = 0, sticky="NSEW")

    def select_filter_file_button_callback(self):
        filter_file = Path(ctk.filedialog.askopenfilename())
        self.fs1.configure(filter_file)

    def sort_button_callback(self):
        if self.fs1:
            self.fs1.sort()

def main():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()