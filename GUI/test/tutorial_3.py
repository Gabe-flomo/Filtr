# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!
''' Events '''

from PyQt5 import QtCore, QtGui, QtWidgets

`Look the through the code and make comments so that you understand what youre doing


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(110, 110, 401, 291))

        font = QtGui.QFont()
        font.setFamily("Fira Code Retina")
        font.setPointSize(36)
        self.label.setFont(font)
        self.label.setObjectName("label")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuedit = QtWidgets.QMenu(self.menubar)
        self.menuedit.setObjectName("menuedit")

        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")

        MainWindow.setStatusBar(self.statusbar)
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actioncopy = QtWidgets.QAction(MainWindow)
        self.actioncopy.setObjectName("actioncopy")
        self.actionpaste = QtWidgets.QAction(MainWindow)
        self.actionpaste.setObjectName("actionpaste")
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionSave)
        self.menuedit.addAction(self.actioncopy)
        self.menuedit.addAction(self.actionpaste)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuedit.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Triggered makes it so that you can do the action with the shortcut (like ctrl+c)
        # also by using a lambda function to call the function we want to use, were able to pass parameters to 
        # that function whereas before we couldnt pass in the arguments because we were only passing in the name 
        # of the function
        self.actionNew.triggered.connect(lambda: self.click("New was clicked"))
        self.actionSave.triggered.connect(lambda: self.click("Save was clicked"))
        self.actioncopy.triggered.connect(lambda: self.click("Copy was clicked"))
        self.actionpaste.triggered.connect(lambda: self.click("Paste was clicked"))


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "TextLabel"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuedit.setTitle(_translate("MainWindow", "edit"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionNew.setStatusTip(_translate("MainWindow", "Create a new file"))
        self.actionNew.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setStatusTip(_translate("MainWindow", "Save a file"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actioncopy.setText(_translate("MainWindow", "copy"))
        self.actioncopy.setStatusTip(_translate("MainWindow", "copy contents"))
        self.actioncopy.setShortcut(_translate("MainWindow", "Ctrl+C"))
        self.actionpaste.setText(_translate("MainWindow", "paste"))
        self.actionpaste.setStatusTip(_translate("MainWindow", "paste content"))

    def click(self, text):
        self.label.setText(text)
        self.label.adjustSize()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
