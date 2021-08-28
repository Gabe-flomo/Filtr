# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'popup.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!
''' QMessageBox and Popup Windows '''

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.button = QtWidgets.QPushButton(self.centralwidget)
        self.button.setGeometry(QtCore.QRect(220, 160, 331, 191))
        self.button.setObjectName("button")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.button.clicked.connect(self.show_pop)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.button.setText(_translate("MainWindow", "Show Popup"))

    def show_pop(self):
        msg = QMessageBox()
        msg.setWindowTitle("Tutorial on pyqt5")
        msg.setText("Main text!")

        # setting an icon
        icon = QMessageBox.Information
        msg.setIcon(icon)

        # getting input from the message box
        msg.setStandardButtons(QMessageBox.Cancel | QMessageBox.Retry | QMessageBox.Ignore)
        msg.setDefaultButton(QMessageBox.Ignore)

        # setting informative text
        msg.setInformativeText("Info text onna gang")

        msg.setDetailedText("details")

        msg.buttonClicked.connect(self.popup_button)
        
        x = msg.exec_()

    def popup_button(self, i):
        print(i.text())
        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
