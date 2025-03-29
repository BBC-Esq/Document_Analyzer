# core/document/pdf.py (modified)
from typing import Optional, Any, Iterator, Union, List
from pathlib import Path

from langchain_community.docstore.document import Document
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.document_loaders.blob_loaders import Blob
from langchain_community.document_loaders.parsers import PyMuPDFParser
import pymupdf

from core.document.base import DocumentLoader
from utils.logging_config import setup_logger

logger = setup_logger(__name__)

class CustomPyMuPDFParser(PyMuPDFParser):
    def _lazy_parse(self, blob: Blob, text_kwargs: Optional[dict[str, Any]] = None) -> Iterator[Document]:
        with PyMuPDFParser._lock:
            with blob.as_bytes_io() as file_path:
                doc = pymupdf.open(stream=file_path, filetype="pdf") if blob.data else pymupdf.open(file_path)
                logger.debug(f"Opened PDF with {len(doc)} pages")

                full_content = []
                for page in doc:
                    page_content = self._get_page_content(doc, page, text_kwargs)
                    if page_content.strip():
                        full_content.append(f"[[page{page.number + 1}]]{page_content}")

                yield Document(
                    page_content="".join(full_content),
                    metadata=self._extract_metadata(doc, blob)
                )

class CustomPyMuPDFLoader(PyMuPDFLoader, DocumentLoader):
    def __init__(self, file_path: Union[str, Path], **kwargs: Any) -> None:
        super().__init__(file_path, **kwargs)
        self.parser = CustomPyMuPDFParser(
            text_kwargs=kwargs.get('text_kwargs'),
            extract_images=kwargs.get('extract_images', False)
        )
        logger.debug(f"CustomPyMuPDFLoader initialized for {file_path}")

def extract_text_from_pdf(pdf_path: Union[str, Path]) -> List[Document]:
    """
    Extract text from a PDF file using CustomPyMuPDFLoader.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        List of Document objects containing the extracted text
    """
    logger.info(f"Extracting text from PDF: {pdf_path}")
    loader_options = {
        "extract_images": False,
        "text_kwargs": {}
    }

    loader = CustomPyMuPDFLoader(pdf_path, **loader_options)
    documents = loader.load()

    logger.info(f"Extracted {len(documents)} documents from PDF")
    return documents