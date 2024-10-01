import customtkinter as ctk
import platform
import subprocess
from pathlib import Path
from ..util.filesorter import Filesorter, Conflict
from ..util.log_handler import LogHandler
import logging

class ConflictWindow(ctk.CTkToplevel):
    def __init__(self, conflicts : list[Conflict]):
        super().__init__()
        self.geometry("1280x720")

        self.title("Conflicts")
        self.grid_columnconfigure(0, weight=2)
        self.grid_rowconfigure(0, weight=2)

        self.text = ctk.CTkTextbox(self)
        self.text.grid(row = 0, column = 0, padx = 20, pady = 20, sticky="NSEW")

        self.text.configure(state="normal")

        for conflict in conflicts:
            self.text.insert("end", str(conflict))
            
        self.text.configure(state="disabled")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=2)

        self.title("dewey Filesorter")
        self.geometry("1280x720")

        self.conflict_window : None | ctk.CTkToplevel = None

        #filter file info and selection fram
        self.file_info_frame = ctk.CTkFrame(self)
        self.file_info_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nswe")
        self.file_info_frame.columnconfigure(0, weight=1)

        #control panel frame
        self.control_panel_frame = ctk.CTkFrame(self)
        self.control_panel_frame.grid(row = 0, column = 1, padx = 20, pady = 20, sticky="nsew")
        self.control_panel_frame.grid_rowconfigure(0, weight=0)
        self.control_panel_frame.grid_rowconfigure(1, weight=0)
        self.control_panel_frame.grid_rowconfigure(2, weight=5)

        #current filter file text box
        self.current_filter_file = ctk.CTkTextbox(self.file_info_frame, height=20)
        self.current_filter_file.grid(row = 0, column = 0, sticky="NSEW")
        self.current_filter_file.insert("0.0", "Current filter file")
        self.current_filter_file.configure(state="disabled")

        # buttons
        self.filter_file_select_button = ctk.CTkButton(self.file_info_frame, text="Select Filter File", command=self.select_filter_file_button_callback)
        self.filter_file_select_button.grid(row = 0, column = 1, sticky="E")

        self.sort_button = ctk.CTkButton(self.control_panel_frame, text="Sort Files", command=self.sort_button_callback, height=50)
        self.sort_button.grid(row = 3, column = 0, padx = 0, pady = 0, sticky="s")

        self.clear_logs_button = ctk.CTkButton(self.control_panel_frame, text="Clear logs", command = self.clear_logs, height=50)
        self.clear_logs_button.grid(row = 1, column = 0, padx = 0, pady = 0, sticky="n")

        self.show_conflicts_button = ctk.CTkButton(self.control_panel_frame, text="Show conflicts", command = self.show_conflicts, height=50)
        self.show_conflicts_button.grid(row = 2, column = 0, padx = 0, pady = 0)

        self.open_logs_button = ctk.CTkButton(self.control_panel_frame, text="Open logs", command = self.open_logs, height=50)
        self.open_logs_button.grid(row = 0, column = 0, padx = 0, pady = 0, sticky="n")

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
        if self.conflict_window is not None and self.conflict_window.winfo_exists():
            self.conflict_window.destroy()
        self.conflict_window = ConflictWindow(conflicts)
        self.conflict_window.focus()
    
    def open_logs(self):
        try:
            if platform.system() == "Windows":
                # Use os.startfile for Windows
                subprocess.run(["explorer", Path(__file__).parent.parent / "logs"])
            elif platform.system() == "Linux":
                # Use xdg-open for Linux
                subprocess.run(["xdg-open", Path(__file__).parent.parent / "logs"])
            else:
                print("Unsupported operating system.")
        except subprocess.CalledProcessError:
            print("Error opening file explorer.")