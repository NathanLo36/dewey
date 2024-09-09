import logging
import customtkinter as ctk

class LogHandler(logging.Handler):
    def __init__(self, text_widget: ctk.CTkTextbox):
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record: str):
        log_message = self.format(record)
        self.text_widget.insert("end", log_message + "\n")