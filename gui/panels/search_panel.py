# gui/panels/search_panel.py
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit
from PySide6.QtCore import Signal

class SearchPanel(QWidget):
    search_term_changed = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.setStyleSheet("border: 1px solid #008080;")  # Teal border
        
    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.addWidget(QLabel("Search Term:"))
        
        self.search_term_edit = QLineEdit()
        self.search_term_edit.textChanged.connect(self.search_term_changed)
        layout.addWidget(self.search_term_edit)
        
    def get_search_term(self):
        return self.search_term_edit.text()