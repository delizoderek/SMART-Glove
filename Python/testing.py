import pyqtgraph as pg
import pyqtgraph.opengl as gl
import numpy as np
from pyqtgraph.Qt import QtCore,QtGui

import Tkinter

class Window(QtGui.QWidget):
        def __init__(self):
            QtGui.QWidget.__init__(self)
#Create the widgets here
            #Start button widget
            self.start = QtGui.QPushButton('Start',self)
            self.start.clicked.connect(self.handleStart)

            #Instructions button widget
            self.instructions = QtGui.QPushButton('Instructions',self)
            self.instructions.clicked.connect(self.handleInstructions)

            #Debug Log Button Widget
            self.debug = QtGui.QPushButton('Debug Log',self)
            self.debug.clicked.connect(self.handleDebug)

            #Version button widget
            self.version = QtGui.QPushButton('Version',self)
            self.version.clicked.connect(self.handleVersion)
                                              
#Layout manager of the widgets           
            layout = QtGui.QGridLayout()
            self.setLayout(layout)
            layout.addWidget(self.start, 0, 0)          ##Start button
            layout.addWidget(self.instructions, 1 , 0)  ## Instructions button
            layout.addWidget(self.debug, 2, 0)          ##Debug button
            layout.addWidget(self.version, 3, 0)        ##Version button
            
            
#Widget event handling
        #This is the event handing for the start button
        #The start button will be pressed and then the connection,
        #and starting of the program will be here
        def handleStart(self): 
            print('Welcome to the SMART Glove')
            print('Plz connect Glove via Bluetooth')
     
        #Instructions button event handling
        def handleInstructions(self):
            print('Here are some steps to begin')
            print('Gucci Gang')

        #Debug Log button event handling
        def handleDebug(self):
            print('This is the debug log')

        def handleVersion(self):
            print('SMART GLOVE Version: Alpha 0.1.0')
    

if __name__ == '__main__': #Inititation code
    import sys

    app = QtGui.QApplication(sys.argv)
 
    w = Window()
    w.show()
    sys.exit(app.exec_())

        
