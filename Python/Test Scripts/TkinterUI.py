import matplotlib
matplotlib.use("TkAgg")

import Tkinter
from Tkinter import *

class VisualizationApp(Tkinter.Tk):
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid()

        self.entry = Tkinter.Entry(self)
        self.entry.grid(column=0,row=0,sticky='EW')
        self.entry.bind("<Return>", self.OnPressEnter)

        button = Tkinter.Button(self,text="Click me!",command=self.OnButtonClick)
        button.grid(column=1,row=0)

        label = Tkinter.Label(self,anchor="w",fg="white",bg="blue")
        label.grid(column=0,row=1,columnspan=2,sticky='EW')
        self.grid_columnconfigure(0,weight=1)
        self.resizable(True,True)

    def OnButtonClick(self):
        print "Button Pressed"

    def OnPressEnter(self,event):
        print "You pressed enter!"

if __name__ == "__main__":
    app = VisualizationApp(None)
    app.title('Picture Perfect')
    app.mainloop()
        
