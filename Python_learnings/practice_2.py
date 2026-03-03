# 1) turtle Module
"""
# import turtle
from turtle import *
# from turtle import forward, right, done
# import time

forward(150)
right(250)
# turtle.circle(75) # 75 is the radius
circle(75) # 75 is the radius
forward(150)

# time.sleep(4)
done()


import shelve
for obj in dir(shelve.Shelf):
    if obj[0] != '_':
        print(obj)

shelve.Shelf

import time

try:
    import tkinter
except ImportError:
    import Tkinter as tkinter

mainWindow = tkinter.Tk()
mainWindow.title("Hello World")
mainWindow.geometry('640x400+0+400')

label = tkinter.Label(mainWindow, text='Hello World')
label.pack(side='top')
canvas = tkinter.Canvas(mainWindow, relief='raised', borderwidth = 1)
canvas.pack(side='top')
# canvas.pack(side='left', fill=tkinter.BOTH, expand=True)

button1 = tkinter.Button(mainWindow, text="button1")
button2 = tkinter.Button(mainWindow, text="button2")
button3 = tkinter.Button(mainWindow, text="button3")
button2.pack(side='top', anchor='n')
button1.pack(side='top', anchor='s')
button3.pack(side='top', anchor='e')

mainWindow.mainloop()
"""

import os
try:
    import tkinter
except ImportError:
    import Tkinter as tkinter

mainWindow = tkinter.Tk()
mainWindow.title("Grid Demo")
mainWindow.geometry('640x400-0-400')

label = tkinter.Label(mainWindow, text="Tkinter Grid Demo")
label.grid(row=0, column=0, columnspan=3)

mainWindow.columnconfigure(0, weight=1)
mainWindow.columnconfigure(1, weight=1)
mainWindow.columnconfigure(2, weight=3)
mainWindow.columnconfigure(3, weight=3)
mainWindow.columnconfigure(4, weight=3)

mainWindow.rowconfigure(0, weight=1)
mainWindow.rowconfigure(1, weight=10)
mainWindow.rowconfigure(2, weight=1)
mainWindow.rowconfigure(3, weight=3)
mainWindow.rowconfigure(4, weight=3)

fileList= tkinter.Listbox(mainWindow)
fileList.grid(row=1, column=0, sticky='nsew', rowspan=2)
fileList.config(border=2, relief='sunken')
for zone in os.listdir('practices'): #use any relative folder of project
    fileList.insert(tkinter.END, zone)

listScroll = tkinter.Scrollbar(mainWindow, orient=tkinter.VERTICAL, command=fileList.yview)
listScroll.grid(row=1, column=1, sticky='nsw', rowspan=2)
fileList['yscrollcommand'] = listScroll.set

optionFrame=tkinter.LabelFrame(mainWindow, text="File Details")
optionFrame.grid(row=1, column=2, sticky='ne')

rbValue=tkinter.IntVar()
rbValue.set(3)

radio1=tkinter.Radiobutton(optionFrame, text='Filename', value=1, variable=rbValue)
radio2=tkinter.Radiobutton(optionFrame, text='Path', value=2, variable=rbValue)
radio3=tkinter.Radiobutton(optionFrame, text='Timestamp', value=3, variable=rbValue)
radio1.grid(row=0, column=0, sticky='w')
radio2.grid(row=1, column=0, sticky='w')
radio3.grid(row=2, column=0, sticky='w')

mainWindow.mainloop()
print(rbValue.get())