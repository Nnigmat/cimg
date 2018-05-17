import sys
from PyQt5.QtWidgets import QMainWindow, QToolTip,  QApplication, QWidget, QPushButton
from PyQt5 import QtGui
from PyQt5 import QtCore


class drawColors(QWidget):

    # All buttons with color that will be printed into the screen
    buttons = []

    # Using as stack for deleted buttons to return them back if user want
    deletedButtons = []

    def __init__(self, colors, n):
        super().__init__()

        self.setFocusPolicy(QtCore.Qt.NoFocus)
        # Store colors and n to drawColors's object
        self.colors = colors
        self.initN = n
        self.n = n

        # Do method initUI
        self.initUI()	

    def initUI(self):
        # Start positions and sizes
        self.btnWidth = 50
        self.btnHeight = 600
        self.btnStartWidthPosition = 25
        self.btnStartHeightPosition = 25
        self.windowWidth = self.btnStartWidthPosition*2 + self.btnWidth * self.n
        self.windowHeight = self.btnHeight + self.btnStartHeightPosition*4

        # App initialization
        self.resize(self.windowWidth, self.windowHeight)
        self.move(300, 300)
        self.setWindowTitle('Cimg')

        # Add buttons to the screen 
        for i in range(self.n):
            el = self.colors[i]
            color = '' + str(hex(el[0]))[2:].upper() + str(hex(el[1]))[2:].upper() + str(hex(el[2]))[2:].upper() 
            btn = QPushButton('   ', self)
            self.buttons.append(btn)
            btn.resize(self.btnWidth, self.btnHeight)
            btn.move(self.btnWidth*i + self.btnStartWidthPosition, self.btnStartHeightPosition)
            btn.setStyleSheet('QPushButton{ background-color: #' + color + ' } QPushButton:active { background-color: #' + color + '}') 
            btn.clicked.connect(self.buttonClicked)
            btn.setDefault(False)
            btn.setAutoDefault(False)

        # Add button Undo and connect it to self
        btn = QPushButton('Undo', self)      
        btn.move(self.btnStartWidthPosition, self.btnHeight + self.btnStartHeightPosition * 2) 
        btn.clicked.connect(self.undo)

        # Start current QWidget
        self.show()
    
   
    def undo(self):
        # If all buttons on the screen do nothing 
        if len(self.deletedButtons) == 0:
            return
          
        # Else get the last one operation
        # lastEl store tuple (el, index)
        # el - QPushButton object, index - from where from self.buttons it was taken
        lastEl = self.deletedButtons.pop()
        self.buttons.insert(lastEl[1], lastEl[0])   

        # Increase self.n which denotes current number of color in the screen
        # If self.n >= self.initN then we just make it equals to initN which denotes starter number of colors
        self.n += 1 if self.n < self.initN else self.initN      

        # Make returned button visible
        lastEl[0].setVisible(True) 
 
        # Recalculate width of buttons, because we return one, then width of each button will decrease
        self.btnWidth = int((self.windowWidth - self.btnStartWidthPosition*2)/self.n) if self.n != 0 else 1

        # Go through all buttons in screen, resize them and move 
        for i in range(self.n-1):
            self.buttons[i].resize(self.btnWidth, self.btnHeight)
            self.buttons[i].move(self.btnWidth*i + self.btnStartWidthPosition, self.btnStartHeightPosition)

        # If exist the last one element then we resize it to the border, because when we've been recalculting them 
        # we round them to integer and lost a little pixels and at each time tail of the colors will be a little 
        # not at exact place. It will always move.
        if self.n - 1 >= 0:
            self.buttons[self.n-1].resize(self.windowWidth - self.btnStartWidthPosition*2-self.btnWidth*(self.n-1), self.btnHeight)
            self.buttons[self.n-1].move(self.btnWidth*(self.n-1) + self.btnStartWidthPosition, self.btnStartHeightPosition)


    def buttonClicked(self):
        # Get button that have been clicked
        sender = self.sender()
        
        # Delete this button and decrease n
        for i in range(self.n):
            if self.buttons[i] == sender:
                self.deletedButtons.append((self.buttons.pop(i), i)) 
                self.n -= 1 
                break
       
        # Make button invisible if user will want to come back 
        sender.setVisible(False)        


        # Code for deleting, left it for myself sender.setParent(QWidget())

        # Change btnWidth, because we've decreased number of buttons on screen
        self.btnWidth = int((self.windowWidth - self.btnStartWidthPosition*2)/self.n) if self.n != 0 else 1

        # Change buttons's positions and sizes, it need to be justified
        for i in range(self.n-1):
            self.buttons[i].resize(self.btnWidth, self.btnHeight)
            self.buttons[i].move(self.btnWidth*i + self.btnStartWidthPosition, self.btnStartHeightPosition)
        
        # If exist button with self.n - 1 index, then we resize it till the border
        if self.n - 1 >= 0:
            self.buttons[self.n-1].resize(self.windowWidth - self.btnStartWidthPosition*2 - self.btnWidth*(self.n-1) , self.btnHeight)
            self.buttons[self.n-1].move(self.btnWidth*(self.n-1) + self.btnStartWidthPosition, self.btnStartHeightPosition)


