# gui/panels/progress_panel.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QProgressBar, QLabel
from PySide6.QtCore import Signal

class ProgressPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.setStyleSheet("border: 1px solid #800080;")  # Purple border

    def setup_ui(self):
        layout = QVBoxLayout(self)

        self.progress = QProgressBar()
        self.status_label = QLabel("Ready to extract document text")

        self.status_label.setWordWrap(True)
        
        layout.addWidget(self.progress)
        layout.addWidget(self.status_label)
        
    def set_progress(self, value, maximum=100):
        if maximum == 0:
            self.progress.setRange(0, 0)
        else:
            self.progress.setRange(0, maximum)
            self.progress.setValue(value)
            
    def set_status(self, message):
        self.status_label.setText(message)