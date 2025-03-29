import logging
import os
import warnings
from pathlib import Path

logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

def setup_logger(name=None):
    """
    Create a logger with the given name.
    If name is None, returns the root logger.
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        # Set logging level
        logger.setLevel(logging.INFO)
        # logger.setLevel(logging.DEBUG)
        # logger.setLevel(logging.WARNING)
        # logger.setLevel(logging.ERROR)
        # logger.setLevel(logging.CRITICAL)

        console_handler = logging.StreamHandler()
        file_handler = logging.FileHandler(logs_dir / f"{name or 'root'}.log")

        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
    
    return logger

root_logger = setup_logger()
