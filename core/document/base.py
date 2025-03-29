from abc import ABC, abstractmethod
from typing import List, Any, Optional
from langchain_community.docstore.document import Document
from utils.logging_config import setup_logger

logger = setup_logger(__name__)

class DocumentLoader(ABC):
    """
    Abstract base class for document loaders.
    
    This class defines the interface that all document loaders must implement.
    """
    
    @abstractmethod
    def load(self) -> List[Document]:
        """
        Load document and return its content as a list of Document objects.
        
        Returns:
            List of Document objects containing the text content.
        """
        pass

# This base class will be extended for different document types (PDF, DOCX, etc.)