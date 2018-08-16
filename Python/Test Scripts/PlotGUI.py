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

#pyqtgraph impot
#from PyQt4 import QtGui 
#import pyqtgraph as pg

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
 #Kevin C code

        #Start Button: Use a start button to start a connection to the bluetooth devince
        #and then start the program?
        self.start = Tkinter.Button(self, text = "Start                  ", command = self.start)
        self.start.pack()
        self.start.place(x = 0, y = 0)
        #Instructions Button
        self.button=Tkinter.Button(self, text="Instructions      ", command = self.instructions)
        self.button.pack()
        self.button.place(x = 0, y = 25)  

        #Debug Log button
        self.debugLog = Tkinter.Button(self, text = "Debugging Log", command = self.dbugLog)
        self.debugLog.pack()
        self.debugLog.place(x = 0, y = 50)

        #Version Button: Just to show the version of this GUI
        self.versionButton = Tkinter.Button(self, text = "Version             ", command = self.version)
        self.versionButton.pack()
        self.versionButton.place(x = 0, y = 75)

        
##        self.btn = Tkinter.Button(self,text='button',command=self.alt)
##        self.btn.pack()


#justify = defines how to align multiple lines of text

    def start(self): #Start code
        t = Tkinter.Toplevel(self)
        t.wm_title("Start") #this will be changed to not open a tab, but start an action
        l = Tkinter.Label(t,justify = "left", text = "Please connect Smart Glove...")
        l.pack(side = "top", fill = "both", expand = True, padx = 1, pady = 1)
        
    def instructions(self): #Insturctions code
        t = Tkinter.Toplevel(self)
        t.wm_title("Instructions")
        l = Tkinter.Label(t,justify = "left", text = "Welcome to the SMART Glove! \nHere are the intructions to begin recording data: :\n\n 1)Press 'start' on this application to pair your Smart Glove to the computer via Bluetooth. \n The program will prompt you when the glove successfully connects. \n\n2)...add on as we go" ) #This is where we can add text
        l.pack(side = "top", fill = "both", expand = True, padx = 1, pady = 1)


    def dbugLog(self): #Debug log code
        t = Tkinter.Toplevel(self)
        t.wm_title("Debug Log")
        l = Tkinter.Label(t,justify = "left", text = "Logs") #This is where the error logs will be printed. 
        l.pack(side = "top", fill = "both", expand = True, padx = 1, pady = 1)
 

    def version(self): #Simple version code
        t = Tkinter.Toplevel(self)
        t.wm_title("Version")
        l = Tkinter.Label(t,justify = "left",text = "Version: Apha 0.1.0") #Just to show what version we are currently working on
        l.pack(side = "top", fill = "both", expand = True, padx = 1, pady = 1)

        
    def sliderValue(self,event):
        self.plotValues(int(event))

    def dest(self):
        self.destroy()
        sys.exit()

    #This is the plotValues method using matplotlib
    def plotValues(self,numValues):
        ax = Axes3D(self.fig)
        canvas = self.canvas
        data1 = self.x
        data2 = self.y
        data3 = self.z
        t = ax.plot(data1[0:numValues], data2[0:numValues], data3[0:numValues])
        ax.set_xlabel('Left/Right Distance (m)', fontsize = 8, rotation = 0) #Labels x-axis
        ax.set_ylabel('Forward/Back Distance (m)',fontsize = 8, rotation = 0) #Labels y-axis
        ax.set_zlabel('Height Distance (m)',fontsize = 8, rotation = 0) #Labels z-axis
        canvas.draw()



if __name__ == "__main__":
    app = E(None)
    app.title('SMART Glove Plotting')
    app.mainloop()
