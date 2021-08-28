from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
''' tutorial 1: Basic gui setup'''

# when working with PyQt, the first thing we need to do when creating an app 
# or a GUI is to define an application.
# we'll define a function named window that does this for us 

def window():
    # this is where we always have to start off
    # passing in sys.argv sets up the configuration for the application
    # so that it knows what OS its running on
    app = QApplication(sys.argv)

    # next we have to create some kind of widget/window that were actually going
    # to show in our application (you can use QMainWindow or QWidget)
    win = QMainWindow()

    # set the size and title of our window by calling the setGeametry() method
    # the arguments are the x position, y position, width, and height
    # the x,y positions are where on your screen do you want the window to appear
    # the width and height is the size of the window
    xpos = 200
    ypos = 200
    width = 300
    height = 300
    win.setGeometry(xpos, ypos, width, height)
    
    # next were going to set a window title which is what you will see in the 
    # status bar of the application.
    win.setWindowTitle("Filtr")

    # Displaying something in the window 
    # in this case its just going to be a basic label
    # by passing in the window to the .QLabel() method were telling
    # the label where we want it to appear, which is on the window.
    label = QtWidgets.QLabel(win)
    # this is how we make the label say something
    label.setText("A Label")
    # now we can tell the label to appear in the window by using the move() method
    xlabel = 50
    ylabel = 50
    label.move(xlabel,ylabel)



    # now to show the window we have to use the .show() method along with
    # another line that basically makes sure that we exit when we close the window
    win.show()
    sys.exit(app.exec_())

window()

