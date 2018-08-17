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
            self.x = list()
            self.y = list()
            self.z = list()
            self.initialize()

        def initialize(self):
            QtGui.QWidget.__init__(self)
            self.setMinimumSize(700,500) 
            self.setMaximumSize(700,500)
            self.setWindowTitle('SMART Glove') # Widget name label
            
##### Create the widgets here #####
                # Start button widget
            self.start = QtGui.QPushButton('Start',self)
            self.start.clicked.connect(self.handleStart)

                # Stop button widget
            self.stop = QtGui.QPushButton('Stop',self)
            self.stop.clicked.connect(self.handleStop)
            
                # Update Plot widget
            self.updatePlot = QtGui.QPushButton('Load from CSV',self)
            self.updatePlot.clicked.connect(self.handleUpdate)
            
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

                #Calibration button widget
            self.calibration = QtGui.QPushButton('Glove Calibration',self)
            self.calibration.clicked.connect(self.handleCalibration)

                #Pressure sensor level widget
            self.pressureLevel = QtGui.QPushButton('Set Pressure Level',self)
            self.pressureLevel.clicked.connect(self.handlePressure)
                #Pressure second window that opens
            self.pressureWindow = Pres(self) #Calls the Version window class
            
                # Text widget: Will dispray number of taps
            self.elapsedTime = QtGui.QLineEdit('Time Elapsed: ')
            self.elapsedTime.setDisabled(True)
            
                # 3D Graph Plot Widget
            self.plot = gl.GLViewWidget()
            self.plot.show()
                # Plot actions/test
                
                #Code Reads from CSV, and creates data points
             #Code to collect max values from csv

            #create Axis
            sca = 60    
            n = sca/20    
            self.axis = gl.GLAxisItem()
            self.axis.setSize(x = sca,y = sca,z = sca)
            self.plot.addItem(self.axis)
            
            #X grid
            self.xgrid = gl.GLGridItem()
            self.xgrid.rotate(90, 0, 1, 0)
            self.xgrid.translate(0*n, 10*n, 10*n) # ( X translates X, Y trans Y, Z trans Z 
            self.xgrid.scale(n,n,n) #xGrid scaling
            self.plot.addItem(self.xgrid)
            
            # Y Grid
            self.ygrid = gl.GLGridItem()
            self.ygrid.rotate(90,0, 0, 1)
            self.ygrid.translate(10*n, 10*n, 0*n) # ( Y trans X, X trans Y, Z trans Z)
            self.ygrid.scale(n,n,n) #yGrid scaling
            self.plot.addItem(self.ygrid)

            # Z Grid
            self.zgrid = gl.GLGridItem()
            self.zgrid.rotate(90,1,0,0)
            self.zgrid.translate(10*n, 0*n, 10*n) # (Z trans X, X trans Y, Y trans Z)
            self.zgrid.scale(n,n,n) # zGrid scaling
            self.plot.addItem(self.zgrid)

            self.pts = np.vstack([0,0,0]).transpose()
            self.plt = gl.GLLinePlotItem(pos=self.pts, color=pg.glColor((1,n*1.3)), width=10., antialias=True)
        
            self.plot.addItem(self.plt) #Plots CSV data onto 3D plot
            
##### Layout manager of the widgets #####          
            layout = QtGui.QGridLayout()
            self.setLayout(layout)
            layout.addWidget(self.start, 0, 0, 1, 2)          ## Start button
            layout.addWidget(self.stop, 1, 0, 1, 2)
            layout.addWidget(self.updatePlot, 2, 0, 1, 2)     ## Update Plot button
            layout.addWidget(self.instructions, 3, 0, 1, 2)   ## Instructions button
            layout.addWidget(self.debug, 4, 0, 1 , 2)         ## Debug button
            layout.addWidget(self.version, 5, 0, 1, 2)        ## Version button
            layout.addWidget(self.calibration, 6, 0, 1, 2)    ## Calibration button
            layout.addWidget(self.pressureLevel, 7, 0, 1, 2)       ## Pressure sensor button  
            layout.addWidget(self.elapsedTime, 8, 0, 1, 2)         ## tapData text display
            layout.addWidget(self.plot, 1, 7, 7, 7)           ##3D Plotting
            
            
