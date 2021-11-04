#!/usr/bin/python
#Imports
import sqlite3
import tkinter
import re
from tkinter import *
from tkinter import ttk
from pathlib import Path
import getpass
from time import strftime

# Varaibles

username= getpass.getuser()
listfile="/home/"+ username + "/.todo/.list"
#Commands
def strikethrough():
    st=TaskViewer.curselection()
    st1=TaskViewer.get(st)
    i = 0
    new_text = ''
    while i < len(st1):
        new_text = new_text + (st1[i] + u'\u0336')
        i = i + 1
    TaskViewer.delete(st)
    TaskViewer.insert(st,new_text)
def autosave():
    with open(Path(listfile),"w") as f:
        for i in TaskViewer.get(0, END):
            f.write( i+"\n")
def enterkey(l):
    Task = NewEntry.get()
    listlength=TaskViewer.size()
    TaskViewer.insert(listlength+1,str(listlength + 1)+ ". " + Task)
    with open(listfile,"a") as f:
        f.write(str(listlength + 1) + ". "+Task+"\n")
def deletekey(a):
    Rm = TaskViewer.curselection()
    TaskViewer.delete(Rm)
    autosave()
def Addtolist():
    Task = NewEntry.get()
    listlength=TaskViewer.size()
    TaskViewer.insert(listlength+1,str(listlength + 1)+ ". " + Task)
    with open(listfile,"a") as f:
        f.write(str(listlength + 1) + ". "+Task+"\n")
def rmslist():
    Rm = TaskViewer.curselection()
    TaskViewer.delete(Rm)
    autosave()
#Window Maker
List = Tk()
List.resizable(False, False)
List.title("Task List")
myfile = Path(listfile)
myfile.touch(exist_ok=True)
wheight= List.winfo_screenheight()
wwidth= List.winfo_screenwidth()

#File Manager
File = open(Path(listfile),"r")
NewFile = File.readlines()
File.close()
NewFile= [data.rstrip() for data in NewFile]
#Widgets
Strike=tkinter.Button(List, text="Strikethrough", command = strikethrough)
NewEntry=Entry(List, width = 50)
addbutton = tkinter.Button(List, text='add', command = Addtolist)
rmbutton = tkinter.Button(List, text= 'remove', command = rmslist)
TaskViewer=Listbox(List, width = 50, height = 25)
scrollbar=Scrollbar(List)
TaskViewer.config(yscrollcommand = scrollbar.set)
scrollbar.config(orient=VERTICAL,command = TaskViewer.yview)

for item in NewFile:
    listlength=TaskViewer.size()
    TaskViewer.insert(listlength,item)
List.bind('<Return>', enterkey )
List.bind('<Delete>', deletekey)
#grids
Strike.grid(row=0, column=1)
addbutton.grid(row = 2, column =1)
rmbutton.grid(row = 0, column = 0)
TaskViewer.grid(row = 1, column  = 0, sticky=NSEW)
scrollbar.grid(row=1, column =1, sticky=NS)
NewEntry.grid(row = 2, column = 0, sticky=EW )
List.mainloop()
