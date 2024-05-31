import logging
from logging.handlers import RotatingFileHandler
from PyQt5.QtCore import QThread, pyqtSignal

import os
from datetime import datetime


class Logger(QThread):
    log_signal = pyqtSignal(str)

    def __init__(self, log_dir, max_size_kb=None, backup_count=5):
        super().__init__()
        self.log_dir = log_dir
        self.max_size_kb = max_size_kb
        self.backup_count = backup_count
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        self.handler = None

    def _setup_handler(self):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file_path = os.path.join(self.log_dir, f"log_{timestamp}.txt")

        if self.max_size_kb:
            handler = RotatingFileHandler(
                log_file_path, maxBytes=int(self.max_size_kb) * 1024,
                backupCount=self.backup_count,
                encoding='utf-8'
            )
        else:
            handler = logging.FileHandler(log_file_path, encoding='utf-8')

        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        return handler

    def run(self):
        self.log_signal.connect(self.log)
        self.exec_()

    def log(self, message):
        if not self.handler:
            self.handler = self._setup_handler()
            self.logger.addHandler(self.handler)
        self.logger.info(message)

    def stop_logging(self):
        self.log_signal.disconnect(self.log)
        if self.handler:
            self.logger.removeHandler(self.handler)
            self.handler.close()
            self.handler = None
        self.quit()
        self.wait()

