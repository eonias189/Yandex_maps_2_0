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
        self.map_mod = 'map'
        self.spnx, self.spny = 10, 10
        self.update_image()
        self.map_mod_c_b = [self.map, self.sat, self.sat_skl]
        for but in self.map_mod_c_b:
            but.clicked.connect(self.change_map_mod)
        self.map.setChecked(True)
        self.move_b = [self.up, self.right, self.left, self.down]
        for but in self.move_b:
            but.clicked.connect(self.move)

    def move(self):
        text = self.sender().text()
        x, y = self.x, self.y
        if text == '↑' and self.y < 85:
            self.y = min(self.y + self.spny / 2, 85)
        if text == '↓' and self.y > -85:
            self.y = max(self.y - self.spny / 2, -85)
        if text == '→' and self.x < 85:
            self.x = min(self.x + self.spnx / 2, 85)
        if text == '←' and self.x > -85:
            self.x = max(self.x - self.spnx / 2, -85)
        if x != self.x or y != self.y:
            self.update_image()

    def change_map_mod(self):
        mod_was = self.map_mod
        text = self.sender().text()
        if text == 'схема':
            self.map_mod = 'map'
        elif text == 'спутник':
            self.map_mod = 'sat'
        elif text == 'гибрид':
            self.map_mod = 'sat,skl'
        if mod_was != self.map_mod:
            self.update_image()

    def update_image(self):
        content = tools.get_image(f'{self.x},{self.y}', spn=f'{self.spnx},{self.spny}', type=self.map_mod)
        tools.save_image(self.image_name, content)
        self.pixmap = QPixmap(self.image_name)
        self.im.setPixmap(self.pixmap)

    def keyPressEvent(self, event):
        spnx, spny = self.spnx, self.spny
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
            if self.spnx >= 0.0002:
                self.spnx = self.spnx / self.scroll_speed
            if self.spny >= 0.0002:
                self.spny = self.spny / self.scroll_speed
        if spnx != self.spnx or spny != self.spny:
            self.update_image()

    def closeEvent(self, event):
        tools.delete_image(self.image_name)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec_())
