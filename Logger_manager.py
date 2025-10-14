import logging
import os
from datetime import datetime

class LoggerManager:
    def __init__(self, base_dir="logs", log_level=logging.INFO):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)

        # Generate a timestamped log file name
        log_filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.log")
        log_path = os.path.join(self.base_dir, log_filename)

        # Configure Python logging
        logging.basicConfig(
            level=log_level,
            format="%(asctime)s | %(levelname)s | %(message)s",
            handlers=[
                logging.FileHandler(log_path, encoding="utf-8"),
                logging.StreamHandler()  # also print to console
            ]
        )

        self.logger = logging.getLogger(__name__)
        self.logger.info(f"📘 Logger initialized → {log_path}")

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def debug(self, msg):
        self.logger.debug(msg)
