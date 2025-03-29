# gui/panels/action_panel.py
from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PySide6.QtCore import Signal

class ActionPanel(QWidget):
    extract_clicked = Signal()
    analyze_clicked = Signal()
    report_clicked = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.setStyleSheet("border: 1px solid #FF0000;")  # Red border
        
    def setup_ui(self):
        layout = QHBoxLayout(self)
        
        extract_button = QPushButton("Extract Text")
        extract_button.clicked.connect(self.extract_clicked)
        
        analyze_button = QPushButton("Analyze Document")
        analyze_button.clicked.connect(self.analyze_clicked)
        
        report_button = QPushButton("Create Report")
        report_button.clicked.connect(self.report_clicked)
        
        layout.addWidget(extract_button)
        layout.addWidget(analyze_button)
        layout.addWidget(report_button)