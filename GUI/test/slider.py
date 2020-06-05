import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QSlider
from PyQt5.QtCore import Qt


class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        mySlider = QSlider(Qt.Horizontal, self)
        mySlider.setGeometry(30, 40, 200, 30)
        mySlider.valueChanged[int].connect(self.changeValue)

        self.label = QtWidgets.QLabel(self)
        self.label.move(100,20)

        self.setGeometry(50, 50, 320, 200)
        self.setWindowTitle("Slider Example")
        self.show()

    def changeValue(self, value):
        self.label.setText(str(value+1))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
