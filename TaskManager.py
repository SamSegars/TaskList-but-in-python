#!/usr/bin/python
#Imports
import sqlite3
import tkinter 
from tkinter import *
from tkinter import ttk


#Commands
def reload():
    TaskViewer.delete(0,END)
    load()
def load():
    for row in cur.execute('select * from task'):
        clean = [data.rstrip() for data in row]
        listlength=TaskViewer.size()
        for i in clean:
            TaskViewer.insert(listlength,str(listlength + 1)+". "+ i)
def strikethrough():
    st=TaskViewer.curselection()
    st1=TaskViewer.get(st)
    st2 = st1[3:]
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
    cur.execute('delete from task where Task ='+ "'"+ st1[3:] +"'")
    cur.execute('insert into task values' +"('"+ new_text + "')")
    con.commit()

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
    Task = TaskViewer.get(Rm)
    rm= Task[3:]
    con= sqlite3.connect('list.db')
    cur = con.cursor()
    cur.execute('delete from task where Task ='+ "'"+ rm +"'")
    con.commit()
    TaskViewer.delete(Rm)
    reload()
#Window Maker
List = Tk()
List.resizable(False, False)
List.geometry("525x490")
List.title("Task List")

con= sqlite3.connect('list.db')
cur = con.cursor()
cur.execute('create table if not exists Task (task text)')
con.commit

#Widgets
Strike=tkinter.Button(List, text="Strikethrough", command = strikethrough)
NewEntry=Entry(List, width = 50)
addbutton = tkinter.Button(List, text='add', command = Addtolist)
rmbutton = tkinter.Button(List, text= 'remove', command = rmslist)
TaskViewer=Listbox(List, width = 50, height = 25)
scrollbar=Scrollbar(List)
TaskViewer.config(yscrollcommand = scrollbar.set)
scrollbar.config(orient=VERTICAL,command = TaskViewer.yview)
scrollbar.set(20,200)
load()
List.bind('<Return>', enterkey )
List.bind('<Delete>', deletekey)
#grids
Strike.place(x=410, y=230)
addbutton.place(x = 410, y =455)
rmbutton.place(x = 410, y = 200)
TaskViewer.place(x = 0, y  = 0)
scrollbar.place(x=390, y =0, height=452)
NewEntry.place(x = 0, y =460 )
List.mainloop()
