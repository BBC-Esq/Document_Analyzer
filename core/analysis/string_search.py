import re
import os
from typing import Dict, Any

from core.analysis.registry import AnalysisStrategy, AnalysisRegistry
from utils.logging_config import setup_logger

logger = setup_logger(__name__)

class StringSearchStrategy(AnalysisStrategy):
    """Strategy for simple string search analysis."""
    
    @staticmethod
    def analyze_text(file_path: str, search_term: str) -> Dict[str, Any]:
        """Analyze text file for occurrences of a search term."""
        # This implementation is identical to your current analyze_text function
        # Copy the implementation from core/analysis/basic.py
        logger.info(f"Analyzing {file_path} for term: '{search_term}'")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            lower_content = content.lower()
            lower_search = search_term.lower()

            # Find page markers
            page_markers = re.findall(r'\[\[page(\d+)\]\]', content)
            logger.debug(f"Found {len(page_markers)} page markers")

            # Find all occurrences of the search term
            search_positions = []
            start_pos = 0

            while True:
                pos = lower_content.find(lower_search, start_pos)
                if pos == -1:
                    break
                search_positions.append(pos)
                start_pos = pos + 1

            # Find which page each occurrence is on
            page_instances = set()
            for pos in search_positions:
                page_matches = re.findall(r'\[\[page(\d+)\]\]', content[:pos])
                if page_matches:
                    page_instances.add(int(page_matches[-1]))

            count = len(search_positions)
            logger.info(f"Found {count} occurrences of '{search_term}' on {len(page_instances)} pages")

            results = {
                'term': search_term,
                'file': os.path.basename(file_path),
                'count': count,
                'pages': sorted(page_instances)
            }

            return results

        except Exception as e:
            logger.error(f"Error analyzing file: {str(e)}", exc_info=True)
            raise Exception(f"Error analyzing file: {str(e)}")
    
    @staticmethod
    def format_results(results: Dict[str, Any]) -> str:
        """Format analysis results as a string for display."""
        # This implementation is identical to your current format_analysis_results function
        # Copy the implementation from core/analysis/basic.py
        if not results:
            logger.warning("No results to format")
            return "No results available"
            
        count = results['count']
        term = results['term']
        filename = results['file']
        pages = results['pages']
        
        output = f"Found {count} instances of '{term}' in {filename}\n"
        output += f"Appearing on {len(pages)} pages: {', '.join(map(str, sorted(pages)))}"
        
        logger.debug(f"Formatted results: {output}")
        return output

# Register the strategy
AnalysisRegistry.register("string_search", StringSearchStrategy)