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
        self.grid_rowconfigure(0, weight=5)

        self.file_info_frame = ctk.CTkFrame(self)
        self.file_info_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nswe")
        self.file_info_frame.columnconfigure(0, weight=1)

        self.current_filter_file = ctk.CTkTextbox(self.file_info_frame, height=20)
        self.current_filter_file.grid(row = 0, column = 0, sticky="NSEW")
        self.current_filter_file.insert("0.0", "Current filter file")
        self.current_filter_file.configure(state="disabled") #makes it read only

        # buttons
        self.filter_file_select_button = ctk.CTkButton(self.file_info_frame, text="Select Filter File", command=self.select_filter_file_button_callback)
        self.filter_file_select_button.grid(row = 0, column = 1, sticky="E")

        self.sort_button = ctk.CTkButton(self, text="Sort Files", command=self.sort_button_callback)
        self.sort_button.grid(row = 0, column = 1, padx = 20, pady = 20)

        self.quit_button = ctk.CTkButton(self, text="Quit", command=self.destroy)
        self.quit_button.grid(row = 1, column = 1, padx = 10, pady = 10)

        #log text box
        self.log_box = ctk.CTkTextbox(self)
        self.log_box.configure(state="disabled")
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