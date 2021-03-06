import sys
import pyperclip
from PyQt5.QtWidgets import QMainWindow, QToolTip,  QApplication, QWidget, QPushButton
from PyQt5 import QtGui
from PyQt5 import QtCore


class drawColors(QWidget):

    # Previous button will be used for changing button's place
    previousButton = None

    # All buttons with color that will be printed into the screen
    buttons = []
    buttonsColor = []

    # Using as stack for deleted buttons to return them back if user want
    deletedButtons = []
    deletedButtonsColor = []

    def __init__(self, colors, n):
        super().__init__()
    
        #self.setStyleSheet('background-color: #000000')
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

            # Parse colors from tuple (x, y, z)
            # Check cases when element is only one digit and add 0's to this number 
            color = ''
            for j in range(3):
                temp =  str(hex(el[j]))[2:].upper() 
                color += temp if len(temp) == 2 else '0' + temp

            btn = QPushButton('   ', self)

            self.buttons.append(btn)
            self.buttonsColor.append('#' + color)

            btn.resize(self.btnWidth, self.btnHeight)
            btn.move(self.btnWidth*i + self.btnStartWidthPosition, self.btnStartHeightPosition)
            btn.setStyleSheet('background-color: #' + color + ';' +
                              'border: 0px') 
            btn.clicked.connect(self.buttonClicked)
            btn.setDefault(False)
            btn.setAutoDefault(False)

        # Add button Undo and connect it to self
        undo = QPushButton('Undo', self)      
        undo.move(self.btnStartWidthPosition, self.btnHeight + self.btnStartHeightPosition * 2) 
        undo.clicked.connect(self.undo)

        # Add button Copy to clipboard
        clip = QPushButton('Copy to clipboard', self) 
     
        clip.move(self.btnStartWidthPosition * 2 + undo.width(), self.btnHeight + self.btnStartHeightPosition * 2)
        clip.clicked.connect(self.copy)

        # Start current QWidget
        self.show()
    

    def copy(self):
        res = ''
        for el in self.buttonsColor:
            res += el + ', '            


        # Copy to clipboard 
        pyperclip.copy(res.strip(', '))   


    def undo(self):
        # If all buttons on the screen do nothing 
        if len(self.deletedButtons) == 0:
            return
          
        # Else get the last one operation
        # lastEl store tuple (el, index)
        # el - QPushButton object, index - from where from self.buttons it was taken
        lastEl = self.deletedButtons.pop()
        self.buttons.insert(lastEl[1], lastEl[0])   
        self.buttonsColor.insert(lastEl[1],self.deletedButtonsColor.pop())

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
        
        if self.previousButton == sender:
            # Delete this button and decrease n
            for i in range(self.n):
                if self.buttons[i] == sender:
                    self.deletedButtons.append((self.buttons.pop(i), i)) 
                    self.deletedButtonsColor.append(self.buttonsColor.pop(i))
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
            self.previousButton = None
        elif self.previousButton == None:
            
            # If self.previousButton have no button then we just make it equal to sender
            self.previousButton = sender

        else:
            
            # Previous index store index to previous button, current index
            # store index to currenter sender in self.buttons array
            prevIndex = 0
            curIndex = 0
 
            # Search in self.buttons indexes to buttons
            for i in range(self.n):
                if self.buttons[i] == self.previousButton:             
                    prevIndex = i
                if self.buttons[i] == sender:
                    curIndex = i

            # If previous button was at right of current, then it goes to left of the current button
            # Otherwise left
            self.buttons.insert(curIndex, self.buttons.pop(prevIndex))
            self.buttonsColor.insert(curIndex, self.buttonsColor.pop(prevIndex))
            
            # Make self.previousButton equals to None
            self.previousButton = None
 
            # Redraw buttons onto the screen
            for i in range(self.n-1):
                self.buttons[i].resize(self.btnWidth, self.btnHeight)
                self.buttons[i].move(self.btnWidth*i + self.btnStartWidthPosition, self.btnStartHeightPosition)
        
            # If exist button with self.n - 1 index, then we resize it till the border
            if self.n - 1 >= 0:
                self.buttons[self.n-1].resize(self.windowWidth - self.btnStartWidthPosition*2 - self.btnWidth*(self.n-1) , self.btnHeight)
                self.buttons[self.n-1].move(self.btnWidth*(self.n-1) + self.btnStartWidthPosition, self.btnStartHeightPosition)
