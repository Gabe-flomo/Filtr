import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QCheckBox


class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.cb = QCheckBox('Movie', self)
        self.cb.move(20, 20)

        self.cb2 = QCheckBox('Music', self)
        self.cb2.move(20, 40)
        self.cb2.toggle()

        self.label = QtWidgets.QLabel(self)
        self.label.setText("")
        xlabel = 100
        ylabel = 30
        self.label.move(xlabel, ylabel)
        
        self.cb.stateChanged.connect(lambda: self.checked(1, self.getState(1)))
        self.cb2.stateChanged.connect(lambda: self.checked(2, self.getState(2)))

        self.setGeometry(50, 50, 320, 200)
        self.setWindowTitle("Checkbox Example")
        self.show()

    def checked(self, box, state):
        print(f"CB{box} state {state}")
        if state:
            self.label.setText(f"Box {box} was clicked")
            self.label.move(100, 30)
        else:
            self.label.setText(f"Box {box} was unclicked")
            

    def getState(self, box):
        if box == 1:
            state = self.cb.isChecked()
        elif box == 2:
            state = self.cb2.isChecked()
        else:
            raise ValueError(f"{box} is not a valid checkbox")

        return state


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
