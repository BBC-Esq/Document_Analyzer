import sys
from PySide6.QtWidgets import QApplication

from gui.app import DocumentProcessorApp
from utils.logging_config import setup_logger
from core.init_strategies import initialize_strategies, initialize_factories

logger = setup_logger(__name__)

def main():
    logger.info("Starting Document Processor application")

    initialize_strategies()
    initialize_factories()

    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = DocumentProcessorApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()