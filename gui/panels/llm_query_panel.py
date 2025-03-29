# gui/panels/llm_query_panel.py
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                              QLineEdit, QPushButton)
from PySide6.QtCore import Signal

class LlmQueryPanel(QWidget):
    query_clicked = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.setStyleSheet("border: 1px solid #800000;")  # Maroon border

    def setup_ui(self):
        layout = QVBoxLayout(self)

        question_layout = QHBoxLayout()
        question_layout.addWidget(QLabel("Ask a question about the text:"))

        self.question_edit = QLineEdit()
        question_layout.addWidget(self.question_edit)

        self.ask_button = QPushButton("Ask LLM")
        self.ask_button.clicked.connect(self._on_ask_clicked)
        question_layout.addWidget(self.ask_button)

        layout.addLayout(question_layout)

    def _on_ask_clicked(self):
        question = self.question_edit.text()
        if question:
            self.query_clicked.emit(question)

    def get_question(self):
        return self.question_edit.text()

    def clear_question(self):
        self.question_edit.clear()