##### Widget event handling #####
            # This is the event handing for the start button
                             
        def handleStart(self):
            #This will reinitialize the plot and data points    
            self.plot.removeItem(self.xgrid)
            self.plot.removeItem(self.ygrid)
            self.plot.removeItem(self.zgrid)
            self.plot.removeItem(self.axis)
            self.plot.removeItem(self.plt)
            print "hello"
            #Code Reads from CSV, and creates data points
            data1 = list()
            data2 = list()
            data3 = list()
            with open('Test.csv','rU') as csvDataFile:
                csvReader = csv.reader(csvDataFile)
                for row in csvReader:
                    if float(row[0]) == 0:
                        print float(row[0])
                        
                    data1.append(float(row[0]))
                    data2.append(float(row[1]))
                    data3.append(float(row[2]))

            #Code to collect max values from csv
            max1 = max(data1)
            max2 = max(data2)
            max3 = max(data3)
            max4 = max(max1, max2, max3)
            n = 500
            self.x = data1
            self.y = data2
            self.z = data3
            
            #For plot scaling
            maxValue = max4/20
            setX = maxValue
            setY = maxValue
            setZ = maxValue

            #create Axis
            self.axis = gl.GLAxisItem()
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
    
            
            
            
            # Stop button event handling
        def handleStop(self):
            print('Stop')    

            # Update Plot button event handling
        def handleUpdate(self):
            #This will reinitialize the plot and data points    
            self.plot.removeItem(self.xgrid)
            self.plot.removeItem(self.ygrid)
            self.plot.removeItem(self.zgrid)
            self.plot.removeItem(self.axis)
            self.plot.removeItem(self.plt)
            
            #Code Reads from CSV, and creates data points
            data1 = list()
            data2 = list()
            data3 = list()
            with open('Test.csv','rU') as csvDataFile:
                csvReader = csv.reader(csvDataFile)
                for row in csvReader:
                    if float(row[0]) == 0:
                        print float(row[0])
                        
                    data1.append(float(row[0]))
                    data2.append(float(row[1]))
                    data3.append(float(row[2]))
        
            #Code to collect max values from csv
            data1.reverse()
            max1 = max(data1)
            max2 = max(data2)
            max3 = max(data3)
            max4 = max(max1, max2, max3)
            n = 500
            self.x = data1
            self.y = data2
            self.z = data3
            
            #For plot scaling
            maxValue = max4/20
            setX = maxValue
            setY = maxValue
            setZ = maxValue

            #create Axis
            self.axis = gl.GLAxisItem()
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
            
            # Instructions button event handling
        def handleInstructions(self):
            self.instrucWindow.show() #This will open the instructions window
            
                       
            # Debug Log button event handling
        def handleDebug(self):
            print('No debug log coming soon. Next version. Sorry')
            
            # Version button event handling
        def handleVersion(self):
            self.versionWindow.show() # This will open the versions window

            #Calibration button event handling
        def handleCalibration(self):
            print('Calibrating')

            # Pressure Sensor Level event handling
        def handlePressure(self):
            self.pressureWindow.show() #This will open the pressure sensor window

       
############### Addional classes that are used ###############
            
##### Insert Start class for actions here #####
class Start(QtGui.QWidget):
        def __init__(self, parent=None):
            QtGui.QWidget.__init__(self)
##### Insert Update Plot class #####
            
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
            self.text.setPlainText('Version: Alpha 0.1.1')
            self.text.setDisabled(True) # setDiabled = true will disable the text edit
           
##### Pressure class to open new window and diaplay whatever actions that are needed #####
class Pres(QtGui.QWidget):
        def __init__(self,parent = None):
            QtGui.QWidget.__init__(self)
            self.setWindowTitle('Pressure Sensor Level')
            self.setMinimumSize(225,225)
            self.setMaximumSize(225,225)

            #Within the window that opens
            self.text = QtGui.QPlainTextEdit(self)
            self.text.setPlainText('Set the Pressure Sensor Level \n1=Low, 2=Middle, 3=High')
            self.text.setDisabled(True)
            
            self.level1 = QtGui.QPushButton('Level 1', self)
            self.level1.clicked.connect(self.handleLevelOne)

            self.level2 = QtGui.QPushButton('Level 2', self)
            self.level2.clicked.connect(self.handleLevelTwo)

            self.level3 = QtGui.QPushButton('Level 3',self)
            self.level3.clicked.connect(self.handleLevelThree)
                
            # Pres Widget layout
            layout = QtGui.QGridLayout()
            self.setLayout(layout)
            layout.addWidget(self.text,0, 0, 5, 2)
            layout.addWidget(self.level1, 2, 0, 1, 2)
            layout.addWidget(self.level2, 3, 0, 1, 2)
            layout.addWidget(self.level3, 4, 0, 1, 2)
            
            # Pressure Level 1 event handling
        def handleLevelOne(self):
                print('test')
            # Pressure Level 2 event handling
        def handleLevelTwo(self):
                print('test2')
            # Pressure Level 3 event handling
        def handleLevelThree(self):
                print('test3')
            
############### Initation code ###############
if __name__ == '__main__': 
    import sys

    app = QtGui.QApplication(sys.argv)
 
    w = Window()
    w.show()
    sys.exit(app.exec_())

 
