#!/usr/bin/python
#Imports
import tkinter
from tkinter import *
from tkinter.ttk import *
from pathlib import Path
import getpass
from time import strftime

# Varaibles

username= getpass.getuser()
listfile="/home/"+ username + "/.todo/.list"
#Commands
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
count = 1

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
addbutton.grid(row = 1, column =3)
rmbutton.grid(row = 0, column = 3)
TaskViewer.grid(row = 0, column  = 0, sticky=NSEW)
scrollbar.grid(row=0, column =2, sticky=NS)
NewEntry.grid(row = 1, column = 0, sticky=EW )
List.grid_columnconfigure(0,weight=1)
List.grid_columnconfigure(1,weight=1)
List.grid_columnconfigure(2,weight=1)
List.grid_columnconfigure(3,weight=1)
List.grid_rowconfigure(0,weight=1)
List.grid_rowconfigure(1,weight=1)
List.mainloop()
