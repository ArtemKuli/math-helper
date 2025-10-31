from PyQt5.QtWidgets import(
    QLabel 
)
from PyQt5.QtCore import Qt, pyqtSignal


class DropArea(QLabel):
    fileDropped = pyqtSignal(str)
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setText("Drag your .xls and similar files here")
        self.setAlignment(Qt.AlignCenter)
        self.resize(60, 60)
        self.setAcceptDrops(True)
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()
            
    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()
            
    def dropEvent(self, event):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            self.setText(f"Dropped: {file_path}")
            self.fileDropped.emit(file_path)
            
        event.acceptProposedAction()
        
    def set_size(self, width, height):
        self.resize(width, height)