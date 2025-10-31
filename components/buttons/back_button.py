from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import pyqtSignal

class back_button(QPushButton):
    goBack = pyqtSignal()
    def __init__(self, text="Back"):
        super().__init__(text)
        self.setFixedWidth(100)
        self.clicked.connect(self.emit_back)
        
    def emit_back(self):
        self.goBack.emit()