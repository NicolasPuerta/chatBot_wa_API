#----------- Librerias ----------#
import logging
from datetime import datetime
import os


logger = logging.getLogger(__name__)

def Create_folder(path : str):
    if not os.path.exists(path):
        os.mkdir(path)
        logger.info(f"Created log folder: {path}")
    if os.path.exists(path):
        logger.info(f"existing log file: {path}")

def logs_continue(msg: str, path_log_name: str):
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(f"{path_log_name}", "a") as f:
        f.write(f"{date} - {msg}\n")