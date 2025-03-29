# gui/app.py
import os
import sys
from pathlib import Path
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QSplitter, QFileDialog, QMessageBox
from PySide6.QtCore import Qt

from gui.panels.file_browser_panel import FileBrowserPanel
from gui.panels.document_selector_panel import DocumentSelectorPanel
from gui.panels.search_panel import SearchPanel
from gui.panels.action_panel import ActionPanel
from gui.panels.progress_panel import ProgressPanel
from gui.panels.results_panel import ResultsPanel

from core.reporting.basic import create_report
from core.document.factory import DocumentProcessorFactory
from workers.document_workers import PdfExtractWorker
from workers.analysis_workers import TextAnalyzeWorker
from utils.logging_config import setup_logger

logger = setup_logger(__name__)

class DocumentProcessorApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.input_file = ""

        self.base_output_dir = os.path.join(os.getcwd(), "extracted_texts")
        os.makedirs(self.base_output_dir, exist_ok=True)

        self.output_dir = self.base_output_dir
        self.selected_txt_file = ""
        self.selected_txt_path = ""
        self.search_results = {}

        self.setWindowTitle("Document Processor")
        self.setGeometry(100, 100, 1000, 700)

        self.init_ui()

        logger.info("DocumentProcessorApp initialized")

    def init_ui(self):
        # Create main layout
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)

        # Initialize panels
        self.file_browser = FileBrowserPanel()
        self.file_browser.set_directory(self.output_dir)
        self.file_browser.file_selected.connect(self.on_txt_select)

        # Create right side container
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        self.document_selector = DocumentSelectorPanel()
        self.document_selector.browse_clicked.connect(self.browse_document)

        self.search_panel = SearchPanel()

        self.action_panel = ActionPanel()
        self.action_panel.extract_clicked.connect(self.process_document)
        self.action_panel.analyze_clicked.connect(self.analyze_document)
        self.action_panel.report_clicked.connect(self.generate_report)

        self.progress_panel = ProgressPanel()

        self.results_panel = ResultsPanel()

        # Add panels to right layout
        right_layout.addWidget(self.document_selector)
        right_layout.addWidget(self.search_panel)
        right_layout.addWidget(self.action_panel)
        right_layout.addWidget(self.progress_panel)
        right_layout.addWidget(self.results_panel)

        # Add panels to splitter
        splitter.addWidget(self.file_browser)
        splitter.addWidget(right_panel)
        splitter.setSizes([300, 600])

        self.setCentralWidget(main_widget)
        logger.debug("UI initialized")

    def browse_document(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Document File",
            "",
            "Document files (*.pdf);;All Files (*.*)"  # Can be expanded later
        )
        if file_path:
            self.input_file = file_path
            self.document_selector.set_path(file_path)
            logger.info(f"Selected document: {file_path}")

    def on_txt_select(self, filename, filepath):
        self.selected_txt_file = filename
        self.selected_txt_path = filepath
        self.progress_panel.set_status(f"Selected: {self.selected_txt_file}")
        logger.debug(f"Selected text file: {self.selected_txt_file}")

    def update_status(self, message):
        self.progress_panel.set_status(message)

    def process_document(self):
        self.input_file = self.document_selector.get_path()

        if not self.input_file:
            QMessageBox.critical(self, "Error", "Please select a PDF file")
            logger.warning("No PDF file selected")
            return

        if not os.path.exists(self.input_file):
            QMessageBox.critical(self, "Error", "Selected PDF file does not exist")
            logger.error(f"PDF file does not exist: {self.input_file}")
            return

        if not os.path.exists(self.output_dir):
            try:
                os.makedirs(self.output_dir)
                logger.info(f"Created output directory: {self.output_dir}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not create output directory: {str(e)}")
                logger.error(f"Could not create output directory: {str(e)}")
                return

        self.progress_panel.set_progress(0, 0)
        self.update_status("Processing PDF...")
        self.results_panel.clear_results()

        logger.info(f"Starting PDF extraction: {self.input_file}")
        self.extract_worker = DocumentProcessorFactory.create_processor(self.input_file, self.output_dir)
        self.extract_worker.signals.finished.connect(self.complete_extraction)
        self.extract_worker.start()

    def analyze_document(self):
        search_term = self.search_panel.get_search_term()

        if not search_term:
            QMessageBox.critical(self, "Error", "Please enter a search term")
            logger.warning("No search term entered")
            return

        if not self.selected_txt_file:
            QMessageBox.critical(self, "Error", "Please select a text file to analyze")
            logger.warning("No text file selected for analysis")
            return

        try:
            file_path = self.selected_txt_path
            if not os.path.exists(file_path):
                QMessageBox.critical(self, "Error", f"File not found: {file_path}")
                logger.error(f"File not found: {file_path}")
                return

            self.progress_panel.set_progress(0, 0)
            self.update_status(f"Analyzing {self.selected_txt_file}...")
            self.results_panel.clear_results()

            logger.info(f"Starting text analysis of {file_path} with term '{search_term}'")
            self.analyze_worker = TextAnalyzeWorker(file_path, search_term)
            self.analyze_worker.signals.finished.connect(self.complete_analysis)
            self.analyze_worker.start()

        except Exception as e:
            self.update_status(f"Error: {str(e)}")
            self.progress_panel.set_progress(0)
            logger.error(f"Error during analysis: {str(e)}")

    def complete_analysis(self, success, message):
        self.progress_panel.set_progress(100 if success else 0)

        self.update_status("Analysis complete" if success else "Analysis failed")
        self.results_panel.set_results(message)

        if success:
            self.search_results = self.analyze_worker.results
            logger.info("Analysis completed successfully")
        else:
            self.search_results = {}
            QMessageBox.critical(self, "Error", message)
            logger.error(f"Analysis failed: {message}")

    def generate_report(self):
        if not self.search_results:
            QMessageBox.critical(self, "Error", "No search results available. Run an analysis first.")
            logger.warning("Attempted to create report with no results")
            return

        try:
            logger.info("Generating report")
            success = create_report(self.search_results)
            if success:
                self.update_status("Report created and opened")
                logger.info("Report created successfully")
            else:
                self.update_status("Report creation failed")
                logger.error("Report creation failed")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to create report: {str(e)}")
            self.update_status("Report creation failed")
            logger.error(f"Error creating report: {str(e)}")

    def complete_extraction(self, success, message):
        self.progress_panel.set_progress(100 if success else 0)
        
        self.update_status(message)
        self.results_panel.set_results(message)

        if success:
            QMessageBox.information(self, "Success", message)
            logger.info("PDF extraction completed successfully")
        else:
            QMessageBox.critical(self, "Error", message)
            logger.error(f"PDF extraction failed: {message}")