# -*- coding: utf-8 -*-
"""
Demonstrate use of GLLinePlotItem to draw cross-sections of a surface.

"""
## Add path to library (just for examples; you do not need this)
#import initExample

from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import pyqtgraph as pg
import numpy as np
import csv

app = QtGui.QApplication([])
w = gl.GLViewWidget()
w.opts['distance'] = 40
w.show()
w.setWindowTitle('pyqtgraph example: GLLinePlotItem')


#Note: the rotations and translate values presented right now
# Make the first point land at (0,0,0)
#Goal: To make the axis scale as we continue plotting

#def fn(x, y):
#    return np.cos((x**2 + y**2)**0.5)

data1=list()
data2=list()
data3=list()
with open('Test.csv','rU') as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    for row in csvReader:
        if float(row[0]) == 0:
            print float(row[0])
            
        data1.append(float(row[0]))
        data2.append(float(row[1]))
        data3.append(float(row[2]))
#Test code to collec the max value of CSV        
max1 = max(data1)
max2 = max(data2)
max3 = max(data3)
max4 = max(max1,max2,max3)
n = 500
x = data1
y = data2
z = data3


maxValue = max4/20 #This value will be taken from a max value in the CSV file
#the /20 is not going to be the case for all values that we find

setX = maxValue
setY = maxValue
setZ = maxValue

axis = gl.GLAxisItem()
axis.setSize(x = max4,y = max4,z = max4)
w.addItem(axis)

#X Grid adjustments
xgrid = gl.GLGridItem()
xgrid.rotate(90, 0, 1, 0)
xgrid.translate(0*setX, 10*setY, 10*setZ) # ( X translates X, Y trans Y, Z trans Z 
xgrid.scale(setZ,setX,setY) #xGrid scaling
w.addItem(xgrid)

w.renderText(100,100,100,'test') #does not work

#Y grid adjustments
ygrid = gl.GLGridItem()
ygrid.rotate(90,0, 0, 1)
ygrid.translate(10*setY, 10*setX, 0*setZ) # ( Y trans X, X trans Y, Z trans Z)
ygrid.scale(setX,setY,setZ) #yGrid scaling
w.addItem(ygrid)

#Z grid adjustments
zgrid = gl.GLGridItem()
zgrid.rotate(90,1,0,0)
zgrid.translate(10*setZ, 0*setX, 10*setY) # (Z trans X, X trans Y, Y trans Z)
zgrid.scale(setY,setZ,setX) # zGrid scaling
w.addItem(zgrid)

pts = np.vstack([x,y,z]).transpose()
plt = gl.GLLinePlotItem(pos=pts, color=pg.glColor((1,n*1.3)), width=100., antialias=True)

w.addItem(plt)
##for i in range(n):
##    yi = np.array([y[i]]*100)
##    d = (x**2 + yi**2)**0.5
##    z = 10 * np.cos(d) / (d+1)
##    pts = np.vstack([x,yi,z]).transpose()
##    plt = gl.GLLinePlotItem(pos=pts, color=pg.glColor((i,n*1.3)), width=(i+1)/10., antialias=True)
##    w.addItem(plt)
    


## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
