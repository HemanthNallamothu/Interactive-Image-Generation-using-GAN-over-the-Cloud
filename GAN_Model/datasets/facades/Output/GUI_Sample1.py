import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Interactive Image Processing using Deep Learning and Neural Networks")
        self.setGeometry(100, 100, 800, 600)
        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)

        self.begin = QPoint()
        self.end = QPoint()
        self.rectangles = []

        mainMenu = self.menuBar()

        fileMenu = mainMenu.addMenu("File")

        resultMenu = mainMenu.addMenu("Results")

        saveAction = QAction("Save", self)
        saveAction.setShortcut("Ctrl+S")
        fileMenu.addAction(saveAction)
        saveAction.triggered.connect(self.save)

        resultAction = QAction("Generate Images", self)
        resultAction.setShortcut("Ctrl+R")
        resultMenu.addAction(resultAction)

        clearAction = QAction("Clear", self)
        clearAction.setShortcut("Ctrl+C")
        fileMenu.addAction(clearAction)
        clearAction.triggered.connect(self.clear)

    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setPen(QPen(Qt.red, 10, Qt.SolidLine))
        qp.setBrush(QBrush(Qt.yellow, Qt.SolidPattern))
     
        for rectangle in self.rectangles:
            qp.drawRect(rectangle)

        if not self.begin.isNull() and not self.end.isNull():
            qp.drawRect(QRect(self.begin, self.end).normalized())
        self.update()

    def mousePressEvent(self, event):
        self.begin = self.end = event.pos()
        self.update()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        
        self.end = event.pos()
        self.update()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        r = QRect(self.begin, self.end).normalized()
        self.rectangles.append(r)
        self.begin = self.end = QPoint()
        self.update()
        super().mouseReleaseEvent(event)

    def save(self):
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "JPEG(*.jpg *.jpeg);;All Files(*.*) ")
        if filePath == "":
            return
        self.image.save(filePath)

    def clear(self):
        # make the whole canvas white
        self.image.fill(Qt.white)
        # update
        self.update()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())
