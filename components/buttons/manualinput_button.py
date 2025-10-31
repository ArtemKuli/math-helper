from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTextEdit,
    QLabel
)

class ManualInput(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        self.x_input = QTextEdit()
        self.y_input = QTextEdit()
        
        
        
        #Layout.add
        layout.addWidget(QLabel("Enter X Values: 1, 2, 3 ...:"))
        layout.addWidget(self.x_input)
        layout.addWidget(QLabel("Enter Y Values: 1, 2, 3 ...:"))
        layout.addWidget(self.y_input)
        
    def get_values(self):
        x_vals = [float(v) for v in self.x_input.toPlainText().splitlines() if v.strip()]
        y_vals = [float(v) for v in self.y_input.toPlainText().splitlines() if v.strip()]
        return x_vals, y_vals