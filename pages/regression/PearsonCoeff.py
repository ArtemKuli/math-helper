from PyQt5.QtWidgets import(
    QWidget, QVBoxLayout, QLabel
)
from PyQt5.QtCore import pyqtSignal
import numpy as np
from components.functions import DropArea, ExcelViewer, PlotCanvas

class PearsonCoeff(QWidget):
    goBack = pyqtSignal()
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        self.drop_area = DropArea()
        self.viewer = ExcelViewer(self.drop_area)
        self.viewer.columnsSelected.connect(self.ComputePearson)
        self.result_label = QLabel()
        self.plot = PlotCanvas(self)
             
        # layout.add
        layout.addWidget(self.drop_area)
        layout.addWidget(self.viewer)
        layout.addWidget(self.result_label)
        layout.addWidget(self.plot, stretch=1)
        
    def ComputePearson(self, col_indices):
        col1, col2 = col_indices
        table = self.viewer.table_widget
        
        col1_vals = []
        col2_vals = []
        
        for row in range(table.rowCount()):
            item1 = table.item(row, col1)
            item2 = table.item(row, col2)
            if not item1 or not item2:
                continue
            
            try:
                col1_vals.append(float(item1.text()))
                col2_vals.append(float(item2.text()))
            except ValueError:
                pass
        if len(col1_vals) < 2 or len(col2_vals) < 2:
            self.result_label.setText("Not enough valid numeri data in selected columns.")
            return
        
        corr = np.corrcoef(col1_vals, col2_vals)[0][1]
        
        abs_corr = abs(corr)
        if abs_corr >= 0.80:
            color = "green"
        elif abs_corr >= 0.50:
            color = "orange"
        else:
            color = "red"
            
        self.result_label.setStyleSheet(f"color: {color}; font-size: 16px;")
        self.result_label.setText(f"Pearson's Correlation: {corr:.4f}")
        
        x = np.array(col1_vals, dtype=float)
        y = np.array(col2_vals, dtype=float)
        
        self.plot.plot_scatter(col1_vals, col2_vals, corr)
        self.plot.draw()