from PyQt5.QtWidgets import QPushButton

def create_button(text, width=250):
    btn = QPushButton(text)
    btn.setFixedWidth(width)
    return btn