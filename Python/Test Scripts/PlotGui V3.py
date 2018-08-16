################################################################################
# Kevin Chung                                                                  #
#                                                                              #
# Capstone Project: SMART Glove                                                #
#                                                                              #
# Description: We are to create a smart glove that track                       #
# Postion, speed, time, and taps of a user in use. The intended use            #
# of the glove is for rehabilitation of stoke patients.                        #
# This python code is the UI that would collect data, and plot the movement of #
# The patient on a 3D plot, and display important data for the researcher.     #
################################################################################

import pyqtgraph as pg
import pyqtgraph.opengl as gl
import numpy as np
from pyqtgraph.Qt import QtCore,QtGui
import csv
import Tkinter

############### Main window class: What holds all the widgets ###############
class Window(QtGui.QWidget):
        def __init__(self, parent=None): 
            QtGui.QWidget.__init__(self)
            self.setMinimumSize(700,500) 
            self.setMaximumSize(700,500)
            self.setWindowTitle('SMART Glove') # Widget name label
            
##### Create the widgets here #####
                # Start button widget
            self.start = QtGui.QPushButton('Start',self)
            self.start.clicked.connect(self.handleStart)

                # Instructions button widget
            self.instructions = QtGui.QPushButton('Instructions')
            self.instructions.clicked.connect(self.handleInstructions)
                #Instructions second window that opens
            self.instrucWindow = Instruc(self) #Calls the instructions window class

                # Debug Log Button Widget
            self.debug = QtGui.QPushButton('Debug Log',self)
            self.debug.clicked.connect(self.handleDebug)

                # Version button widget
            self.version = QtGui.QPushButton('Version',self)
            self.version.clicked.connect(self.handleVersion)
                # Versions second window that opens
            self.versionWindow = Vers(self) #Calls the Version window class

                # Text widget: Will dispray number of taps
            self.tapData = QtGui.QLineEdit('Tap Data:')
            #self.tapData.setMinimumSize(1,1)
            self.tapData.setDisabled(True)
            
                # 3D Graph Plot Widget
            self.plot = gl.GLViewWidget()
            self.plot.show()
                # Plot actions/test
                
                #Code Reads from CSV, and creates data points
            data1 = list()
            data2 = list()
            data3 = list()
##            with open('Test.csv','rU') as csvDataFile:
##                csvReader = csv.reader(csvDataFile)
##                for row in csvReader:
##                    if float(row[0]) == 0:
##                        print float(row[0])
##                        
##                    data1.append(float(row[0]))
##                    data2.append(float(row[1]))
##                    data3.append(float(row[2]))
##
##            #Code to collect max values from csv
##            max1 = max(data1)
##            max2 = max(data2)
##            max3 = max(data3)
##            max4 = max(max1, max2, max3)
##            n = 500
##            self.x = data1
##            self.y = data2
##            self.z = data3
##            
            #For plot scaling
            n = 500
            self.x = data1.append(0)
            self.y = data2.append(0)
            self.z = data3.append(0)
            max4 = 40
            maxValue = max4/20
            setX = maxValue
            setY = maxValue
            setZ = maxValue

            #create Axis
            self.axis = gl.GLAxisItem()
##            self.axis.setSize(x = max4,y = max4,z = max4)
            self.axis.setSize(x = max4,y = max4,z = max4)
            self.plot.addItem(self.axis)
            
            #X grid
            self.xgrid = gl.GLGridItem()
            self.xgrid.rotate(90, 0, 1, 0)
            self.xgrid.translate(0*setX, 10*setY, 10*setZ) # ( X translates X, Y trans Y, Z trans Z 
            self.xgrid.scale(setZ,setX,setY) #xGrid scaling
            self.plot.addItem(self.xgrid)
            
            # Y Grid
            self.ygrid = gl.GLGridItem()
            self.ygrid.rotate(90,0, 0, 1)
            self.ygrid.translate(10*setY, 10*setX, 0*setZ) # ( Y trans X, X trans Y, Z trans Z)
            self.ygrid.scale(setX,setY,setZ) #yGrid scaling
            self.plot.addItem(self.ygrid)

            # Z Grid
            self.zgrid = gl.GLGridItem()
            self.zgrid.rotate(90,1,0,0)
            self.zgrid.translate(10*setZ, 0*setX, 10*setY) # (Z trans X, X trans Y, Y trans Z)
            self.zgrid.scale(setY,setZ,setX) # zGrid scaling
            self.plot.addItem(self.zgrid)

            self.pts = np.vstack([self.x,self.y,self.z]).transpose()
            self.plt = gl.GLLinePlotItem(pos=self.pts, color=pg.glColor((1,n*1.3)), width=10., antialias=True)
        
            self.plot.addItem(self.plt) #Plots CSV data onto 3D plot
            
##### Layout manager of the widgets #####          
            layout = QtGui.QGridLayout()
            self.setLayout(layout)
            layout.addWidget(self.start, 0, 0, 1, 2)          ## Start button
            layout.addWidget(self.instructions, 1 , 0, 1, 2)  ## Instructions button
            layout.addWidget(self.debug, 2, 0, 1 , 2)         ## Debug button
            layout.addWidget(self.version, 3, 0, 1, 2)        ## Version button
            layout.addWidget(self.tapData,4, 0, 1, 2)         ## tapData text display
            layout.addWidget(self.plot, 0, 6, 6, 6)           ##3D Plotting
            
            
##### Widget event handling #####
            # This is the event handing for the start button
        def handleStart(self): 
            print('Welcome to the SMART Glove')
            print('Plz connect Glove via Bluetooth')
     
            # I nstructions button event handling
        def handleInstructions(self):
            self.instrucWindow.show() #This will open the instructions window
            
                       
            # Debug Log button event handling
        def handleDebug(self):
            print('This is the debug log')
            
            # Version button event handling
        def handleVersion(self):
            self.versionWindow.show() # This will open the versions window
            
############### Addional classes that are used ###############
            
##### Insert Start class for actions here #####
            
##### Instructions class to open new window and display instructions #####           
class Instruc(QtGui.QWidget):
        def __init__(self, parent=None):
            QtGui.QWidget.__init__(self)
            self.setWindowTitle('SMART Glove: Instructions')
            self.setMinimumSize(250,150)
            self.setMaximumSize(250,150) # Adjust window size as more instructions are added
            
                # The contents within the opened window 
            self.text = QtGui.QPlainTextEdit(self)
            self.text.setPlainText("Welcome to the SMART Glove! \nHere are the intructions to begin recording data: \n\n1)Press 'start' on this application to pair your Smart Glove to the computer via Bluetooth. \n The program will prompt you when the glove successfully connects. \n\n2)...add on as we go")
            self.text.setDisabled(True) # setDisabld = true will disable text edit 
    
##### Insert Debug Log class here if it is going to be used #####
            
##### Version class to open new window and display current version of application #####
class Vers(QtGui.QWidget):
        def __init__(self,parent=None):
            QtGui.QWidget.__init__(self)
            self.setWindowTitle('SMART Glove: Version')
            self.setMinimumSize(225,20)
            self.setMaximumSize(225,20)
            
                # What is within the window that opens
            self.text = QtGui.QPlainTextEdit(self) 
            self.text.setPlainText('Version: Alpha 0.1.0')
            self.text.setDisabled(True) # setDiabled = true will disable the text edit
           
                
############### Initation code ###############
if __name__ == '__main__': 
    import sys

    app = QtGui.QApplication(sys.argv)
 
    w = Window()
    w.show()
    sys.exit(app.exec_())

        
