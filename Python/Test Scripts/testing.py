
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

#Scan the CSV file, and set the highest Value to X, Y and D to scale the plot
#The XYZ values will scale equally
maxValue = 10 #This value will be taken from a max value in the CSV file
setX = maxValue
setY = maxValue
setZ = maxValue

#test = gl.GLAxisItem()
#test.setSize(x = setX,y = setY,z = setZ)
#w.addItem(test)

#X Grid adjustments
xgrid = gl.GLGridItem()
xgrid.rotate(90, 0, 1, 0)
xgrid.translate(0*setX, 10*setY, 10*setZ) # ( X translates X, Y trans Y, Z trans Z 
xgrid.scale(setZ,setX,setY) #xGrid scaling

w.addItem(xgrid)

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


#Note: the rotations and translate values presented right now
# Make the first point land at (0,0,0)
#Goal: To make the axis scale as we continue plotting

#def fn(x, y):
#    return np.cos((x**2 + y**2)**0.5)

#data1=list()
#data2=list()
#data3=list()
#with open('Test.csv','rU') as csvDataFile:
#    csvReader = csv.reader(csvDataFile)
#    for row in csvReader:
#        if float(row[0]) == 0:
#            print float(row[0])
            
#        data1.append(float(row[0]))
#        data2.append(float(row[1]))
#        data3.append(float(row[2]))

#n = 500
#x = data1
#y = data2
#z = data3
#pts = np.vstack([x,y,z]).transpose()
#plt = gl.GLLinePlotItem(pos=pts, color=pg.glColor((1,n*1.3)), width=100., antialias=True)
#w.addItem(plt)



## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

