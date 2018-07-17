import matplotlib
matplotlib.use('TkAgg')
import csv
from mpl_toolkits.mplot3d import  axes3d,Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib.ticker import LinearLocator, FixedLocator, FormatStrFormatter

import Tkinter
import sys

class E(Tkinter.Tk):
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.x = None
        self.y = None
        self.z = None


        self.protocol("WM_DELETE_WINDOW", self.dest)
        self.main()

    def intialize(self):
        self.grid
        
    def main(self):
        self.fig = Figure(figsize=(5,5))

        self.frame = Tkinter.Frame(self)
        self.frame.pack(padx=15,pady=15)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)

        self.canvas.get_tk_widget().pack(side='top', fill='both')


        self.canvas._tkcanvas.pack(side='top', fill='both', expand=1)

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

        self.x = data1
        self.y = data2
        self.z = data3
        
        self.plotValues(len(data3) - 1)
        
        self.label = Tkinter.Label(self, text="Time to Complete")
        self.label.pack()
        self.scale = Tkinter.Scale(self,from_=0,to=len(data3)-1,length=600,tickinterval=5,orient='horizontal',command=self.sliderValue)
        self.scale.pack()
##        self.btn = Tkinter.Button(self,text='button',command=self.alt)
##        self.btn.pack()

    def sliderValue(self,event):
        self.plotValues(int(event))

    def dest(self):
        self.destroy()
        sys.exit()

    def plotValues(self,numValues):
        ax = Axes3D(self.fig)
        canvas = self.canvas
        data1 = self.x
        data2 = self.y
        data3 = self.z
        t = ax.plot(data1[0:numValues], data2[0:numValues], data3[0:numValues])
        canvas.draw()



if __name__ == "__main__":
    app = E(None)
    app.title('Embedding in TK')
    app.mainloop()
