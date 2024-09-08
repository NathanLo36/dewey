import logging.handlers
import logging.config
import json
from os import makedirs
from pathlib import Path

LOGGING_CONFIG = "./dewey/util/log_stream_config.json"
LOGS_DIRECTORY = "./dewey/logs"

class LogStream:
    def __init__(self):
        self.text_stack: list[str] = []

        if not Path(LOGS_DIRECTORY).is_dir():
            makedirs(LOGS_DIRECTORY)

        with open(LOGGING_CONFIG) as f_in:
            logger_config = json.load(f_in)
        
        logging.config.dictConfig(logger_config)
        self.logger = logging.getLogger("LogStream")

    def add_text(self, text: str) -> None:
        if len(self.text_stack) > 1024:
            self.text_stack.pop()
            self.logger.warning("Text Stack has too many entries, oldest ones removed")
        self.text_stack.append(text)
        self.logger.debug(f"{text} appended to text_stack")

    def pop_text(self) -> str:
        if self.text_stack:
            text = self.text_stack.pop()
            self.logger.debug(f"{text} popped from text_stack")
            return text
        else:
            self.logger.warning("No entries in text_stack")
            return ""
