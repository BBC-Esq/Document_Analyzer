import os
import tempfile
from typing import Dict, Any, Optional
from utils.logging_config import setup_logger

logger = setup_logger(__name__)

def create_report(search_results: Dict[str, Any]) -> bool:
    """
    Create a report file from search results and open it.
    
    Args:
        search_results: Dictionary containing search results
        
    Returns:
        Boolean indicating success
    """
    if not search_results:
        logger.warning("Attempted to create report with empty search results")
        return False

    try:
        logger.info(f"Creating report for search term: {search_results['term']}")
        with tempfile.NamedTemporaryFile(delete=False, suffix='.txt', mode='w', encoding='utf-8') as tmp:
            tmp.write(f"Search Term: {search_results['term']}\n\n")
            tmp.write(f"Document: {search_results['file']}\n")
            tmp.write(f"Total Occurrences: {search_results['count']}\n\n")
            tmp.write("Found on pages:\n")
            for page in search_results['pages']:
                tmp.write(f"{page}\n")

            tmp_path = tmp.name
            logger.debug(f"Report written to temporary file: {tmp_path}")

        # Open the file with the default application
        os.startfile(tmp_path)
        logger.info("Report opened with default application")
        return True

    except Exception as e:
        logger.error(f"Failed to create report: {str(e)}", exc_info=True)
        raise Exception(f"Failed to create report: {str(e)}")