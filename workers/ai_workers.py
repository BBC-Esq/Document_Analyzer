from workers.base import BaseWorker
from utils.logging_config import setup_logger

logger = setup_logger(__name__)

# This file will contain worker threads for AI-related operations
# Placeholder for future implementation

class LlmQueryWorker(BaseWorker):
    """
    Worker thread for querying LLM server.
    This is a placeholder for future implementation.
    """
    
    def __init__(self, text, prompt):
        super().__init__()
        self.text = text
        self.prompt = prompt
        self.response = ""
        logger.debug("LlmQueryWorker initialized (placeholder)")
        
    def run(self):
        # Placeholder for future implementation
        # Will connect to LLM server and retrieve response
        logger.info("LlmQueryWorker.run() called (not implemented)")
        self.signals.finished.emit(False, "LLM querying not implemented yet")