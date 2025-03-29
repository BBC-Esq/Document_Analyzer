# gui/panels/file_browser_panel.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QListView, QFileSystemModel
from PySide6.QtCore import Qt, QDir, Signal

class FileBrowserPanel(QWidget):
    file_selected = Signal(str, str)  # Emits filename and full path
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.setStyleSheet("border: 1px solid #00FF00;")  # Green border
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        self.setLayout(layout)
        
        txt_list_frame = QGroupBox("Text Files")
        txt_list_layout = QVBoxLayout(txt_list_frame)
        
        self.file_model = QFileSystemModel()
        self.file_model.setFilter(QDir.Files)
        self.file_model.setNameFilters(["*.txt"])
        self.file_model.setNameFilterDisables(False)
        
        self.txt_listbox = QListView()
        self.txt_listbox.setModel(self.file_model)
        self.txt_listbox.clicked.connect(self._on_file_select)
        
        txt_list_layout.addWidget(self.txt_listbox)
        layout.addWidget(txt_list_frame)
        
    def set_directory(self, directory):
        self.file_model.setRootPath(directory)
        self.txt_listbox.setRootIndex(self.file_model.index(directory))
        
    def _on_file_select(self, index):
        filename = self.file_model.fileName(index)
        filepath = self.file_model.filePath(index)
        self.file_selected.emit(filename, filepath)