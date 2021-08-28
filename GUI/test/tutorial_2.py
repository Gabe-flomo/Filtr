from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
''' tutorial 2: Buttons and Events'''

def click():
    print("Clicked")

def wind():
    
    app = QApplication(sys.argv)
    win = QMainWindow()

    xpos = 200
    ypos = 200
    width = 300
    height = 300
    

    label = QtWidgets.QLabel(win)
    label.setText("A Label")
    xlabel = 50
    ylabel = 50
    label.move(xlabel,ylabel)

    # adding a button is similar to adding a label
    # we have to first create a button object and make it appear
    # on the window.
    # then we can set the text that the button displays with the setText() method
    b1 = QtWidgets.QPushButton(win)
    b1.setText("Button")

    # currently this button does nothing, so were going to write a function (on line 6)
    # that will be triggered whenever this button is pressed.
    # to have the function trigger when we press the button, we pass the function
    # without brackets as a parameter to the connect() method
    b1.clicked.connect(click)


    win.show()
    sys.exit(app.exec_())


'''
right now all our button does is just print "clicked" to the screen, which isnt
very useful at all. So instead lets make our function change the contents of our label
but our click function doesnt have access to any of the code that we wrote in the window function.
So were going to put all of our code into a class so that all of the functions cal talk to each other.
'''

# were going to inherit from QMainWindow so that our class
# can use all of the properties that QMainWindow has.
class MyWindow(QMainWindow):
    def __init__(self):
        # calls the parent (QMainWindow) constructor and sets everything up
        # so we can use the properties in our class
        super(MyWindow, self).__init__()
        self.xpos = 200     # set the window x position on the screen
        self.ypos = 200     # set the window y position on the screen
        self.width = 1000    # set the windows screen width
        self.height = 500   # set the windows screen height
        self.setGeometry(self.xpos, self.ypos, self.width, self.height)
        self.setWindowTitle("Filtr")
        self.initUI()
    
    def initUI(self):
        '''
        Sets up the window

        sidenote: since we are inheriting from the QMainWindow class, which is the
        object we used to set up the window before putting it into the class (win = QMainWindow)
        everywhere that had a win or win.method() can be replaced with self since MyWindow
        is now the window object.
        
        This pretty much makes it so that if we want to change properties of the window
        we can do that by just using self then the name of the method (for example self.setGeometry())
        '''        
        # we make the label and button class variables by adding
        # self so that those functions can be accessed from anywhere in our class.
        self.label = QtWidgets.QLabel(self)
        self.label.setText("A Label")
        xlabel = 500
        ylabel = 250
        self.label.move(xlabel, ylabel)
        
        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setText("Button")
        self.b1.clicked.connect(self.click)

    def click(self):
        ''' changes the label text'''
        self.label.setText("Button pressed")
        self.update()

    def update(self):
        '''
        Utility function that is called every time we make a change to the window 
        that for now only adjusts the size of the label button width
        '''
        self.label.adjustSize()

  
def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())

window()