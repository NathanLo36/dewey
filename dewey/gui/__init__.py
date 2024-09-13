import customtkinter as ctk
from pathlib import Path
from ..util.filesorter import Filesorter, Conflict
from ..util.log_handler import LogHandler
import logging

class ConflictWindow(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.geometry("720x360")

        self.label = ctk.CTkLabel(self, text="Conflicts")
        self.label.pack(padx=20, pady=20)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=2)

        self.title("dewey Filesorter")
        self.geometry("1280x720")

        #filter file info and selection fram
        self.file_info_frame = ctk.CTkFrame(self)
        self.file_info_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nswe")
        self.file_info_frame.columnconfigure(0, weight=1)

        #control panel frame
        self.control_panel_frame = ctk.CTkFrame(self)
        self.control_panel_frame.grid(row = 0, column = 1, padx = 20, pady = 20, sticky="nsew")
        self.control_panel_frame.grid_rowconfigure(0, weight=10)
        self.control_panel_frame.grid_rowconfigure(1, weight=1)

        #current filter file text box
        self.current_filter_file = ctk.CTkTextbox(self.file_info_frame, height=20)
        self.current_filter_file.grid(row = 0, column = 0, sticky="NSEW")
        self.current_filter_file.insert("0.0", "Current filter file")
        self.current_filter_file.configure(state="disabled")

        # buttons
        self.filter_file_select_button = ctk.CTkButton(self.file_info_frame, text="Select Filter File", command=self.select_filter_file_button_callback)
        self.filter_file_select_button.grid(row = 0, column = 1, sticky="E")

        self.sort_button = ctk.CTkButton(self.control_panel_frame, text="Sort Files", command=self.sort_button_callback, height=50)
        self.sort_button.grid(row = 1, column = 0, padx = 0, pady = 0, sticky="s")

        self.clear_logs_button = ctk.CTkButton(self.control_panel_frame, text="Clear logs", command = self.clear_logs)
        self.clear_logs_button.grid(row = 0, column = 0, padx = 0, pady = 0)

        self.show_conflicts_button = ctk.CTkButton(self.control_panel_frame, text="Show conflicts", command = self.show_conflicts)


        self.quit_button = ctk.CTkButton(self, text="Quit", command=self.destroy)
        self.quit_button.grid(row = 1, column = 1, padx = 10, pady = 10)

        #log text box
        self.log_box = ctk.CTkTextbox(self)
        self.log_box.configure(state="disabled")
        self.log_box.grid(row = 0, column = 0, sticky="NSEW")

        log_handler = LogHandler(self.log_box)
        log_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s", "%Y-%m-%d %H:%M:%S %z"))
        log_handler.setLevel("INFO")

        self.fs1 = Filesorter(log_handler=log_handler)

    def select_filter_file_button_callback(self):
        self.log_box.configure(state="normal")
        self.current_filter_file.configure(state="normal")

        filter_file = Path(ctk.filedialog.askopenfilename())
        self.fs1.configure(filter_file)

        self.current_filter_file.delete("0.0", "end")
        self.current_filter_file.insert("0.0", str(filter_file))
        self.current_filter_file.configure(state="disabled")
        self.log_box.configure(state="disabled")

    def sort_button_callback(self):
        self.log_box.configure(state="normal")
        if self.fs1:
            self.fs1.sort()
        self.log_box.configure(state="disabled")

    def clear_logs(self):
        self.log_box.configure(state="normal")
        self.fs1.clear_logs()
        self.log_box.configure(state="disabled")

    def show_conflicts(self):
        conflicts = self.fs1.get_conflicts()
