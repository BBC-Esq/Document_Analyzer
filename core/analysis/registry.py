from typing import Dict, Type, Any, Optional
from utils.logging_config import setup_logger

logger = setup_logger(__name__)

class AnalysisStrategy:
    """Base class for analysis strategies."""

    @staticmethod
    def analyze_text(file_path: str, search_term: str) -> Dict[str, Any]:
        """
        Analyze text file according to the strategy.

        Args:
            file_path: Path to the text file
            search_term: Term to search for

        Returns:
            Dictionary with analysis results
        """
        raise NotImplementedError("Subclasses must implement analyze_text")

    @staticmethod
    def format_results(results: Dict[str, Any]) -> str:
        """
        Format analysis results as a string for display.

        Args:
            results: Dictionary with analysis results

        Returns:
            Formatted string for display
        """
        raise NotImplementedError("Subclasses must implement format_results")

class AnalysisRegistry:
    """Registry for analysis strategies."""

    _strategies: Dict[str, Type[AnalysisStrategy]] = {}

    @classmethod
    def register(cls, name: str, strategy_class: Type[AnalysisStrategy]):
        """Register an analysis strategy."""
        cls._strategies[name] = strategy_class
        logger.info(f"Registered analysis strategy: {name}")

    @classmethod
    def get_strategy(cls, name: str) -> Optional[Type[AnalysisStrategy]]:
        """Get an analysis strategy by name."""
        strategy = cls._strategies.get(name)
        if not strategy:
            logger.warning(f"Analysis strategy not found: {name}")
        return strategy

    @classmethod
    def get_default_strategy(cls) -> Type[AnalysisStrategy]:
        """Get the default analysis strategy."""
        if not cls._strategies:
            logger.error("No analysis strategies registered")
            raise ValueError("No analysis strategies registered")

        # string search is the default
        return cls._strategies.get("string_search")