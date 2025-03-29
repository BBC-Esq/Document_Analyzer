# core/analysis/text_splitter.py
from typing import List
from utils.logging_config import setup_logger

logger = setup_logger(__name__)

def split_text(text: str, chunk_size: int = 4000, overlap: int = 200) -> List[str]:
    """
    Split text into overlapping chunks based on character count.

    Args:
        text: Text to split into chunks
        chunk_size: Size of each chunk in characters
        overlap: Number of characters to overlap between chunks

    Returns:
        List of text chunks
    """
    logger.info(f"Splitting text of length {len(text)} into chunks of {chunk_size} characters with {overlap} overlap")

    if not text:
        logger.warning("Empty text provided to split_text")
        return []

    if len(text) <= chunk_size:
        logger.info("Text smaller than chunk size, returning as single chunk")
        return [text]

    chunks = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))

        chunk = text[start:end]
        chunks.append(chunk)

        start += chunk_size - overlap

        start = max(start, 0)

        if start >= len(text):
            break

    logger.info(f"Split text into {len(chunks)} chunks")
    return chunks