import sys

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow

import tools


class Window(QMainWindow):
    def __init__(self, image_name='will_be_deleted.png', ll=None):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.image_name = image_name
        self.scroll_speed = 2
        if ll is None:
            print('введите координаты (через запятую,без пробела)')
            ll = input()
        self.x, self.y = map(float, ll.split(','))
        self.spnx, self.spny = 10, 10
        self.update_image()

    def update_image(self):
        content = tools.get_image(f'{self.x},{self.y}', spn=f'{self.spnx},{self.spny}')
        tools.save_image(self.image_name, content)
        self.pixmap = QPixmap(self.image_name)
        self.im.setPixmap(self.pixmap)

    def keyPressEvent(self, event):
        spnx, spny, x, y = self.spnx, self.spny, self.x, self.y
        if event.key() == Qt.Key_PageDown:
            if self.spnx == 90:
                pass
            elif (90 // self.scroll_speed) < self.spnx < 90:
                self.spnx = 90
            else:
                self.spnx = self.scroll_speed * self.spnx
            if self.spny == 90:
                pass
            elif (90 // self.scroll_speed) < self.spny < 90:
                self.spny = 90
            else:
                self.spny = self.scroll_speed * self.spny
        if event.key() == Qt.Key_PageUp:
            self.spnx = self.spnx / self.scroll_speed
            self.spny = self.spny / self.scroll_speed
        if event.key() == Qt.Key_Up and self.y < 85:
            self.y = min(self.y + self.spny / 2, 85)
        if event.key() == Qt.Key_Down and self.y > -85:
            self.y = max(self.y - self.spny / 2, -85)
        if event.key() == Qt.Key_Right and self.x < 85:
            self.x = min(self.x + self.spnx / 2, 85)
        if event.key() == Qt.Key_Left and self.x > -85:
            self.x = max(self.x - self.spnx / 2, -85)
        if spnx != self.spnx or spny != self.spny or x != self.x or y != self.y:
            self.update_image()

    def closeEvent(self, event):
        tools.delete_image(self.image_name)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec_())
