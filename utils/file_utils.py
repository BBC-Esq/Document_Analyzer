# utils/file_utils.py
import os
import hashlib
from pathlib import Path
from typing import Union
from datetime import datetime
from utils.logging_config import setup_logger

logger = setup_logger(__name__)

def get_file_hash(file_path: Union[str, Path]) -> str:
    """
    Calculate MD5 hash of a file.
    
    Args:
        file_path: Path to the file
        
    Returns:
        MD5 hash of the file
    """
    logger.debug(f"Calculating hash for file: {file_path}")
    with open(file_path, 'rb') as f:
        file_hash = hashlib.md5(f.read()).hexdigest()
    return file_hash

def get_unique_filename(original_path: Union[str, Path], output_dir: Union[str, Path]) -> Path:
    """
    Generate a unique filename based on the original file's name and hash.
    
    Args:
        original_path: Path to the original file
        output_dir: Base output directory
    
    Returns:
        Path object for the unique output file (no extension)
    """
    original_path = Path(original_path)
    original_filename = original_path.stem

    file_hash = get_file_hash(original_path)
    logger.debug(f"File hash for {original_path}: {file_hash[:10]}")

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    unique_name = f"{original_filename}_{file_hash[:10]}"
    return Path(output_dir) / unique_name