from PyQt4 import QtGui # The example applies equally well to PySide
import pyqtgraph as pg

##ALways start by initializing Qt (only once per application)
app = QtGui.QApplication([])

##Define a top-level widget to hold everything
w = QtGui.QWidget()

##Create some widgets to be placed inside
btn = QtGui.QPushButton('Hoe')
text = QtGui.QLineEdit('Enter Sext')
listw = QtGui.QListWidget()
plot = pg.PlotWidget()

##Create a grid layout to manage the widgets size and position
layout = QtGui.QGridLayout()
w.setLayout(layout)

##Add widgets to the layout in their proper positions
layout.addWidget(btn,0,0) #Button
layout.addWidget(text,1,0) #Text
layout.addWidget(listw,2,0) #List widget
layout.addWidget(plot,0,1,3,1) #Plot goes on right side, spanning 3 row


##Display the widget as a new window
w.show()

##Start the Qt event Loop
app.exec_()

#Notes: PyOpenGL is not neccessary for our purpose. It is for 3D GRAPHICS, not
#3D Plotting 

