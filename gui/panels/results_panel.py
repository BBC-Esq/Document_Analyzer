# gui/panels/results_panel.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QTextEdit

class ResultsPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        results_group = QGroupBox("Results")
        results_layout = QVBoxLayout(results_group)
        
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        
        results_layout.addWidget(self.result_text)
        layout.addWidget(results_group)
        
    def set_results(self, text):
        self.result_text.setText(text)
        
    def clear_results(self):
        self.result_text.clear()