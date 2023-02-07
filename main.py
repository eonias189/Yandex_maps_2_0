import sys

from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow

import tools


class Window(QMainWindow):
    def __init__(self, image_name='will_be_deleted.png', ll=None):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.image_name = image_name
        if ll is None:
            print('введите координаты (через запятую,без пробела)')
            ll = input()
        self.ll = ll
        self.spn = '90,90'
        self.update_image()

    def update_image(self):
        content = tools.get_image(self.ll, spn=self.spn)
        tools.save_image(self.image_name, content)
        self.pixmap = QPixmap(self.image_name)
        self.im.setPixmap(self.pixmap)

    def closeEvent(self, event):
        tools.delete_image(self.image_name)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec_())
