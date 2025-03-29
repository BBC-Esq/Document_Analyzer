from utils.logging_config import setup_logger

logger = setup_logger(__name__)

def initialize_strategies():
    """Initialize all analysis strategies and ensure they're registered."""
    logger.info("Initializing analysis strategies")

    from core.analysis.string_search import StringSearchStrategy

    logger.info("Analysis strategies initialized")

def initialize_factories():
    """Initialize all factories."""
    logger.info("Initializing document processor factories")

    from core.document.factory import DocumentProcessorFactory

    logger.info("Document processor factories initialized")