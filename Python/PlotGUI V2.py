#Imports
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import numpy as np
from pyqtgraph.Qt import QtCore,QtGui

import Tkinter
import sys

###############################
# you need to call this ONCE ##
app = QtGui.QApplication([])
###############################


## Define a top-level widget to hold everything
w = QtGui.QWidget()

## Create some widgets to be placed inside
strt = QtGui.QPushButton('Start') #Creates the Start button
#Insert start button action
strt.setCheckable(True)
strt.toggle()
strt.clicked.connect(self.btnstate)

#This is a test to see if button states work correctly
def btnstate(self):
    if self.strt.isChecked():
        print "Gucci"
    else:
        print "Gang"
        

instr = QtGui.QPushButton('Instructions') #Creates the Instructions button
#Insert intructions button action

debug = QtGui.QPushButton('Debug Log') #Creates the Debug Log button
#Inert debug log button action

version = QtGui.QPushButton('Version') #Creates the Version Button
#Insert version button action

#plot = pg.PlotWidget() #Plotting widget, try and change to 3D widget

#3Dplot widget code
plot = gl.GLViewWidget()
plot.show()
#Insert plot actions
xgrid = gl.GLGridItem() #This example creates an X axis grid
plot.addItem(xgrid)
xgrid.rotate(90,0,1,0)
xgrid.scale(0.2,0.1,0.1)


## Create a grid layout to manage the widgets size and position
layout = QtGui.QGridLayout() #Create a grid layout
w.setLayout(layout)

## Add widgets to the layout in their proper positions
layout.addWidget(strt, 0, 0)   #Start Button
layout.addWidget(instr, 1, 0)   #Instructions Button
layout.addWidget(debug, 2, 0)  #Debug Log button
layout.addWidget(version, 3, 0) #Version button
layout.addWidget(plot, 0, 5, 5, 5)  #Adds the plot 


## Display the widget as a new window
w.show()

## Start the Qt event loop
app.exec_()
