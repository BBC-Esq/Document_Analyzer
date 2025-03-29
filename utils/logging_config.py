import logging
import os
import warnings
from pathlib import Path

logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

def configure_logging(level=logging.INFO):
    """
    Configure the root logger and set the global logging level.
    
    Args:
        level: The logging level to use (e.g., logging.DEBUG, logging.INFO)
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    root_logger.handlers.clear()

    console_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    file_handler = logging.FileHandler(logs_dir / "application.log")
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

def setup_logger(name=None):
    """
    Create a logger with the given name. Uses the root logger's level.
    If you want a module-specific log file, this function will create it.
    """
    logger = logging.getLogger(name)

    if name and not any(isinstance(h, logging.FileHandler) for h in logger.handlers):
        file_handler = logging.FileHandler(logs_dir / f"{name}.log")
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

configure_logging()
