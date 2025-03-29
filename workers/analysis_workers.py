from core.analysis.registry import AnalysisRegistry
from workers.base import BaseWorker
from utils.logging_config import setup_logger

logger = setup_logger(__name__)

class TextAnalyzeWorker(BaseWorker):
    """Worker thread for analyzing text files."""

    def __init__(self, file_path, search_term, strategy_name="string_search"):
        super().__init__()
        self.file_path = file_path
        self.search_term = search_term
        self.strategy_name = strategy_name
        self.results = {}
        logger.debug(f"TextAnalyzeWorker initialized with file: {file_path}, term: {search_term}")

    def run(self):
        try:
            # Get the strategy
            strategy_class = AnalysisRegistry.get_strategy(self.strategy_name)

            # Perform the analysis
            logger.info(f"Analyzing '{self.file_path}' for term: '{self.search_term}'")
            self.results = strategy_class.analyze_text(self.file_path, self.search_term)

            # Format the results
            results_str = strategy_class.format_results(self.results)

            # Signal completion
            logger.info(f"Analysis complete: Found {self.results['count']} instances")
            self.signals.finished.emit(True, results_str)

        except Exception as e:
            logger.error(f"Error analyzing file: {str(e)}", exc_info=True)
            self.signals.finished.emit(False, f"Error analyzing file: {str(e)}")