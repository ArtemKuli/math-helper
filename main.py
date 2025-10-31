from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QPushButton, QStackedWidget, QLabel
)
from PyQt5.QtCore import Qt
from components.ui.topbar import TopBar
from pages.statspage import StatsPage

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Math Helper(Name may change)")
        self.resize(500, 500)
        
        main_layout = QVBoxLayout(self)
        
        # STACK
        self.stack = QStackedWidget()
        
        # PAGES
        menu_page = QWidget() #menu page aka this page
        menu_layout = QVBoxLayout(menu_page)
        
        
        # BUTTONS
        btn_stats = QPushButton("Statistics Page")
        btn_stats.setFixedWidth(250)
        btn_stats.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        menu_layout.addWidget(btn_stats, alignment=Qt.AlignHCenter | Qt.AlignTop)
        
        #pages
        stats_page = StatsPage()
        stats_page.goBack.connect(lambda: self.stack.setCurrentIndex(0))
    
        #main_layout.add
        main_layout.addWidget(self.stack)
        
        #menu_layout.add
        menu_layout.addStretch()
        
        #stack.add
        self.stack.addWidget(menu_page)
        self.stack.addWidget(stats_page) #index 1
        
        
if __name__ == "__main__":
    import sys
    import os
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication([])
    qss_path = os.path.join(os.path.dirname(__file__), "styles", "main.qss")
    
    with open(qss_path, "r") as f:
        app.setStyleSheet(f.read())

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())        