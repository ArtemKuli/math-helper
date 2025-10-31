from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QSizePolicy
import numpy as np


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None):
        
        fig = Figure(figsize = (5, 4))
        self.ax = fig.add_subplot(111)
        
        super().__init__(fig)
        self.setParent(parent)
        self.fig = fig
        
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.updateGeometry()
        
        self.cid = self.mpl_connect("button_press_event", self.on_click)
        self.last_points = None
        
        #colorize dark
        self.fig.patch.set_facecolor('#2e2e2e')
        self.ax.set_facecolor('#2e2e2e')
        self.ax.tick_params(colors='white')
        self.ax.spines['bottom'].set_color('white')
        self.ax.spines['top'].set_color('white')
        self.ax.spines['left'].set_color('white')
        self.ax.spines['right'].set_color('white')
        self.ax.xaxis.label.set_color('white')
        self.ax.yaxis.label.set_color('white')
        self.ax.title.set_color('white')
        
    def plot_scatter(self, x, y, r_value):
        self.ax.clear()
        self.apply_dark_style()
        self.last_points = (np.array(x), np.array(y))
        self.ax.grid(True, color="#555555", linestyle="--", linewidth=0.5)
        self.restore_instructions_text()
        self.ax.scatter(x,y)
        
        if len(x) > 1:
            m, b = np.polyfit(x, y, 1)
            reg_x = np.array([min(x), max(x)])
            reg_y = m * reg_x + b
            self.ax.plot(reg_x, reg_y)
            
        self.ax.set_title(f"Pearson r = {r_value:.4f}")
        self.ax.set_xlabel("Column X")
        self.ax.set_ylabel("Column Y")
        
        self.ax.relim()
        self.ax.autoscale()
        self.fig.tight_layout()
        
        self.draw()
        
    def plot_regression(self, x, y, y_pred, error_threshold=None):
        
        self.ax.clear()
        self.apply_dark_style()
        self.last_points = (np.array(x), np.array(y))
        self.ax.grid(True, color="#555555", linestyle="--", linewidth=0.5)
        self.restore_instructions_text()
        residuals = y - y_pred
        # Optional error coloring
        if error_threshold is None:
            error_threshold = np.std(residuals)
            
            
        colors = ['red' if e > error_threshold else 'lime' for e in residuals]

        self.ax.scatter(x, y, color='cyan', label="Data")
        
        self.ax.plot(x, y_pred,'-' ,color='magenta', label="Regression Line")
        
        for xi, yi, ypi in zip(x, y, y_pred):
            self.ax.plot([xi, xi], [ypi, yi], color='yellow', linewidth=1)
        
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.legend()

        
        self.last_points = (np.array(x), np.array(y))
        self.ax.grid(True, color="#555555", linestyle="--", linewidth=0.5)
        self.fig.tight_layout()
        self.draw()
        
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.fig.tight_layout()
        self.draw()
        
    def apply_dark_style(self):
        
        self.fig.patch.set_facecolor('#2e2e2e')
        self.ax.set_facecolor('#2e2e2e')
        self.ax.tick_params(colors='white')
        self.ax.spines['bottom'].set_color('white')
        self.ax.spines['top'].set_color('white')
        self.ax.spines['left'].set_color('white')
        self.ax.spines['right'].set_color('white')
        self.ax.xaxis.label.set_color('white')
        self.ax.yaxis.label.set_color('white')
        self.ax.title.set_color('white')
    
    def on_click(self, event):
        if event.inaxes != self.ax or self.last_points is None:
            return
        
        x_click = event.xdata
        y_click = event.ydata
        
        x, y = self.last_points
        
        distances = (x - x_click) **2 + (y - y_click) **2
        idx = np.argmin(distances)
        
        nearest_x = x[idx]
        nearest_y = y[idx]
        
        if hasattr(self, "annotation"):
            self.annotation.remove()
            
        self.annotation = self.ax.annotate(
            f"({nearest_x:.2f}, {nearest_y:.2f})",
            xy = (nearest_x, nearest_y),
            xytext=(10, 10),
            textcoords="offset points",
            color="white",
            fontsize=9,
            bbox=dict(boxstyle="round,pad=0.3", fc="#444444", ec="white", alpha=0.8)
        )
        
        if hasattr(self, "highlight"):
            self.highlight.remove()
            
        self.highlight = self.ax.scatter(
            [nearest_x], [nearest_y],
            color="yellow",
            s=80,
            zorder=10
        )
        
        self.draw()
        
    def restore_instructions_text(self):
        self.instruction = self.ax.text(
            0.02, 0.98,
            "click data points\n to show coordinates",
            transform=self.ax.transAxes,
            va='top',
            fontsize=10,
            color='gray'
        )