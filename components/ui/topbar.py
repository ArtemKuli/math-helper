from PyQt5.QtWidgets import (
    QHBoxLayout, QWidget, QLabel
)
from PyQt5.QtCore import Qt, pyqtSignal
from components.buttons.back_button import back_button


class TopBar(QWidget):
    goBack = pyqtSignal()
    def __init__(self, title="Page Title", parent=None):
        super().__init__()
        
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)
        self.setLayout(layout)
        
        self.back_btn = back_button()
        self.back_btn.goBack.connect(self.goBack)
        
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold;")

        
        ## layout.add 
        layout.addWidget(self.back_btn)
        layout.addWidget(self.title_label, alignment=Qt.AlignCenter)
        layout.addStretch()
    
    def set_title(self, text):
        self.title_label.setText(text)