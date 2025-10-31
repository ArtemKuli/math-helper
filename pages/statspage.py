from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QStackedWidget
)
from PyQt5.QtCore import pyqtSignal, Qt
from components.ui import TopBar
from components.buttons.create_button import create_button
from pages.regression.PearsonCoeff import PearsonCoeff
from pages.regression.standerrofest import StandErrOfEst

class StatsPage(QWidget):
    goBack = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        
        self.topbar = TopBar("Statistics Page")
        self.topbar.goBack.connect(self.goBack)
        
        self.stack = QStackedWidget()
        
        menu_page = QWidget()
        menu_layout = QVBoxLayout(menu_page)
        #buttons yippie
        btn_pearson = create_button("Pearson's Correlation") 
        btn_pearson.clicked.connect(lambda: self.show_page(1, "Pearson's Correlation Coefficient",
                                                           internal=True)) #increment number for each addition
        btn_standerrofest = create_button("Standard Error of Estimate")
        btn_standerrofest.clicked.connect(lambda: self.show_page(2, "Standard Error of Estimate",
                                                                 internal = True))
        
        #pages
        self.pearson_page = PearsonCoeff()
        self.standerrofest_page = StandErrOfEst()
        
        # layout.add 
        layout.addWidget(self.topbar)
        layout.addWidget(self.stack)

        #menu_layout.add
        menu_layout.addWidget(btn_pearson, alignment=Qt.AlignHCenter | Qt.AlignTop)
        menu_layout.addWidget(btn_standerrofest, alignment=Qt.AlignHCenter | Qt.AlignTop)
        menu_layout.addStretch()
        # stack.add
        self.stack.addWidget(menu_page)
        self.stack.addWidget(self.pearson_page)
        self.stack.addWidget(self.standerrofest_page)
    def show_page(self, index, title, internal=False):
        self.stack.setCurrentIndex(index)
        self.topbar.set_title(title)
        if internal:
            self.topbar.back_btn.goBack.disconnect()
            self.topbar.back_btn.goBack.connect(lambda: self.show_page(0, "Stats Page"))
        else:
            self.topbar.back_btn.goBack.connect(self.goBack.emit)
            
        
        