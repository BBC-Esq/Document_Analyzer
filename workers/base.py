from PySide6.QtCore import QObject, Signal, QThread
from utils.logging_config import setup_logger

logger = setup_logger(__name__)

class WorkerSignals(QObject):
    """Defines the signals available from a running worker thread."""
    finished = Signal(bool, str)  # Success status, message

class BaseWorker(QThread):
    """
    Base worker thread class.
    
    Inherits from QThread to handle worker thread setup.
    Contains a signals attribute to communicate with the main thread.
    """
    def __init__(self):
        super().__init__()
        self.signals = WorkerSignals()
        logger.debug(f"BaseWorker initialized: {self.__class__.__name__}")