from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton,
    QLabel, QLineEdit, QTableWidget,
    QTableWidgetItem
)
from PyQt5.QtCore import pyqtSignal
import numpy as np
from components.functions import DropArea, ExcelViewer, PlotCanvas
from components.buttons.manualinput_button import ManualInput

class StandErrOfEst(QWidget):
    goBack = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        self.toggle_btn = QPushButton("Switch to Manual Input")
        self.toggle_btn.setCheckable(True)
        self.toggle_btn.toggled.connect(self.toggle_inputs)
        
        self.manual_input = ManualInput()
        self.manual_input.hide()
        
        self.compute_btn = QPushButton("Compute")
        self.compute_btn.clicked.connect(self.compute_manual_input)
        self.compute_btn.hide()
        
        self.drop_area = DropArea()
        self.viewer = ExcelViewer(self.drop_area)
        layout.addWidget(self.viewer)
        self.viewer.columnsSelected.connect(self.compute_standard_error)
        self.result_label = QLabel()
        
        self.round_input = QLineEdit()
        self.round_input.setPlaceholderText("Decimal places (e.g., 2)")
        self.round_input.setFixedWidth(120)
        
        self.update_table_btn = QPushButton("Update Table Rounding")
        self.update_table_btn.clicked.connect(self.update_table_rounding)
        
        self.tab = QTableWidget()
        self.plot = PlotCanvas(self)
        
        #layout.add
        layout.addWidget(self.toggle_btn)
        layout.addWidget(self.manual_input)
        layout.addWidget(self.compute_btn)
        layout.addWidget(self.drop_area)
        layout.addWidget(self.viewer)
        layout.addWidget(self.result_label)
        layout.addWidget(self.round_input)
        layout.addWidget(self.update_table_btn)
        layout.addWidget(self.tab)
        layout.addWidget(self.plot, stretch=1)
        
        # internal storage for rounding
        self.x_values   = []
        self.y_values   = []
        self.y_pred     = []
        self.y_diff     = []
        self.y_diff_sq  = []
        
    def compute_standard_error(self, col_indices):
        col1, col2 = col_indices
        table = self.viewer.table_widget
        
        col1_vals, col2_vals = [], []
        
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
            
        if len(col1_vals) < 2:
            self.result_label.setText("Not enough numeric data.")
            return
        
        x = np.array(col1_vals)
        y = np.array(col2_vals)
        
        
        b, a        = np.polyfit(x, y, 1)
        y_pred      = a + b * x
        y_diff      = y - y_pred
        y_diff_sq   = y_diff ** 2
        n           = len(y)
        standerr    = np.sqrt(np.sum(y_diff_sq) / (n - 2))
        
        self.x_values   = x
        self.y_values   = y
        self.y_pred     = y_pred
        self.y_diff     = y_diff
        self.y_diff_sq  = y_diff_sq
        
        decimals = 2
        self.tab.clear()
        self.tab.setRowCount(n)
        self.tab.setColumnCount(5)
        self.tab.setHorizontalHeaderLabels(['x', 'y', "y'", "y - y'", "(y - y')^2"])
        
        for i in range(n):
            self.tab.setItem(i, 0, QTableWidgetItem(f"{x[i]:.{decimals}f}"))
            self.tab.setItem(i, 1, QTableWidgetItem(f"{y[i]:.{decimals}f}"))
            self.tab.setItem(i, 2, QTableWidgetItem(f"{y_pred[i]:.{decimals}f}"))
            self.tab.setItem(i, 3, QTableWidgetItem(f"{y_diff[i]:.{decimals}f}"))
            self.tab.setItem(i, 4, QTableWidgetItem(f"{y_diff_sq[i]:.{decimals}f}"))

        self.result_label.setText(
            f"Regression line: y' = {a:.2f} + {b:.2f}x\n"
            f"Standard Error of Estimate: {standerr:.2f}"
        )
        
        self.tab.resizeColumnsToContents()
        self.tab.horizontalHeader().setStretchLastSection(True)
        
        self.plot.plot_regression(x, y, y_pred)
        
    def update_table_rounding(self):
        try:
            decimals = int(self.round_input.text())
        except ValueError:
            decimals = 2
            
        if len(self.x_values) == 0:
            return
        
        for i in range(len(self.x_values)):
            self.tab.setItem(i, 0, QTableWidgetItem(f"{self.x_values[i]:.{decimals}f}"))
            self.tab.setItem(i, 1, QTableWidgetItem(f"{self.y_values[i]:.{decimals}f}"))
            self.tab.setItem(i, 2, QTableWidgetItem(f"{self.y_pred[i]:.{decimals}f}"))
            self.tab.setItem(i, 3, QTableWidgetItem(f"{self.y_diff[i]:.{decimals}f}"))
            self.tab.setItem(i, 4, QTableWidgetItem(f"{self.y_diff_sq[i]:.{decimals}f}"))
            
    def toggle_inputs(self, checked):
        if checked:
            self.toggle_btn.setText("Switch to Excel Input")
            self.drop_area.hide()
            self.viewer.hide()
            self.manual_input.show()
            self.compute_btn.show()
            
        else:
            self.toggle_btn.setText("Switch to Manual Input")
            self.drop_area.show()
            self.viewer.show()
            self.manual_input.hide()
            self.compute_btn.hide()
            
    def compute_manual_input(self):
        try:
            x_text = self.manual_input.x_input.toPlainText().strip()
            y_text = self.manual_input.y_input.toPlainText().strip()
            
            x_vals = [float(v) for v in x_text.split(",") if v.strip()]
            y_vals = [float(v) for v in y_text.split(",") if v.strip()]
            
            if len(x_vals) != len(y_vals):
                self.result_label.setText("Error: X and Y must have Same Length.")
                return
            
            self.x_values = x_vals
            self.y_values = y_vals
            
            self.compute_standard_error()
            
        except ValueError:
            self.result_label.setText("Invalud input. Only numbers separated by commas.")