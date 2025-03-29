# workers/document_workers.py
import os
from pathlib import Path

from workers.base import BaseWorker
from core.document.pdf import extract_text_from_pdf
from utils.file_utils import get_unique_filename
from utils.logging_config import setup_logger

logger = setup_logger(__name__)

class PdfExtractWorker(BaseWorker):
    """Worker thread for extracting text from PDF files."""

    def __init__(self, pdf_path, output_dir):
        super().__init__()
        self.pdf_path = pdf_path
        self.output_dir = output_dir
        logger.debug(f"PdfExtractWorker initialized with PDF: {pdf_path}")

    def run(self):
        try:
            logger.info(f"Starting PDF extraction for {self.pdf_path}")

            documents = extract_text_from_pdf(self.pdf_path)
            
            if not documents:
                logger.warning("No content extracted from PDF")
                self.signals.finished.emit(False, "No content could be extracted from the PDF")
                return

            output_path_base = get_unique_filename(self.pdf_path, self.output_dir)
            output_path = output_path_base.with_suffix('.txt')

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(documents[0].page_content)

            logger.info(f"PDF extraction successful: {output_path}")
            self.signals.finished.emit(True, f"Text successfully extracted to: {output_path}")

        except Exception as e:
            logger.error(f"Error processing PDF: {str(e)}", exc_info=True)
            self.signals.finished.emit(False, f"Error processing PDF: {str(e)}")