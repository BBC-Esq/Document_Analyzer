# gui/panels/document_selector_panel.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox
from PySide6.QtCore import Signal

class DocumentSelectorPanel(QWidget):
    document_selected = Signal(str)
    browse_clicked = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.setStyleSheet("border: 1px solid #0000FF;")  # Blue border
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        layout.addWidget(QLabel("Select Document File:"))
        file_layout = QHBoxLayout()
        
        self.document_path_edit = QLineEdit()
        browse_file_btn = QPushButton("Browse...")
        browse_file_btn.clicked.connect(self._on_browse_clicked)
        
        file_layout.addWidget(self.document_path_edit)
        file_layout.addWidget(browse_file_btn)
        layout.addLayout(file_layout)
        
    def _on_browse_clicked(self):
        self.browse_clicked.emit()
        
    def set_path(self, path):
        self.document_path_edit.setText(path)
        self.document_selected.emit(path)
        
    def get_path(self):
        return self.document_path_edit.text()