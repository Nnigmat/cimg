import sys
from PyQt5.QtWidgets import QToolTip,  QApplication, QWidget, QPushButton
from PyQt5 import QtGui

def drawColors(colors, n):
   btnWidth = 50
   btnHeight = 600
   btnStartWidthPosition = 25
   btnStartHeightPosition = 25
   windowWidth = btnStartWidthPosition*2 + btnWidth * n
   windowHeight = btnHeight + btnStartHeightPosition*2

   app = QApplication(sys.argv)
   w = QWidget()
   w.resize(windowWidth, windowHeight)
   w.move(300, 300)
   w.setWindowTitle('Cimg')

   # QToolTip.setFont(QtGui.QFont('SansSerif', 10))
   # btn = QPushButton('   ', w)
   # btn.setToolTip('This is a dsakjflslkjf')
   # btn.resize(btnWidth, btnHeight)
   # btn.setStyleSheet('background-color: #DDFFDD')
      
   for i in range(n):
       el = colors[i]
       color = '' + str(hex(el[0]))[2:].upper() + str(hex(el[1]))[2:].upper() + str(hex(el[2]))[2:].upper() 
       btn = QPushButton('   ', w)
       btn.resize(btnWidth, btnHeight)
       btn.move(btnWidth*i + btnStartWidthPosition, btnStartHeightPosition)
       btn.setStyleSheet('background-color: #' + color) 
   w.show()
   sys.exit(app.exec_())
