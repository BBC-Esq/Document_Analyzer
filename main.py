import sys
import argparse
import logging
from PySide6.QtWidgets import QApplication

from gui.app import DocumentProcessorApp
from utils.logging_config import configure_logging
from core.init_strategies import initialize_strategies, initialize_factories

def main():
    parser = argparse.ArgumentParser(description='Document Processor Application')
    parser.add_argument(
        '--log-level',
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='Set the logging level (default: INFO)'
    )
    args = parser.parse_args()

    log_level = getattr(logging, args.log_level)

    configure_logging(log_level)

    logger = logging.getLogger(__name__)
    logger.info(f"Starting Document Processor application with log level: {args.log_level}")

    initialize_strategies()
    initialize_factories()

    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = DocumentProcessorApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
