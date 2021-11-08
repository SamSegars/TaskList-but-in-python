#!/usr/bin/python
#Imports
import sqlite3
import tkinter 
from tkinter import *
from tkinter import ttk


#Commands
def reload():
    TaskViewer.delete(0,END)
    Rowids.delete(0,END)
    load()

def load():
    for row in cur.execute('select rowid from task order by rowid'):
        listlength=Rowids.size()
        for i in row:
            Rowids.insert(listlength,i)
    for row in cur.execute('select * from task order by rowid'):
        clean = [data.rstrip() for data in row]
        listlength=TaskViewer.size()
        for i in clean:
            TaskViewer.insert(listlength,str(listlength + 1)+". "+ i)

def strikethrough():
    st=TaskViewer.curselection()
    st1=TaskViewer.get(st)
    st2 = st1[3:]
    rowid=Rowids.get(st)
    Numb = st1[0:3]
    i = 0
    new_text = ''
    while i < len(st2):
        new_text = new_text + (st2[i] + u'\u0336')
        i = i + 1
    TaskViewer.delete(st)
    TaskViewer.insert(st,Numb + new_text)
    con= sqlite3.connect('list.db')
    cur = con.cursor()
    cur.execute('Update Task set Task = '+"'"+ new_text + "'" +' where rowid =' + "'" + str(rowid) + "'")
    con.commit()
    reload()

def SendtoBottom():
    st=TaskViewer.curselection()
    st1=TaskViewer.get(st)
    st2 = st1[3:]
    Rowid=Rowids.get(st)
    Numb = st1[0:3]
    i = 0
    new_text = ''
    while i < len(st2):
        new_text = new_text + (st2[i] + u'\u0336')
        i = i + 1
    TaskViewer.insert(st,Numb + new_text)
    listlength=TaskViewer.size()
    TaskViewer.insert(listlength+1,str(listlength + 1) + ". " + st2)
    con= sqlite3.connect('list.db')
    cur = con.cursor()
    cur.execute('Update Task set Task = '+"'"+ new_text + "'" +' where rowid =' +  str(Rowid))
    cur.execute('insert into task values' + "('"+ st2 + "')")
    con.commit()
    reload()
     
def enterkey(l):
    Addtolist()

def deletekey(a):
    rmslist()
    
def Addtolist():
    Task = NewEntry.get()
    listlength=TaskViewer.size()
    TaskViewer.insert(listlength+1,str(listlength + 1)+ ". " + Task)
    con= sqlite3.connect('list.db')
    cur = con.cursor()
    cur.execute('insert into task values' +"('"+ Task+ "')")
    con.commit()
    reload()

def rmslist():
    Rm = TaskViewer.curselection()
    Task = Rowids.get(Rm)
    con= sqlite3.connect('list.db')
    cur = con.cursor()
    cur.execute('delete from task where rowid ='+ str(Task))
    con.commit()
    TaskViewer.delete(Rm)
    reload()

#Window Maker
List = Tk()
List.resizable(False, False)
List.geometry("525x490")
List.title("Task List")

#Data Manager
con= sqlite3.connect('list.db')
cur = con.cursor()
cur.execute('create table if not exists Task (task text)')
con.commit

#Widgets
Strike=tkinter.Button(List, text="Complete", command = strikethrough)
MTB=tkinter.Button(List, text='Duplicate', command = SendtoBottom)
NewEntry=Entry(List, width = 50)
addbutton = tkinter.Button(List, text='Add', command = Addtolist)
rmbutton = tkinter.Button(List, text= 'Remove', command = rmslist)
TaskViewer=Listbox(List, width = 50, height = 25)
scrollbar=Scrollbar(List)
TaskViewer.config(yscrollcommand = scrollbar.set)
scrollbar.config(orient=VERTICAL,command = TaskViewer.yview)
scrollbar.set(20,200)
Rowids=Listbox(List)
#Load Data
load()
#Key Bindings
List.bind('<Return>', enterkey )
List.bind('<Delete>', deletekey)
#grids
rmbutton.place(x=410, y=230)
MTB.place(x=410, y=170)
addbutton.place(x = 410, y =455)
Strike.place(x = 410, y = 200)
TaskViewer.place(x = 0, y  = 0)
scrollbar.place(x=390, y =0, height=452)
NewEntry.place(x = 0, y =460 )
List.mainloop()
