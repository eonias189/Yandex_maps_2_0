import sys

from PIL import Image
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel


class Window(QMainWindow):
    def __init__(self, filename, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.setWindowTitle('Яндекс карты 2.0')
        if filename:
            im = Image.open(filename)
            x, y = im.size
            im.close()
            self.resize(x, y)
            self.imLabel = QLabel(self)
            self.imLabel.move(0, 0)
            self.imLabel.resize(x, y)
            self.pixmap = QPixmap(filename)
            self.imLabel.setPixmap(self.pixmap)
        else:
            self.resize(600, 450)

    def closeEvent(self, event):
        if self.mainWindow:
            self.mainWindow.pictureIsShowing = False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window(None, None)
    ex.show()
    sys.exit(app.exec_())
