from pathlib import Path
from typing import Union

from workers.document_workers import PdfExtractWorker
from workers.base import BaseWorker
from utils.logging_config import setup_logger

logger = setup_logger(__name__)

class DocumentProcessorFactory:
    """Factory for creating document processor workers based on file type."""

    @staticmethod
    def create_processor(file_path: Union[str, Path], output_dir: Union[str, Path]) -> BaseWorker:
        """
        Create and return the appropriate document processor worker for the given file.

        Args:
            file_path: Path to the document file
            output_dir: Directory to output the extracted text

        Returns:
            A worker instance that can process the document

        Raises:
            ValueError: If the file type is not supported
        """
        ext = Path(file_path).suffix.lower()

        if ext == '.pdf':
            logger.info(f"Creating PDF processor for {file_path}")
            return PdfExtractWorker(file_path, output_dir)
        else:
            logger.error(f"Unsupported file type: {ext}")
            raise ValueError(f"Unsupported file type: {ext}")